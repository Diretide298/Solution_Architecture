# WS01 — Access Control board 1

**10 screens · 20 operations · 29 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ACCESS_POINT_CONFIGURE, SCOPE_MANAGE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-144` | Access Control Command Center | B–D | 0 | 30 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-145` | Venue & Park Access Structure | B–D | 0 | 0 | 6 | 6 | 0 | 0 | — | notStarted (generated) |
| `BO-146` | Access Area & Zone Builder | B–D | 12 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-147` | Attraction Access Configuration | B–D | 12 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-148` | Access Point Directory | B–D | 25 | 0 | 5 | 2 | 2 | 0 | — | notStarted (generated) |
| `BO-149` | Gate & Lane Configuration | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-150` | Access Control Graphical Map Designer | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-151` | Access Location Grouping | A | 6 | 3 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-152` | Operating Calendar & Special Access Days | B–D | 23 | 7 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-153` | Topology Validation & Publication | B–D | 1 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-144, BO-145, BO-146, BO-147, BO-149, BO-150, BO-151, BO-153 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-144` Access Control Command Center

**Central operational/configuration landing page for the complete Access Control module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Dashboard should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-control-command-center-bo-144` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The command centre monitors (VO-R02); creating an access point belongs on the Access Point Directory BO-148 (design-notes correction venue-operations BO-144).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The landing page of the whole Access Control module and of board 1 (topology): an access manager or duty manager sees the estate (venues, access points, gates, devices) and its live state (devices online, gates open, occupancy, admission rate, failed scans, overrides, alerts) and jumps into the nine topology screens. The pack asks for it to be "highly visual rather than a traditional configuration table", with a venue map showing gate health. The one thing to get right: it is a dashboard of tiles, a map and an alert list (per VO-R02), not the one-row "Every access" table the generator drew.

**Known correction pending (do not draw the wrong version)**

