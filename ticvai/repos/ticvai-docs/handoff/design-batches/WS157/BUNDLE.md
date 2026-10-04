# WS157 — Resource Management Configuration board 3

**10 screens · 34 operations · 37 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `PRODUCT_VIEW, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW, USER_MANAGE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
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
| `BO-873` | Staff Resource Directory | D | 3 | 10 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-874` | Staff Resource Profile | D | 11 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-875` | Skills & Competency Management | D | 0 | 7 | 6 | 9 | 1 | 0 | — | notStarted (—) |
| `BO-876` | Certification & Expiry Management | D | 10 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-877` | Qualification & Assignment Rule Engine | A | 12 | 41 | 6 | 34 | 0 | 0 | — | notStarted (—) |
| `BO-878` | Staff Availability & Working Pattern | D | 21 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-879` | Shift Template & Assignment Configuration | D | 6 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-880` | Break, Leave & Absence Configuration | D | 9 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-881` | Overtime & Working-Hour Rules | D | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-882` | Workforce Integration & Synchronization Center | D | 0 | 16 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-875 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-873` Staff Resource Directory

**Provide the centralized master directory for all personnel who may be assigned as operational resources within TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-873 |
| Who uses it | venue staff holding `USER_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/staff-resource-directory-bo-873` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Everyone who can be assigned as an operational resource (staff with skills and availability). As wired it is the principal list again.

**Fixed on main** (the package already carries these; draw what it says): Same listPrincipals as BO-053. (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search staff resource | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, department, role, staff type, skill, certification and 4 more — which are present is a decision the pack already made. | — |
| Job title | picker: choose an id | optional | — | — | shows names, sends the id | The role filter: job titles by name. | `WorkforceJobTitle.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Scope path | text field | — | — | `listPrincipals` ?scopePath |
| Is active | toggle | — | — | `listPrincipals` ?isActive |
| Employee | picker: choose an employee | — | — | `listWorkAssignments` ?employeeId |
| Active on | date picker | — | — | `listWorkAssignments` ?activeOn |

#### Outputs: what the screen shows and produces

**Shown**

**Staff resources** (data table, from `listWorkAssignments`): The workforce postings (job title, venue) beside each person, so the directory is a resource view, not a second copy of the staff directory (BO-053).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Employee | the name it points at, never the id | — |
| Job title | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Effective from | 1 Oct 2026 | — |
| Effective to | 1 Oct 2026 | — |
| Is primary | yes / no (icon or chip) | — |
| Status | text | — |

**Data it reads**: `listPrincipals` (onLoad, The staff directory); `listWorkAssignments` (onLoad, Who is posted to which job title at which venue); `listJobTitles` (onLoad, Job titles, for the role filter)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-874` Staff Resource Profile: *Staff Resource Profile*; carries `employeeId`
- → `BO-875` Skills & Competency Management: *Skills & Competency Management*
- → `BO-876` Certification & Expiry Management: *Certification & Expiry Management*
- → `BO-877` Qualification & Assignment Rule Engine: *Qualification & Assignment Rule Engine*
- → `BO-878` Staff Availability & Working Pattern: *Staff Availability & Working Pattern*
- → `BO-879` Shift Template & Assignment Configuration: *Shift Template & Assignment Configuration*
- → `BO-880` Break, Leave & Absence Configuration: *Break, Leave & Absence Configuration*
- → `BO-881` Overtime & Working-Hour Rules: *Overtime & Working-Hour Rules*
- → `BO-882` Workforce Integration & Synchronization Center: *Workforce Integration & Synchronization Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff resource yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the staff resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listPrincipals (Principal):
- username: fatima.almansoori
  displayName: Fatima Al Mansoori
  isActive: true
  validFrom: 01/10/2026 09:14
  validTo: 31/12/2026 23:59
  lastLoginAt: 01/10/2026 09:14
- username: '10482'
  displayName: Rahul Menon
  isActive: true
  validFrom: 30/09/2026 18:02
  validTo: 15/10/2026 00:00
  lastLoginAt: 30/09/2026 18:02
```

#### Permissions

- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `listWorkAssignments` → `WORKFORCE_VIEW` (read) · staff
- `listJobTitles` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Personnel (cashiers, trainers, drivers, other staff) are a resource type; command-centre view shows total personnel and how many are on duty, available or on leave. A staff profile's operational summary lists associated bookings. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-485)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-873` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-873`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 1: Opens Staff Resource Directory → Provide the centralized master directory for all personnel who may be assigned as operational resources within TICVAI.
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F266 branch at step 1 (expected): when Nothing has been set up on Staff Resource Directory yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F266 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-873?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-874`, `BO-875`, `BO-876`, `BO-877`, `BO-878`, `BO-879`, `BO-880`, `BO-881`, `BO-882`.
- [ ] Every gated control is gated: `USER_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-874` Staff Resource Profile

**Maintain the operational resource profile for an individual employee or contractor. This profile shall complement the organization's HR employee record rather than unnecessarily duplicate an HR system.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-874 |
| Who uses it | venue staff holding `RESOURCE_VIEW`, `USER_MANAGE`, `WORKFORCE_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `principalId` (session), `employeeId` (BO-873) · cold entry: Opened from BO-873 with the employee picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says … |
| Route | `/rentals/staff-resource-profile-bo-874` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The operational profile of one staff resource (employee or contractor): who they are, as the HR system has them, plus what operations needs to schedule them - bookable, scheduling enabled, priority, maximum concurrent assignments, default assignment duration, preferred area, languages, tags - and a summary of availability, skills, certifications and upcoming assignments. The one thing to get right: fields the HR system masters are shown locked with their source, and only the operational fields are editable here.

**Known correction pending (do not draw the wrong version)**

