# P07-access-01 — P07 · Access (1 of 2)

**10 screens · 21 operations · 32 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, ORDER_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW, TICKET_LOOKUP, TURNSTILE_MODE_SET`. A control nobody can use must say so,
  not sit enabled and fail.
- **11 of these operations work offline**: consumeCrossRegionEntitlement, endPodiumShift, getAccessPoint, getCrossRegionEntitlement, getCurrentSession, listAccessPoints, lookupTicket, overrideAccess
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `SCN-001` | Sign in | A | 14 | 20 | 8 | 5 | 0 | 0 | — | notStarted (generated) |
| `SCN-002` | Access point & direction | C | 4 | 9 | 6 | 6 | 0 | 0 | — | notStarted (generated) |
| `SCN-003` | Ready to scan | A | 21 | 0 | 10 | 46 | 8 | 0 | — | notStarted (generated) |
| `SCN-007` | Group admission | C | 6 | 5 | 6 | 13 | 2 | 0 | — | notStarted (generated) |
| `SCN-008` | Manual entry | C | 8 | 5 | 6 | 47 | 1 | 0 | — | notStarted (generated) |
| `SCN-009` | Ticket lookup | C | 7 | 12 | 6 | 15 | 4 | 0 | — | notStarted (generated) |
| `SCN-011` | Delegated right | B | 4 | 5 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `SCN-013` | Offline journal | C | 31 | 5 | 6 | 53 | 2 | 0 | — | notStarted (generated) |
| `SCN-014` | Sync & reconciliation | A | 35 | 16 | 6 | 60 | 3 | 0 | — | notStarted (generated) |
| `SCN-015` | Offline package | C | 1 | 5 | 6 | 8 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**SCN-011, SCN-015 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SCN-001` Sign in

**PIN or badge, so every scan is attributable to a person at this gate. The scanner sends its workstation.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `core` module |
| Block | Block A · task APP-SCANNER-SCN-001 |
| Who uses it | venue; in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | form (comfortable density): PIN or badge on a gate scanner, then the role - a form, not a list. |
| Offline | **Signs in against the cached principal list from the last bundle.** A steward locked out at 08:00 because the venue wifi is down is a gate that does not open. |
| Opens with | `challengeId` (navigation) · cold entry: **The only screen of the scanner that needs nothing.** The scanner's `workstationId` travels in the sign-in request from the device itself (CHG-DOOR-001). |
| Route | `/access/sign-in` |