- **Content region is a dataTable "Every access" whose fifteen columns are the KPIs, with a detail panel repeating them** Why: listAccess returns one object of counts; KPIs are tiles on a command centre (VO-R02), and the pack asks for a visual, map-led page. *(source: screens/P08-venue-back-office.yaml#BO-144 / contracts/spine/access.yaml#listAccess; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The read carries no map positions, no AI findings and no alert list** Why: The pack's gate-health map and AI assistant cannot be drawn from listAccess alone; the map needs the BO-150 map with live gate state (listGraphicalAccessMap serves BO-256) and the findings need a source. *(source: screens/P08-venue-back-office.yaml#BO-145 / contracts/spine/access.yaml#listGraphicalAccessMap; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation lists BO-145 to BO-149 only as named triggers; BO-150 to BO-153 are in exitTo without labels** Why: All nine board screens need a labelled tile, in the pack's navigation order. *(source: screens/P08-venue-back-office.yaml#BO-153 / DI-653; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): createAccessPoint is bound as an action of the command centre (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Over what period are Failed scans, Overrides and Security alerts counted - today since the venue day start, or a rolling window?** → Drawn default stands (answer: "Today since the day start, with the delta against the same time last week"): Today since calendarDayStartHour, with the delta against the same time last week. *(decided by Chinmay, 2026-10-02; DEC-226 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every access** (data table, from `listAccess`)

| Shows | Format | Notes |
|---|---|---|
| Total venues | 1,234 | Total venues |
| Active access points | 1,234 | Active access points |
| Entry gates | 1,234 | Entry gates |
| Exit gates | 1,234 | Exit gates |
| Attraction gates | 1,234 | Attraction gates |
| Turnstiles | 1,234 | Turnstiles |
| Handheld devices | 1,234 | Handheld devices |
| Devices online/offline | text | not in the schema: `Devices online/offline` |
| Gates open/closed | text | not in the schema: `Gates open/closed` |
| Current in venue occupancy | 1,234 | Current in-venue occupancy |
| Current admission rate | 12.5% | Admissions per minute across the estate |
| Failed scans | 1,234 | Failed scans |
| Overrides | 1,234 | Overrides |
| Security alerts | 1,234 | Security alerts |
| Synchronization status | chip: In sync, Sync pending, Sync failed | Estate-wide offline sync state of devices |

**The selected access** (detail panel): The pack groups this record's detail under its own headings: “Display hierarchy such as”.

| Shows | Format | Notes |
|---|---|---|
| Total venues | 1,234 | Total venues |
| Active access points | 1,234 | Active access points |
| Entry gates | 1,234 | Entry gates |
| Exit gates | 1,234 | Exit gates |
| Attraction gates | 1,234 | Attraction gates |
| Turnstiles | 1,234 | Turnstiles |
| Handheld devices | 1,234 | Handheld devices |
| Devices online/offline | text | not in the schema: `Devices online/offline` |
| Gates open/closed | text | not in the schema: `Gates open/closed` |
| Current in venue occupancy | 1,234 | Current in-venue occupancy |
| Current admission rate | 12.5% | Admissions per minute across the estate |
| Failed scans | 1,234 | Failed scans |
| Overrides | 1,234 | Overrides |
| Security alerts | 1,234 | Security alerts |
| Synchronization status | chip: In sync, Sync pending, Sync failed | Estate-wide offline sync state of devices |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Estate KPI tiles (first row)**: Total venues, Active access points, Entry gates, Exit gates, Attraction gates, Turnstiles, Handheld devices. Static counts, no delta. Each tile opens the screen that owns the thing counted (access points to BO-148, gates to BO-149, devices to BO-194). *(source: screens/P08-venue-back-office.yaml#BO-144 / contracts/spine/access.yaml#listAccess)*
- **Live KPI tiles (second row)**: Devices online / offline drawn as one tile "142 online, 6 offline" (offline in red when above zero, the pack's separate "Offline devices" bullet is this same number); Gates open / closed as one tile; Current in-venue occupancy (people); Current admission rate as "admissions per minute"; Failed scans, Overrides and Security alerts with today's count since the venue day start. Failed scans and Security alerts turn amber and red above a threshold and open the scan activity and alert lists behind them. *(source: screens/P08-venue-back-office.yaml#BO-145 / contracts/spine/access.yaml#/components/schemas/AccessControlCommandCenterView / DI-623 / DI-625)*
- **Synchronisation status chip**: One estate-wide chip beside the page title - In sync (green), Sync pending (amber), Sync failed (red) - with the count of devices behind it opening the device list filtered to them (BO-194). *(source: contracts/spine/access.yaml#/components/schemas/AccessControlCommandCenterView)*
- **Hierarchy strip**: A breadcrumb-style filter Tenant > Venue > Park > Zone > Attraction > Access point > Gate > Device; choosing a park or zone narrows the tiles and the map. The venue comes from the top-bar switcher (VO-R09). *(source: screens/P08-venue-back-office.yaml#BO-144)*
- **Venue map with gate health**: The graphical map from BO-150 with every gate as a dot coloured by health (green online and open, grey closed, amber degraded or local mode, red offline); clicking a gate opens its lane (BO-149) or device (BO-194). Where no map has been uploaded, show the topology tree instead with "Upload a venue plan" leading to BO-150. *(source: screens/P08-venue-back-office.yaml#BO-145 / DI-623)*
- **AI Access Operations Assistant panel**: A list of advisory findings, each with its evidence and a "Go to" link, never an automatic change (VO-R11): abnormal rejection rate, unusual queue build-up, offline devices, abnormal gate traffic, configuration conflicts, capacity risks, unusual access patterns. Pack example to draw verbatim: "Gate A03 rejection rate is 18.4%, compared with the normal 2.1%. Most failures are caused by an incorrect access-zone assignment." *(source: screens/P08-venue-back-office.yaml#BO-145)*
- **Board tiles**: Nine tiles in the pack's left-navigation order and wording - Venue & Parks, Areas & Zones, Attractions, Access Points, Gates & Lanes, Graphical Map, Location Groups, Operating Calendar, Validate & Publish - each returning here (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-153 / DI-653 / F111 step 1)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open a tile or board screen**: Navigates to BO-145 to BO-153; each returns to this command centre. *(source: F111 step 3 / DI-653)*
- **Add access point**: Draw it as a shortcut that opens the Access Point Directory (BO-148) with a new record, not as a form on the dashboard; the create belongs where access points are listed and edited. *(source: contracts/spine/access.yaml#createAccessPoint)*

**Data it reads**: `listAccess` (onLoad, Access Control Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-145` Venue & Park Access Structure: *Works in Venue & Park Access Structure*; calls `listAccess`
- → `BO-146` Access Area & Zone Builder: *Works in Access Area & Zone Builder*; calls `listAccess`
- → `BO-147` Attraction Access Configuration: *Works in Attraction Access Configuration*; calls `listAccess`
- → `BO-148` Access Point Directory: *Works in Access Point Directory*; calls `listAccess`
- → `BO-149` Gate & Lane Configuration: *Works in Gate & Lane Configuration*; calls `listAccess`
- → `BO-150` Access Control Graphical Map Designer: *Works in Access Control Graphical Map Designer*; calls `listAccess`
- → `BO-151` Access Location Grouping: *Works in Access Location Grouping*; calls `listAccess`
- → `BO-152` Operating Calendar & Special Access Days: *Works in Operating Calendar & Special Access Days*; calls `listAccess`
- → `BO-153` Topology Validation & Publication: *Works in Topology Validation & Publication*; calls `listAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Tenant with several venues**: Total venues only means something at tenant scope; at venue scope (the switcher) show it as "1 of 3 venues" with a link to switch to the tenant view, rather than a lonely "1". *(source: contracts/spine/access.yaml#listAccess)*
- **No devices registered yet (new venue)**: Live tiles show "No devices yet" with "Register a device" leading to BO-196; estate tiles still count access points. *(source: designer default)*
- **Viewer without access configuration rights**: Tiles and map readable; Add access point disabled with "Needs access configuration rights" (VO-R08). *(source: contracts/spine/access.yaml#createAccessPoint)*

#### Consistency with other screens

- Match `BO-194`: Device online/offline, gates open/closed and sync figures must equal the device command centre's tiles at the same moment; same colours.
- Match `BO-224`: Occupancy and admission rate are the same live figures as the Live Operations dashboard; label them identically.
- Match `BO-150`: The map here is the BO-150 map in monitoring mode; one map component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  totalVenues: 2
  activeAccessPoints: 38
  entryGates: 22
  exitGates: 12
  attractionGates: 26
  turnstiles: 64
  handheldDevices: 18
  devicesOnline: 142
  devicesOffline: 6
  gatesOpen: 51
  gatesClosed: 9
  occupancy: 7840
  admissionRate: 46 per min
  failedScans: 312
  overrides: 14
  securityAlerts: 2
  sync: Sync pending
aiFindings:
- Main Plaza Gate 3 rejection rate is 18.4% against a normal 2.1%; most failures are Wrong gate (zone assignment).
- North Entry queue 22 min, 3x the usual for 10:00; 2 of 4 lanes closed.
```

#### Permissions

- `listAccess` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Venue-wide attendance overview (open/closed gates, offline/maintenance status, graphed) and a visual map of all access-control locations across venues/tenants, including entry and exit turnstile layouts that vary by venue. *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-623)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-144` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-144`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 1: Opens Access Control Command Center → Central operational/configuration landing page for the complete Access Control module.
- Flow F111 *Access Control board 1: Access Control Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F111 branch at step 1 (expected): when Nothing has been set up on Access Control Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F111 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-144?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-145`, `BO-146`, `BO-147`, `BO-148`, `BO-149`, `BO-150`, `BO-151`, `BO-152`, `BO-153`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-145` Venue & Park Access Structure

**Define the highest-level physical access hierarchy.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_MANAGE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `orgUnitId` (navigation) |
| Route | `/access-venue/venue-park-access-structure-bo-145` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The physical access hierarchy of a venue (park, zones, gates) as org units: create and amend them so access rules have something to attach to. The structure is binding and nested.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | `listOrgUnits` ?level |
| Include inactive | toggle | off | — | `listOrgUnits` ?includeInactive |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Org unit**: Parent required (tree picker), code unique per venue, kind from the hierarchy levels. *(source: ADR-0011; R108)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create org unit (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listVenueParkAccess` (onLoad, Venue & Park Access Structure); `listOrgUnits` (onLoad, The venue, park and zone tree the access structure hangs …)

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `listVenueParkAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue park access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue park access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue park access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue park access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds SCOPE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: SCOPE_MANAGE for createOrgUnit, updateOrgUnit. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#createOrgUnit)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tree:
- AquaCove Abu Dhabi
- '  Main Gate'
- '  Wave Zone'
- '    Wave Pool Gate'
- '  Lagoon Zone'
```

#### Permissions

- `listVenueParkAccess` → `SCOPE_VIEW` (read) · staff
- `listOrgUnits` → `SCOPE_VIEW` (read) · staff
- `createOrgUnit` → `SCOPE_MANAGE` (configure) · staff
- `updateOrgUnit` → `SCOPE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.41 | Venue-Specific Policies - System shall support venue-specific access policies. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 3.3.43 | Policy Inheritance - System shall support inheritance of policies across organizational structures. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 7.1.13 | The system shall support permission assignment at company, department, venue, park, attraction, facility, event, sales channel, POS terminal, and product levels. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.27 | The system shall support management of companies, business units, departments, parks, venues, attractions, facilities, cost centers, and reporting structures. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.37 | Allow administrators to restrict access by venue, park, facility, attraction, sales channel, POS terminal, country, region, IP address and network range. Policies should support allow/deny logic and … | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.52 | Support policies spanning multiple parks, venues, attractions, departments and business units while maintaining centralized governance. | F&B POS | CONTRACTED | `listOrgUnits` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-145` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-145`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 2: Works in Venue & Park Access Structure → Define the highest-level physical access hierarchy.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-145?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create org unit, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `SCOPE_MANAGE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-146` Access Area & Zone Builder

**Divide a venue into controlled access areas.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-area-zone-builder-bo-146` |

**What the spec says about it.** **Zone security classification: Public, Restricted, Secure, Critical, renamable (decided 2 October 2026 by Chinmay, DEC-227; CHG-CSP-025, `securityClassificationLevel`).**

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists access areas and zones (setAccessAreaZone has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Divides a venue into controlled areas - public, ticketed, VIP, staff, back-of-house, attraction, restricted, fast pass, event and temporary zones - each with a capacity, operating schedule, security classification, entry and exit requirements and the credential classes it admits. The pack asks for zones dragged onto a graphical venue structure. The one thing to get right: a zone is a node of the one venue tree (venue > park > zone > attraction > access point) that other screens pick from, so draw a tree with a zone editor, not a free form.

**Known correction pending (do not draw the wrong version)**

- **zoneId and venueId are required in the write** Why: A new zone has no id yet and the venue is the session's (VO-R03). *(source: contracts/spine/access.yaml#setAccessAreaZone; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **operatingSchedule, securityClassification, entryRequirements and exitRequirements are free strings** Why: They need references (calendar, rule) or a closed set to be enforced at a gate. *(source: contracts/spine/access.yaml#setAccessAreaZone; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Zones exist twice - as org units (BO-064, createOrgUnit) and as access areas (setAccessAreaZone, AccessDevicePlacement.accessAreaId)** Why: Two zone models mean two trees, with placements pointing at one while rules point at the other; decide one source of zone nodes. *(source: contracts/spine/tenancy.yaml#createOrgUnit / contracts/spine/access.yaml#/components/schemas/AccessDevicePlacement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Content region is two buttons (Save changes, Cancel) and nothing else; no read is bound (CHG-WIR-004)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What are the security classification levels for a zone?** → Zone security classification levels: Public / Restricted / Secure / Critical (renamable). *(decided by Chinmay, 2026-10-02; DEC-227 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Form: Save zone** (modal, opened by *Save zone*; *Save zone* calls `setAccessAreaZone`, *Cancel* sends nothing)

**Collects what `setAccessAreaZone` sends before it is called.** Required: `zoneId`, `venueId`, `name`, `zoneType`. Optional: `capacity`, `operatingSchedule`, `securityClassification`, `securityClassificationLevel`, `entryRequirements`, `exitRequirements`, `allowedCredentialClasses`, `parentId`. The classification level is one of the four, shown with the venue's labels. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | — | — | Zone name, e.g. | `setAccessAreaZone` body |
| Venue `venueId` | text field | required | — | — | — | Venue the zone belongs to | `setAccessAreaZone` body |
| Zone `zoneId` | text field | required | — | — | — | Zone being written | `setAccessAreaZone` body |
| Zone type `zoneType` | select | required | — | Public · Ticketed · Vip · Staff · Back of house · Attraction · Restricted · Fast pass · Event · Temporary | — | Vocabulary listed under Create. | `setAccessAreaZone` body |
| Capacity `capacity` | number field | optional | — | — | — | capacity | `setAccessAreaZone` body |
| Operating schedule `operatingSchedule` | text field | optional | — | — | — | operating schedule | `setAccessAreaZone` body |
| Security classification `securityClassification` | text field | optional | — | — | — | The venue's label for the classification level, renamable (DEC-227; CHG-CSP-025) | `setAccessAreaZone` body |
| Security classification level `securityClassificationLevel` | radio group | optional | — | Public · Restricted · Secure · Critical | — | Public, Restricted, Secure or Critical (decided 2 October 2026, Chinmay, BO-146; DEC-227; CHG-CSP-025); the label shown is `securityClassification` | `setAccessAreaZone` body |
| Entry requirements `entryRequirements` | text field | optional | — | — | — | entry requirements | `setAccessAreaZone` body |
| Exit requirements `exitRequirements` | text field | optional | — | — | — | exit requirements | `setAccessAreaZone` body |
| Allowed credential classes `allowedCredentialClasses` | list of values (chips) | optional | — | — | — | Credential classes admitted to the zone | `setAccessAreaZone` body |
| Parent `parentId` | text field | optional | — | — | — | Park or zone this zone sits under in the venue structure | `setAccessAreaZone` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **zoneType**: Required single choice of the ten pack types (Public, Ticketed, VIP, Staff, Back-of-house, Attraction, Restricted, Fast Pass, Event, Temporary) as a coloured chip on the tree node; the colour is reused on the map (BO-150) and in every zone picker. *(source: screens/P08-venue-back-office.yaml#BO-146 / screens/P08-venue-back-office.yaml#BO-147 / contracts/spine/access.yaml#setAccessAreaZone)*
- **name**: Required, staff-facing, with Arabic variant (VO-R10), e.g. "VIP Lounge". *(source: contracts/spine/access.yaml#setAccessAreaZone)*
- **parentId**: Set by dragging the zone under a park or another zone in the tree; a zone cannot be dropped inside itself or its own children. A Temporary or Event zone shows its schedule dates on the node. *(source: screens/P08-venue-back-office.yaml#BO-147 / contracts/spine/access.yaml#setAccessAreaZone)*
- **capacity**: Whole number of people, empty means no zone limit; show the sum of child zone capacities beside it and warn if the children exceed the parent (the "capacity inconsistencies" check of BO-153). *(source: screens/P08-venue-back-office.yaml#BO-153 / contracts/spine/access.yaml#setAccessAreaZone)*
- **operatingSchedule**: Pick from the venue's operating calendar (BO-152) - "Park hours", "Event dates only" - never typed text. *(source: contracts/spine/access.yaml#setAccessAreaZone)*
- **allowedCredentialClasses**: Multi-select chips (Ticket, Membership, Pass, Accreditation credential, Staff) - the credential types the rule builder uses; empty means "Any valid credential" and must say so. *(source: screens/P08-venue-back-office.yaml#BO-155 / contracts/spine/access.yaml#setAccessAreaZone)*
- **entryRequirements / exitRequirements / securityClassification**: The write holds these as free text. Draw entry and exit requirements as links to the admission profile or rule that governs the zone (BO-032 / BO-155), and security classification as a select: Public, Restricted, Secure, Critical (the venue may rename them). *(source: contracts/spine/access.yaml#setAccessAreaZone / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **zoneId, venueId**: Not inputs; the server assigns the id and the venue is the session's (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Zone tree over the venue structure**: Left, the tree Venue > Park > Zone (nested) with type chip, capacity and the count of access points inside; right, the selected zone's editor. The pack's example structure (Main Park > Public Plaza, Paid Park Area, VIP Lounge, Attraction Cluster A, Back of House) is the shape to mock. *(source: screens/P08-venue-back-office.yaml#BO-147)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add zone / drag zone**: Creates or moves the zone (whole-record upsert, VO-R04); moving a zone moves its access points and attractions with it and the confirmation says how many. *(source: contracts/spine/access.yaml#setAccessAreaZone)*
- **Save zone**: Sends every field; "Last changed by" shown after save (VO-R05). *(source: contracts/spine/access.yaml#setAccessAreaZone)*

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `setAccessAreaZone`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access area zone list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access area zone untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access area zone yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access area zone are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Zone with access points or devices in it is retyped or moved**: Confirmation lists the access points and device placements affected; rules that name the zone keep working because they reference the zone, not its position. *(source: contracts/spine/access.yaml#/components/schemas/AccessDevicePlacement)*
- **Two zones with the same name under one park**: Refused against the name field. *(source: designer default)*

#### Consistency with other screens

- Match `BO-064`: Zones & Areas (BO-064) builds the same venue tree from org units; the access board must not show a second, different zone tree. One tree component, one set of nodes.
- Match `BO-145`: Venue & Park Access Structure supplies the venue and park levels this tree hangs from.
- Match `BO-150`: Zones drawn on the graphical map and zones in this tree are the same records, same colours.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
zones:
- name: Public Plaza
  type: Public
  parent: Aqua Park
  capacity: ''
  accessPoints: 0
- name: Paid Park Area
  type: Ticketed
  parent: Aqua Park
  capacity: 9000
  accessPoints: 6
- name: VIP Lounge
  type: VIP
  parent: Paid Park Area
  capacity: 120
  credentials: Pass, Membership
- name: Wave Rider Cluster
  type: Attraction
  parent: Paid Park Area
  capacity: 1400
- name: Back of House
  type: Back-of-house
  parent: Aqua Park
  credentials: Staff
```

#### Permissions

- `setAccessAreaZone` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-146` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-146`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 4: Works in Access Area & Zone Builder → Divide a venue into controlled access areas.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-146?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-147` Attraction Access Configuration

**Configure attractions as access-controlled destinations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `accessPointId` (navigation) |
| Route | `/access-venue/attraction-access-configuration-bo-147` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists attraction access records (setAttractionAccess has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Makes an attraction (a ride or show such as Falcon Coaster) an access-controlled destination with its own entry and exit points, capacity and eligibility (height, age, adult companion, membership, VIP, entitlement, biometric), independently of the park ticket. The one thing to get right: eligibility reads as the pack's sentence - "Height >= 130 cm AND Valid Park Admission AND Ride Entitlement Available" - so a supervisor can see why a rider will be refused, and every condition maps to a deny reason the scanner shows.

**Known correction pending (do not draw the wrong version)**

- **venue, zone, entitlementRequirement, operatingCalendar and temporaryClosureBehavior are free strings; attractionId required** Why: Venue is session scope; zone, entitlement and calendar are references; closure behaviour is a closed set; a new record cannot supply its own id. *(source: contracts/spine/access.yaml#/components/schemas/AttractionAccessConfigurationInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write-only (setAttractionAccess) with no read; content region is only Save and Cancel (CHG-WIR-004)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What should an access point do when its attraction is temporarily closed - deny, offer a virtual queue return window, or refer to an operator?** → An access point whose attraction is temporarily closed denies, shows the reopening time, and offers a virtual-queue return window where enabled. *(decided by Chinmay, 2026-10-02; DEC-228 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Form: Close temporarily** (modal, opened by *Close temporarily*; *Close temporarily* calls `updateAccessPoint`, *Cancel* sends nothing)

**Collects what `updateAccessPoint` sends before it is called.** Nothing in the body is required. Optional: `name`, `direction`, `antiPassbackEnabled`, `requiresExitBeforeReentry`, `isActive`, `driver`, `temporaryClosure`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateAccessPoint` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `updateAccessPoint` body |
| Anti passback enabled `antiPassbackEnabled` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Driver `driver` | text field | optional | — | — | — | Driver identifier for the controller behind this access point. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific. | `updateAccessPoint` body |
| Temporary closure `temporaryClosure` | group | optional | — | — | — | Close or reopen the access point's attraction for a while (`AccessPoint.temporaryClosure`; DEC-228; CHG-CSP-026). | `updateAccessPoint` body |
| Is closed `temporaryClosure.isClosed` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Reason `temporaryClosure.reason` | text area | optional | — | max length 200 | — | — | `updateAccessPoint` body |
| Reopens at `temporaryClosure.reopensAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessPoint` body |
| Offer virtual queue return `temporaryClosure.offerVirtualQueueReturn` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Queue `temporaryClosure.queueId` | picker: choose a queue | optional | — | — | shows names, sends the id | — | `updateAccessPoint` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **attraction (attractionId, name)**: Pick an existing attraction from the venue's attraction list (the same records the games, rides and queue screens use); name is shown read-only from it with its Arabic variant. Never typed as an id. *(source: contracts/spine/access.yaml#setAttractionAccess)*
- **venue / zone**: Venue from the top-bar switcher (VO-R09), not an input; zone picked from the zone tree of BO-146. *(source: contracts/spine/access.yaml#setAttractionAccess)*
- **entryPoints / exitPoints**: Multi-select of access points filtered by direction (entry or re-entry for entry points, exit for exit points); at least one entry point before the attraction can be published. *(source: screens/P08-venue-back-office.yaml#BO-147 / contracts/spine/access.yaml#setAttractionAccess)*
- **heightRestriction / ageRestriction**: "Minimum height [130] cm" and "Minimum age [ ] years", whole numbers, empty = no limit. Height needs a sensor on the reader (BO-199) or an operator check; say so under the field. *(source: screens/P08-venue-back-office.yaml#BO-148 / contracts/spine/access.yaml#setAttractionAccess / contracts/spine/access.yaml#setReaderScannerPeripheral)*
- **adultCompanionRequirement**: Toggle "Must be accompanied by an adult"; when on, link to the companion rules (BO-161) that define who qualifies, rather than a second definition here. *(source: contracts/spine/access.yaml#setAttractionAccess / DI-628 / MATRIX 7.4.22)*
- **fastPassSupport / membershipAccess / vipAccess / biometricRequirement**: Toggles grouped as "Who has a lane"; biometric links to the biometric profile (BO-185) that sets where a face is required. *(source: contracts/spine/access.yaml#setAttractionAccess)*
- **entitlementRequirement**: Select from entitlement types (Ride, Attraction admission, Fast Pass, Experience) as the consumption engine (BO-159) names them, not free text. *(source: contracts/spine/access.yaml#setAttractionAccess / contracts/spine/access.yaml#setEntitlementConsumption)*
- **operatingCalendar / temporaryClosureBehavior**: Calendar as a link to the attraction's operating days on BO-152 (Day/Week/Month per VO-R01); closure behaviour: deny with "Attraction temporarily closed" and the reopening time, plus a virtual-queue return window where the attraction has one enabled. *(source: contracts/spine/access.yaml#setAttractionAccess / designer default / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Close temporarily (secondary button) | `updateAccessPoint` PATCH `/access-points/{accessPointId}` | inline | AccessPoint | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Eligibility sentence**: Above the form, the conditions joined with AND in the pack's layout, updating as fields change. *(source: screens/P08-venue-back-office.yaml#BO-148)*
- **Attraction list (left)**: Name, zone, entry/exit points (counts), capacity, height/age limits, Fast Pass yes/no, status Open / Temporarily closed. *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save attraction access**: Whole-record upsert (VO-R04); applies at gates after the next package / publication (BO-153). *(source: contracts/spine/access.yaml#setAttractionAccess)*

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `setAttractionAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attraction access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Height limit set but no reader at the entry point has a height sensor**: Warn "Height will be checked by the operator (yellow outcome)" before save. *(source: contracts/spine/access.yaml#setReaderScannerPeripheral)*
- **Attraction temporarily closed while guests hold virtual queue return windows**: The closure confirmation states how many return windows are affected. *(source: designer default)*

#### Consistency with other screens

- Match `SCN-003`: Each condition corresponds to a deny reason - Below minimum height, Below minimum age, Child needs an accompanying adult, No ride entitlement (VO-R06).
- Match `BO-001`: Attractions here are the same records the queue directory shows wait times for (games-module meaning of attraction, DI-863).
- Match `BO-159`: The entitlement requirement names the entitlement type the engine consumes at this attraction.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
attractions:
- name: Falcon Coaster
  zone: Attraction Cluster A
  entry: Falcon Entry, Falcon Fast Pass
  exit: Falcon Exit
  capacity: 24
  height: 130 cm
  companion: Under 12
  fastPass: true
  eligibility: Height >= 130 cm AND Valid park admission AND Ride entitlement available
- name: Wave Rider
  zone: Paid Park Area
  height: 120 cm
  age: 8
  fastPass: false
```

#### Permissions

- `setAttractionAccess` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `updateAccessPoint` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-147` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-147`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 6: Works in Attraction Access Configuration → Configure attractions as access-controlled destinations.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-147?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Close temporarily, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-148` Access Point Directory

**Create the logical access points where validation occurs. An Access Point is different from a physical reader/device.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Additional settings) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `accessPointId` (navigation) |
| Route | `/access-venue/access-point-directory-bo-148` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The directory of logical access points - the places where a scan is judged (Main Entrance North), each grouping several physical gates and devices (Gate N01-N03, Accessible Gate N04). It is where an access point is created, typed, put in a zone and given its fixed direction. The one thing to get right: the access point is not the device; show the point with its gates and devices beneath it, and keep the live mode (set by the podium) separate from the configuration (set here).

**Known correction pending (do not draw the wrong version)**

- **The pack's 13 access point types, zone, capacity, schedule, ticket categories and fallback behaviour are not on AccessPoint** Why: The schema holds code, name, direction, anti-passback, exit-before-re-entry, driver, mode, geofence; the pack's configuration has nowhere to be stored. *(source: screens/P08-venue-back-office.yaml#BO-149 / contracts/spine/access.yaml#/components/schemas/AccessPoint; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Direction has no Entry/Exit (bidirectional) value** Why: The pack's type list and the lane screen (BO-149, direction bidirectional) both need it; a point and its lanes cannot disagree. *(source: contracts/spine/access.yaml#/components/schemas/AccessPoint / contracts/spine/access.yaml#setGateLane; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Fields drawn as selectFields (capacity, operating schedule, default mode)** Why: Capacity is a number, schedule a calendar link, default mode a select of the operating modes. *(source: screens/P08-venue-back-office.yaml#BO-148; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The screen binds only listAccessPoints and six unbound selectFields; there is no create or update (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| operating schedule | select field | — | — | — | — | — | — |
| allowed direction | select field | — | — | — | — | — | — |
| capacity | select field | — | — | — | — | — | — |
| default mode | select field | — | — | — | — | — | — |
| associated zone | select field | — | — | — | — | — | — |
| allowed ticket categories | select field | — | — | — | — | — | — |

**Form: Add access point** (modal, opened by *Add access point*; *Add access point* calls `createAccessPoint`, *Cancel* sends nothing)

**Collects what `createAccessPoint` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createAccessPoint` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createAccessPoint` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createAccessPoint` body |
| Direction `direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `createAccessPoint` body |
| Anti passback enabled `antiPassbackEnabled` | toggle | optional | off | — | — | — | `createAccessPoint` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `createAccessPoint` body |
| Driver `driver` | text field | optional | — | — | — | — | `createAccessPoint` body |

Errors to draw in the form: 400 Validation failed

**Form: Save access point** (modal, opened by *Save access point*; *Save access point* calls `updateAccessPoint`, *Cancel* sends nothing)

**Collects what `updateAccessPoint` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateAccessPoint` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `updateAccessPoint` body |
| Anti passback enabled `antiPassbackEnabled` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Driver `driver` | text field | optional | — | — | — | Driver identifier for the controller behind this access point. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific. | `updateAccessPoint` body |
| Temporary closure `temporaryClosure` | group | optional | — | — | — | Close or reopen the access point's attraction for a while (`AccessPoint.temporaryClosure`; DEC-228; CHG-CSP-026). | `updateAccessPoint` body |
| Is closed `temporaryClosure.isClosed` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Reason `temporaryClosure.reason` | text area | optional | — | max length 200 | — | — | `updateAccessPoint` body |
| Reopens at `temporaryClosure.reopensAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessPoint` body |
| Offer virtual queue return `temporaryClosure.offerVirtualQueueReturn` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Queue `temporaryClosure.queueId` | picker: choose a queue | optional | — | — | shows names, sends the id | — | `updateAccessPoint` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name / code**: Name (max 200, Arabic variant) and code (max 64, upper-case, e.g. MAIN-N); code unique in the venue. *(source: contracts/spine/access.yaml#createAccessPoint)*
- **Access point type**: The pack's closed list as cards - Main entry, Exit, Entry/Exit, Re-entry, Crossover, Attraction entry, Fast Pass, VIP, Staff, Accessible/POD, Group, Event, Temporary. The contract has only direction (see corrections); draw type and direction as two fields. *(source: screens/P08-venue-back-office.yaml#BO-148 / screens/P08-venue-back-office.yaml#BO-149)*
- **direction**: Entry, Exit, Re-entry, Crossover - fixed per access point and changed only here, never by the podium (R221). Changing it on a point with gates in use asks for confirmation naming the gates and profiles affected. *(source: contracts/spine/access.yaml#/components/schemas/AccessPoint / R221)*
- **antiPassbackEnabled / requiresExitBeforeReentry**: Two toggles under "Sharing protection", default off; a hint says the time window and sequence are set in Anti-Passback & Journey Sequence (BO-157). *(source: contracts/spine/access.yaml#createAccessPoint)*
- **associated zone, capacity, operating schedule, allowed ticket categories, fallback behaviour, default mode**: Pack fields: zone from the BO-146 tree; capacity in people; schedule as a link to BO-152; ticket categories as chips; fallback behaviour (what the point does when its devices are offline) as a closed choice (Validate offline, Podium validation, Close). Default mode is the normal operating mode at opening; the live mode is shown read-only with "Set by the podium". *(source: screens/P08-venue-back-office.yaml#BO-149 / contracts/spine/access.yaml#setTurnstileMode)*
- **driver**: Select from the supported controller drivers (OSDP first), not free text. *(source: contracts/spine/access.yaml#/components/schemas/AccessPoint / ADR-0015)*
- **id, venueId, scopePath**: Not inputs (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add access point (secondary button) | `createAccessPoint` POST `/access-points` | CreateAccessPointRequest | AccessPoint | 400 Validation failed | opens modal first |
| Save access point (secondary button) | `updateAccessPoint` PATCH `/access-points/{accessPointId}` | inline | AccessPoint | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Access point list**: Grouped by zone; columns Name, Code, Type, Direction icon, Gates (count), Devices (online / total), Live mode chip in the gate-mode colours, Active. Reference list, normal paging allowed (VO-R12). *(source: contracts/spine/access.yaml#listAccessPoints)*
- **Point detail**: The fields above plus its gates and lanes (from BO-149) and placed devices (from BO-196) as a small tree, as in the pack's Main Entrance North example. *(source: screens/P08-venue-back-office.yaml#BO-148)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New access point**: Creates with no id; required name, code, direction; success opens the point to add gates. *(source: contracts/spine/access.yaml#createAccessPoint)*
- **Save access point**: Replaces the point's configuration; changes reach gates after publication (BO-153). *(source: contracts/spine/access.yaml#updateAccessPoint)*
- **Deactivate**: Sets isActive false after a confirmation naming gates, devices and admission profiles that reference it; never a hard delete. *(source: contracts/spine/access.yaml#/components/schemas/AccessPoint)*

**Data it reads**: `listAccessPoints` (onLoad, List access points)

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `listAccessPoints`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access point configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access point untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access point configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Access point with no gates or devices**: Row flagged "No gate" (amber); BO-153 reports it as missing reader/device association. *(source: screens/P08-venue-back-office.yaml#BO-153)*
- **Code already used**: Inline error on code; nothing else lost. *(source: contracts/spine/access.yaml#createAccessPoint)*

#### Consistency with other screens

- Match `BO-144`: The command centre's Add access point opens this screen.
- Match `BO-064`: Same access point record, direction set in one place only (R221); same labels and segmented direction control.
- Match `BO-032`: Admission profiles pick these access points in "Where it is valid"; same names and codes.
- Match `SCN-016`: The live mode chip uses the podium's mode names and colours.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
accessPoints:
- name: Main Entrance North
  code: MAIN-N
  type: Main entry
  direction: Entry
  zone: Public Plaza
  gates: 4
  devices: 6 / 6
  mode: Normal
- name: Main Plaza Exit
  code: MAIN-X
  type: Exit
  direction: Exit
  gates: 3
  mode: Normal
- name: Aqua to Summit Crossover
  code: XO-AS
  type: Crossover
  direction: Crossover
  gates: 2
  mode: Closed
```

#### Permissions

- `listAccessPoints` → `SCOPE_VIEW` (read) · staff
- `createAccessPoint` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `updateAccessPoint` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.60 | Check-in / Check-out entitlement control | Ticketing Catalogue | CONTRACTED | `createAccessPoint` |
| 3.2.11 | The system should be able to define and configure all access control rules, all gates (entrances of access-control areas), access points and locations (a group of areas). | Admission and Access | CONTRACTED | `createAccessPoint` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*
- Tiered access (e.g. Bronze/Silver/Gold): the client fills a matrix of which gates/attractions each tier may scan into; configured as location → admission profile → gate → access point, with explicit deny rules (e.g. Gold denied at the Silver/Bronze entrance). *(agreed · MoM 7 Aug 2026, 24. Tiered Ticketing & Access Control Deep Dive · DI-185)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-148` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-148`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 8: Works in Access Point Directory → Create the logical access points where validation occurs. An Access Point is different from a physical reader/device.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-148?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add access point, Save access point.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-149` Gate & Lane Configuration

**Configure individual physical gates/lanes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/gate-lane-configuration-bo-149` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists gates and lanes (setGateLane has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Configures each physical gate or lane under an access point (Gate N01-N03, Accessible Gate N04): its lane number, type (standard, VIP, Fast Pass, accessible, group, staff, attraction), size (wide lanes for buggies and wheelchairs) and default mode. The pack's acceptance condition is that every lane can be configured on its own "while inheriting settings from its parent access point". The one thing to get right: inherited values are visibly inherited, and overriding one is a deliberate act.

**Known correction pending (do not draw the wrong version)**

- **Lane direction can be set per lane (entry, exit, bidirectional) while R221 fixes direction per access point** Why: Two places decide direction; either the lane override is allowed and the validator judges by lane, or the field is read-only inherited. *(source: contracts/spine/access.yaml#setGateLane / R221 / contracts/spine/access.yaml#/components/schemas/AccessPoint; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **gateId required and accessPoint and location are free strings** Why: A new lane has no id (VO-R03); the access point is a reference; location follows from the access point. *(source: contracts/spine/access.yaml#/components/schemas/GateLaneConfigurationInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write-only screen (setGateLane) with no read; content is only Save and Cancel (CHG-WIR-004)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **accessPoint / gateName / laneNumber**: Access point picked from BO-148 (never typed); gate name (Arabic variant) and lane number shown together as "N04 - Lane 4". Location is the access point's zone, shown read-only. *(source: contracts/spine/access.yaml#setGateLane)*
- **direction**: Shown as "Inherited: Entry (from Main Entrance North)" with an Override switch; when overridden, Entry / Exit / Bidirectional. Re-entry and Crossover are the two lane flags below, not directions. *(source: screens/P08-venue-back-office.yaml#BO-149 / contracts/spine/access.yaml#setGateLane / R221)*
- **reEntry / crossover**: Two toggles "Lane accepts re-entry scans" and "Crossover lane between parks"; crossover only offered when the venue has more than one park. *(source: contracts/spine/access.yaml#setGateLane)*
- **type**: Chips Standard, VIP, Fast Pass, Accessible, Group, Staff, Attraction - one per lane. *(source: screens/P08-venue-back-office.yaml#BO-149 / contracts/spine/access.yaml#setGateLane)*
- **operationalMode (default)**: Select of the operating modes with the pack's word as helper text: Normal ("Validation"), Free flow ("Free spin" / "Count only"), Drop arm ("Emergency"), Closed, Podium ("Manual"), Maintenance. This is the lane's default at opening; the podium changes it live (SCN-016). *(source: screens/P08-venue-back-office.yaml#BO-150 / contracts/spine/access.yaml#setGateLane / R221)*
- **laneSize**: Standard / Wide; Wide shows a wheelchair-and-buggy icon in every gate list. *(source: screens/P08-venue-back-office.yaml#BO-150 / contracts/spine/access.yaml#setGateLane / MATRIX 3.2.28)*
- **gateId, scopePath**: Not inputs on create (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lanes by access point**: Tree Access point > lanes, each lane row with lane number, type chip, size icon, direction (inherited in grey italic, overridden in bold), default mode chip and the device(s) mounted on it (from BO-196). *(source: screens/P08-venue-back-office.yaml#BO-150 / designer default)*
- **Inheritance panel**: For the selected lane, a two-column view "Access point value / This lane" for each inheritable setting, with Reset to inherited. *(source: screens/P08-venue-back-office.yaml#BO-150)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save lane**: Whole-record upsert (VO-R04); takes effect after publication (BO-153). *(source: contracts/spine/access.yaml#setGateLane)*
- **Reset to inherited**: Clears the lane override for that setting; the save sends the cleared value. *(source: designer default)*

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `setGateLane`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gate lane list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gate lane untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gate lane yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gate lane are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Lane direction overridden to Exit on an Entry access point**: Warn that admission profiles and journey rules judge by the access point, and BO-153 lists it under "incorrect entry/exit direction". *(source: screens/P08-venue-back-office.yaml#BO-153 / R221)*
- **Lane with no device mounted**: Flagged "No reader" and reported by BO-153 as missing reader/device association. *(source: screens/P08-venue-back-office.yaml#BO-153)*

#### Consistency with other screens

- Match `BO-197`: Turnstile behaviour (unlock duration, pass-through timeout) is set per access point there; mode names identical.
- Match `SCN-016`: Live mode changes made at the podium show here as "Live now - Free flow, set by Rahul Menon 10:42".

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
lanes:
- accessPoint: Main Entrance North
  gate: N01 - Lane 1
  type: Standard
  size: Standard
  direction: Entry (inherited)
  mode: Normal
- accessPoint: Main Entrance North
  gate: N04 - Lane 4
  type: Accessible
  size: Wide
  direction: Entry (inherited)
  mode: Normal
- accessPoint: Main Plaza Gate 3
  gate: G3 - Lane 2
  type: Fast Pass
  size: Standard
  direction: Bidirectional (overridden)
  reEntry: true
```

#### Permissions

- `setGateLane` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-149` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-149`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 10: Works in Gate & Lane Configuration → Configure individual physical gates/lanes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-149?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-150` Access Control Graphical Map Designer

**Create a graphical digital twin of the access-control environment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-control-graphical-map-designer-bo-150` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of the saved access map (setAccessGraphicalMap has no get), and no operation accepts an AI-proposed topology.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The graphical digital twin of the access estate and, per the pack, "one of the visually strongest TICVAI screens": the administrator uploads a CAD, PDF, image or venue plan, AI proposes entrances, exits, gates, attractions, zones and pathways, and the administrator drags gates, turnstiles, scanners, beacons, cameras, RFID readers and face devices onto the map; clicking a device opens its configuration. The one thing to get right: AI proposes, the person accepts - nothing is created until "Create the proposed topology" is confirmed.

**Known correction pending (do not draw the wrong version)**

- **A separate access drawing is uploaded with setAccessGraphicalMap while the venue-map contract already imports geometry, proposes labels with AI and publishes the map** Why: Two venue maps would drift; reuse importVenueGeometry, acceptVenueLabelProposals, setVenuePoint and publishVenueMap. *(source: contracts/satellite/venue-map.yaml#importVenueGeometry / contracts/satellite/venue-map.yaml#acceptVenueLabelProposals; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Device placements carry no map position** Why: AccessDevicePlacement has area, access point and lane but no coordinates, so a dragged device cannot be saved where it was dropped. *(source: contracts/spine/access.yaml#/components/schemas/AccessDevicePlacement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **mapId and venueId are required in the write** Why: Server-owned / session (VO-R03). *(source: contracts/spine/access.yaml#setAccessGraphicalMap; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Screen is Save changes and Cancel only; no read of the map (CHG-WIR-004)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **sourceFileType / sourceFile**: Upload drop zone accepting CAD, PDF, image, venue plan or architectural drawing; the type is detected from the file and confirmed, not chosen first. *(source: screens/P08-venue-back-office.yaml#BO-150 / contracts/spine/access.yaml#setAccessGraphicalMap)*
- **Device palette**: Left palette in the pack's order - Gate, Turnstile, Scanner, Beacon, Camera, RFID reader, Face recognition device. Dropping an item asks which registered device (BO-196) or access point (BO-148) it is; an unregistered drop stays a dashed "planned" marker. *(source: screens/P08-venue-back-office.yaml#BO-150 / contracts/spine/access.yaml#placeAccessDevice)*
- **mapId, venueId**: Not inputs; one map per venue from the session (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Canvas**: The drawing as base layer; zones as translucent shapes in the zone-type colours (BO-146); access points as pins with direction arrows; devices as icons with health dots; pathways as lines. Layer toggles (Zones, Access points, Devices, Beacons, Pathways). Works right-to-left in Arabic (VO-R10). *(source: screens/P08-venue-back-office.yaml#BO-150)*
- **AI proposal**: After upload, a banner "I detected 14 likely access lanes and 3 emergency exits. Create the proposed topology?" with the proposed items drawn dashed; Accept all, Accept selected, Discard (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-151)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Accept proposed topology**: Creates the accepted access points and zones; confirmation lists what will be created by type. *(source: contracts/spine/access.yaml#setAccessGraphicalMap)*
- **Click a device or access point**: Opens its configuration (getAccessPoint / the placement) in a side panel. *(source: screens/P08-venue-back-office.yaml#BO-150 / contracts/spine/access.yaml#getAccessPoint)*
- **Save map**: Whole-record upsert (VO-R04). *(source: contracts/spine/access.yaml#setAccessGraphicalMap)*

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `setAccessGraphicalMap`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access graphical map list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access graphical map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access graphical map yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access graphical map are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Upload that cannot be read (scanned photo, unsupported CAD version)**: The drawing still becomes the base layer; AI reports "Nothing detected" and manual placement continues. *(source: designer default)*
- **Device dropped where no access point exists**: Prompt to create the access point first or attach to the nearest one (an orphan device is a BO-153 finding). *(source: screens/P08-venue-back-office.yaml#BO-153)*

#### Consistency with other screens

- Match `BO-093`: Venue map import with AI label proposals (importVenueGeometry, acceptVenueLabelProposals) already exists for the venue map; this designer must use the same map, not a second drawing.
- Match `BO-256`: The live map (gate performance) is this map with live data; same pins and colours.
- Match `BO-168`: Beacons placed here are the beacon registry's records.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
upload:
  file: Aqua-Park-site-plan-2026.pdf
  type: PDF
  detected: 14 access lanes, 3 emergency exits, 6 zones, 9 attractions
placed:
- Main Plaza Gate 1 - TRN-01 (online)
- Main Entrance Beacon 1
- Falcon Coaster Entry - face camera FC-02
```

#### Permissions

- `setAccessGraphicalMap` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Venue-wide attendance overview (open/closed gates, offline/maintenance status, graphed) and a visual map of all access-control locations across venues/tenants, including entry and exit turnstile layouts that vary by venue. *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-623)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-150` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-150`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 12: Works in Access Control Graphical Map Designer → Create a graphical digital twin of the access-control environment.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-150?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-151` Access Location Grouping

**Group multiple access points for operational and capacity purposes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20671 (APP-SETUP-BO-151) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `groupId` (navigation) |
| Route | `/access-venue/access-location-grouping-bo-151` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Groups access points into named, nestable groups (Main Entrance = Gates 01-04; Adventure Zone = Coaster, Drop Tower, Adventure Hall gates) whose scans roll up into one occupancy, entries, exits and throughput figure. Gate mode policies and capacity rules then name a group instead of individual gates. The one thing to get right: a tree with live roll-up numbers, so the manager sees why a group exists.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The content region is an unbound empty table and the read's roll-up figures are absent (CHG-SBO-005)
- Request body requires id and scopePath (CHG-SBO-005)

#### Inputs: what the user enters or picks

**Form: Save access point group** (modal, opened by *Save access point group*; *Save access point group* calls `setAccessPointGroup`, *Cancel* sends nothing)

**Collects what `setAccessPointGroup` sends before it is called.** Required: `id`, `venueId`, `name`, `scopePath`. Optional: `parentGroupId`, `accessPointIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setAccessPointGroup` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setAccessPointGroup` body |
| Name `name` | text field | required | — | — | — | Group name, e.g. | `setAccessPointGroup` body |
| Parent group `parentGroupId` | picker: choose a parent group | optional | — | — | shows names, sends the id | Enclosing group, for nested groups | `setAccessPointGroup` body |
| Access points `accessPointIds` | multi-picker: choose access points | optional | — | — | — | Member access points (access.access_point) | `setAccessPointGroup` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setAccessPointGroup` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `group-cycle`: the parent named would make the group its own ancestor.; 422 A member access point is not in the group's venue.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name**: Required; staff-facing, Arabic variant (VO-R10); e.g. "Main Entrance". *(source: contracts/spine/access.yaml#setAccessPointGroup)*
- **parentGroupId**: "Inside group" picker limited to groups of the same venue; a group cannot be placed inside itself or its own children. *(source: screens/P08-venue-back-office.yaml#BO-151 / contracts/spine/access.yaml#setAccessPointGroup)*
- **accessPointIds**: Pick from the venue topology tree (park > zone > access point). Show direction icons so a group mixing entry and exit gates is visible (entries and exits both roll up). *(source: screens/P08-venue-back-office.yaml#BO-151 / contracts/spine/access.yaml#/components/schemas/AccessAccessPointGroup)*
- **id, venueId, scopePath, timestamps**: Not inputs (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Access-point groups** (data table, from `listAccessLocationGrouping`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | Group name, e.g. |
| Parent group | text | Enclosing group, for nested groups |
| Access points | list or chips (count when long) | Access points whose counts roll up into this group |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save access point group (primary button) | `setAccessPointGroup` PUT `/access-point-groups` | AccessAccessPointGroup | AccessAccessPointGroup | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Delete access point group (destructive button) | `deleteAccessPointGroup` DELETE `/access-point-groups/{groupId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Group tree with roll-ups**: Each group row shows Entries, Exits, Current occupancy, Throughput per hour and Capacity as the pack lists; where the read does not return them, show the tree and grey the figures with "Live figures on the Live Operations board". *(source: screens/P08-venue-back-office.yaml#BO-151 / contracts/spine/access.yaml#listAccessLocationGrouping)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save group**: Upsert of the whole group (VO-R04); member list replaced as a set. *(source: contracts/spine/access.yaml#setAccessPointGroup)*
- **Delete group**: Refused while a nested group or a gate mode policy names it - the message names which, so nothing silently widens to the whole venue. *(source: contracts/spine/access.yaml#deleteAccessPointGroup)*

**Data it reads**: `listAccessLocationGrouping` (onLoad, Access Location Grouping)

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `listAccessLocationGrouping`

**What opens over it**

- confirmDialog *Delete access point group*: **Names what `deleteAccessPointGroup` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access location grouping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access location grouping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access location grouping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access location grouping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `group-cycle`: the parent named would make the group its own ancestor.; 409 `group-in-use`: a nested group or a gate mode policy still names this group.; 422 A member access point is not in the group's venue. |

#### Edge cases to draw

- **Access point deactivated after being grouped**: Shown struck-through inside the group with "Inactive". *(source: designer default)*

#### Consistency with other screens

- Match `BO-201`: Gate mode policies pick these groups by name.
- Match `BO-255`: Occupancy monitoring reports by the same groups.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
groups:
- name: Main Entrance
  members: Gate 01, Gate 02, Gate 03, Gate 04
  entries: 4210
  exits: 1180
  occupancy: 3030
  throughput: 1,150/h
- name: Adventure Zone
  members: Coaster Gate, Drop Tower Gate, Adventure Hall Gate
  parent: Aqua Park
```

#### Permissions

- `listAccessLocationGrouping` → `SCOPE_VIEW` (read) · staff
- `setAccessPointGroup` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `deleteAccessPointGroup` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-151` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-151`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 14: Works in Access Location Grouping → Group multiple access points for operational and capacity purposes.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (3 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-151?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save access point group, Delete access point group.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-152` Operating Calendar & Special Access Days

**Allow access topology and operating behavior to change by date/time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `entryId` (navigation) |
| Route | `/access-venue/operating-calendar-special-access-days-bo-152` |

**What the spec says about it.** **Overlapping entries: the venue sets a priority per entry (decided 2 October 2026 by Chinmay, DEC-229; CHG-CSP-027);** equal priorities on an overlap are refused. An entry can close the whole venue (`venueClosed`).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The venue's access calendar: normal operating days, weekends, holidays, seasons, private events, free-entry days, maintenance periods, special events, ladies-only and school/group sessions and after-hours events, each a dated entry that changes how gates behave without gate-by-gate edits (the pack's Free View Day: main gate free entry, attraction gates still validating). The one thing to get right: one calendar (Day/Week/Month/Agenda per VO-R01) with entries coloured by kind and a side panel that says what the gates will do in that window.

**Known correction pending (do not draw the wrong version)**

- **Ten selectFields, one per kind of day (normal operating days, weekends, holidays ... school/group sessions)** Why: The kinds are values of one dayType field (eleven, including after-hours events), drawn as a select and a legend. *(source: contracts/spine/access.yaml#setOperatingCalendarEntry / screens/P08-venue-back-office.yaml#BO-152; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The entry cannot say which gates or which topology it changes; only two booleans (main gates, attractions)** Why: The pack's purpose is that "access topology and operating behaviour change by date/time" and activate automatically; per-gate modes or a profile to switch to are not stored. *(source: screens/P08-venue-back-office.yaml#BO-151 / screens/P08-venue-back-office.yaml#BO-153 / contracts/spine/access.yaml#/components/schemas/AccessOperatingCalendarEntry; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No recurrence on an entry** Why: Weekends, normal operating days, seasonal schedules and weekly sessions are recurring; one row per occurrence is unusable. *(source: screens/P08-venue-back-office.yaml#BO-151 / contracts/spine/access.yaml#/components/schemas/AccessOperatingCalendarEntry; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The write body requires id and scopePath** Why: Server-owned (VO-R03); the description itself says no id creates. *(source: contracts/spine/access.yaml#setOperatingCalendarEntry; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **When two calendar entries overlap (a holiday inside a season, a private event on a free-entry day), which wins?** → Overlapping calendar entries: the venue sets a priority per entry. *(decided by Chinmay, 2026-10-02; DEC-229 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| normal operating days | select field | — | — | — | — | — | — |
| weekends | select field | — | — | — | — | — | — |
| holidays | select field | — | — | — | — | — | — |
| seasonal schedules | select field | — | — | — | — | — | — |
| private events | select field | — | — | — | — | — | — |
| free-entry days | select field | — | — | — | — | — | — |
| maintenance periods | select field | — | — | — | — | — | — |
| special events | select field | — | — | — | — | — | — |
| ladies-only sessions | select field | — | — | — | — | — | — |
| school/group sessions | select field | — | — | — | — | — | — |

**Form: Save operating calendar entry** (modal, opened by *Save operating calendar entry*; *Save operating calendar entry* calls `setOperatingCalendarEntry`, *Cancel* sends nothing)

**Collects what `setOperatingCalendarEntry` sends before it is called.** Required: `id`, `venueId`, `dayType`, `startsAt`, `endsAt`, `scopePath`. Optional: `name`, `ticketValidationRequired`, `admissionType`, `attractionValidation`, `manualAttendanceRequired`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setOperatingCalendarEntry` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setOperatingCalendarEntry` body |
| Day type `dayType` | select | required | — | Normal operating day · Weekend · Holiday · Seasonal schedule · Private event · Free entry day · Maintenance period · Special event · Ladies only session · School group session · After hours event | — | Kind of calendar entry | `setOperatingCalendarEntry` body |
| Name `name` | text field | optional | — | — | — | — | `setOperatingCalendarEntry` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setOperatingCalendarEntry` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setOperatingCalendarEntry` body |
| Ticket validation required `ticketValidationRequired` | toggle | optional | on | — | — | False on free-entry days | `setOperatingCalendarEntry` body |
| Admission type `admissionType` | segmented control | optional | — | Free view day · Special event | — | Set on special admission windows only | `setOperatingCalendarEntry` body |
| Attraction validation `attractionValidation` | toggle | optional | — | — | — | Special windows: attraction gates keep validating tickets | `setOperatingCalendarEntry` body |
| Manual attendance required `manualAttendanceRequired` | toggle | optional | — | — | — | Special windows: operator enters attendance count | `setOperatingCalendarEntry` body |
| Venue closed `venueClosed` | toggle | optional | off | — | — | A day the whole venue is closed (design-notes correction on BO-019, Block B: "No operation sets product blackout dates or a venue closure day"; CHG-CSP-051). | `setOperatingCalendarEntry` body |
| Priority `priority` | number field | optional | 0 | min 0; max 1000 | — | Which entry wins where two overlap: the higher priority (decided 2 October 2026, Chinmay, batch 6 set 10a, BO-152: "The venue sets a priority per entry"; DEC-229; CHG-CSP-027). | `setOperatingCalendarEntry` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setOperatingCalendarEntry` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `endsAt` is not after `startsAt`, or the entry overlaps another with the same `priority` (`overlapping-entry-same-priority`; CHG-CSP-027).

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **dayType**: One select (or legend chips that double as filters) with the eleven kinds: Normal operating day, Weekend, Holiday, Seasonal schedule, Private event, Free-entry day, Maintenance period, Special event, Ladies-only session, School/group session, After-hours event. Not one field per kind. *(source: screens/P08-venue-back-office.yaml#BO-151 / screens/P08-venue-back-office.yaml#BO-153 / contracts/spine/access.yaml#setOperatingCalendarEntry)*
- **name**: Optional, shown on the calendar block, e.g. "National Day", "Ladies Night"; Arabic variant. *(source: contracts/spine/access.yaml#setOperatingCalendarEntry)*
- **startsAt / endsAt**: Date and time pickers in venue time; end after start; dragging on the Day or Week view pre-fills them. *(source: contracts/spine/access.yaml#setOperatingCalendarEntry)*
- **ticketValidationRequired / attractionValidation / manualAttendanceRequired**: A two-row behaviour table "Main gates: Validate tickets / Free entry" and "Attraction gates: Validate / Do not validate", plus "Staff enter an attendance count". Free-entry day defaults main gates to Free entry and attractions to Validate, as the pack's example. *(source: screens/P08-venue-back-office.yaml#BO-153 / contracts/spine/access.yaml#/components/schemas/AccessOperatingCalendarEntry)*
- **admissionType**: Only for free-view and special-event windows (Free view day / Special event); hidden for every other kind. *(source: contracts/spine/access.yaml#setOperatingCalendarEntry)*
- **id, venueId, scopePath, createdAt, updatedAt**: Never inputs, although the overlay lists them as required (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*
- **priority**: A priority per calendar entry, set by the venue; where entries overlap, the higher priority wins. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `listOperatingCalendarSpecial`): Operating days and special access days on the month view. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

| Shows | Format | Notes |
|---|---|---|
| Ends at | 1 Oct 2026, 14:30 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Entry | text | — |
| Day type | chip: Normal operating day, Weekend, Holiday, Seasonal schedule, Private event, Free … | Kind of calendar entry |
| Venue | text | — |
| Name | text | — |
| Ticket validation required | yes / no (icon or chip) | False on free-entry days |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save operating calendar entry (primary button) | `setOperatingCalendarEntry` PUT `/operating-calendar-entries` | AccessOperatingCalendarEntry | AccessOperatingCalendarEntry | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Delete operating calendar entry (destructive button) | `deleteOperatingCalendarEntry` DELETE `/operating-calendar-entries/{entryId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Calendar**: Month view default; Day view in hours from calendarDayStartHour; entries coloured by kind with a legend that filters; overlapping entries stacked, not hidden. Week starts on the venue's first day; days run right to left in Arabic. *(source: contracts/spine/access.yaml#listOperatingCalendarSpecial / DI-919)*
- **Entry panel**: For the selected entry, the gates affected and what each will do, and the AI conflict warnings (below). *(source: screens/P08-venue-back-office.yaml#BO-153)*
- **AI conflict warnings**: Advisory amber notes using the pack's example "Main Gate is configured for Free Entry on 14 September, but the inherited Park Policy still requires credential validation", each with Go to; saving is still allowed (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-153)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save calendar entry**: Whole-entry upsert (VO-R04); no id creates. The confirmation states when gates change ("Main gates switch to free entry at 08:00 on Fri 13 Nov"). *(source: contracts/spine/access.yaml#setOperatingCalendarEntry)*
- **Delete calendar entry**: Confirmation names the window; an entry already started is refused 409 entry-in-progress - show "This entry has started; shorten its end time instead" with a button that opens it with End pre-selected. *(source: contracts/spine/access.yaml#deleteOperatingCalendarEntry)*

**Data it reads**: `listOperatingCalendarSpecial` (onLoad, Operating Calendar & Special Access Days)

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `listOperatingCalendarSpecial`

**What opens over it**

- confirmDialog *Delete operating calendar entry*: **Names what `deleteOperatingCalendarEntry` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operating calendar special configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operating calendar special untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operating calendar special configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `entry-in-progress`: the entry has already started.; 422 `endsAt` is not after `startsAt`, or the entry overlaps another with the same `priority` (`overlapping-entry-same-priority`; CHG-CSP-027). |

#### Edge cases to draw

- **Two entries overlap on the same gates with opposite behaviour**: Both shown stacked and flagged; the entry with the higher priority wins (the venue sets a priority per entry), and the panel says which. *(source: screens/P08-venue-back-office.yaml#BO-153 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **Entry ends while guests are inside on a free-entry day**: Panel notes that guests admitted free are counted, not ticketed, and exits are counted only where exit scans are on. *(source: MATRIX 3.2.62 / DI-626)*

#### Consistency with other screens

- Match `BO-222`: The same write serves Special Event & Free View; draw one calendar with a "Special admission" filter (VO-R14).
- Match `BO-158`: Blackout dates in an admission profile are product validity, not venue operation; a holiday here does not by itself block a ticket. Keep the two words apart (Blackout vs Venue calendar).
- Match `BO-147`: Attraction operating days link here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entries:
- kind: Holiday
  name: UAE National Day
  window: Wed 2 Dec 2026 00:00 - Thu 3 Dec 2026 23:59
  mainGates: Validate
  attractions: Validate
- kind: Free-entry day
  name: Free View Day
  window: Fri 13 Nov 2026 08:00-18:00
  mainGates: Free entry
  attractions: Validate
- kind: Ladies-only session
  name: Ladies Night
  window: Every Tue 18:00-22:00 (Aqua Park)
  mainGates: Validate
- kind: Maintenance period
  name: Wave pool refit
  window: 1-7 Feb 2027
```

#### Permissions

- `listOperatingCalendarSpecial` → `SCOPE_VIEW` (read) · staff
- `setOperatingCalendarEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `deleteOperatingCalendarEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-152` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-152`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 16: Works in Operating Calendar & Special Access Days → Allow access topology and operating behavior to change by date/time.

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-152?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save operating calendar entry, Delete operating calendar entry.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-153` Topology Validation & Publication

**Final validation and controlled deployment of access configuration. Before publication, TICVAI automatically validates: orphan gates devices without access points access points without zones incorrect entry/exit direction missing offline configuration conflicting operating calendars inaccessible zones missing emergency configuration capacity inconsistencies missing reader/device association policy dependencies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `versionId` (navigation) |
| Route | `/access-venue/topology-validation-publication-bo-153` |

**What the spec says about it.** **Publication approval is a venue policy, off by default; when on, a second person approves (decided 2 October 2026 by Chinmay, DEC-230; CHG-CSP-028).** A publication held for approval answers 200 with `awaitingApproval`, shown as "Waiting for approval".

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists access configuration versions with their validation results.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The gate before production for topology: the administrator runs TICVAI's validation (orphan gates, devices without access points, access points without zones, wrong direction, missing offline configuration, conflicting calendars, inaccessible zones, missing emergency configuration, capacity inconsistencies, missing reader association, policy dependencies), takes the version through Draft > Validate > Test > Approval > Schedule > Publish, publishes now or on a schedule to a chosen target, and can roll back. The one thing to get right: blocking findings are unmistakable and each one links to the screen that fixes it.

**Known correction pending (do not draw the wrong version)**

- **validationIssues is a client-supplied field of the publish request** Why: Validation findings are the server's output; a client cannot be trusted to send its own blocking list. A validate operation that returns findings is needed. *(source: contracts/spine/access.yaml#publishTopologyValidation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The primary Publish button is bound to no operation, and nothing reads the versions or their validation results** Why: Bind publishTopologyValidation to Publish; the version list and history need a read. *(source: screens/P08-venue-back-office.yaml#BO-153 / contracts/spine/access.yaml#publishTopologyValidation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's Test and Approval steps have no operation** Why: Lifecycle Draft > Validate > Test > Approval > Schedule > Publish; the contract covers validate, schedule, publish and rollback only, and "authorization" is in the acceptance condition. *(source: screens/P08-venue-back-office.yaml#BO-153; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who approves a topology publication, and must the approver differ from the author?** → Topology publication approval is a policy the venue switches on or off; when on, a second person approves. *(decided by Chinmay, 2026-10-02; DEC-230 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Form: Rollback configuration version** (modal, opened by *Rollback configuration version*; *Rollback configuration version* calls `rollbackConfigurationVersion`, *Cancel* sends nothing)

**Collects what `rollbackConfigurationVersion` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `rollbackConfigurationVersion` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `not-active` or `no-previous-version`.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **configurationVersionId**: The version comes from the entry (versionId) or a version picker showing version number, author, created time and status; never typed. *(source: contracts/spine/access.yaml#publishTopologyValidation)*
- **targetScope / targetIds**: Entire tenant, Venue, Park, Zone, Access point, Selected gates/devices as a radio list; the last four open a topology tree picker; the count of devices that will receive it is shown live ("Goes to 46 devices"). *(source: screens/P08-venue-back-office.yaml#BO-153 / contracts/spine/access.yaml#publishTopologyValidation)*
- **publishMode / scheduledAt**: Publish now or Schedule deployment; the date-time (venue time) appears only for Schedule and must be in the future. *(source: screens/P08-venue-back-office.yaml#BO-153 / contracts/spine/access.yaml#publishTopologyValidation)*
- **validationIssues**: Not an input - findings are produced by TICVAI's validation and shown, never typed or sent by the user. *(source: contracts/spine/access.yaml#publishTopologyValidation)*
- **rollback reason**: Required, max 500 characters. *(source: contracts/spine/access.yaml#rollbackConfigurationVersion)*
- **Approval policy**: A venue policy, on or off: when on, publishing a topology needs a second person with access configuration rights, never the author; when off, the author publishes. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish (primary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Rollback configuration version (secondary button) | `rollbackConfigurationVersion` POST `/configuration-versions/{versionId}/rollback` | inline | AccessConfigurationVersion | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lifecycle stepper**: Draft > Validate > Test > Approval > Schedule > Publish with the current step highlighted and who did each step and when. *(source: screens/P08-venue-back-office.yaml#BO-153)*
- **Validation checklist**: The eleven pack checks as rows with Pass / Warning / Blocking and a count; expanding a row lists the items with "Fix" links - orphan gates to BO-149, devices without access points to BO-196, access points without zones to BO-148, wrong direction to BO-149, conflicting calendars to BO-152, inaccessible zones to BO-146, missing emergency configuration to BO-201. Publish stays disabled while any row is Blocking. *(source: screens/P08-venue-back-office.yaml#BO-153)*
- **AI readiness score**: "Access Configuration Readiness: 96%" with the remaining risks explained; advisory only, it never turns a Blocking row into a pass (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-153)*
- **What publishing changes**: The publish gate names what goes live, where and from when ("Version 14 to Aqua Park, 46 devices, now"), and how many devices have picked it up afterwards. *(source: screens/P08-venue-back-office.yaml#BO-153 / contracts/spine/access.yaml#/components/schemas/DeviceGateCommandCenterView)*
- **Version history**: Versions with status (draft, active, scheduled, rolled back), published by, published at, target; a rolled-back version is marked and cannot be republished. *(source: contracts/spine/access.yaml#rollbackConfigurationVersion)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validate**: Runs the checks and fills the checklist; repeatable. *(source: screens/P08-venue-back-office.yaml#BO-153)*
- **Publish / Schedule**: Publishes the version to the target; confirmation repeats the publish gate wording; a scheduled one shows as Scheduled with Cancel. *(source: contracts/spine/access.yaml#publishTopologyValidation)*
- **Roll back**: Only on the active version; confirmation names the version restored and the devices that will receive it; 409 not-active and 409 no-previous-version shown as plain messages ("Only the version in force can be rolled back", "There is no earlier version to return to"). *(source: contracts/spine/access.yaml#rollbackConfigurationVersion)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The topology validation publication list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the topology validation publication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No topology validation publication yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the topology validation publication are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `not-active` or `no-previous-version`. |

#### Edge cases to draw

- **Devices offline at publication**: They are listed as "Will update when back online" with the version they still run; publication is not blocked by them. *(source: contracts/spine/access.yaml#/components/schemas/DeviceGateCommandCenterView)*
- **Two people publishing different versions to overlapping targets**: The second is refused with who published what and when. *(source: designer default)*

#### Consistency with other screens

- Match `BO-163`: Rule sets have the same lifecycle stepper and publish gate; one component for both.
- Match `BO-194`: Configuration version per device there is the version published here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
version:
  number: 14
  author: Fatima Al Hashimi
  status: Validated
  target: Aqua Park (46 devices)
  readiness: 96%
findings:
- check: Orphan gates
  result: Blocking
  items: Main Plaza Gate 3 - Lane 5 has no access point
- check: Missing offline configuration
  result: Warning
  items: North Entry HH-04 has no offline policy
- check: Conflicting operating calendars
  result: Pass
```

#### Permissions

- `publishTopologyValidation` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `rollbackConfigurationVersion` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-153` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-153`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 18: Works in Topology Validation & Publication → Final validation and controlled deployment of access configuration. Before publication, TICVAI automatically validates: orphan gates devices without access points access points without zones …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-153?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish, What publishing changes, Rollback configuration version.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAccessPoint": {"method":"POST","path":"/access-points","contract":"access","summary":"Create an access point","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateAccessPointRequest","responds":"AccessPoint"},
"createOrgUnit": {"method":"POST","path":"/org-units","contract":"tenancy","summary":"Create a scope node","permission":"SCOPE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"brand","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateScopeNodeRequest","responds":"OrgUnit"},
"deleteAccessPointGroup": {"method":"DELETE","path":"/access-point-groups/{groupId}","contract":"access","summary":"Delete an access-point group","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteOperatingCalendarEntry": {"method":"DELETE","path":"/operating-calendar-entries/{entryId}","contract":"access","summary":"Delete an operating calendar entry","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAccess": {"method":"GET","path":"/access","contract":"access","summary":"Access Control Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessControlCommandCenterView"},
"listAccessLocationGrouping": {"method":"GET","path":"/access-location-grouping","contract":"access","summary":"Access Location Grouping","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessLocationGroupingView"},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOperatingCalendarSpecial": {"method":"GET","path":"/operating-calendar-special","contract":"access","summary":"Operating Calendar & Special Access Days","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OperatingCalendarSpecialAccessDaysView"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVenueParkAccess": {"method":"GET","path":"/venue-park-access","contract":"access","summary":"Venue & Park Access Structure","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VenueParkAccessStructureView"},
"publishTopologyValidation": {"method":"PUT","path":"/topology-validation","contract":"access","summary":"Topology Validation & Publication","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TopologyValidationPublicationInput","responds":"TopologyValidationPublicationView"},
"rollbackConfigurationVersion": {"method":"POST","path":"/configuration-versions/{versionId}/rollback","contract":"access","summary":"Roll back an active access configuration version","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessConfigurationVersion"},
"setAccessAreaZone": {"method":"PUT","path":"/access-area-zone","contract":"access","summary":"Access Area & Zone Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessAreaZoneBuilderInput","responds":"AccessAreaZoneBuilderView"},
"setAccessGraphicalMap": {"method":"PUT","path":"/access-graphical-map","contract":"access","summary":"Access Control Graphical Map Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessControlGraphicalMapDesignerInput","responds":"AccessControlGraphicalMapDesignerView"},
"setAccessPointGroup": {"method":"PUT","path":"/access-point-groups","contract":"access","summary":"Create or replace an access-point group","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessAccessPointGroup","responds":"AccessAccessPointGroup"},
"setAttractionAccess": {"method":"PUT","path":"/attraction-access","contract":"access","summary":"Attraction Access Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AttractionAccessConfigurationInput","responds":"AttractionAccessConfigurationView"},
"setGateLane": {"method":"PUT","path":"/gate-lane","contract":"access","summary":"Gate & Lane Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GateLaneConfigurationInput","responds":"GateLaneConfigurationView"},
"setOperatingCalendarEntry": {"method":"PUT","path":"/operating-calendar-entries","contract":"access","summary":"Create or replace an operating calendar entry","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessOperatingCalendarEntry","responds":"AccessOperatingCalendarEntry"},
"updateAccessPoint": {"method":"PATCH","path":"/access-points/{accessPointId}","contract":"access","summary":"Update an access point","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPoint"},
"updateOrgUnit": {"method":"PATCH","path":"/org-units/{orgUnitId}","contract":"tenancy","summary":"Rename or deactivate a scope node","permission":"SCOPE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"brand","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrgUnit"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAccessPointGroup": {"type":"object","x-ticvai-persistence":"access.access_point_group","description":"A named group of access points in one venue (e.g. Main Entrance), optionally nested, whose counts roll up to a common occupancy (declared 29 September, data-model close-out DM1)","required":["id","venueId","name","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"name":{"type":"string","description":"Group name, e.g. Main Entrance"},"parentGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Enclosing group, for nested groups"},"accessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Member access points (access.access_point)"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessAreaZoneBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is access.parking_facility at 14%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Access Area & Zone Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each zone receives* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"name":{"type":"string","description":"Zone name, e.g. VIP Lounge"},"venueId":{"type":"string","description":"Venue the zone belongs to"},"zoneId":{"type":"string","description":"Zone being written"},"zoneType":{"type":"string","enum":["public","ticketed","vip","staff","backOfHouse","attraction","restricted","fastPass","event","temporary"],"description":"Vocabulary listed under Create."},"capacity":{"type":"integer","description":"capacity"},"operatingSchedule":{"type":"string","description":"operating schedule"},"securityClassification":{"type":"string","description":"The venue's label for the classification level, renamable (DEC-227; CHG-CSP-025)"},"securityClassificationLevel":{"type":"string","enum":["public","restricted","secure","critical"],"description":"Public, Restricted, Secure or Critical (decided 2 October 2026, Chinmay, BO-146; DEC-227; CHG-CSP-025); the label shown is `securityClassification`"},"entryRequirements":{"type":"string","description":"entry requirements"},"exitRequirements":{"type":"string","description":"exit requirements"},"allowedCredentialClasses":{"type":"array","items":{"type":"string"},"description":"Credential classes admitted to the zone"},"parentId":{"type":"string","description":"Park or zone this zone sits under in the venue structure"}},"x-ticvai-record-definition":"Each zone receives","required":["zoneId","venueId","name","zoneType"]},
"AccessAreaZoneBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Area & Zone Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Zone name, e.g. VIP Lounge"},"venueId":{"type":"string","description":"Venue the zone belongs to"},"zoneId":{"type":"string","description":"Zone being written"},"zoneType":{"type":"string","enum":["public","ticketed","vip","staff","backOfHouse","attraction","restricted","fastPass","event","temporary"],"description":"Vocabulary listed under Create."},"capacity":{"type":"integer","description":"capacity"},"operatingSchedule":{"type":"string","description":"operating schedule"},"securityClassification":{"type":"string","description":"The venue's label for the classification level, renamable (DEC-227; CHG-CSP-025)"},"securityClassificationLevel":{"type":"string","enum":["public","restricted","secure","critical"],"description":"Public, Restricted, Secure or Critical (decided 2 October 2026, Chinmay, BO-146; DEC-227; CHG-CSP-025); the label shown is `securityClassification`"},"entryRequirements":{"type":"string","description":"entry requirements"},"exitRequirements":{"type":"string","description":"exit requirements"},"allowedCredentialClasses":{"type":"array","items":{"type":"string"},"description":"Credential classes admitted to the zone"},"parentId":{"type":"string","description":"Park or zone this zone sits under in the venue structure"}},"required":["zoneId","venueId","name","zoneType"]},
"AccessConfigurationVersion": {"type":"object","x-ticvai-persistence":"access.configuration_version","description":"One version of access configuration (a topology or a rule set) moving through simulate, validate, schedule, publish and roll back, with its target, schedule, validation findings and the previous version kept for rollback (declared 29 September, data-model close-out DM1)","required":["id","configurationKind","version","status","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true},"configurationKind":{"type":"string","enum":["topology","ruleSet"]},"version":{"type":"string","description":"Version label"},"snapshot":{"type":"object","description":"The configuration captured by this version, restored on rollback"},"status":{"type":"string","enum":["draft","validated","pendingApproval","scheduled","active","inactive","rolledBack"],"default":"draft"},"lastStep":{"type":"string","enum":["simulate","validate","schedule","publish","rollBack"],"nullable":true,"description":"Last lifecycle step run on this version"},"targetScope":{"type":"string","enum":["tenant","venue","park","zone","accessPoint","selectedGates","selectedDevices"],"nullable":true,"description":"What the publication covers"},"targetIds":{"type":"array","items":{"type":"string"},"description":"IDs within the target scope"},"publishMode":{"type":"string","enum":["now","scheduled"],"nullable":true},"scheduledAt":{"type":"string","format":"date-time","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"validationIssues":{"type":"array","items":{"type":"string"},"description":"Blocking findings from pre-publication validation"},"conflicts":{"type":"array","items":{"type":"string"},"description":"Rule conflicts found by the conflict check (advisory)"},"previousVersionId":{"type":"string","format":"uuid","nullable":true,"description":"Version this one replaces, for rollback"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"Approval request raised in the approvals engine"},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessControlCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Control Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"totalVenues":{"type":"integer","description":"Total venues"},"activeAccessPoints":{"type":"integer","description":"Active access points"},"entryGates":{"type":"integer","description":"Entry gates"},"exitGates":{"type":"integer","description":"Exit gates"},"attractionGates":{"type":"integer","description":"Attraction gates"},"turnstiles":{"type":"integer","description":"Turnstiles"},"handheldDevices":{"type":"integer","description":"Handheld devices"},"devicesOnline":{"type":"integer","description":"Devices online"},"devicesOffline":{"type":"integer","description":"Devices offline"},"gatesOpen":{"type":"integer","description":"Gates open"},"gatesClosed":{"type":"integer","description":"Gates closed"},"currentInVenueOccupancy":{"type":"integer","description":"Current in-venue occupancy"},"currentAdmissionRate":{"type":"number","description":"Admissions per minute across the estate"},"failedScans":{"type":"integer","description":"Failed scans"},"overrides":{"type":"integer","description":"Overrides"},"securityAlerts":{"type":"integer","description":"Security alerts"},"synchronizationStatus":{"type":"string","enum":["inSync","syncPending","syncFailed"],"description":"Estate-wide offline sync state of devices"}}},
"AccessControlGraphicalMapDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Access Control Graphical Map Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"venueId":{"type":"string","description":"Venue the map belongs to"},"mapId":{"type":"string","description":"Map being written"},"sourceFileType":{"type":"string","enum":["cad","pdf","image","venuePlan","architecturalDrawing"],"description":"Kind of drawing uploaded as the map base"},"sourceFile":{"type":"string","description":"Reference to the uploaded drawing"}},"required":["mapId","venueId"]},
"AccessControlGraphicalMapDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Control Graphical Map Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue the map belongs to"},"mapId":{"type":"string","description":"Map being written"},"sourceFileType":{"type":"string","enum":["cad","pdf","image","venuePlan","architecturalDrawing"],"description":"Kind of drawing uploaded as the map base"},"sourceFile":{"type":"string","description":"Reference to the uploaded drawing"}},"required":["mapId","venueId"]},
"AccessLocationGroupingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Location Grouping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Group name, e.g. Main Entrance"},"groupId":{"type":"string"},"venueId":{"type":"string"},"parentGroupId":{"type":"string","description":"Enclosing group, for nested groups"},"accessPointIds":{"type":"array","items":{"type":"string"},"description":"Access points whose counts roll up into this group"}},"required":["groupId","name"]},
"AccessOperatingCalendarEntry": {"type":"object","x-ticvai-persistence":"access.operating_calendar_entry","description":"One dated entry in a venue operating calendar (normal day, holiday, private event, free-entry day, special event and so on), with whether tickets must be validated. Merges access.special_admission_window, whose free-view and special-event windows are entries carrying an admission type (declared 29 September, data-model close-out DM1)","required":["id","venueId","dayType","startsAt","endsAt","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"dayType":{"type":"string","enum":["normalOperatingDay","weekend","holiday","seasonalSchedule","privateEvent","freeEntryDay","maintenancePeriod","specialEvent","ladiesOnlySession","schoolGroupSession","afterHoursEvent"],"description":"Kind of calendar entry"},"name":{"type":"string","nullable":true},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"ticketValidationRequired":{"type":"boolean","default":true,"description":"False on free-entry days"},"admissionType":{"type":"string","enum":["freeViewDay","specialEvent"],"nullable":true,"description":"Set on special admission windows only"},"attractionValidation":{"type":"boolean","nullable":true,"description":"Special windows: attraction gates keep validating tickets"},"manualAttendanceRequired":{"type":"boolean","nullable":true,"description":"Special windows: operator enters attendance count"},"venueClosed":{"type":"boolean","default":false,"description":"**A day the whole venue is closed** (design-notes correction on BO-019, Block B: \"No operation sets product blackout dates or a venue closure day\"; CHG-CSP-051). Every gate refuses admission for the entry's dates, as `temporaryClosure` does for one attraction, and the closures screen shows it beside the product blackouts (catalogue `setEntitlementTemplateBlackoutDates`). Stopping sales for those dates is the performances' own (`cancelPerformance`, catalogue)."},"priority":{"type":"integer","minimum":0,"maximum":1000,"default":0,"description":"**Which entry wins where two overlap: the higher priority** (decided 2 October 2026, Chinmay, batch 6 set 10a, BO-152: \"The venue sets a priority per entry\"; DEC-229; CHG-CSP-027). A holiday inside a season, a private event on a free-entry day: the venue says which applies by giving it the higher number. Two overlapping entries with the same priority are refused `422 overlapping-entry-same-priority`, so the calendar never has to guess."},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n\n**R221 amended 2 October 2026: a gate's direction can be switched live** (Chinmay, critical set 1, BO-230: \"Live direction switch with permission, logged\"; DEC-255; CHG-CSP-032; DI-648: more entry gates in the morning, more exit gates in the evening). `setAccessPointDirection` switches it from Live Gate Mode & Lane Control (BO-230) or the scanner's gate mode screen (SCN-016) for a holder of the configuration right, logged; the podium's `setTurnstileMode` still never touches it.\n"},"temporaryClosure":{"type":"object","nullable":true,"description":"**What the access point does while its attraction is temporarily closed** (decided 2 October 2026, Chinmay, batch 6 set 9, BO-147: \"Deny + reopening time + a virtual-queue return window where enabled\"; DEC-228; CHG-CSP-026). While `isClosed`, every scan is denied (`ValidationResult.denyCause` `attractionTemporarilyClosed`) with the reopening time when it is known; where the venue offers it and the attraction has a virtual queue, the guest is offered a return window (`queue.joinQueue`) instead of being turned away empty-handed. Set with `updateAccessPoint`; null when open. Travels in the offline package, so an offline gate denies the same way.","properties":{"isClosed":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":200,"nullable":true,"description":"Shown to staff; the guest sees \"Attraction temporarily closed\"."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When it is expected to reopen; shown to the guest when known."},"offerVirtualQueueReturn":{"type":"boolean","default":false,"description":"Offer a virtual-queue return window at the denied scan, where the attraction has a queue."},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The virtual queue the return window is taken in."}}},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"AttractionAccessConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is access.parking_facility at 6%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Attraction Access Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each attraction* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"attractionId":{"type":"string","description":"Attraction ID"},"name":{"type":"string","description":"Name"},"venue":{"type":"string","description":"Venue"},"zone":{"type":"string","description":"Zone"},"capacity":{"type":"integer","description":"Capacity"},"entryPoints":{"type":"array","items":{"type":"string"},"description":"Access point IDs used to enter"},"exitPoints":{"type":"array","items":{"type":"string"},"description":"Access point IDs used to exit"},"fastPassSupport":{"type":"boolean","description":"Fast Pass support"},"heightRestriction":{"type":"integer","description":"Minimum rider height in cm, e.g. 130"},"ageRestriction":{"type":"integer","description":"Minimum age in years"},"adultCompanionRequirement":{"type":"boolean","description":"Adult companion requirement"},"membershipAccess":{"type":"boolean","description":"Membership access"},"vipAccess":{"type":"boolean","description":"VIP access"},"entitlementRequirement":{"type":"string","description":"entitlement requirement"},"biometricRequirement":{"type":"boolean","description":"biometric requirement"},"operatingCalendar":{"type":"string","description":"operating calendar"},"temporaryClosureBehavior":{"type":"string","description":"temporary closure behavior"}},"x-ticvai-record-definition":"For each attraction","required":["attractionId","name","venue"]},
"AttractionAccessConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Attraction Access Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"attractionId":{"type":"string","description":"Attraction ID"},"name":{"type":"string","description":"Name"},"venue":{"type":"string","description":"Venue"},"zone":{"type":"string","description":"Zone"},"capacity":{"type":"integer","description":"Capacity"},"entryPoints":{"type":"array","items":{"type":"string"},"description":"Access point IDs used to enter"},"exitPoints":{"type":"array","items":{"type":"string"},"description":"Access point IDs used to exit"},"fastPassSupport":{"type":"boolean","description":"Fast Pass support"},"heightRestriction":{"type":"integer","description":"Minimum rider height in cm, e.g. 130"},"ageRestriction":{"type":"integer","description":"Minimum age in years"},"adultCompanionRequirement":{"type":"boolean","description":"Adult companion requirement"},"membershipAccess":{"type":"boolean","description":"Membership access"},"vipAccess":{"type":"boolean","description":"VIP access"},"entitlementRequirement":{"type":"string","description":"entitlement requirement"},"biometricRequirement":{"type":"boolean","description":"biometric requirement"},"operatingCalendar":{"type":"string","description":"operating calendar"},"temporaryClosureBehavior":{"type":"string","description":"temporary closure behavior"}},"required":["attractionId","name","venue"]},
"CreateAccessPointRequest": {"type":"object","required":["code","name","venueId","direction"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"direction":{"$ref":"#/components/schemas/Direction"},"antiPassbackEnabled":{"type":"boolean","default":false},"requiresExitBeforeReentry":{"type":"boolean","default":false},"driver":{"type":"string"}}},
"CreateScopeNodeRequest": {"type":"object","required":["level","parentId","code","name"],"properties":{"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","description":"Required for every level except tenant, which the cell creates at provisioning."},"code":{"type":"string","maxLength":64,"pattern":"^[a-z0-9_]+$","description":"Becomes the final ltree segment. Immutable once created."},"name":{"type":"string","maxLength":200}}},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"GateLaneConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Gate & Lane Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"gateId":{"type":"string","description":"Gate ID"},"gateName":{"type":"string","description":"Gate name"},"accessPoint":{"type":"string","description":"Access point"},"location":{"type":"string","description":"Location"},"laneNumber":{"type":"string","description":"lane number"},"direction":{"type":"string","enum":["entry","exit","bidirectional"],"description":"Lane direction, inherited from the access point unless set"},"reEntry":{"type":"boolean","description":"Lane accepts re-entry scans"},"crossover":{"type":"boolean","description":"Lane is a crossover lane between parks"},"type":{"type":"string","enum":["standard","vip","fastPass","accessible","group","staff","attraction"],"description":"Vocabulary listed under Gate type."},"operationalMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"description":"Default operating mode of the lane, in the AccessPointOperatingMode vocabulary the podium sets (R221). Aligned (decided 29 September, writers pass): the old validation, freeSpin, emergencyDropArm, manual and countOnly are normal, freeFlow, dropArm, podium and freeFlow."},"laneSize":{"type":"string","enum":["standard","wide"],"description":"Wide lanes take buggies and wheelchairs"}},"required":["gateId","accessPoint"]},
"GateLaneConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Gate & Lane Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"gateId":{"type":"string","description":"Gate ID"},"gateName":{"type":"string","description":"Gate name"},"accessPoint":{"type":"string","description":"Access point"},"location":{"type":"string","description":"Location"},"laneNumber":{"type":"string","description":"lane number"},"direction":{"type":"string","enum":["entry","exit","bidirectional"],"description":"Lane direction, inherited from the access point unless set"},"reEntry":{"type":"boolean","description":"Lane accepts re-entry scans"},"crossover":{"type":"boolean","description":"Lane is a crossover lane between parks"},"type":{"type":"string","enum":["standard","vip","fastPass","accessible","group","staff","attraction"],"description":"Vocabulary listed under Gate type."},"operationalMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"description":"Default operating mode of the lane, in the AccessPointOperatingMode vocabulary the podium sets (R221). Aligned (decided 29 September, writers pass): the old validation, freeSpin, emergencyDropArm, manual and countOnly are normal, freeFlow, dropArm, podium and freeFlow."},"laneSize":{"type":"string","enum":["standard","wide"],"description":"Wide lanes take buggies and wheelchairs"}},"required":["gateId","accessPoint"]},
"OperatingCalendarSpecialAccessDaysView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Operating Calendar & Special Access Days displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"endsAt":{"type":"string","format":"date-time"},"startsAt":{"type":"string","format":"date-time"},"entryId":{"type":"string"},"dayType":{"type":"string","enum":["normalOperatingDay","weekend","holiday","seasonalSchedule","privateEvent","freeEntryDay","maintenancePeriod","specialEvent","ladiesOnlySession","schoolGroupSession","afterHoursEvent"],"description":"Kind of calendar entry"},"venueId":{"type":"string"},"name":{"type":"string"},"ticketValidationRequired":{"type":"boolean","description":"False on free-entry days"}},"required":["entryId","dayType","startsAt","endsAt"]},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"TopologyValidationPublicationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Topology Validation & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"publishMode":{"type":"string","enum":["now","scheduled"]},"configurationVersionId":{"type":"string","description":"Topology version being published"},"targetScope":{"type":"string","enum":["tenant","venue","park","zone","accessPoint","selectedGates","selectedDevices"],"description":"What the publication covers"},"targetIds":{"type":"array","items":{"type":"string"},"description":"IDs within the target scope"},"scheduledAt":{"type":"string","format":"date-time"},"validationIssues":{"type":"array","items":{"type":"string"},"description":"Blocking findings from pre-publication validation"}},"required":["configurationVersionId","targetScope","publishMode"]},
"TopologyValidationPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Topology Validation & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"awaitingApproval":{"type":"boolean","readOnly":true,"default":false,"description":"True when the venue's approval policy is on and the publication waits for a second person (DEC-230; CHG-CSP-028)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The approval request the publication waits on (approvals `ApprovalRequest`), when it waits."},"publishMode":{"type":"string","enum":["now","scheduled"]},"configurationVersionId":{"type":"string","description":"Topology version being published"},"targetScope":{"type":"string","enum":["tenant","venue","park","zone","accessPoint","selectedGates","selectedDevices"],"description":"What the publication covers"},"targetIds":{"type":"array","items":{"type":"string"},"description":"IDs within the target scope"},"scheduledAt":{"type":"string","format":"date-time"},"validationIssues":{"type":"array","items":{"type":"string"},"description":"Blocking findings from pre-publication validation"}},"required":["configurationVersionId","targetScope","publishMode"]},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]},
"VenueParkAccessStructureView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Venue & Park Access Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"entityType":{"type":"string","enum":["venue","park","building","eventSpace","waterpark","themePark","museum","arena","stadium","exhibition","temporaryVenue"],"description":"What kind of place this entity is"},"name":{"type":"string","description":"Name"},"code":{"type":"string","description":"Code"},"tenant":{"type":"string","description":"Tenant"},"parentEntity":{"type":"string","description":"Parent entity"},"timeZone":{"type":"string","description":"IANA time zone, e.g. Asia/Dubai"},"operatingCalendar":{"type":"string","description":"Operating calendar"},"capacity":{"type":"integer","description":"Capacity"},"accessControlEnabled":{"type":"boolean","description":"Access-control enabled"},"defaultEntryPolicy":{"type":"string","description":"Default entry policy"},"defaultExitPolicy":{"type":"string","description":"Default exit policy"},"defaultCredentialRules":{"type":"string","description":"Default credential rules"},"offlinePolicy":{"type":"string","description":"Reference to the offline validation policy the entity inherits"},"emergencyBehavior":{"type":"string","description":"Emergency behavior"},"supportMultiParkEnvironments":{"type":"boolean","description":"Support multi-park environments"}},"required":["code","name","entityType"]}
}
```