- **Entry parameter principalId taken from the session** Why: The session principal is the viewer, not the employee being viewed; the profile must open on the employee chosen in BO-873. *(source: screens/P08-venue-back-office.yaml#BO-874; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"External agency", "External employee ID", "Source system", "Synchronization status", "Last synchronization" are drawn as action buttons** Why: External agency is a value of employment classification; the other four are read-only system-link fields. *(source: screens/P08-venue-back-office.yaml#BO-875; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Yes/no fields drawn as select fields and "Individual selection allowed yes/no" as a text field** Why: Closed two-value set; draw toggles. *(source: screens/P08-venue-back-office.yaml#BO-875; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No write is bound; getPrincipal needs USER_MANAGE (an identity administrator right)** Why: A workforce manager editing operational fields needs a write (updateResource on the staff resource, or a profile write) and should not need user-administration rights to read the profile. *(source: contracts/satellite/resources.yaml#updateResource / screens/P08-venue-back-office.yaml#BO-874; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where are the per-person operational fields stored (resource attributes on the staff resource, or the employee profile)?** → Drawn default accepted: Draw them as one "Operational information" section with Save; mark storage as pending. *(decided by Chinmay, 2026-10-02; DEC-493 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource priority | select field | — | — | — | — | — | — |
| Customer selectable yes/no | select field | — | — | — | — | — | — |
| Individual selection allowed yes/no | text field | — | — | — | — | — | — |
| Bookable yes/no | select field | — | — | — | — | — | — |
| Scheduling enabled yes/no | select field | — | — | — | — | — | — |
| Maximum concurrent assignment | select field | — | — | — | — | — | — |
| Default assignment duration | select field | — | — | — | — | — | — |
| Preferred operating area | select field | — | — | — | — | — | — |
| Languages | select field | — | — | — | — | — | — |
| Tags | select field | — | — | — | — | — | — |
| Employment Classification | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `listResources` ?kind |
| Available from | date and time picker | — | — | `listResources` ?availableFrom |
| Available to | date and time picker | — | — | `listResources` ?availableTo |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Identity block (employee number, name, photo, staff type, job title, department, employment type, primary and secondary …**: Read from the employee record; any field listed as externally mastered is read-only with a lock and "Managed in Oracle HCM". Status is a pill (Active, On leave, Suspended). *(source: screens/P08-venue-back-office.yaml#BO-874 / contracts/satellite/workforce.yaml#getEmployee / contracts/satellite/workforce.yaml#/components/schemas/WorkforceEmployeeProfile)*
- **Bookable, Scheduling enabled, Customer selectable, Individual selection allowed**: Toggles (yes/no), not selects or text. Customer selectable is available only when the resource type allows it; otherwise shown off and locked with "Not allowed for Staff resources". *(source: screens/P08-venue-back-office.yaml#BO-875 / contracts/satellite/resources.yaml#/components/schemas/ResourceType)*
- **Resource priority, Maximum concurrent assignments, Default assignment duration**: Priority as a number 1-10 (1 = first choice); concurrent assignments a whole number, default 1; duration in minutes with presets (30, 60, 90, 120). *(source: screens/P08-venue-back-office.yaml#BO-875 / designer default)*
- **Preferred operating area, Languages, Tags**: Area is a venue topology picker; languages a multi-select (Arabic, English, Hindi, Russian...); tags free chips. *(source: screens/P08-venue-back-office.yaml#BO-875)*
- **Employment classification**: Single choice Full-time / Part-time / Contractor / Temporary / Seasonal / External agency (from HR where mastered). *(source: screens/P08-venue-back-office.yaml#BO-875)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| External agency (primary button) | navigation or local | — | — | — | — |
| External employee ID (secondary button) | navigation or local | — | — | — | — |
| Source system (secondary button) | navigation or local | — | — | — | — |
| Synchronization status (secondary button) | navigation or local | — | — | — | — |
| Last synchronization (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Operational summary tiles**: Availability now, Skills (count), Certifications (valid / expiring), Upcoming assignments (next 3 with time and booking), Venue access, Current status. *(source: screens/P08-venue-back-office.yaml#BO-875 / screens/P08-venue-back-office.yaml#BO-874 / DI-485)*
- **System links**: Read-only panel: External employee ID, Source system, Synchronisation status, Last synchronisation, Record ownership. Status in words (Healthy, Expiring credentials, Failed) with a link to BO-882. *(source: screens/P08-venue-back-office.yaml#BO-875 / contracts/satellite/workforce.yaml#listIntegrationSources)*
- **Leave balances**: Per leave type, available of entitled days for the year ("Annual 18.5 of 30"). *(source: contracts/satellite/workforce.yaml#/components/schemas/WorkforceLeaveBalance)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save profile**: Saves the operational fields only (per VO-R04 the whole operational set is sent); identity fields are never sent. *(source: contracts/satellite/resources.yaml#updateResource)*
- **View calendar**: Opens the person's availability and assignment calendar (Day, Week, Month). *(source: screens/P08-venue-back-office.yaml#BO-874)*

**Data it reads**: `getPrincipal` (onLoad, One person); `listResources` (onLoad, Them as a bookable resource)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff resource profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff resource profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff resource profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Employee terminated in HR but with future assignments**: Red banner "Terminated in Oracle HCM on 30 Sep; 4 future assignments at risk" linking to the sync conflict. *(source: contracts/satellite/workforce.yaml#/components/schemas/WorkforceSyncConflict)*
- **Viewer without sensitive-data rights**: Date of birth, contact details and pay rate are hidden with "Restricted"; operational fields remain. *(source: screens/P08-venue-back-office.yaml#BO-882)*

#### Consistency with other screens

- Match `BO-873`: Opened from the directory row; back returns to the same filtered list.
- Match `BO-882`: Ownership locks and sync status come from the integration centre.
- Match `BO-055`: Upcoming assignments are rota assignments; same time and post format.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  name: Maria Santos
  employeeNo: EMP-10234
  staffType: Cashier
  department: Guest Services
  primaryVenue: Aqua Park
  secondaryVenues:
  - Summit Peaks
  manager: Fatima Al Hashimi
  classification: Full-time
  bookable: true
  priority: 3
  languages:
  - English
  - Tagalog
  - Arabic (basic)
  externalId: HCM-558120
  source: Oracle HCM - last synchronised 1 Oct 2026 06:00 - Healthy
```

#### Permissions

- `getPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `listResources` → `RESOURCE_VIEW` (read) · staff
- `getEmployee` → `WORKFORCE_VIEW` (read) · staff
- `listIntegrationSources` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Personnel (cashiers, trainers, drivers, other staff) are a resource type; command-centre view shows total personnel and how many are on duty, available or on leave. A staff profile's operational summary lists associated bookings. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-485)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-874` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-874`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 2: Works in Staff Resource Profile → Maintain the operational resource profile for an individual employee or contractor. This profile shall complement the organization's HR employee record rather than unnecessarily duplicate an HR …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-874?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: External agency, External employee ID, Source system, Synchronization status, Last synchronization.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`, `USER_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-875` Skills & Competency Management

**Define what each staff resource is capable of performing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-875 |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/skills-competency-management-bo-875` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The skill library (Ski instruction, Snowboarding, First aid, Lifeguarding, AV operation, Crowd management, Customer service, Languages) with proficiency levels, and each staff member's skills at a level, with review date and evidence. The assignment and recommendation engines read these. The one thing to get right: a skill is held at a level (Ski instruction - Level 3), and a person who fails a mandatory level is excluded from matching, not ranked lower.

**Known correction pending (do not draw the wrong version)**

- **No skill library operation and no proficiency level, assessor, evidence or verified status on a qualification** Why: Qualification holds code, name, issued, expiry, issuer and a document; the pack's library and employee skill fields cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-875 / contracts/satellite/resources.yaml#/components/schemas/Qualification; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The screen has only Save and Cancel, and the gap note says nothing is drawable** Why: The pack lists the library, ten skill settings, levels and eight employee fields. *(source: screens/P08-venue-back-office.yaml#BO-875; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Only setResourceQualifications is bound; no read of the person's current skills (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a skill level stored as a qualification code per level (SKI-L3) or as a level on one skill?** → Drawn default accepted: Draw one skill row with a level select; store as the code per level the Block A screen already uses (SKI-L3). *(decided by Chinmay, 2026-10-02; DEC-494 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Skill (library)**: Code, name (Arabic variant), skill category, description, level structure (Beginner / Intermediate / Advanced / Expert, or Level 1-4), applicable roles, venues and experiences, effective dates, active. Levels are an ordered list so "Level 3 or higher" works. *(source: screens/P08-venue-back-office.yaml#BO-875)*
- **Staff skill rows**: For the person opened from the staff directory - skill (from the library), proficiency level, effective date, expiry or review date (date pickers), assessor (staff picker), evidence (upload), notes, verified tick with who verified. The whole set saves at once. *(source: screens/P08-venue-back-office.yaml#BO-875 / contracts/satellite/resources.yaml#setResourceQualifications)*

#### Outputs: what the screen shows and produces

**Shown**

**Skills** (data table, from `getResourceQualifications`)

| Shows | Format | Notes |
|---|---|---|
| Resource | the name it points at, never the id | The resource that holds this qualification. Set from the path of `setResourceQualifications`; without it a stored qualification belongs to … |
| Code | text | — |
| Name | text | — |
| Issued at | 1 Oct 2026 | — |
| Expires at | 1 Oct 2026 | The field that makes this worth having. A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last … |
| Issuer | text | — |
| Document image | the image or video | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Skill library list**: Skill name, category, levels, active badge, number of staff holding it; search above. *(source: screens/P08-venue-back-office.yaml#BO-875)*
- **Staff skill table**: Skill, proficiency level, effective from, expiry/review (amber within 30 days, red past), verified; sorted by expiry. *(source: screens/P08-venue-back-office.yaml#BO-875 / contracts/satellite/resources.yaml#getResourceQualifications)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save skills**: Loads the person's current set first and replaces it whole (VO-R04); never a blind overwrite. *(source: contracts/satellite/resources.yaml#getResourceQualifications / contracts/satellite/resources.yaml#setResourceQualifications)*
- **New skill**: Adds a library entry (tenant configuration). *(source: screens/P08-venue-back-office.yaml#BO-875)*

**Data it reads**: `getResourceQualifications` (onLoad, The person's skills and certificates as saved)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The skills competency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the skills competency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No skills competency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the skills competency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Lowering a person's level below what their future bookings require**: Warn listing the bookings that will no longer be qualified (e.g. 3 Advanced private lessons) before saving. *(source: screens/P08-venue-back-office.yaml#BO-875 / DI-493)*
- **Retiring a skill still required by an experience**: Refuse with the experiences named. *(source: designer default)*

#### Consistency with other screens

- Match `BO-098`: The Block A qualifications screen shows the same records for one person; same columns and expiry colours.
- Match `BO-877`: Rule attributes (skill, level) are picked from this library.
- Match `BO-858`: Do not also model skill level as a free attribute; one source for "Ski instruction Level 3".

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
library:
- Ski instruction (Level 1-4)
- Snowboarding (Level 1-4)
- First aid (Valid/Expired)
- Lifeguarding
- AV operation (Level 1-3)
- Crowd management
- Customer service
person: Maria Santos
rows:
- skill: Ski instruction
  level: Level 3 - Advanced
  from: 10 Jan 2024
  review: 10 Jan 2027
  verified: Rahul Menon
- skill: Snowboarding
  level: Level 2 - Intermediate
  from: 10 Jan 2024
  review: 10 Jan 2027
- skill: Customer service
  level: Level 4 - Expert
  from: 1 Feb 2024
  review: 1 Feb 2027
```

#### Permissions

- `setResourceQualifications` → `RESOURCE_MANAGE` (configure) · staff
- `getResourceQualifications` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.3 | The system should allow management of the schedules of the staff resources with the possibility to set the parameters such as total hours, breaks, leave plan, absences. This data can be captured via … | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.4 | The system should allow linking of staff resources in different combinations and time-slot capacity with individual attraction experiences such as group lessons and private lessons. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.5 | The system should allow selection of specific instructors, staff skillset and/or specific timeslots for the staff offering experiences. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.12 | System should allow to assign the resources dynamically based on the resources availability and piority. The same functionality should be available over API / Online websites | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.34 | System shall maintain employee skill profiles. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.35 | System shall track certifications and expiry dates. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.36 | System shall validate qualifications before assignment. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 1.2.52 | System shall support priority-based allocation. | Ticketing Catalogue | CONTRACTED | data `Qualification` |
| 17.2.6 | Maintenance Resource Planning - System shall support maintenance resource planning. | Maintenance & Safety Management | CONTRACTED | data `Qualification` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Skills & competency define qualifications required for a role (e.g. level 1/2/3 ski-instructor certification for an advanced trainer); certification expiry tracking flags when recertification is due (e.g. annual renewal). *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-486)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-875` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-875`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 4: Works in Skills & Competency Management → Define what each staff resource is capable of performing.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-875?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-876` Certification & Expiry Management

**Manage certifications, licenses and credentials required for staff assignments.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-876 |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/certification-expiry-management-bo-876` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Certifications and licences required for assignments (First aid, Lifeguard, Instructor licence, Security licence, Child safeguarding), each person's certificates with numbers and expiry, staged expiry alerts (90, 60, 30, 14, 7 days, expired) and what expiry does to assignments. The one thing to get right: expiry and its consequence are the headline - a lapsed lifeguard certificate on today's rota is a safety failure shown at the top, not a row in a table.

**Known correction pending (do not draw the wrong version)**

- **The ten library settings are selectFields and there is no library operation** Why: Nothing stores certification definitions, validity, warning periods or renewal rules. *(source: screens/P08-venue-back-office.yaml#BO-876; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Certificate number, verification status, verified by and date have no field on a qualification** Why: The pack's employee certificate record cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-876 / contracts/satellite/resources.yaml#/components/schemas/Qualification; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation stores the expiry consequence** Why: Warn / prevent / cancel / override is required by the pack and decides what the assignment engine does. *(source: screens/P08-venue-back-office.yaml#BO-877; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Write bound without the read of current certificates** Why: Same blind-overwrite problem as BO-098; bind getResourceQualifications. *(source: contracts/satellite/resources.yaml#getResourceQualifications; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Certification code | select field | — | — | — | — | — | — |
| Certification name | select field | — | — | — | — | — | — |
| Issuing authority | select field | — | — | — | — | — | — |
| Applicable roles | select field | — | — | — | — | — | — |
| Applicable resource types | select field | — | — | — | — | — | — |
| Applicable venues | select field | — | — | — | — | — | — |
| Validity period | select field | — | — | — | — | — | — |
| Renewal requirements | select field | — | — | — | — | — | — |
| Mandatory/optional | select field | — | — | — | — | — | — |
| Warning period | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `validateWorkforceCompliance` ?from |
| To | date picker | — | — | `validateWorkforceCompliance` ?to |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Certification library**: Code, name, issuing authority, applicable roles, resource types and venues, validity period (months), renewal requirements, mandatory/optional, warning period (alert stages ticked from 90/60/30/14/7). *(source: screens/P08-venue-back-office.yaml#BO-876)*
- **Expiry consequence**: Per certification, one choice - Warn only / Prevent new assignments / Cancel future assignments / Require manager override. Default Prevent new assignments for mandatory safety certificates. *(source: screens/P08-venue-back-office.yaml#BO-877)*
- **Employee certificate**: Certification, certificate number, issue date and expiry date (pickers; expiry defaults to issue + validity), issuing authority, attachment, verification status, verified by and date. *(source: screens/P08-venue-back-office.yaml#BO-876 / contracts/satellite/resources.yaml#setResourceQualifications)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lapse banner**: Expired or missing qualifications of people rostered in the next 7 days, from the compliance check, each with the shift and a link to the rota. *(source: contracts/satellite/workforce.yaml#validateWorkforceCompliance)*
- **Person's certificates**: Certification, certificate no., expiry, status chip (Valid green, Expires in N days amber within the warning period, Expired red); sorted by expiry. *(source: screens/P08-venue-back-office.yaml#BO-876 / contracts/satellite/resources.yaml#getResourceQualifications)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save certificates**: Replaces the person's set after loading it (VO-R04). *(source: contracts/satellite/resources.yaml#setResourceQualifications)*
- **Add certification (library)**: Adds a library entry for the tenant. *(source: screens/P08-venue-back-office.yaml#BO-876)*

**Data it reads**: `validateWorkforceCompliance` (onLoad, What has lapsed)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The certification expiry configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the certification expiry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No certification expiry configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Certificate expires while the person has future assignments**: The consequence applies and is shown ("Prevent new assignments - 4 future lessons kept, flagged for review"). *(source: screens/P08-venue-back-office.yaml#BO-877)*
- **Certificate with no expiry date**: Allowed only for certifications whose validity is "No expiry"; otherwise expiry is required. *(source: contracts/satellite/resources.yaml#/components/schemas/Qualification)*

#### Consistency with other screens

- Match `BO-098`: Same records and status colours as the Block A qualifications screen.
- Match `BO-877`: The expiry consequence is set here per the pack's screen 04; the lead's rule engine (BO-877) also lists it - keep one control and show it read-only on the other.
- Match `EMP-003`: The employee sees "Your certification expires in 14 days" on the Staff App home.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
library:
- code: FA-1
  name: First aid
  authority: Red Crescent
  validity: 24 months
  warning: 60, 30, 7 days
  onExpiry: Prevent new assignments
- code: LG-1
  name: Lifeguard certification
  authority: RLSS
  validity: 12 months
  onExpiry: Cancel future assignments
person: Maria Santos
certificates:
- cert: Ski instructor level 3
  number: PSIA-3456
  expires: 11 Jan 2027
  status: Valid
- cert: First aid
  number: FA-9876
  expires: 2 Nov 2026
  status: Expires in 32 days
- cert: Avalanche safety
  number: AS-5566
  expires: 10 Apr 2026
  status: Expired
```

#### Permissions

- `setResourceQualifications` → `RESOURCE_MANAGE` (configure) · staff
- `validateWorkforceCompliance` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Skills & competency define qualifications required for a role (e.g. level 1/2/3 ski-instructor certification for an advanced trainer); certification expiry tracking flags when recertification is due (e.g. annual renewal). *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-486)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-876` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-876`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 6: Works in Certification & Expiry Management → Manage certifications, licenses and credentials required for staff assignments.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-876?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-877` Qualification & Assignment Rule Engine

**Convert skills, certifications and operational policies into machine-enforceable assignment rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 1 · needs the `resources` module |
| Block | Block A · task APP-SETUP-BO-877 |
| Who uses it | venue staff holding `PRODUCT_VIEW`, `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `resourceId` (navigation), `experienceId` (navigation) · cold entry: Opened from BO-873 with the experience picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and … |
| Route | `/rentals/qualification-assignment-rule-engine-bo-877` |

**What the spec says about it.** **The experience is picked on the screen 4 October 2026 (listProducts; experienceId is the product's id), so a cold entry has a list to pick from** (CHG-FXS-003) **The generator's 'needs a person' gap removed 4 October 2026: the screen's content is defined (tables, panels and actions bound to its operations)** (CHG-FXS-005)

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Recording a person's qualifications is BO-098 and BO-876; this screen defines requirements (design-notes correction venue-operations BO-877).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Turns skills and certifications into enforceable assignment rules for experiences: requirements built from role, skill and level, certification, language, venue, department, attraction, event type, resource type and working status, combined with AND/OR/NOT and marked minimum, preferred or mandatory; a live "who qualifies" list tests the rule. Matching is attribute/keyword based, not AI. The one thing to get right: mandatory rules block assignment, preferred ones only rank.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No operation stores the expiry behaviour (warn, prevent, cancel, override) (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Minimum / Preferred / Mandatory drawn as three action buttons; empty content region (CHG-SBO-009); setResourceQualifications (a person's certificates) bound on a rule screen (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Experience | picker: choose an id | optional | — | — | shows names, sends the id | Opened without experienceId, the user picks one here. | `Product.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Resource type | picker: choose a resource type | — | — | `suggestResources` ?resourceTypeId |
| From | date and time picker | — | — | `suggestResources` ?from |
| To | date and time picker | — | — | `suggestResources` ?to |
| Attributes | text field | — | — | `suggestResources` ?attributes |
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `listResources` ?kind |
| Available from | date and time picker | — | — | `listResources` ?availableFrom |
| Available to | date and time picker | — | — | `listResources` ?availableTo |
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Form: Save requirements** (modal, opened by *Save requirements*; *Save requirements* calls `setExperienceResourceRequirements`, *Cancel* sends nothing)

**Collects what `setExperienceResourceRequirements` sends before it is called.** Required: `requirements`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Requirements `requirements` | repeatable rows | required | — | — | — | — | `setExperienceResourceRequirements` body |
| ID `requirements[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `setExperienceResourceRequirements` body |
| Resource type `requirements[].resourceTypeId` | picker: choose a resource type | optional | — | — | shows names, sends the id | — | `setExperienceResourceRequirements` body |
| Category `requirements[].categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `setExperienceResourceRequirements` body |
| Resource `requirements[].resourceId` | picker: choose a resource | optional | — | — | shows names, sends the id | A fixed component, and the exception rather than the rule. Meeting Room A really is Meeting Room A; the technician is not. | `setExperienceResourceRequirements` body |
| Quantity `requirements[].quantity` | number field | required | 1 | — | — | — | `setExperienceResourceRequirements` body |
| Mandatory `requirements[].mandatory` | toggle | optional | on | — | — | — | `setExperienceResourceRequirements` body |
| Required qualifications `requirements[].requiredQualifications` | list of values (chips) | optional | — | — | — | — | `setExperienceResourceRequirements` body |
| Required attributes `requirements[].requiredAttributes` | key and value settings | optional | — | — | — | — | `setExperienceResourceRequirements` body |
| Substitute resources `requirements[].substituteResourceIds` | multi-picker: choose substitute resources | optional | — | — | — | — | `setExperienceResourceRequirements` body |
| Scope path `requirements[].scopePath` | text field | optional | — | — | — | — | `setExperienceResourceRequirements` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Requirement rows**: Attribute (from the pack list), operator, value (e.g. Ski level >= 3, Language = English), and a strength tag Minimum / Preferred / Mandatory. *(source: screens/P08-venue-back-office.yaml#BO-877 / contracts/satellite/resources.yaml#setExperienceResourceRequirements)*
- **Logic**: AND/OR/NOT grouping as in the access rule builder. *(source: screens/P08-venue-back-office.yaml#BO-877)*
- **Expiry behaviour**: When a certification expires - Warn only / Prevent new assignments / Cancel future assignments / Require manager override. *(source: screens/P08-venue-back-office.yaml#BO-877)*

#### Outputs: what the screen shows and produces

**Shown**

**List the resources the assignment rules choose from** (card list, from `listResources`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Setup minutes | 1,234 | Before the booking, not inside it. An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that … |
| Teardown minutes | 1,234 | After the booking. Kept as it is (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added … |
| Deposit amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Status | chip: Available, Booked, Checked out, Maintenance, Retired | — |

**Load the experience's resource requirements** (card list, from `getExperienceResourceRequirements`)

| Shows | Format | Notes |
|---|---|---|
| Quantity | 1,234 | — |
| Mandatory | yes / no (icon or chip) | — |
| Required qualifications | list or chips (count when long) | — |
| Required attributes | grouped details | — |

**Requirement rules** (data table, from `setExperienceResourceRequirements`): The editable rule grid: one row per requirement with its strength (minimum, preferred or mandatory) and quantity; the board drew the strengths as buttons. The current mapping of the experience is opened from BO-894.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Resource type | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Resource | the name it points at, never the id | A fixed component, and the exception rather than the rule. Meeting Room A really is Meeting Room A; the technician is not. |
| Quantity | 1,234 | — |
| Mandatory | yes / no (icon or chip) | — |
| Required qualifications | list or chips (count when long) | — |
| Required attributes | grouped details | — |
| Substitute resources | list or chips (count when long) | — |
| Package | the name it points at, never the id | The package this requirement is a component of (4 October 2026, CHG-FXC-003). Written by `updateResourcePackage`, which replaces the … |
| Product | the name it points at, never the id | The experience product this requirement belongs to (`setExperienceResourceRequirements`). |

**Who qualifies** (data table, from `suggestResources`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Kind | chip: Cabana, Lounger, Locker, Wheelchair, Stroller, Equipment… | BL-135. `locker` was an entitlement kind in `orders` and nothing issued, assigned or released one. |
| Venue | the name it points at, never the id | — |
| Parent resource | the name it points at, never the id | A pool cabana belongs to the pool area; a seat belongs to an auditorium. Booking a parent takes its children with it, which is the … |
| Principal | the name it points at, never the id | For a resource of kind `instructor` or `staff`. `workforce` still owns their rota — this says whether they are qualified and whether they … |
| Attributes | grouped details | Configurable per kind — capacity, size, shade, power, poolside. |
| Setup minutes | 1,234 | Before the booking, not inside it. An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that … |
| Teardown minutes | 1,234 | After the booking. Kept as it is (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added … |
| Cleaning policy | grouped details | How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`. |
| Mode | chip: After every booking, Times per day | — |
| Buffer minutes | 1,234 | Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct). |
| Cleanings per day | 1,234 | Required for `timesPerDay`; ignored for `afterEveryBooking`. |
| Window start | text | Venue-local time the cleaning window opens. Null means the resource's opening time. |
| Window end | text | Venue-local time the cleaning window closes. Null means the resource's closing time. |
| Requires qualification | list or chips (count when long) | Qualification codes a person must hold to be assigned to this. |
| Deposit amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Status | chip: Available, Booked, Checked out, Maintenance, Retired | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save requirements (primary button) | `setExperienceResourceRequirements` PUT `/experiences/{experienceId}/resource-requirements` | inline | ResourceRequirement[] | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Who qualifies**: Ranked list of matching staff for a chosen window with the attributes that matched; missing mandatory items named. *(source: contracts/satellite/resources.yaml#suggestResources / DI-495)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save requirements**: Binds the requirements to the experience; assignment of an unqualified person is then refused for mandatory rules. *(source: contracts/satellite/resources.yaml#setExperienceResourceRequirements / DI-493)*

**Data it reads**: `suggestResources` (onLoad, Who qualifies); `getExperienceResourceRequirements` (onLoad, Load the experience's resource requirements); `listResources` (onLoad, List the resources the assignment rules choose from); `listProducts` (onLoad, The experiences to pick from: experienceId is the catalogue …)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The qualification rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the qualification rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No qualification rule yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the qualification rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `RESOURCE_VIEW`, which `getExperienceResourceRequirements` requires to show this screen, and names that permission (the screen's other reads need `PRODUCT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `RESOURCE_CONFIGURE` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 … |

#### Consistency with other screens

- Match `BO-155`: Use the same AND/OR/NOT builder component as the access rule builder.
- Match `BO-894`: The combination builder references these requirements.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  experience: Advanced Private Ski Lesson
  requirements: Ski instructor level >= 3 (Mandatory) AND First aid valid (Mandatory) AND Language = English or
    Arabic (Preferred)
  qualifies: Maria Santos, Ahmed Al Mansoori
```

#### Permissions

- `suggestResources` → `RESOURCE_VIEW` (read) · staff
- `setExperienceResourceRequirements` → `RESOURCE_CONFIGURE` (configure) · staff
- `getExperienceResourceRequirements` → `RESOURCE_VIEW` (read) · staff
- `listResources` → `RESOURCE_VIEW` (read) · staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner

**A refused user sees:** Shown when the caller lacks `RESOURCE_VIEW`, which `getExperienceResourceRequirements` requires to show this screen, and names that permission (the screen's other reads need `PRODUCT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `RESOURCE_CONFIGURE` for …

#### Requirements it meets

34 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.53 | AI shall recommend optimal resources. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.54 | AI shall recommend suitable staff based on skills and availability. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.56 | AI shall propose alternatives for scheduling conflicts. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.5 | System shall support pricing calendar management. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.6 | System shall support automatic activation of future pricing. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 22 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-877` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-877`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 8: Works in Qualification & Assignment Rule Engine → Convert skills, certifications and operational policies into machine-enforceable assignment rules.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-877?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save requirements.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`, `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-878` Staff Availability & Working Pattern

**Define when an individual staff resource is normally available to work.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-878 |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (2 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Users shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation), `sourceId` (navigation) |
| Route | `/rentals/staff-availability-working-pattern-bo-878` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** When an individual staff resource normally works - one or more working patterns (Peak season Mon-Fri 08:00-18:00, Off season Mon-Thu 09:00-16:00), availability type, and dated overrides - with a live calendar preview of available, working, leave, break and existing assignments. It feeds the resource calendar and the assignment engine. The one thing to get right: show whether the pattern is mastered here or by the external HR system, and lock it when it is external.

**Known correction pending (do not draw the wrong version)**

- **Time zone is a field** Why: The region owns the time zone (ADR-0011); a person cannot have their own. *(source: ADR-0011; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The preview's legend values (Available, Working, Unavailable, Leave, Break, Existing assignment) and the headings are selectFields, and "External schedule" is the primary button** Why: They are legend colours and options; the primary action is Save pattern. *(source: screens/P08-venue-back-office.yaml#BO-878; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The screen places things in time but has no calendar component** Why: The pack asks for a live calendar preview (VO-R01). *(source: screens/P08-venue-back-office.yaml#BO-879; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Availability type, named patterns and override kinds have no field** Why: ResourceSchedule has one mode (always, scheduled, on request), windows and dated exceptions only. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceSchedule; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which record is the master of a staff member's availability - the resource schedule here or workforce shift patterns?** → Drawn default accepted: Draw this screen as the master of availability and show assigned shifts from workforce read-only on the preview. *(decided by Chinmay, 2026-10-02; DEC-495 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Working days | select field | — | — | — | — | — | — |
| Start time | select field | — | — | — | — | — | — |
| End time | select field | — | — | — | — | — | — |
| Time zone | select field | — | — | — | — | — | — |
| Effective period | select field | — | — | — | — | — | — |
| Weekly hours | select field | — | — | — | — | — | — |
| Availability type | select field | — | — | — | — | — | — |
| Seasonal pattern | select field | — | — | — | — | — | — |
| Availability Types | select field | — | — | — | — | — | — |
| Additional availability | select field | — | — | — | — | — | — |
| Temporary unavailability | select field | — | — | — | — | — | — |
| Special working day | select field | — | — | — | — | — | — |
| Venue reassignment | select field | — | — | — | — | — | — |
| Restricted hours | select field | — | — | — | — | — | — |
| Calendar Preview | select field | — | — | — | — | — | — |
| Available | select field | — | — | — | — | — | — |
| Working | select field | — | — | — | — | — | — |
| Unavailable | select field | — | — | — | — | — | — |
| Leave | select field | — | — | — | — | — | — |
| Break | select field | — | — | — | — | — | — |
| Existing assignment | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Working patterns**: One or more named patterns, each a week grid of on/off days with start-end times and an effective period; weekly hours computed and shown, not typed. Patterns may not overlap in dates. *(source: screens/P08-venue-back-office.yaml#BO-878 / screens/P08-venue-back-office.yaml#BO-879 / contracts/satellite/resources.yaml#/components/schemas/ResourceSchedule)*
- **Availability type**: One choice - Regular, Flexible, Seasonal, On-call, Temporary, External schedule. *(source: screens/P08-venue-back-office.yaml#BO-879)*
- **Overrides**: Dated entries of kind Additional availability, Temporary unavailability, Special working day, Venue reassignment, Restricted hours, each with date(s) and times; shown on the preview. *(source: screens/P08-venue-back-office.yaml#BO-879 / contracts/satellite/resources.yaml#setResourceSchedule)*
- **Time zone**: Not a field; the venue's region time zone is shown read-only. *(source: ADR-0011)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| External schedule (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Calendar preview**: Day / Week / Month preview (VO-R01) with Available, Working, Unavailable, Leave, Break and Existing assignment as legend colours, not as fields. *(source: screens/P08-venue-back-office.yaml#BO-879)*
- **Source badge**: "Managed here" or "Managed in Oracle HCM - last synced 10:42"; when external, pattern fields are read-only with the reason. *(source: contracts/satellite/workforce.yaml#setFieldOwnership / contracts/satellite/workforce.yaml#listIntegrationSources)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save pattern**: Loads and sends the whole schedule (VO-R04); refuses overlapping patterns. *(source: contracts/satellite/resources.yaml#getResourceSchedule / contracts/satellite/resources.yaml#setResourceSchedule)*
- **Use external schedule**: Marks the pattern as mastered by the selected integration source (workforce administrators only, VO-R08). *(source: contracts/satellite/workforce.yaml#setFieldOwnership)*

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff availability working configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff availability working untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff availability working configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **New pattern removes hours that already have assignments**: Warn listing the assignments that fall outside the new pattern. *(source: designer default)*
- **Integration source failing**: Banner "Oracle HCM last synced 2 days ago - availability may be out of date". *(source: contracts/satellite/workforce.yaml#listIntegrationSources)*

#### Consistency with other screens

- Match `BO-866`: Same schedule record and week-grid component as the resource availability schedule.
- Match `BO-879`: Shift templates (workforce) define shifts; this is the person's availability. The rota is workforce's.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
person: Maria Santos
patterns:
- name: Peak season
  days: Sun-Thu
  time: 08:00-18:00
  effective: 1 Oct 2026 - 30 Apr 2027
  weeklyHours: 50
- name: Off season
  days: Sun-Wed
  time: 09:00-16:00
  effective: 1 May 2027 - 30 Sep 2027
  weeklyHours: 28
overrides:
- Temporary unavailability 20-22 Oct 2026 (training course)
- Special working day Sat 5 Dec 2026 08:00-14:00
```

#### Permissions

- `getResourceSchedule` → `RESOURCE_VIEW` (read) · staff
- `setResourceSchedule` → `RESOURCE_CONFIGURE` (configure) · staff
- `setFieldOwnership` → `WORKFORCE_MANAGE` (configure) · staff
- `listIntegrationSources` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.59 | Users shall manage resources through conversational AI commands. | Ticketing Catalogue | CONTRACTED | `setResourceSchedule` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-878` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-878`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 10: Works in Staff Availability & Working Pattern → Define when an individual staff resource is normally available to work.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-878?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: External schedule.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-879` Shift Template & Assignment Configuration

**Configure reusable workforce shift structures that can later be used by the operational roster engine.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-879 |
| Who uses it | venue staff holding `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/shift-template-assignment-configuration-bo-879` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Shift template and assignment-rule configuration: the reusable shifts a rota is built from (Morning 08:00-16:00, Evening 16:00-00:00, Event 14:00-23:00, Split 08:00-12:00 / 16:00-20:00) with their breaks, roles, qualifications and rate, and the assignment controls that limit how they are used. It configures; it does not build the roster (board 4 does). The one thing to get right: each template shows how it will appear on the calendar, including breaks and splits, before it is saved.

**Known correction pending (do not draw the wrong version)**

- **Two models for the same thing - shift templates (ShiftTemplate) and shift patterns (WorkforceShift with crossesMidnight)** Why: Both are named shift definitions on the same screen; per VO-R14 keep one editor, and the template already knows when it crosses midnight. *(source: contracts/satellite/workforce.yaml#listShiftTemplates / contracts/satellite/workforce.yaml#listShiftPatterns; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **WorkforceShift startTime and endTime have maxLength 0, and tenantId and createdAt are required request fields** Why: A time cannot be stored in a zero-length string; tenant and creation time are server-owned (VO-R03). *(source: contracts/satellite/workforce.yaml#/components/schemas/WorkforceShift; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **ShiftTemplate has one start and end, one roleCode, and no venue, department, effective dates, overtime eligibility or minimum rest** Why: The pack's split shift needs two parts and "Applicable roles" is plural; the other fields are listed on the pack page. *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#/components/schemas/ShiftTemplate; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Assignment controls (maximum shifts per day, allowed roles, venue restrictions, skill requirements) are drawn but bound to nothing** Why: No field holds them; maximum consecutive days and minimum rest exist only venue-wide in StaffingRules. *(source: contracts/satellite/workforce.yaml#/components/schemas/StaffingRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are assignment controls per template, or only venue-wide (BO-881)?** → Drawn default accepted: Show them per template, greyed except where they equal the venue rule. *(decided by Chinmay, 2026-10-02; DEC-496 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum shifts per day | text field | — | — | — | — | — | — |
| Maximum consecutive days | select field | — | — | — | — | — | — |
| Minimum rest between shifts | text field | — | — | — | — | — | — |
| Allowed roles | select field | — | — | — | — | — | — |
| Venue restrictions | select field | — | — | — | — | — | — |
| Skill requirements | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Code and name**: Code short and unique per venue (e.g. MOR-001), upper case; name in English and Arabic. *(source: contracts/satellite/workforce.yaml#/components/schemas/ShiftTemplate)*
- **Kind**: Early, Late, Middle, Split, Double, Night, On call, Overtime as chips; Split reveals a second start-end pair. *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#/components/schemas/ShiftTemplate)*
- **Start, end, duration**: Time pickers in venue time; duration computed and shown ("8 h, 7 h 30 paid"); an end before start is a next-day end shown "+1". *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#listShiftPatterns)*
- **Breaks**: Rows of "after [4] h, [30] min, paid / unpaid"; add row; total break shown. *(source: contracts/satellite/workforce.yaml#/components/schemas/ShiftTemplate)*
- **Applicable roles, required qualifications, cost centre, hourly rate**: Roles and qualifications as multi-select pickers from the skills and certification libraries; rate in AED with two decimals. *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#/components/schemas/ShiftTemplate)*
- **Venue, department, overtime eligibility, minimum rest, effective dates**: Shown as the pack lists them; greyed with "Not stored yet" where the template has no field. *(source: screens/P08-venue-back-office.yaml#BO-880)*
- **Assignment controls**: Maximum shifts per day, maximum consecutive days, minimum rest between shifts (hours), allowed roles, venue restrictions, skill requirements; whole numbers, with the venue-wide limit from BO-881 shown as the ceiling ("Venue limit 6 days"). *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#/components/schemas/StaffingRules)*
- **id, scopePath**: Never inputs (per VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Template list**: Name, code, time ("08:00-16:00"), duration, breaks ("1 x 30 min unpaid"), roles, rate; split shifts show both parts. *(source: screens/P08-venue-back-office.yaml#BO-879 / contracts/satellite/workforce.yaml#listShiftTemplates)*
- **Calendar preview**: The template as a bar on a one-day calendar with its break blocks, as it will appear on the rota. *(source: screens/P08-venue-back-office.yaml#BO-880)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New template / Save template**: Saves the whole template (PUT replaces, per VO-R04); existing rota assignments are not changed, and the confirm says so. *(source: contracts/satellite/workforce.yaml#setShiftTemplate)*

**Data it reads**: `listShiftTemplates` (onLoad, Shift templates); `listShiftPatterns` (onLoad, Shift patterns)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift template configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shift template configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Breaks longer than the shift or after its end**: Refused against the field ("Break after 9 h is past the 8 h shift"). *(source: designer default)*
- **Template in use by published assignments**: Editable; confirm "Used by 42 assignments next week; they keep their current times." *(source: contracts/satellite/workforce.yaml#setShiftTemplate)*

#### Consistency with other screens

- Match `BO-881`: Rest, consecutive days and overtime limits are venue rules there; the template's controls cannot exceed them.
- Match `BO-880`: Break policy vocabulary (paid, unpaid, after N hours) is the same.
- Match `BO-055`: The rota's "Add shift" picks these templates.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
templates:
- code: MOR-001
  name: Morning Shift
  time: 08:00-16:00
  breaks: 30 min unpaid after 4 h
  roles: Instructor, Lifeguard, CS Staff
  rate: AED 45.00/h
- code: EVE-001
  name: Evening Shift
  time: 16:00-00:00 +1
  breaks: 30 min unpaid after 4 h
- code: EVT-001
  name: Event Shift
  time: 14:00-23:00
  breaks: 2 x 30 min
- code: SPL-001
  name: Split Shift
  time: 08:00-12:00 / 16:00-20:00
  breaks: none
```

#### Permissions

- `listShiftTemplates` → `WORKFORCE_VIEW` (read) · staff
- `setShiftTemplate` → `WORKFORCE_MANAGE` (configure) · staff
- `listShiftPatterns` → `WORKFORCE_VIEW` (read) · staff
- `setShiftPattern` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-879` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-879`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 12: Works in Shift Template & Assignment Configuration → Configure reusable workforce shift structures that can later be used by the operational roster engine.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-879?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-880` Break, Leave & Absence Configuration

**Ensure employee availability reflects breaks, approved leave, absences and other workforce exceptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-880 |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/break-leave-absence-configuration-bo-880` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Break, leave and absence configuration: the break policies shifts follow, the leave types staff can request (with paid/unpaid, approval and quotas), and the absence types that make a person unavailable - so availability reflects them and scheduling cannot ignore them without an authorised override. The one thing to get right: approving leave or recording an absence shows at once which assignments it affects ("3 assignments affected by Maria's absence").

**Known correction pending (do not draw the wrong version)**

- **LeaveRequest.kind is a fixed enum (annual, sick, unpaid, parental, compassionate, training, timeOffInLieu) while leave types are configurable** Why: A configured type such as Emergency or Personal leave can never be requested; the request should reference a leave type id. *(source: contracts/satellite/workforce.yaml#/components/schemas/LeaveRequest / contracts/satellite/workforce.yaml#/components/schemas/WorkforceLeaveType; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listLeaveTypes says "how each accrues" but the type has no accrual, quota, maximum days or carry-forward field** Why: The client render shows Max days per year and Carry forward; quotas are named in DI-487. *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#listLeaveTypes / DI-487; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation stores a break policy; break fields are drawn as select fields bound to nothing** Why: Only ShiftTemplate.breaks (after, minutes, paid) exists; type, mandatory, earliest, latest and count have no home. *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#/components/schemas/ShiftTemplate; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Administrative block" is drawn as an action button, and ResourceBlock.reason has no administrative or absence value** Why: It is an absence reason; blocks today allow setup, teardown, maintenance, blackout, closed, operational, training. *(source: contracts/satellite/resources.yaml#createResourceBlock; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is approving leave done here, in the approvals inbox, or both?** → Drawn default accepted: Approve and Reject on each request row, routed through approvals. *(decided by Chinmay, 2026-10-02; DEC-497 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Break type | select field | — | — | — | — | — | — |
| Minimum shift duration | select field | — | — | — | — | — | — |
| Break duration | select field | — | — | — | — | — | — |
| Paid/unpaid | select field | — | — | — | — | — | — |
| Mandatory/optional | select field | — | — | — | — | — | — |
| Earliest break | select field | — | — | — | — | — | — |
| Latest break | select field | — | — | — | — | — | — |
| Number of breaks | select field | — | — | — | — | — | — |
| Leave Types | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listLeaveRequests` ?status |
| Employee | picker: choose an employee | — | — | `listLeaveBalances` ?employeeId |
| Leave type | picker: choose a leave type | — | — | `listLeaveBalances` ?leaveTypeId |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Break policy**: Break type (meal, rest, prayer), minimum shift duration that earns it (hours), duration (minutes), paid / unpaid, mandatory / optional, earliest and latest break (hours after shift start), number of breaks. Numbers and toggles, not select fields. *(source: screens/P08-venue-back-office.yaml#BO-880)*
- **Leave type**: Code, name (English and Arabic), paid / unpaid, requires approval, active; plus maximum days per year and carry forward as the client render shows. Seeded with Annual, Sick, Emergency, Unpaid, Training, Personal. *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#setLeaveType)*
- **Leave entry (manual, on behalf)**: Person, leave type, from, to, half day, reason; the coverage impact appears before Submit. *(source: contracts/satellite/workforce.yaml#requestLeave)*
- **Absence / administrative block**: Person, from-to date-time, reason (Planned absence, Unplanned absence, Sick, No-show, Training, Administrative block), note. *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/resources.yaml#createResourceBlock)*
- **id, tenantId, createdAt, scopePath**: Never inputs (per VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Administrative block (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Tabs**: Break policies / Leave types / Absence types / Leave requests, as in the client render. *(source: screens/P08-venue-back-office.yaml#BO-880)*
- **Leave requests list**: Person, type, dates, days, status (Requested, Approved, Rejected, Cancelled, Taken), and coverage impact ("Gate stewards short by 1 on Sat"). *(source: contracts/satellite/workforce.yaml#listLeaveRequests)*
- **Balances**: Entitled, used, pending, available days per person and type for the year. *(source: contracts/satellite/workforce.yaml#listLeaveBalances)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save leave type**: Saves the whole type (PUT, per VO-R04); deactivating a type keeps existing requests. *(source: contracts/satellite/workforce.yaml#setLeaveType)*
- **Submit leave (on behalf)**: Returns the request with its coverage impact; the approval routes through approvals. *(source: contracts/satellite/workforce.yaml#requestLeave)*
- **Add absence block**: The person becomes unavailable for the window; the confirm names affected assignments and offers "Find replacements". *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/resources.yaml#createResourceBlock)*

**Data it reads**: `listLeaveRequests` (onLoad, Leave and absence); `listLeaveTypes` (onLoad, Leave types); `listLeaveBalances` (onLoad, Leave balances)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The break leave absence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the break leave absence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No break leave absence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Bookings already exist in the window. They are listed, because blocking over a booked resource is sometimes right and must never be silent. (ResourceConflictProblem) |

#### Edge cases to draw

- **Leave beyond the available balance**: Warned with the balance ("Available 2 days, requested 5"); submit allowed only as unpaid or with override, per policy. *(source: contracts/satellite/workforce.yaml#listLeaveBalances)*
- **Leave imported from HR**: Shown with "From Oracle HCM", read-only here. *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#getFieldOwnership)*

#### Consistency with other screens

- Match `EMP-025`: Break policy text on the phone comes from here.
- Match `BO-879`: Template breaks use the same fields.
- Match `BO-883`: On-leave count on the command centre comes from approved leave here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
breakPolicies:
- type: Meal
  earnedAfter: 6 h
  duration: 30 min
  paid: false
  mandatory: true
  window: between 3 h and 5 h after start
leaveTypes:
- name: Annual leave
  paid: true
  approval: true
  maxDays: 30
  carryForward: true
- name: Sick leave
  paid: true
  approval: false
  maxDays: 14
- name: Emergency leave
  paid: true
  approval: true
  maxDays: 5
- name: Unpaid leave
  paid: false
  approval: true
  maxDays: 60
request:
  person: Maria Santos
  type: Annual leave
  dates: 18-22 Oct 2026
  impact: Cashiers short by 1 on Tue 20 Oct 09:00-17:00
  status: Requested
```

#### Permissions

- `listLeaveRequests` → `WORKFORCE_VIEW` (read) · staff
- `requestLeave` → `WORKFORCE_VIEW` (read) · staff
- `listLeaveTypes` → `WORKFORCE_VIEW` (read) · staff
- `setLeaveType` → `WORKFORCE_MANAGE` (configure) · staff
- `listLeaveBalances` → `WORKFORCE_VIEW` (read) · staff
- `createResourceBlock` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-880` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-880`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 14: Works in Break, Leave & Absence Configuration → Ensure employee availability reflects breaks, approved leave, absences and other workforce exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-880?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Administrative block.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-881` Overtime & Working-Hour Rules

**Configure workforce rules controlling employee working hours and overtime eligibility before operational rostering occurs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-881 |
| Who uses it | venue staff holding `WORKFORCE_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/overtime-working-hour-rules-bo-881` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of staffing rules (no getStaffingRules); affects BO-881 and BO-885.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Overtime and working-hour rules for the venue: standard and maximum hours per day and week, minimum rest, maximum consecutive days, and whether overtime is allowed, prohibited or needs approval - checked automatically before any assignment is confirmed. The one thing to get right: these rules share one record with minimum staffing (BO-885), so the editor must load and send the whole record, or saving overtime wipes the venue's minimum cover.

**Known correction pending (do not draw the wrong version)**

- **setStaffingRules is a write with no read (there is no getStaffingRules)** Why: The editor cannot open pre-filled, and because the PUT replaces the whole record (including every minimumCover row, "a position left out no longer has a minimum"), saving overtime here would erase BO-885's minimum cover. *(source: contracts/satellite/workforce.yaml#setStaffingRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Standard daily and weekly hours, maximum overtime, daily overtime threshold, and role or employee-group rules have no field** Why: The pack lists them; StaffingRules holds maximums, rest, consecutive days and a weekly overtime threshold only. *(source: screens/P08-venue-back-office.yaml#BO-881 / contracts/satellite/workforce.yaml#/components/schemas/StaffingRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Approval required" drawn as a primary button; the hour fields as select fields** Why: Approval is one of three overtime choices; hours are numbers. *(source: screens/P08-venue-back-office.yaml#BO-881; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should working-hour rules vary by role or employee group (e.g. lifeguards 10 h max)?** → Drawn default accepted: Venue-wide only; role overrides drawn greyed. *(decided by Chinmay, 2026-10-02; DEC-498 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Standard daily hours | select field | — | — | — | — | — | — |
| Standard weekly hours | select field | — | — | — | — | — | — |
| Maximum daily hours | select field | — | — | — | — | — | — |
| Maximum weekly hours | select field | — | — | — | — | — | — |
| Minimum rest period | select field | — | — | — | — | — | — |
| Maximum consecutive working days | text field | — | — | — | — | — | — |
| Overtime threshold | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Working hours**: Standard daily hours, standard weekly hours, maximum daily hours, maximum weekly hours, minimum rest between shifts (hours), maximum consecutive working days - whole-number steppers with units; maximum must be at least standard. *(source: screens/P08-venue-back-office.yaml#BO-881 / contracts/satellite/workforce.yaml#/components/schemas/StaffingRules)*
- **Overtime**: One choice Allowed / Allowed with approval / Prohibited; threshold "after [48] h a week"; rate multiplier ("x1.25"); maximum overtime per week. Approval is a choice here, not a button. *(source: screens/P08-venue-back-office.yaml#BO-881 / contracts/satellite/workforce.yaml#/components/schemas/StaffingRules)*
- **Night work and open-shift incentives**: Minimum age for night shifts; default and maximum incentive multiplier for released shifts, and the multiplier above which a second person approves. *(source: contracts/satellite/workforce.yaml#/components/schemas/StaffingRules)*
- **Scope**: Venue-wide (the top-bar venue); role and employee-group overrides drawn as a greyed "Add rule for a role" until supported. *(source: screens/P08-venue-back-office.yaml#BO-881)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approval required (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rule summary**: Plain sentences ("Overtime needs a manager's approval", "Maximum 6 consecutive days", "Minimum 11 h rest between shifts") as in the client render. *(source: screens/P08-venue-back-office.yaml#BO-881)*
- **Warnings the rota will raise**: Approaching overtime, Overtime generated, Maximum hours exceeded, Rest-period violation, Consecutive-day violation - each with an example. *(source: screens/P08-venue-back-office.yaml#BO-881)*
- **AI consideration note**: "Smart assignment prefers candidates who create no overtime" with the example (Maria +2 h overtime, David none: recommends David). *(source: screens/P08-venue-back-office.yaml#BO-881)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rules**: Sends the full staffing-rules record including the current minimum cover rows (per VO-R04); confirm names the effect ("Next week's rota: 3 assignments will now breach the 60 h weekly limit"). *(source: contracts/satellite/workforce.yaml#setStaffingRules)*

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The overtime working-hour rules configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the overtime working-hour rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No overtime working-hour rules configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A tighter rule makes published assignments breach it**: Saved; breaches appear on BO-890 and the confirm says how many. *(source: contracts/satellite/workforce.yaml#validateWorkforceCompliance)*
- **Viewer without WORKFORCE_MANAGE**: Read-only with "Needs workforce management rights" on Save. *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-885`: Same record (StaffingRules); draw as two sections of one editor or make both send the whole record.
- Match `BO-890`: Every rule here is a finding code there; same words.
- Match `BO-879`: Template controls cannot exceed these limits.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
  standardDaily: 8 h
  standardWeekly: 48 h
  maxDaily: 12 h
  maxWeekly: 60 h
  minRest: 11 h
  maxConsecutiveDays: 6
  overtime: Allowed with approval after 48 h a week, x1.25
  maxOvertimeWeek: 12 h
  minAgeNight: 18
```

#### Permissions

- `setStaffingRules` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-881` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-881`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 16: Works in Overtime & Working-Hour Rules → Configure workforce rules controlling employee working hours and overtime eligibility before operational rostering occurs.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-881?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Approval required.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-882` Workforce Integration & Synchronization Center

**Connect TICVAI Resource Management with external HR, workforce management, payroll, identity and employee systems where applicable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-882 |
| Who uses it | venue staff holding `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `sourceId` (navigation) |
| Route | `/rentals/workforce-integration-synchronization-center-bo-882` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): listRotaAssignments was bound as "Rota synchronisation"; the rota has nothing to do with the integration and synchronisation centre (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Workforce integration and synchronisation centre: which external systems (HRMS, workforce management, payroll, time and attendance, identity, staffing agencies) feed TICVAI, how, who masters each field, how each synchronisation went in counts, and the disagreements a person must settle. Tenant-wide, not per venue. The one thing to get right: failures are stated as their operational consequence ("4 employees have assignments in the next 24 hours") and a termination conflict says what happens to future shifts.

**Known correction pending (do not draw the wrong version)**

- **The table and detail carry the pack's labels as unbound text and the gap says no schema exists** Why: listIntegrationSources, listSyncRuns, listSyncConflicts and their schemas now exist; bind them. *(source: contracts/satellite/workforce.yaml#listIntegrationSources / contracts/satellite/workforce.yaml#listSyncRuns / contracts/satellite/workforce.yaml#listSyncConflicts; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"API", "Webhooks/event-driven integration", "Scheduled synchronization", "Manual synchronization", "File import where required" are drawn as action buttons** Why: They are values of a source's transport. *(source: contracts/satellite/workforce.yaml#/components/schemas/WorkforceIntegrationSource; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **setIntegrationSource accepts authenticationStatus and lastSynchronisedAt** Why: Both are observed by the server, not set by an administrator (VO-R03). *(source: contracts/satellite/workforce.yaml#setIntegrationSource; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): listRotaAssignments is bound as "Rota synchronisation" (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where are field mappings (external field name to TICVAI field) and connection credentials configured? Only ownership has an operation.** → Drawn default accepted: Draw a "Mapping" tab and a "Connection" section greyed with "Configured by TICVAI support". *(decided by Chinmay, 2026-10-02; DEC-499 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Source | picker: choose a source | — | — | `listSyncRuns` ?sourceId |
| Status | text field | — | — | `listSyncRuns` ?status |
| Source | picker: choose a source | — | — | `listSyncConflicts` ?sourceId |
| Status | text field | — | — | `listSyncConflicts` ?status |
| Kind | text field | — | — | `listSyncConflicts` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Source**: Name, code, kind (HRMS, Workforce management, Payroll, Time and attendance, Identity, Staffing agency), transport (API, Webhook, Scheduled, Manual, File import), status (Active, Degraded, Suspended). Authentication status and last synchronised are shown, not entered. *(source: screens/P08-venue-back-office.yaml#BO-882 / contracts/satellite/workforce.yaml#setIntegrationSource)*
- **Field ownership**: A grid of TICVAI fields (Employee ID, Name, Department, Role, Venue, Employment status, Working hours, Leave, Shift, Skills, Certifications) with Master = TICVAI / External and On conflict = External wins / TICVAI wins / Flag for review. Unlisted means TICVAI. Saved as one set. *(source: screens/P08-venue-back-office.yaml#BO-882 / contracts/satellite/workforce.yaml#setFieldOwnership)*
- **Run now**: Source picker and "Dry run (report only)" toggle, on by default for the first run of a new source. *(source: contracts/satellite/workforce.yaml#startSync)*

#### Outputs: what the screen shows and produces

**Shown**

**Every workforce integration synchronization** (data table)

| Shows | Format | Notes |
|---|---|---|
| Connected systems | text | not in the schema: `Connected systems` |
| Last synchronization | text | not in the schema: `Last synchronization` |
| Successful records | text | not in the schema: `Successful records` |
| Failed records | text | not in the schema: `Failed records` |
| Warnings | text | not in the schema: `Warnings` |
| Mapping errors | text | not in the schema: `Mapping errors` |
| Authentication status | text | not in the schema: `Authentication status` |
| Conflict handling | text | not in the schema: `Conflict Handling` |

**The selected workforce integration synchronization** (detail panel): The pack groups this record's detail under its own headings: “Integration Sources”, “External System Master”, “For example”, “Board 3 Shared Governance”, “Board 3 End-to-End Outcome”, “The platform understands”.

| Shows | Format | Notes |
|---|---|---|
| Connected systems | text | not in the schema: `Connected systems` |
| Last synchronization | text | not in the schema: `Last synchronization` |
| Successful records | text | not in the schema: `Successful records` |
| Failed records | text | not in the schema: `Failed records` |
| Warnings | text | not in the schema: `Warnings` |
| Mapping errors | text | not in the schema: `Mapping errors` |
| Authentication status | text | not in the schema: `Authentication status` |
| Conflict handling | text | not in the schema: `Conflict Handling` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| API (primary button) | navigation or local | — | — | — | — |
| Webhooks/event-driven integration (secondary button) | navigation or local | — | — | — | — |
| Scheduled synchronization (secondary button) | navigation or local | — | — | — | — |
| Manual synchronization (secondary button) | navigation or local | — | — | — | — |
| File import where required (secondary button) | navigation or local | — | — | — | — |
| Integration Monitoring (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Connected systems**: One row per source with kind, transport, last synchronised ("12 min ago"), authentication status (Healthy, Expiring, Expired, Failed, Not configured) and status, as tiles on top (Connected, Last sync, Records synced, Failed). *(source: screens/P08-venue-back-office.yaml#BO-882 / contracts/satellite/workforce.yaml#listIntegrationSources)*
- **Synchronisation runs**: Started, finished, trigger, status (Running, Succeeded, Partial, Failed), records read, applied, failed, warnings, mapping errors; cursor paged. *(source: contracts/satellite/workforce.yaml#listSyncRuns)*
- **Conflicts**: Kind in words (In HR but not in TICVAI, In TICVAI but not in HR, Venue changed in HR, Certification expired, Terminated in HR, Field disagreement), employee, detail, assignments at risk (count, snapshot), raised, status. *(source: contracts/satellite/workforce.yaml#listSyncConflicts / contracts/satellite/workforce.yaml#/components/schemas/WorkforceSyncConflict)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resolve conflict**: Accept external / Keep TICVAI / Retry / Ignore / Escalate with a note (max 1,000). For Terminated in HR, a required choice "Release the 4 future assignments to the marketplace" or "Keep them for now", stated in the confirm. *(source: contracts/satellite/workforce.yaml#resolveSyncConflict)*
- **Run synchronisation now**: Starts a run; the row shows Running; a dry run reports "Would update 37 employees, 2 conflicts" without applying. *(source: contracts/satellite/workforce.yaml#startSync)*
- **Save ownership**: Replaces the whole ownership set for the source; confirm lists the fields moving between masters. *(source: contracts/satellite/workforce.yaml#setFieldOwnership)*

**Data it reads**: `listIntegrationSources` (onLoad, Connected workforce systems); `getFieldOwnership` (onLoad, Which system masters each field); `listSyncRuns` (onLoad, Synchronisation runs); `listSyncConflicts` (onLoad, Disagreements between systems)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workforce integration synchronization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workforce integration synchronization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workforce integration synchronization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workforce integration synchronization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A run is already in progress for this source; 409 Already resolved, or the resolution is not available for this kind |

#### Edge cases to draw

- **Credentials expiring or failed**: Amber or red row with "Credentials expire in 5 days" and the last good run; never just "integration failed". *(source: contracts/satellite/workforce.yaml#/components/schemas/WorkforceIntegrationSource)*
- **Partial run**: "12 availability updates could not be applied. 4 employees have assignments in the next 24 hours." with a link to them. *(source: contracts/satellite/workforce.yaml#/components/schemas/WorkforceSyncRun)*
- **Venue switcher changed**: Nothing changes; banner "Applies to all venues of Yas Leisure Group". *(source: contracts/satellite/workforce.yaml#listIntegrationSources)*

#### Consistency with other screens

- Match `BO-874`: Ownership locks on the profile come from this grid.
- Match `BO-880`: Leave imported from HR is marked with the source named here.
- Match `BO-887`: Released assignments from a termination conflict appear in the marketplace.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sources:
- name: Oracle HCM
  kind: HRMS
  transport: API
  lastSync: 1 Oct 2026 06:00
  auth: Healthy
  status: Active
- name: UKG Workforce
  kind: Workforce management
  transport: Webhook
  lastSync: 12 min ago
  auth: Healthy
- name: Payroll (SAP)
  kind: Payroll
  transport: Scheduled
  lastSync: 30 Sep 2026 23:00
  auth: Expiring
- name: Staffing agency - Emirates Talent
  kind: Staffing agency
  transport: File import
  lastSync: 28 Sep 2026
  auth: Not configured
run:
  source: Oracle HCM
  status: Partial
  read: 1248
  applied: 1225
  failed: 23
  warnings: 4
  mappingErrors: 2
conflict:
  kind: Terminated in HR
  employee: Yousef Al Ali
  atRisk: 4 assignments (10-13 Oct)
  status: Open
```

#### Permissions

- `listIntegrationSources` → `WORKFORCE_VIEW` (read) · staff
- `setIntegrationSource` → `WORKFORCE_MANAGE` (configure) · staff
- `getFieldOwnership` → `WORKFORCE_VIEW` (read) · staff
- `setFieldOwnership` → `WORKFORCE_MANAGE` (configure) · staff
- `listSyncRuns` → `WORKFORCE_VIEW` (read) · staff
- `startSync` → `WORKFORCE_MANAGE` (configure) · staff
- `listSyncConflicts` → `WORKFORCE_VIEW` (read) · staff
- `resolveSyncConflict` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-882` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-882`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 18: Works in Workforce Integration & Synchronization Center → Connect TICVAI Resource Management with external HR, workforce management, payroll, identity, and employee systems where applicable.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-882?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: API, Webhooks/event-driven integration, Scheduled synchronization, Manual synchronization, File import where required, Integration Monitoring.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createResourceBlock": {"method":"POST","path":"/resource-blocks","contract":"resources","summary":"Take a resource out of service for a window, with a reason","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceBlock","responds":"ResourceBlock"},
"getEmployee": {"method":"GET","path":"/employees/{employeeId}","contract":"workforce","summary":"One person, with their employment, postings and leave balances","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"employeeId","in":"path","required":true}],"requestBody":null,"responds":"WorkforceEmployeeProfile"},
"getExperienceResourceRequirements": {"method":"GET","path":"/experiences/{experienceId}/resource-requirements","contract":"resources","summary":"What an experience needs before it can run","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceRequirement"},
"getFieldOwnership": {"method":"GET","path":"/integration-sources/{sourceId}/field-ownership","contract":"workforce","summary":"Which fields this source masters","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"sourceId","in":"path","required":true}],"requestBody":null,"responds":"WorkforceFieldOwnership"},
"getPrincipal": {"method":"GET","path":"/principals/{principalId}","contract":"identity","summary":"Read a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Principal"},
"getResourceQualifications": {"method":"GET","path":"/resources/{resourceId}/qualifications","contract":"resources","summary":"What an instructor or staff resource is certified to do, and until when — as saved","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Qualification"},
"getResourceSchedule": {"method":"GET","path":"/resources/{resourceId}/schedule","contract":"resources","summary":"The pattern of when it is normally available","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceSchedule"},
"listIntegrationSources": {"method":"GET","path":"/integration-sources","contract":"workforce","summary":"External systems that master workforce data, and their health","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"WorkforceIntegrationSource"},
"listJobTitles": {"method":"GET","path":"/job-titles","contract":"workforce","summary":"The job titles a posting can name","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkforceJobTitle"},
"listLeaveBalances": {"method":"GET","path":"/leave-balances","contract":"workforce","summary":"What each person has left, by leave type","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"employeeId","in":"query","required":null},{"name":"leaveTypeId","in":"query","required":null}],"requestBody":null,"responds":"WorkforceLeaveBalance"},
"listLeaveRequests": {"method":"GET","path":"/leave-requests","contract":"workforce","summary":"Leave, absence and their effect on cover","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"LeaveRequest"},
"listLeaveTypes": {"method":"GET","path":"/leave-types","contract":"workforce","summary":"Leave types and how each accrues","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkforceLeaveType"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResources": {"method":"GET","path":"/resources","contract":"resources","summary":"Resources at this venue","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"availableFrom","in":"query","required":null},{"name":"availableTo","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"listShiftPatterns": {"method":"GET","path":"/shift-patterns","contract":"workforce","summary":"Named shift patterns","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkforceShift"},
"listShiftTemplates": {"method":"GET","path":"/shift-templates","contract":"workforce","summary":"Named shift patterns a rota is built from","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ShiftTemplate"},
"listSyncConflicts": {"method":"GET","path":"/sync-conflicts","contract":"workforce","summary":"Disagreements a person has to settle","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"sourceId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSyncRuns": {"method":"GET","path":"/sync-runs","contract":"workforce","summary":"Synchronisation history, with counts","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"sourceId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkAssignments": {"method":"GET","path":"/work-assignments","contract":"workforce","summary":"Where each person is posted, and from when","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"employeeId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"activeOn","in":"query","required":null}],"requestBody":null,"responds":"WorkforceWorkAssignment"},
"requestLeave": {"method":"POST","path":"/leave-requests","contract":"workforce","summary":"Ask for time off, against the cover it would cost","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LeaveRequest","responds":"LeaveRequest"},
"resolveSyncConflict": {"method":"POST","path":"/sync-conflicts","contract":"workforce","summary":"Settle a disagreement","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResolveSyncConflictRequest","responds":"WorkforceSyncConflict"},
"setExperienceResourceRequirements": {"method":"PUT","path":"/experiences/{experienceId}/resource-requirements","contract":"resources","summary":"Bind resource requirements to an experience","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceRequirement"},
"setFieldOwnership": {"method":"PUT","path":"/integration-sources/{sourceId}/field-ownership","contract":"workforce","summary":"Declare who masters each field","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"sourceId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"WorkforceFieldOwnership","responds":"WorkforceFieldOwnership"},
"setIntegrationSource": {"method":"PUT","path":"/integration-sources","contract":"workforce","summary":"Connect or reconfigure an external workforce system","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkforceIntegrationSource","responds":"WorkforceIntegrationSource"},
"setLeaveType": {"method":"PUT","path":"/leave-types","contract":"workforce","summary":"Define a leave type","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkforceLeaveType","responds":"WorkforceLeaveType"},
"setResourceQualifications": {"method":"PUT","path":"/resources/{resourceId}/qualifications","contract":"resources","summary":"What a person resource is certified to do, and until when","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Qualification"},
"setResourceSchedule": {"method":"PUT","path":"/resources/{resourceId}/schedule","contract":"resources","summary":"Operating hours, working pattern and bookable slots","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ResourceSchedule","responds":"ResourceSchedule"},
"setShiftPattern": {"method":"PUT","path":"/shift-patterns","contract":"workforce","summary":"Define a shift pattern and its break","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkforceShift","responds":"WorkforceShift"},
"setShiftTemplate": {"method":"PUT","path":"/shift-templates","contract":"workforce","summary":"Define a shift pattern, its breaks and its qualifications","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ShiftTemplate","responds":"ShiftTemplate"},
"setStaffingRules": {"method":"PUT","path":"/staffing-rules","contract":"workforce","summary":"Minimum cover, working-hour limits and overtime","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StaffingRules","responds":"StaffingRules"},
"startSync": {"method":"POST","path":"/sync-runs","contract":"workforce","summary":"Run a synchronisation now","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"suggestResources": {"method":"GET","path":"/resource-suggestions","contract":"resources","summary":"Resources matching a requirement, by attribute","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceTypeId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"attributes","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"validateWorkforceCompliance": {"method":"GET","path":"/workforce-compliance","contract":"workforce","summary":"Where the rota breaks a rule","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"WorkforceComplianceFinding"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"LeaveRequest": {"type":"object","x-ticvai-persistence":"workforce.leave_request","description":"Resource board 3.8. **Approving leave without seeing the gap is how four supervisors book the same week.**\n","required":["principalId","from","to","kind"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["annual","sick","unpaid","parental","compassionate","training","timeOffInLieu"]},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"halfDay":{"type":"boolean","default":false},"reason":{"type":"string","nullable":true},"status":{"type":"string","enum":["requested","approved","rejected","cancelled","taken"]},"coverageImpact":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/StaffingCoverage"}},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"**The event this product sells admission to** (4 October 2026, CHG-FXC-011; WEB-002, WEB-004): a product page finds its event and the event's performances (`Performance.eventId`) give it dates. Null for a product not tied to an event (merchandise, a pass, a membership)."}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"Qualification": {"type":"object","x-ticvai-persistence":"resources.qualification","description":"1.2.36. **A role is not a skill**, and the check happens before assignment rather than after.\n","required":["code","name"],"properties":{"resourceId":{"type":"string","format":"uuid","readOnly":true,"description":"**The resource that holds this qualification.** Set from the path of `setResourceQualifications`; without it a stored qualification belongs to nobody and the check before assignment has nothing to check against. One row per resource and `code`.\n"},"code":{"type":"string"},"name":{"type":"string"},"issuedAt":{"type":"string","format":"date","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**The field that makes this worth having.** A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one.\n"},"issuer":{"type":"string","nullable":true},"documentAssetId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ResolveSyncConflictRequest": {"type":"object","x-ticvai-persistence":"none — writes sync_conflict","required":["conflictId","resolution"],"properties":{"conflictId":{"type":"string","format":"uuid"},"resolution":{"type":"string","enum":["acceptExternal","keepTicvai","retry","ignore","escalate"]},"note":{"type":"string","maxLength":1000,"nullable":true},"releaseAffectedAssignments":{"type":"boolean","default":false,"description":"**For a termination conflict, what happens to the shifts already rostered.** Board 3 requires the downstream consequence to be acted on rather than reported: releasing them puts the shifts back on the marketplace, and leaving them means a manager has decided to cover them another way.\n"}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true},"resourceTypeId":{"type":"string","format":"uuid","nullable":true,"description":"**The configurable resource type** (`resources.resource_type`, 4 October 2026, CHG-FXC-003). `kind` is the fixed family a type belongs to; this is the tenant's own type within it, and the `resourceTypeId` filter of `suggestResources` and `ResourceRequirement.resourceTypeId` match on it."}}},
"ResourceBlock": {"type":"object","x-ticvai-persistence":"resources.resource_block","description":"Board 2.07. **A block is not a booking**, and the reason travels with it so an operator knows whether to wait or to look elsewhere.\n","required":["resourceId","from","to","reason"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["setup","teardown","maintenance","blackout","closed","operational","training"]},"note":{"type":"string","nullable":true},"createdBy":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourceRequirement": {"type":"object","x-ticvai-persistence":"resources.resource_requirement","description":"**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n","required":["quantity"],"properties":{"id":{"type":"string","format":"uuid"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"},"quantity":{"type":"integer","default":1},"mandatory":{"type":"boolean","default":true},"requiredQualifications":{"type":"array","items":{"type":"string"}},"requiredAttributes":{"type":"object","additionalProperties":true},"substituteResourceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"},"packageId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The package this requirement is a component of** (4 October 2026, CHG-FXC-003). Written by `updateResourcePackage`, which replaces the package's `components` as these rows; `listResourcePackages` reads them back by it. Null for an experience's own requirement (`productId`)."},"productId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The experience product this requirement belongs to (`setExperienceResourceRequirements`). Exactly one of `packageId` and `productId` is set."}}},
"ResourceSchedule": {"type":"object","x-ticvai-persistence":"resources.resource_schedule","description":"Boards 2.03 and 2.04. **A recurring pattern with exceptions, not a list of dates.** A schedule written as concrete dates silently expires.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"availabilityMode":{"type":"string","enum":["alwaysAvailable","scheduled","onRequest"]},"windows":{"type":"array","items":{"type":"object","properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."},"to":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true}}}},"slotMinutes":{"type":"integer","nullable":true,"description":"**How finely this resource's time can be cut**, which is a property of the resource and not of the product sold against it.\n"},"minimumBookingMinutes":{"type":"integer","nullable":true},"maximumBookingMinutes":{"type":"integer","nullable":true},"advanceBookingDays":{"type":"integer","nullable":true},"exceptions":{"type":"array","items":{"type":"object","properties":{"date":{"type":"string","format":"date"},"closed":{"type":"boolean"},"from":{"type":"string","nullable":true,"pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."},"to":{"type":"string","nullable":true,"pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."}}}},"scopePath":{"type":"string"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"ShiftTemplate": {"type":"object","x-ticvai-persistence":"workforce.shift_template","description":"Resource board 3.7. **The unit a manager actually thinks in.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["early","late","middle","split","double","night","onCall","overtime"]},"startsAt":{"type":"string"},"endsAt":{"type":"string"},"breaks":{"type":"array","items":{"type":"object","properties":{"afterMinutes":{"type":"integer"},"minutes":{"type":"integer"},"paid":{"type":"boolean","default":false}}}},"requiredQualifications":{"type":"array","items":{"type":"string"}},"roleCode":{"type":"string","nullable":true},"costCentre":{"type":"string","nullable":true},"hourlyRate":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"StaffingCoverage": {"type":"object","description":"Resource board 4.4. **The gap is the product.**","properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"from":{"type":"string"},"to":{"type":"string"},"required":{"type":"integer"},"rostered":{"type":"integer"},"qualified":{"type":"integer","description":"**A position filled by somebody not qualified for it is still a gap.**"},"gap":{"type":"integer"},"severity":{"type":"string","enum":["covered","tight","short","blocking"]},"openShiftIds":{"type":"array","items":{"type":"string","format":"uuid"}},"basisApplied":{"type":"string","enum":["minimum","forecastRequirement"],"description":"Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the period, `minimum`."},"minimumRequired":{"type":"integer","nullable":true,"description":"The configured minimum for the position and window."},"forecastRequired":{"type":"number","nullable":true,"description":"The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. Null where none was handed over."},"forecastRequiredP90":{"type":"number","nullable":true,"description":"The busy-case requirement, for planning to the busy case."},"forecastVersionId":{"type":"string","format":"uuid","nullable":true,"description":"The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it."}}},
"StaffingRules": {"type":"object","x-ticvai-persistence":"workforce.staffing_rules + workforce.position_requirement","description":"Resource board 4.3. **A safety rule before it is a cost rule.**","properties":{"minimumCover":{"type":"array","description":"**Minimum staffing per position, venue and time window, with the qualifications it requires**: the rows of `workforce.position_requirement` (data model for the agreed operations, 29 September). `getStaffingCoverage` measures the rota against them; before this they were an array with no table, so no minimum was stored.","items":{"type":"object","required":["id","positionCode","minimumHeadcount"],"properties":{"id":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"venueId":{"type":"string","format":"uuid","nullable":true},"attractionId":{"type":"string","format":"uuid","nullable":true},"minimumHeadcount":{"type":"integer","minimum":0},"daysOfWeek":{"type":"array","nullable":true,"description":"Days the minimum applies; absent means every day the venue is open","items":{"type":"string","enum":["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]}},"startsAt":{"type":"string","nullable":true,"description":"Start of the time window, local time (HH:MM) as `ShiftTemplate.startsAt`; absent means opening"},"endsAt":{"type":"string","nullable":true,"description":"End of the time window, local time (HH:MM); absent means closing"},"requiredQualifications":{"type":"array","items":{"type":"string"}},"appliesWhenOpen":{"type":"boolean","default":true},"blocksOperation":{"type":"boolean","default":true,"description":"**A ride requiring two operators cannot run with one.** Where this is true the attraction closes rather than running short.\n"}}}},"maximumHoursPerDay":{"type":"integer","nullable":true},"maximumHoursPerWeek":{"type":"integer","nullable":true},"minimumRestHours":{"type":"integer","nullable":true},"maximumConsecutiveDays":{"type":"integer","nullable":true},"overtime":{"type":"object","properties":{"allowed":{"type":"boolean","default":true},"afterHoursPerWeek":{"type":"integer","nullable":true},"rateMultiplier":{"type":"number","nullable":true},"requiresApproval":{"type":"boolean","default":true}}},"minimumAgeForNightShift":{"type":"integer","nullable":true},"defaultIncentiveRateMultiplier":{"type":"number","nullable":true,"minimum":1,"description":"**What an open shift pays above base when it is released.** Added 22 September: `workforce.open_shift.incentive_rate_multiplier` was set per shift with nothing behind it, so two identical shifts could price differently and record no reason. The shift still carries its own value — **as the snapshot**, the rule-and-record split `payments.fee_rule` and `orders.order_fee` use — and this is where it comes from.\n**Top-level rather than beside `overtime`** so the value is its own column. Nested in an object it would be a key inside a JSON blob, which nothing can index, constrain or pair to the shift that uses it.\n"},"maximumIncentiveRateMultiplier":{"type":"number","nullable":true,"minimum":1,"description":"**The ceiling on an incentive.** A shift nobody claims is the moment somebody raises the multiplier in a hurry — the same reason `maximumDailyCharge` bounds a late fee."},"incentiveApprovalAbove":{"type":"number","nullable":true,"minimum":1,"description":"**Above this multiplier a second person approves the release.** Routed as an approval, not a boolean — `overtime.requiresApproval` beside it is one of 26 approval flags across the contracts that no approval kind, matrix row or SLA reaches."},"scopePath":{"type":"string"}}},
"WorkforceComplianceFinding": {"type":"object","description":"Resource board 4.8. **Checked before the rota is published, not in an inspection.**","properties":{"code":{"type":"string","enum":["expiredQualification","missingQualification","exceededDailyHours","exceededWeeklyHours","insufficientRest","missedBreak","consecutiveDaysExceeded","underAgeNightShift","belowMinimumCover"]},"severity":{"type":"string","enum":["breach","warning"]},"principalId":{"type":"string","format":"uuid","nullable":true},"principalName":{"type":"string","nullable":true},"date":{"type":"string","format":"date","nullable":true},"detail":{"type":"string"},"rotaAssignmentIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"WorkforceEmployee": {"type":"object","x-ticvai-persistence":"workforce.employee","description":"**Taken from the backend workbook, 20 September.** Stores the main employee/staff master record.","required":["tenantId","code","firstName","lastName","dateOfJoining","employmentType","employmentStatus","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid","nullable":true},"code":{"type":"string","maxLength":50},"firstName":{"type":"string","maxLength":100},"lastName":{"type":"string","maxLength":100},"email":{"type":"string","maxLength":254,"nullable":true},"mobile":{"type":"string","maxLength":30,"nullable":true},"dateOfJoining":{"type":"string","format":"date"},"dateOfBirth":{"type":"string","format":"date","nullable":true,"description":"**What the under-age check needs** (data model for the agreed operations, 29 September): `validateWorkforceCompliance` reports `underAgeNightShift` against `StaffingRules.minimumAgeForNightShift`, and that rule has nothing to compare with unless the employee's age is on file. **An employee with no date of birth is reported as a warning**, not assumed to be of age."},"employmentType":{"type":"string","maxLength":30},"employmentStatus":{"type":"string","maxLength":30},"managerEmployeeId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkforceEmployeeProfile": {"type":"object","x-ticvai-persistence":"none — composed from employee and four related tables","description":"**One person and everything a profile screen asks about them.** The employment record, the postings and the leave balances are separate tables and one question, so fanning out across four endpoints is four round trips and four chances to render a half-loaded person.\n","required":["employee"],"properties":{"employee":{"$ref":"#/components/schemas/WorkforceEmployee"},"employments":{"type":"array","description":"Most recent first. **More than one is normal** — a seasonal worker rehired each summer has several, and collapsing them to the current one loses the service history that leave accrual is calculated from.\n","items":{"$ref":"#/components/schemas/WorkforceEmployment"}},"assignments":{"type":"array","items":{"$ref":"#/components/schemas/WorkforceWorkAssignment"}},"leaveBalances":{"type":"array","items":{"$ref":"#/components/schemas/WorkforceLeaveBalance"}},"jobTitles":{"type":"array","description":"The titles the postings name, so a client does not have to resolve them one by one.\n","items":{"$ref":"#/components/schemas/WorkforceJobTitle"}},"externallyMasteredFields":{"type":"array","description":"**Which fields on this record the venue may not edit**, resolved from `field_ownership` for whichever source masters this employee. A screen that shows an editable input over a field the HRMS owns has promised something it cannot keep.\n","items":{"type":"string"}}}},
"WorkforceEmployment": {"type":"object","x-ticvai-persistence":"workforce.employment","description":"**Taken from the backend workbook, 20 September.** Stores employment terms and contract validity.","required":["employeeId","contractType","startDate","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"employeeId":{"type":"string","format":"uuid"},"contractType":{"type":"string","maxLength":30},"startDate":{"type":"string","format":"date"},"endDate":{"type":"string","format":"date","nullable":true},"standardHoursPerWeek":{"type":"number","nullable":true},"probationEndDate":{"type":"string","format":"date","nullable":true},"status":{"type":"string","maxLength":30},"createdAt":{"type":"string","format":"date-time"}}},
"WorkforceFieldOwnership": {"type":"object","x-ticvai-persistence":"workforce.field_ownership","description":"**Which system owns a field, which is what prevents conflicting updates.** Board 3: *\"For every field, administrators shall determine ... External System Master.\"* Without this, an employee record mastered in HRMS and edited here disagrees with its source and nothing can say which answer is right.\nOne row per table and column. Absent means ours, so nothing has to be enumerated before it is decided.\n","required":["tableName","columnName","master"],"properties":{"id":{"type":"string","format":"uuid"},"tableName":{"type":"string","maxLength":120},"columnName":{"type":"string","maxLength":120},"master":{"type":"string","enum":["ticvai","external"]},"sourceId":{"type":"string","format":"uuid","nullable":true,"description":"The integration source that masters it, when `master` is `external`."},"onConflict":{"type":"string","enum":["externalWins","ticvaiWins","flagForReview"]},"scopePath":{"type":"string","nullable":true}}},
"WorkforceIntegrationSource": {"type":"object","x-ticvai-persistence":"workforce.integration_source","description":"**An external system that masters some of our workforce data.** Board 3 names HRMS, Workforce Management, Payroll, Time & Attendance, Identity Management and external staffing agencies. The six-state display Board 10 asks for lives on this row: what is connected, when it last synchronised, and whether its credentials still work.\n","required":["code","name","kind","transport","status"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":60},"name":{"type":"string","maxLength":150},"kind":{"type":"string","enum":["hrms","workforceManagement","payroll","timeAndAttendance","identity","staffingAgency"]},"transport":{"type":"string","enum":["api","webhook","scheduled","manual","fileImport"],"description":"Board 3, Support. **`manual` and `fileImport` are in the list on purpose** — a staffing agency that sends a spreadsheet is still a system of record, and modelling only the API cases would leave the messiest source unmanaged.\n"},"authenticationStatus":{"type":"string","enum":["healthy","expiring","expired","failed","notConfigured"]},"lastSynchronisedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","degraded","suspended"]},"scopePath":{"type":"string","nullable":true}}},
"WorkforceJobTitle": {"type":"object","x-ticvai-persistence":"workforce.job_title","description":"**Taken from the backend workbook, 20 September.** Stores job/designation definitions such as Cashier, Manager, Chef or Technician.","required":["tenantId","code","name","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":50},"name":{"type":"string","maxLength":150},"description":{"type":"string","maxLength":500,"nullable":true},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkforceLeaveBalance": {"type":"object","x-ticvai-persistence":"workforce.leave_balance","description":"**Taken from the backend workbook, 20 September.** Stores leave entitlement, used amount and remaining balance per employee/period.","required":["employeeId","typeId","periodYear","entitledDays","usedDays","pendingDays","availableDays","updatedAt"],"properties":{"id":{"type":"string","format":"uuid"},"employeeId":{"type":"string","format":"uuid"},"typeId":{"type":"string","format":"uuid"},"periodYear":{"type":"integer"},"entitledDays":{"type":"number"},"usedDays":{"type":"number"},"pendingDays":{"type":"number"},"availableDays":{"type":"number"},"updatedAt":{"type":"string","format":"date-time"}}},
"WorkforceLeaveType": {"type":"object","x-ticvai-persistence":"workforce.leave_type","description":"**Taken from the backend workbook, 20 September.** Defines leave categories and basic leave behavior.","required":["tenantId","code","name","isPaid","requiresApproval","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":50},"name":{"type":"string","maxLength":100},"isPaid":{"type":"boolean"},"requiresApproval":{"type":"boolean"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"WorkforceShift": {"type":"object","x-ticvai-persistence":"workforce.shift","description":"**Taken from the backend workbook, 20 September.** Defines reusable shifts such as Morning, Evening or Night.","required":["tenantId","code","name","startTime","endTime","breakMinutes","crossesMidnight","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":50},"name":{"type":"string","maxLength":100},"startTime":{"type":"string","maxLength":0},"endTime":{"type":"string","maxLength":0},"breakMinutes":{"type":"integer"},"crossesMidnight":{"type":"boolean"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"WorkforceSyncConflict": {"type":"object","x-ticvai-persistence":"workforce.sync_conflict","description":"**A disagreement a person has to settle, and the assignments it puts at risk.** Board 3 lists the cases by name: an employee in HR and not here, a venue changed externally, a certification expired, and *\"employee terminated externally but has future TICVAI assignments\"* — where *\"the system shall flag affected downstream assignments\"*.\n`affectedAssignmentIds` is deliberately an array and deliberately an exception: it is a snapshot of what was at risk when the conflict was raised, not a live relationship, and it must not change when a roster does.\n","required":["sourceId","kind","status","raisedAt"],"properties":{"id":{"type":"string","format":"uuid"},"sourceId":{"type":"string","format":"uuid"},"syncRunId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["missingInTicvai","missingExternally","venueChangedExternally","certificationExpired","terminatedExternally","fieldDisagreement"]},"employeeId":{"type":"string","format":"uuid","nullable":true},"externalReference":{"type":"string","maxLength":200,"nullable":true},"detail":{"type":"string","maxLength":1000,"nullable":true},"affectedAssignmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","enum":["open","retried","reprocessed","escalated","resolved","ignored"]},"raisedAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","nullable":true}}},
"WorkforceSyncRun": {"type":"object","x-ticvai-persistence":"workforce.sync_run","description":"**One synchronisation, and what it did.** Board 10 asks the page to show successful records, failed records, warnings and mapping errors rather than *\"integration failed\"* — and to say the operational consequence: *\"12 employee availability updates could not be synchronised. Four employees have assignments within the next 24 hours.\"* That sentence needs counts on a row, not a log line.\n","required":["sourceId","startedAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"sourceId":{"type":"string","format":"uuid"},"startedAt":{"type":"string","format":"date-time"},"finishedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["running","succeeded","partial","failed"]},"recordsRead":{"type":"integer"},"recordsApplied":{"type":"integer"},"recordsFailed":{"type":"integer"},"warningCount":{"type":"integer"},"mappingErrorCount":{"type":"integer"},"trigger":{"type":"string","enum":["scheduled","manual","webhook","fileImport"]},"scopePath":{"type":"string","nullable":true}}},
"WorkforceWorkAssignment": {"type":"object","x-ticvai-persistence":"workforce.work_assignment","description":"**Taken from the backend workbook, 20 September.** Assigns an employee to a job and operational location/scope for an effective period.","required":["employeeId","jobTitleId","effectiveFrom","isPrimary","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"employeeId":{"type":"string","format":"uuid"},"jobTitleId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true},"effectiveFrom":{"type":"string","format":"date"},"effectiveTo":{"type":"string","format":"date","nullable":true},"isPrimary":{"type":"boolean"},"status":{"type":"string","maxLength":30},"createdAt":{"type":"string","format":"date-time"}}}
}
```
