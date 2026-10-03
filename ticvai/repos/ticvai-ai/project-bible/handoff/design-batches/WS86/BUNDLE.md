# WS86 — Game and Ride board 9

**10 screens · 7 operations · 5 schemas · 3 permissions**

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
  `DEVICE_CONFIGURE, DEVICE_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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
| `BO-474` | Reader Integration Command Center | D | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-475` | Reader Manufacturer & Model Profile | C | 24 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-476` | Communication Protocol Configuration | D | 10 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-477` | Reader Command & Event Mapping | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-478` | Reader Configuration Deployment & Synchronization | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-479` | Game Trigger & I/O Control Mapping | D | 0 | 12 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-480` | Reader Screen, LED & Sound Output Mapping | D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-481` | Edge Cache & Offline Rule Package | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-482` | Device Diagnostics & Integration Logs | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-483` | Integration Certification & Test Console | B | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-477, BO-478, BO-479, BO-480, BO-481, BO-482, BO-483 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-474` Reader Integration Command Center

**Provide the technical team with a centralized view of every reader integration deployed across TICVAI clients and venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-474 |
| Who uses it | venue staff holding `DEVICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/reader-integration-command-center-bo-474` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The technical team's landing for reader integration: every integrated reader with its model, protocol, attraction, connection and configuration state, and how many are failing. It is the entry to the hardware-independence layer the pack recommends (TICVAI business rules, a standard reader interface, vendor adaptors, then the reader). The one thing to get right: model and configuration version are first- class columns, because "which readers are on the old configuration" and "which model is failing" are the questions this board answers.

**Known correction pending (do not draw the wrong version)**

- **KPI tiles and overview rely on listReaders** Why: Reader has no model, protocol, configuration version or response time; model and versions live in the device register (ADR-0067) and the hardware model library. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / ADR-0067 / contracts/spine/access.yaml#setHardwareModel; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The pack describes a view across all TICVAI clients; is the cross-tenant view a platform-console (P09) screen?** → Drawn default accepted: P08 shows the current venue only; flag a P09 counterpart. *(decided by Chinmay, 2026-10-02; DEC-427 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search reader integration | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by client, venue, manufacturer, model, protocol, status and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Manufacturer, Model, Protocol, Status, Configuration version. Venue from the top bar; the pack's Client filter belongs to the platform console. *(source: screens/P08-venue-back-office.yaml#BO-475)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Integrated Readers** (metric tile)

**Online** (metric tile)

**Offline** (metric tile)

**Integration Errors** (metric tile)

**Pending Configuration Sync** (metric tile)

**Transactions Today** (metric tile)

**Average Response Time** (metric tile)

**Protocol Errors** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Total integrated readers, Online, Offline, Integration errors, Pending configuration sync, Transactions today, Average response time (ms), Protocol errors. *(source: screens/P08-venue-back-office.yaml#BO-474)*
- **Integration overview**: Columns Reader, Model, Protocol, Attraction, Status, Config (Synced / Pending / Out of sync). Out of sync and offline first. *(source: screens/P08-venue-back-office.yaml#BO-474)*
- **Architecture band**: A thin diagram at the top - TICVAI business rules, Reader integration layer, Vendor adaptor, Reader, Game or ride controller - each layer linking to its screen. *(source: screens/P08-venue-back-office.yaml#BO-474 / screens/P08-venue-back-office.yaml#BO-484)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add integration**: Starts from the model library (BO-475) then protocol (BO-476). *(source: screens/P08-venue-back-office.yaml#BO-475)*
- **Test connection, Synchronise, View logs, Open reader**: Row actions - test runs the reader test; synchronise deploys the current configuration; logs open BO-482. *(source: contracts/satellite/games.yaml#testReader / contracts/satellite/games.yaml#deployReaderConfiguration)*

**Data it reads**: `listReaders` (onLoad, Integrations by reader)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-475` Reader Manufacturer & Model Profile: *Reader Manufacturer & Model Profile*
- → `BO-476` Communication Protocol Configuration: *Communication Protocol Configuration*
- → `BO-477` Reader Command & Event Mapping: *Reader Command & Event Mapping*
- → `BO-478` Reader Configuration Deployment & Synchronization: *Reader Configuration Deployment & Synchronization*
- → `BO-479` Game Trigger & I/O Control Mapping: *Game Trigger & I/O Control Mapping*
- → `BO-480` Reader Screen, LED & Sound Output Mapping: *Reader Screen, LED & Sound Output Mapping*
- → `BO-481` Edge Cache & Offline Rule Package: *Edge Cache & Offline Rule Package*
- → `BO-482` Device Diagnostics & Integration Logs: *Device Diagnostics & Integration Logs*
- → `BO-483` Integration Certification & Test Console: *Integration Certification & Test Console*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader integration list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader integration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A model fails certification after readers are deployed**: Its readers carry a "Model not certified" warning badge (see BO-483). *(source: screens/P08-venue-back-office.yaml#BO-482)*

#### Consistency with other screens

- Match `BO-404`: The board-2 reader dashboard covers attraction mapping and business settings; this board covers protocol and adaptor. Same reader identity and status words.
- Match `BO-466`: Health columns use the same states and colours.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
readers:
- reader: R-001
  model: GR-X10
  protocol: TCP/IP
  attraction: Falcon Coaster
  status: Online
  config: Synced
- reader: R-014
  model: GR-X10
  protocol: TCP/IP
  attraction: VR Racing
  status: Online
  config: Synced
- reader: R-023
  model: GR-X20
  protocol: REST API
  attraction: Basketball Pro
  status: Online
  config: Pending
- reader: R-031
  model: GR-X20
  protocol: REST API
  attraction: Prize Crane
  status: Offline
  config: Out of sync
```

#### Permissions

- `listReaders` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reader integration board configures lighting/display behaviour and other device-level settings exposed via the vendor SDK. *(client request · MoM 11 Sep 2026, 4.14 Reader Integration Protocol Management · DI-884)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-474` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-474`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 1: Opens Reader Integration Command Center → Provide the technical team with a centralized view of every reader integration deployed across TICVAI clients and venues.
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F195 branch at step 1 (expected): when Nothing has been set up on Reader Integration Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F195 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-474?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-475`, `BO-476`, `BO-477`, `BO-478`, `BO-479`, `BO-480`, `BO-481`, `BO-482`, `BO-483`.
- [ ] Every gated control is gated: `DEVICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-475` Reader Manufacturer & Model Profile

**Allow TICVAI to support multiple reader manufacturers/models without building business rules specifically for one Chinese reader.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block C · task VM-BO-475 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure supported capabilities) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/reader-manufacturer-model-profile-bo-475` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): ReaderProfile holds display behaviour, retry and replay window, not manufacturer, model or capabilities; the model belongs to the hardware model library …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** A capability profile per reader manufacturer and model, so TICVAI knows what each device can do (screen, LED, sound, relay, offline storage) without building rules around one supplier. The one thing to get right: this is the same hardware model library the access-control board uses (one device register), shown filtered to readers, and its capability flags drive what the later screens allow.

**Known correction pending (do not draw the wrong version)**

- **Capabilities drawn as select fields labelled with a ticked box** Why: Generated from the pack's checkbox list; they are checkboxes. *(source: screens/P08-venue-back-office.yaml#BO-475; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): setReaderProfile is bound (CHG-WIR-001); The model record has no SDK or API version, protocols, touch screen, local storage, runtime capabilities or certification status (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ☑ RFID | select field | — | — | — | — | — | — |
| ☑ NFC | select field | — | — | — | — | — | — |
| ☑ Screen | select field | — | — | — | — | — | — |
| ☑ LED / RGB Lighting | text field | — | — | — | — | — | — |
| ☑ Sound | select field | — | — | — | — | — | — |
| ☑ Touch Screen | select field | — | — | — | — | — | — |
| ☑ Local Storage | select field | — | — | — | — | — | — |
| ☑ I/O Output | select field | — | — | — | — | — | — |
| ☑ Network Connectivity | select field | — | — | — | — | — | — |

**Form: Save model** (modal, opened by *Save model*; *Save model* calls `setHardwareModel`, *Cancel* sends nothing)

**Collects what `setHardwareModel` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setHardwareModel` body |
| Manufacturer `manufacturer` | text field | required | — | — | — | — | `setHardwareModel` body |
| Model `model` | text field | required | — | — | — | — | `setHardwareModel` body |
| Device category `deviceCategory` | radio group | required | — | Turnstile · Special gate · Mobile · Reader · Other | — | — | `setHardwareModel` body |
| Hardware type `hardwareType` | select | required | — | Standard turnstile · Full height turnstile · Tripod turnstile · Speed gate · Wide lane · Accessible pod gate · Buggy gate · Vip gate · Staff gate · Android handheld · Ios device · Tablet … | — | The specific hardware under a device's `kind` (ADR-0067, accepted 1 October: one device register). | `setHardwareModel` body |
| Supported technologies `supportedTechnologies` | list of values (chips) | optional | — | — | — | — | `setHardwareModel` body |
| Connectivity `connectivity` | list of values (chips) | optional | — | — | — | — | `setHardwareModel` body |
| Offline capability `offlineCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Screen capability `screenCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Sound capability `soundCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Light capability `lightCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Relay controller support `relayControllerSupport` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Payment capability `paymentCapability` | toggle | optional | off | — | — | Payment capability where available | `setHardwareModel` body |
| Firmware software information `firmwareSoftwareInformation` | text field | optional | — | — | — | — | `setHardwareModel` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setHardwareModel` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Manufacturer, Model, Device family**: Manufacturer and model required text; device family fixed to Reader here. *(source: contracts/spine/access.yaml#setHardwareModel / ADR-0067)*
- **Firmware, SDK version, API version**: Firmware as free text; SDK and API versions have no field and are greyed (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-475 / contracts/spine/access.yaml#setHardwareModel)*
- **Supported protocols**: Multi-select of TCP/IP, REST API, WebSocket, MQTT, SDK, Serial RS-232/485, Other. *(source: screens/P08-venue-back-office.yaml#BO-476)*
- **Hardware capabilities**: Checkboxes - RFID, NFC (supported technologies), Screen, LED / RGB lighting, Sound, Touch screen, Local storage, I/O output (relay), Network connectivity. Not select fields. *(source: screens/P08-venue-back-office.yaml#BO-475 / contracts/spine/access.yaml#setHardwareModel)*
- **Runtime capabilities**: Checkboxes - Display price, Display wallet balance, Display messages, Change LED colour, Trigger game, Receive game result, Cache configuration, Store offline transactions. *(source: screens/P08-venue-back-office.yaml#BO-475)*
- **Certification status**: Read-only; set only by the certification console (BO-483) when all mandatory tests pass. *(source: screens/P08-venue-back-office.yaml#BO-475 / screens/P08-venue-back-office.yaml#BO-482)*

#### Outputs: what the screen shows and produces

**Shown**

**Reader models** (data table, from `listDeviceTypeHardware`)

| Shows | Format | Notes |
|---|---|---|
| Hardware type | chip: Standard turnstile, Full height turnstile, Tripod turnstile, Speed gate, Wide lane … | Specific hardware type within the device category |
| Manufacturer | text | Manufacturer |
| Model | text | Model |
| Device category | chip: Turnstile, Special gate, Mobile, Reader, Other | Device Category |
| Supported technologies | list or chips (count when long) | Supported technologies |
| Connectivity | list or chips (count when long) | Connectivity |
| Offline capability | yes / no (icon or chip) | Offline capability |
| Screen capability | yes / no (icon or chip) | Screen capability |
| Sound capability | yes / no (icon or chip) | Sound capability |
| Light capability | yes / no (icon or chip) | Light capability |
| Relay controller support | yes / no (icon or chip) | Relay/controller support |
| Payment capability where available | yes / no (icon or chip) | payment capability where available |
| Firmware software information | text | firmware/software information |
| Hardware model | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save model (secondary button) | `setHardwareModel` PUT `/hardware-models` | AccessHardwareModel | AccessHardwareModel | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Capability summary**: A compact "Can / Cannot" card per model used in other screens' headers ("GR-X20: no sound"). *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save model**: Saves the model in the tenant's library (whole row, VO-R04); every venue's readers can reference it. *(source: contracts/spine/access.yaml#setHardwareModel)*

**Data it reads**: `listDeviceTypeHardware` (onLoad, Reader models in the hardware library)

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader manufacturer model configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader manufacturer model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader manufacturer model configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **A capability is switched off while readers of the model use it**: Warn with the count ("12 readers use LED colours; they will fall back to screen text"). *(source: designer default)*

#### Consistency with other screens

- Match `BO-195`: Device Type & Hardware Library is the same record (ADR-0067, one register); draw one editor and let this board open it filtered to readers (VO-R14).
- Match `BO-480`: Output options there are greyed where the model lacks the capability.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
model:
  manufacturer: Guangzhou RideTech
  model: GR-X20
  family: Reader
  firmware: 3.4.0
  protocols: REST API, TCP/IP
  capabilities: RFID, NFC, Screen, LED, I/O output, Local storage
  certification: Approved for TICVAI
```

