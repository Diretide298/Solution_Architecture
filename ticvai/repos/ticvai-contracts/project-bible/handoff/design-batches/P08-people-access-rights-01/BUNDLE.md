# P08-people-access-rights-01 — P08 · People & Access Rights (1 of 2)

**10 screens · 47 operations · 41 schemas · 12 permissions**

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

- **Every control that can be refused must be gated.** 12 permissions apply here:
  `ANNOUNCEMENT_PUBLISH, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW, PERMISSION_VIEW, ROLE_MANAGE, SCOPE_VIEW, SESSION_FORCE_LOGOUT, USER_MANAGE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
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

### Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue)

Venue operations is everything that happens after a sale and inside the gates. A guest's ticket is one virtual ticket with interchangeable media (QR, dynamic QR, RFID wristband, NFC, Face Pass or Face Tag); at an access point a scanner (P07, or the scan function inside the Staff App P06) validates the media against the admission profile and the guest admission policy, offline if it must, and every deny carries a reason and a next action. The back office (Venue Management P08) configures that estate: the venue topology (venue, park, zone, attraction, access point, gate and lane, device placement), admission profiles and rules (entry, exit, re-entry, anti-passback, validity, crossover, companions), credential security (dynamic QR, device binding, beacons), biometrics, gate modes, and the live operations, fraud and monitoring views. Accreditation (P08 setup and review, P11 web portal for applicants, web first) takes an applicant from a configurable form through document checks, OCR, duplicate blocking and multi-level approval to a credential with zone rights. Resources and capacity manage bookable resources (rooms, vehicles, equipment, cabanas, instructors) that are booked as a consequence of selling a product, never sold directly. Workforce covers shift templates, rosters, attendance, swaps and breaks, mirrored on the Staff App. Maintenance and safety cover the asset register, preventive calendars, work orders with scored priority, inspections and incidents, with technicians working from the Staff App. Games and rides configure readers, credit types and consumption priority, play entitlements, game pricing, retry pricing, redemption and the card lifecycle. The virtual queue (Q1) gives a guest a live wait time and a return window for a ride; it is not the on-sale waiting room (Q2). Every calendar has day, week and month views. Configuration resolves tenant, region, venue (outlet only for F&B and retail), and a user's permissions, never the device, decide what they may do. The guest apps (P01, P02) show the guest's side of this: My Tickets, the scan code, Face Pass, wait times, the virtual queue, map booking of cabanas and the visit planner.
*(source: F06 step 1 / F112 step 1 / F111 step 1 / ADR-0002 / ADR-0012 / ADR-0018 / ADR-0041 / ADR-0066 / ADR-0067 / ADR-0068 / DI-652 / DI-627 / DI-640 / DI-654 / DI-666 / DI-482 / DI-483 / DI-907 / DI-919 / DI-923 / DI-865 / DI-678 / TRACKER Actions row 160 / MoM 2026-09-02 AccessControl / MoM 2026-09-07 …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Ticket | The one virtual record a guest owns (ticket number, product, validity, entries). Its number never changes, whatever media carries it or whoever it is transferred or resold to. | Pass (unless the product is a pass), Booking, Order line | DI-652 / DI-620 / contracts/spine/access.yaml#/components/schemas/TicketStatus |
| Media | What the ticket is presented by at a gate (QR code, dynamic QR, wristband/RFID card, NFC, Face Pass, Face Tag). One ticket can carry several media as fallbacks; a media code can also cover several tickets scanned as one group. Show one … | Credential (for guest media; keep Credential for accreditation badges and staff), Ticket code | DI-180 / DI-608 / DI-652 |
| Access point | A place where a scan is judged, with a fixed direction (entry, exit, re-entry, crossover). Hierarchy shown to users is Venue > Park > Zone > Attraction > Access point > Gate/lane > Device. | Scanner (that is the device), Door | screens/P08-venue-back-office.yaml#BO-144 / … |
| Admission profile | The named set of rules an access point enforces (opening window, entries, exit scan, re-entry, validity, crossover). Products point at a profile; tiers such as Bronze/Silver/Gold are profiles with gate allow and deny lists. | Admission rules (as a screen title), Access rule set | DI-185 / contracts/spine/access.yaml#/components/schemas/AdmissionRules |
| Admitted / Denied / Overridden | The three scan outcomes. A denial is always shown with its reason in plain words and a next action; an override is a supervisor admitting despite a denial, and is always attributed and reasoned. | Valid/Invalid, Success/Fail, Error | contracts/spine/access.yaml#/components/schemas/ScanOutcome / … |
| Used | A ticket entry is used the moment a scan succeeds, whether or not the guest physically passed. Mistakes are resolved from the scan history, not by un-scanning. | Redeemed (for admission), Checked in (that is group check-in, a different step) | DI-627 / TRACKER Actions row 221 / TRACKER Actions row 189 |
| Gate mode | What a lane is doing now, set live by the podium or supervisor - Normal, Free flow (counts, does not validate), Drop arm (everybody through, evacuation), Closed (nobody through), Podium (staff validating by eye), Maintenance. Direction is … | Turnstile mode (as a label for direction), Open/Locked | contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode / R221 |
| Offline package | What a scanner holds to validate with no network - entitlements, blacklist, admission profiles and the active guest admission policy version - with its age always visible. | Cache, Local DB | F06 step 3 / ADR-0068 |
| Sync and reconciliation | Sending the offline scan journal to the server, and the duty manager's review of scans the server rejected after the device had already admitted the guest. | Upload, Retry | F06 step 6 / DI-065 |
| Face Pass / Face Tag | Face Pass is the long-lived face credential for members and season-pass holders (renewable); Face Tag is short-lived, for one day or event. Retention is set per tier by the venue. | Face ID, Biometric login | DI-640 / ADR-0063 |
| Accreditation / Credential (accreditation) | Accreditation is the application and approval of a person (media, contractor, corporate, staff of a partner) for an event or season; the credential is what is issued after approval (photo badge, QR or RFID) with zone access rights. | Registration (for the whole process), Ticket | DI-654 / DI-662 |
| Resource | A bookable thing or person a product needs (room, vehicle, cabana, equipment set, instructor). Guests buy products; resources are assigned to the booking, pre-assigned or dynamically. | Asset (that is maintenance), Inventory (that is stock) | DI-475 / DI-482 / TRACKER Actions row 160 |
| Asset | A physical item maintained by the venue (ride, turnstile, printer, pump) with a register record, documents, warranty and maintenance history. | Resource, Device (unless it is an IT device in the device register) | DI-910 / ADR-0067 |
| Work order | A unit of maintenance work, lifecycle Created > Assigned > In progress > Review > Closed, with a resolution timer. | Ticket (reserved for guest tickets), Job card | DI-231 |
| Game / attraction (games module) | In the games and rides module an attraction is an individual game or ride (roller coaster, racing game, bumper cars), not a venue. | Venue, Park | DI-863 |
| Virtual queue / Return window | A guest's place in a ride's queue held without standing in line, with a return window (for example 4:50 to 5:00 PM) that recalculates live. Distinct from the walk-in line and the VIP/express lane, and from the on-sale waiting room. | Waiting room, Fast pass (that is the express product), Booking | DI-675 / DI-678 / DI-679 / ADR-0066 |
| Wait time source | Where a ride's wait time comes from - Sensor, Throughput, Manual, or Unavailable - always shown beside the number. | Live (when the source is manual) | contracts/satellite/queue.yaml#/components/schemas/WaitTimeSource / DI-315 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-053` | Staff Directory | B | 28 | 21 | 6 | 3 | 0 | 0 | — | notStarted (generated) |
| `BO-054` | Role Assignment | A | 16 | 16 | 6 | 6 | 1 | 5 | — | notStarted (generated) |
| `BO-055` | Rota & Scheduling | A | 32 | 19 | 6 | 21 | 0 | 0 | — | notStarted (generated) |
| `BO-056` | Time & Attendance | D | 5 | 19 | 6 | 2 | 0 | 0 | — | notStarted (generated) |
| `BO-057` | Training & Certification | B–D | 2 | 22 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-066` | Notification Settings | D | 12 | 23 | 6 | 4 | 0 | 0 | — | notStarted (generated) |
| `BO-084` | Approval Inbox | A | 11 | 11 | 6 | 22 | 0 | 3 | — | notStarted (generated) |
| `BO-085` | Approval Request | A | 8 | 12 | 6 | 24 | 0 | 3 | — | notStarted (generated) |
| `BO-086` | Approval Matrix | B | 34 | 10 | 6 | 49 | 0 | 3 | — | notStarted (generated) |
| `BO-087` | Approval Delegations | A | 43 | 22 | 6 | 51 | 0 | 3 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-053` Staff Directory

**Find anyone who works at this venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 1 · needs the `core` module |
| Block | Block B · ticket #29045 (VM-BO-053) |
| Who uses it | venue staff holding `PERMISSION_VIEW`, `SESSION_FORCE_LOGOUT`, `USER_MANAGE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (2 read, 1 operate, 2 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPrincipals` reads the population and `getPrincipal` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `challengeId` (navigation), `sessionId` (session), `principalId` (navigation) · cold entry: Opened from the Venue Management menu; lists everyone in scope. The selected person comes from the row, not the session. |
| Route | `/venue-operations/staff-directory` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 31 August** — `Marketing Board 1.dc.html` frame `crm-1b` (*Guest Directory*), matched on title at 0.80 within this board’s platforms.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Find anyone who works at the venues in scope, see their roles and validity, create a staff member, change their validity or primary role, and reset a forgotten password or PIN under a second factor. It is a directory first: search by name or employee number, then act on one person.

**Fixed on main** (the package already carries these; draw what it says): The navigation has no entry or exit (entryFrom and exitTo empty), and entryState reads principalId from the session. (CHG-SBO-015); Reaches resetPrincipalCredential (step-up mfa) and declares no way to raise the challenge. (CHG-SBO-015); Tables show every schema field, plumbing included: 'Every principal' drop id, primaryRoleId. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listPrincipals`. | `listPrincipals` ?scopePath |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listPrincipals`. | `listPrincipals` ?isActive |
| Authentication code | text field | — | — | — | — | Asked in place inside the Sign everyone out confirmation; its result is the `stepUpToken`. Five wrong codes lock step-up for the lockout minutes (audit R126). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Employee | picker: choose an employee | — | — | `listWorkAssignments` ?employeeId |
| Active on | date picker | — | — | `listWorkAssignments` ?activeOn |
| Principal | picker: choose a principal | — | — | `listActiveSessions` ?principalId |
| Workstation | picker: choose a workstation | — | — | `listActiveSessions` ?workstationId |

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

**Form: End this session** (confirmDialog, opened by *End this session*; *End session* calls `forceLogout`, *Cancel* sends nothing)

**Names whose session ends, where and since when, and that their shift stays open and their float does not move.** Collects what `forceLogout` sends: Required: `reason`.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `forceLogout` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | The till making the call. Required with no session (the POS-000 door; CHG-RUL-015). | `forceLogout` body |
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | The supervisor ending the session, signing on this device. Required with no session (POS-000), ignored with one (CHG-RUL-015). | `forceLogout` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `forceLogout` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `forceLogout` body |

Carried, not typed: `sessionId`

Errors to draw in the form: 403 The caller lacks SESSION_FORCE_LOGOUT, or, with no session, the supervisor step-up is missing or failed or the session is not at the till's venue …

**Form: Sign everyone out** (confirmDialog, opened by *Sign everyone out*; *Sign everyone out* calls `revokeAllSessions`, *Cancel* sends nothing)

**Says how many people in which venues are signed out, and whether the caller is one of them.** Collects what `revokeAllSessions` sends: Required: `reason`, `stepUpToken` (the authentication code, asked in place). Optional: `venueId`, `excludeSelf`.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `revokeAllSessions` body |
| Step up token `stepUpToken` | text field | required | — | — | — | — | `revokeAllSessions` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `revokeAllSessions` body |
| Exclude self `excludeSelf` | toggle | optional | on | — | — | — | `revokeAllSessions` body |

Errors to draw in the form: 403 Step-up token missing, expired or issued for a different action