**What the spec says about it.** **Rebuilt as a sign-in form on 2 October 2026 (CHG-DOOR-002/003; Chinmay, 2 October 2026: fix the Block A blockers now).** It was generated as a list over active sessions, MFA methods and SSO providers with Force logout and Revoke all sessions on the door, which a person who is not yet signed in can never use (platform-foundation process notes). The sequence is the same on every staff and partner door: credentials (or the organisation's SSO) -> the authentication code only when a permission demands it (R135) -> the role prompt when several roles are held (ADR-0003) -> the landing. Managing sessions moved to the staff directory (BO-053); managing MFA methods stays on each app's own security or profile screen. **resolvePermissions and getCurrentShift left the door**: simulating a principal's permissions is an administration tool (BO-068), and a scanner runs no cash shift, so a steward was shown a SHIFT_OPEN no-access state at sign-in.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): resolvePermissions (an administration simulator, PERMISSION_VIEW) and getCurrentShift (SHIFT_OPEN, a cash shift) were on the scanner sign-in; a steward never … Removed 2 October 2026 (CHG-WIR-021): resolvePermissions (an administration simulator, PERMISSION_VIEW) and getCurrentShift (SHIFT_OPEN, a cash shift) were on the scanner sign-in; a steward never …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The scanner's door: PIN or badge, so every scan is attributable to a person at this gate. Offline sign-in against the last bundle's staff list, because a steward locked out at opening is a gate that does not open.

**Fixed on main** (the package already carries these; draw what it says): resolvePermissions (simulate a principal's permissions, PERMISSION_VIEW) is on the scanner's sign-in. (CHG-WIR-021); getCurrentShift with emptyNoAccess naming SHIFT_OPEN. (CHG-WIR-021); listDetail with MFA-method and SSO-provider tables. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every MFA method' drop id; 'Every SSO provider' drop id, scopePath. (CHG-WIR-021).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Employee number | text field | — | — | — | — | Goes into `LoginRequest.username`; a badge tap fills it. | — |
| PIN | text field | — | — | — | — | Goes into `LoginRequest.credential` with `method: pin`, or the badge with `method: card` or `rfid`. The scanner sends its own `workstationId` (CHG-DOOR-001), so every scan is attributable to a person … | — |
| Authentication code | text field | — | — | — | — | Shown only when the sign-in comes back `requiresMfa`: the person holds a permission in `PasswordPolicy.mfaRequiredForPermissions` (ROLE_MANAGE, LEDGER_APPROVE, every PLATFORM_* permission, or one the … | — |
| New PIN | text field | — | — | — | — | Only when the PIN was reset and is temporary (audit R132). | — |

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

**Sent by *Choose role*** (`selectRole`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `selectRole` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **PIN or badge**: Badge tap fills username and credential (method card or rfid); otherwise employee number and PIN on the keypad. *(source: contracts/spine/identity.yaml#/components/schemas/LoginRequest; F06 step 1)*

#### Outputs: what the screen shows and produces

**Shown**

**Signed in as** (banner, from `getCurrentSession`): Read once the sign-in is complete (after the code and the role, where asked): the person's name and role, then straight on. Then the access point is confirmed (SCN-002).

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
| Verify (primary button) | `verifyMfaChallenge` POST `/auth/mfa/challenge/{challengeId}/verify` | inline | inline | — | — |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |
| Choose role (secondary button) | `selectRole` POST `/auth/select-role` | inline | Session | 403 Authenticated but not permitted at the requested scope | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (liftsTotal, refundsTotal, salesTotal)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Where the user goes next**

- → `SCN-002` Access point & direction: *Confirms access point and direction*
- → `SCN-003` Ready to scan: *Ready to scan*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Checking the credential. The form stays visible and disabled. |
| Empty, first run (`?state=emptyFirstRun`) | **Nobody signed in** - the normal state of a door. A scanner between shifts shows the keypad and a badge prompt. |
| Error (`?state=error`) | Identity could not be reached. **Says so rather than saying the password is wrong**, and keeps what was typed. |
| Denied (`?state=denied`) | The credential does not match, or the account is locked. One message for both, with the attempts left before the lock; a locked account says when to try again. |
| Permission denied (`?state=emptyNoAccess`) | Signed in, and the person holds no role in this app. Says who at the tenant grants access; distinct from a wrong password. A door has no permission of its own to name, because the person is not signed in until it succeeds. |
| Session held (`?state=sessionHeld`) | `login` answered 409: this person already holds a session elsewhere (audit R184, ADR-0004). Says where and since when; only a holder of SESSION_FORCE_LOGOUT ends it, on the staff directory (BO-053), and signing in never ends it by itself. |
| MFA required (`?state=mfaRequired`) | **Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any PLATFORM_* permission, or one the tenant added), so the screen calls `createMfaChallenge` (`action: signIn`) and asks for the authentication code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says until when (audit R135, R126). A person without such a … |
| Offline (`?state=offline`) | **Signs in against the cached principal list from the last bundle.** A steward locked out at 08:00 because the venue wifi is down is a gate that does not open. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused.; 422 The new credential fails the password policy, or matches the current one or any of the previous `PasswordPolicy.reusePreventionCount` credentials (5 unless the … |

#### Consistency with other screens

- Match `EMP-001`: Same door.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
steward:
  name: Yusuf Rahman
  badge: RFID 04:A2:19:7C
  gate: Main Gate Lane 2 (AUH-SCN-02)
```

#### Permissions

- `login` → no permission · anonymous, partner
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest
- `selectRole` → no permission · staff, partner
- `changeOwnCredential` → no permission · staff, partner
- `getCurrentSession` → no permission · staff, partner

**A refused user sees:** Signed in, and the person holds no role in this app. Says who at the tenant grants access; distinct from a wrong password. A door has no permission of its own to name, because the person is not signed in until it succeeds.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.5 | The system should have the option to be used by several waiters at the same time. | F&B & Guest Management | CONTRACTED | `login` |
| 5.8.2 | The system should only allow one session per user. | F&B & Guest Management | CONTRACTED | `login` |
| 7.1.4 | The system should be able to have a login override option for the supervisor level in order to login to the POS if the need arises and the previous user has not logged out. | F&B POS | CONTRACTED | `selectRole` |
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |

#### Client meeting inputs

None names this screen.

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-001` · status **notStarted** · provenance generated
- Flow F06 *Guest enters the venue*, step 1: Steward signs in with PIN or badge → Session carries the workstation, so every scan is attributable. A scanner runs no cash shift, so the door reads none (CHG-DOOR-003)
- Flow F61 *A gate opens, a steward signs in, and a group is admitted*, step 1: The steward signs in and takes a role for the session. → **The person carries the authority, not the device** (ADR-0002). A handheld passed to a colleague at a break carries nothing with it, which is the property that makes a shared device safe.
- Flow F61 branch at step 1 (medium): when The steward has no role at this venue., Refused at sign-in rather than at first scan. **A person who reaches the lane and then cannot scan has already formed a queue behind them.**
- ADR-0003 *Conditional role selection at login* (`docs/adr/0003-conditional-role-selection-at-login.md`)
- ADR-0004 *Single session per user* (`docs/adr/0004-single-session-per-user.md`)
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-001?state=<state>`: loading, emptyFirstRun, error, denied, emptyNoAccess, sessionHeld, mfaRequired, offline.
- [ ] Every action is wired with its success and its failure: Sign in, Verify, Email me a code instead, Choose role.
- [ ] Every transition is wired: `SCN-002`, `SCN-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-002` Access point & direction

**Confirm what this device is doing before it does it.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | Block C · task APP-SCANNER-SCN-002 |
| Who uses it | venue staff holding `SCOPE_VIEW`, `TURNSTILE_MODE_SET` (1 read, 1 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAccessPoints` reads the population and `getAccessPoint` reads one of them — list, select, act |
| Offline | Fully offline. The access point list is in the bundle |
| Opens with | `accessPointId` (deepLink), `podiumId` (session), `shiftId` (session) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/access/access-point-direction` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Authoring operations removed 24 August**: createAccessPoint, setAccessPointGeofence, updateAccessPoint. **A scanner reads the gate configuration; it does not write it.** An access point is created in the back office and a geofence is a venue decision — a handheld at a lane that can redefine the lane is a handheld that can admit anywhere. **`setTurnstileMode` belongs here and flow F06 is why.** It was taken off on 4 September on the reasoning that this screen only reads — but F06 *guest enters the venue* step 2 is 'confirms access point and direction'. **Since 28 September (audit R221) confirming the direction is not setting the mode**: the direction is fixed per access point and shown here read-only; what the operator sets is the operating mode (required), with the turnstile mode (freeRotation or closed) as an optional narrowing under normal or podium only.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Setting the gate's operating mode is the live podium act on SCN-016 Gate mode (R221); on SCN-002 the primary act is confirming the access point and starting the …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Start of a scanner session: the steward confirms which access point the handheld is at and starts their podium shift, so every scan is attributable to a person, a device and a gate. The direction (entry, exit, re-entry, crossover) is shown as the access point's fixed property. The one thing to get right: the device states what it is about to do in large type before the first scan.

**Known correction pending (do not draw the wrong version)**

- **F61 step 2 says the steward picks the direction ("the same lane runs entry in the morning and exit at close") but R221 fixes direction per access point in the back office** Why: Contradiction between the flow and the decided model; a lane that changes direction needs two access points or the flow must change. *(source: F61 step 2 / R221 / DI-648; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Save gate mode as the primary action and a "Venue id" text field** Why: The primary act here is confirming the point and starting the shift; venue comes from the session. *(source: screens/P07-staff-scanner.yaml#SCN-002; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listAccessPoints`. | `listAccessPoints` ?venueId |

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

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Access point**: Pick from the venue's access points grouped by park and zone (from the offline bundle); large touch rows with name and a direction badge; the last one used is preselected. *(source: contracts/spine/access.yaml#listAccessPoints / F06 step 2)*
- **Podium shift**: Starting a shift closes any open shift of the same operator; no fields beyond the role already chosen at sign-in. *(source: contracts/spine/access.yaml#startPodiumShift)*

#### Outputs: what the screen shows and produces

**Shown**

**Every access point** (data table, from `listAccessPoints`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |
| Direction | chip: Entry, Exit, Reentry, Crossover | Fixed per access point (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium. |

**The selected access point** (detail panel, from `getAccessPoint`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Operating mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Set by the podium with `setTurnstileMode`, and it wins (audit R221). BL-107 and BL-109. |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |
| Direction | chip: Entry, Exit, Reentry, Crossover | Fixed per access point (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Start podium shift (secondary button) | `startPodiumShift` POST `/podiums/{podiumId}/shifts` | inline | AccessPodiumShift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; gated `TURNSTILE_MODE_SET`; opens modal first |
| End podium shift (secondary button) | `endPodiumShift` POST `/podium-shifts/{shiftId}/end` | inline | AccessPodiumShift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; gated `TURNSTILE_MODE_SET`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Confirmation banner**: "Main Plaza Gate 2 - ENTRY - Rahul Menon - offline package from 06:40" and the gate's current mode (Normal, Free flow, Closed...). *(source: F06 step 2 / contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start scanning**: Loads or refreshes the offline package (SCN-015) and opens the ready screen (SCN-003). *(source: F06 step 3 / F61 step 3)*
- **Gate mode**: Opens SCN-016 for supervisors holding the permission; hidden-with-reason for stewards. *(source: contracts/spine/access.yaml#setTurnstileMode)*

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listAccessPoints` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TURNSTILE_MODE_SET` for `startPodiumShift`, `endPodiumShift`. |
| Offline (`?state=offline`) | Fully offline. The access point list is in the bundle |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `shift-ended`: the shift is already ended. |

#### Edge cases to draw

- **Offline at start**: Works from the bundle; the package age is shown in amber. *(source: screens/P07-staff-scanner.yaml#SCN-002 / F06 step 4)*

#### Consistency with other screens

- Match `BO-064`: Access point names and direction badges match the back office.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
session:
  point: Main Plaza Gate 2
  direction: Entry
  steward: Rahul Menon
  package: 06:40, valid to 18:00
```

#### Permissions

- `listAccessPoints` → `SCOPE_VIEW` (read) · staff
- `getAccessPoint` → `SCOPE_VIEW` (read) · staff
- `startPodiumShift` → `TURNSTILE_MODE_SET` (operate) · staff
- `endPodiumShift` → `TURNSTILE_MODE_SET` (operate) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listAccessPoints` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TURNSTILE_MODE_SET` for `startPodiumShift`, `endPodiumShift`.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
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
- Flow F06 branch at step 2 (recoverable): when The gate's direction is switched live during the shift, **The device picks up the new direction from the next push** (decided 2 October 2026, BO-230: "Live direction switch with permission, logged; R221 amended"; DEC-255, CHG-CSP-032). The switch is made …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Start podium shift, End podium shift.
- [ ] Every transition is wired: `SCN-015`, `SCN-001`, `SCN-003`, `SCN-016`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `TURNSTILE_MODE_SET`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-003` Ready to scan

**The screen the device sits on all day.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | Block A · task APP-SCANNER-SCN-003 |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `TICKET_LOOKUP` (3 operate); in the flows as contractor, gate operator, guest, partner |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | **Same loop, different truth. Amber says so.** Was a separate screen until 18 August, and the screen already had an `offline` state — two places describing one condition is two places to disagree. |
| Opens with | `mediaCode` (deepLink), `rightId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/access/ready-to-scan` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Absorbed SCN-004, SCN-005, SCN-006, SCN-010, SCN-012 on 18 August.** A scanner is one screen the device sits on all day, and an outcome is a state of it — **routing to `/access/admitted` for something gone in 1.5 seconds is a page load per guest**, and at a gate doing 40 a minute that is the whole problem. Every absorbed screen kept its copy as a named state. **Authoring operations removed 24 August**: addBlacklistEntry, removeBlacklistEntry. **A scanner reads the gate configuration; it does not write it.** An access point is created in the back office and a geofence is a venue decision — a handheld at a lane that can redefine the lane is a handheld that can admit anywhere.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): F06 step 4 says the ready screen calls nothing and is idle by design; the scan history (listScans needs the venue report permission) belongs to SCN-009, sync to … Removed 2 October 2026 (CHG-WIR-001): F06 step 4 says the ready screen calls nothing and is idle by design; the scan history (listScans needs the venue report permission) belongs to SCN-009, sync to … Removed 2 October 2026 (CHG-WIR-001): F06 step 4 says the ready screen calls nothing and is idle by design; the scan history (listScans needs the venue report permission) belongs to SCN-009, sync to …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The screen a scanner sits on all day: a camera/reader target, the access point and direction, the offline and package status, and each outcome as a state of the same screen - Admitted (green, gone in 1.5 s, party size and the right used), Denied (reason and the previous scan's time and gate), Override required, Blocked (blacklisted: no override, call a supervisor), plus Venue full and Waiver not completed. The one thing to get right: the reason is readable from arm's length and tells the steward what to say.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Customer photo on the result (DI-129) is still an open question (CHG-SPO-019)

**Fixed on main** (the package already carries these; draw what it says): Scan history table and filters (listScans needs venue report permission), blacklist table, sync and offline package panels on the ready … (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the admitted state show the guest's photo for name-bound passes?** → Drawn default accepted: Show name only; photo for accreditation credentials. *(decided by Chinmay, 2026-10-02; DEC-140 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

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

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Read**: Camera or RFID/NFC reader always armed; no typing on this screen. A manual-entry button leads to SCN-008, lookup to SCN-009, group to SCN-007. *(source: F06 step 4 / contracts/spine/access.yaml#validateAccess)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |
| Consume cross region entitlement (secondary button) | `consumeCrossRegionEntitlement` POST `/cross-region-entitlements/{rightId}/consume` | inline | CrossRegionEntitlement | 409 Entries exhausted, or the right is revoked or outside its window | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Admitted state**: Full-screen green, product and holder name where name-bound, "Admits 3", entries left; tier colour where the venue sets it (e.g. orange for child). *(source: screens/P07-staff-scanner.yaml#SCN-003 / DI-644 / contracts/spine/access.yaml#/components/schemas/ValidationResult)*
- **Denied state**: Red, the VO-R06 label in large type plus detail ("Already used 09:58 at Main Plaza Gate 1"), and the next action (Lookup, Call supervisor). *(source: F06 step 5 / contracts/spine/access.yaml#/components/schemas/DenyReason / DI-627)*
- **Blocked state**: Distinct from denied (black/red with a shield), no override button, "Call a supervisor". *(source: F06 step 5 / screens/P07-staff-scanner.yaml#SCN-003)*
- **Status strip**: Online/offline, package age, scans waiting to sync, access point and direction - always visible. *(source: DI-072 / F06 step 4)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Supervisor override**: Only for a denied (not blocked) scan; the supervisor authenticates, gives a reason; recorded as its own row against the denial. *(source: contracts/spine/access.yaml#overrideAccess / R228 / DI-649)*

**Where the user goes next**

- → `SCN-014` Sync & reconciliation: *Syncs the journal when signal returns*
- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Ready to scan*; carries `mediaCode`, `rightId`
- → `PTR-015` Order History: *Reviews usage*; calls `validateAccess`
- → `SCN-011` Delegated right: *Delegated right*; carries `rightId`
- → `SCN-007` Group admission: *A school party of forty arrives on one booking*; calls `validateAccess`

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A ready scan this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ready scan list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ready scan untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ready scan yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the ready scan are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TICKET_LOOKUP`, which `lookupTicket` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Same loop, different truth. Amber says so.** Was a separate screen until 18 August, and the screen already had an `offline` state — two places describing one condition is two places to disagree. |
| Admitted (`?state=admitted`) | **Green, and gone in 1.5 seconds.** The absorbed SCN-004. Shows what was admitted and against which right; at a gate doing 40 a minute this is the state the device is in most of the time. |
| Denied (`?state=denied`) | Denied with the reason and the time of the previous scan. **The reason matters more than the refusal** — a steward has to explain it to somebody standing in front of them. The absorbed SCN-005. Two causes read differently on the device: **"Time window ended"** for a time-bound entitlement scanned after its N minutes from the first scan (`timeBoundWindowElapsed`, CHG-CSP-030), and **"Reader offline too long"** when the reader is past the venue's maximum offline duration and must reconnect before … |
| Override required (`?state=overrideRequired`) | A supervisor override, which requires a permission a steward may not hold, and records who, why and when. The absorbed SCN-006. |
| Blocked (`?state=blocked`) | Blacklisted or otherwise barred. **No override is offered on the device** — this is not a judgement a steward makes at a lane. The absorbed SCN-010. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 No identifier supplied; 400 Validation failed; 409 Entries exhausted, or the right is revoked or outside its window |

#### Edge cases to draw

- **Offline**: Same loop in amber; validation from the bundle; every scan journalled. *(source: F06 step 4 / DI-013 / DI-646)*
- **Venue at maximum live occupancy**: Denied "Venue full - entry resumes as guests leave". *(source: DI-650)*
- **Waiver incomplete**: Denied "Waiver not completed" with where to complete it. *(source: DI-574)*
- **Exit without matching check-out**: Next re-entry denied "Exit scan missing - see supervisor". *(source: DI-461)*
- **Accreditation credential presented**: Shows the person's photo, organisation, category and zones allowed now. *(source: contracts/satellite/accreditation.yaml#verifyAccreditationCredential)*
- **Face review range**: Amber "Check the guest's face" with operator confirm where face thresholds put the match in review. *(source: contracts/spine/access.yaml#setFaceMatchingVerification)*

#### Consistency with other screens

- Match `EMP-010`: Same states and wording in the Staff App.
- Match `BO-034`: Same deny labels in the back office.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outcomes:
- state: Admitted
  product: Aqua Park Day Pass
  admits: 1
  remaining: 0
- state: Denied
  reason: Already used
  detail: 09:58 at Main Plaza Gate 1
- state: Blocked
  reason: Blacklisted
```

#### Permissions

- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff
- `consumeCrossRegionEntitlement` → `ACCESS_VALIDATE` (operate) · staff
- `verifyAccreditationCredential` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `TICKET_LOOKUP`, which `lookupTicket` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

46 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.17 | The system should have the ability to scan a ticket into a POS terminal and display record of ticket’s history: transaction time, clerk, payment method, etc. | Admission and Access | CONTRACTED | `lookupTicket` |
| 1.1.61 | Entitlement validity validation | Ticketing Catalogue | CONTRACTED | `validateAccess` |
| 1.1.62 | Entitlement consumption tracking | Ticketing Catalogue | CONTRACTED | `validateAccess` |
| 3.1.3 | Dynamic Refresh: QR codes refresh periodically (e.g., every 30–60 seconds) to prevent screenshots or duplication. | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.2 | The Ticketing PLUs shall be printed on E-tickets Ticketing PLUs shall be printed on Wristbands (paper and RFID) | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.3 | The Ticketing PLUs shall be printed on M-tickets | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.5 | The ticket id can be generated in 2D barcode The ticket id can be generated in QR code The ticket id can be generated in RFID (ISO 15693) The ticket ID number sequence is created by the sales system … | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.8 | The system should be able to validate different media types in a transparent way, linear barcode, QR code, RFID and NFC. | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.12 | The system should be able to support child-protection journey in multiple ways such as: - Require scan of an adult ticket as a pair to a child ticket to enable entry/exit from an attraction - Require … | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.14 | The system should have the ability to recognize and read the ticket format sold by resellers and external partners. | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.15 | The system should have the ability to display a reason code on the scanner if the ticket is invalid. A ticket can be manually invalidated by an administrator. | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.16 | The system should have the ability to scan and check-in at self-service turnstile and access control device. | Admission and Access | CONTRACTED | `validateAccess` |
| … 34 more | | | | `traceability.json` |

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
- Flow F62 *A ticket will not scan*, step 3: It is valid. The guest is admitted. → Recorded as a manual admission. **The manual rate at a gate is a hardware signal** — one lane doing forty a day has a broken reader.
- Flow F06 branch at step 5 (recoverable): when Entitlement already fully consumed, SCN-003 shows denied with the reason and the time of the previous scan. **The reason matters more than the denial** — a steward facing a guest needs to say what happened, not just no.
- Flow F06 branch at step 5 (requiresStaff): when Guest is blacklisted, SCN-003, handled differently from an ordinary denial: no override offered on the device, and a supervisor is summoned.
- Flow F06 branch at step 5 (recoverable): when Media unreadable — damaged QR, dead phone, SCN-008 manual entry by reference, or SCN-009 lookup by name. Both are slower and both are necessary.
- Flow F06 branch at step 5 (recoverable): when Party larger than the entitlement, SCN-007 group admission admits what is valid and states the shortfall, rather than refusing the whole party at a gate with a queue behind it.
- Flow F06 branch at step 5 (requiresStaff): when Steward believes the denial is wrong, Supervisor override on SCN-003, which requires a permission a steward may not hold and records who, why and against which scan.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, admitted, denied, overrideRequired, blocked.
- [ ] Every action is wired with its success and its failure: Lookup ticket, Override access, Validate access, Validate group access, Consume cross region entitlement.
- [ ] Every transition is wired: `SCN-014`, `SCN-001`, `SCN-002`, `SCN-003`, `PTR-015`, `SCN-011`, `SCN-007`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `TICKET_LOOKUP`.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 6 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-007` Group admission

**Partial admission is the normal case, not the error.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | Block C · task APP-SCANNER-SCN-007 |
| Who uses it | venue staff holding `ACCESS_VALIDATE`, `TICKET_LOOKUP` (2 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Fully offline. Admits what is valid and states the shortfall |
| Opens with | nothing: it opens on its own |
| Route | `/access/group-admission` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Scan history, sync, override and single-validate actions were generated from the scanner set; the group screen needs the group counter and the admit stepper … Removed 2 October 2026 (CHG-WIR-001): Scan history, sync, override and single-validate actions were generated from the scanner set; the group screen needs the group counter and the admit stepper … Removed 2 October 2026 (CHG-WIR-001): Scan history, sync, override and single-validate actions were generated from the scanner set; the group screen needs the group counter and the admit stepper …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Admitting a school party or tour group on one credential: the scanner shows the party size, how many have entered and how many remain, and the steward enters how many are passing now. Partial admission is the normal case; the group stays open for the rest. The one thing to get right: a big counter (38 of 40 in, 2 to come) and a fast stepper.

**Fixed on main** (the package already carries these; draw what it says): Scan history filters and table, sync, override and single validate actions on the group screen (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
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

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Admit count**: Stepper defaulting to the remaining count; cannot exceed remaining; each admission is counted individually for occupancy. *(source: contracts/spine/access.yaml#validateGroupAccess / F61 step 5)*

#### Outputs: what the screen shows and produces

**Shown**

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Validate group access (primary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Group counter**: Group name/booking, size, admitted so far, remaining; for a group QR model also shows whether it is one QR for the headcount or individual QRs. *(source: contracts/spine/access.yaml#validateGroupAccess / DI-569 / DI-137)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Admit**: Admits the number, states any shortfall ("2 not yet arrived - group stays open"). *(source: F06 step 5 / F61 step 6)*

**Data it reads**: `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation)

**Where the user goes next**

- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Ready to scan*; carries `mediaCode`, `rightId`
- → `SCN-014` Sync & reconciliation: *The session ends and the device syncs*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group admission list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group admission untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group admission yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the group admission are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`. |
| Offline (`?state=offline`) | Fully offline. Admits what is valid and states the shortfall |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 409 Requested count exceeds the remaining group allowance |

#### Edge cases to draw

- **Party larger than the entitlement**: Admits what is valid and states the shortfall rather than refusing all. *(source: F06 step 5)*
- **Offline**: Works from the bundle; the counter is local until sync. *(source: screens/P07-staff-scanner.yaml#SCN-007)*

#### Consistency with other screens

- Match `EMP-015`: Same counter on the Staff App.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
group:
  booking: Al Noor School - Grade 5
  size: 40
  admitted: 38
  remaining: 2
```

#### Permissions

- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 1 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Validate group access, Lookup ticket.
- [ ] Every transition is wired: `SCN-001`, `SCN-002`, `SCN-003`, `SCN-014`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`, `TICKET_LOOKUP`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-008` Manual entry

**Damaged media, dead phone battery, printed slip.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | Block C · task APP-SCANNER-SCN-008 |
| Who uses it | venue staff holding `ACCESS_VALIDATE`, `TICKET_LOOKUP` (2 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Searches the bundle only. A reference issued after the last sync will not be found, and the screen says so rather than denying |
| Opens with | nothing: it opens on its own |
| Route | `/access/manual-entry` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Manual entry needs the reference field and the validate result only; the scan table, sync, override and group validation were generated from the scanner set … Removed 2 October 2026 (CHG-WIR-001): Manual entry needs the reference field and the validate result only; the scan table, sync, override and group validation were generated from the scanner set … Removed 2 October 2026 (CHG-WIR-001): Manual entry needs the reference field and the validate result only; the scan table, sync, override and group validation were generated from the scanner set …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Manual entry when media will not read (damaged QR, dead phone, printed slip): the steward types the ticket or media reference exactly - no fuzzy matching - and the result is the same as a scan. The one thing to get right: an exact, structured entry field matching the ticket number format.

**Fixed on main** (the package already carries these; draw what it says): Generated scan table, sync, override and group validation actions (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |

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

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reference**: Input mask matching the venue's ticket number format (e.g. VT-2026-000009821) or media code; exact match only. *(source: F62 step 1 / contracts/spine/access.yaml#setVirtualTicketIdentity)*

#### Outputs: what the screen shows and produces

**Shown**

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lookup ticket (primary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Result**: Found - show the ticket and validate (outcome states as SCN-003); not found - "No ticket with this number" never "denied". *(source: F62 step 1 / screens/P07-staff-scanner.yaml#SCN-008)*

**Data it reads**: `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation)

**Where the user goes next**

- → `SCN-009` Ticket lookup: *The ticket is found and its history read*; calls `lookupTicket`
- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Ready to scan*; carries `mediaCode`, `rightId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The manual entry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the manual entry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No manual entry yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the manual entry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`. |
| Offline (`?state=offline`) | Searches the bundle only. A reference issued after the last sync will not be found, and the screen says so rather than denying |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed |

#### Edge cases to draw

- **Offline and the ticket was issued after the last sync**: "Not in this device's package (from 06:40) - check with a supervisor", not a denial. *(source: screens/P07-staff-scanner.yaml#SCN-008)*

#### Consistency with other screens

- Match `SCN-009`: Found tickets can open their history.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entry:
  typed: VT-2026-000009821
  found: Aqua Park Day Pass - valid today
```

#### Permissions

- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`.

#### Requirements it meets

47 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 1.1.61 | Entitlement validity validation | Ticketing Catalogue | CONTRACTED | `validateAccess` |
| 1.1.62 | Entitlement consumption tracking | Ticketing Catalogue | CONTRACTED | `validateAccess` |
| 3.1.3 | Dynamic Refresh: QR codes refresh periodically (e.g., every 30–60 seconds) to prevent screenshots or duplication. | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.2 | The Ticketing PLUs shall be printed on E-tickets Ticketing PLUs shall be printed on Wristbands (paper and RFID) | Admission and Access | CONTRACTED | `validateAccess` |
| … 35 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket, Validate access.
- [ ] Every transition is wired: `SCN-009`, `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`, `TICKET_LOOKUP`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-009` Ticket lookup

**Reads. Does not admit, does not decrement.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | Block C · task APP-SCANNER-SCN-009 |
| Who uses it | venue staff holding `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (3 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Bundle only, and the bundle age is shown beside the results |
| Opens with | nothing: it opens on its own |
| Route | `/access/ticket-lookup` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Validate, group validate, sync and override contradict the screen's own purpose ("Reads. Does not admit, does not decrement") and lookupTicket's contract … Removed 2 October 2026 (CHG-WIR-001): Validate, group validate, sync and override contradict the screen's own purpose ("Reads. Does not admit, does not decrement") and lookupTicket's contract … Removed 2 October 2026 (CHG-WIR-001): Validate, group validate, sync and override contradict the screen's own purpose ("Reads. Does not admit, does not decrement") and lookupTicket's contract …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Read-only ticket lookup: validity, entries used and left, and the complete scan history (gate and time of every attempt, outcome and reason) so security can resolve "it says I already used it" - for example a scan that marked the ticket used though the guest never passed. It never admits and never decrements. The one thing to get right: the history line "Scanned at North Gate at 10:14" is the answer, shown first.

**Fixed on main** (the package already carries these; draw what it says): Validate, group validate, sync and override actions on a lookup screen whose purpose is "does not admit" (CHG-WIR-001).

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

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search**: Scan the media or type the exact reference; name search only where the ticket is name-bound. *(source: contracts/spine/access.yaml#lookupTicket / F06 step 5)*

#### Outputs: what the screen shows and produces

**Shown**

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |

**The selected scan event** (detail panel, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | Null while pending. Differs from recordedAt for offline scans. |

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lookup ticket (primary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ticket status**: Product, validity window, entries used of allowed, inside the venue or not, holder where name-bound. *(source: contracts/spine/access.yaml#/components/schemas/TicketStatus)*
- **History**: Every attempt with gate, time, outcome, reason and operator, newest first; consumption beyond admission (F&B combo redeemed, wallet spend) where available. *(source: DI-649 / DI-462 / DI-627 / F62 step 2)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Back to scanning / supervisor override**: Override only through SCN-003 on a denied scan with the supervisor's credentials. *(source: contracts/spine/access.yaml#overrideAccess)*

**Data it reads**: `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *It is valid*; carries `mediaCode`, `rightId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket lookup list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket lookup untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket lookup yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the ticket lookup are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_VENUE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`. |
| Offline (`?state=offline`) | Bundle only, and the bundle age is shown beside the results |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied |

#### Edge cases to draw

- **Offline**: Bundle only, with the bundle age beside the results. *(source: screens/P07-staff-scanner.yaml#SCN-009)*

#### Consistency with other screens

- Match `BO-226`: Back-office ticket lookup shows the same history.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ticket:
  number: VT0010
  product: Aqua Park Day Pass
  used: 1 of 1
  history:
  - 10:14 Admitted - North Gate - Rahul Menon
  - 10:16 Denied - Already used - Main Plaza Gate 2
```

#### Permissions

- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_VENUE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 3 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket.
- [ ] Every transition is wired: `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-011` Delegated right

**A ticket issued in another cell, redeemed here.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `core` module |
| Block | Block B · task APP-SCANNER-SCN-011 |
| Who uses it | venue staff holding `ACCESS_VALIDATE`, `TICKET_LOOKUP` (2 operate) |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getCrossRegionEntitlement` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available offline.** A delegated right issued in another region cannot be verified from a local bundle, and admitting on trust is how a pass gets used twice in two countries |
| Opens with | `rightId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/access/delegated-right` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** At the gate, a ticket or membership issued in another country's cell is redeemed here: the scanner reads the local copy of the right (not the right itself), shows entries allowed and used, and consumes one entry. Reconciliation with the issuing cell happens afterwards.

**Fixed on main** (the package already carries these; draw what it says): formConsumeCrossRegionEntitlement asks the person for id. (CHG-SPO-018); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SPO-018).

#### Inputs: what the user enters or picks

**Form: Consume cross region entitlement** (modal, opened by *Consume cross region entitlement*; *Consume cross region entitlement* calls `consumeCrossRegionEntitlement`, *Cancel* sends nothing)

**Confirms the redemption.** The id is a UUIDv7 the device generates; status and time are the server's, so nothing here is typed (design-notes correction platform-foundation SCN-011).

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
| Issuing cell name | text | — |
| Consuming cell name | text | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Status | chip: Active, Exhausted, Revoked, Expired | — |
| Last consumed at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Consume cross region entitlement (primary button) | `consumeCrossRegionEntitlement` POST `/cross-region-entitlements/{rightId}/consume` | inline | CrossRegionEntitlement | 409 Entries exhausted, or the right is revoked or outside its window | works offline; opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Right**: Issuing cell (country), validity window in the venue's time zone, entries used of allowed, status; a right valid elsewhere but not here says why. *(source: contracts/spine/cross-region.yaml#getCrossRegionEntitlement; F19 step 2)*

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
| Empty, first run (`?state=emptyFirstRun`) | Never a create action: a delegated right arrives by scan. With nothing scanned the screen says "Scan the ticket from the other venue". |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TICKET_LOOKUP`, which `getCrossRegionEntitlement` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_VALIDATE` for `consumeCrossRegionEntitlement`. |
| Offline (`?state=offline`) | **Not available offline.** A delegated right issued in another region cannot be verified from a local bundle, and admitting on trust is how a pass gets used twice in two countries |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Entries exhausted, or the right is revoked or outside its window |

#### Edge cases to draw

- **Offline at the gate**: The right is read from the local copy (offline-capable); the consumption is reconciled later and the screen says so. *(source: contracts/spine/cross-region.yaml#getCrossRegionEntitlement; F19 step 5)*
- **Can read but not change (holds TICKET_LOOKUP only)**: Everything reads; the actions needing another permission are not offered as live buttons: ACCESS_VALIDATE for Consume cross region entitlement. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/cross-region.yaml#consumeCrossRegionEntitlement)*
- **consumeCrossRegionEntitlement answers 409**: Show it as something the person can act on, not a failure: Entries exhausted, or the right is revoked or outside its window *(source: contracts/spine/cross-region.yaml#consumeCrossRegionEntitlement)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
right:
  holder: Aisha Al Nuaimi
  product: AquaCove Annual Pass Gold
  issuedIn: UAE cell
  venue: AquaCove Muscat
  entries: 3 of unlimited
  validTo: 31/12/2026
```

#### Permissions

- `getCrossRegionEntitlement` → `TICKET_LOOKUP` (operate) · staff
- `consumeCrossRegionEntitlement` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `TICKET_LOOKUP`, which `getCrossRegionEntitlement` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_VALIDATE` for `consumeCrossRegionEntitlement`.

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
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-011?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Consume cross region entitlement.
- [ ] Every transition is wired: `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`, `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-013` Offline journal

**What the device decided, before anyone confirmed it.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | Block C · task APP-SCANNER-SCN-013 |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `TICKET_LOOKUP` (3 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | The journal is the offline record. It is why an offline admit is recoverable |
| Opens with | nothing: it opens on its own |
| Route | `/access/offline-journal` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The offline journal is local to the device and needs no server read; listScans returns server scans and needs the venue report permission (F63 step 2 …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The offline journal: every decision the device made while disconnected - admissions and refusals - in sequence, waiting to be posted. The one thing to get right: the count and the oldest unsynced time are prominent, because a journal is what makes an offline admit recoverable.

**Fixed on main** (the package already carries these; draw what it says): The journal is drawn from listScans (server scans, venue report permission) (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
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

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lookup ticket (primary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Sync scans (secondary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Journal list**: Sequence number, device time, media, outcome and reason, sync state (waiting, sent, accepted, rejected); refusals included. *(source: F63 step 2 / DI-065)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Sync now**: Posts in sequence order in batches; scanning continues during sync. *(source: contracts/spine/access.yaml#syncScans / F06 step 6)*

**Data it reads**: `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation)

**Where the user goes next**

- → `SCN-014` Sync & reconciliation: *The network returns and the journal posts*
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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess`; `TICKET_LOOKUP` for `lookupTicket`. |
| Offline (`?state=offline`) | The journal is the offline record. It is why an offline admit is recoverable |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Edge cases to draw

- **Journal too large for one pass**: Batched with progress; the device keeps journalling. *(source: F06 step 6)*

#### Consistency with other screens

- Match `SCN-014`: After posting, rejections appear there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
journal:
  waiting: 214
  oldest: '10:02'
  last: 10:41 Admitted VT0912
```

#### Permissions

- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess`; `TICKET_LOOKUP` for `lookupTicket`.

#### Requirements it meets

53 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| 3.2.17 | The system should have the ability to scan a ticket into a POS terminal and display record of ticket’s history: transaction time, clerk, payment method, etc. | Admission and Access | CONTRACTED | `lookupTicket` |
| 18.1.4 | Synchronization - System shall synchronize data when connectivity is restored. | Employee Mobile App & AI Assistant | CONTRACTED | `syncScans` |
| 1.1.61 | Entitlement validity validation | Ticketing Catalogue | CONTRACTED | `validateAccess` |
| 1.1.62 | Entitlement consumption tracking | Ticketing Catalogue | CONTRACTED | `validateAccess` |
| 3.1.3 | Dynamic Refresh: QR codes refresh periodically (e.g., every 30–60 seconds) to prevent screenshots or duplication. | Admission and Access | CONTRACTED | `validateAccess` |
| … 41 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-013?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket, Override access, Sync scans, Validate access, Validate group access.
- [ ] Every transition is wired: `SCN-014`, `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `TICKET_LOOKUP`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-014` Sync & reconciliation

**The screen nobody designs and everybody needs.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | Block A · task APP-SCANNER-SCN-014 |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `ORDER_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate, 1 read); in the flows as gate operator, guest |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listSyncRejections` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Not applicable. This screen exists to end the offline period |
| Opens with | nothing: it opens on its own |
| Route | `/access/sync-reconciliation` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Cross-platform navigation removed 24 August**: ADM-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): A scanner replays scans; syncOrders replays till sales and belongs to the POS (design-notes correction venue-operations SCN-014).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Ends the offline period: the journal posts in sequence, the server accepts most and may reject some, and the steward sees which admissions the server disagreed with (the guest is already inside) so a duty manager can deal with them. The one thing to get right: rejections never disappear behind an "all synced" tick.

**Fixed on main** (the package already carries these; draw what it says): Sync orders (till sales) and a "Workstation id" text filter on the scanner (CHG-WIR-001).

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
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |

**The selected sync rejection** (detail panel, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Resolved at | 1 Oct 2026, 14:30 | — |

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sync scans (primary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Sync summary**: Sent, accepted, rejected counts with recorded and synced times. *(source: DI-065 / F06 step 6)*
- **Rejections**: Each rejected scan with ticket, gate, device time and the server's reason; marked "for the duty manager" (resolved in BO-038). *(source: contracts/spine/orders.yaml#listSyncRejections / F06 step 6)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Sync scans**: Ordered batch, stops at the first entry it cannot accept and reports those processed. *(source: contracts/spine/access.yaml#syncScans)*

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission (the screen's other reads need `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess` … |
| Offline (`?state=offline`) | Not applicable. This screen exists to end the offline period |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Edge cases to draw

- **Cross-region pass redeemed here**: Shown when the issuing cell later disagrees; surfaced, not silently resolved. *(source: F19 step 4 / contracts/spine/cross-region.yaml#consumeCrossRegionEntitlement)*

#### Consistency with other screens

- Match `BO-038`: Same rejection rows on the back office.
- Match `EMP-017`: Same screen in the Staff App.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sync:
  sent: 214
  accepted: 212
  rejected: 2
  rejection: VT0933 at North Entry 10:12 - already used at 09:58 Gate 1
```

#### Permissions

- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission (the screen's other reads need `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess` …

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 48 more | | | | `traceability.json` |

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
- Flow F61 *A gate opens, a steward signs in, and a group is admitted*, step 7: The session ends and the device syncs. → Scans posted in sequence. **A duplicate scan across two devices is resolved on sync, not at the gate** — refusing a guest because another lane might have seen them is a queue nobody accepts.
- Flow F63 *A gate goes offline and reconciles*, step 3: The network returns and the journal posts. → **In sequence, not by timestamp.** Two handhelds with clocks a minute apart produce an order nobody can reconstruct.
- Flow F06 branch at step 6 (requiresStaff): when Server rejects a scan the device already admitted, SCN-014 reconciliation. The guest is already inside. This is a revenue and audit event, not a gate event, and it is why the journal exists.
- Flow F06 branch at step 6 (recoverable): when Journal too large to sync in one pass, Batched. The device keeps journalling while it syncs — a device that stops scanning to sync is a closed gate.
- Flow F19 branch at step 4 (requiresStaff): when Both cells think the pass was used once, at the same time, A single-entry pass redeemed in two countries in one day is either fraud or a clock. **The scan timestamps decide**, and both are retained with recordedAt and syncedAt for exactly this.
- Flow F61 branch at step 7 (medium): when The same guest was scanned at two lanes while both were offline., **Both scans post and the duplicate is a reconciliation task**, not a reversal. The guest is inside either way; the question is which lane counted them.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync scans, Lookup ticket, Override access, Validate access, Validate group access.
- [ ] Every transition is wired: `SCN-001`, `SCN-002`, `SCN-003`, `ADM-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `ORDER_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-015` Offline package

**Rule changes land here, not instantly.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | Block C · task APP-SCANNER-SCN-015 |
| Who uses it | venue staff holding `ACCESS_VALIDATE`, `TICKET_LOOKUP` (2 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Cannot refresh. The existing bundle continues to be used and its age is shown |
| Opens with | nothing: it opens on its own |
| Route | `/access/offline-package` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The package screen shows the package; the scan table, override, validate and sync actions were the generated scanner set (design-notes correction … Removed 2 October 2026 (CHG-WIR-001): The package screen shows the package; the scan table, override, validate and sync actions were the generated scanner set (design-notes correction … Removed 2 October 2026 (CHG-WIR-001): The package screen shows the package; the scan table, override, validate and sync actions were the generated scanner set (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The offline package on the device: when it was built, its validity window, what it holds (entitlements, blacklist, admission profiles, active policy version, accreditation credentials) and a refresh. Rule changes land here, not instantly. The one thing to get right: the package age and "valid until" are shown in plain words and turn amber when old.

**Fixed on main** (the package already carries these; draw what it says): Scan table, override, validate and sync actions (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |

#### Outputs: what the screen shows and produces

**Shown**

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lookup ticket (primary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Package card**: "Built 06:40 - valid until 18:00 - 12,480 tickets - blacklist 37 - policy version 3.5"; amber after a venue-set age. *(source: contracts/spine/access.yaml#getOfflinePackage / ADR-0068 / F06 step 3)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Refresh**: Conditional download (unchanged package not re-downloaded); pulled before the session, not at first scan. *(source: contracts/spine/access.yaml#getOfflinePackage / F61 step 3)*

**Data it reads**: `getOfflinePackage` (onLoad, From the flow it appears in)

**Where the user goes next**

- → `SCN-013` Offline journal: *Scans journal locally while the network is gone*; calls `getOfflinePackage`
- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Waits at the ready screen*; carries `mediaCode`, `rightId`; calls `getOfflinePackage`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline package list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline package untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline package yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the offline package are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`. |
| Offline (`?state=offline`) | Cannot refresh. The existing bundle continues to be used and its age is shown |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied |

#### Edge cases to draw

- **Offline**: Cannot refresh; existing bundle continues and its age is shown. *(source: screens/P07-staff-scanner.yaml#SCN-015)*

#### Consistency with other screens

- Match `BO-032`: Profile edits say they apply after the next package refresh; this screen shows when that happened.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
package:
  built: 06:40
  validTo: '18:00'
  tickets: 12480
  blacklist: 37
  policy: v3.5
```

#### Permissions

- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TICKET_LOOKUP` for `lookupTicket`.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| 3.2.17 | The system should have the ability to scan a ticket into a POS terminal and display record of ticket’s history: transaction time, clerk, payment method, etc. | Admission and Access | CONTRACTED | `lookupTicket` |

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

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket.
- [ ] Every transition is wired: `SCN-013`, `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`, `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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
"changeOwnCredential": {"method":"POST","path":"/auth/credential","contract":"identity","summary":"Change the caller's own password or PIN","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChangeCredentialRequest","responds":null},
"consumeCrossRegionEntitlement": {"method":"POST","path":"/cross-region-entitlements/{rightId}/consume","contract":"cross-region","summary":"Consume entries against a right, locally authoritative","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CrossRegionEntitlement"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"endPodiumShift": {"method":"POST","path":"/podium-shifts/{shiftId}/end","contract":"access","summary":"End an operator shift on a podium","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPodiumShift"},
"getAccessPoint": {"method":"GET","path":"/access-points/{accessPointId}","contract":"access","summary":"Read an access point","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccessPoint"},
"getCrossRegionEntitlement": {"method":"GET","path":"/cross-region-entitlements/{rightId}","contract":"cross-region","summary":"Read a redemption right","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CrossRegionEntitlement"},
"getCurrentSession": {"method":"GET","path":"/auth/session","contract":"identity","summary":"Current session and effective permissions","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Session"},
"getOfflinePackage": {"method":"GET","path":"/access/offline-package","contract":"access","summary":"Entitlement and rule set for offline validation","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"sinceVersion","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":"validFrom","in":"query","required":true},{"name":"validTo","in":"query","required":true},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"OfflinePackage"},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSyncRejections": {"method":"GET","path":"/sync/rejections","contract":"orders","summary":"Entries the server refused","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"resolved","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"login": {"method":"POST","path":"/auth/login","contract":"identity","summary":"Authenticate and open a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LoginRequest","responds":"LoginResponse"},
"lookupTicket": {"method":"GET","path":"/access/lookup","contract":"access","summary":"Read-only validity check without admitting","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaCode","in":"query","required":null},{"name":"ticketId","in":"query","required":null}],"requestBody":null,"responds":"TicketStatus"},
"overrideAccess": {"method":"POST","path":"/access/override","contract":"access","summary":"Admit against a failed validation","permission":"ACCESS_OVERRIDE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"selectRole": {"method":"POST","path":"/auth/select-role","contract":"identity","summary":"Choose a role for a multi-role session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Session"},
"startPodiumShift": {"method":"POST","path":"/podiums/{podiumId}/shifts","contract":"access","summary":"Start an operator shift on a podium","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPodiumShift"},
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
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n\n**R221 amended 2 October 2026: a gate's direction can be switched live** (Chinmay, critical set 1, BO-230: \"Live direction switch with permission, logged\"; DEC-255; CHG-CSP-032; DI-648: more entry gates in the morning, more exit gates in the evening). `setAccessPointDirection` switches it from Live Gate Mode & Lane Control (BO-230) or the scanner's gate mode screen (SCN-016) for a holder of the configuration right, logged; the podium's `setTurnstileMode` still never touches it.\n"},"temporaryClosure":{"type":"object","nullable":true,"description":"**What the access point does while its attraction is temporarily closed** (decided 2 October 2026, Chinmay, batch 6 set 9, BO-147: \"Deny + reopening time + a virtual-queue return window where enabled\"; DEC-228; CHG-CSP-026). While `isClosed`, every scan is denied (`ValidationResult.denyCause` `attractionTemporarilyClosed`) with the reopening time when it is known; where the venue offers it and the attraction has a virtual queue, the guest is offered a return window (`queue.joinQueue`) instead of being turned away empty-handed. Set with `updateAccessPoint`; null when open. Travels in the offline package, so an offline gate denies the same way.","properties":{"isClosed":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":200,"nullable":true,"description":"Shown to staff; the guest sees \"Attraction temporarily closed\"."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When it is expected to reopen; shown to the guest when known."},"offerVirtualQueueReturn":{"type":"boolean","default":false,"description":"Offer a virtual-queue return window at the denied scan, where the attraction has a queue."},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The virtual queue the return window is taken in."}}},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"AccreditationCredentialVerification": {"type":"object","description":"18.8.3. **What a steward needs to believe the person in front of them**: the face, the name, the category and the zones, and whether any of it is valid now. Returned by `verifyAccreditationCredential`; not stored.\n","required":["outcome"],"properties":{"outcome":{"type":"string","enum":["valid","notYetValid","expired","suspended","revoked","credentialReplaced","credentialLost","credentialInactive"],"description":"`valid` only when the holder is `active`, today is inside the holder's validity, and the credential is `issued` or `active`"},"reason":{"type":"string","nullable":true},"credentialId":{"type":"string","format":"uuid"},"credentialKind":{"type":"string"},"credentialStatus":{"type":"string"},"holderId":{"type":"string","format":"uuid"},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"photoUrl":{"type":"string","nullable":true,"description":"Signed and short-lived, so the scan screen can show the face without a second call"},"organisationName":{"type":"string","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"categoryName":{"type":"string","nullable":true},"holderStatus":{"type":"string"},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"effectiveZones":{"type":"array","description":"The zones the holder may enter under their profiles and exceptions, today","items":{"type":"object","properties":{"zoneId":{"type":"string","format":"uuid"},"zoneName":{"type":"string"},"allowedNow":{"type":"boolean","description":"Inside the profile schedule (date, day, time, event phase) at this moment"}}}},"escortRequired":{"type":"boolean"},"zoneCheck":{"type":"object","nullable":true,"description":"Present when `zoneId` was given","properties":{"zoneId":{"type":"string","format":"uuid"},"allowed":{"type":"boolean"},"reason":{"type":"string","nullable":true}}},"checkedAt":{"type":"string","format":"date-time"}}},
"ChangeCredentialRequest": {"type":"object","description":"Request only. The credential itself is stored hashed in `identity.principal_credential` and is never returned by any operation (`handoff/schema-storage-only.md`).\n","required":["method","currentCredential","newCredential"],"properties":{"method":{"type":"string","enum":["password","pin"],"description":"Which credential is being changed. Card, RFID and SSO are not secrets the principal holds, so they are not changed here."},"currentCredential":{"type":"string","maxLength":512,"writeOnly":true},"newCredential":{"type":"string","maxLength":512,"writeOnly":true}}},
"CrossRegionEntitlement": {"x-ticvai-persistence":"platform.cross_region_entitlement","type":"object","required":["rightId","ticketId","issuingCellName","consumingCellName","validFrom","validTo","entriesAllowed","entriesConsumed","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"rightId":{"type":"string","format":"uuid"},"ticketId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"issuingCellName":{"type":"string"},"consumingCellName":{"type":"string"},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"admissionRulesId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Null where the right is valid at any venue in the consuming cell."},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"entriesConsumed":{"type":"integer"},"status":{"type":"string","enum":["active","exhausted","revoked","expired"]},"lastConsumedAt":{"type":"string","format":"date-time","nullable":true},"lastReconciledAt":{"type":"string","format":"date-time","nullable":true}}},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"LoginRequest": {"type":"object","description":"**`workstationId` is required for a device door and absent from a browser door** (CHG-DOOR-001, 2 October 2026). It was required on every login, so no browser could sign in: the TICVAI Console (ADM-001), Venue Management (SUP-001) and the partner portal (PTR-001) have no workstation. Optional in the schema is additive against r1; the rule moved to where it belongs, the device-bound methods: `pin`, `card` and `rfid` without a `workstationId` are refused 400 (`workstation-required`). A `password` sign-in from a till, handheld or scanner still sends it, because the workstation decides the Sale Board, the hardware and the till identity (never a permission, ADR-0002).\n","required":["username","credential"],"properties":{"username":{"type":"string","maxLength":256},"credential":{"type":"string","description":"Password, PIN, card token or RFID token depending on `method`.\n","maxLength":512,"writeOnly":true},"method":{"type":"string","description":"**`pin` is how a till is actually used.** A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets shortened, shared or written on the drawer. The employee number goes in `username` and the PIN in `credential`, so the shape of the request does not change — only what the operator types.\n\n**A PIN is weaker than a password and the difference is bounded by the device, not by the secret.** A `pin` (like `card` and `rfid`) is accepted only with a `workstationId`, refused 400 `workstation-required` without one (CHG-DOOR-001), and the workstation is *NOT a permission source*: it says which till, and the till is on a venue network in a staff area. A PIN is a reasonable credential there and nowhere else, which is why this is an enum value and not a policy flag — a surface that wants it has to ask for it by name.\n\nAdded 10 September 2026 for `POS-000 Sign In`.\n","enum":["password","pin","card","rfid","sso"],"default":"password"},"workstationId":{"type":"string","format":"uuid","description":"Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. NOT a permission source.\n\n**Sent by a device door, never by a browser** (CHG-DOOR-001, 2 October 2026). Required in effect for the device-bound methods `pin`, `card` and `rfid` (400 `workstation-required` without it); absent on the TICVAI Console, Venue Management and partner portal sign-ins, which have no workstation.\n"},"deviceFingerprint":{"type":"string","maxLength":256}}},
"LoginResponse": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/TokenPair"},{"type":"object","required":["requiresRoleSelection","requiresMfa"],"properties":{"requiresRoleSelection":{"type":"boolean"},"requiresMfa":{"type":"boolean","description":"True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). The session is not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge."},"hasMfaMethod":{"type":"boolean","description":"Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 (5))."},"mfaMethods":{"type":"array","description":"The principal's active methods, so the client can offer the right one for the `signIn` challenge. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"availableRoles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"session":{"$ref":"#/components/schemas/Session"}}}]},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"OfflinePackage": {"x-ticvai-persistence":"none — generated artefact in object storage","type":"object","required":["etag","generatedAt","validFrom","validTo","accessPointId","entitlements"],"properties":{"etag":{"type":"string"},"generatedAt":{"type":"string","format":"date-time"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"accessPointId":{"type":"string","format":"uuid"},"entitlementsVersion":{"type":"integer","description":"The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."},"policySetVersion":{"type":"string","description":"**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."},"dynamicPolicies":{"type":"array","description":"The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.","items":{"$ref":"#/components/schemas/AccessDynamicPolicy"}},"entitlements":{"type":"array","description":"Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.","items":{"type":"object","required":["ticketId","mediaCodes","validFrom","validTo","entriesAllowed","reentryAllowed"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id`."},"mediaCodes":{"type":"array","items":{"type":"string"},"description":"A ticket may carry several media over its life."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesAllowed":{"type":"integer","nullable":true},"entriesUsed":{"type":"integer"},"reentryAllowed":{"type":"boolean"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"delegatedRights":{"type":"array","description":"Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n","items":{"type":"object","required":["rightId","ticketId","issuingCellId","validFrom","validTo","entriesAllowed","entriesConsumed"],"properties":{"rightId":{"type":"string"},"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id` in the issuing cell."},"issuingCellId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"entriesAllowed":{"type":"integer","nullable":true},"entriesConsumed":{"type":"integer"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"blacklist":{"type":"array","items":{"type":"string"},"description":"Media codes to deny outright regardless of entitlement state."},"admissionRules":{"type":"array","items":{"type":"object","required":["id","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid"},"openMinutesBefore":{"type":"integer"},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean"}}}},"accreditationCredentials":{"type":"array","description":"Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.","items":{"$ref":"#/components/schemas/AccessAccreditationCredential"}}}},
"OfflineScan": {"x-ticvai-persistence":"none — client-side journal","allOf":[{"$ref":"#/components/schemas/ValidateRequest"},{"type":"object","required":["sequence","localOutcome"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. The server processes in this order."},"localOutcome":{"allOf":[{"$ref":"#/components/schemas/ScanOutcome"}],"description":"What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"},"localDenyReason":{"$ref":"#/components/schemas/DenyReason"},"overriddenByPrincipalId":{"type":"string","format":"uuid","nullable":true},"overrideReason":{"type":"string","nullable":true}}}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"ScanSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer","description":"Entries processed before any stop."},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string"},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","reconciled","rejected"]},"serverOutcome":{"$ref":"#/components/schemas/ScanOutcome"},"divergence":{"type":"string","nullable":true,"description":"Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SyncRejection": {"x-ticvai-persistence":"sync.rejection","type":"object","required":["id","workstationId","kind","rejectedAt","problem"],"properties":{"id":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","payment","refund","void","scan"]},"recordedAt":{"type":"string","format":"date-time"},"rejectedAt":{"type":"string","format":"date-time"},"problem":{"$ref":"../shared/common.yaml#/components/schemas/Problem"},"payload":{"type":"object","additionalProperties":true,"description":"**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolution":{"type":"string","nullable":true,"readOnly":true,"enum":["posted","voided","refunded"],"description":"What `resolveSyncRejection` recorded. Null while the rejection waits."},"resolvedRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order, void or refund the resolution produced — what stops the entry being posted twice."}}},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]},
"ValidateRequest": {"type":"object","required":["id","mediaCode","mediaKind","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key and dedupe key."},"mediaCode":{"type":"string","maxLength":256,"description":"What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"},"mediaKind":{"$ref":"#/components/schemas/MediaKind"},"direction":{"$ref":"#/components/schemas/Direction"},"groupSize":{"type":"integer","minimum":1,"description":"For group media admitting several holders on one read."},"proximityToken":{"type":"string","description":"BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"},"recordedAt":{"type":"string","format":"date-time","description":"Device time of the read. Authoritative for ordering, not for validity."}}},
"ValidationResult": {"x-ticvai-persistence":"none — computed, persisted as scan_event","type":"object","required":["scanId","outcome","accessPointId","recordedAt"],"properties":{"scanId":{"type":"string","format":"uuid"},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"denyDetail":{"type":"string","description":"Human-readable, localised. For operator display, never for logic."},"denyCause":{"type":"string","nullable":true,"enum":["attractionTemporarilyClosed","timeBoundWindowElapsed","offlineLimitExceeded"],"description":"**The finer cause of three denials decided on 2 October 2026**, beside the r1 `denyReason` a client already switches on (a new `DenyReason` value would be a breaking change against r1; CHG-CSP-026, CHG-CSP-030, CHG-CSP-035). `attractionTemporarilyClosed` (DEC-228): `denyReason` `outsideAdmissionWindow`, with `reopensAt` and `queueReturnOffer`. `timeBoundWindowElapsed` (DEC-232): a time-bound entitlement scanned after its window from first scan, `denyReason` `expired`. `offlineLimitExceeded` (DEC-426): a reader offline longer than the venue's `AccessOfflinePolicy.maxOfflineDurationHours` refusing a tap it cannot check, `denyReason` `outsideAdmissionWindow`. Null for every other denial."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When a temporarily closed attraction expects to reopen, where known (DEC-228; CHG-CSP-026)."},"queueReturnOffer":{"type":"object","nullable":true,"description":"A virtual-queue return window offered at a denied scan of a temporarily closed attraction, where the venue enables it (DEC-228; CHG-CSP-026). Taking it is `queue.joinQueue`.","properties":{"queueId":{"type":"string","format":"uuid"},"returnWindowStart":{"type":"string","format":"date-time"},"returnWindowEnd":{"type":"string","format":"date-time"}}},"accessPointId":{"type":"string","format":"uuid"},"ticket":{"$ref":"#/components/schemas/TicketStatus"},"admittedCount":{"type":"integer","description":"Holders admitted on this read. Differs from groupSize on partial admission."},"recordedAt":{"type":"string","format":"date-time"},"serverEvaluatedAt":{"type":"string","format":"date-time"},"advisory":{"type":"object","nullable":true,"description":"BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n","properties":{"genderClassification":{"type":"string","enum":["women","men","undetermined"],"description":"**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"},"confidence":{"type":"number","minimum":0,"maximum":1,"description":"**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"},"reportedByDeviceId":{"type":"string","format":"uuid","description":"**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"}}}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
