# P07-access-02 — P07 · Access (2 of 2)

**1 screens · 5 operations · 9 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ACCESS_DIRECTION_SET, SCOPE_VIEW, TURNSTILE_MODE_SET`. A control nobody can use must say so,
  not sit enabled and fail.
- **3 of these operations work offline**: getAccessPoint, listAccessPoints, setTurnstileMode
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
| `SCN-016` | Gate mode | B–D | 9 | 26 | 6 | 9 | 1 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SCN-016` Gate mode

**Podium operation. Changes what the gate does.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_DIRECTION_SET`, `SCOPE_VIEW`, `TURNSTILE_MODE_SET` (1 ?, 1 read, 1 operate) |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAccessPoints` reads the population and `getAccessPoint` reads one of them — list, select, act |
| Offline | **Requests only.** Hardware control is out of contract and the vendor SDK is outstanding (CF-33) |
| Opens with | `accessPointId` (deepLink), `changeId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/access/gate-mode` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Authoring operations removed 24 August**: createAccessPoint, setAccessPointGeofence, updateAccessPoint. **A scanner reads the gate configuration; it does not write it.** An access point is created in the back office and a geofence is a venue decision — a handheld at a lane that can redefine the lane is a handheld that can admit anywhere. **The podium sets the operating mode** (normal, freeFlow, dropArm, closed, podium, maintenance), required on every save; the turnstile mode (freeRotation or closed) is optional and offered only under normal or podium. **Direction is display-only here**: it is fixed per access point and set in the back office (BO-064) (decided 28 September, audit R221).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Podium control of a gate's operating mode: Normal, Free flow (count only), Drop arm (emergency, everybody through), Closed (nobody through), Podium (staff validating by eye), Maintenance, optionally narrowed to free rotation or held closed, now or at a scheduled time, with a reason. The one thing to get right: Drop arm and Closed are visually opposite and both need a deliberate confirmation.

**Known correction pending (do not draw the wrong version)**

- **DI-648 asks to switch turnstiles between entry and exit during the day, but direction is fixed per access point (R221) and cannot be changed here** Why: The client's daily entry/exit rebalancing has no supported path. *(source: DI-648 / R221; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How does a venue swing a lane from entry to exit during the day under the fixed-direction model?** → Drawn default accepted: Two access points per reversible lane; the steward switches the active one in SCN-002. *(decided by Chinmay, 2026-10-02; DEC-273 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

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

**Form: Switch direction** (modal, opened by *Switch direction*; *Switch direction* calls `setAccessPointDirection`, *Cancel* sends nothing)