**Sent by *Reset principal credential*** (`resetPrincipalCredential`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Method `method` | segmented control | required | — | Password · PIN | — | — | `resetPrincipalCredential` body |
| Temporary credential `temporaryCredential` | text area | required | — | max length 512 | — | Issued to the principal out of band. Must be changed at next sign-in. | `resetPrincipalCredential` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `resetPrincipalCredential` body |

**Sent by *Email me a code instead*** (`createMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Create staff member**: Username (unique within the tenant's cell) and display name required; an initial credential is optional and, when given, must be changed at first sign-in (default on); validity end date optional; roles picked from the tenant's roles. The job title and posting can be set here (workforce), and suggested roles appear from peers with the same title. *(source: contracts/spine/identity.yaml#createPrincipal; contracts/satellite/workforce.yaml#setWorkAssignment; contracts/spine/identity.yaml#suggestRoleAssignment)*
- **Reset credential**: Password or PIN; a temporary value issued out of band, changed at next sign-in; a reason of at least 3 characters. The person resetting cannot reset their own. *(source: contracts/spine/identity.yaml#resetPrincipalCredential)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setJobTitle: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/workforce.yaml#setJobTitle)*

#### Outputs: what the screen shows and produces

**Shown**

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
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**Signed in now** (detail panel, from `listActiveSessions`): **Session management lives here, not on the doors** (CHG-DOOR-003, 2 October 2026). The selected person's active session (`?principalId=`): where, since when, and whether a shift is open on it. Shown only to a holder of SESSION_FORCE_LOGOUT; absent, not empty, for anyone else. This is where a supervisor ends the session a door refused with 409 (audit R184).

| Shows | Format | Notes |
|---|---|---|
| Principal name | text | Read from `identity.principal` with the row. |
| Role name | text | Read from `identity.role` with the row. |
| Workstation name | text | Read from the workstation with the row. |
| Device info | text | — |
| Has open shift | yes / no (icon or chip) | Revoking this session leaves cash unreconciled. Computed on read from the shift the principal holds open at the workstation … |
| Started at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| End this session (destructive button) | `forceLogout` POST `/auth/sessions/{sessionId}/force-logout` | inline | — | 403 The caller lacks SESSION_FORCE_LOGOUT, or, with no session, the supervisor step-up is missing or failed or the session is not at the till's venue … | step-up: pin (On the POS-000 door nobody at the till has a session, so a supervisor's own PIN on the device proves who ended the …); opens confirmDialog first |
| Create principal (primary button) | `createPrincipal` POST `/principals` | CreatePrincipalRequest | Principal | 400 Validation failed; 409 Username already in use within this cell | opens modal first |
| Save principal (secondary button) | `updatePrincipal` PATCH `/principals/{principalId}` | inline | Principal | — | opens modal first |
| Reset principal credential (destructive button) | `resetPrincipalCredential` POST `/principals/{principalId}/credential-reset` | ResetCredentialRequest | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | step-up: mfa (Replaces somebody else's secret, which is the whole of an account takeover.) |
| Sign everyone out (destructive button) | `revokeAllSessions` POST `/auth/sessions/revoke-all` | inline | inline | 403 Step-up token missing, expired or issued for a different action | opens confirmDialog first |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Directory rows**: Name, username or employee number, primary role and other roles, job title and venue posting, active/inactive, valid until, last sign-in. Inactive and expired people are filtered out by default. *(source: contracts/spine/identity.yaml#listPrincipals)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Deactivate**: Ends the person's sessions immediately (end date, primary role and permission changes revoke sessions at once); the confirmation says so. *(source: R126; contracts/spine/identity.yaml#updatePrincipal)*
- **Reset principal credential**: Confirmation names the consequence first, then asks for the authentication code (authenticator app, or an emailed code as fallback); only a verified challenge sends resetPrincipalCredential with its single-use stepUpToken. Wrong code: the action is not sent and nothing changes; five wrong codes lock step-up for the policy's lockout minutes and the screen says when it lifts. Why the control exists: Replaces somebody else's secret, which is the whole of an account takeover. *(source: contracts/spine/identity.yaml#resetPrincipalCredential; R126; contracts/spine/identity.yaml#createMfaChallenge)*

**Data it reads**: `listPrincipals` (onLoad, List principals); `getPrincipal` (onLoad, Read a principal); `listJobTitles` (onLoad, Job titles); `listWorkAssignments` (onLoad, Who is posted to which job title at which venue); `listActiveSessions` (onLoad, Where the selected person is signed in now, so a supervisor …)

**Where the user goes next**

- → `BO-055` Rota & Scheduling: *Rota & Scheduling*; carries `assignmentId`

**What opens over it**

- confirmDialog *Reset principal credential*: **Names what `resetPrincipalCredential` changes and what it leaves alone**, in the consequence rather than the verb. A staff this affects should be identified in the dialog, not just counted. **Collects what `resetPrincipalCredential` sends before it is called.** Required: `method` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff yet. Offers Create principal (`createPrincipal`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on scopePath, isActive and the staff are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires to show this screen, and names that permission (the screen's other reads need `SESSION_FORCE_LOGOUT`, `WORKFORCE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERMISSION_VIEW` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither `principalId` nor `jobTitleId` with `scopePath`, or both.; 400 Validation failed; 409 Overlaps an existing primary posting, or the employee is terminated externally; 409 Username already in use within this cell |

#### Edge cases to draw

- **Username already used**: Refused 409; says the username exists in this cell and suggests a variant. *(source: contracts/spine/identity.yaml#createPrincipal)*
- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds PERMISSION_VIEW, USER_MANAGE, WORKFORCE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: WORKFORCE_MANAGE for setJobTitle, setWorkAssignment. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/workforce.yaml#setJobTitle)*
- **createPrincipal answers 409**: Show it as something the person can act on, not a failure: Username already in use within this cell *(source: contracts/spine/identity.yaml#createPrincipal)*
- **setWorkAssignment answers 409**: Show it as something the person can act on, not a failure: Overlaps an existing primary posting, or the employee is terminated externally *(source: contracts/satellite/workforce.yaml#setWorkAssignment)*

#### Consistency with other screens

- Match `BO-054`: Roles assigned here are the ones defined there.
- Match `CMS-019`: The CMS User Access list must be this directory filtered, not a copy.
- Match `BO-873`: The Staff Resource Directory is the workforce view of the same people.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
staff:
- name: Rahul Menon
  username: '10482'
  primaryRole: Cashier
  jobTitle: Ticket Sales Associate
  venue: AquaCove Abu Dhabi
  validUntil: ''
  lastSignIn: 01/10/2026 08:55
- name: Omar Haddad
  username: omar.haddad
  primaryRole: Supervisor
  roles:
  - Supervisor
  - Cashier
  venue: AquaCove Abu Dhabi
  lastSignIn: 01/10/2026 07:40
- name: Layla Hassan
  username: '10611'
  primaryRole: Cashier
  venue: AquaCove Dubai
  validUntil: 31/12/2026
  lastSignIn: 29/09/2026 17:20
```

#### Permissions

- `resetPrincipalCredential` → `USER_MANAGE` (configure) · staff · step-up mfa
- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `getPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `createPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `updatePrincipal` → `USER_MANAGE` (configure) · staff, partner
- `listJobTitles` → `WORKFORCE_VIEW` (read) · staff
- `setJobTitle` → `WORKFORCE_MANAGE` (configure) · staff
- `listWorkAssignments` → `WORKFORCE_VIEW` (read) · staff
- `setWorkAssignment` → `WORKFORCE_MANAGE` (configure) · staff
- `suggestRoleAssignment` → `PERMISSION_VIEW` (read) · staff
- `listActiveSessions` → `SESSION_FORCE_LOGOUT` (operate) · staff, partner · step-up pin
- `forceLogout` → `SESSION_FORCE_LOGOUT` (operate) · staff, partner · step-up pin
- `revokeAllSessions` → `SESSION_FORCE_LOGOUT` (operate) · staff, partner
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

**A refused user sees:** Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires to show this screen, and names that permission (the screen's other reads need `SESSION_FORCE_LOGOUT`, `WORKFORCE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERMISSION_VIEW` for …

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.6 | The system should be able to create a new Back Office/POS user and Logon to back office/POS using new user. | F&B POS | CONTRACTED | `createPrincipal` |
| 7.1.35 | The system shall provide AI-assisted recommendations for user provisioning, permission optimization, excessive privilege detection, access reviews, and security risk identification. | F&B POS | CONTRACTED | `suggestRoleAssignment` |
| 7.1.20 | The system shall allow administrators to view active sessions, force logout users, revoke sessions, configure inactivity timeouts, and control concurrent session limits. | F&B POS | CONTRACTED | `listActiveSessions` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-053` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Marketing Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Marketing Board 1.dc.html`
- Client design-board frames: `Marketing Board 1.dc.html#crm-1b`
- ADR-0004 *Single session per user* (`docs/adr/0004-single-session-per-user.md`)
- ADR-0033 *Every asynchronous handoff has an outbox and a place to fail* (`docs/adr/0033-outbox-and-dead-letters.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (400, 403, 404, 409, 410, 422).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-053?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: End this session, Create principal, Save principal, Reset principal credential, Sign everyone out, Email me a code instead.
- [ ] Every transition is wired: `BO-055`.
- [ ] Every gated control is gated: `PERMISSION_VIEW`, `SESSION_FORCE_LOGOUT`, `USER_MANAGE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-054` Role Assignment

**Give somebody the permissions their job needs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 1 · needs the `core` module |
| Block | Block A · ticket #27938 (APP-SETUP-BO-054) |
| Who uses it | venue staff holding `PERMISSION_VIEW`, `ROLE_MANAGE`, `USER_MANAGE` (1 read, 2 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRoles` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `principalId` (navigation), `campaignId` (navigation), `roleId` (navigation) |
| Route | `/venue-operations/role-assignment` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Define what each role may do, per module, and see who holds it: roles are fully configurable (nothing predefined; the five seeded roles are editable starting points). Admins compare two roles side by side, see unused and missing permissions, and run access reviews. The rule to get right: granting a role is per scope, and the screen must show at which level a grant applies.

**Fixed on main** (the package already carries these; draw what it says): The screen declares only listRoles and createRole for roles; no operation sets a role's permissions or grants a role to a person. (CHG-WIR-021); entryState reads campaignId. (CHG-SBO-011); setRolePermissions lives in tenancy.yaml with a tenant scope level while roles live in identity.yaml at venue. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every role' drop id, inheritsFromRoleId. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Start from presets | picker: choose an id | optional | — | — | shows names, sends the id | **There are no default roles (decided 2 October 2026 by Chinmay, DEC-007; CHG-CSP-003, CHG-CSA-006).** A role starts from presets per module (All, Viewer, Mid-level); picking one fills that module's … | `CapabilityTemplate.id` |
| Permissions by module | multi-select chips | optional | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | The per-module checklist: one group per module, every permission in exactly one module (x-ticvai-permission-modules). | `Role.permissions` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | — | Open · Completed · Expired | `listAccessReviewCampaigns` ?status |
| Module | text field | — | — | `listCapabilityTemplates` ?module |

**Form: Save role permissions** (modal, opened by *Save role permissions*; *Save role permissions* calls `setRolePermissions`, *Cancel* sends nothing)

**Collects what `setRolePermissions` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | — | `setRolePermissions` body |
| Inherits from role `inheritsFromRoleId` | picker: choose an inherits from role | optional | — | — | shows names, sends the id | — | `setRolePermissions` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Breaches a segregation rule. Names the rule and both permissions.

**Form: Grant role** (modal, opened by *Grant role*; *Grant role* calls `updatePrincipal`, *Cancel* sends nothing)

**Collects what `updatePrincipal` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `updatePrincipal` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updatePrincipal` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePrincipal` body |
| Primary role `primaryRoleId` | picker: choose a primary role | optional | — | — | shows names, sends the id | — | `updatePrincipal` body |

**Form: Preview effective permissions** (modal, opened by *Preview effective permissions*; *Preview effective permissions* calls `resolvePermissions`, *Cancel* sends nothing)

**Collects what `resolvePermissions` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Principal `principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `resolvePermissions` body |
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `resolvePermissions` body |
| At scope path `atScopePath` | text field | optional | — | — | — | Optional. When supplied, the response also carries `decisionsAtScope`: PERMIT or DENY per permission at that node. | `resolvePermissions` body |

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

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Role permissions**: Grouped by module with three levels per module (edit and view, view only, hidden) and sub-permissions inside a module; TICVAI-only permissions (PLATFORM_*, DEVELOPER_ADMIN) never offered to a tenant role. Granting ROLE_MANAGE or LEDGER_APPROVE warns that holders will need MFA at sign-in. *(source: DI-387; R229; R135)*
- **Role code**: Unique per tenant, compared case-insensitively; a clash is the duplicate-code refusal. *(source: R108)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setCapabilityTemplate: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/identity.yaml#setCapabilityTemplate)*

#### Outputs: what the screen shows and produces

**Shown**

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
| Create role (primary button) | `createRole` POST `/roles` | inline | Role | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A preset code that does not exist … | opens modal first |
| Save role permissions (secondary button) | `setRolePermissions` PUT `/roles/{roleId}/permissions` | inline | inline | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Breaches a segregation rule. Names the rule and both permissions. | opens modal first |
| Grant role (secondary button) | `updatePrincipal` PATCH `/principals/{principalId}` | inline | Principal | — | opens modal first |
| Preview effective permissions (secondary button) | `resolvePermissions` POST `/permissions/resolve` | inline | inline | — | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Roles comparison**: Two roles side by side, differences highlighted (e.g. cashier lacks refund and void that supervisor has). *(source: DI-153)*
- **Holders**: Principal count and grant count per role, linking to the people; system (seeded) roles marked editable but not deletable. *(source: contracts/spine/identity.yaml#listRoles)*

**Data it reads**: `listRoles` (onLoad, List roles); `listAccessReviewCampaigns` (onLoad, Open access reviews); `listCapabilityTemplates` (onLoad, The presets (All, Viewer, Mid-level) per module that fill …)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The role assignment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the role assignment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No role assignment yet. Offers Create role (`createRole`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listRoles` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires to show this screen, and names that permission (the screen's other reads need `PERMISSION_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `USER_MANAGE` for `updatePrincipal`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither `principalId` nor `jobTitleId` with `scopePath`, or both.; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 Breaches a segregation rule. Names the rule and both permissions.; 422 A preset code that does not exist (`unknown-preset`), or an initial permission set that … |

#### Edge cases to draw

- **Editing a role held by people who are signed in**: Permission changes revoke the holders' sessions at once; the save confirmation says how many people will be signed out. *(source: R126)*
- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Consistency with other screens

- Match `BO-1066`: Roles, Permissions & Masking is the same role model with data masking; it must not be a second role editor.
- Match `ADM-342`: The MFA permission list there decides the warning shown here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
roles:
- code: CASHIER
  name: Cashier
  holders: 46
  system: true
- code: SUPERVISOR
  name: Supervisor
  holders: 9
  system: true
- code: FNB_OUTLET_MGR
  name: F&B Outlet Manager
  holders: 3
  system: false
```

#### Permissions

- `listRoles` → `ROLE_MANAGE` (configure) · staff
- `createRole` → `ROLE_MANAGE` (configure) · staff
- `setCapabilityTemplate` → `ROLE_MANAGE` (configure) · staff
- `listPermissionFindings` → `PERMISSION_VIEW` (read) · staff
- `suggestRoleAssignment` → `PERMISSION_VIEW` (read) · staff
- `listAccessReviewCampaigns` → `PERMISSION_VIEW` (read) · staff
- `listAccessReviewItems` → `PERMISSION_VIEW` (read) · staff
- `setRolePermissions` → `ROLE_MANAGE` (configure) · staff
- `updatePrincipal` → `USER_MANAGE` (configure) · staff, partner
- `resolvePermissions` → `PERMISSION_VIEW` (read) · staff
- `listCapabilityTemplates` → `PERMISSION_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires to show this screen, and names that permission (the screen's other reads need `PERMISSION_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `USER_MANAGE` for `updatePrincipal`.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.47 | Provide a sandbox environment to test authorization policies before deployment and identify conflicts, missing permissions and excessive permissions. | F&B POS | CONTRACTED | `listPermissionFindings` |
| 7.1.35 | The system shall provide AI-assisted recommendations for user provisioning, permission optimization, excessive privilege detection, access reviews, and security risk identification. | F&B POS | CONTRACTED | `suggestRoleAssignment` |
| 3.3.27 | Real-Time Authorization - System shall evaluate access decisions in real time. | Admission and Access | CONTRACTED | `resolvePermissions` |
| 7.1.15 | The system shall support inheritance of permissions from parent roles, groups, departments, venues, or business structures while allowing controlled overrides. | F&B POS | CONTRACTED | `resolvePermissions` |
| 7.1.31 | The system shall restrict access to guest profiles, CRM data, financial data, wallet data, loyalty data, membership data, inventory costs, and marketing data based on permissions. | F&B POS | CONTRACTED | `resolvePermissions` |
| 7.1.51 | Evaluate authorization decisions in real time for every protected transaction, screen, API call or business action. | F&B POS | CONTRACTED | `resolvePermissions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam: add a "roles comparison" view letting an admin compare two roles side by side (e.g. confirm a cashier role lacks the refund/void permissions a supervisor role has). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-153)*

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-054` · status **notStarted** · provenance generated
- ADR-0051 *Every AI function ships on a baseline and learns per tenant; a model goes live only on evidence* (`docs/adr/0051-ai-ships-on-a-baseline-and-learns-per-tenant.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-054?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create role, Save role permissions, Grant role, Preview effective permissions.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PERMISSION_VIEW`, `ROLE_MANAGE`, `USER_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-055` Rota & Scheduling

**Decide who is on which gate, when.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 1 · needs the `core` module |
| Block | Block A · ticket #28417 (APP-SETUP-BO-055) |
| Who uses it | venue staff holding `SCOPE_VIEW`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (2 read, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRotaAssignments` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `assignmentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/rota-scheduling` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The rota: who is on which gate, till or ride, when - as a calendar (Day by hour from the venue's day start, Week, Month, Agenda) with people as rows, flagged for overlaps, missing roles, rest-period and working-hour breaches, overtime and labour cost at the point of scheduling. The one thing to get right: breaches are flagged when the shift is placed, not discovered at payroll.

**Fixed on main** (the package already carries these; draw what it says): No calendar component; a table with date pickers (CHG-SBO-009); Filters are principal and department id text fields; no navigation in or out (inferred, none) (CHG-SBO-009).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listRotaAssignments`. | `listRotaAssignments` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listRotaAssignments`. | `listRotaAssignments` ?to |
| Staff member | picker: choose a principal | optional | — | — | shows names, sends the id | A pick list of staff by name. | `RotaAssignment.principalId` |
| Department | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `OrgUnit.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet; Modelling a restaurant as a department would put it in the staffing tree, which is why the two cannot be collapsed (CF-138, ADR-0018). | `listOrgUnits` ?level |
| Include inactive | toggle | off | — | `listOrgUnits` ?includeInactive |

**Form: Create rota assignment** (modal, opened by *Create rota assignment*; *Create rota assignment* calls `createRotaAssignment`, *Cancel* sends nothing)

**Collects what `createRotaAssignment` sends before it is called.** Required: `principalId`, `venueId`, `position`, `startsAt`, `endsAt`. Optional: `restPeriodBefore`, `labourCost`, `departmentId`, `requiredRoleId`, `workstationId`, `status`, `breakMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `breachesWorkingHourLimit`, `displayName`, `id`, `overtimeMinutes` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rest period before `restPeriodBefore` | number field | optional | — | — | — | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and unsafe in all of them. | `createRotaAssignment` body |
| Labour cost `labourCost` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. | `createRotaAssignment` body |
| Principal `principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Position `position` | text field | required | — | — | — | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota assignment is not a shift. | `createRotaAssignment` body |
| Required role `requiredRoleId` | picker: choose a required role | optional | — | — | shows names, sends the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. | `createRotaAssignment` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. | `createRotaAssignment` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRotaAssignment` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRotaAssignment` body |
| Status `status` | select | optional | — | Planned · Published · Confirmed · Swap pending · Cancelled · Completed · No show | — | — | `createRotaAssignment` body |
| Break minutes `breakMinutes` | number field (minutes) | optional | — | — | — | — | `createRotaAssignment` body |
| Note `note` | text area | optional | — | — | — | — | `createRotaAssignment` body |

Errors to draw in the form: 409 Overlaps an existing assignment, or the person lacks the required role

**Form: Save rota assignment** (modal, opened by *Save rota assignment*; *Save rota assignment* calls `updateRotaAssignment`, *Cancel* sends nothing)

**Collects what `updateRotaAssignment` sends before it is called.** Required: `principalId`, `venueId`, `position`, `startsAt`, `endsAt`. Optional: `restPeriodBefore`, `labourCost`, `departmentId`, `requiredRoleId`, `workstationId`, `status`, `breakMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `breachesWorkingHourLimit`, `displayName`, `id`, `overtimeMinutes` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rest period before `restPeriodBefore` | number field | optional | — | — | — | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and unsafe in all of them. | `updateRotaAssignment` body |
| Labour cost `labourCost` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. | `updateRotaAssignment` body |
| Principal `principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `updateRotaAssignment` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `updateRotaAssignment` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `updateRotaAssignment` body |
| Position `position` | text field | required | — | — | — | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota assignment is not a shift. | `updateRotaAssignment` body |
| Required role `requiredRoleId` | picker: choose a required role | optional | — | — | shows names, sends the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. | `updateRotaAssignment` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. | `updateRotaAssignment` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateRotaAssignment` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateRotaAssignment` body |
| Status `status` | select | optional | — | Planned · Published · Confirmed · Swap pending · Cancelled · Completed · No show | — | — | `updateRotaAssignment` body |
| Break minutes `breakMinutes` | number field (minutes) | optional | — | — | — | — | `updateRotaAssignment` body |
| Note `note` | text area | optional | — | — | — | — | `updateRotaAssignment` body |

**Form: Request shift swap** (modal, opened by *Request shift swap*; *Request shift swap* calls `requestShiftSwap`, *Cancel* sends nothing)

**Collects what `requestShiftSwap` sends before it is called.** Required: `toPrincipalId`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `requestShiftSwap` body |
| Reason `reason` | text area | optional | — | max length 300 | — | — | `requestShiftSwap` body |

Errors to draw in the form: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the …

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Assignment**: Person (picker), position (gate steward, cashier, lifeguard, technician), required role, workstation only where the position needs a till, start-end in venue time, break minutes, note. *(source: contracts/satellite/workforce.yaml#createRotaAssignment)*
- **Filters**: Department and person pickers, date range from the calendar; no id text fields. *(source: contracts/satellite/workforce.yaml#listRotaAssignments)*

#### Outputs: what the screen shows and produces

**Shown**

**Rota** (calendar view, from `listRotaAssignments`): Day, week and month views (VO-R01); the table below is the same rota as a list.

| Shows | Format | Notes |
|---|---|---|
| Display name | text | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| Display name | text | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |

**The selected rota assignment** (detail panel, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| Display name | text | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create rota assignment (primary button) | `createRotaAssignment` POST `/rota-assignments` | RotaAssignment | RotaAssignment | 409 Overlaps an existing assignment, or the person lacks the required role | opens modal first |
| Save rota assignment (secondary button) | `updateRotaAssignment` PATCH `/rota-assignments/{assignmentId}` | RotaAssignment | RotaAssignment | — | opens modal first |
| Request shift swap (secondary button) | `requestShiftSwap` POST `/rota-assignments/{assignmentId}/swap` | inline | ShiftSwap | 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rota calendar**: Shift bars per person coloured by status (Planned, Published, Confirmed, Swap pending, Cancelled, Completed, No show); icons for overtime, rest-period under the minimum and working-hour breach; labour cost per day and per person in AED. *(source: contracts/satellite/workforce.yaml#/components/schemas/RotaAssignment / DI-488)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add shift**: Refused on overlap or missing role, with the reason named. *(source: contracts/satellite/workforce.yaml#createRotaAssignment)*
- **Request swap (for a person)**: Routes through approvals; both parties accept before the supervisor sees it. *(source: contracts/satellite/workforce.yaml#requestShiftSwap)*

**Data it reads**: `listRotaAssignments` (onLoad, The rota); `listOrgUnits` (onLoad, List scope nodes visible to the session (the pick list))

**Where the user goes next**

- → `BO-056` Time & Attendance: *Time & Attendance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rota scheduling list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rota scheduling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rota scheduling yet. Offers Create rota assignment (`createRotaAssignment`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to, principalId, departmentId and the rota scheduling are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `WORKFORCE_MANAGE` for `createRotaAssignment` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Overlaps an existing assignment, or the person lacks the required role; 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … |

#### Consistency with other screens

- Match `EMP-022`: Staff see their own rota from the same data.
- Match `BO-883`: The workforce roster boards use the same calendar and statuses.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
shifts:
- person: Rahul Menon
  position: Gate steward - Main Plaza Gate 2
  time: Sat 10 Oct 07:00-15:00
  status: Published
- person: Fatima Al Hashimi
  position: Duty supervisor
  time: Sat 10 Oct 14:00-23:00
  flags: Rest 9 h before (min 11 h)
  cost: AED 540
```

#### Permissions

- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `createRotaAssignment` → `WORKFORCE_MANAGE` (configure) · staff
- `updateRotaAssignment` → `WORKFORCE_MANAGE` (configure) · staff
- `requestShiftSwap` → `WORKFORCE_VIEW` (read) · staff
- `listOrgUnits` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `WORKFORCE_MANAGE` for `createRotaAssignment` …

#### Requirements it meets

21 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 1.2.80 | System shall allow employees to request shift swaps, shift transfers, shift pickups, and shift releases. Approval workflows, qualification validation, staffing rules, and manager approvals shall be … | Ticketing Catalogue | CONTRACTED | `requestShiftSwap` |
| 3.3.41 | Venue-Specific Policies - System shall support venue-specific access policies. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 3.3.43 | Policy Inheritance - System shall support inheritance of policies across organizational structures. | Admission and Access | CONTRACTED | `listOrgUnits` |
| … 9 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-055` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-055?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create rota assignment, Save rota assignment, Request shift swap.
- [ ] Every transition is wired: `BO-056`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-056` Time & Attendance

**Record who actually turned up.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 2 · needs the `core` module |
| Block | Block D · task VM-BO-056 |
| Who uses it | venue staff holding `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAttendance` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `recordId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/time-attendance` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Attendance is self clock-in only** (decided by Chinmay, 3 October 2026 (CHG-SPF-009), not the recommendation): staff clock in and out themselves on the staff app (`recordAttendance`, EMP-024 and EMP-025); a supervisor corrects a record afterwards here with Amend attendance (`amendAttendance`). Record attendance left this screen.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Attendance against the rota: who clocked in and out, where, late starts, no-shows and who covered, with supervisor amendments kept as history (the original is never overwritten). The one thing to get right: clock-ins are shown beside the assignments that expected them, so exceptions jump out.

**Known correction pending (do not draw the wrong version)**

- **Raw latitude and longitude columns and amendedByPrincipalId** Why: Show the place name and the person's name (VO-R12). *(source: contracts/satellite/workforce.yaml#listAttendance; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No navigation in or out (inferred)** Why: Should sit beside the rota (BO-055) under People & Access Rights. *(source: screens/P08-venue-back-office.yaml#BO-056; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listAttendance`. | `listAttendance` ?date |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listAttendance`. | `listAttendance` ?principalId |
| Exceptions only | toggle | optional | — | — | — | Sends `?exceptionsOnly=` to `listAttendance`. | `listAttendance` ?exceptionsOnly |

**Form: Amend attendance** (modal, opened by *Amend attendance*; *Amend attendance* calls `amendAttendance`, *Cancel* sends nothing)

**Collects what `amendAttendance` sends before it is called.** Required: `correctedAt`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Corrected at `correctedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `amendAttendance` body |
| Reason `reason` | text area | required | — | max length 300 | — | — | `amendAttendance` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Date (default today), person picker, Exceptions only toggle. *(source: contracts/satellite/workforce.yaml#listAttendance)*
- **Amend**: Corrected time and a required reason (max 300); each amendment appends. *(source: contracts/satellite/workforce.yaml#amendAttendance)*
- **Record attendance (on behalf)**: Kind (clock in, clock out, break start, break end), time, assignment; access point where the venue requires it. *(source: contracts/satellite/workforce.yaml#recordAttendance)*

#### Outputs: what the screen shows and produces

**Shown**

**Every attendance** (data table, from `listAttendance`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Clock in, Clock out, Break start, Break end | — |
| Occurred at | 1 Oct 2026, 14:30 | Device time — when it happened. |
| Recorded at | 1 Oct 2026, 14:30 | When the server received it. Both are kept: a steward clocking in offline at a gate is not late because the sync was. |
| Latitude | 1,234.5 | — |
| Longitude | 1,234.5 | — |
| Is amended | yes / no (icon or chip) | — |

**The selected attendance** (detail panel, from `listAttendance`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Clock in, Clock out, Break start, Break end | — |
| Occurred at | 1 Oct 2026, 14:30 | Device time — when it happened. |
| Recorded at | 1 Oct 2026, 14:30 | When the server received it. Both are kept: a steward clocking in offline at a gate is not late because the sync was. |
| Latitude | 1,234.5 | — |
| Longitude | 1,234.5 | — |
| Amendment reason | text | The latest amendment's reason. The full history is `amendments` (audit R129 (7)). |
| Original occurred at | 1 Oct 2026, 14:30 | The original is never overwritten. Attendance feeds pay, and a record that can be quietly rewritten is not evidence. |
| Amendments | list or chips (count when long) | Every correction, oldest first, one row each (decided 28 September, audit R129 (7)). |

**Amendment history** (data table, from `listAttendance`): **Every correction, not only the last** (decided 28 September, audit R129 (7)) — read from `AttendanceRecord.amendments`: who, when, before, after and why.

| Shows | Format | Notes |
|---|---|---|
| Amended at | 1 Oct 2026, 14:30 | — |
| Amended by principal | the name it points at, never the id | — |
| Occurred at before | 1 Oct 2026, 14:30 | The record's time before this correction. |
| Occurred at after | 1 Oct 2026, 14:30 | The time this correction set (`correctedAt` on the request). |
| Reason | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Amend attendance (primary button) | `amendAttendance` POST `/attendance/{recordId}/amend` | inline | AttendanceRecord | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Day view**: Per assignment - scheduled start/end vs actual clock in/out, late minutes, break taken, location (access point name, not coordinates), status (On time, Late, No show, Covered, Amended). *(source: contracts/satellite/workforce.yaml#listAttendance / DI-489)*
- **Amendment history**: Every correction - who, when, before, after, why. *(source: contracts/satellite/workforce.yaml#listAttendance)*

**Data it reads**: `listAttendance` (onLoad, Who was here)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The time attendance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the time attendance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No time attendance yet. Offers Record attendance (`recordAttendance`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on date, principalId, exceptionsOnly and the time attendance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAttendance` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `WORKFORCE_MANAGE` for `amendAttendance`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Clock-in recorded offline**: Shows device time and arrival time; not marked absent. *(source: contracts/satellite/workforce.yaml#recordAttendance)*

#### Consistency with other screens

- Match `EMP-024`: Clock in/out on the Staff App writes these records.
- Match `BO-888`: Live workforce command centre counts come from the same records.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
day:
- person: Rahul Menon
  scheduled: 07:00-15:00
  actual: 06:52-15:04
  status: On time
  at: Main Plaza Gate 2
- person: Omar Haddad
  scheduled: 07:00-15:00
  actual: '-'
  status: No show
- person: Maria Santos
  scheduled: 09:00-17:00
  actual: 09:18-17:00
  status: Late 18 min, Amended (phone died)
```

#### Permissions

- `listAttendance` → `WORKFORCE_VIEW` (read) · staff
- `amendAttendance` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listAttendance` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `WORKFORCE_MANAGE` for `amendAttendance`.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.7 | System shall display staffing levels, shift attendance, assignments, absences, overtime, and workforce utilization. | Unified Operations Dashboard | CONTRACTED | `listAttendance` |
| 1.2.75 | System shall maintain complete audit logs. | Ticketing Catalogue | CONTRACTED | `amendAttendance` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-056` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-056?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Amend attendance.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-057` Training & Certification

**Know who is allowed to do what.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `USER_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPrincipals` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/training-certification` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Who is trained and certified to do what (ride operator, first aid, cash handling), with expiry, so a supervisor can see who may be rostered on a task. As wired it only lists principals; the certification data is missing.

**Fixed on main** (the package already carries these; draw what it says): The only operation is listPrincipals; nothing reads or records training or certification. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every principal' drop id, primaryRoleId. (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listPrincipals`. | `listPrincipals` ?scopePath |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listPrincipals`. | `listPrincipals` ?isActive |

#### Outputs: what the screen shows and produces

**Shown**

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

**Training records** (data table, from `listTrainingRecords`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Course name | text | — |
| Required | yes / no (icon or chip) | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| State | chip: Not started, In progress, Passed, Failed, Expired | — |
| Evidence ref | text | — |

**The selected principal** (detail panel, from `listPrincipals`)

| Shows | Format | Notes |
|---|---|---|
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**Data it reads**: `listPrincipals` (onLoad, List principals); `listTrainingRecords` (onLoad, Training completed and what is expiring, per person)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The training certification list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the training certification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No training certification yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on scopePath, isActive and the training certification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
certifications:
- staff: Yusuf Rahman
  certificate: Wave pool lifeguard
  issued: 12/03/2026
  expires: 11/03/2027
- staff: Mariam Saeed
  certificate: Cash handling
  expires: 30/10/2026 (expiring)
```

#### Permissions

- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `listTrainingRecords` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-057` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-057?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `USER_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-066` Notification Settings

**Decide what this venue tells people, and how.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 2 · needs the `core` module |
| Block | Block D · task VM-BO-066 |
| Who uses it | venue staff holding `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `announcementId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/notification-settings` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Acknowledging an announcement is the recipient's act on the Staff App, not a back-office action (design-notes correction venue-operations BO-066).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Despite its name, this screen publishes staff announcements (operational, safety, emergency, HR, celebration) targeted by venue, department and role, with acknowledgement and reach (who has not acknowledged). The one thing to get right: Emergency is not a louder Operational - it overrides the Staff App home screen, bypasses quiet hours, requires acknowledgement and shows the roll call of who has not confirmed.

**Known correction pending (do not draw the wrong version)**

- **Name "Notification Settings" does not match the content (staff announcements)** Why: Rename to Staff Announcements, or bind notification preference settings if that was the intent. *(source: screens/P08-venue-back-office.yaml#BO-066; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Acknowledge announcement as a back-office action and publishedByPrincipalId / publishedAt as inputs (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Unacknowledged only | toggle | optional | — | — | — | Sends `?unacknowledgedOnly=` to `listAnnouncements`. | `listAnnouncements` ?unacknowledgedOnly |

**Form: Publish announcement** (modal, opened by *Publish announcement*; *Publish announcement* calls `publishAnnouncement`, *Cancel* sends nothing)

**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `locale`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `publishedByPrincipalId` (3 October 2026, CHG-SPF-001).

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

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Kind**: Operational / Safety / Emergency / HR / Celebration; choosing Emergency forces acknowledgement on and shows "This will take over staff phones". *(source: contracts/satellite/workforce.yaml#publishAnnouncement)*
- **Audience**: Venues, departments, roles as pickers with a live count of people reached. *(source: contracts/satellite/workforce.yaml#publishAnnouncement)*
- **Title, body, expiry, channels, locale**: Title max 140, body max 4000 with Arabic version; expiry date-time; channels In-app (always) and Push. *(source: contracts/satellite/workforce.yaml#publishAnnouncement)*

#### Outputs: what the screen shows and produces

**Shown**

**Every announcement** (data table, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Expires at | 1 Oct 2026, 14:30 | — |
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
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reach**: Targeted, delivered, acknowledged, outstanding - with the outstanding names listed first for emergencies. *(source: contracts/satellite/workforce.yaml#getAnnouncementReach)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Publish**: The publish gate names who will receive it and from when. *(source: screens/P08-venue-back-office.yaml#BO-066)*

**Data it reads**: `listAnnouncements` (onLoad, What staff have been told)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The notification settings list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the notification settings untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No notification settings yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on unacknowledgedOnly and the notification settings are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ANNOUNCEMENT_PUBLISH` for `publishAnnouncement`. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `EMP-038`: Broadcast to team on the Staff App uses the same kinds.
- Match `EMP-047`: Emergency mode on the Staff App is triggered by an emergency announcement.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
announcements:
- kind: Emergency
  title: Evacuate Adventure Zone via North Exit
  audience: Aqua Park - all staff
  reach: 212 targeted, 188 acknowledged, 24 outstanding
- kind: Operational
  title: Gate 3 exit-only from 17:00
  audience: Gate stewards
```

#### Permissions

- `listAnnouncements` → `WORKFORCE_VIEW` (read) · staff
- `publishAnnouncement` → `ANNOUNCEMENT_PUBLISH` (configure) · staff
- `getAnnouncementReach` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ANNOUNCEMENT_PUBLISH` for `publishAnnouncement`.

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

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-066` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-066?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish announcement, What publishing changes.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-084` Approval Inbox

**What is waiting on this person, sorted by what breaches soonest.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 1 · needs the `core` module |
| Block | Block A · ticket #28028 (VM-BO-084) |
| Who uses it | venue staff holding `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW` (2 operate, 1 read); in the flows as cashier, technician, venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `decideApprovalRequest` decides items that `listApprovalRequests` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `requestId` (deepLink), `approvalRequestId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/approvals/approval-inbox` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The approver's queue in Venue Management: everything waiting on this person (and, toggled, what they raised), sorted by what breaches its SLA soonest, with the decision taken in place. Empty is the good outcome. The one thing to get right: a decision that needs a second factor or a signature asks for it in the decision dialog, and the screen never implies the approval performs the action.

**Fixed on main** (the package already carries these; draw what it says): Table columns include rerouteOnNoApprover, outOfOfficeDelegateId, allowEmailApproval, reopenedFrom, subjectContract, subjectType, scopePath. (CHG-SBO-011); Status and kind filters are free text fields. (CHG-SBO-011); Tables show every schema field, plumbing included: 'Waiting for a decision' drop id, outOfOfficeDelegateId, reopenedFrom, subjectContract … (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Assigned to me | toggle | optional | — | — | — | Sends `?assignedToMe=` to `listApprovalRequests`. | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | optional | — | — | — | Sends `?raisedByMe=` to `listApprovalRequests`. | `listApprovalRequests` ?raisedByMe |
| Status | select | optional | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | — | The request status values in words, as chips; free text matched nothing. | `ApprovalRequest.status` |
| Kind | select | optional | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | — | The request kind values in words, as chips; free text matched nothing. | `ApprovalRequest.kind` |
| Breaching within minutes | number field (minutes) | optional | — | — | — | Sends `?breachingWithinMinutes=` to `listApprovalRequests`. | `listApprovalRequests` ?breachingWithinMinutes |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

**Form: Decide approval request** (modal, opened by *Decide approval request*; *Decide approval request* calls `decideApprovalRequest`, *Cancel* sends nothing)

**Collects what `decideApprovalRequest` sends before it is called.** Required: `decision`. Optional: `comment`, `reason`, `stepUpToken`, `signature`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Approve · Reject · Return · Request information | — | — | `decideApprovalRequest` body |
| Comment `comment` | text area | optional | — | max length 1000 | — | — | `decideApprovalRequest` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required on rejection. | `decideApprovalRequest` body |
| Step up token `stepUpToken` | text field | optional | — | — | — | Where the rule demands MFA (11.1.60). | `decideApprovalRequest` body |
| Signature `signature` | text field | optional | — | — | — | 11.1.57. Where the rule demands a digital signature. | `decideApprovalRequest` body |

Errors to draw in the form: 403 The approver may not decide this request. Always carries `refusedReason`, one value per cause — the approver is the requester (`approverIsRequester`), is not … (ApprovalRefusedProblem); 409 The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and … (ApprovalStateProblem)

**Form: Escalate approval request** (modal, opened by *Escalate approval request*; *Escalate approval request* calls `escalateApprovalRequest`, *Cancel* sends nothing)

**Collects what `escalateApprovalRequest` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 300 | — | — | `escalateApprovalRequest` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Filters**: Assigned to me on by default; Raised by me as the other tab. Kind and status are pick-lists of the approval kinds and statuses, never free text; Breaching within (minutes) as quick chips 15 / 60 / today. *(source: contracts/spine/approvals.yaml#listApprovalRequests)*
- **Decision comment and reason**: Reason required on reject (500 characters), comment optional on approve (1000) and encouraged: six months later it is the only record of why the exception was allowed. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **stepUpToken**: Never a visible field. It is what verifyMfaChallenge returns after the in-place challenge, short-lived and single-purpose; the form shows the challenge step, not a token box. *(source: contracts/spine/identity.yaml#verifyMfaChallenge)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listApprovalRequests`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Status | chip: Draft, Pending, Escalated, Returned, Information requested, Approved… | — |
| Summary | text | — |

**The selected approval request** (detail panel, from `listApprovalRequests`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Reroute on no approver | yes / no (icon or chip) | BL-154. An approver on leave is an approval that waits for them to come back. |
| Allow email approval | yes / no (icon or chip) | Approving from an email link with no second factor is the weakest path in the system, so it is off by default and available only below a … |
| Reopened from | the name it points at, never the id | Reopening a decided approval creates a new one that points back. Editing a decision in place destroys the record of what was originally … |
| Status | chip: Draft, Pending, Escalated, Returned, Information requested, Approved… | — |
| Subject contract | text | — |
| Subject type | text | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Decide approval request (primary button) | `decideApprovalRequest` POST `/approval-requests/{requestId}/decide` | inline | ApprovalRequest | 403 The approver may not decide this request. Always carries `refusedReason`, one value per cause — the approver is the requester (`approverIsRequester`), is not … (ApprovalRefusedProblem); 409 The request is no longer … | opens modal first |
| Escalate approval request (secondary button) | `escalateApprovalRequest` POST `/approval-requests/{requestId}/escalate` | inline | ApprovalRequest | — | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Queue rows**: Kind as words (Refund above threshold), the subject summary, amount with currency, requester name, venue, raised time and SLA remaining; overdue rows red and on top. AI risk band and priority shown as context only, never as an approve/reject suggestion. *(source: contracts/spine/approvals.yaml#listApprovalRequests; contracts/satellite/ai.yaml#getApprovalRequestScore)*
- **Money columns (amount)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Escalate**: Adds an approver above; the original stays in the chain. Requires a reason. *(source: contracts/spine/approvals.yaml#escalateApprovalRequest)*
- **Decide (Approve / Reject / Return / Request information)**: Four outcomes, not two: reject needs a reason the requester reads; return sends it back to amend; request information pauses the SLA clock. Approving records an authorisation and does not perform the action; on a multi-level chain the request moves to the next level. Where the rule demands MFA the decision carries a stepUpToken from the in-place challenge; where it demands a signature, the signature step comes first. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; F14 step 4)*

**Data it reads**: `listApprovalRequests` (onLoad, Requests awaiting a decision, or already decided); `getApprovalRequestScore` (onLoad, Risk band, priority and suggested escalation for the …)

**Where the user goes next**

- → `BO-052` Goods Receipt: *The goods arrive and are received*
- → `BO-087` Approval Delegations: *Approval Delegations*
- → `BO-364` Approval Command Center Dashboard: *Back to the approval command centre*
- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*
- → `BO-085` Approval Request: *Approves it*; carries `requestId`; calls `listApprovalRequests`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on assignedToMe, raisedByMe, status, kind, breachingWithinMinutes and the approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `APPROVAL_VIEW`, which `listApprovalRequests` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_DECIDE` for `decideApprovalRequest`; `APPROVAL_REQUEST` for `escalateApprovalRequest`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and … (ApprovalStateProblem) |

#### Edge cases to draw

- **The request was decided by someone else while open on screen**: The decision is refused 409 alreadyDecided; the row updates to who decided and how, nothing is lost. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for Decide approval request; APPROVAL_REQUEST for Escalate approval request. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 403**: Show it as something the person can act on, not a failure: The approver may not decide this request. **Always carries `refusedReason`**, one value per cause — the approver is the requester (`approverIsRequester`), is not in the resolved chain (`notInApproverChain`), lacks the permission the rule demands (`insufficientPermission`), gave no step-up token where the rule requires MFA (`mfaR... *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 409**: Show it as something the person can act on, not a failure: The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and `currentStatus` carries the status it is in. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **The approver raised the request, or sits outside the resolved chain**: Decide is refused 403 with refusedReason (approverIsRequester, notInApproverChain, missing permission or step-up); show the reason in words and who can decide instead. Segregation of duties survives delegation. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Consistency with other screens

- Match `BO-085`: Same decision dialog; BO-085 is the single request opened from a row or a deep link.
- Match `BO-365`: The workshop board's My Approval Inbox is the same queue; it must not be a second implementation.
- Match `POS-005`: A discount raised at the till appears here with the guest waiting (F14 step 3); the till learns the outcome on its own device.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- kind: Refund above threshold
  summary: Refund 4 tickets, order AQC-AUH-260930-0412
  amount: AED 1,180.00
  requester: Rahul Menon
  venue: AquaCove Abu Dhabi
  slaRemaining: 12 min
- kind: Discount override
  summary: 25% group discount, Desert Gate Tours
  amount: AED 3,400.00
  requester: Mariam Saeed
  venue: AquaCove Dubai
  slaRemaining: 2 h 40 min
- kind: Purchase order
  summary: Compressor for wave machine 2
  amount: AED 18,200.00
  requester: Joseph D'Souza
  venue: AquaCove Abu Dhabi
  slaRemaining: Breached 25 min ago
```

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public
- `decideApprovalRequest` → `APPROVAL_DECIDE` (operate) · staff, public
- `escalateApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `getApprovalRequestScore` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `APPROVAL_VIEW`, which `listApprovalRequests` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_DECIDE` for `decideApprovalRequest`; `APPROVAL_REQUEST` for `escalateApprovalRequest`.

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 11.1.20 | Approval Comments - System shall allow approvers to add comments to approval decisions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.21 | Approval Rejection Reasons - System shall require rejection reasons when approvals are denied. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.57 | Digital Signature Support - System shall support digital signatures for sensitive approvals. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.59 | Approval Authentication - System shall require authentication before approval actions are executed. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.60 | MFA-Protected Approvals - System shall support MFA requirements for sensitive approval actions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-084` · status **notStarted** · provenance generated
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 2: Works in My Approval Inbox → Provide each approver with their personal actionable queue.
- Flow F14 *A discount needs a manager*, step 3: The manager sees it in their inbox → Sorted by what breaches soonest, and this one has a guest waiting
- Flow F15 *A part is needed and ordered*, step 3: A manager approves it → Value-based routing — a bearing and a compressor are not the same decision
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 2: Works in Unified Approval Inbox & Decision Workspace → Provide users with one approval inbox across all TICVAI modules. This is extremely important. A manager should not need to open Finance for one approval, Pricing for another, Procurement for another …
- Flow F14 branch at step 3 (recoverable): when The manager is on the shop floor, Mobile approval — `EMP-037` on the staff app. A manager who must return to an office to approve a discount is a queue at the till.
- Flow F15 branch at step 3 (recoverable): when The requisition is returned for more information, **Not a rejection.** The technician amends and resubmits without starting again, which is why `approveRequisition` has a return decision (CHG-SPF-010).

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-084?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Decide approval request, Escalate approval request.
- [ ] Every transition is wired: `BO-052`, `BO-087`, `BO-364`, `ADM-248`, `BO-085`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 6 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-085` Approval Request

**One request, its subject, and the decision.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 1 · needs the `core` module |
| Block | Block A · ticket #27830 (VM-BO-085) |
| Who uses it | venue staff holding `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW` (2 operate, 1 read); in the flows as cashier |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): One request opened by `requestId`: its subject, its trail and the decision. The queue is BO-084 (design-note correction, 2 October 2026). |
| Offline | online only |
| Opens with | `requestId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/approvals/approval-request` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Cross-platform navigation removed 24 August**: POS-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **The single request is read with getApprovalRequest (agreed, ledger) 4 October 2026; listApprovalRequests has no id filter** (CHG-FXS-003)

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): evaluateApprovalRequirement answers "does this need approval, and from whom" for the raising screen (till, purchase order) before a request exists; it has no …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** One approval request opened from the inbox or a deep link (email approval): its subject with the evidence, the chain (who has decided, who is next), the matrix version it was raised under, and the decision. A requester sees the same page with Withdraw and, after a rejection, Resubmit. It should be a detail page, not a second queue.

**Fixed on main** (the package already carries these; draw what it says): Pattern approvalInbox with the full queue table and filters, the same layout as BO-084. (CHG-SBO-011); "Evaluate approval requirement" is a button for the approver. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Waiting for a decision' drop id, outOfOfficeDelegateId, reopenedFrom, subjectContract … (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

**Form: Decide approval request** (modal, opened by *Decide approval request*; *Decide approval request* calls `decideApprovalRequest`, *Cancel* sends nothing)

**Collects what `decideApprovalRequest` sends before it is called.** Required: `decision`. Optional: `comment`, `reason`, `stepUpToken`, `signature`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Approve · Reject · Return · Request information | — | — | `decideApprovalRequest` body |
| Comment `comment` | text area | optional | — | max length 1000 | — | — | `decideApprovalRequest` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required on rejection. | `decideApprovalRequest` body |
| Step up token `stepUpToken` | text field | optional | — | — | — | Where the rule demands MFA (11.1.60). | `decideApprovalRequest` body |
| Signature `signature` | text field | optional | — | — | — | 11.1.57. Where the rule demands a digital signature. | `decideApprovalRequest` body |

Errors to draw in the form: 403 The approver may not decide this request. Always carries `refusedReason`, one value per cause — the approver is the requester (`approverIsRequester`), is not … (ApprovalRefusedProblem); 409 The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and … (ApprovalStateProblem)

**Form: Resubmit approval request** (modal, opened by *Resubmit approval request*; *Resubmit approval request* calls `resubmitApprovalRequest`, *Cancel* sends nothing)

**Collects what `resubmitApprovalRequest` sends before it is called.** Required: `changes`. Optional: `amount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Changes `changes` | text area | required | — | max length 1000 | — | What was changed in response to the rejection | `resubmitApprovalRequest` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `resubmitApprovalRequest` body |

**Sent by *Withdraw approval request*** (`withdrawApprovalRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 300 | — | — | `withdrawApprovalRequest` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **stepUpToken**: Never a visible field. It is what verifyMfaChallenge returns after the in-place challenge, short-lived and single-purpose; the form shows the challenge step, not a token box. *(source: contracts/spine/identity.yaml#verifyMfaChallenge)*

#### Outputs: what the screen shows and produces

**Shown**

**The request** (detail panel, from `getApprovalRequest`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Status | chip: Draft, Pending, Escalated, Returned, Information requested, Approved… | — |
| Requested by principal | the name it points at, never the id | — |
| Requested at | 1 Oct 2026, 14:30 | — |

**The request** (detail panel, from `listApprovalRequests`): Read with `listApprovalRequests` filtered to the one `requestId` (no single-request read exists).

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Status | chip: Draft, Pending, Escalated, Returned, Information requested, Approved… | — |
| Subject | text | — |
| Summary | text | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Justification | text | — |
| Requested by principal | the name it points at, never the id | — |
| Matrix version | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Decide approval request (primary button) | `decideApprovalRequest` POST `/approval-requests/{requestId}/decide` | inline | ApprovalRequest | 403 The approver may not decide this request. Always carries `refusedReason`, one value per cause — the approver is the requester (`approverIsRequester`), is not … (ApprovalRefusedProblem); 409 The request is no longer … | opens modal first |
| Resubmit approval request (secondary button) | `resubmitApprovalRequest` POST `/approval-requests/{requestId}/resubmit` | inline | ApprovalRequest | — | opens modal first |
| Withdraw approval request (destructive button) | `withdrawApprovalRequest` POST `/approval-requests/{requestId}/withdraw` | inline | ApprovalRequest | 409 Already decided. `refusedReason` is `alreadyDecided` and `currentStatus` says whether it was approved or rejected. (ApprovalStateProblem) | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Subject and evidence**: The business object being approved (e.g. the refund with order lines, original payment and the guest), amount with currency, justification, and attachments, so the approver decides without leaving the page. *(source: contracts/spine/approvals.yaml#listApprovalRequests; F14 step 4)*
- **Chain and version**: Levels in order with each decision, decider and time; "raised under matrix v4" shown, because the request is decided by the rules it was raised under. *(source: contracts/spine/approvals.yaml#setApprovalMatrix; R129)*
- **Money columns (amount)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Withdraw (requester)**: Takes it back with an optional reason; it does not count as a rejection. Refused 409 once decided, with the outcome. *(source: contracts/spine/approvals.yaml#withdrawApprovalRequest)*
- **Resubmit (after rejection)**: Creates a new request linked to the rejected one, asking what changed; the rejection stays in the record. *(source: contracts/spine/approvals.yaml#resubmitApprovalRequest)*
- **Decide (Approve / Reject / Return / Request information)**: Four outcomes, not two: reject needs a reason the requester reads; return sends it back to amend; request information pauses the SLA clock. Approving records an authorisation and does not perform the action; on a multi-level chain the request moves to the next level. Where the rule demands MFA the decision carries a stepUpToken from the in-place challenge; where it demands a signature, the signature step comes first. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; F14 step 4)*

**Data it reads**: `listApprovalRequests` (onLoad, Requests awaiting a decision, or already decided); `getApprovalRequest` (onLoad, The one request the screen opens on (requestId): agreed …)

**Where the user goes next**

- → `BO-084` Approval Inbox: *Approval Inbox*; carries `approvalRequestId`, `requestId`
- → `BO-087` Approval Delegations: *Approval Delegations*
- → `POS-005` Payment: *The till applies it and completes the sale*; calls `decideApprovalRequest`

**What opens over it**

- confirmDialog *Withdraw approval request*: **Names what `withdrawApprovalRequest` changes and what it leaves alone**, in the consequence rather than the verb. A approval request this affects should be identified in the dialog, not just counted. **Collects what `withdrawApprovalRequest` sends before it is called.** Nothing in the body is …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval request list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval request untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: the screen opens one request. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `APPROVAL_VIEW`, which `listApprovalRequests` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_DECIDE` for `decideApprovalRequest`; `APPROVAL_REQUEST` for `resubmitApprovalRequest`, `withdrawApprovalRequest`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already decided. `refusedReason` is `alreadyDecided` and `currentStatus` says whether it was approved or rejected. (ApprovalStateProblem); 409 The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and … (ApprovalStateProblem) |

#### Edge cases to draw

- **Opened from an email link after the request expired**: Shows the request read-only with "Expired at 14:00, no decision recorded" and no decision buttons. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for Decide approval request; APPROVAL_REQUEST for Resubmit approval request, Withdraw approval request. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 403**: Show it as something the person can act on, not a failure: The approver may not decide this request. **Always carries `refusedReason`**, one value per cause — the approver is the requester (`approverIsRequester`), is not in the resolved chain (`notInApproverChain`), lacks the permission the rule demands (`insufficientPermission`), gave no step-up token where the rule requires MFA (`mfaR... *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 409**: Show it as something the person can act on, not a failure: The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and `currentStatus` carries the status it is in. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **withdrawApprovalRequest answers 409**: Show it as something the person can act on, not a failure: Already decided. `refusedReason` is `alreadyDecided` and `currentStatus` says whether it was approved or rejected. *(source: contracts/spine/approvals.yaml#withdrawApprovalRequest)*
- **The approver raised the request, or sits outside the resolved chain**: Decide is refused 403 with refusedReason (approverIsRequester, notInApproverChain, missing permission or step-up); show the reason in words and who can decide instead. Segregation of duties survives delegation. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Consistency with other screens

- Match `BO-084`: Same decision dialog and refusal wording.
- Match `BO-367`: The workshop's Approval Request Detail is this page; one implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request:
  ref: APR-2026-004812
  kind: Refund above threshold
  amount: AED 1,180.00
  requester: Rahul Menon, Main Gate Till 3
  justification: Guest charged twice at Main Gate Till 3
  matrixVersion: 4
chain:
- 'Level 1 Supervisor: Omar Haddad, approved 10:12'
- 'Level 2 Venue Manager: Fatima Al Mansoori, waiting'
```

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public
- `decideApprovalRequest` → `APPROVAL_DECIDE` (operate) · staff, public
- `resubmitApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `withdrawApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `getApprovalRequest` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `APPROVAL_VIEW`, which `listApprovalRequests` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_DECIDE` for `decideApprovalRequest`; `APPROVAL_REQUEST` for `resubmitApprovalRequest`, `withdrawApprovalRequest`.

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 11.1.20 | Approval Comments - System shall allow approvers to add comments to approval decisions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.21 | Approval Rejection Reasons - System shall require rejection reasons when approvals are denied. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.57 | Digital Signature Support - System shall support digital signatures for sensitive approvals. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.59 | Approval Authentication - System shall require authentication before approval actions are executed. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.60 | MFA-Protected Approvals - System shall support MFA requirements for sensitive approval actions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-085` · status **notStarted** · provenance generated
- Flow F14 *A discount needs a manager*, step 4: Approves it → Recorded with who and why. **The approval does not apply the discount**
- Flow F14 branch at step 4 (requiresStaff): when The manager is the cashier, **Refused.** Segregation of duties survives a busy Saturday, and the cashier must find someone else.
- Flow F14 branch at step 4 (recoverable): when It breaches the SLA, Escalates to the next level. At a till the SLA is minutes, not hours, and the escalation is what stops a guest waiting for someone in a meeting.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-085?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Decide approval request, Resubmit approval request, Withdraw approval request.
- [ ] Every transition is wired: `BO-084`, `BO-087`, `POS-005`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 7 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-086` Approval Matrix

**What needs approval here, and who grants it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 2 · needs the `core` module |
| Block | Block B · ticket #29421 (VM-BO-086) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listApprovalMatrices` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/approvals/approval-matrix` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What needs approval at this level and who grants it: ordered rules per kind (threshold, levels, approver role, parallel or sequential, SLA). A venue sets only its own matrix and may only tighten what the tenant or region set.

**Fixed on main** (the package already carries these; draw what it says): Tables show every schema field, plumbing included: 'Every approval matrix' drop id, scopePath. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Kind | select | optional | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | — | Sends `?kind=` to `listApprovalMatrices`. | `listApprovalMatrices` ?kind |
| Effective | toggle | optional | off | — | — | Sends `?effective=` to `listApprovalMatrices`. | `listApprovalMatrices` ?effective |

**Form: Save approval matrix** (modal, opened by *Save approval matrix*; *Save approval matrix* calls `setApprovalMatrix`, *Cancel* sends nothing)

**Collects what `setApprovalMatrix` sends before it is called.** Required: `kind`, `scopeLevel`, `rules`. Optional: `isActive`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | — | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. | `setApprovalMatrix` body |
| Scope level `scopeLevel` | segmented control | required | — | Tenant · Region · Venue | — | — | `setApprovalMatrix` body |
| Rules `rules` | repeatable rows | required | — | — | — | — | `setApprovalMatrix` body |
| Order `rules[].order` | number field | required | — | — | — | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about. | `setApprovalMatrix` body |
| Min amount `rules[].minAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setApprovalMatrix` body |
| Max amount `rules[].maxAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setApprovalMatrix` body |
| Risk score above `rules[].riskScoreAbove` | number field | optional | — | — | — | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). | `setApprovalMatrix` body |
| Condition `rules[].condition` | text field | optional | — | — | — | 11.1.13. Evaluated against the attributes the caller supplied. | `setApprovalMatrix` body |
| Approver roles `rules[].approverRoleIds` | multi-picker: choose approver roles | required | — | at least 1 | — | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. | `setApprovalMatrix` body |
| Approver scope level `rules[].approverScopeLevel` | radio group | optional | — | Venue · Department · Region · Tenant | — | 11.1.39. Which organisational level the approver must sit at. | `setApprovalMatrix` body |
| Mode `rules[].mode` | radio group | required | — | Sequential · Parallel · Consensus · Majority | — | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. | `setApprovalMatrix` body |
| Levels `rules[].levels` | number field | optional | 1 | — | — | 11.1.3. Multi-level chains ask each level in turn. | `setApprovalMatrix` body |
| Requires MFA `rules[].requiresMfa` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Requires signature `rules[].requiresSignature` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Sla minutes `rules[].slaMinutes` | number field (minutes) | optional | — | — | — | 11.1.14. Null means no SLA, which is different from a long one. | `setApprovalMatrix` body |
| Escalate after minutes `rules[].escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setApprovalMatrix` body |
| Escalate to roles `rules[].escalateToRoleIds` | multi-picker: choose escalate to roles | optional | — | — | — | Role ids from `identity.listRoles`, as `approverRoleIds`. | `setApprovalMatrix` body |
| Expires after minutes `rules[].expiresAfterMinutes` | number field (minutes) | optional | — | — | — | 11.1.53. An unanswered request eventually stops waiting. | `setApprovalMatrix` body |
| Subject types `rules[].subjectTypes` | list of values (chips) | optional | — | — | — | Which subjects of the kind this rule matches (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example … | `setApprovalMatrix` body |
| Signature methods `rules[].signatureMethods` | multi-select chips | optional | — | Platform key · Uae pass · External certificate · Drawn signature | — | The signature methods this level accepts, where `requiresSignature` is true (design-notes correction on ADM-344, Block B: "Configuring which stages need a signature is a policy … | `setApprovalMatrix` body |
| External provider `rules[].externalProviderId` | picker: choose an external provider | optional | — | — | shows names, sends the id | 11.1.65 (29 September). This level is decided in an external workflow system (`ApprovalExternalProvider`) rather than by a person in TICVAI. | `setApprovalMatrix` body |
| Code `rules[].code` | text field | optional | — | max length 64 | — | A stable code for the rule, unique within its matrix (4 October 2026, CHG-FXC-005). | `setApprovalMatrix` body |
| Minimum approvals `rules[].minimumApprovals` | number field | optional | — | min 1 | — | N in N-of-M (CHG-FXC-005). Null means every approver the mode asks. | `setApprovalMatrix` body |
| Required approver role `rules[].requiredApproverRoleId` | picker: choose a required approver role | optional | — | — | shows names, sends the id | A role that must be among the approvals whatever N is (the CFO in an N-of-M group); it is also one of `approverRoleIds` (CHG-FXC-005). | `setApprovalMatrix` body |
| Rejection behavior `rules[].rejectionBehavior` | segmented control | optional | — | Reject request · Return to previous level · Return to requester | — | What a rejection at this rule does; null is `rejectRequest` (CHG-FXC-005). | `setApprovalMatrix` body |
| Allow request changes `rules[].allowRequestChanges` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Allow delegate `rules[].allowDelegate` | toggle | optional | on | — | — | — | `setApprovalMatrix` body |
| Allow reassign `rules[].allowReassign` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Min percentage `rules[].minPercentage` | number field | optional | — | — | — | A percentage threshold (a discount or a margin impact) at or above which the rule applies, beside `minAmount` (CHG-FXC-005). | `setApprovalMatrix` body |
| Match attributes `rules[].matchAttributes` | key and value settings | optional | — | — | — | The request attributes a rule matches on (CHG-FXC-005): keys `module`, `product`, `department`, `customerType`, `risk`, `exceptionType`, `legalEntity`, each an exact value the … | `setApprovalMatrix` body |
| Composite mode `rules[].compositeMode` | select | optional | — | Single · Sequential · Parallel · Any one · All must approve · Conditional · Multi level | — | The `approvalMode` the composite screen sent, kept so it reads back what it saved; `mode`, `levels` and `minimumApprovals` are what the engine runs (CHG-FXC-005). | `setApprovalMatrix` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `setApprovalMatrix` body |

Errors to draw in the form: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem)

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalMatrix: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalMatrix)*
- **Approval matrix rules**: Ordered; the first matching rule wins. A venue may tighten and never loosen a rule from above: a higher threshold, fewer approvers or a different approver role are each loosening and refused 409 loosensParentRule. Saving creates a new version; requests in flight keep the version they were raised under. *(source: contracts/spine/approvals.yaml#setApprovalMatrix; R129; R183)*

#### Outputs: what the screen shows and produces

**Shown**

**Every approval matrix** (data table, from `listApprovalMatrices`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Scope level | chip: Tenant, Region, Venue | — |
| Rules | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**The selected approval matrix** (detail panel, from `listApprovalMatrices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Scope level | chip: Tenant, Region, Venue | — |
| Scope path | text | — |
| Rules | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save approval matrix (primary button) | `setApprovalMatrix` PUT `/approval-matrices` | ApprovalMatrix | ApprovalMatrix | 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which … | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Inherited rules**: Rules from above are shown read-only above the venue's own, with "tighter than tenant" or "inherited" per rule. *(source: R129; R183; contracts/spine/approvals.yaml#setApprovalMatrix)*
- **Version**: Each save is a new version; requests in flight show the version they were raised under. *(source: contracts/spine/approvals.yaml#setApprovalMatrix)*

**Data it reads**: `listApprovalMatrices` (onLoad, What requires approval here)

**Where the user goes next**

- → `BO-084` Approval Inbox: *Approval Inbox*
- → `BO-085` Approval Request: *Approval Request*
- → `BO-087` Approval Delegations: *Approval Delegations*
- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on kind, effective and the approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `APPROVAL_CONFIGURE`, which `listApprovalMatrices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **setApprovalMatrix answers 409**: Show it as something the person can act on, not a failure: Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold, fewer approvers or a different approver role; audit R129); or `unreachableRule` — a rule can never match because an earlier one always does. `ruleOrder` names the offending r... *(source: contracts/spine/approvals.yaml#setApprovalMatrix)*

#### Consistency with other screens

- Match `BO-639`: Reviewer assignment for accreditation uses this same matrix operation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
  kind: Refund above threshold
  rules:
  - order: 1
    minAmount: AED 500.00
    levels: 1
    approverRole: Supervisor
    sla: 15 min
  - order: 2
    minAmount: AED 2,000.00
    levels: 2
    approverRole: Supervisor then Venue Manager
    sla: 1 h
```

#### Permissions

- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `APPROVAL_CONFIGURE`, which `listApprovalMatrices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

49 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
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
| 11.1.4 | Role-Based Approval Routing System shall automatically route approval requests based on organizational hierarchy and user roles. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.5 | Escalation Rules System shall automatically escalate pending approvals after configurable time thresholds. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| … 37 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-086` · status **notStarted** · provenance generated
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 8: Works in Approval Matrix & Multi-Level Approval Configuration → Configure when approvals are required and who must approve.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (34), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-086?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save approval matrix.
- [ ] Every transition is wired: `BO-084`, `BO-085`, `BO-087`, `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-087` Approval Delegations

**Who is standing in for whom, and until when.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | People & Access Rights · wave 2 · needs the `core` module |
| Block | Block A · ticket #27939 (APP-SETUP-BO-087) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_VIEW` (1 configure, 1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listApprovalDelegations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `delegationId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/approvals/approval-delegations` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **ADM-243 (merged into BO-087 as a section on 2 October) brings its bindings: the approval matrices are read with listApprovalMatrices and saved with setApprovalMatrix (the plan builds them on APP-SETUP-BO-087; ledger, 4 October 2026)** (CHG-FXS-002)

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Who stands in for whom, for which kinds of approval, up to what amount and until when. An approver going on leave sets a delegate here; a manager sees all delegations in their venues. Every delegation is time-bounded and can only hand over authority the delegator actually has.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- createApprovalDelegation is gated by APPROVAL_DECIDE with an escalated permission APPROVAL_DELEGATE; nothing says who holds APPROVAL_DELEGATE or what escalates. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Tables show every schema field, plumbing included: 'Every approval delegation' drop id, delegatorPrincipalId, delegatePrincipalId … (CHG-SBO-004).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |

**Form: Create approval delegation** (modal, opened by *Create approval delegation*; *Create approval delegation* calls `createApprovalDelegation`, *Cancel* sends nothing)

**Collects what `createApprovalDelegation` sends before it is called.** Required: `delegatorPrincipalId`, `delegatePrincipalId`, `from`, `to`. Optional: `kinds`, `maxAmount`, `reason`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `isActive` (3 October 2026, CHG-SPF-001).

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
| Delegation type `delegationType` | text field | optional | — | — | — | The composite screen's `delegationType` (planned absence, temporary cover ...), for display and reporting; the engine treats every delegation alike (4 October 2026, CHG-FXC-005). | `createApprovalDelegation` body |
| Max percentage `maxPercentage` | number field | optional | — | — | — | A percentage cap beside `maxAmount` (the composite's `authorityPercentage`, CHG-FXC-005). | `createApprovalDelegation` body |
| Required role `requiredRoleId` | picker: choose a required role | optional | — | — | shows names, sends the id | A role the delegate must hold for the delegation to act (the composite's `requiredRole`); checked when the delegate decides, refused with 409 at creation where the delegate does … | `createApprovalDelegation` body |

Errors to draw in the form: 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 403 The delegation would hand over authority that is not there. `refusedReason` is `delegateLacksPermission` where the delegate does not hold the permission being … (DelegationRefusedProblem)

**Form: Save approval limits** (modal, opened by *Save approval limits*; *Save approval limits* calls `setApprovalMatrix`, *Cancel* sends nothing)

**Collects what `setApprovalMatrix` sends before it is called.** Required: `kind`, `scopeLevel`, `rules` (each with `order`, `approverRoleIds`, `mode`; optional amount band, risk score, levels, MFA). Optional: `isActive`. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | — | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. | `setApprovalMatrix` body |
| Scope level `scopeLevel` | segmented control | required | — | Tenant · Region · Venue | — | — | `setApprovalMatrix` body |
| Rules `rules` | repeatable rows | required | — | — | — | — | `setApprovalMatrix` body |
| Order `rules[].order` | number field | required | — | — | — | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about. | `setApprovalMatrix` body |
| Min amount `rules[].minAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setApprovalMatrix` body |
| Max amount `rules[].maxAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setApprovalMatrix` body |
| Risk score above `rules[].riskScoreAbove` | number field | optional | — | — | — | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). | `setApprovalMatrix` body |
| Condition `rules[].condition` | text field | optional | — | — | — | 11.1.13. Evaluated against the attributes the caller supplied. | `setApprovalMatrix` body |
| Approver roles `rules[].approverRoleIds` | multi-picker: choose approver roles | required | — | at least 1 | — | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. | `setApprovalMatrix` body |
| Approver scope level `rules[].approverScopeLevel` | radio group | optional | — | Venue · Department · Region · Tenant | — | 11.1.39. Which organisational level the approver must sit at. | `setApprovalMatrix` body |
| Mode `rules[].mode` | radio group | required | — | Sequential · Parallel · Consensus · Majority | — | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. | `setApprovalMatrix` body |
| Levels `rules[].levels` | number field | optional | 1 | — | — | 11.1.3. Multi-level chains ask each level in turn. | `setApprovalMatrix` body |
| Requires MFA `rules[].requiresMfa` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Requires signature `rules[].requiresSignature` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Sla minutes `rules[].slaMinutes` | number field (minutes) | optional | — | — | — | 11.1.14. Null means no SLA, which is different from a long one. | `setApprovalMatrix` body |
| Escalate after minutes `rules[].escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setApprovalMatrix` body |
| Escalate to roles `rules[].escalateToRoleIds` | multi-picker: choose escalate to roles | optional | — | — | — | Role ids from `identity.listRoles`, as `approverRoleIds`. | `setApprovalMatrix` body |
| Expires after minutes `rules[].expiresAfterMinutes` | number field (minutes) | optional | — | — | — | 11.1.53. An unanswered request eventually stops waiting. | `setApprovalMatrix` body |
| Subject types `rules[].subjectTypes` | list of values (chips) | optional | — | — | — | Which subjects of the kind this rule matches (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example … | `setApprovalMatrix` body |
| Signature methods `rules[].signatureMethods` | multi-select chips | optional | — | Platform key · Uae pass · External certificate · Drawn signature | — | The signature methods this level accepts, where `requiresSignature` is true (design-notes correction on ADM-344, Block B: "Configuring which stages need a signature is a policy … | `setApprovalMatrix` body |
| External provider `rules[].externalProviderId` | picker: choose an external provider | optional | — | — | shows names, sends the id | 11.1.65 (29 September). This level is decided in an external workflow system (`ApprovalExternalProvider`) rather than by a person in TICVAI. | `setApprovalMatrix` body |
| Code `rules[].code` | text field | optional | — | max length 64 | — | A stable code for the rule, unique within its matrix (4 October 2026, CHG-FXC-005). | `setApprovalMatrix` body |
| Minimum approvals `rules[].minimumApprovals` | number field | optional | — | min 1 | — | N in N-of-M (CHG-FXC-005). Null means every approver the mode asks. | `setApprovalMatrix` body |
| Required approver role `rules[].requiredApproverRoleId` | picker: choose a required approver role | optional | — | — | shows names, sends the id | A role that must be among the approvals whatever N is (the CFO in an N-of-M group); it is also one of `approverRoleIds` (CHG-FXC-005). | `setApprovalMatrix` body |
| Rejection behavior `rules[].rejectionBehavior` | segmented control | optional | — | Reject request · Return to previous level · Return to requester | — | What a rejection at this rule does; null is `rejectRequest` (CHG-FXC-005). | `setApprovalMatrix` body |
| Allow request changes `rules[].allowRequestChanges` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Allow delegate `rules[].allowDelegate` | toggle | optional | on | — | — | — | `setApprovalMatrix` body |
| Allow reassign `rules[].allowReassign` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Min percentage `rules[].minPercentage` | number field | optional | — | — | — | A percentage threshold (a discount or a margin impact) at or above which the rule applies, beside `minAmount` (CHG-FXC-005). | `setApprovalMatrix` body |
| Match attributes `rules[].matchAttributes` | key and value settings | optional | — | — | — | The request attributes a rule matches on (CHG-FXC-005): keys `module`, `product`, `department`, `customerType`, `risk`, `exceptionType`, `legalEntity`, each an exact value the … | `setApprovalMatrix` body |
| Composite mode `rules[].compositeMode` | select | optional | — | Single · Sequential · Parallel · Any one · All must approve · Conditional · Multi level | — | The `approvalMode` the composite screen sent, kept so it reads back what it saved; `mode`, `levels` and `minimumApprovals` are what the engine runs (CHG-FXC-005). | `setApprovalMatrix` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `setApprovalMatrix` body |

Errors to draw in the form: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem)

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Delegation window and limits**: Always time-bounded: 'to' must follow 'from' (refused invalidWindow); the delegate cannot exceed the delegator's kinds or maxAmount and must hold the permission (exceedsDelegatorAuthority, delegateLacksPermission); a delegate never approves a request the delegator raised. *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Outputs: what the screen shows and produces

**Shown**

**Every approval delegation** (data table, from `listApprovalDelegations`)

| Shows | Format | Notes |
|---|---|---|
| Kinds | list or chips (count when long) | Absent means everything the delegator may approve. |
| Max amount | AED 1,234.50 | A delegate may be given less authority than the delegator, never more. |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | Required. An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it. |
| Reason | text | — |
| Is active | yes / no (icon or chip) | — |

**Approval limits** (data table, from `listApprovalMatrices`): ADM-243's section: one matrix per approval kind and scope.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Scope level | chip: Tenant, Region, Venue | — |
| Version | 1,234 | 11.1.80. A request is decided by the rules it was raised under. |
| Is active | yes / no (icon or chip) | — |

**Rules of the selected matrix** (data table, from `listApprovalMatrices`)

| Shows | Format | Notes |
|---|---|---|
| Order | 1,234 | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason … |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approver roles | list or chips (count when long) | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Requires MFA | yes / no (icon or chip) | — |

**The selected approval delegation** (detail panel, from `listApprovalDelegations`)

| Shows | Format | Notes |
|---|---|---|
| Kinds | list or chips (count when long) | Absent means everything the delegator may approve. |
| Max amount | AED 1,234.50 | A delegate may be given less authority than the delegator, never more. |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | Required. An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it. |
| Reason | text | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create approval delegation (primary button) | `createApprovalDelegation` POST `/delegations` | ApprovalDelegation | ApprovalDelegation | 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 403 The delegation would hand … | opens modal first |
| Revoke approval delegation (destructive button) | `revokeApprovalDelegation` DELETE `/delegations/{delegationId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save approval limits (secondary button) | `setApprovalMatrix` PUT `/approval-matrices` | ApprovalMatrix | ApprovalMatrix | 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which … | gated `APPROVAL_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Delegation rows**: Delegator and delegate by name (never ids), kinds as words or "Everything I may approve", limit with currency, window in the venue's dates, and a state chip: scheduled, active, ended, revoked. *(source: contracts/spine/approvals.yaml#listApprovalDelegations)*
- **Money columns (maxAmount)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Revoke**: Ends it now; requests already decided by the delegate stand; open requests return to the delegator. Confirmation names both people. *(source: contracts/spine/approvals.yaml#revokeApprovalDelegation)*

**Data it reads**: `listApprovalDelegations` (onLoad, Who is standing in for whom); `listApprovalMatrices` (onLoad, The approval matrices (ADM-243's section, merged here on 2 …)

**Where the user goes next**

- → `BO-084` Approval Inbox: *Approval Inbox*
- → `BO-085` Approval Request: *Approval Request*

**What opens over it**

- confirmDialog *Revoke approval delegation*: **Names what `revokeApprovalDelegation` changes and what it leaves alone**, in the consequence rather than the verb. A approval delegations this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval delegations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval delegations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval delegations yet. Offers Create approval delegation (`createApprovalDelegation`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listApprovalDelegations` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `APPROVAL_VIEW`, which `listApprovalDelegations` requires to show this screen, and names that permission (the screen's other reads need `APPROVAL_CONFIGURE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_DECIDE` for `createApprovalDelegation` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says … |

#### Edge cases to draw

- **Delegating to someone who lacks the permission**: Refused 403 delegateLacksPermission; the people picker should already grey out principals without it. *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*
- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for Create approval delegation, Revoke approval delegation. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*
- **createApprovalDelegation answers 403**: Show it as something the person can act on, not a failure: The delegation would hand over authority that is not there. `refusedReason` is `delegateLacksPermission` where the delegate does not hold the permission being delegated, or `exceedsDelegatorAuthority` where `kinds` or `maxAmount` go beyond what the delegator may approve. The shared `Forbidden`, with no `refusedReason`, is the ca... *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Consistency with other screens

- Match `BO-385`: The board's Delegation Management is the same function; one implementation.
- Match `BO-387`: Out-of-office routing reads these delegations.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
delegations:
- delegator: Fatima Al Mansoori
  delegate: Omar Haddad
  kinds:
  - Refund above threshold
  - Discount override
  maxAmount: AED 5,000.00
  from: 05/10/2026
  to: 12/10/2026
  state: scheduled
```

#### Permissions

- `listApprovalDelegations` → `APPROVAL_VIEW` (read) · staff
- `createApprovalDelegation` → `APPROVAL_DECIDE` (operate) · staff
- `revokeApprovalDelegation` → `APPROVAL_DECIDE` (operate) · staff
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `APPROVAL_VIEW`, which `listApprovalDelegations` requires to show this screen, and names that permission (the screen's other reads need `APPROVAL_CONFIGURE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_DECIDE` for `createApprovalDelegation` …

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

Also apply: 2 for P08 · People & Access Rights, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-087` · status **notStarted** · provenance generated
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (43), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-087?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create approval delegation, Revoke approval delegation, Save approval limits.
- [ ] Every transition is wired: `BO-084`, `BO-085`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
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

### In P08 · People & Access Rights

- No role or permission is predefined: any privilege, including refund approval, can be assigned to any custom role. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-255)*
- Rights can be set at site, operating area (department, e.g. B2B, B2C, OTA, on-site POS, finance), workstation, role or user level; site-level settings (password policy, UI rights, configuration rights) cascade to everything beneath. *(agreed · MoM 7 Aug 2026, 2. System Organization: Tenant & Site Setup · DI-148)*

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"amendAttendance": {"method":"POST","path":"/attendance/{recordId}/amend","contract":"workforce","summary":"A supervisor corrects a record","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"createApprovalDelegation": {"method":"POST","path":"/delegations","contract":"approvals","summary":"Delegate approval authority","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalDelegation","responds":"ApprovalDelegation"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createPrincipal": {"method":"POST","path":"/principals","contract":"identity","summary":"Create a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePrincipalRequest","responds":"Principal"},
"createRole": {"method":"POST","path":"/roles","contract":"identity","summary":"Create a role","permission":"ROLE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Role"},
"createRotaAssignment": {"method":"POST","path":"/rota-assignments","contract":"workforce","summary":"Put someone on the rota","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RotaAssignment","responds":"RotaAssignment"},
"decideApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/decide","contract":"approvals","summary":"Approve, reject, return or ask for information","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"escalateApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/escalate","contract":"approvals","summary":"Move it up a level","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"forceLogout": {"method":"POST","path":"/auth/sessions/{sessionId}/force-logout","contract":"identity","summary":"Supervisor termination of an abandoned session","permission":"SESSION_FORCE_LOGOUT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"sessionId","in":"path","required":true}],"requestBody":null,"responds":null},
"getAnnouncementReach": {"method":"GET","path":"/announcements/{announcementId}/reach","contract":"workforce","summary":"Who has acknowledged, and who has not","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AnnouncementReach"},
"getApprovalRequest": {"method":"GET","path":"/approval-requests/{requestId}","contract":"approvals","summary":"One approval request","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"requestId","in":"path","required":true}],"requestBody":null,"responds":"ApprovalRequest"},
"getApprovalRequestScore": {"method":"GET","path":"/approval-requests/{approvalRequestId}/score","contract":"ai","summary":"The latest context score of an approval request","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiApprovalRequestScore"},
"getPrincipal": {"method":"GET","path":"/principals/{principalId}","contract":"identity","summary":"Read a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Principal"},
"listAccessReviewCampaigns": {"method":"GET","path":"/access-review-campaigns","contract":"identity","summary":"Access review campaigns, open first","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccessReviewItems": {"method":"GET","path":"/access-review-campaigns/{campaignId}/items","contract":"identity","summary":"The grants a campaign asks somebody to certify or revoke","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"assignedToMe","in":"query","required":null},{"name":"findingKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listActiveSessions": {"method":"GET","path":"/auth/sessions","contract":"identity","summary":"List active sessions","permission":"SESSION_FORCE_LOGOUT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"X-Supervisor-Principal-Id","in":"header","required":false},{"name":"X-Supervisor-Pin","in":"header","required":false},{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAnnouncements": {"method":"GET","path":"/announcements","contract":"workforce","summary":"What staff have been told","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"unacknowledgedOnly","in":"query","required":null}],"requestBody":null,"responds":"Announcement"},
"listApprovalDelegations": {"method":"GET","path":"/delegations","contract":"approvals","summary":"Who is standing in for whom","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ApprovalDelegation"},
"listApprovalMatrices": {"method":"GET","path":"/approval-matrices","contract":"approvals","summary":"What requires approval here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"ApprovalMatrix"},
"listApprovalRequests": {"method":"GET","path":"/approval-requests","contract":"approvals","summary":"Requests awaiting a decision, or already decided","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToMe","in":"query","required":null},{"name":"raisedByMe","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"breachingWithinMinutes","in":"query","required":null},{"name":"sort","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAttendance": {"method":"GET","path":"/attendance","contract":"workforce","summary":"Who was here","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"date","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"exceptionsOnly","in":"query","required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"listCapabilityTemplates": {"method":"GET","path":"/capability-templates","contract":"identity","summary":"Saved tick-sets","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"CapabilityTemplate"},
"listJobTitles": {"method":"GET","path":"/job-titles","contract":"workforce","summary":"The job titles a posting can name","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkforceJobTitle"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPermissionFindings": {"method":"GET","path":"/permission-findings","contract":"identity","summary":"Excessive, missing and conflicting permissions, per principal or role","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"principalId","in":"query","required":null},{"name":"roleId","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"lookbackDays","in":"query","required":null},{"name":"deniedThreshold","in":"query","required":null},{"name":"draftPolicyId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRoles": {"method":"GET","path":"/roles","contract":"identity","summary":"List roles","permission":"ROLE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRotaAssignments": {"method":"GET","path":"/rota-assignments","contract":"workforce","summary":"The rota","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTrainingRecords": {"method":"GET","path":"/training-records","contract":"workforce","summary":"Training completed and what is expiring","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TrainingRecord"},
"listWorkAssignments": {"method":"GET","path":"/work-assignments","contract":"workforce","summary":"Where each person is posted, and from when","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"employeeId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"activeOn","in":"query","required":null}],"requestBody":null,"responds":"WorkforceWorkAssignment"},
"publishAnnouncement": {"method":"POST","path":"/announcements","contract":"workforce","summary":"Tell staff something","permission":"ANNOUNCEMENT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Announcement","responds":"Announcement"},
"requestShiftSwap": {"method":"POST","path":"/rota-assignments/{assignmentId}/swap","contract":"workforce","summary":"Ask someone to take your shift","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"resetPrincipalCredential": {"method":"POST","path":"/principals/{principalId}/credential-reset","contract":"identity","summary":"Reset a member of staff's password or PIN","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResetCredentialRequest","responds":null},
"resolvePermissions": {"method":"POST","path":"/permissions/resolve","contract":"identity","summary":"Simulate a principal's effective permissions","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"resubmitApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/resubmit","contract":"approvals","summary":"Amend a rejected request and try again","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"revokeAllSessions": {"method":"POST","path":"/auth/sessions/revoke-all","contract":"identity","summary":"Revoke every session in scope","permission":"SESSION_FORCE_LOGOUT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"revokeApprovalDelegation": {"method":"DELETE","path":"/delegations/{delegationId}","contract":"approvals","summary":"End a delegation early","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setCapabilityTemplate": {"method":"PUT","path":"/capability-templates","contract":"identity","summary":"Save a tick-set under a name","permission":"ROLE_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CapabilityTemplate","responds":"CapabilityTemplate"},
"setJobTitle": {"method":"PUT","path":"/job-titles","contract":"workforce","summary":"Define a job title","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkforceJobTitle","responds":"WorkforceJobTitle"},
"setRolePermissions": {"method":"PUT","path":"/roles/{roleId}/permissions","contract":"tenancy","summary":"What this role may do","permission":"ROLE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setWorkAssignment": {"method":"PUT","path":"/work-assignments","contract":"workforce","summary":"Post a person to a job title at a venue","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkforceWorkAssignment","responds":"WorkforceWorkAssignment"},
"suggestRoleAssignment": {"method":"GET","path":"/role-suggestions","contract":"identity","summary":"Which roles a person should probably hold, from peers with the same job and posting","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"principalId","in":"query","required":null},{"name":"jobTitleId","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"minPeerShare","in":"query","required":null},{"name":"minPeers","in":"query","required":null},{"name":"lookbackDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"updatePrincipal": {"method":"PATCH","path":"/principals/{principalId}","contract":"identity","summary":"Update or deactivate a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Principal"},
"updateRotaAssignment": {"method":"PATCH","path":"/rota-assignments/{assignmentId}","contract":"workforce","summary":"Move or cancel an assignment","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RotaAssignment","responds":"RotaAssignment"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"withdrawApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/withdraw","contract":"approvals","summary":"The requester takes it back","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ActiveSession": {"x-ticvai-persistence":"identity.session","description":"**The session record, in `identity.session`** (3 October 2026, CHG-R1S-008; the HLD/LLD cross-check and the r1 gate). Until then it was \"none — Redis session registry\", and 11 operations wrote a session no SQL created: nothing defined its columns, so `listActiveSessions` could not page, filter by workstation or venue, or run under row-level security. The row is the record of record, tenant-scoped and under RLS like every identity table; Redis stays the token cache in front of it (ADR-0004: a session is a token with a validity window, and the cache answers that check). The names and `hasOpenShift` are read with it, not stored.","type":"object","required":["sessionId","principalId","status","startedAt","lastSeenAt"],"properties":{"status":{"allOf":[{"$ref":"#/components/schemas/SessionStatus"}],"description":"**A registry that only holds live sessions cannot answer why one ended.** Kept on the record so a supervisor asking *what happened to till 4* gets `terminated` or `expired` rather than an absence.\n"},"sessionId":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"principalName":{"type":"string","x-ticvai-persisted":false,"description":"Read from `identity.principal` with the row."},"roleId":{"type":"string","format":"uuid","nullable":true},"roleName":{"type":"string","nullable":true,"x-ticvai-persisted":false,"description":"Read from `identity.role` with the row."},"workstationId":{"type":"string","format":"uuid","nullable":true},"workstationName":{"type":"string","nullable":true,"x-ticvai-persisted":false,"description":"Read from the workstation with the row."},"venueId":{"type":"string","format":"uuid","nullable":true},"ipAddress":{"type":"string","nullable":true},"deviceInfo":{"type":"string","nullable":true},"hasOpenShift":{"type":"boolean","x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"Revoking this session leaves cash unreconciled. **Computed on read** from the shift the principal holds open at the workstation (`orders.pos_shift`), never stored here."},"mfaSatisfied":{"type":"boolean"},"startedAt":{"type":"string","format":"date-time"},"lastSeenAt":{"type":"string","format":"date-time"}}},
"AiApprovalRequestScore": {"type":"object","x-ticvai-persistence":"ai.approval_request_score","description":"**Context for an approval reviewer** (11.1.73..75): risk, priority and a suggested escalation for one pending request, the latest per request. **There is no approve or reject field, by design** (minutes of 8 September: AI in approvals never recommends or influences approve or reject).","required":["approvalRequestId","riskScore","riskBand","priorityScore","escalationSuggestion"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"approvalRequestId":{"type":"string","format":"uuid","x-ticvai-references":"approvals.request"},"trigger":{"type":"string","enum":["submitted","resubmitted","slaTick","escalated"]},"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"],"description":"Design 5.6: a risk score and band, never a probability."},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"description":"For ordering work in an inbox; higher first."},"escalationSuggestion":{"type":"object","required":["action"],"properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}},"description":"A suggestion for an SLA problem, carried out if at all by a person or the tenant's SLA policy."},"signals":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","description":"e.g. `amountAboveRequesterNorm`, `requesterEntityRisk`, `outOfHours`, `irreversibleAction`, `slaDueSoon`, `stepBreachRate`, `approverUnavailable`."},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"scoredAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"Announcement": {"type":"object","x-ticvai-persistence":"workforce.announcement","required":["title","body","kind","publishedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"type":"string","maxLength":140},"body":{"type":"string","maxLength":4000},"kind":{"$ref":"#/components/schemas/AnnouncementKind"},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresAcknowledgement":{"type":"boolean"},"deliveryChannels":{"type":"array","description":"How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n","items":{"type":"string","enum":["inApp","push"]},"default":["inApp","push"]},"expiresAt":{"type":"string","format":"date-time","nullable":true},"publishedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"publishedAt":{"type":"string","format":"date-time"},"locale":{"type":"string","nullable":true}}},
"AnnouncementKind": {"type":"string","description":"`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n","enum":["operational","safety","emergency","hr","celebration"]},
"AnnouncementReach": {"type":"object","x-ticvai-persistence":"none — computed from workforce.announcement_receipt","properties":{"announcementId":{"type":"string","format":"uuid"},"targeted":{"type":"integer"},"delivered":{"type":"integer"},"acknowledged":{"type":"integer"},"outstanding":{"type":"array","description":"**The list that matters.** For an operational notice it measures whether anyone read it; during an emergency it is the roll call.\n","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"onShift":{"type":"boolean"}}}}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalDelegation": {"type":"object","x-ticvai-persistence":"approvals.delegation","required":["delegatorPrincipalId","delegatePrincipalId","from","to"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"delegatorPrincipalId":{"type":"string","format":"uuid","description":"A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and `identity.getPrincipal`.\n"},"delegatePrincipalId":{"type":"string","format":"uuid","description":"A principal id, resolved to a name the same way as `delegatorPrincipalId`."},"kinds":{"type":"array","description":"Absent means everything the delegator may approve.","items":{"$ref":"#/components/schemas/ApprovalKind"}},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"A delegate may be given less authority than the delegator, never more."},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time","description":"**Required.** An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it.\n"},"reason":{"type":"string"},"isActive":{"type":"boolean","readOnly":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"},"delegationType":{"type":"string","nullable":true,"description":"The composite screen's `delegationType` (planned absence, temporary cover ...), for display and reporting; the engine treats every delegation alike (4 October 2026, CHG-FXC-005)."},"maxPercentage":{"type":"number","nullable":true,"description":"A percentage cap beside `maxAmount` (the composite's `authorityPercentage`, CHG-FXC-005)."},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"A role the delegate must hold for the delegation to act (the composite's `requiredRole`); checked when the delegate decides, refused with 409 at creation where the delegate does not hold it (CHG-FXC-005)."}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n\n**A rota shift swap** (4 October 2026, CHG-FXC-008; Sprint 1-2 judging: `workforce.requestShiftSwap` raised a request\nwith no kind that fits). `configurationChange`, subject `shiftSwap`, `subjectContract` `workforce`, `subjectId` the\nShiftSwap id: an existing kind narrowed by `subjectTypes`, as the optional review steps above, so no kind is added.","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"},"code":{"type":"string","maxLength":64,"nullable":true,"description":"**A stable code for the rule, unique within its matrix** (4 October 2026, CHG-FXC-005). The composite `approveMatrixMultiLevel` upserts a rule by it; `setApprovalMatrix` may leave it null."},"minimumApprovals":{"type":"integer","minimum":1,"nullable":true,"description":"N in N-of-M (CHG-FXC-005). Null means every approver the mode asks."},"requiredApproverRoleId":{"type":"string","format":"uuid","nullable":true,"description":"A role that must be among the approvals whatever N is (the CFO in an N-of-M group); it is also one of `approverRoleIds` (CHG-FXC-005)."},"rejectionBehavior":{"type":"string","nullable":true,"enum":["rejectRequest","returnToPreviousLevel","returnToRequester"],"description":"What a rejection at this rule does; null is `rejectRequest` (CHG-FXC-005)."},"allowRequestChanges":{"type":"boolean","default":false},"allowDelegate":{"type":"boolean","default":true},"allowReassign":{"type":"boolean","default":false},"minPercentage":{"type":"number","nullable":true,"description":"A percentage threshold (a discount or a margin impact) at or above which the rule applies, beside `minAmount` (CHG-FXC-005)."},"matchAttributes":{"type":"object","x-ticvai-persistence-column":"jsonb","nullable":true,"additionalProperties":{"type":"string"},"description":"**The request attributes a rule matches on** (CHG-FXC-005): keys `module`, `product`, `department`, `customerType`, `risk`, `exceptionType`, `legalEntity`, each an exact value the request's attributes must carry. Every key given must match; an absent key matches anything. Evaluated before `condition`."},"compositeMode":{"type":"string","nullable":true,"enum":["single","sequential","parallel","anyOne","allMustApprove","conditional","multiLevel"],"description":"The `approvalMode` the composite screen sent, kept so it reads back what it saved; `mode`, `levels` and `minimumApprovals` are what the engine runs (CHG-FXC-005)."}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"AttendanceAmendment": {"type":"object","x-ticvai-persistence":"workforce.attendance_amendment","description":"One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n","required":["id","attendanceRecordId","amendedByPrincipalId","amendedAt","occurredAtBefore","occurredAtAfter","reason"],"properties":{"id":{"type":"string","format":"uuid"},"attendanceRecordId":{"type":"string","format":"uuid"},"amendedByPrincipalId":{"type":"string","format":"uuid"},"amendedAt":{"type":"string","format":"date-time"},"occurredAtBefore":{"type":"string","format":"date-time","description":"The record's time before this correction."},"occurredAtAfter":{"type":"string","format":"date-time","description":"The time this correction set (`correctedAt` on the request)."},"reason":{"type":"string","maxLength":300}}},
"AttendanceRecord": {"type":"object","x-ticvai-persistence":"workforce.attendance","required":["id","principalId","kind","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clockIn","clockOut","breakStart","breakEnd"]},"occurredAt":{"type":"string","format":"date-time","description":"Device time — when it happened."},"recordedAt":{"type":"string","format":"date-time","description":"When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"isAmended":{"type":"boolean","readOnly":true},"amendedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who made the latest amendment. The full history is `amendments` (audit R129 (7))."},"amendmentReason":{"type":"string","nullable":true,"readOnly":true,"description":"The latest amendment's reason. The full history is `amendments` (audit R129 (7))."},"originalOccurredAt":{"type":"string","format":"date-time","nullable":true,"description":"**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"},"amendments":{"type":"array","readOnly":true,"description":"**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n","items":{"$ref":"#/components/schemas/AttendanceAmendment"}},"exception":{"type":"string","nullable":true,"enum":["late","earlyLeave","missingClockOut","noShow","outOfGeofence","unscheduled"],"description":"Computed against the rota. Null where the record matches what was expected."}}},
"CapabilityTemplate": {"x-ticvai-persistence":"identity.capability_template","type":"object","description":"3.3.23, BL-110. **A named tick-set — a role, with nothing depending on the name.**\n","required":["code","name","capabilities"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"capabilities":{"type":"array","items":{"type":"string"}},"module":{"type":"string","nullable":true,"description":"**The module a per-module preset belongs to** (a contract name, as `listModuleCapabilities`; CHG-CSP-003). Null for a template that spans modules, such as the Cashier starting configuration.\n"},"presetLevel":{"type":"string","nullable":true,"enum":["all","viewer","midLevel"],"description":"**Which of the three per-module presets this is** (decided 2 October 2026, Chinmay; DEC-007; CHG-CSP-003): All, Viewer or Mid-level. Null on a template a tenant saved itself and on a cross-module starting configuration.\n"},"isPreset":{"type":"boolean","default":false,"readOnly":true,"description":"**Seeded by the platform, not saved by the tenant** (CHG-CSP-003). A preset is offered when a role is created and cannot be deleted; a tenant saves its own tick-sets beside them with `setCapabilityTemplate`.\n"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written by the server at `tenant` scope; ignored if a request sends it."}}},
"CreatePrincipalRequest": {"type":"object","required":["username","displayName"],"properties":{"username":{"type":"string","maxLength":256},"displayName":{"type":"string","maxLength":200},"initialCredential":{"type":"string","maxLength":512,"writeOnly":true},"mustChangeCredential":{"type":"boolean","default":true},"validTo":{"type":"string","format":"date-time"},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"IdentityAccessReviewCampaign": {"type":"object","x-ticvai-persistence":"identity.access_review_campaign","description":"**A periodic access review** (7.1.35, 7.1.56; decided 29 September, build pass, group G2): which grants, reviewed by whom, by when. Its items are `identity.access_review_item`. Lifecycle in `states/access-review-campaign.yaml`.","required":["name","scopePath","reviewerMode","dueAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string","maxLength":200},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), and what is reviewed: every grant at or below it. Inside the caller's own scope. Operations write it at `venue` scope."},"roleIds":{"type":"array","nullable":true,"description":"Only grants of these roles; null reviews every grant in scope.","items":{"type":"string","format":"uuid"}},"reviewerMode":{"type":"string","enum":["lineManager","named"],"description":"`lineManager`: each item goes to the holder's manager from their primary work assignment, falling back to the named reviewers where none is found. `named`: the named reviewers share the items."},"reviewerPrincipalIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"}},"dueAt":{"type":"string","format":"date-time"},"recurrence":{"type":"string","enum":["none","quarterly","semiAnnual","annual"],"default":"none"},"prefillFromFindings":{"type":"boolean","default":true},"lookbackDays":{"type":"integer","minimum":7,"maximum":365,"default":90},"status":{"type":"string","enum":["open","completed","expired"],"readOnly":true},"itemCount":{"type":"integer","readOnly":true},"decidedCount":{"type":"integer","readOnly":true,"description":"Kept by `decideAccessReviewItem` in the same write, so the campaign list needs no count query."},"revokedCount":{"type":"integer","readOnly":true},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"closedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"IdentityAccessReviewItem": {"type":"object","x-ticvai-persistence":"identity.access_review_item","description":"One grant under review in a campaign, with the finding that pre-filled it and the reviewer's decision (decided 29 September, build pass, group G2). Lifecycle in `states/access-review-item.yaml`.","required":["campaignId","delegatedAccessId","principalId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"campaignId":{"type":"string","format":"uuid","x-ticvai-references":"identity.access_review_campaign"},"delegatedAccessId":{"type":"string","format":"uuid","x-ticvai-references":"identity.delegated_access","description":"The grant under review."},"principalId":{"type":"string","format":"uuid","x-ticvai-references":"identity.principal"},"roleId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.role"},"scopePath":{"type":"string","description":"The grant's scope. **The partition key** (ADR-0005)."},"reviewerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"findingKind":{"type":"string","enum":["none","excessive","conflicting"],"default":"none"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true},"recommendation":{"type":"string","enum":["certify","revoke","review"]},"status":{"type":"string","enum":["pending","certified","revoked","notReviewed"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"reason":{"type":"string","maxLength":1000,"nullable":true}}},
"IdentityPermissionFinding": {"type":"object","x-ticvai-persistence":"none — computed from grants (roles, delegations, policies) against identity.access_decision and identity.segregation_rule","description":"One excessive, missing or conflicting permission (7.1.47; decided 29 September, build pass).","required":["kind","principalId","permission"],"properties":{"kind":{"type":"string","enum":["excessive","missing","conflicting"]},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid","nullable":true,"description":"The role that grants it, for excessive and conflicting; the role whose peers hold it, for missing."},"permission":{"type":"string"},"conflictingPermission":{"type":"string","nullable":true,"description":"The other half of the pair, for conflicting."},"segregationRuleId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"grantedBy":{"type":"string","enum":["role","delegation","policy"],"nullable":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"description":"The last permit that used it; null when never used in the window."},"deniedCount":{"type":"integer","nullable":true,"description":"For missing, the denials in the window."},"peersHoldingPercent":{"type":"number","minimum":0,"maximum":100,"nullable":true,"description":"For missing, the share of the role's holders at the same scope who hold the permission."},"recommendation":{"type":"string","enum":["revoke","grant","review"]},"asDraft":{"type":"boolean","default":false,"description":"True when the finding exists only because of the `draftPolicyId` evaluated."}}},
"IdentityRoleSuggestion": {"type":"object","x-ticvai-persistence":"none — computed from workforce.work_assignment peers, identity.delegated_access and identity.access_decision","description":"One role suggested for a person because peers with the same job title and posting hold it (7.1.35, 7.1.56; decided 29 September, build pass, group G2).","required":["roleId","scopePath","peersHoldingPercent","recommendation"],"properties":{"roleId":{"type":"string","format":"uuid"},"roleCode":{"type":"string"},"roleName":{"type":"string"},"scopePath":{"type":"string","description":"Where the peers hold it, and so where it would be granted."},"peerCount":{"type":"integer","description":"Principals with the same job title at the same posting."},"peersHolding":{"type":"integer"},"peersHoldingPercent":{"type":"number","minimum":0,"maximum":100},"peersUsingPercent":{"type":"number","minimum":0,"maximum":100,"nullable":true,"description":"Of the peers holding it, the share with a permit using one of its permissions in `lookbackDays`."},"alreadyHeld":{"type":"boolean"},"recommendation":{"type":"string","enum":["grant","review","held"],"description":"`grant` where most peers hold and use it; `review` where they hold it and do not use it; `held` where the person has it already."},"evidence":{"type":"object","description":"What the suggestion rests on, so the person granting can check it.","properties":{"jobTitleId":{"type":"string","format":"uuid"},"postingScopePath":{"type":"string"},"samplePeerPrincipalIds":{"type":"array","maxItems":5,"items":{"type":"string","format":"uuid"}},"requiresApproval":{"type":"boolean","description":"Whether granting this role raises an approval (a role carrying permission or price authority, ApprovalKind level 2)."}}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/tenancy::ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PermissionSet": {"type":"array","items":{"$ref":"#/components/schemas/Permission"},"uniqueItems":true},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"ResetCredentialRequest": {"type":"object","description":"Request only; see `ChangeCredentialRequest`.","required":["method","temporaryCredential","reason"],"properties":{"method":{"type":"string","enum":["password","pin"]},"temporaryCredential":{"type":"string","maxLength":512,"writeOnly":true,"description":"Issued to the principal out of band. Must be changed at next sign-in."},"reason":{"type":"string","minLength":3,"maxLength":500}}},
"Role": {"x-ticvai-persistence":"identity.role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. Unique per tenant, not per venue, because a grant names a role anywhere in the tree; `createRole` refuses a duplicate with `409 duplicate-code`.\n"},"name":{"type":"string"},"description":{"type":"string"},"permissions":{"type":"array","description":"**A role that grants no permissions is not a role.** `Role` carried a code, a name and two counts until 18 August, and `identity.role_permission` derived from it with exactly one column — `role_id`. **A join table that joins to nothing**, found by Hrushikant in review and missed by the schema audit that ran the same day.\n**The audit asked whether every table had columns, a relationship and an owner, and this table had all three.** What it did not ask is whether a table with one column can do the job its name claims.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"inheritsFromRoleId":{"type":"string","format":"uuid","nullable":true,"description":"**Role composition, one level deep and no deeper.** A supervisor role that is a cashier plus three permissions is how venues actually describe them.\n**Cycles are refused and depth is capped at one**, because a permission set nobody can read off the screen is a permission set nobody audits.\n"},"isSystem":{"type":"boolean","default":false,"description":"**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n**The seeded system roles are Cashier, Supervisor, Venue Manager, Finance and Tenant Admin** (proposed in `docs/active/seed-data-proposal.md` section 2, client to correct; audit R229).\n\n**Superseded 2 October 2026: no fixed default roles** (Chinmay; DEC-007; CHG-CSP-003). The five are presets (`CapabilityTemplate`, `isPreset`) a role starts from, not roles a tenant is given. The field stays for clients built at r1 and is false on every role created from 2 October.\n"},"presetCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":64,"description":"**The preset this role was started from, for the record only** (decided 2 October 2026, Chinmay; DEC-007; CHG-CSP-003): the first of `createRole.presetCodes`, or null for a role ticked by hand. It binds nothing; a later edit of the preset never changes this role.\n"},"principalCount":{"type":"integer"},"grantCount":{"type":"integer"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"ScopedPermissions": {"type":"object","description":"Permissions effective at a given scope path, after deny resolution. Clients filter navigation on this and never compute permissions themselves.\n","required":["scopePath","permissions"],"properties":{"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"permissions":{"$ref":"#/components/schemas/PermissionSet"}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SessionStatus": {"type":"string","description":"**The life of one signed-in session, which is not the life of a shift.** A shift holds the float and survives a break; a session holds the person and does not. `ShiftStatus.suspended` is where a break lives — *break cover; float intact, workstation released* — and the release of the workstation is exactly why the session ends rather than pausing: the next person opens their own.\n**One principal, one active session per workstation.** Enforced by the `ActiveSession` registry rather than by a state, because it is a fact about the set of sessions and not about any one of them.\n","enum":["active","signedOut","terminated","expired"]},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"TrainingRecord": {"type":"object","x-ticvai-persistence":"workforce.training_record","description":"**Drafted 4 September.** One person, one course, one outcome. **The field that matters is the expiry** - a lapsed food-safety or first-aid certificate is a person who may not work a station, and a list without it is a list nobody can roster from.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"courseName":{"type":"string"},"required":{"type":"boolean"},"completedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"},"state":{"type":"string","enum":["notStarted","inProgress","passed","failed","expired"]},"evidenceRef":{"type":"string"}}},
"WorkforceJobTitle": {"type":"object","x-ticvai-persistence":"workforce.job_title","description":"**Taken from the backend workbook, 20 September.** Stores job/designation definitions such as Cashier, Manager, Chef or Technician.","required":["tenantId","code","name","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":50},"name":{"type":"string","maxLength":150},"description":{"type":"string","maxLength":500,"nullable":true},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkforceWorkAssignment": {"type":"object","x-ticvai-persistence":"workforce.work_assignment","description":"**Taken from the backend workbook, 20 September.** Assigns an employee to a job and operational location/scope for an effective period.","required":["employeeId","jobTitleId","effectiveFrom","isPrimary","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"employeeId":{"type":"string","format":"uuid"},"jobTitleId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true},"effectiveFrom":{"type":"string","format":"date"},"effectiveTo":{"type":"string","format":"date","nullable":true},"isPrimary":{"type":"boolean"},"status":{"type":"string","maxLength":30},"createdAt":{"type":"string","format":"date-time"}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
