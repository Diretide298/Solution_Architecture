# WS07 — Access Control board 7

**10 screens · 12 operations · 19 schemas · 3 permissions**

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
  `ACCESS_POINT_CONFIGURE, INCIDENT_MANAGE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-204` | Offline & Edge Operations Command Center | B–D | 0 | 182 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-205` | Edge Node & Local Processing Configuration | B–D | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-206` | Offline Validation Policy Builder | B–D | 13 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-207` | Edge Package & Data Distribution | B–D | 16 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-208` | Offline Credential & Revocation Cache | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-209` | Offline Entitlement & Usage Ledger | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-210` | Connectivity Failure & Degraded Mode Policy | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-211` | Reconnection, Synchronization & Conflict Resolution | B–D | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-212` | Offline Simulation & Resilience Testing | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-213` | Edge Security, Audit & Deployment | B–D | 3 | 110 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-206, BO-208, BO-209, BO-210, BO-211, BO-212 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-204` Offline & Edge Operations Command Center

**Provide a real-time overview of offline readiness across the entire access-control estate.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/offline-edge-operations-command-center-bo-204` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Board 7 command centre: can every venue, gate and device keep admitting guests safely if the cloud, the venue WAN or the edge node disappears. Ten KPI tiles, a venue readiness table with a readiness score and its six checks, and AI risk highlights such as a revocation package not synced for six hours. The one thing to get right: "the venue does not stop when the cloud goes down" - readiness problems (stale revocation data, expiring packages, pending transactions) are surfaced first and each opens the screen that fixes it.

**Known correction pending (do not draw the wrong version)**

- **Sync Conflicts drawn as the only column of the data table, and missing from the tiles** Why: It is a KPI tile in the pack and in the summary (VO-R02); the table's columns are the venue readiness columns. *(source: screens/P08-venue-back-office.yaml#BO-204 / contracts/spine/access.yaml#listOfflineEdge; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every offline edge operations" and "The selected offline edge operations"** Why: Generated placeholders; use "Venue readiness" and the venue name (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is this command centre venue-scoped (rows are parks and zones of the selected venue) or estate-wide across venues, as the pack's table of Adventure Park, Water Park and Event Arena suggests?** → Drawn default accepted: Rows per venue the user can see, with the top-bar venue highlighted; the read is venue-scoped today. *(decided by Chinmay, 2026-10-02; DEC-246 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Offline-Ready Devices** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Currently Online** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Currently Offline** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Devices in Degraded Mode** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Edge Nodes Online** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Packages Current** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Packages Expiring** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Pending Offline Transactions** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Offline Security Alerts** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Every offline edge operations** (data table, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Sync conflicts | text | not in the schema: `Sync Conflicts` |

**The selected offline edge operations** (detail panel): The pack groups this record's detail under its own headings: “Venue Readiness”, “Checks”.

| Shows | Format | Notes |
|---|---|---|
| Sync conflicts | text | not in the schema: `Sync Conflicts` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: The ten pack tiles per VO-R02: Offline-ready devices, Currently online, Currently offline, Devices in degraded mode, Edge nodes online, Packages current, Packages expiring, Pending offline transactions, Sync conflicts, Offline security alerts. Sync conflicts and security alerts red when above zero; tiles open BO-211 and BO-213. *(source: screens/P08-venue-back-office.yaml#BO-204 / contracts/spine/access.yaml#listOfflineEdge)*
- **Venue readiness table**: Columns Venue, Devices, Offline ready, Package (Current / Expiring / Expired), Pending transactions, Status (Ready green, Warning amber, Not ready red); sorted Not ready first. *(source: screens/P08-venue-back-office.yaml#BO-204 / contracts/spine/access.yaml#listOfflineEdge)*
- **Readiness score and checks**: Detail of a venue: "Adventure Park - 98% READY" and the six checks (Rules cached, Verification material current, Revocation data current, Credential definitions available, Device storage healthy, Last synchronization successful) as ticks or crosses, each failed check linking to its screen (revocation > BO-208, package > BO-207, sync > BO-211). *(source: screens/P08-venue-back-office.yaml#BO-204 / contracts/spine/access.yaml#listOfflineEdge)*
- **Central visual**: A banner "VENUE EDGE - ACTIVE, 84 GATES OPERATING" when a venue is running on its edge, with local transactions accumulating and a sync flow back once reconnected. *(source: screens/P08-venue-back-office.yaml#BO-213 / screens/P08-venue-back-office.yaml#BO-214)*
- **AI highlights**: Plain sentences naming the gates and the age ("Two Water Park gates have not synced their revocation package for 6 hours"), each with Open; advisory only. *(source: screens/P08-venue-back-office.yaml#BO-204)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open a board screen**: Tiles and failed checks open BO-205 to BO-213 and return here. *(source: DI-653 / F117 step 1)*

**Data it reads**: `listOfflineEdge` (onLoad, Offline & Edge Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-205` Edge Node & Local Processing Configuration: *Works in Edge Node & Local Processing Configuration*; calls `listOfflineEdge`
- → `BO-206` Offline Validation Policy Builder: *Works in Offline Validation Policy Builder*; calls `listOfflineEdge`
- → `BO-207` Edge Package & Data Distribution: *Works in Edge Package & Data Distribution*; calls `listOfflineEdge`
- → `BO-208` Offline Credential & Revocation Cache: *Works in Offline Credential & Revocation Cache*; calls `listOfflineEdge`
- → `BO-209` Offline Entitlement & Usage Ledger: *Works in Offline Entitlement & Usage Ledger*; calls `listOfflineEdge`
- → `BO-210` Connectivity Failure & Degraded Mode Policy: *Works in Connectivity Failure & Degraded Mode Policy*; calls `listOfflineEdge`
- → `BO-211` Reconnection, Synchronization & Conflict Resolution: *Works in Reconnection, Synchronization & Conflict Resolution*; calls `listOfflineEdge`
- → `BO-212` Offline Simulation & Resilience Testing: *Works in Offline Simulation & Resilience Testing*; calls `listOfflineEdge`
- → `BO-213` Edge Security, Audit & Deployment: *Works in Edge Security, Audit & Deployment*; calls `listOfflineEdge`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline edge operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline edge operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline edge operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline edge operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Package expired at a venue**: Status Not ready in red with "Gates are in Unsafe / Expired mode" wording shared with BO-210. *(source: screens/P08-venue-back-office.yaml#BO-210 / contracts/spine/access.yaml#listConnectivityFailureDegraded)*
- **Battery or runtime estimate not available**: The pack's "43 minutes of offline runtime" highlight only appears for devices that report battery; others say "Not reported". *(source: screens/P08-venue-back-office.yaml#BO-204 / DI-900)*

#### Consistency with other screens

- Match `BO-144`: Same command centre pattern and tile style as the access board hub (VO-R02).
- Match `SCN-015`: Package age and "pending to sync" wording match the scanner's offline package screen (VO-R07).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  offlineReady: 171
  online: 168
  offline: 3
  degraded: 2
  edgeNodesOnline: 3 / 3
  packagesCurrent: 171
  packagesExpiring: 2
  pendingTxns: 18
  syncConflicts: 1
  securityAlerts: 0
venues:
- venue: Aqua Park
  devices: 61
  offlineReady: 59
  package: Current
  pending: 18
  status: Warning
- venue: Summit Peaks
  devices: 84
  offlineReady: 84
  package: Current
  pending: 0
  status: Ready
  score: 98% READY
- venue: Summit Peaks Event Arena
  devices: 28
  offlineReady: 28
  package: Expiring
  pending: 0
  status: Warning
```

#### Permissions

- `listOfflineEdge` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-204` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-204`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 1: Opens Offline & Edge Operations Command Center → Provide a real-time overview of offline readiness across the entire access-control estate.
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F117 branch at step 1 (expected): when Nothing has been set up on Offline & Edge Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F117 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (182 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-204?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-205`, `BO-206`, `BO-207`, `BO-208`, `BO-209`, `BO-210`, `BO-211`, `BO-212`, `BO-213`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-205` Edge Node & Local Processing Configuration

**Configure where local access decisions are processed when central services cannot be reached.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Fields) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/edge-node-local-processing-configuration-bo-205` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists edge nodes (setEdgeNodeLocal has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Says which edge component makes local access decisions when central services are unreachable (venue edge node, gate controller, turnstile local engine or handheld local engine) and which devices each one serves, with primary and secondary nodes where the infrastructure allows. The one thing to get right: every deployed device is covered by exactly one responsible component, shown as a topology, and the values a node reports about itself (heartbeat, software version, security status) are displayed, never typed.

**Known correction pending (do not draw the wrong version)**

- **Tenant and Venue drawn as selectFields; Last heartbeat, software version and security status drawn as editable selectFields** Why: Tenant and venue are session scope (VO-R03); the other three are reported by the node and read only. *(source: contracts/spine/access.yaml#setEdgeNodeLocal; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Device assignment is a single `deviceGroup` string and redundancy a free string** Why: The pack's acceptance is "which edge component is responsible for every deployed device" and a primary/secondary pair; one string can hold neither. *(source: screens/P08-venue-back-office.yaml#BO-205 / screens/P08-venue-back-office.yaml#BO-206; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write-only screen (setEdgeNodeLocal) with no read of the nodes (CHG-WIR-004)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What are the processing modes of an edge node (for example active, standby, pass-through)?** → Drawn default accepted: Draw the select greyed with "Options to be agreed". *(decided by Chinmay, 2026-10-02; DEC-247 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Edge Node ID | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Network | select field | — | — | — | — | — | — |
| Device Group | select field | — | — | — | — | — | — |
| Processing Mode | select field | — | — | — | — | — | — |
| Storage allocation | select field | — | — | — | — | — | — |
| redundancy | select field | — | — | — | — | — | — |
| last heartbeat | select field | — | — | — | — | — | — |
| software version | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **nodeType**: Four cards with the pack's one-line meaning: Venue edge node (shared local processing for a venue), Gate controller (at gate level), Turnstile local engine (embedded in the device), Handheld local engine (mobile offline). Required. *(source: screens/P08-venue-back-office.yaml#BO-205 / contracts/spine/access.yaml#setEdgeNodeLocal)*
- **edgeNodeId**: Chosen from the device register (an edge node is a registered device), not typed; for a turnstile or handheld engine it is the device itself. *(source: ADR-0067 / contracts/spine/access.yaml#setEdgeNodeLocal)*
- **tenantId / venueId**: Not inputs; the venue is the top-bar venue and the tenant is the session's (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule / ADR-0030)*
- **Device assignment (deviceGroup)**: A topology tree "Adventure Park Edge Cluster > Main Entrance Gates 01-20, VIP Gates 01-04, Fast Pass Gates, Attraction Gates, Handheld Group A" where gate groups are ticked; a device already served by another node shows that node's name. Show "3 devices with no edge assignment" until zero. *(source: screens/P08-venue-back-office.yaml#BO-205 / contracts/spine/access.yaml#setEdgeNodeLocal)*
- **redundancy**: "High availability" section, only for Venue edge node: pick a secondary edge node that takes over on failure of the primary; hidden for embedded and handheld engines. *(source: screens/P08-venue-back-office.yaml#BO-205 / screens/P08-venue-back-office.yaml#BO-206)*
- **network / processingMode / storageAllocation**: Network as the venue network segment the node sits on; storage allocation in GB with the current use beside it; processing mode as a select whose options are still to be agreed (see decisions). *(source: contracts/spine/access.yaml#setEdgeNodeLocal / designer default)*
- **lastHeartbeat / softwareVersion / securityStatus**: Read-only status strip at the top ("Last heartbeat 10:04:22, v5.2.1, Secure"); set by the node, never inputs. *(source: contracts/spine/access.yaml#setEdgeNodeLocal / ADR-0067)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Edge topology**: Venue > edge cluster > node (primary, secondary) > gate groups and handheld groups, with each node's heartbeat colour; matches the board's central "venue edge active" visual. *(source: screens/P08-venue-back-office.yaml#BO-205 / screens/P08-venue-back-office.yaml#BO-213)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save edge node**: Whole-row upsert (VO-R04); confirmation names the devices whose responsible node changes ("24 gates move from Gate controller to Venue edge node AP-EDGE-01"). Devices take it at their next package refresh. *(source: contracts/spine/access.yaml#setEdgeNodeLocal)*

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `setEdgeNodeLocal`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The edge node local configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the edge node local untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No edge node local configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Primary node fails**: The topology shows the secondary active and the primary red with the time it was last seen. *(source: screens/P08-venue-back-office.yaml#BO-206)*
- **Node heartbeat older than a few minutes**: Amber with age; the node's devices fall back to their own local engine (Local offline), stated in the panel. *(source: screens/P08-venue-back-office.yaml#BO-210 / designer default)*

#### Consistency with other screens

- Match `BO-210`: Edge mode and Local offline are the states this assignment decides between; same names.
- Match `BO-196`: Edge nodes and devices come from the one device register (ADR-0067); Access only places them.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
nodes:
- node: AP-EDGE-01
  type: Venue edge node
  cluster: Aqua Park Edge Cluster
  serves: Main Plaza Gates 1-3 (20 lanes), North Entry (4), Handheld Group A (12)
  secondary: AP-EDGE-02
  heartbeat: '10:04:22'
  version: 5.2.1
  security: Secure
- node: Falcon Coaster controller
  type: Gate controller
  serves: Falcon Coaster gates (2)
  heartbeat: '10:04:18'
```

#### Permissions

- `setEdgeNodeLocal` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-205` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-205`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 2: Works in Edge Node & Local Processing Configuration → Configure where local access decisions are processed when central services cannot be reached.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-205?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-206` Offline Validation Policy Builder

**Define exactly which access checks are allowed to run locally. The matrix identifies key offline criteria including eligible media, eligible site, eligible time, ticket validity and eligible access mode.**

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
| Route | `/access-venue/offline-validation-policy-builder-bo-206` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): The gate offline validation policy is written by setGateOfflinePolicy (access, ACCESS_POINT_CONFIGURE); setOfflinePolicy is the tenancy POS till policy (sales …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Which access checks a gate may run locally when offline: eligible media, site, time window, ticket validity, access mode. Each check either runs offline or requires the server; the policy is per venue.

**Fixed on main** (the package already carries these; draw what it says): setOfflinePolicy requires TENANT_CONFIGURE. (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Form: Save offline validation policy** (modal, opened by *Save offline validation policy*; *Save offline validation policy* calls `setGateOfflinePolicy`, *Cancel* sends nothing)

**Collects what `setGateOfflinePolicy` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setGateOfflinePolicy` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setGateOfflinePolicy` body |
| Max offline duration hours `maxOfflineDurationHours` | number field (hours) | optional | — | min 0 | — | Hours a reader may validate offline; past it, readers refuse offline taps (decided 2 October 2026, Chinmay, critical set 1, BO-471: "Yes: the venue sets a maximum offline … | `setGateOfflinePolicy` body |
| Offline checks `offlineChecks` | multi-select chips | optional | — | Credential authenticity · Digital signature · Ticket ID · Venue · Park · Zone · Visit date · Time window · Credential status snapshot · Ticket type · Guest category · Seat … | — | What a gate may validate locally | `setGateOfflinePolicy` body |
| After threshold behavior `afterThresholdBehavior` | radio group | optional | — | Continue restricted validation · Operator warning · Supervisor mode · Fail closed · Fallback | — | — | `setGateOfflinePolicy` body |
| Revocation trigger events `revocationTriggerEvents` | multi-select chips | optional | — | Fraud lock · Refund · Cancellation · Lost credential · Transfer · Reissue · Manual invalidation | — | Events that push an invalidation into the offline cache | `setGateOfflinePolicy` body |
| Revocation max allowed age minutes `revocationMaxAllowedAgeMinutes` | number field (minutes) | optional | — | min 0 | — | Maximum allowed revocation cache age | `setGateOfflinePolicy` body |
| Revocation staleness action `revocationStalenessAction` | select | optional | — | Continue · Continue with warning · Restricted products only · Supervisor mode · Deny selected credential classes · Fail closed | — | What devices do when the cache is older than the maximum allowed age | `setGateOfflinePolicy` body |
| Operating modes `operatingModes` | multi-select chips | optional | — | Online · Degraded · Edge mode · Local offline · Unsafe expired | — | Operating modes a device moves through as connectivity fails | `setGateOfflinePolicy` body |
| Central unavailable after seconds `centralUnavailableAfterSeconds` | number field (seconds) | optional | — | min 0 | — | Seconds without central services before switching to edge mode | `setGateOfflinePolicy` body |
| Edge unavailable after seconds `edgeUnavailableAfterSeconds` | number field (seconds) | optional | — | min 0 | — | Seconds without the venue edge before switching to local offline | `setGateOfflinePolicy` body |
| Automatic switch `automaticSwitch` | toggle | optional | on | — | — | Switch modes automatically without stopping guest flow | `setGateOfflinePolicy` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setGateOfflinePolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 The edge threshold is shorter than the central one.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setOfflinePolicy: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setOfflinePolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Save offline validation policy (secondary button) | `setGateOfflinePolicy` PUT `/offline-policies` | AccessOfflinePolicy | AccessOfflinePolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 The edge threshold is shorter than the central one. | opens modal first |

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `setGateOfflinePolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline validation policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline validation policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline validation policy yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline validation policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The edge threshold is shorter than the central one. |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  eligibleMedia:
  - QR
  - RFID wristband
  eligibleSite: true
  eligibleTime: true
  ticketValidity: true
  maxOfflineMinutes: 120
```

#### Permissions

- `setGateOfflinePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-206` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-206`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 4: Works in Offline Validation Policy Builder → Define exactly which access checks are allowed to run locally. The matrix identifies key offline criteria including eligible media, eligible site, eligible time, ticket validity and eligible access …

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-206?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Save offline validation policy.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-207` Edge Package & Data Distribution

**Define what configuration and operational data is securely distributed to edge devices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Access Configuration; Credential Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/edge-package-data-distribution-bo-207` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): getOfflinePackage is workstation-scoped (ACCESS_VALIDATE) and refuses a back-office browser with 403; the screen reads listEdgePackageData (design-notes …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** What the signed edge package carries to venue edge nodes and devices (access configuration, credential configuration, security material, operational data), its version, size and validity, how it is distributed (central > venue edge > device groups > devices) and each device's state (Downloaded, Verified, Activated, Failed) after the integrity check. The one thing to get right: only a package that passes signature, completeness, version and device authorisation checks can become active, and the screen shows per device where it stopped.

**Known correction pending (do not draw the wrong version)**

- **Only eight of the fifteen content sets drawn, as selectFields; no write defines package contents** Why: The pack asks to define what the package carries; contents are read-only in the view and publish only deploys a version. *(source: screens/P08-venue-back-office.yaml#BO-207 / contracts/spine/access.yaml#listEdgePackageData; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Per-device status (Downloaded, Verified, Activated, Failed) is not in the read** Why: The pack requires each device to display it. *(source: screens/P08-venue-back-office.yaml#BO-208; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Publish button labelled "What publishing changes"** Why: Generated label; "Publish package" with the summary in the confirmation. *(source: screens/P08-venue-back-office.yaml#BO-207; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The package view does not show the policy set version it carries** Why: ADR-0068 makes the active policy version part of the package; the screen must show it so a scan can be explained. *(source: ADR-0068 / contracts/spine/access.yaml#/components/schemas/OfflinePackage; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): getOfflinePackage is bound on load (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| venues | select field | — | — | — | — | — | — |
| zones | select field | — | — | — | — | — | — |
| gates | select field | — | — | — | — | — | — |
| access rules | select field | — | — | — | — | — | — |
| calendars | select field | — | — | — | — | — | — |
| media profiles | select field | — | — | — | — | — | — |
| verification profiles | select field | — | — | — | — | — | — |
| entitlement definitions | select field | — | — | — | — | — | — |

**Sent by *What publishing changes*** (`publishHardwareDeployment`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated deployment id | `publishHardwareDeployment` body |
| Configuration version `configurationVersion` | text field | required | — | — | — | The access configuration version being deployed | `publishHardwareDeployment` body |
| Target scope `targetScope` | radio group | required | — | Pilot · Selected gates · Device group · Venue | — | — | `publishHardwareDeployment` body |
| Venue `venueId` | text field | required | — | — | — | — | `publishHardwareDeployment` body |
| Gates `gateIds` | list of values (chips) | optional | — | — | — | Required for pilot and selectedGates | `publishHardwareDeployment` body |
| Device group `deviceGroupId` | text field | optional | — | — | — | Required for deviceGroup | `publishHardwareDeployment` body |
| Run compatibility test first `runCompatibilityTestFirst` | toggle | optional | on | — | — | Devices that fail the compatibility test are skipped and named in the result | `publishHardwareDeployment` body |
| Scheduled at `scheduledAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Empty deploys now | `publishHardwareDeployment` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Package contents**: All fifteen data sets as a checklist in the pack's four groups: Access configuration (venues, zones, gates, access rules, calendars), Credential configuration (media profiles, verification profiles, entitlement definitions), Security (trusted verification material, revocation information, credential security parameters), Operational (reason codes, gate responses, languages, operator permissions). Mandatory sets (access rules, revocation, verification material) are ticked and locked. *(source: screens/P08-venue-back-office.yaml#BO-207 / contracts/spine/access.yaml#listEdgePackageData)*
- **Publish target**: Same target choice and compatibility toggle as BO-203 (pilot, selected gates, device group, venue; now or scheduled). *(source: contracts/spine/access.yaml#publishHardwareDeployment)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | `publishHardwareDeployment` POST `/hardware-deployments` | HardwareDeploymentInput | HardwareDeploymentView | 409 A deployment to an overlapping target set is still queued or in progress; 422 gateIds or deviceGroupId missing for the chosen targetScope | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Package card**: Name (e.g. AC-EDGE-AUH-1001-V31), version, devices, size in MB, valid from-to in venue time, and the active guest admission policy version and entitlements version it carries. *(source: screens/P08-venue-back-office.yaml#BO-207 / screens/P08-venue-back-office.yaml#BO-208 / ADR-0068 / contracts/spine/access.yaml#/components/schemas/OfflinePackage)*
- **Integrity check**: Four ticks before activation - Signature valid, Package complete, Version valid, Device authorised; any cross blocks activation on that device. *(source: screens/P08-venue-back-office.yaml#BO-208 / contracts/spine/access.yaml#listEdgePackageData)*
- **Distribution and device status**: A flow Central platform > Venue edge > Device groups > Individual devices, and per device a status chip Downloaded / Verified / Activated / Failed with the failure reason; counts per status at the top. *(source: screens/P08-venue-back-office.yaml#BO-208)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Publish package**: Confirmation names the version, the target, the device count and devices that will be skipped; devices pick it up at their next refresh and the status chips move from Downloaded to Activated. *(source: contracts/spine/access.yaml#publishHardwareDeployment)*

**Data it reads**: `listEdgePackageData` (onLoad, Edge Package & Data Distribution)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listEdgePackageData`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The edge package data configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the edge package data untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No edge package data configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A deployment to an overlapping target set is still queued or in progress; 422 gateIds or deviceGroupId missing for the chosen targetScope |

#### Edge cases to draw

- **A device fails the integrity check**: It keeps its previous package (shown with its age) and appears as Failed with the check that failed; it is never left with no package. *(source: screens/P08-venue-back-office.yaml#BO-208 / designer default)*
- **Package validity about to end**: Amber "Expires 30 Aug 06:00" on the card and the Packages expiring tile on BO-204. *(source: contracts/spine/access.yaml#listEdgePackageData / contracts/spine/access.yaml#listOfflineEdge)*

#### Consistency with other screens

- Match `SCN-015`: The scanner's offline package screen shows the same version, validity and policy version.
- Match `BO-241`: The policy distribution screen shows the policy version this package carries; same version label.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
package:
  name: AC-EDGE-AUH-1001-V31
  version: '31.2'
  devices: 84
  size: 126 MB
  valid: 1 Oct 2026 06:00 - 2 Oct 2026 06:00
  policyVersion: Guest admission policy 3.5
  status: 'Activated 81, Downloaded 1, Failed 2 (signature invalid: HH-07, HH-09)'
```

#### Permissions

- `listEdgePackageData` → `SCOPE_VIEW` (read) · staff
- `publishHardwareDeployment` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-207` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-207`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 6: Works in Edge Package & Data Distribution → Define what configuration and operational data is securely distributed to edge devices.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-207?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-208` Offline Credential & Revocation Cache

**Manage the local information required to reject credentials that should no longer be usable. This is especially important because Board 3 requires refunded, cancelled, transferred, exchanged, upgraded and reissued credentials to be invalidated.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/offline-credential-revocation-cache-bo-208` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): Save was bound to setOfflinePolicy (tenancy, the POS till policy) with TENANT_CONFIGURE; the gate revocation policy is written by setGateOfflinePolicy, already …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How quickly invalidations reach offline gates and what gates do when their revocation data is too old: which events (fraud lock, refund, cancellation, lost credential, transfer, reissue, manual invalidation) trigger an urgent edge distribution, the current cache age against the maximum allowed, and the staleness action. The one thing to get right: the cache age is the headline (last updated, age, maximum allowed) and the staleness action is explained by its consequence for guests at the gate.

**Known correction pending (do not draw the wrong version)**

- **Content is an empty unbound table** Why: The read listOfflineCredentialRevocation returns the cache age and policy; bind it. *(source: contracts/spine/access.yaml#listOfflineCredentialRevocation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The Save button is bound to setOfflinePolicy (tenancy, the POS till policy - sales, refunds, value ceilings) with TENANT_CONFIGURE (CHG-WIR-001); Three screens write slices of one whole-row PUT, and no read returns the whole row (CHG-WIR-001); Staleness actions "Restricted products only" and "Deny selected credential classes" have nowhere to say which products or classes (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The read returns one cache age per venue; is that the oldest device, the edge node or an average?** → Drawn default accepted: Show it as "Oldest device" and list devices past the maximum. *(decided by Chinmay, 2026-10-02; DEC-248 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **revocationTriggerEvents**: Seven chips under "These events push an urgent update to the gates"; refund, cancellation, transfer, reissue and lost credential are on by default because Board 3 requires those credentials to be invalidated. *(source: screens/P08-venue-back-office.yaml#BO-208 / screens/P08-venue-back-office.yaml#BO-209 / contracts/spine/access.yaml#setGateOfflinePolicy)*
- **revocationMaxAllowedAgeMinutes**: Minutes, whole number, at least 1, default 30 (the pack's example); shown as "Gates trust revocation data up to [30] min old". *(source: screens/P08-venue-back-office.yaml#BO-209 / contracts/spine/access.yaml#setGateOfflinePolicy)*
- **revocationStalenessAction**: Single choice, each with its effect at the gate: Continue; Continue with warning (steward sees "Revocation data 42 min old"); Restricted products only; Supervisor mode (every scan needs a supervisor); Deny selected credential classes; Fail closed (nobody admitted - red, with VO-R16 confirmation on save). *(source: screens/P08-venue-back-office.yaml#BO-209 / contracts/spine/access.yaml#setGateOfflinePolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save gate offline policy (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Cache age**: Three figures "Last updated 10:02:14 / Age 3 min / Maximum allowed 30 min" with a bar that turns amber at 80% and red past the maximum; a list of devices currently past the maximum. *(source: screens/P08-venue-back-office.yaml#BO-209 / contracts/spine/access.yaml#listOfflineCredentialRevocation)*
- **What the cache holds**: Credential cache, revocation list, blacklist, security updates, entitlement snapshot, priority updates, each with its version and time. *(source: screens/P08-venue-back-office.yaml#BO-208)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save revocation policy**: Writes the venue's offline policy row. Because it is one whole row shared with BO-171 and BO-210, the screen must load and resend their values too (VO-R04); confirmation names the venue's gates affected. *(source: contracts/spine/access.yaml#setGateOfflinePolicy)*

**Data it reads**: `listOfflineCredentialRevocation` (onLoad, Offline Credential & Revocation Cache)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listOfflineCredentialRevocation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline credential revocation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline credential revocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline credential revocation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline credential revocation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The edge threshold is shorter than the central one. |

#### Edge cases to draw

- **Gate past the maximum age with Fail closed**: Live consequence shown in red ("2 gates are refusing all guests"), linking to BO-204. *(source: screens/P08-venue-back-office.yaml#BO-209 / contracts/spine/access.yaml#listOfflineCredentialRevocation)*
- **Blacklisted media while a gate is offline**: Urgent distribution is attempted; the device list shows which gates have not yet received it. *(source: screens/P08-venue-back-office.yaml#BO-209 / contracts/spine/access.yaml#/components/schemas/OfflinePackage)*

#### Consistency with other screens

- Match `BO-171`: BO-171, BO-208 and BO-210 edit one offline policy row per venue; draw them as tabs of one Offline policy editor with one Save (VO-R14).
- Match `BO-170`: Revocation lifecycle events are named the same.
- Match `BO-033`: The blacklist the cache carries is the one managed on BO-033 and BO-229.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cache:
  lastUpdated: '10:02:14'
  age: 3 min
  maxAllowed: 30 min
  triggers: Fraud lock, Refund, Cancellation, Lost credential, Transfer, Reissue
  staleness: Continue with warning
devicesPastMax:
- device: North Entry lane 2
  age: 47 min
```

#### Permissions

- `setGateOfflinePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listOfflineCredentialRevocation` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-208` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-208`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 8: Works in Offline Credential & Revocation Cache → Manage the local information required to reject credentials that should no longer be usable. This is especially important because Board 3 requires refunded, cancelled, transferred, exchanged …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-208?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save gate offline policy, Cancel.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-209` Offline Entitlement & Usage Ledger

**Track entitlement consumption while the central system is unavailable. This is necessary for tickets such as: 3 Fast Pass uses 1 park entry 1 meal 1 re-entry where usage can occur during an outage.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/offline-entitlement-usage-ledger-bo-209` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The record of entitlements consumed while gates were offline (Fast Pass uses, park entry, meal, re-entry): credential, device, gate, entitlement, quantity, time, local sequence, operator, decision and package version, with the local balance after each use. A duty manager uses it to see that offline consumption did not double-spend. The one thing to get right: read it per credential as a running balance ("Fast Pass remaining 3 > Ride A -1 = 2 > Ride B -1 = 1"), and mark which entries are still waiting to sync.

**Known correction pending (do not draw the wrong version)**

- **Content is an empty unbound table (pack "gives nothing that can be drawn")** Why: The pack lists the ten stored fields and the read returns them; bind listOfflineEntitlementUsage. *(source: screens/P08-venue-back-office.yaml#BO-209 / contracts/spine/access.yaml#listOfflineEntitlementUsage; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The read has no filters (ticket, gate, date) and no balance-after or sync state** Why: A ledger of offline consumption cannot be investigated without them. *(source: contracts/spine/access.yaml#listOfflineEntitlementUsage; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The risk policy (Online only / Offline allowed - maximum N per entitlement) has no write** Why: The pack makes it configurable for high-risk entitlements. *(source: screens/P08-venue-back-office.yaml#BO-209; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's credential example "VC-908172"** Why: Guests have one ticket number (VT format); show the ticket number and the media code, not a separate credential number. *(source: DI-652 / DI-620; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Ticket number or media code, entitlement, gate, device, date-time range (default today), decision; the read has none yet (see corrections). *(source: designer default / contracts/spine/access.yaml#listOfflineEntitlementUsage)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ledger**: Time to the second, ticket number with media, entitlement, quantity (-1), local balance after, gate, device, local sequence, operator, decision (Admitted / Denied), package version; cursor paging, newest first (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-209 / contracts/spine/access.yaml#listOfflineEntitlementUsage)*
- **Credential view**: Selecting a row shows that ticket's offline uses as a timeline with the balance before the outage and after each use. *(source: screens/P08-venue-back-office.yaml#BO-209)*
- **Duplicate prevention**: Per entry whether the device shared its usage state with the venue edge ("Shared with edge" / "Device only"). *(source: screens/P08-venue-back-office.yaml#BO-209)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open conflict**: An entry that collided with another offline use of the same entitlement links to its conflict on BO-211. *(source: screens/P08-venue-back-office.yaml#BO-212)*

**Data it reads**: `listOfflineEntitlementUsage` (onLoad, Offline Entitlement & Usage Ledger)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listOfflineEntitlementUsage`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline entitlement usage list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline entitlement usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline entitlement usage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline entitlement usage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **High-risk entitlement used offline**: Entitlements configured "Online only" never appear here as admitted; "Offline allowed - maximum 1" shows the cap reached. The configuration has no write yet. *(source: screens/P08-venue-back-office.yaml#BO-209)*
- **Entry not yet synced**: Marked "On device, not synced" with the device's last contact time; synced rows show both scan and sync times. *(source: DI-065 / F06 step 6)*

#### Consistency with other screens

- Match `BO-159`: Entitlement names and units match the entitlement consumption engine.
- Match `SCN-013`: The scanner's offline journal is the device side of this ledger; same columns.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ledger:
- time: 1 Oct 2026 14:02:11
  ticket: VT0010
  media: QR-7F3K-92LD
  entitlement: Fast Pass
  qty: -1
  balanceAfter: 2
  gate: Falcon Coaster FP lane
  device: HH-03
  seq: 1182
  operator: Rahul Menon
  decision: Admitted
  package: '31.2'
- time: 1 Oct 2026 14:19:40
  ticket: VT0010
  entitlement: Fast Pass
  qty: -1
  balanceAfter: 1
  gate: Wave Rider FP lane
  device: WR-01
  seq: 407
  operator: Maria Santos
  decision: Admitted
  package: '31.2'
```

#### Permissions

- `listOfflineEntitlementUsage` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-209` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-209`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 10: Works in Offline Entitlement & Usage Ledger → Track entitlement consumption while the central system is unavailable. This is necessary for tickets such as: 3 Fast Pass uses 1 park entry 1 meal 1 re-entry where usage can occur during an outage.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-209?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-210` Connectivity Failure & Degraded Mode Policy

**Configure how devices transition from normal online operation to offline/degraded operation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/connectivity-failure-degraded-mode-policy-bo-210` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): The gate degraded-mode policy is setGateOfflinePolicy; setOfflinePolicy and setConnectivityThresholds are tenancy policies for POS workstations, keyed by …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How devices step down as connectivity fails - Online, Degraded, Edge mode, Local offline, Unsafe/Expired - after how many seconds, whether automatically, and how each credential class is treated offline (continue, operator review, online required). The one thing to get right: draw the five states as a ladder with the timers on the arrows and what the operator sees in each, so nobody mistakes it for a list of options.

**Known correction pending (do not draw the wrong version)**

- **Content is an empty unbound table and a Save with no operation** Why: The read listConnectivityFailureDegraded returns the timers and states; this is a form, not a list. *(source: contracts/spine/access.yaml#listConnectivityFailureDegraded; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Policy by credential has no field** Why: The pack's four examples need a per-credential-class offline treatment. *(source: screens/P08-venue-back-office.yaml#BO-211; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Three writes bound - setGateOfflinePolicy (no trigger), and the tenancy till policies setOfflinePolicy and setConnectivityThresholds (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should gates use return-online hysteresis (several good responses and a stable period) like POS workstations do?** → Drawn default accepted: Show only the two step-down timers; note that return to online follows the workstation thresholds. *(decided by Chinmay, 2026-10-02; DEC-249 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **centralUnavailableAfterSeconds / edgeUnavailableAfterSeconds**: On the ladder arrows: "Central unavailable for [30] s > Edge mode", "Edge unavailable for [30] s > Local offline". Whole seconds, at least 5. *(source: screens/P08-venue-back-office.yaml#BO-210 / contracts/spine/access.yaml#setGateOfflinePolicy)*
- **automaticSwitch**: On by default ("Switch automatically without stopping guest flow"); off shows a warning that a supervisor must switch each gate. *(source: screens/P08-venue-back-office.yaml#BO-210 / contracts/spine/access.yaml#setGateOfflinePolicy)*
- **operatingModes**: Shown as the fixed ladder; if a venue may skip a state (no edge node, so no Edge mode), that is derived from BO-205, not unticked here. *(source: contracts/spine/access.yaml#setGateOfflinePolicy / designer default)*
- **Policy by credential**: A table of credential classes with Continue offline / Operator review / Online required (Standard day ticket - Continue; Annual pass - Continue; External partner ticket - Operator review; High-risk credential - Online required). Drawn but greyed: no field holds it. *(source: screens/P08-venue-back-office.yaml#BO-210 / screens/P08-venue-back-office.yaml#BO-211)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save gate offline policy (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Operator display preview**: The device banner for each state ("OFFLINE MODE ACTIVE - Package valid - Last sync 10:04"), matching the scanner's offline indicator. *(source: screens/P08-venue-back-office.yaml#BO-210)*
- **Last successful sync**: Time and age for the venue, red past the offline package validity. *(source: contracts/spine/access.yaml#listConnectivityFailureDegraded)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save degraded-mode policy**: Writes the venue's offline policy row with the other screens' values (VO-R04); confirmation names the gates and that it applies at their next refresh. *(source: contracts/spine/access.yaml#setGateOfflinePolicy)*
- **Cancel**: Discards edits and returns to BO-204. *(source: screens/P08-venue-back-office.yaml#BO-210)*

**Data it reads**: `listConnectivityFailureDegraded` (onLoad, Connectivity Failure & Degraded Mode Policy)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listConnectivityFailureDegraded`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The connectivity failure degraded list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the connectivity failure degraded untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No connectivity failure degraded yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the connectivity failure degraded are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The edge threshold is shorter than the central one. |

#### Edge cases to draw

- **Unsafe / Expired**: The bottom rung is red; the operator display says the package is no longer trusted and what the gate does (per the after-threshold behaviour on BO-171). *(source: screens/P08-venue-back-office.yaml#BO-210 / contracts/spine/access.yaml#setGateOfflinePolicy)*
- **Marginal Wi-Fi making a handheld flip between states**: Explain that timers apply both ways; a gate does not return Online on one good response. *(source: contracts/spine/tenancy.yaml#setConnectivityThresholds)*

#### Consistency with other screens

- Match `BO-208`: Same offline policy row; one editor with BO-171 and BO-208 (VO-R14).
- Match `SCN-003`: The offline banner on the scanner uses the state names here (VO-R07).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ladder:
  centralUnavailable: 30 s > Edge mode
  edgeUnavailable: 30 s > Local offline
  automatic: true
  lastSync: '10:04'
byCredential:
- class: Standard day ticket
  offline: Continue
- class: Annual pass
  offline: Continue
- class: External partner ticket
  offline: Operator review
- class: High-risk credential
  offline: Online required
```

#### Permissions

- `setGateOfflinePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listConnectivityFailureDegraded` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-210` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-210`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 12: Works in Connectivity Failure & Degraded Mode Policy → Configure how devices transition from normal online operation to offline/degraded operation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-210?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save gate offline policy, Cancel.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-211` Reconnection, Synchronization & Conflict Resolution

**Synchronize everything that occurred offline when connectivity returns.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/reconnection-synchronization-conflict-resolution-bo-211` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** What happens when a gate reconnects: the ten-step reconnection workflow (authenticate, upload, sequence, reconcile credentials and entitlements, update attendance, resolve conflicts, download configuration, return online), the sync queue counts, and the conflicts where two offline gates used the same entitlement. The one thing to get right: no access transaction is ever silently discarded - every conflict shows both transactions side by side and a resolution that a person or a stated rule applied.

**Known correction pending (do not draw the wrong version)**

- **The conflict row holds only the credential, balance before the outage and the resolution policy** Why: A conflict cannot be judged without the transactions that collided (gate, device, time, operator). *(source: screens/P08-venue-back-office.yaml#BO-212 / contracts/spine/access.yaml#listReconnectionSynchronizationConflict; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No write resolves a conflict or sets the default resolution policy** Why: The pack lists resolution policies and requires a complete audit trail of reconciliation. *(source: screens/P08-venue-back-office.yaml#BO-212; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every reconnection synchronization conflict" and "The selected ..."** Why: Generated placeholders; "Sync conflicts" (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resolution policy**: Choice of Preserve both and flag (default), Earliest transaction wins, Configured business rule, Supervisor review, Security investigation; a reason is required for the last two. *(source: screens/P08-venue-back-office.yaml#BO-212 / contracts/spine/access.yaml#listReconnectionSynchronizationConflict)*

#### Outputs: what the screen shows and produces

**Shown**

**Every reconnection synchronization conflict** (data table, from `listReconnectionSynchronizationConflict`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Conflict | text | Conflict identifier |
| Central remaining balance before outage | 1,234 | Entitlement uses remaining centrally before the outage (a count, not money) |
| Resolution policy | chip: Preserve both and flag, Earliest transaction wins, Configured business rule … | How this conflict is resolved |
| Credential | text | Credential involved |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Pending scans | 1,234 | Pending scans |
| Entitlement events | 1,234 | Entitlement events |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Overrides | 1,234 | Overrides |
| Security events | 1,234 | Security events |

**The selected reconnection synchronization conflict** (detail panel): The pack groups this record's detail under its own headings: “Connectivity Restored”, “Authenticate”, “Upload Offline Transactions”, “Sequence Events”, “Reconcile Credential State”, “Reconcile Entitlements”.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Sync queue tiles**: Pending scans, Entitlement events, Entries, Exits, Overrides, Security events as tiles above the list (VO-R02), with "as of" time. *(source: screens/P08-venue-back-office.yaml#BO-211 / contracts/spine/access.yaml#listReconnectionSynchronizationConflict)*
- **Reconnection progress**: Per reconnecting device or edge node, the ten steps as a horizontal rail with the current step and any failed step. *(source: screens/P08-venue-back-office.yaml#BO-211)*
- **Conflict list**: One row per conflict: ticket number, entitlement, balance before the outage, the two (or more) transactions (gate, device, time, operator), resolution policy and status. Open conflicts first. *(source: screens/P08-venue-back-office.yaml#BO-212 / contracts/spine/access.yaml#listReconnectionSynchronizationConflict)*
- **Conflict detail**: Both transactions side by side with the ticket's scan history; the outcome wording keeps "used" as used (a successful scan stays used even if the guest did not pass). *(source: screens/P08-venue-back-office.yaml#BO-212 / DI-627)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resolve conflict**: Records the policy applied, by whom and why; the transactions remain in history. Drawn greyed until an operation exists. *(source: screens/P08-venue-back-office.yaml#BO-212)*
- **Open investigation**: For Security investigation, opens BO-252 with the ticket and both transactions attached. *(source: contracts/spine/access.yaml#setSecurityInvestigationEvidence)*

**Data it reads**: `listReconnectionSynchronizationConflict` (onLoad, Reconnection, Synchronization & Conflict Resolution)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listReconnectionSynchronizationConflict`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reconnection synchronization conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reconnection synchronization conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reconnection synchronization conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reconnection synchronization conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Large backlog after a long outage**: Counts show progress ("4,821 pending scans, uploading"); attendance figures say "Updating after reconnection" until done. *(source: screens/P08-venue-back-office.yaml#BO-211)*
- **Sync rejected for a scan the device admitted**: Goes to the duty manager's reconciliation review, not dropped. *(source: F06 step 6 / DI-065)*

#### Consistency with other screens

- Match `BO-038`: The reconciliation queue is where rejected offline scans are reviewed; conflicts here and rows there must not be two lists of the same thing (VO-R14).
- Match `SCN-014`: Scanner sync and reconciliation uses the same counts and words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
  pendingScans: 4821
  entitlementEvents: 682
  entries: 3240
  exits: 1204
  overrides: 18
  securityEvents: 7
conflict:
  ticket: VT0418
  entitlement: Fast Pass
  balanceBefore: 1
  a: Falcon Coaster FP, 13:02, HH-03, Rahul Menon
  b: Wave Rider FP, 13:09, WR-01, Maria Santos
  result: CONFLICT
  policy: Preserve both and flag
```

#### Permissions

- `listReconnectionSynchronizationConflict` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-211` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-211`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 14: Works in Reconnection, Synchronization & Conflict Resolution → Synchronize everything that occurred offline when connectivity returns.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-211?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-212` Offline Simulation & Resilience Testing

**Allow venues to prove that their access environment will survive outages before opening to guests.**

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
| Route | `/access-venue/offline-simulation-resilience-testing-bo-212` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** A pre-opening drill: pick an outage scenario, run it against a venue without touching live gates, and see each check pass or fail (edge mode switch, dynamic QR verified locally, date and entitlement verified, anti-passback, gate opens, attendance stored, transaction queued), plus a load test (10,000 validations over a 2-hour outage) measuring speed, storage, sync time and error rate. The one thing to get right: the checks are results the system reports, not boxes the user ticks.

**Known correction pending (do not draw the wrong version)**

- **The eight checks and the edge-mode switch are request inputs (booleans) and the screen draws nothing for them** Why: They are what the run reports; they belong in the response, with `result`. *(source: contracts/spine/access.yaml#simulateOfflineResilienceTesting; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Scenario enum has three values against the pack's ten** Why: Revocation cache stale, expired package, device isolated and reconnect after an extended outage are the scenarios that test BO-208 to BO-211. *(source: screens/P08-venue-back-office.yaml#BO-212 / contracts/spine/access.yaml#simulateOfflineResilienceTesting; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The load test has a count but no duration and returns no measurements** Why: The pack measures speed, storage, synchronisation time and error rate over a stated outage. *(source: screens/P08-venue-back-office.yaml#BO-213; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The simulation is a PUT** Why: A run is a new result each time, not an upsert; past runs need a history to show readiness before opening. *(source: contracts/spine/access.yaml#simulateOfflineResilienceTesting; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should past simulation runs be kept as evidence of readiness (per venue, per release)?** → Drawn default accepted: Draw a "Previous runs" list greyed. *(decided by Chinmay, 2026-10-02; DEC-250 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **scenario**: The pack's ten scenarios as cards (Central API failure, Database unavailable, Internet failure, Venue WAN failure, Edge node failure, Device isolated, Revocation cache stale, Expired edge package, High offline volume, Reconnect after extended outage); only the three the contract has are enabled. *(source: screens/P08-venue-back-office.yaml#BO-212 / contracts/spine/access.yaml#simulateOfflineResilienceTesting)*
- **Load test (validationCount, duration)**: Number of validations (default 10,000) and outage length (default 2 hours); duration is greyed (no field). *(source: screens/P08-venue-back-office.yaml#BO-213 / contracts/spine/access.yaml#simulateOfflineResilienceTesting)*
- **venueId**: The top-bar venue; optionally narrowed to a gate group (not in the contract). *(source: designer default)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run simulation (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Check list**: The eight checks as rows that fill in as the run proceeds, ticks or crosses with the reason, then the verdict "OFFLINE READINESS: PASSED" in green or FAILED in red with the failed checks first. *(source: screens/P08-venue-back-office.yaml#BO-213 / contracts/spine/access.yaml#simulateOfflineResilienceTesting)*
- **Load results**: Validation speed (ms per scan), storage used, synchronisation time and error rate. *(source: screens/P08-venue-back-office.yaml#BO-213)*
- **AI resilience advisor**: A projection with its basis ("Main Entrance can operate about 11 hours at projected peak before local storage reaches its warning level"); advisory. *(source: screens/P08-venue-back-office.yaml#BO-213)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Run simulation**: Runs against a simulated copy; no real scan, attendance or entitlement change. Confirmation says so. *(source: DI-629 / contracts/spine/access.yaml#simulateOfflineResilienceTesting)*
- **Cancel**: Stops a running simulation and returns to BO-204. *(source: screens/P08-venue-back-office.yaml#BO-212)*

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `simulateOfflineResilienceTesting`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline simulation resilience list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline simulation resilience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline simulation resilience yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline simulation resilience are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Simulation while gates are live**: Allowed; a banner states live gates are not affected. *(source: DI-629)*

#### Consistency with other screens

- Match `BO-163`: The rule simulation tool uses the same "virtual scan, no real transaction" wording.
- Match `BO-213`: A passed offline simulation is a stage of the edge deployment lifecycle (Offline simulation); link the latest result there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
run:
  venue: Aqua Park
  scenario: Central API failure
  validations: 10000
  outage: 2 hours
  result: PASSED
  speed: 310 ms per scan
  storage: 412 MB of 2 GB
  syncTime: 6 min 40 s
  errorRate: 0.02%
```

#### Permissions

- `simulateOfflineResilienceTesting` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-212` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-212`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 16: Works in Offline Simulation & Resilience Testing → Allow venues to prove that their access environment will survive outages before opening to guests.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-212?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run simulation, Cancel.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-213` Edge Security, Audit & Deployment

**Govern the complete offline/edge environment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `alertId` (navigation) |
| Route | `/access-venue/edge-security-audit-deployment-bo-213` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No operation rolls back an edge policy version or runs the four edge emergency actions.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Governance of the edge estate: security tiles (certificates and credentials, package signatures, authorised and revoked devices, failed package validation, unauthorised connection attempts, configuration changes, offline override activity), edge policy versions moving through Draft > Validate > Security test > Offline simulation > Approval > Pilot > Publish, what is in production and what is scheduled, rollback, the audit trail and the emergency actions. The one thing to get right: production and scheduled versions are unmistakable ("Current production V4.7 - Scheduled V4.8 tonight 02:00") and emergency actions are fast but confirmed.

**Known correction pending (do not draw the wrong version)**

- **Edge certificates/credentials drawn as the only table column; offline override activity tile missing** Why: Both are summary tiles; the table lists edge policy versions. *(source: contracts/spine/access.yaml#listEdgeSecurityDeployment; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Rollback and the four emergency actions have no operations; the only write is updateSecurityAlert** Why: The pack makes them the screen's purpose ("must restore", "authorised security administrators can"). *(source: screens/P08-venue-back-office.yaml#BO-213; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Button "Save security alert" in the action bar** Why: An alert move only makes sense when opened from an alert; draw it inside the alert drawer with Acknowledge / Resolve / Dismiss labels. *(source: contracts/spine/access.yaml#updateSecurityAlert; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every edge security audit" and "The selected edge security audit"** Why: Generated placeholders; "Edge policy versions" (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Form: Save security alert** (modal, opened by *Save security alert*; *Save security alert* calls `updateSecurityAlert`, *Cancel* sends nothing)

**Collects what `updateSecurityAlert` sends before it is called.** Required: `status`. Optional: `note`, `securityInvestigationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Acknowledged · Resolved · Dismissed | — | — | `updateSecurityAlert` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `updateSecurityAlert` body |
| Security investigation `securityInvestigationId` | picker: choose a security investigation | optional | — | — | shows names, sends the id | — | `updateSecurityAlert` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The alert is already resolved or dismissed.

#### Outputs: what the screen shows and produces

**Shown**

**Package signatures** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**Authorized devices** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**Revoked devices** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**Failed package validation** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**unauthorized connection attempts** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**configuration changes** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**Every edge security audit** (data table, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Edge certificates/credentials | text | not in the schema: `Edge certificates/credentials` |

**The selected edge security audit** (detail panel): The pack groups this record's detail under its own headings: “Draft”, “Deployment Scope”, “Current Production”, “Scheduled”, “Rollback”, “FORCE ONLINE-ONLY”.

| Shows | Format | Notes |
|---|---|---|
| Edge certificates/credentials | text | not in the schema: `Edge certificates/credentials` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save security alert (primary button) | `updateSecurityAlert` POST `/security-alerts/{alertId}/status` | inline | AccessSecurityAlert | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `INCIDENT_MANAGE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Security tiles**: The nine summary counts as tiles; failed validation and unauthorised attempts red when above zero (VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-213 / contracts/spine/access.yaml#listEdgeSecurityDeployment)*
- **Version list**: Edge policy versions with stage on a seven-step rail, deployment scope (tenant, venue, park, edge cluster, gate group, device group, device), Production badge, scheduled time in venue time. *(source: screens/P08-venue-back-office.yaml#BO-213 / contracts/spine/access.yaml#listEdgeSecurityDeployment)*
- **Audit**: Who changed what, when, previous and new value, approval, deployment target and result, read-only. *(source: screens/P08-venue-back-office.yaml#BO-213 / contracts/spine/tenancy.yaml#listAuditRecords)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Roll back to V4.7**: Confirmation lists what is restored (offline rules, device configuration, security policy, edge package definitions) and the devices reached. Greyed (no operation). *(source: screens/P08-venue-back-office.yaml#BO-213)*
- **Emergency actions (Revoke edge package, Disable device, Force resync, Force online-only)**: Security administrators only; each opens a confirmation naming the consequence and the devices affected with a reason, and creates an audit record. Greyed (no operations). *(source: screens/P08-venue-back-office.yaml#BO-213)*
- **Acknowledge / Resolve / Dismiss alert**: When opened from an alert (alertId), an alert drawer with the three moves and a note (max 1,000); a resolved or dismissed alert cannot move again (409 shown as "This alert is already closed"). *(source: contracts/spine/access.yaml#updateSecurityAlert)*

**Data it reads**: `listEdgeSecurityDeployment` (onLoad, Edge Security, Audit & Deployment)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The edge security audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the edge security audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No edge security audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the edge security audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The alert is already resolved or dismissed. |

#### Edge cases to draw

- **Scheduled version due while a gate is offline**: The gate keeps the production version until it reconnects; the version row shows "Applied on 81 / 84 devices". *(source: screens/P08-venue-back-office.yaml#BO-213 / contracts/spine/access.yaml#publishHardwareDeployment)*

#### Consistency with other screens

- Match `BO-212`: The Offline simulation stage shows the latest BO-212 result.
- Match `BO-244`: Security alerts use the same alert drawer and statuses on the fraud command centre.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  certificates: 3
  credentials: 171
  packageSignatures: 171
  authorisedDevices: 171
  revokedDevices: 2
  failedValidation: 2
  unauthorisedAttempts: 0
  configChanges: 14
  offlineOverrides: 6
versions:
- version: V4.7
  stage: Published
  scope: Venue Aqua Park
  production: true
- version: V4.8
  stage: Approved
  scope: Venue Aqua Park
  scheduled: 2 Oct 2026 02:00 (tonight)
  approvedBy: Omar Haddad
```

#### Permissions

- `listEdgeSecurityDeployment` → `SCOPE_VIEW` (read) · staff
- `updateSecurityAlert` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-213` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-213`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 18: Works in Edge Security, Audit & Deployment → Govern the complete offline/edge environment.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (110 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-213?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save security alert.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listConnectivityFailureDegraded": {"method":"GET","path":"/connectivity-failure-degraded","contract":"access","summary":"Connectivity Failure & Degraded Mode Policy","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConnectivityFailureDegradedModePolicyView"},
"listEdgePackageData": {"method":"GET","path":"/edge-package-data","contract":"access","summary":"Edge Package & Data Distribution","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEdgeSecurityDeployment": {"method":"GET","path":"/edge-security-deployment","contract":"access","summary":"Edge Security, Audit & Deployment","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOfflineCredentialRevocation": {"method":"GET","path":"/offline-credential-revocation","contract":"access","summary":"Offline Credential & Revocation Cache","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OfflineCredentialRevocationCacheView"},
"listOfflineEdge": {"method":"GET","path":"/offline-edge","contract":"access","summary":"Offline & Edge Operations Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOfflineEntitlementUsage": {"method":"GET","path":"/offline-entitlement-usage","contract":"access","summary":"Offline Entitlement & Usage Ledger","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReconnectionSynchronizationConflict": {"method":"GET","path":"/reconnection-synchronization-conflict","contract":"access","summary":"Reconnection, Synchronization & Conflict Resolution","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishHardwareDeployment": {"method":"POST","path":"/hardware-deployments","contract":"access","summary":"Deploy a gate configuration version","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"HardwareDeploymentInput","responds":"HardwareDeploymentView"},
"setEdgeNodeLocal": {"method":"PUT","path":"/edge-node-local","contract":"access","summary":"Edge Node & Local Processing Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EdgeNodeLocalProcessingConfigurationInput","responds":"EdgeNodeLocalProcessingConfigurationView"},
"setGateOfflinePolicy": {"method":"PUT","path":"/offline-policies","contract":"access","summary":"Set the offline policy of a venue","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessOfflinePolicy","responds":"AccessOfflinePolicy"},
"simulateOfflineResilienceTesting": {"method":"PUT","path":"/offline-resilience-testing","contract":"access","summary":"Offline Simulation & Resilience Testing","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OfflineSimulationResilienceTestingInput","responds":"OfflineSimulationResilienceTestingView"},
"updateSecurityAlert": {"method":"POST","path":"/security-alerts/{alertId}/status","contract":"access","summary":"Acknowledge, resolve or dismiss a security alert","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessSecurityAlert"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessOfflinePolicy": {"type":"object","x-ticvai-persistence":"access.offline_policy","description":"The offline policy of one venue: what gates validate locally and for how long, how old the revocation cache may get, and how devices step down through degraded modes. Merges access.offline_validation_profile, access.revocation_cache_policy and access.degraded_mode_policy (declared 29 September, data-model close-out DM1)","required":["id","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"maxOfflineDurationHours":{"type":"integer","minimum":0,"nullable":true,"description":"**Hours a reader may validate offline; past it, readers refuse offline taps** (decided 2 October 2026, Chinmay, critical set 1, BO-471: \"Yes: the venue sets a maximum offline duration; readers then refuse offline taps\"; DEC-426; CHG-CSP-035). Counted from the reader's last successful sync. Past the limit an access gate, a handheld and a games reader refuse every tap they would have validated from their local package (`ValidationResult.denyCause` `offlineLimitExceeded`) until they reconnect; `afterThresholdBehavior` decides only what the operator is shown and whether a supervisor may admit by hand (`supervisorMode`), and none of its values lets a reader keep validating unattended. The limit travels in the offline package (ADR-0068), so a reader that has lost the platform still knows it. Null sets no limit beyond the package's own expiry."},"offlineChecks":{"type":"array","items":{"type":"string","enum":["credentialAuthenticity","digitalSignature","ticketId","venue","park","zone","visitDate","timeWindow","credentialStatusSnapshot","ticketType","guestCategory","seat","timeslot","reservation","entitlements","reEntryPermissions","validityPeriod"]},"description":"What a gate may validate locally"},"afterThresholdBehavior":{"type":"string","enum":["continueRestrictedValidation","operatorWarning","supervisorMode","failClosed","fallback"],"nullable":true},"revocationTriggerEvents":{"type":"array","items":{"type":"string","enum":["fraudLock","refund","cancellation","lostCredential","transfer","reissue","manualInvalidation"]},"description":"Events that push an invalidation into the offline cache"},"revocationMaxAllowedAgeMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"Maximum allowed revocation cache age"},"revocationStalenessAction":{"type":"string","enum":["continue","continueWithWarning","restrictedProductsOnly","supervisorMode","denySelectedCredentialClasses","failClosed"],"nullable":true,"description":"What devices do when the cache is older than the maximum allowed age"},"operatingModes":{"type":"array","items":{"type":"string","enum":["online","degraded","edgeMode","localOffline","unsafeExpired"]},"description":"Operating modes a device moves through as connectivity fails"},"centralUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without central services before switching to edge mode"},"edgeUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without the venue edge before switching to local offline"},"automaticSwitch":{"type":"boolean","default":true,"description":"Switch modes automatically without stopping guest flow"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessSecurityAlert": {"type":"object","x-ticvai-persistence":"access.security_alert","description":"One access security or fraud alert - severity, what was detected, where and on which credential, identity or device - including biometric anomalies and edge security events (certificate, credential or package-signature failures, unauthorised connections, device authorisation and revocation). Merges the proposed access.security_alert and access.edge_security_event (declared 29 September, data-model close-out DM1). Created `open` by the detection jobs (fraud rules, sharing detection, biometric anomaly, edge security events) and moved by updateSecurityAlert; the lifecycle is states/access-security-alert.yaml (decided 29 September, writers pass).","required":["id","scopePath","category","severity","status","detectedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The alertId / anomalyId the lists show"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"category":{"type":"string","enum":["fraudSignal","credentialSharing","duplicateAccess","blacklist","biometric","companion","edgeSecurity"]},"alertType":{"type":"string","maxLength":60,"nullable":true,"description":"The kind within the category - for fraudSignal the fraud rule's signal; for biometric one of faceChanged, reEnrollment, repeatedFaceMismatch, multipleFacesOneCredential, oneFaceMultipleCredentials, suspiciousEnrollmentFrequency, unusualVerificationFailures; for edgeSecurity one of certificateFailure, credentialFailure, packageSignatureFailure, unauthorizedConnection, deviceAuthorized, deviceRevoked"},"severity":{"type":"string","enum":["low","medium","high","critical"]},"description":{"type":"string","maxLength":500,"nullable":true,"description":"e.g. Credential attempted simultaneous entry at two gates"},"fraudRuleId":{"type":"string","format":"uuid","nullable":true,"description":"The access fraud rule that raised the alert, if one did"},"entitlementId":{"type":"string","format":"uuid","nullable":true,"description":"The credential (the list's credentialId)"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The identity concerned, where known"},"zoneId":{"type":"string","format":"uuid","nullable":true},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"The gate (the list's gateId)"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"The device concerned, for device-sharing and edge events"},"faceReenrolmentAttemptId":{"type":"string","format":"uuid","nullable":true,"description":"Biometric alerts raised on a re-enrolment; the attempt holds the old and new references, operator, reason and review"},"faceProfileReference":{"type":"string","maxLength":200,"nullable":true,"description":"Biometric alerts. Opaque Face Pass reference; never a template"},"securityInvestigationId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["open","acknowledged","resolved","dismissed"],"default":"open"},"detectedAt":{"type":"string","format":"date-time"},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}},
"ConnectivityFailureDegradedModePolicyView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Connectivity Failure & Degraded Mode Policy displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue"},"operatingModes":{"type":"array","items":{"type":"string","enum":["online","degraded","edgeMode","localOffline","unsafeExpired"]},"description":"Operating modes a device moves through as connectivity fails"},"centralUnavailableAfterSeconds":{"type":"integer","description":"Seconds without central services before switching to edge mode"},"edgeUnavailableAfterSeconds":{"type":"integer","description":"Seconds without the venue edge before switching to local offline"},"automaticSwitch":{"type":"boolean","description":"Switch modes automatically without stopping guest flow"},"lastSyncAt":{"type":"string","format":"date-time","description":"Last successful synchronization"}},"required":["venueId"]},
"EdgeNodeLocalProcessingConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Edge Node & Local Processing Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"nodeType":{"type":"string","enum":["venueEdgeNode","gateController","turnstileLocalEngine","handheldLocalEngine"],"description":"Which edge component makes local access decisions"},"edgeNodeId":{"type":"string","description":"Edge Node ID"},"tenantId":{"type":"string","description":"Tenant"},"venueId":{"type":"string","description":"Venue"},"network":{"type":"string","description":"Network"},"deviceGroup":{"type":"string","description":"Device Group"},"processingMode":{"type":"string","description":"Processing Mode"},"storageAllocation":{"type":"string","description":"Storage allocation"},"redundancy":{"type":"string","description":"redundancy"},"lastHeartbeat":{"type":"string","format":"date-time","description":"Last heartbeat, set by the node, read only"},"softwareVersion":{"type":"string","description":"software version"},"securityStatus":{"type":"string","description":"security status"}},"required":["edgeNodeId","venueId","nodeType"]},
"EdgeNodeLocalProcessingConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Edge Node & Local Processing Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"nodeType":{"type":"string","enum":["venueEdgeNode","gateController","turnstileLocalEngine","handheldLocalEngine"],"description":"Which edge component makes local access decisions"},"edgeNodeId":{"type":"string","description":"Edge Node ID"},"tenantId":{"type":"string","description":"Tenant"},"venueId":{"type":"string","description":"Venue"},"network":{"type":"string","description":"Network"},"deviceGroup":{"type":"string","description":"Device Group"},"processingMode":{"type":"string","description":"Processing Mode"},"storageAllocation":{"type":"string","description":"Storage allocation"},"redundancy":{"type":"string","description":"redundancy"},"lastHeartbeat":{"type":"string","format":"date-time","description":"Last heartbeat, set by the node, read only"},"softwareVersion":{"type":"string","description":"software version"},"securityStatus":{"type":"string","description":"security status"}},"required":["edgeNodeId","venueId","nodeType"]},
"EdgePackageDataDistributionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Edge Package & Data Distribution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"packageId":{"type":"string","description":"Edge package identifier"},"contents":{"type":"array","items":{"type":"string","enum":["venues","zones","gates","accessRules","calendars","mediaProfiles","verificationProfiles","entitlementDefinitions","trustedVerificationMaterial","revocationInformation","credentialSecurityParameters","reasonCodes","gateResponses","languages","operatorPermissions"]},"description":"Data sets included in this edge package"},"version":{"type":"string","description":"Version (the pack shows 24.6, 89 | Pag e)"},"devices":{"type":"integer","description":"Devices (the pack shows 84)"},"signatureValid":{"type":"boolean","description":"✓ Signature valid"},"packageComplete":{"type":"boolean","description":"✓ Package complete"},"versionValid":{"type":"boolean","description":"✓ Version valid"},"deviceAuthorized":{"type":"boolean","description":"✓ Device authorized"},"sizeBytes":{"type":"integer","description":"Package size"},"validFrom":{"type":"string","format":"date-time","description":"Valid from"},"validTo":{"type":"string","format":"date-time","description":"Valid to"}},"required":["packageId"]},
"EdgeSecurityAuditDeploymentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Edge Security, Audit & Deployment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"policyVersionId":{"type":"string","description":"Edge policy version identifier"},"deploymentScope":{"type":"string","enum":["tenant","venue","park","edgeCluster","gateGroup","deviceGroup","individualDevice"],"description":"Where this edge policy version deploys"},"version":{"type":"string","description":"Version label, e.g. V4.8"},"stage":{"type":"string","enum":["draft","validated","securityTested","offlineSimulated","approved","pilot","published"],"description":"Release stage"},"isProduction":{"type":"boolean","description":"Currently in production"},"scheduledAt":{"type":"string","format":"date-time","description":"Scheduled deployment time"}},"required":["policyVersionId"]},
"EdgeSecurityAuditDeploymentViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"edgeCertificates":{"type":"integer","description":"Edge certificates"},"edgeCredentials":{"type":"integer","description":"Edge credentials"},"packageSignatures":{"type":"integer","description":"Package signatures"},"authorizedDevices":{"type":"integer","description":"Authorized devices"},"revokedDevices":{"type":"integer","description":"Revoked devices"},"failedPackageValidation":{"type":"integer","description":"Failed package validation"},"unauthorizedConnectionAttempts":{"type":"integer","description":"unauthorized connection attempts"},"configurationChanges":{"type":"integer","description":"configuration changes"},"offlineOverrideActivity":{"type":"integer","description":"offline override activity"}}},
"HardwareDeploymentInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Deploy one gate configuration version to a target set (decided 29 September, VM close-out).","required":["id","configurationVersion","targetScope","venueId"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated deployment id"},"configurationVersion":{"type":"string","description":"The access configuration version being deployed"},"targetScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"]},"venueId":{"type":"string"},"gateIds":{"type":"array","items":{"type":"string"},"description":"Required for pilot and selectedGates"},"deviceGroupId":{"type":"string","description":"Required for deviceGroup"},"runCompatibilityTestFirst":{"type":"boolean","default":true,"description":"Devices that fail the compatibility test are skipped and named in the result"},"scheduledAt":{"type":"string","format":"date-time","description":"Empty deploys now"}}},
"HardwareDeploymentView": {"type":"object","x-ticvai-persistence":"access.hardware_deployment","description":"**One rollout of one gate configuration version to one target set** (decided 29 September, VM close-out). The lifecycle is the one `tenancy.ProfileDeployment` uses for configuration profiles, so a partial failure is visible and retried or rolled back, never an end state.","required":["id","configurationVersion","targetScope","status"],"properties":{"id":{"type":"string","format":"uuid"},"configurationVersion":{"type":"string"},"targetScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"]},"venueId":{"type":"string"},"gateIds":{"type":"array","items":{"type":"string"}},"deviceGroupId":{"type":"string"},"status":{"type":"string","enum":["queued","inProgress","completed","partiallyFailed","rolledBack"]},"devicesTargeted":{"type":"integer"},"devicesAcknowledged":{"type":"integer"},"failedDeviceIds":{"type":"array","items":{"type":"string"},"description":"Devices that failed the compatibility test or did not acknowledge"},"requestedByPrincipalId":{"type":"string"},"requestedAt":{"type":"string","format":"date-time"},"scheduledAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"The partition key (ADR-0005). Written at venue scope"}}},
"OfflineCredentialRevocationCacheView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline Credential & Revocation Cache displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue"},"triggerEvents":{"type":"array","items":{"type":"string","enum":["fraudLock","refund","cancellation","lostCredential","transfer","reissue","manualInvalidation"]},"description":"Events that push an invalidation into the offline cache"},"stalenessAction":{"type":"string","enum":["continue","continueWithWarning","restrictedProductsOnly","supervisorMode","denySelectedCredentialClasses","failClosed"],"description":"What devices do when the cache is older than the maximum allowed age"},"lastUpdated":{"type":"string","format":"date-time","description":"When the cache was last refreshed"},"ageSeconds":{"type":"integer","description":"Current cache age"},"maxAllowedAgeMinutes":{"type":"integer","description":"Maximum allowed cache age"}},"required":["venueId"]},
"OfflineEdgeOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline & Edge Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue"},"rulesCached":{"type":"boolean","description":"✓ Rules cached"},"verificationMaterialCurrent":{"type":"boolean","description":"✓ Verification material current"},"revocationDataCurrent":{"type":"boolean","description":"✓ Revocation data current"},"credentialDefinitionsAvailable":{"type":"boolean","description":"✓ Credential definitions available"},"deviceStorageHealthy":{"type":"boolean","description":"✓ Device storage healthy"},"lastSynchronizationSuccessful":{"type":"boolean","description":"✓ Last synchronization successful"},"venueName":{"type":"string","description":"Venue name"},"devices":{"type":"integer","description":"Devices at the venue"},"offlineReady":{"type":"integer","description":"Devices ready to operate offline"},"readinessPercent":{"type":"number","description":"Share of devices offline ready"},"packageStatus":{"type":"string","enum":["current","expiring","expired"],"description":"Edge package status"},"pendingTransactions":{"type":"integer","description":"Offline transactions not yet synchronized"},"readinessStatus":{"type":"string","enum":["ready","warning","notReady"],"description":"Venue readiness"}},"required":["venueId"]},
"OfflineEdgeOperationsCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"offlineReadyDevices":{"type":"integer","description":"Offline-Ready Devices"},"currentlyOnline":{"type":"integer","description":"Currently Online"},"currentlyOffline":{"type":"integer","description":"Currently Offline"},"devicesInDegradedMode":{"type":"integer","description":"Devices in Degraded Mode"},"edgeNodesOnline":{"type":"integer","description":"Edge Nodes Online"},"packagesCurrent":{"type":"integer","description":"Packages Current"},"packagesExpiring":{"type":"integer","description":"Packages Expiring"},"pendingOfflineTransactions":{"type":"integer","description":"Pending Offline Transactions"},"syncConflicts":{"type":"integer","description":"Sync conflicts"},"offlineSecurityAlerts":{"type":"integer","description":"Offline Security Alerts"}}},
"OfflineEntitlementUsageLedgerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline Entitlement & Usage Ledger displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ledgerEntryId":{"type":"string","description":"Ledger entry identifier"},"credential":{"type":"string","description":"Credential"},"device":{"type":"string","description":"Device"},"gate":{"type":"string","description":"Gate"},"entitlement":{"type":"string","description":"Entitlement"},"quantity":{"type":"integer","description":"Quantity"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"localSequence":{"type":"integer","description":"Device-local sequence number"},"operator":{"type":"string","description":"operator"},"decision":{"type":"string","description":"decision"},"packageVersion":{"type":"string","description":"package version"}},"required":["ledgerEntryId"]},
"OfflineSimulationResilienceTestingInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Offline Simulation & Resilience Testing submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"scenario":{"type":"string","enum":["centralOutage","edgeOutage","fullOffline"],"description":"Outage scenario to simulate"},"venueId":{"type":"string","description":"Venue under test"},"dynamicQrVerifiedLocally":{"type":"boolean","description":"✓ Dynamic QR verified locally"},"ticketDateVerified":{"type":"boolean","description":"✓ Ticket date verified"},"entryEntitlementVerified":{"type":"boolean","description":"✓ Entry entitlement verified"},"antiPassbackEnforced":{"type":"boolean","description":"✓ Anti-passback enforced"},"gateOpens":{"type":"boolean","description":"✓ Gate opens"},"attendanceStoredLocally":{"type":"boolean","description":"✓ Attendance stored locally"},"transactionQueued":{"type":"boolean","description":"✓ Transaction queued"},"validationCount":{"type":"integer","description":"Number of simulated validations"},"switchedToEdgeMode":{"type":"boolean","description":"Gate switched to edge mode"},"result":{"type":"string","enum":["passed","failed"],"description":"Offline readiness result, read only"}},"required":["venueId","scenario"]},
"OfflineSimulationResilienceTestingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline Simulation & Resilience Testing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"scenario":{"type":"string","enum":["centralOutage","edgeOutage","fullOffline"],"description":"Outage scenario to simulate"},"venueId":{"type":"string","description":"Venue under test"},"dynamicQrVerifiedLocally":{"type":"boolean","description":"✓ Dynamic QR verified locally"},"ticketDateVerified":{"type":"boolean","description":"✓ Ticket date verified"},"entryEntitlementVerified":{"type":"boolean","description":"✓ Entry entitlement verified"},"antiPassbackEnforced":{"type":"boolean","description":"✓ Anti-passback enforced"},"gateOpens":{"type":"boolean","description":"✓ Gate opens"},"attendanceStoredLocally":{"type":"boolean","description":"✓ Attendance stored locally"},"transactionQueued":{"type":"boolean","description":"✓ Transaction queued"},"validationCount":{"type":"integer","description":"Number of simulated validations"},"switchedToEdgeMode":{"type":"boolean","description":"Gate switched to edge mode"},"result":{"type":"string","enum":["passed","failed"],"description":"Offline readiness result, read only"}},"required":["venueId","scenario"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReconnectionSynchronizationConflictResolutionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Reconnection, Synchronization & Conflict Resolution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"conflictId":{"type":"string","description":"Conflict identifier"},"centralRemainingBalanceBeforeOutage":{"type":"integer","description":"Entitlement uses remaining centrally before the outage (a count, not money)"},"resolutionPolicy":{"type":"string","enum":["preserveBothAndFlag","earliestTransactionWins","configuredBusinessRule","supervisorReview","securityInvestigation"],"description":"How this conflict is resolved"},"credentialId":{"type":"string","description":"Credential involved"}},"required":["conflictId"]},
"ReconnectionSynchronizationConflictResolutionViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"pendingScans":{"type":"integer","description":"Pending scans"},"entitlementEvents":{"type":"integer","description":"Entitlement events"},"entries":{"type":"integer","description":"Entries"},"exits":{"type":"integer","description":"Exits"},"overrides":{"type":"integer","description":"Overrides"},"securityEvents":{"type":"integer","description":"Security events"}}}
}
```