**Collects what `setAccessPointDirection` sends**: the new direction (Entry or Exit), a reason, and optionally when it takes effect. Names the gate and its current direction. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Direction `direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `setAccessPointDirection` body |
| Reason `reason` | text area | required | — | min length 3; max length 200 | — | Why the gate is turned round, kept on the log. | `setAccessPointDirection` body |
| Effective at `effectiveAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Absent or not in the future, at once; in the future, held `pending` until then. | `setAccessPointDirection` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Sent by *Cancel gate mode change*** (`cancelGateModeChange`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 200 | — | — | `cancelGateModeChange` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Operating mode**: Six large tiles with what each does; Drop arm and Closed require confirmation and, where the policy says, a reason and emergency code. *(source: contracts/spine/access.yaml#setTurnstileMode / contracts/spine/access.yaml#setGateModePolicy / R221)*
- **Effective at**: Now (default) or a future time; a pending change shows with Cancel. *(source: contracts/spine/access.yaml#setTurnstileMode / contracts/spine/access.yaml#cancelGateModeChange)*

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
| Cancel gate mode change (destructive button) | `cancelGateModeChange` POST `/gate-mode-changes/{changeId}/cancel` | inline | AccessGateModeChange | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `TURNSTILE_MODE_SET` |
| Switch direction (secondary button) | `setAccessPointDirection` PUT `/access-points/{accessPointId}/direction` | inline | AccessPoint | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_DIRECTION_SET`; opens modal first |

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Apply mode**: Offline-capable request; refused if the operator's role is not allowed by the gate mode policy. *(source: contracts/spine/access.yaml#setTurnstileMode)*

**Data it reads**: `listAccessPoints` (onLoad, List access points)

**Where the user goes next**

- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Ready to scan*

**What opens over it**

- confirmDialog *Cancel gate mode change*: **Names what `cancelGateModeChange` changes and what it leaves alone**, in the consequence rather than the verb. A access gate mode change this affects should be identified in the dialog, not just counted. **Collects what `cancelGateModeChange` sends before it is called.** Nothing in the body is …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gate mode list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gate mode untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gate mode yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId and the gate mode are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `getAccessPoint` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Requests only.** Hardware control is out of contract and the vendor SDK is outstanding (CF-33) |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `not-pending`: the change is already applied or cancelled. |

#### Edge cases to draw

- **Hardware does not respond**: The request is recorded; hardware control depends on the vendor SDK, so the screen says "Requested - confirm at the gate". *(source: screens/P07-staff-scanner.yaml#SCN-016)*

#### Consistency with other screens

- Match `BO-201`: Same mode names, colours and safeguards.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
gate:
  point: Main Plaza Gate 3
  current: Normal
  requested: Free flow from 17:00
  by: Fatima Al Hashimi
```

#### Permissions

- `setTurnstileMode` → `TURNSTILE_MODE_SET` (operate) · staff
- `getAccessPoint` → `SCOPE_VIEW` (read) · staff
- `listAccessPoints` → `SCOPE_VIEW` (read) · staff
- `cancelGateModeChange` → `TURNSTILE_MODE_SET` (operate) · staff
- `setAccessPointDirection` → `ACCESS_DIRECTION_SET` (tier not set) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `getAccessPoint` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations dashboard: real-time attendance by venue and gate with each gate's online/offline status and entry count. Turnstile mode can be switched through the day (more entry gates in the morning, more exit in the evening). *(client request · MoM 2 Sep 2026, 4.15 Live Operations Dashboard · DI-648)*

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-016` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-016?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save gate mode, Cancel gate mode change, Switch direction.
- [ ] Every transition is wired: `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_DIRECTION_SET`, `SCOPE_VIEW`, `TURNSTILE_MODE_SET`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cancelGateModeChange": {"method":"POST","path":"/gate-mode-changes/{changeId}/cancel","contract":"access","summary":"Cancel a scheduled gate mode change","permission":"TURNSTILE_MODE_SET","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessGateModeChange"},
"getAccessPoint": {"method":"GET","path":"/access-points/{accessPointId}","contract":"access","summary":"Read an access point","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccessPoint"},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setAccessPointDirection": {"method":"PUT","path":"/access-points/{accessPointId}/direction","contract":"access","summary":"Switch a gate's direction live","permission":"ACCESS_DIRECTION_SET","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPoint"},
"setTurnstileMode": {"method":"PUT","path":"/access-points/{accessPointId}/mode","contract":"access","summary":"Set the operating mode of an access point","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPoint"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessGateModeChange": {"type":"object","x-ticvai-persistence":"access.gate_mode_change","description":"One gate mode change on an access point, pending or applied: from and target mode, operator, reason and effective time. Append-only history (declared 29 September, data-model close-out DM1) Written by setTurnstileMode (applied at once, or pending until a future effectiveAt) and cancelGateModeChange; a timer applies a pending change at its effective time (decided 29 September, writers pass).","required":["id","venueId","accessPointId","targetMode","status","changedByPrincipalId","changedAt","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid"},"fromMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"nullable":true},"targetMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}]},"fromDirection":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"nullable":true,"description":"Set on a live direction switch (`setAccessPointDirection`; DEC-255; CHG-CSP-032); null on a mode change. On a direction switch `targetMode` repeats the unchanged operating mode."},"toDirection":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"nullable":true,"description":"The direction switched to (CHG-CSP-032)."},"status":{"type":"string","enum":["pending","applied","cancelled"]},"reason":{"type":"string","maxLength":500,"nullable":true},"effectiveAt":{"type":"string","format":"date-time","nullable":true},"changedByPrincipalId":{"type":"string","format":"uuid","description":"Operator"},"changedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"}}},
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n\n**R221 amended 2 October 2026: a gate's direction can be switched live** (Chinmay, critical set 1, BO-230: \"Live direction switch with permission, logged\"; DEC-255; CHG-CSP-032; DI-648: more entry gates in the morning, more exit gates in the evening). `setAccessPointDirection` switches it from Live Gate Mode & Lane Control (BO-230) or the scanner's gate mode screen (SCN-016) for a holder of the configuration right, logged; the podium's `setTurnstileMode` still never touches it.\n"},"temporaryClosure":{"type":"object","nullable":true,"description":"**What the access point does while its attraction is temporarily closed** (decided 2 October 2026, Chinmay, batch 6 set 9, BO-147: \"Deny + reopening time + a virtual-queue return window where enabled\"; DEC-228; CHG-CSP-026). While `isClosed`, every scan is denied (`ValidationResult.denyCause` `attractionTemporarilyClosed`) with the reopening time when it is known; where the venue offers it and the attraction has a virtual queue, the guest is offered a return window (`queue.joinQueue`) instead of being turned away empty-handed. Set with `updateAccessPoint`; null when open. Travels in the offline package, so an offline gate denies the same way.","properties":{"isClosed":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":200,"nullable":true,"description":"Shown to staff; the guest sees \"Attraction temporarily closed\"."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When it is expected to reopen; shown to the guest when known."},"offerVirtualQueueReturn":{"type":"boolean","default":false,"description":"Offer a virtual-queue return window at the denied scan, where the attraction has a queue."},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The virtual queue the return window is taken in."}}},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]}
}
```