#### Permissions

- `listDeviceTypeHardware` → `DEVICE_VIEW` (read) · staff
- `setHardwareModel` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-475` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-475`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 2: Works in Reader Manufacturer & Model Profile → Allow TICVAI to support multiple reader manufacturers/models without building business rules specifically for one Chinese reader.
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-475?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save model.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-476` Communication Protocol Configuration

**Configure how TICVAI communicates with each reader/device family.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-476 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Connection Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/communication-protocol-configuration-bo-476` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How TICVAI talks to each reader family: protocol, address, authentication, timeouts, heartbeat and encryption, with a test that proves the connection. The one thing to get right: fields change with the protocol (a serial reader has no host, a REST reader has an endpoint), and secrets are write-only.

**Known correction pending (do not draw the wrong version)**

- **setReaderProfile is bound and every field is a select** Why: No operation or schema holds protocol, host, port, endpoint, authentication, timeouts, heartbeat or encryption; host and port are typed values, not choices. *(source: contracts/satellite/games.yaml#setReaderProfile / screens/P08-venue-back-office.yaml#BO-476; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are protocol settings per model (family) with per-reader address overrides, or wholly per reader?** → Drawn default accepted: Per model with a per-reader host and port. *(decided by Chinmay, 2026-10-02; DEC-428 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Protocol | select field | — | — | — | — | — | — |
| Host / IP | select field | — | — | — | — | — | — |
| Port | select field | — | — | — | — | — | — |
| Endpoint | select field | — | — | — | — | — | — |
| Authentication | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Retry Count | select field | — | — | — | — | — | — |
| Heartbeat Interval | select field | — | — | — | — | — | — |
| Encryption | select field | — | — | — | — | — | — |
| Connection Mode | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Protocol**: Select from the model's supported protocols (BO-475). *(source: screens/P08-venue-back-office.yaml#BO-476)*
- **Host / IP, Port, Endpoint**: Text and number fields, not selects. Host and port for TCP/IP, MQTT and WebSocket; endpoint URL for REST; COM port and baud rate replace them for serial. *(source: screens/P08-venue-back-office.yaml#BO-476)*
- **Authentication, Encryption**: Authentication type (None, API key, Certificate, Username and password); the secret is entered once and shown masked thereafter. Encryption on by default. *(source: screens/P08-venue-back-office.yaml#BO-476)*
- **Timeout, Retry count, Heartbeat interval, Connection mode**: Timeout in seconds (example 3), retries whole number, heartbeat in seconds (example 10), connection mode Persistent or On demand. *(source: screens/P08-venue-back-office.yaml#BO-476)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Connection test result**: "Connected, response 42 ms" in green, or the failing step in red ("Timed out after 3 s at 192.168.10.55:9100"). *(source: screens/P08-venue-back-office.yaml#BO-476)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test connection**: Runs the connectivity check against one reader using these settings and reports per step. *(source: contracts/satellite/games.yaml#testReader)*
- **Save**: Greyed until a record holds protocol settings (VO-R13). *(source: DI-653)*

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The communication protocol configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the communication protocol untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No communication protocol configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Heartbeat interval longer than the reader's real reporting**: Explain that a reader whose last report is older than this interval shows as Unreachable on the monitors. *(source: contracts/satellite/games.yaml#reportReaderQueue)*

#### Consistency with other screens

- Match `BO-475`: Only the model's supported protocols are offered.
- Match `BO-466`: The heartbeat interval set here is what the health monitor measures against.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
connection:
  protocol: TCP/IP
  host: 192.168.10.55
  port: 9100
  timeout: 3 s
  heartbeat: 10 s
  retries: 2
  encryption: 'On'
  result: Connected, 42 ms
```

#### Permissions

- `setReaderProfile` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reader integration board configures lighting/display behaviour and other device-level settings exposed via the vendor SDK. *(client request · MoM 11 Sep 2026, 4.14 Reader Integration Protocol Management · DI-884)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-476` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-476`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 4: Works in Communication Protocol Configuration → Configure how TICVAI communicates with each reader/device family.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-476?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-477` Reader Command & Event Mapping

**Translate TICVAI's standardized commands into the specific commands understood by each reader manufacturer. This is one of the most important architectural screens. DISPLAY_PRICE DISPLAY_MESSAGE LED_COLOR APPROVE_PLAY REJECT_PLAY TRIGGER_GAME SHOW_BALANCE SYNC_CONFIG**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block B · task VM-BO-477 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/reader-command-event-mapping-bo-477` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): Command and event mapping is the vendor adaptor's, per model (ADR-0015); setReaderConfiguration writes one reader, and the screen is reached from the integration …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The translation table between TICVAI's standard reader commands and events and what one vendor's reader actually understands. The pack calls it one of the most important architectural screens, because if the reader is replaced only this mapping changes. The one thing to get right: it is defined per reader model (adaptor), not per reader, and it shows clearly which standard commands a model cannot do.

**Fixed on main** (the package already carries these; draw what it says): setReaderConfiguration (one reader) is bound with "Save reader configuration" (CHG-WIR-001); Entry parameter readerId (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the mapping editable by an administrator at run time, or fixed in the adaptor and only displayed?** → Drawn default accepted: Read-only display of the adaptor's mapping with its version. *(decided by Chinmay, 2026-10-02; DEC-429 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Model**: Select of reader models from the library; the mapping belongs to the model's adaptor. *(source: ADR-0015 / contracts/satellite/games.yaml#/components/schemas/Reader)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Commands table**: Rows DISPLAY_PRICE, DISPLAY_MESSAGE, LED_COLOR, APPROVE_PLAY, REJECT_PLAY, TRIGGER_GAME, SHOW_BALANCE, SYNC_CONFIG; columns TICVAI command, Vendor command (e.g. CMD:PLAY:01), Status (Mapped / Not supported). *(source: screens/P08-venue-back-office.yaml#BO-477)*
- **Events table**: Rows CARD_TAPPED, GAME_STARTED, GAME_COMPLETED, SCORE_RECEIVED, PRIZE_WON, DEVICE_ERROR, HEARTBEAT; columns Vendor event, TICVAI event, Status. *(source: screens/P08-venue-back-office.yaml#BO-477)*
- **Adaptor version**: Header shows the adaptor name and version that implements this mapping. *(source: ADR-0015)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Compare models**: Two models' mappings side by side, to see what a reader swap would lose. *(source: screens/P08-venue-back-office.yaml#BO-477 / designer default)*

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader command event list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader command event untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader command event yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader command event are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A standard command not supported by the model**: Shown "Not supported" in grey with its effect ("No LED; free games shown by screen text only"). *(source: screens/P08-venue-back-office.yaml#BO-475)*

#### Consistency with other screens

- Match `BO-482`: Event names in the diagnostics log are these standard names.
- Match `BO-479`: TRIGGER_GAME's physical output is defined there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
commands:
- ticvai: APPROVE_PLAY
  vendor: CMD:PLAY:01
  status: Mapped
- ticvai: LED_COLOR
  vendor: CMD:LED:<rgb>
  status: Mapped
- ticvai: SHOW_BALANCE
  vendor: CMD:TXT:2
  status: Mapped
events:
- vendor: EVT:TAP
  ticvai: CARD_TAPPED
  status: Mapped
- vendor: EVT:END
  ticvai: GAME_COMPLETED
  status: Mapped
- vendor: (none)
  ticvai: PRIZE_WON
  status: Not supported
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-477` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-477`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 6: Works in Reader Command & Event Mapping → Translate TICVAI's standardized commands into the specific commands understood by each reader manufacturer. This is one of the most important architectural screens. DISPLAY_PRICE DISPLAY_MESSAGE …
- ADR-0015 *Standards-First Device Drivers* (`docs/adr/0015-standards-first-device-drivers.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-477?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-474`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-478` Reader Configuration Deployment & Synchronization

**Push backend configuration from TICVAI to readers where local configuration is required.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-478 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/reader-configuration-deployment-synchronization-bo-478` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No bulk reader deploy, rollback, version compare or deployment status read.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Pushes TICVAI configuration (prices, entitlements, display rules, retap settings, offline package) to the readers that cache it, and shows which version each reader runs. A change nobody deployed is a change that did not happen. The one thing to get right: current versus target version per reader, with the failures and their reasons first, and a clear statement of what a deployment changes before it is sent.

**Known correction pending (do not draw the wrong version)**

- **Primary button with an empty label** Why: Generated placeholder; it is "Deploy to 126 readers". *(source: screens/P08-venue-back-office.yaml#BO-478; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Deployment is per reader with no body, no version list and no rollback** Why: deployReaderConfiguration sends one reader's current configuration; bulk deploy, rollback, version compare and a status read of all readers have no operation. *(source: contracts/satellite/games.yaml#deployReaderConfiguration / contracts/satellite/games.yaml#/components/schemas/ReaderDeployment; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Versions written "V2.8" in the pack** Why: configurationVersion is an integer; show "28", not a dotted version that cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-479 / contracts/satellite/games.yaml#/components/schemas/ReaderDeployment; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Readers to deploy**: Select by zone, attraction, model, or "All readers behind target"; the count shows ("126 readers selected"). *(source: screens/P08-venue-back-office.yaml#BO-479)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Package contents**: Read-only list of what the package carries - reader id, attraction, display theme and messages, LED rules, price display, retap settings, device parameters, offline parameters, version. *(source: screens/P08-venue-back-office.yaml#BO-477 / screens/P08-venue-back-office.yaml#BO-479)*
- **What publishing changes**: Before Deploy, a summary of the differences since the readers' current version ("Prices changed on 3 games; free-game glow on 1 reader; offline limit AED 5,000") and the count of readers affected. *(source: screens/P08-venue-back-office.yaml#BO-478)*
- **Status table**: Columns Reader, Current, Target, Status (Pending, Sending, Synced, Failed, Out of date), Edge package expires. Failed rows show the failure reason and sort first. *(source: screens/P08-venue-back-office.yaml#BO-479 / contracts/satellite/games.yaml#/components/schemas/ReaderDeployment)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Deploy**: Sends to each selected reader; rows move from Pending to Synced as readers acknowledge. Offline readers stay Pending until they reconnect. *(source: contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Retry**: Re-sends to failed readers only. *(source: contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Rollback, Compare versions**: Greyed until versions can be listed and redeployed (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-479)*

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader deployment synchronization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader deployment synchronization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader deployment synchronization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader deployment synchronization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Deployment during operating hours**: Confirm notes readers apply it between taps; no tap is interrupted. *(source: designer default)*
- **Edge package close to expiry on readers that cannot be reached**: Amber warning "4 readers' offline packages expire in 6 hours; they will refuse offline taps after that". *(source: contracts/satellite/games.yaml#/components/schemas/ReaderDeployment)*

#### Consistency with other screens

- Match `BO-443`: Pricing publication decides what is approved; this screen delivers it to readers. Only published prices are in the package.
- Match `BO-466`: The Resync configuration action there is a single-reader deploy from here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
deployment:
  version: 28
  selected: 126
status:
- reader: R-031
  current: 26
  target: 28
  status: Failed, reader offline
- reader: R-023
  current: 27
  target: 28
  status: Pending
- reader: R-001
  current: 28
  target: 28
  status: Synced
```

#### Permissions

- `deployReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-478` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-478`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 8: Works in Reader Configuration Deployment & Synchronization → Push backend configuration from TICVAI to readers where local configuration is required.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-478?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-479` Game Trigger & I/O Control Mapping

**Configure how an approved TICVAI transaction physically starts a game or ride.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-479 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card Tap) and no metric row |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/game-trigger-i-o-control-mapping-bo-479` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How an approved tap physically starts a game or ride: which output the reader fires (relay pulse, digital output, a command), for how long, and which inputs tell TICVAI the game started, finished, paid out or faulted. Agreed with the client as a dry-contact start signal, like a turnstile. The one thing to get right: the output and input lines come from the reader model, and a test fires a real machine, so it must be confirmed.

**Known correction pending (do not draw the wrong version)**

- **Table "Every game trigger mapping" with the flow arrows as columns** Why: The pack's flow parsed as columns; the screen is one reader's mapping form with a flow diagram. *(source: screens/P08-venue-back-office.yaml#BO-479; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The I/O mapping has no schema** Why: ioMapping is an open object whose keys are the model's lines; the form can only be drawn generically until each adaptor publishes its lines. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / ADR-0015; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Game and reader**: The reader arrives from the command centre or is picked; the game is its mapped attraction, read-only. *(source: contracts/satellite/games.yaml#/components/schemas/Reader)*
- **Trigger type**: Relay output, Digital output, Pulse, TCP/IP command, Serial command, API command; only those the model supports. *(source: screens/P08-venue-back-office.yaml#BO-479 / screens/P08-venue-back-office.yaml#BO-480)*
- **Output line and pulse duration**: Output line from the model's lines (DO-1, DO-2); pulse duration in milliseconds (example 500 ms), shown only for relay and pulse types. *(source: screens/P08-venue-back-office.yaml#BO-480 / contracts/satellite/games.yaml#/components/schemas/Reader)*
- **Feedback inputs**: For each of Game started, Game completed, Prize won, Fault, Score result, pick the input line or "Not wired". *(source: screens/P08-venue-back-office.yaml#BO-480)*

#### Outputs: what the screen shows and produces

**Shown**

**Every game trigger mapping** (data table)

| Shows | Format | Notes |
|---|---|---|
| → TICVAI authorization | text | not in the schema: `→ TICVAI Authorization` |
| → APPROVED | text | not in the schema: `→ APPROVED` |
| → reader receives command | text | not in the schema: `→ Reader receives command` |
| → reader sends output | text | not in the schema: `→ Reader sends output` |
| → game controller | text | not in the schema: `→ Game Controller` |
| → GAME START | text | not in the schema: `→ GAME START` |

**The selected game trigger mapping** (detail panel): The pack groups this record's detail under its own headings: “Depending on hardware”, “Page 90 of 105”, “Basketball Pro”, “Potential inputs”.

| Shows | Format | Notes |
|---|---|---|
| → TICVAI authorization | text | not in the schema: `→ TICVAI Authorization` |
| → APPROVED | text | not in the schema: `→ APPROVED` |
| → reader receives command | text | not in the schema: `→ Reader receives command` |
| → reader sends output | text | not in the schema: `→ Reader sends output` |
| → game controller | text | not in the schema: `→ Game Controller` |
| → GAME START | text | not in the schema: `→ GAME START` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Flow**: Card tap, TICVAI authorisation, Approved, Reader receives command, Reader output, Game controller, Game start; the configured output shown on the arrow. *(source: screens/P08-venue-back-office.yaml#BO-479)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save reader configuration**: Saves the reader's whole configuration including the I/O mapping (VO-R04); takes effect after deployment (BO-478). *(source: contracts/satellite/games.yaml#setReaderConfiguration)*
- **Test game trigger**: Confirmation per VO-R16 "This starts Basketball Pro now. Make sure the machine is clear." Then shows trigger sent and whether the start signal came back. *(source: contracts/satellite/games.yaml#testReader)*

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game trigger mapping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game trigger mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game trigger mapping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game trigger mapping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Trigger sent but no start confirmation**: Shown as "Game trigger failed" with the explanation from the diagnostics screen; the play is a candidate for reversal. *(source: screens/P08-venue-back-office.yaml#BO-482)*
- **Reader model with no I/O output**: Trigger types limited to command types; relay options hidden with the reason. *(source: contracts/spine/access.yaml#setHardwareModel)*

#### Consistency with other screens

- Match `BO-400`: Attraction to reader mapping is set there; this screen shows it read-only.
- Match `BO-482`: The same trigger test appears in diagnostics.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
trigger:
  game: Basketball Pro
  reader: R-023
  type: Relay pulse
  output: DO-1
  pulse: 500 ms
  started: DI-1
  completed: DI-2
  score: Via command
```

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-479` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-479`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 10: Works in Game Trigger & I/O Control Mapping → Configure how an approved TICVAI transaction physically starts a game or ride.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-479?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-480` Reader Screen, LED & Sound Output Mapping

**Map TICVAI transaction results to the physical reader's screen, lighting and sound capabilities. This supports the matrix requirement for free-game color indication and custom reader themes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-480 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/reader-screen-led-sound-output-mapping-bo-480` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Maps each tap result to what the physical reader does: screen text, LED colour, sound. The client asked for a distinct free-game colour and custom themes, because a guest at a machine reads a light, not a sentence. The one thing to get right: a result-by-output grid with a live reader mockup for Normal, Free, VIP and Rejected, and rejection messages that say why ("No plays left on your pass"), not "Declined".

**Known correction pending (do not draw the wrong version)**

- **The per-outcome mapping is on the reader profile, but the screen binds the reader** Why: ReaderProfile.displayBehaviour holds accepted, freeGame, insufficientCredit, cardBlocked and readError; Reader.displayRules holds only glow, show balance, show price, theme and languages. Bind both. *(source: contracts/satellite/games.yaml#/components/schemas/ReaderProfile / contracts/satellite/games.yaml#/components/schemas/Reader; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No VIP, retry, expired-card or sound mapping** Why: displayBehaviour has five outcomes as single strings, with no separate LED colour, sound or Arabic text. *(source: screens/P08-venue-back-office.yaml#BO-480 / contracts/satellite/games.yaml#/components/schemas/ReaderProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Result mapping**: Rows Authorised, Free play, VIP price, Retry offer ("CONTINUE? RETRY AED 10"), Insufficient credit, Card blocked, Card expired, Other refusal, Read error; columns Screen text (English and Arabic), LED colour (swatch picker), Sound (Success, Free play, Error, None). Pack defaults - Authorised green, Free play the configured free-play colour, VIP the VIP theme, Rejected red with the error tone. *(source: screens/P08-venue-back-office.yaml#BO-480 / screens/P08-venue-back-office.yaml#BO-481 / DI-868)*
- **Free-game glow, Show balance, Show price, Theme, Languages**: Reader-level toggles and theme select, defaults on, on, on. *(source: contracts/satellite/games.yaml#/components/schemas/Reader)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save reader configuration (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reader preview**: A physical reader mockup with tabs NORMAL, FREE, VIP, REJECTED showing text, light and a sound icon; tenant brand on the reader (VO-R15). *(source: screens/P08-venue-back-office.yaml#BO-480 / screens/P08-venue-back-office.yaml#BO-481)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save reader configuration**: Saves the reader's whole configuration (VO-R04); applies after deployment. *(source: contracts/satellite/games.yaml#setReaderConfiguration)*
- **Test display, Test LED**: Pushes the selected state to the real reader for a few seconds. *(source: contracts/satellite/games.yaml#testReader)*

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader screen led list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader screen led untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader screen led yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader screen led are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Screen text longer than the model's display**: Counter under each text ("18 of 20 characters"); over-long text is refused, not cut on the device. *(source: designer default)*
- **Model without LED or sound**: Those columns greyed with "GR-X20 has no sound". *(source: contracts/spine/access.yaml#setHardwareModel)*

#### Consistency with other screens

- Match `BO-410`: Free Game Glow & Reader Display Rules and Reader Theme (BO-411) edit the same reader settings; draw one output editor with board entries as anchors (VO-R14).
- Match `BO-442`: The reader mockup is the same component as the pricing preview.
- Match `BO-468`: Refusal messages correspond to the reason labels there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
mapping:
- result: Authorised
  text: PLAY AUTHORISED
  textAr: تم التفويض
  led: Green
  sound: Success
- result: Free play
  text: FREE PLAY - TAP TO START
  led: Purple
  sound: Free play
- result: VIP price
  text: VIP PRICE AED 15
  led: Gold
  sound: Success
- result: Insufficient credit
  text: TOP UP TO PLAY
  led: Red
  sound: Error
```

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reader integration board configures lighting/display behaviour and other device-level settings exposed via the vendor SDK. *(client request · MoM 11 Sep 2026, 4.14 Reader Integration Protocol Management · DI-884)*
- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-480` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-480`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 12: Works in Reader Screen, LED & Sound Output Mapping → Map TICVAI transaction results to the physical reader's screen, lighting and sound capabilities. This supports the matrix requirement for free-game color indication and custom reader themes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-480?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save reader configuration, Cancel.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-481` Edge Cache & Offline Rule Package

**Configure what information can be securely distributed to the edge/reader or local gateway for temporary offline operation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-481 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/edge-cache-offline-rule-package-bo-481` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Decides what a reader may hold so it can keep working when the cloud is unreachable, and the limits that cap the money at risk while it does. The one thing to get right: the exposure limits (time, count, value) are the headline, the package contents are a checklist, and the security properties are shown as guarantees, not switches anyone can turn off.

**Known correction pending (do not draw the wrong version)**

- **Primary button with an empty label; deployment bound as the save** Why: Deploying sends the package; nothing saves the limits or contents. Duration, count and content selection have no field, and the value limit lives in the validation rules. *(source: contracts/satellite/games.yaml#deployReaderConfiguration / contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are offline limits venue-wide or settable per reader (a crane versus a coaster)?** → Drawn default accepted: Venue-wide, as the contract holds them. *(decided by Chinmay, 2026-10-02; DEC-430 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Allow offline operation**: On / off, default on; off means readers refuse every tap without a connection. *(source: screens/P08-venue-back-office.yaml#BO-481 / contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*
- **Maximum offline duration, Maximum transaction count, Maximum value exposure**: Hours (example 2), count (example 500), AED (example 5,000). Value maps to offlineMaximumValue; duration and count have no field and are greyed (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-481 / contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*
- **Package contents**: Checklist - reader identity, attraction, price rules, card validation data (including blocked cards), entitlement data, retap rules, offline limits, security keys, configuration version. Identity, keys and version are mandatory and locked on. *(source: screens/P08-venue-back-office.yaml#BO-481)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Security**: Read-only ticks - Signed configuration, Encrypted, Package expiry (date shown), Device binding, Version validation. *(source: screens/P08-venue-back-office.yaml#BO-481 / contracts/satellite/games.yaml#/components/schemas/ReaderDeployment)*
- **Offline flow**: Cloud unavailable, Reader detects outage, Cached rules used, Plays stored, Connection restored, Plays uploaded, TICVAI reconciles. *(source: screens/P08-venue-back-office.yaml#BO-481)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save and deploy**: Saves the limits and opens the deployment summary (BO-478) naming the readers that will receive the new package. *(source: contracts/satellite/games.yaml#deployReaderConfiguration)*

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The edge cache offline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the edge cache offline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No edge cache offline yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the edge cache offline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A card is blocked after the last package build**: Offline readers still accept it until redeployed; the screen shows "Blocked list in package as of 10:05". *(source: contracts/satellite/games.yaml#deployReaderConfiguration / screens/P08-venue-back-office.yaml#BO-460)*
- **Limits reached while offline**: The reader refuses further offline taps with "Please see staff"; the monitor shows "Offline limit reached". *(source: screens/P08-venue-back-office.yaml#BO-481)*

#### Consistency with other screens

- Match `BO-471`: The monitor shows readers against these limits.
- Match `BO-425`: Offline allowed and maximum value are the same venue-wide validation settings; edit once.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
limits:
  offline: 'On'
  duration: 2 hours
  count: 500
  value: AED 5,000.00
```

#### Permissions

- `deployReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-481` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-481`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 14: Works in Edge Cache & Offline Rule Package → Configure what information can be securely distributed to the edge/reader or local gateway for temporary offline operation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-481?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-482` Device Diagnostics & Integration Logs

**Give development team / support teams detailed technical visibility when a reader or game is not operating correctly.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-482 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/device-diagnostics-integration-logs-bo-482` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Technical diagnostics for one reader: whether it is connected, what it last did, and a log of every message between TICVAI, the reader and the game, so support can see exactly where a play broke. The one thing to get right: the chain TICVAI, Reader, Game drawn as hops with the failed hop red, because "the reader never saw the card" and "the game did not start" send an engineer to different places.

**Known correction pending (do not draw the wrong version)**

- **Primary button with an empty label and Cancel are the only components** Why: The diagnostics panel, event log and test actions are not drawn. *(source: screens/P08-venue-back-office.yaml#BO-482; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No event log read, and tests cannot be run one at a time** Why: testReader runs every check together and has no LED check; nothing returns the command and event log the pack shows. *(source: contracts/satellite/games.yaml#testReader / contracts/satellite/games.yaml#/components/schemas/ReaderTestResult; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reader**: Arrives from the command centre or health monitor; shown in the header with model and attraction. *(source: screens/P08-venue-back-office.yaml#BO-482)*
- **Log filters**: Direction, event name, result, time window (default last 15 minutes). *(source: screens/P08-venue-back-office.yaml#BO-482)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Diagnostics panel**: Connection status, Last heartbeat, Protocol status, Response time, Configuration version, Firmware, Last successful transaction, Last error. *(source: screens/P08-venue-back-office.yaml#BO-482)*
- **Event log**: Columns Time (HH:mm:ss.SSS), Direction (Reader to TICVAI, TICVAI to Reader, Reader to Game), Event (standard names), Result. A failed sequence is grouped and labelled, e.g. "GAME_TRIGGER_FAILED: reader received approval but no game-start confirmation was returned". *(source: screens/P08-venue-back-office.yaml#BO-482)*
- **Test results**: Separate rows for Connectivity, Card read, Balance check, Display, Sound, Game trigger, Game-complete signal, each pass or fail with detail; overall Pass, Partial or Fail. *(source: contracts/satellite/games.yaml#/components/schemas/ReaderTestResult)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ping, Test reader, Test display, Test LED, Test game trigger**: Run the reader test; the game-trigger test confirms first (VO-R16) because it starts the machine. *(source: contracts/satellite/games.yaml#testReader)*
- **Download logs**: Downloads the filtered log as a file for the vendor. *(source: screens/P08-venue-back-office.yaml#BO-482)*

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device diagnostics integration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device diagnostics integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device diagnostics integration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the device diagnostics integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reader offline**: Tests disabled with "Reader not reachable since 10:25"; log shows the last messages received. *(source: contracts/satellite/games.yaml#/components/schemas/ReaderSyncStatus)*

#### Consistency with other screens

- Match `BO-477`: Event names are the standard names from the mapping.
- Match `BO-413`: The balance-check test console on board 2 uses the same test result rows.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
log:
- time: '10:42:01.120'
  direction: Reader to TICVAI
  event: CARD_TAPPED
  result: Received
- time: '10:42:01.310'
  direction: TICVAI to Reader
  event: APPROVE_PLAY
  result: Sent
- time: '10:42:02.004'
  direction: Reader to Game
  event: TRIGGER_GAME
  result: Success
- time: '10:42:03.210'
  direction: Reader to TICVAI
  event: GAME_STARTED
  result: Received
```

#### Permissions

- `testReader` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-482` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-482`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 16: Works in Device Diagnostics & Integration Logs → Give development team / support teams detailed technical visibility when a reader or game is not operating correctly.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-482?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-483` Integration Certification & Test Console

**Provide a controlled environment for testing and approving a new reader model before deployment. This is particularly important for your plan because you will purchase the hardware separately and TICVAI must verify that the reader supports everything required by the platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block B · task VM-BO-483 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card; Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/integration-certification-test-console-bo-483` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-021): certifyIntegration (DEVELOPER_ADMIN, a TICVAI permission) certifies an API integration listing; a tenant cannot hold it and reader-model certification is a … Contract gap recorded 2 October 2026 (CHG-WIR-024): No operation records or reads the certification of a reader (access or games hardware) model.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Test and certify a new reader model before deployment: each required capability (RFID tap, NFC, credential read, display text, price, balance) passed or failed, then certified with an end date.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 6 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): certifyIntegration (DEVELOPER_ADMIN, a TICVAI permission) on a venue screen; requiresModule 'games'. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every integration certification test** (data table)

| Shows | Format | Notes |
|---|---|---|
| RFID tap | text | not in the schema: `RFID Tap` |
| NFC tap | text | not in the schema: `NFC Tap` |
| Credential reading | text | not in the schema: `Credential Reading` |
| Text | text | not in the schema: `Text` |
| Price | text | not in the schema: `Price` |
| Balance | text | not in the schema: `Balance` |

**The selected integration certification test** (detail panel): The pack groups this record's detail under its own headings: “Connectivity”, “LED”, “Gameplay”, “Transactions”, “Offline”, “GR-X20 Reader”.

| Shows | Format | Notes |
|---|---|---|
| RFID tap | text | not in the schema: `RFID Tap` |
| NFC tap | text | not in the schema: `NFC Tap` |
| Credential reading | text | not in the schema: `Credential Reading` |
| Text | text | not in the schema: `Text` |
| Price | text | not in the schema: `Price` |
| Balance | text | not in the schema: `Balance` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Balance, Price)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration certification test list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration certification test untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration certification test yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration certification test are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every integration certification test:
- RFID Tap: 128
  NFC Tap: 11
  Credential Reading: 312
  Text: 19
  Price: AED 1,250.00
  Balance: 11
- RFID Tap: 46
  NFC Tap: 128
  Credential Reading: 74
  Text: 233
  Price: AED 48,000.00
  Balance: 128
- RFID Tap: 312
  NFC Tap: 46
  Credential Reading: 19
  Text: 57
  Price: OMR 48.500
  Balance: 46
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-483` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-483`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 18: Works in Integration Certification & Test Console → Provide a controlled environment for testing and approving a new reader model before deployment. This is particularly important for your plan because you will purchase the hardware separately and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-483?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-474`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"deployReaderConfiguration": {"method":"POST","path":"/readers/{readerId}/deploy","contract":"games","summary":"Push configuration and the offline rule package to a reader","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listDeviceTypeHardware": {"method":"GET","path":"/device-type-hardware","contract":"access","summary":"Device Type & Hardware Library","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeviceTypeHardwareLibraryView"},
"listReaders": {"method":"GET","path":"/readers","contract":"games","summary":"Readers, their attractions and their health","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Reader"},
"setHardwareModel": {"method":"PUT","path":"/hardware-models","contract":"access","summary":"Create or replace a hardware model in the library","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessHardwareModel","responds":"AccessHardwareModel"},
"setReaderConfiguration": {"method":"PUT","path":"/readers/{readerId}","contract":"games","summary":"What this reader charges, opens, shows and refuses","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Reader","responds":"Reader"},
"setReaderProfile": {"method":"PUT","path":"/reader-profiles","contract":"games","summary":"How a reader behaves and what it shows","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReaderProfile","responds":"ReaderProfile"},
"testReader": {"method":"POST","path":"/readers/{readerId}/test","contract":"games","summary":"Prove a reader works before a guest finds out it does not","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReaderTestResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessHardwareModel": {"type":"object","x-ticvai-persistence":"access.hardware_model","description":"One hardware model in the reusable library, independent of deployed devices: manufacturer, model, category and type, supported technologies, connectivity, capability flags and firmware information (declared 29 September, data-model close-out DM1)","required":["id","manufacturer","model","deviceCategory","hardwareType","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"manufacturer":{"type":"string"},"model":{"type":"string"},"deviceCategory":{"type":"string","enum":["turnstile","specialGate","mobile","reader","other"]},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType"},"supportedTechnologies":{"type":"array","items":{"type":"string"}},"connectivity":{"type":"array","items":{"type":"string"}},"offlineCapability":{"type":"boolean","default":false},"screenCapability":{"type":"boolean","default":false},"soundCapability":{"type":"boolean","default":false},"lightCapability":{"type":"boolean","default":false},"relayControllerSupport":{"type":"boolean","default":false},"paymentCapability":{"type":"boolean","default":false,"description":"Payment capability where available"},"firmwareSoftwareInformation":{"type":"string","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DeviceTypeHardwareLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Device Type & Hardware Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"hardwareType":{"type":"string","enum":["standardTurnstile","fullHeightTurnstile","tripodTurnstile","speedGate","wideLane","accessiblePodGate","buggyGate","vipGate","staffGate","androidHandheld","iosDevice","tablet","qrBarcodeReader","rfidReader","nfcReader","multiTechnologyReader","biometricReader","podium","counter","beacon","cameraController","externalAccessDevice"],"description":"Specific hardware type within the device category"},"manufacturer":{"type":"string","description":"Manufacturer"},"model":{"type":"string","description":"Model"},"deviceCategory":{"type":"string","enum":["turnstile","specialGate","mobile","reader","other"],"description":"Device Category"},"supportedTechnologies":{"type":"array","items":{"type":"string"},"description":"Supported technologies"},"connectivity":{"type":"array","items":{"type":"string"},"description":"Connectivity"},"offlineCapability":{"type":"boolean","description":"Offline capability"},"screenCapability":{"type":"boolean","description":"Screen capability"},"soundCapability":{"type":"boolean","description":"Sound capability"},"lightCapability":{"type":"boolean","description":"Light capability"},"relayControllerSupport":{"type":"boolean","description":"Relay/controller support"},"paymentCapabilityWhereAvailable":{"type":"boolean","description":"payment capability where available"},"firmwareSoftwareInformation":{"type":"string","description":"firmware/software information"},"hardwareModelId":{"type":"string"}}},
"Reader": {"type":"object","x-ticvai-persistence":"games.reader","description":"Board 2. **A `tenancy` device with a game configuration on it.**","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"`tenancy.RegisteredDevice`. **Enrolment, firmware and tamper state live there.**\n"},"gameId":{"type":"string","format":"uuid","nullable":true},"readerProfileId":{"type":"string","format":"uuid","nullable":true},"acceptedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"acceptsDirectPay":{"type":"boolean","default":false},"retapDelaySeconds":{"type":"integer","default":3,"description":"**The setting that stops a guest paying twice for one go.** A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest.\n"},"displayRules":{"type":"object","properties":{"freeGameGlow":{"type":"boolean","default":true,"description":"**What tells a guest their entitlement was used rather than their money.** Without it the complaint arrives at the desk.\n"},"showBalance":{"type":"boolean","default":true},"showPrice":{"type":"boolean","default":true},"themeCode":{"type":"string","nullable":true},"languages":{"type":"array","items":{"type":"string"}}}},"ioMapping":{"type":"object","additionalProperties":true,"description":"Board 9.6. Which output starts the game, which input reports it finished. **Deliberately open.** The keys are the reader model's own I/O lines, so the shape belongs to the vendor adaptor for that model (game readers are a driver, not a build — ADR-0012, ADR-0015), not to this contract.\n"},"status":{"type":"string","enum":["unconfigured","active","offline","maintenance","disabled"]},"scopePath":{"type":"string"}}},
"ReaderProfile": {"type":"object","x-ticvai-persistence":"games.reader_profile","description":"BL-153. **`games` is well built on the money and what is missing sits at the reader.**\n10.2.14 and 10.2.17 want a different colour for a free game and a different one for insufficient credit — **because a guest at an arcade machine cannot read a message, they can only see a light.** The whole interaction is a second long and happens across a noisy room.\n","required":["id","name"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"displayBehaviour":{"type":"object","description":"**What the reader shows, per outcome.** Colour and tone, because the guest is looking at a machine rather than a screen.\n","properties":{"accepted":{"type":"string"},"freeGame":{"type":"string"},"insufficientCredit":{"type":"string"},"cardBlocked":{"type":"string"},"readError":{"type":"string"}}},"retryPricing":{"type":"object","nullable":true,"description":"**A retry after a machine fault is not a second play.** Without this a guest whose game crashed pays twice, and the attendant refunds by hand — which is how an arcade loses money and goodwill at once.\n","properties":{"isFree":{"type":"boolean","default":true},"withinSeconds":{"type":"integer","default":60},"maxRetries":{"type":"integer","default":1}}},"rePlayWindowSeconds":{"type":"integer","nullable":true,"description":"**A second tap within this window is the same play, not a new one.** A guest tapping twice because nothing appeared to happen should not be charged twice.\n"},"entitlementProductIds":{"type":"array","description":"**Per-game entitlement.** A pass that includes ten specific rides needs the reader to know which, and a card that works everywhere is a different product.\n","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ReaderTestResult": {"type":"object","description":"Boards 2.10 and 9.9. **Each check separately**, because they send an engineer to different places.\n","properties":{"readerId":{"type":"string","format":"uuid"},"testedAt":{"type":"string","format":"date-time"},"checks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["connectivity","cardRead","balanceCheck","display","sound","gameTrigger","gameCompleteSignal"]},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"overall":{"type":"string","enum":["pass","partial","fail"]}}}
}
```
