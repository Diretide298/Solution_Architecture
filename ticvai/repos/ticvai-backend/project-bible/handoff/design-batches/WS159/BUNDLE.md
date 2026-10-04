# WS159 — Resource Management Configuration board 5

**10 screens · 12 operations · 10 schemas · 3 permissions**

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
  `RESOURCE_BOOK, RESOURCE_CONFIGURE, RESOURCE_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-893` | Experience Resource Requirement Builder | D | 11 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-894` | Staff-to-Experience Qualification Mapping | D | 19 | 11 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-895` | Resource Combination Builder | D | 28 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-896` | Ticket Demand & Resource Capacity Mapping | D | 3 | 17 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-897` | Customer Resource Selection Configuration | D | 1 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-898` | Skill-Based & Smart Resource Selection | D | 4 | 22 | 6 | 22 | 1 | 0 | — | notStarted (—) |
| `BO-899` | Customer / Cashier Resource Assignment Experience | D | 1 | 0 | 6 | 4 | 2 | 6 | — | notStarted (—) |
| `BO-900` | Dynamic Resource Allocation Engine | D | 10 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-901` | Priority, Scoring & Allocation Policy | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-902` | Automatic Replacement & Assignment Recovery | D | 8 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-897, BO-899, BO-901 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-893` Experience Resource Requirement Builder

**Define which operational resources are required for each attraction, experience, ticket product, session, or service.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-893 |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `experienceId` (navigation) |
| Route | `/rentals/experience-resource-requirement-builder-bo-893` |

**Known gaps.** **Experience Resource Requirement Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The landing screen of the experience board: for one experience (Private Ski Lesson, VIP Cabana Experience), the resources it needs before it can be sold - staff, space, equipment, optional extras - with quantity, whether each is assigned automatically or chosen, and a visual requirement map. This is what makes "guests buy products, not resources" work. The one thing to get right: a slot is sellable only when every mandatory requirement can be met, and the screen says so in its preview.

**Known correction pending (do not draw the wrong version)**

- **The gap note says the screen declares no write** Why: setExperienceResourceRequirements is bound; the note is stale. *(source: screens/P08-venue-back-office.yaml#BO-893; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The requirement properties and the "Visual Requirement Map" heading are drawn as selectFields** Why: They are per-row properties and an output diagram. *(source: screens/P08-venue-back-office.yaml#BO-893; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Minimum/maximum quantity, fixed/dynamic quantity, customer visible, auto-assign, allocation timing, priority and effective dates have no field on a requirement** Why: ResourceRequirement carries type, category, resource, quantity, mandatory, qualifications, attributes and substitutes only. *(source: screens/P08-venue-back-office.yaml#BO-894 / contracts/satellite/resources.yaml#/components/schemas/ResourceRequirement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How is the pre-assigned model recorded - a named instructor mapped to a specific performance slot in advance (DI-482)?** → Drawn default accepted: Draw "Pre-assigned" on a requirement row with a link "Assign per session" that opens the performance's resource bookings; greyed until an operation exists. *(decided by Chinmay, 2026-10-02; DEC-509 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Mandatory/optional | select field | — | — | — | — | — | — |
| Minimum quantity | select field | — | — | — | — | — | — |
| Maximum quantity | select field | — | — | — | — | — | — |
| Fixed/dynamic quantity | select field | — | — | — | — | — | — |
| Customer visible | select field | — | — | — | — | — | — |
| Customer selectable | select field | — | — | — | — | — | — |
| Auto-assign | select field | — | — | — | — | — | — |
| Allocation timing | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Visual Requirement Map | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Experience selection**: Venue (session), attraction, experience, ticket product and variant, session type and effective period, as cascading pickers; the status toggle shows whether requirements are in force. *(source: screens/P08-venue-back-office.yaml#BO-893)*
- **Requirement rows**: Each row - what is required (specific resource, resource type, category, package, staff role, skill, certification, space, equipment, rental item), quantity (min-max, or fixed), mandatory/optional, required level or certification for staff, assignment model (Pre-assigned named resource / Assigned at sale), customer visible, allocation timing, priority, effective dates. *(source: screens/P08-venue-back-office.yaml#BO-894 / contracts/satellite/resources.yaml#/components/schemas/ResourceRequirement / DI-482)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Requirement map**: Experience at the centre with branches Required staff, Required space, Required equipment, Optional resources, each node showing quantity and rule. *(source: screens/P08-venue-back-office.yaml#BO-894)*
- **Sellability preview**: For a chosen date, the slots with a tick or the missing requirement ("14:00 - no Level 3 instructor free"); the pack's rule that an open slot is not enough. *(source: screens/P08-venue-back-office.yaml#BO-893 / screens/P08-venue-back-office.yaml#BO-902)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save requirements**: Replaces the experience's requirement set (VO-R04); allocation at sale then fills it. *(source: contracts/satellite/resources.yaml#setExperienceResourceRequirements)*
- **Board tiles**: Links to qualification mapping (BO-894), combinations (BO-895), demand mapping (BO-896), selection policy (BO-897), smart selection (BO-898), cashier experience (BO-899), allocation engine (BO-900), scoring (BO-901), recovery (BO-902). *(source: screens/P08-venue-back-office.yaml#BO-893)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-894` Staff-to-Experience Qualification Mapping: *Staff-to-Experience Qualification Mapping*; carries `experienceId`
- → `BO-895` Resource Combination Builder: *Resource Combination Builder*; carries `packageId`
- → `BO-896` Ticket Demand & Resource Capacity Mapping: *Ticket Demand & Resource Capacity Mapping*
- → `BO-897` Customer Resource Selection Configuration: *Customer Resource Selection Configuration*
- → `BO-898` Skill-Based & Smart Resource Selection: *Skill-Based & Smart Resource Selection*
- → `BO-899` Customer / Cashier Resource Assignment Experience: *Customer / Cashier Resource Assignment Experience*
- → `BO-900` Dynamic Resource Allocation Engine: *Dynamic Resource Allocation Engine*
- → `BO-901` Priority, Scoring & Allocation Policy: *Priority, Scoring & Allocation Policy*
- → `BO-902` Automatic Replacement & Assignment Recovery: *Automatic Replacement & Assignment Recovery*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The experience resource requirement configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the experience resource requirement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No experience resource requirement configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Removing a requirement from an experience already on sale**: Confirm naming future bookings that will no longer receive the resource. *(source: designer default)*
- **Requirement that no resource in the venue can ever meet**: Warn "No resource of type Instructor Level 4 exists at Summit Peaks". *(source: contracts/satellite/resources.yaml#suggestResources)*

#### Consistency with other screens

- Match `BO-861`: A requirement may reference a package; same component picker.
- Match `BO-015`: Performances (time slots) belong to the ticketing performance calendar; requirements attach to them, they do not create slots (DI-481).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
experience: Private Ski Lesson - Standard - Summit Peaks Ski School - 1 Oct 2026 to 30 Apr 2027
requirements:
- what: Ski instructor
  qty: 1
  rule: Level 3+, Instructor licence valid
  mandatory: true
  model: Assigned at sale
- what: Training Area
  qty: 1
  mandatory: true
  model: Assigned at sale
- what: Ski equipment set
  qty: 1 per participant
  mandatory: false
  customerVisible: true
- what: Helmet
  qty: 1 per participant
  mandatory: false
  model: Auto-include
```

#### Permissions

- `getExperienceResourceRequirements` → `RESOURCE_VIEW` (read) · staff
- `setExperienceResourceRequirements` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: two assignment models — pre-assigned (named vehicle/instructor/room mapped to a time slot in advance) and dynamic (only type + quantity, e.g. "one SUV and one guide", with an available resource auto-assigned at sale). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models; 5. Key Decisions · DI-482)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-893` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-893`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 1: Opens Experience Resource Requirement Builder → Define which operational resources are required for each attraction, experience, ticket product, session, or service.
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F268 branch at step 1 (expected): when Nothing has been set up on Experience Resource Requirement Builder yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F268 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-893?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-894`, `BO-895`, `BO-896`, `BO-897`, `BO-898`, `BO-899`, `BO-900`, `BO-901`, `BO-902`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-894` Staff-to-Experience Qualification Mapping

**Define which types of employees are permitted to deliver a specific experience.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-894 |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `experienceId` (navigation) |
| Route | `/rentals/staff-to-experience-qualification-mapping-bo-894` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): setResourceQualifications writes a person's certificates; this screen defines what an experience requires, so it binds the experience requirements read and write …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Which staff may deliver an experience: mandatory requirements (role Ski instructor, Ski instruction Level 3 or higher, instructor licence valid, first aid valid) and preferred ones (customer's language, previous private-lesson experience), with an eligibility preview (38 qualified, 7 with warning, 12 not qualified) and the reason for each person. The one thing to get right: it reuses the skill and certification records of board 3 and never asks for a person's certificates here.

**Known correction pending (do not draw the wrong version)**

- **The eligibility preview's "with warning" and "not qualified" counts and reasons have no source** Why: suggestResources returns only matching, free resources; nobody returns the excluded people or why. *(source: screens/P08-venue-back-office.yaml#BO-895 / contracts/satellite/resources.yaml#suggestResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Requirement rows carry no Preferred strength** Why: requiredQualifications and requiredAttributes are all mandatory; preferred criteria cannot be stored. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceRequirement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): setResourceQualifications (a person's certificates) is bound and the entry parameter is resourceId (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Required role | select field | — | — | — | — | — | — |
| Required skill | select field | — | — | — | — | — | — |
| Minimum skill level | select field | — | — | — | — | — | — |
| Required certification | select field | — | — | — | — | — | — |
| Required language | select field | — | — | — | — | — | — |
| Required venue authorization | select field | — | — | — | — | — | — |
| Experience-specific qualification | select field | — | — | — | — | — | — |
| Preferred attributes | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Resource type | picker: choose a resource type | — | — | `suggestResources` ?resourceTypeId |
| From | date and time picker | — | — | `suggestResources` ?from |
| To | date and time picker | — | — | `suggestResources` ?to |
| Attributes | text field | — | — | `suggestResources` ?attributes |

**Form: Save requirements** (modal, opened by *Save requirements*; *Save requirements* calls `setExperienceResourceRequirements`, *Cancel* sends nothing)

**Collects what `setExperienceResourceRequirements` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

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

- **Experience**: The experience from the board (entry parameter is the experience, not a resource). *(source: contracts/satellite/resources.yaml#setExperienceResourceRequirements)*
- **Mandatory and preferred rows**: Required role, required skill with minimum level, required certification (valid on the session date), required language, venue authorisation, experience-specific qualification; each row tagged Mandatory or Preferred. Values picked from the skill and certification libraries. *(source: screens/P08-venue-back-office.yaml#BO-895 / DI-493)*

#### Outputs: what the screen shows and produces

**Shown**

**Requirements** (data table, from `getExperienceResourceRequirements`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save requirements (secondary button) | `setExperienceResourceRequirements` PUT `/experiences/{experienceId}/resource-requirements` | inline | ResourceRequirement[] | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Eligibility preview**: Four tiles - Qualified, Qualified with warning, Not qualified, Total staff - each opening the list with the reason per person ("First aid expires before 14 Nov", "Level 2 - needs Level 3"). *(source: screens/P08-venue-back-office.yaml#BO-895 / screens/P08-venue-back-office.yaml#BO-894)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rule**: Saves as the qualification part of the experience's staff requirement; assignment of anyone failing a mandatory row is then refused. *(source: contracts/satellite/resources.yaml#setExperienceResourceRequirements / DI-493)*
- **Test rule against all staff**: Recomputes the preview for a chosen date. *(source: screens/P08-venue-back-office.yaml#BO-894)*

**Data it reads**: `suggestResources` (onLoad, Staff who qualify); `getExperienceResourceRequirements` (onLoad, The qualifications the experience requires)

**Where the user goes next**

- → `BO-893` Experience Resource Requirement Builder: *Back to Experience Resource Requirement Builder*; carries `experienceId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff-to-experience qualification mapping configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff-to-experience qualification mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff-to-experience qualification mapping configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Rule leaves nobody qualified**: Warning "No staff meet this rule - the experience cannot be sold"; save still allowed with confirmation. *(source: screens/P08-venue-back-office.yaml#BO-893)*

#### Consistency with other screens

- Match `BO-877`: The lead's rule engine is the same rule for the same experience (VO-R14); draw this screen as BO-877's editor opened from the experience, with the same builder and the same Qualified / Warning / Not qualified result.
- Match `BO-875`: Skills and levels picked from that library.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
experience: Advanced Private Ski Lesson
mandatory:
- Role = Ski instructor
- Ski instruction Level 3 or higher
- Instructor licence valid
- First aid valid
preferred:
- Customer language match
- Previous private-lesson experience
preview:
  qualified: 38
  warning: 7
  notQualified: 12
  total: 57
```

#### Permissions

- `suggestResources` → `RESOURCE_VIEW` (read) · staff
- `getExperienceResourceRequirements` → `RESOURCE_VIEW` (read) · staff
- `setExperienceResourceRequirements` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.53 | AI shall recommend optimal resources. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.54 | AI shall recommend suitable staff based on skills and availability. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.56 | AI shall propose alternatives for scheduling conflicts. | Ticketing Catalogue | CONTRACTED | `suggestResources` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- An event can require a specific qualification level (e.g. advanced instructor only, excluding intermediate/beginner), enforced by the system. The resource combination builder sets required types, quantities and mandatory/optional per event (e.g. instructor, area, equipment set). *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-493)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-894` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-894`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 2: Works in Staff-to-Experience Qualification Mapping → Define which types of employees are permitted to deliver a specific experience.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state.
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-894?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save requirements.
- [ ] Every transition is wired: `BO-893`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-895` Resource Combination Builder

**Allow experiences to require multiple resources in valid combinations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-895 |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Option A; Option B) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `packageId` (navigation) |
| Route | `/rentals/resource-combination-builder-bo-895` |

**Known gaps.** **Resource Combination Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Valid ways to staff and equip an experience when there is more than one: "2 Level 2 instructors OR 1 Level 3 + 1 Level 1 instructor", "Meeting room AND AV package AND (1 technician OR 2 AV operators)", with conditions (participant count, ticket type, day, accessibility). Availability is confirmed when at least one combination can be met. The one thing to get right: draw the logic as readable options (Option A / Option B) with AND inside each, not as a free expression.

**Known correction pending (do not draw the wrong version)**

- **The example lines "2 x Level 2 Instructors", "1 x Level 3 Instructor", "1 x Level 1 Instructor" and "+" are drawn as fields** Why: They are the pack's worked example; the screen needs the option cards and logic controls. *(source: screens/P08-venue-back-office.yaml#BO-895; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A package is a flat list of components; OR, alternatives, At least X, Exactly X and conditions cannot be stored** Why: ResourcePackage.components is an array of requirements with no grouping or logic; the combination builder has nowhere to save. *(source: screens/P08-venue-back-office.yaml#BO-895 / contracts/satellite/resources.yaml#/components/schemas/ResourcePackage; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The gap note says no write is declared, and only create is bound (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 2 × Level 2 Instructors | text field | — | — | — | — | — | — |
| 1 × Level 3 Instructor | text field | — | — | — | — | — | — |
| + | select field | — | — | — | — | — | — |
| 1 × Level 1 Instructor | text field | — | — | — | — | — | — |

**Form: Save combination** (modal, opened by *Save combination*; *Save combination* calls `updateResourcePackage`, *Cancel* sends nothing)

**Collects what `updateResourcePackage` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `updateResourcePackage` body |
| Code `code` | text field | required | — | — | — | — | `updateResourcePackage` body |
| Name `name` | text field | required | — | — | — | — | `updateResourcePackage` body |
| Description `description` | text area | optional | — | — | — | — | `updateResourcePackage` body |
| Applicable venues `applicableVenueIds` | multi-picker: choose applicable venues | optional | — | — | — | — | `updateResourcePackage` body |
| Components `components` | repeatable rows | optional | — | — | — | — | `updateResourcePackage` body |
| ID `components[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `updateResourcePackage` body |
| Resource type `components[].resourceTypeId` | picker: choose a resource type | optional | — | — | shows names, sends the id | — | `updateResourcePackage` body |
| Category `components[].categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateResourcePackage` body |
| Resource `components[].resourceId` | picker: choose a resource | optional | — | — | shows names, sends the id | A fixed component, and the exception rather than the rule. Meeting Room A really is Meeting Room A; the technician is not. | `updateResourcePackage` body |
| Quantity `components[].quantity` | number field | required | 1 | — | — | — | `updateResourcePackage` body |
| Mandatory `components[].mandatory` | toggle | optional | on | — | — | — | `updateResourcePackage` body |
| Required qualifications `components[].requiredQualifications` | list of values (chips) | optional | — | — | — | — | `updateResourcePackage` body |
| Required attributes `components[].requiredAttributes` | key and value settings | optional | — | — | — | — | `updateResourcePackage` body |
| Substitute resources `components[].substituteResourceIds` | multi-picker: choose substitute resources | optional | — | — | — | — | `updateResourcePackage` body |
| Scope path `components[].scopePath` | text field | optional | — | — | — | — | `updateResourcePackage` body |
| Allocation priority `allocationPriority` | number field | optional | 0 | — | — | — | `updateResourcePackage` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateResourcePackage` body |
| Effective to `effectiveTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateResourcePackage` body |
| Minimum minutes `minimumMinutes` | number field (minutes) | optional | — | — | — | — | `updateResourcePackage` body |
| Maximum minutes `maximumMinutes` | number field (minutes) | optional | — | — | — | — | `updateResourcePackage` body |
| Requires approval `requiresApproval` | toggle | optional | off | — | — | — | `updateResourcePackage` body |
| Internal cost `internalCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateResourcePackage` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `updateResourcePackage` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Combination logic**: Logic type per group - All of (AND), One of (OR), At least X, Exactly X, Optional; alternatives as Option A, Option B cards, each a table of resource/package, type, quantity, mandatory. *(source: screens/P08-venue-back-office.yaml#BO-895)*
- **Conditions**: "Use this option when" builder - participant count range, ticket type, customer type, venue, day, time, variant, accessibility need. *(source: screens/P08-venue-back-office.yaml#BO-895)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save combination (secondary button) | `updateResourcePackage` PUT `/resource-packages/{packageId}` | ResourcePackage | ResourcePackage | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validation result**: Per option - availability, dependency rules, circular requirements, qualification, capacity, venue restrictions ticked or explained; and "At least one option can be met on 14 Oct 10:00" for a test date. *(source: screens/P08-venue-back-office.yaml#BO-895 / screens/P08-venue-back-office.yaml#BO-896)*
- **Dependency view**: A tab showing the combination as a tree of required resources. *(source: screens/P08-venue-back-office.yaml#BO-895)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save combination**: Saves the combination for the experience; editing an existing one is a full replace (VO-R04). *(source: contracts/satellite/resources.yaml#createResourcePackage / contracts/satellite/resources.yaml#updateResourcePackage)*

**Data it reads**: `listResourcePackages` (onLoad, Existing combinations)

**Where the user goes next**

- → `BO-893` Experience Resource Requirement Builder: *Back to Experience Resource Requirement Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource combination configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource combination untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource combination configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Two options both valid**: The allocation policy picks (rotation by default); the screen shows the option order as the tie-break. *(source: contracts/satellite/resources.yaml#getResourceAllocationPolicy)*
- **An option refers to itself through a package**: Refused as circular with the path. *(source: screens/P08-venue-back-office.yaml#BO-895)*

#### Consistency with other screens

- Match `BO-861`: Packages are the building blocks of options; the lead's BO-861 note pointing the combination builder at BO-894 means this screen, BO-895.
- Match `BO-893`: A combination is one kind of requirement on the experience.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
experience: Group Ski Lesson (up to 16)
options:
- option: A
  components: 2 x Ski instructor Level 2
- option: B
  components: 1 x Ski instructor Level 3 + 1 x Ski instructor Level 1
condition: Option B only when participants 9-16
```

#### Permissions

- `listResourcePackages` → `RESOURCE_VIEW` (read) · staff
- `createResourcePackage` → `RESOURCE_CONFIGURE` (configure) · staff
- `updateResourcePackage` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- An event can require a specific qualification level (e.g. advanced instructor only, excluding intermediate/beginner), enforced by the system. The resource combination builder sets required types, quantities and mandatory/optional per event (e.g. instructor, area, equipment set). *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-493)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-895` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-895`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 4: Works in Resource Combination Builder → Allow experiences to require multiple resources in valid combinations.

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-895?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save combination.
- [ ] Every transition is wired: `BO-893`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-896` Ticket Demand & Resource Capacity Mapping

**Connect ticket sales and participant quantity directly to resource requirements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-896 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/ticket-demand-resource-capacity-mapping-bo-896` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How ticket sales turn into resource demand, and how resource supply caps what can be sold: Fixed (1 cabana per reservation), Ratio (1 instructor per 8), Tiered (1-8 -> 1, 9-16 -> 2, 17-24 -> 3) or Capacity-based (training area holds 30). The live calculator shows "Session capacity 40, ratio 1:8, 4 qualified instructors free - you can sell 32". The one thing to get right: the saleable number is the smaller of venue capacity and what resources can support, and it is shown as the headline.

**Known correction pending (do not draw the wrong version)**

- **The screen binds getResourceUtilisation and draws a utilisation table with a capacity detail panel** Why: Minutes of utilisation cannot compute a saleable capacity; the screen is a per-experience capacity model with a live calculator. *(source: screens/P08-venue-back-office.yaml#BO-896 / contracts/satellite/resources.yaml#getResourceUtilisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No field stores the capacity model, ratio or tiers, and no operation computes resource-supported capacity** Why: ResourceRequirement has a single quantity; the pack's core rule (sell no more than resources can deliver) has no source. *(source: screens/P08-venue-back-office.yaml#BO-896 / contracts/satellite/resources.yaml#/components/schemas/ResourceRequirement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Session capacity and Maximum operational capacity tiles have no field (already noted by the package)** Why: Confirmed; they need the performance capacity and the computed figure. *(source: screens/P08-venue-back-office.yaml#BO-896; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does the ratio apply per sales channel (DI-494 says assignment may vary by channel) or per experience only?** → Drawn default accepted: Per experience; channel differences live in the selection policy (BO-897). *(decided by Chinmay, 2026-10-02; DEC-510 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Group by | select field | — | — | — | — | Sends `?groupBy=` (resource, resourceType, category, venue). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Capacity model**: One choice - Fixed, Ratio-based, Tiered, Capacity-based, Custom formula; the fields below change with it. *(source: screens/P08-venue-back-office.yaml#BO-896)*
- **Ratio / tiers**: Ratio "1 [Instructor] per [8] participants"; tiers as rows "from-to participants -> N resources", contiguous with no gaps. *(source: screens/P08-venue-back-office.yaml#BO-896 / DI-494)*
- **Participant source and limits**: Count from booked participants (tickets sold) with min and max participants per session. *(source: screens/P08-venue-back-office.yaml#BO-896)*
- **Oversell policy**: Off by default; when on, an authorised oversell margin with approver; otherwise sales stop at the resource-supported capacity. *(source: screens/P08-venue-back-office.yaml#BO-896)*

#### Outputs: what the screen shows and produces

**Shown**

**Session capacity** (metric tile): The pack asks for session capacity; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Session capacity | text | not in the schema: `Session capacity` |

**Maximum operational capacity** (metric tile): The pack's 32 of 40: capacity the available resources can support. Nothing computes it.

| Shows | Format | Notes |
|---|---|---|
| Maximum operational capacity | text | not in the schema: `Maximum operational capacity` |

**Resource capacity** (data table, from `getResourceUtilisation`)

| Shows | Format | Notes |
|---|---|---|
| Label | text | — |
| Available minutes | 1,234 | — |
| Booked minutes | 1,234 | — |
| Blocked minutes | 1,234 | — |
| Utilisation percent | 1,234.5 | — |
| Booking count | 1,234 | — |

**Capacity mapping for the selected resource** (detail panel, from `getResourceUtilisation`): The mapping chain is Ticket demand, participants, resource demand, resource capacity, saleable capacity.

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Available minutes | 1,234 | — |
| Booked minutes | 1,234 | — |
| Utilisation percent | 1,234.5 | — |
| Capacity model | text | not in the schema: `Capacity model` |
| Resource ratio | text | not in the schema: `Resource ratio` |
| Available qualified resources | text | not in the schema: `Available qualified resources` |
| Maximum operational capacity | text | not in the schema: `Maximum operational capacity` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Live capacity calculation**: Five boxes in a chain - Booked participants, Ratio, Required resources, Available qualified resources, Saleable participants - with the sentence "This session can accept up to 32 participants based on 4 available qualified instructors" and the limiting factor named. *(source: screens/P08-venue-back-office.yaml#BO-896)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save mapping**: Saves the model for the experience; ticket availability then reflects it across channels. *(source: screens/P08-venue-back-office.yaml#BO-896 / DI-494)*

**Data it reads**: `getResourceUtilisation` (onLoad, Capacity against demand)

**Where the user goes next**

- → `BO-893` Experience Resource Requirement Builder: *Back to Experience Resource Requirement Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket demand resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket demand resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket demand resource yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ticket demand resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **An instructor calls in sick after 28 tickets are sold at 1:8 with 4 instructors**: Saleable capacity drops to 24; sales stop and the screen shows "Oversold by 4 - recovery needed" linking to BO-902. *(source: screens/P08-venue-back-office.yaml#BO-896 / DI-497)*
- **Shared resource full (a room with pods)**: Further sales blocked and reopened automatically if a booking is cancelled. *(source: DI-496)*

#### Consistency with other screens

- Match `BO-015`: Session capacity is the performance capacity from the ticketing performance calendar; this screen only caps it.
- Match `BO-893`: The ratio applies to a requirement row on the experience.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
experience: Group Ski Lesson - Sat 10 Oct 2026 10:00
model: Ratio 1 instructor per 8
calc:
  sessionCapacity: 40
  booked: 24
  requiredInstructors: 3
  availableQualified: 4
  saleable: 32
  limitedBy: Qualified instructors
```

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resource allocation is fixed-quantity or ratio-based/dynamic — e.g. one tour guide covers up to 10 tickets, and resources are added as sales grow. Whether resources are auto-assigned by type or specifically allocated can vary by sales channel. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-494)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-896` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-896`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 6: Works in Ticket Demand & Resource Capacity Mapping → Connect ticket sales and participant quantity directly to resource requirements.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-896?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-893`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-897` Customer Resource Selection Configuration

**Control whether customers or cashiers may choose a specific staff member or resource during purchase.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-897 |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/customer-resource-selection-configuration-bo-897` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of the resource selection policy.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Whether a guest or cashier may choose the resource for a ticket type: no choice (assigned automatically), choose a type or level ("Instructor Level 3"), choose a specific person ("Maria Santos"), or state a preference the platform may override - set per ticket type and, in the pack, per channel. Decided 26 August: private-session products may let the guest pick an instructor; group sessions auto-assign without showing a choice. The one thing to get right: sensitive staff data never reaches the guest card.

**Known correction pending (do not draw the wrong version)**

- **A selectField "No Selection" stands for the whole mode choice** Why: The four modes are one choice drawn as cards. *(source: screens/P08-venue-back-office.yaml#BO-897; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The policy has two modes (autoAssign, guestMayChoose), no channel dimension and no card-field settings** Why: The pack's resource-type selection, preference only, per-channel behaviour and card content cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-897 / contracts/satellite/resources.yaml#/components/schemas/ResourceSelectionPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Write bound with no read of the current policy** Why: The form opens blank and overwrites the ticket type's policy. *(source: contracts/satellite/resources.yaml#setResourceSelectionPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| No Selection | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ticket type**: The policy is one per ticket type; pick the ticket type first (Private Ski Lesson 60 min). *(source: contracts/satellite/resources.yaml#setResourceSelectionPolicy / DI-504)*
- **Selection mode**: Four cards - No selection, Resource type selection, Specific resource selection, Preference only; disabled with the reason when the resource type is not customer selectable (BO-855). *(source: screens/P08-venue-back-office.yaml#BO-897 / contracts/satellite/resources.yaml#createResourceType)*
- **Channels**: Tabs POS, B2C website, Mobile app, B2B portal, Call centre, API; each can narrow the mode (e.g. B2B auto only, POS cashier may override). *(source: screens/P08-venue-back-office.yaml#BO-897 / DI-494)*
- **Guest card content**: Tick list of what the card shows - photo, name, role, skill level, languages, availability, next available time, venue, suitability, customer-facing description. Internal ID, employment type and cost/salary are listed but cannot be ticked, labelled "Never shown to guests". *(source: screens/P08-venue-back-office.yaml#BO-897 / screens/P08-venue-back-office.yaml#BO-898)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Card preview**: A guest-side resource card rendered with the ticked fields in the tenant brand (VO-R15), Arabic and English. *(source: DI-296 / DI-297 / ADR-0011 / DI-019)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save channel settings**: Replaces the ticket type's policy (one PUT per ticket type). *(source: contracts/satellite/resources.yaml#setResourceSelectionPolicy)*

**Where the user goes next**

- → `BO-893` Experience Resource Requirement Builder: *Back to Experience Resource Requirement Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer resource selection configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer resource selection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer resource selection configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Guest picks an instructor who then becomes unavailable**: Specific selection - the guest is told and offered another time or instructor; Preference only - another eligible instructor is assigned and the guest is notified. *(source: screens/P08-venue-back-office.yaml#BO-897 / contracts/satellite/resources.yaml#allocateResources)*
- **Group session product**: Mode fixed to No selection with "Group sessions are assigned automatically (decided 26 Aug)". *(source: DI-504 / TRACKER Actions row 160)*

#### Consistency with other screens

- Match `WEB-005`: The guest booking flow shows the instructor choice only when this policy allows it.
- Match `BO-899`: The cashier assignment screen follows the POS channel setting.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policies:
- ticketType: Private Ski Lesson 60 min
  mode: Specific resource selection
  channels: B2C and app choose; POS may override; B2B auto
- ticketType: Group Ski Lesson
  mode: No selection
card:
  name: Maria Santos
  level: Level 3
  languages: Arabic, English
  next: Today 14:00
```

#### Permissions

- `setResourceSelectionPolicy` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision (Qossai, Ski Dubai): instructor choice is a per-ticket-type setting — private-session products may let the guest pick a specific instructor; group-session products auto-assign without showing a choice. Private and group are separate, separately priced products (a private request on a group instructor is its own product). *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-504)*
- Resource allocation is fixed-quantity or ratio-based/dynamic — e.g. one tour guide covers up to 10 tickets, and resources are added as sales grow. Whether resources are auto-assigned by type or specifically allocated can vary by sales channel. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-494)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-897` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-897`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 8: Works in Customer Resource Selection Configuration → Control whether customers or cashiers may choose a specific staff member or resource during purchase.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-897?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-893`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-898` Skill-Based & Smart Resource Selection

**Allow users to request the type or capability of resource they require without manually choosing an individual resource.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-898 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/skill-based-smart-resource-selection-bo-898` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Find resources by what they can do rather than by name - "Ski instructor, Level 3+, Arabic speaking, tomorrow 14:00" - returning only eligible resources as cards with the criteria each one meets. Used by supervisors and cashiers who do not know staff by name. The one thing to get right: the criteria are structured controls built from the tenant's searchable attributes, and the result explains itself in facts, not an AI percentage (26 August decision).

**Known correction pending (do not draw the wrong version)**

- **"Required attributes" is a single textField sending the raw attributes query** Why: Each searchable attribute needs its own control; staff cannot be expected to type code=value pairs. *(source: screens/P08-venue-back-office.yaml#BO-898 / contracts/satellite/resources.yaml#suggestResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table columns include venueId, scopePath, id, isActive and a "Match score" that is not a field** Why: Spec leakage (VO-R12); matching is attribute based and returns no score (DI-495). *(source: DI-495; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource type | select field | — | — | — | — | Sends `?resourceTypeId=` (e.g. Ski Instructor). | — |
| From | date picker | — | — | — | — | Sends `?from=`. | — |
| To | date picker | — | — | — | — | Sends `?to=`. | — |
| Required attributes | text field | — | — | — | — | Sends `?attributes=`: level, language, skill, accessibility capability, equipment type, room capacity. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Resource type | picker: choose a resource type | — | — | `suggestResources` ?resourceTypeId |
| From | date and time picker | — | — | `suggestResources` ?from |
| To | date and time picker | — | — | `suggestResources` ?to |
| Attributes | text field | — | — | `suggestResources` ?attributes |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resource type, date, time**: Type select (Ski instructor), date picker and time (or window); the search runs only for resources free in that window. *(source: contracts/satellite/resources.yaml#suggestResources)*
- **Required attributes**: One control per searchable attribute of the chosen type (BO-858) - Skill level (Level 3 or higher), Language (chips Arabic, English...), Accessibility capability, Equipment type, Room capacity (min), Resource feature; never a raw text box of "language=ar,skillLevel=3". *(source: screens/P08-venue-back-office.yaml#BO-898 / contracts/satellite/resources.yaml#createResourceAttribute / DI-495)*

#### Outputs: what the screen shows and produces

**Shown**

**Eligible resources** (data table, from `suggestResources`): Only eligible resources are returned. The pack ranks them with a match percentage (Maria Garcia 98%), which is not a field.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Code | text | — |
| Kind | chip: Cabana, Lounger, Locker, Wheelchair, Stroller, Equipment… | BL-135. `locker` was an entitlement kind in `orders` and nothing issued, assigned or released one. |
| Venue | the name it points at, never the id | — |
| Attributes | grouped details | Configurable per kind — capacity, size, shade, power, poolside. |
| Requires qualification | list or chips (count when long) | Qualification codes a person must hold to be assigned to this. |
| Status | chip: Available, Booked, Checked out, Maintenance, Retired | — |
| Match score | text | not in the schema: `Match score` |

**The selected resource** (detail panel, from `suggestResources`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Kind | chip: Cabana, Lounger, Locker, Wheelchair, Stroller, Equipment… | BL-135. `locker` was an entitlement kind in `orders` and nothing issued, assigned or released one. |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Attributes | grouped details | Configurable per kind — capacity, size, shade, power, poolside. |
| Requires qualification | list or chips (count when long) | Qualification codes a person must hold to be assigned to this. |
| Setup minutes | 1,234 | Before the booking, not inside it. An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that … |
| Teardown minutes | 1,234 | After the booking. Kept as it is (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added … |
| Status | chip: Available, Booked, Checked out, Maintenance, Retired | — |
| Is active | yes / no (icon or chip) | — |
| Match score | text | not in the schema: `Match score` |
| Match reasons | text | not in the schema: `Match reasons` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Result cards**: Photo or icon, name, role and level, languages, venue, next free time, and a "Meets 4 of 4" line with the ticked facts (Level 3, Arabic, Available, Same venue, No overtime). "Show best match first" orders by the allocation policy's score (BO-901) when on, otherwise by name. No internal ids, venue ids or scope paths (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-899 / screens/P08-venue-back-office.yaml#BO-898 / DI-495)*
- **Detail panel**: Attributes, qualifications with expiry, setup/teardown, today's bookings; Assign or Use in booking. *(source: contracts/satellite/resources.yaml#getResource)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search**: Runs the attribute match for the window; results update as criteria change. *(source: contracts/satellite/resources.yaml#suggestResources)*
- **Select**: Hands the chosen resource back to the flow that opened the screen (a booking, BO-899, BO-872). *(source: designer default)*

**Data it reads**: `suggestResources` (onLoad, Attribute matching, not a model)

**Where the user goes next**

- → `BO-893` Experience Resource Requirement Builder: *Back to Experience Resource Requirement Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The skill-based smart resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the skill-based smart resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No skill-based smart resource yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the skill-based smart resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No eligible resource**: "No Level 3 Arabic-speaking instructor free at 14:00" with the nearest alternatives (another time, relax one criterion). *(source: screens/P08-venue-back-office.yaml#BO-900)*
- **Attribute not marked searchable**: Not offered as a criterion; administrators see "Make Skill level searchable to use it here". *(source: contracts/satellite/resources.yaml#createResourceAttribute)*

#### Consistency with other screens

- Match `BO-865`: Same result card and "Meets N of N" wording as calendar discovery.
- Match `BO-899`: Cashier cards use this match, restricted by the selection policy.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
criteria: Ski instructor, Level 3+, Arabic, Sun 11 Oct 2026 14:00, Summit Peaks
results:
- name: Maria Santos
  level: Level 3
  languages: Arabic, English
  next: '14:00'
  meets: 4 of 4
- name: Ahmed Al Mansoori
  level: Level 3
  languages: Arabic, English
  next: '14:00'
  meets: 4 of 4 - 6 h worked today
- name: Omar Haddad
  level: Level 3
  languages: Arabic
  next: '15:30'
  meets: 3 of 4 - free from 15:30
```

#### Permissions

- `suggestResources` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.53 | AI shall recommend optimal resources. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.54 | AI shall recommend suitable staff based on skills and availability. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.56 | AI shall propose alternatives for scheduling conflicts. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.1 | The system should allow management of all types of resources: - Areas with limited capacity (e.g. Meeting rooms, Cabanas, etc.) - Staff (e.g. Ski School Instructors, etc.) - Objects (e.g. Strollers … | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.2 | The system should allow easy creation and tracking of resources, and link them to individual attraction experiences, so that a ticket is not only based on available time-slots but also on relevant … | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.14 | Ability to define resources required for each event along with the availability schedule. The resources could be of any type: | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.15 | Venues & Spaces: Auditoriums, halls, rooms, stages, breakout areas. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.16 | Equipment & Assets: AV systems, lighting, sound systems, projectors, chairs, booths. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.17 | Staff & Personnel: Event managers, ushers, security, performers, technical crew, mascots, hosts. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.23 | System shall support configurable resource types including staff, venues, equipment, rooms and rental items. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.24 | System shall support categorization of resources. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| 1.2.25 | System shall support parent-child resource relationships. | Ticketing Catalogue | CONTRACTED | data `Resource` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision (Chinmay): skill-based resource matching uses straightforward attribute/keyword matching (skill level, language), not a full AI-matching system. *(agreed · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment; 5. Key Decisions · DI-495)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-898` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-898`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 10: Works in Skill-Based & Smart Resource Selection → Allow users to request the type or capability of resource they require without manually choosing an individual resource.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-898?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-893`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-899` Customer / Cashier Resource Assignment Experience

**Provide the fast, visual assignment interface shown during ticket or experience purchase. This screen shall be optimized for speed and simplicity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-899 |
| Who uses it | venue staff holding `RESOURCE_BOOK`, `RESOURCE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§AI Recommended Option) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/customer-cashier-resource-assignment-experience-bo-899` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The cashier's (and authorised channels') fast path to put a resource on a sale: Experience, Date, Time, Resource, Confirm. Times show available, few left, full and resource-dependent states; after a time is chosen, eligible instructors appear as cards with one recommended. The one thing to get right: the recommended card is exactly who the platform would assign anyway, so one tap confirms it, and a choice of person is offered only where the ticket type allows it.

**Known correction pending (do not draw the wrong version)**

- **A selectField "Best Match" with a sparkle and an unlabelled primary button** Why: Best match is a badge on a card; the primary is Confirm. *(source: screens/P08-venue-back-office.yaml#BO-899; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A cashier sale-time experience is placed in the venue back office (P08)** Why: The pack describes the POS and customer channel flow; the working screen belongs to the POS sale and guest booking, with P08 holding only configuration. *(source: screens/P08-venue-back-office.yaml#BO-899 / screens/P08-venue-back-office.yaml#BO-902; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "Best match" the next resource by rotation, or the top weighted score?** → Drawn default accepted: Show what the allocation engine would assign (validate-only), whatever the strategy, so recommendation and auto-assignment never disagree. *(decided by Chinmay, 2026-10-02; DEC-511 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ✨ Best Match | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Resource type | picker: choose a resource type | — | — | `suggestResources` ?resourceTypeId |
| From | date and time picker | — | — | `suggestResources` ?from |
| To | date and time picker | — | — | `suggestResources` ?to |
| Attributes | text field | — | — | `suggestResources` ?attributes |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Date and time**: Day strip plus calendar; time list with Available, Few left (amber), Full (struck) and "No instructor" states; a slot open in the schedule but without a qualified resource is shown full with the reason. *(source: screens/P08-venue-back-office.yaml#BO-899 / screens/P08-venue-back-office.yaml#BO-902)*
- **Resource choice**: Cards (photo, name, level, languages, Available) only when the ticket type's policy allows choosing; otherwise a single line "An instructor will be assigned". A guest preference is sent only when the policy permits; otherwise it is not offered. *(source: contracts/satellite/resources.yaml#setResourceSelectionPolicy / contracts/satellite/resources.yaml#allocateResources / DI-504)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Recommended card**: Marked Best match, the result of the allocation engine in validate-only mode for this window, with a one-line reason ("Level 3, speaks Arabic, rotation is due"). *(source: contracts/satellite/resources.yaml#allocateResources / DI-497)*
- **Booking summary**: Experience, date, time, instructor, participants, price in AED. *(source: screens/P08-venue-back-office.yaml#BO-899)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Confirm**: Allocates the resource with the order; a clash since the list loaded returns the unmet requirement and the list refreshes. *(source: contracts/satellite/resources.yaml#allocateResources / contracts/satellite/resources.yaml#/components/schemas/ResourceAllocationProblem)*
- **No resource available**: Offers another time, another date, an alternative resource, the waiting list where configured, and manager override where permitted (named permission, VO-R08). *(source: screens/P08-venue-back-office.yaml#BO-900)*

**Data it reads**: `suggestResources` (onLoad, What is free and suitable)

**Where the user goes next**

- → `BO-893` Experience Resource Requirement Builder: *Back to Experience Resource Requirement Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer cashier resource configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer cashier resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer cashier resource configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Nothing available, or a dependency is missing. Both are named — "no instructor free" and "the stage has no sound system" need different actions from the person … (ResourceAllocationProblem) |

#### Edge cases to draw

- **Cashier picks a non-recommended instructor**: Allowed where the POS channel may override; the receipt records "Cashier choice". *(source: screens/P08-venue-back-office.yaml#BO-897)*
- **Group session product**: No cards; auto-assigned after payment. *(source: DI-504)*

#### Consistency with other screens

- Match `POS-003`: This flow lives in the POS timed-entry sale (P04) and the guest booking flow (WEB-005); the P08 entry is the configuration preview of it.
- Match `BO-898`: Same card layout and facts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
flow: Private Ski Lesson 60 min - Sun 11 Oct 2026 - 14:00 - 2 guests - AED 300.00
times:
- 10:00 Available
- 12:00 Few left
- 14:00 Available (selected)
- 15:00 Few left
- 16:00 Full - no instructor
cards:
- name: Maria Santos
  level: Level 3
  languages: Arabic, English
  tag: Best match
- name: Ahmed Al Mansoori
  level: Level 3
  languages: Arabic, English
- name: Rahul Menon
  level: Level 2
  languages: English, Hindi
  tag: Not eligible - Level 3 required
```

#### Permissions

- `allocateResources` → `RESOURCE_BOOK` (operate) · staff
- `suggestResources` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.57 | AI shall optimize schedules automatically. | Ticketing Catalogue | CONTRACTED_PARTIAL | `allocateResources` |
| 1.2.53 | AI shall recommend optimal resources. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.54 | AI shall recommend suitable staff based on skills and availability. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.56 | AI shall propose alternatives for scheduling conflicts. | Ticketing Catalogue | CONTRACTED | `suggestResources` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision (Qossai, Ski Dubai): instructor choice is a per-ticket-type setting — private-session products may let the guest pick a specific instructor; group-session products auto-assign without showing a choice. Private and group are separate, separately priced products (a private request on a group instructor is its own product). *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-504)*
- Resource allocation is fixed-quantity or ratio-based/dynamic — e.g. one tour guide covers up to 10 tickets, and resources are added as sales grow. Whether resources are auto-assigned by type or specifically allocated can vary by sales channel. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-494)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-899` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-899`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 12: Works in Customer / Cashier Resource Assignment Experience → Provide the fast, visual assignment interface shown during ticket or experience purchase. This screen shall be optimized for speed and simplicity.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-899?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-893`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`, `RESOURCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-900` Dynamic Resource Allocation Engine

**Configure how TICVAI automatically chooses a resource when a customer or cashier does not make a specific selection.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-900 |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/dynamic-resource-allocation-engine-bo-900` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): allocateResources was bound as a live action on a configuration screen; the save is setResourceAllocationPolicy, which was not bound (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How the platform assigns a resource when nobody chooses one: the mode (manual, automatic, recommend and confirm, fully automatic), when it happens (at search, reservation, payment, ticket issue, N hours before, at roster publication, at check-in), when the assignment locks, and whether it reassigns automatically if the resource drops out. The one thing to get right: rotation across all available resources is the default and is shown as the agreed rule, not buried as one option.

**Known correction pending (do not draw the wrong version)**

- **Modes drawn as two selectFields and a textField ("AI recommended + user confirmation"), and "Allocation Timing" as a heading field** Why: Mode is one choice; timing is a select. *(source: screens/P08-venue-back-office.yaml#BO-900; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Allocation mode, timing, lock and reassignment window have no field** Why: ResourceAllocationPolicy stores strategy, resource priority, weights and partial allocation only. *(source: screens/P08-venue-back-office.yaml#BO-900 / contracts/satellite/resources.yaml#/components/schemas/ResourceAllocationPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): allocateResources is bound as a live action on a configuration screen, and the write setResourceAllocationPolicy is not bound (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Manual | select field | — | — | — | — | — | — |
| Automatic | select field | — | — | — | — | — | — |
| AI recommended + user confirmation | text field | — | — | — | — | — | — |
| Fully automatic | select field | — | — | — | — | — | — |
| Allocation Timing | select field | — | — | — | — | — | — |

**Form: Save allocation policy** (modal, opened by *Save allocation policy*; *Save allocation policy* calls `setResourceAllocationPolicy`, *Cancel* sends nothing)

**Collects what `setResourceAllocationPolicy` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Strategy `strategy` | radio group | optional | Rotate | Rotate · Least utilised · Priority order · Nearest first | — | `rotate` is the default because 26 August made it one. | `setResourceAllocationPolicy` body |
| Respect resource priority `respectResourcePriority` | toggle | optional | on | — | — | — | `setResourceAllocationPolicy` body |
| Scoring weights `scoringWeights` | key and value settings | optional | — | — | — | — | `setResourceAllocationPolicy` body |
| Allow partial allocation `allowPartialAllocation` | toggle | optional | off | — | — | False by default. A stage allocated without its sound system is worse than no allocation, because it looks finished. | `setResourceAllocationPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setResourceAllocationPolicy` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Allocation mode**: One choice - Manual, Automatic, Recommend and confirm, Fully automatic. "Fully automatic" is the rule engine (rotation and policy), not an AI acting alone; the label says so. *(source: screens/P08-venue-back-office.yaml#BO-900)*
- **Allocation timing and lock**: Timing select (At payment default); lock "Assignment fixed [2] hours before the experience"; reassignment window "Reassign automatically up to [4] hours before". *(source: screens/P08-venue-back-office.yaml#BO-900 / screens/P08-venue-back-office.yaml#BO-901)*
- **Strategy**: Rotate (default, "Spreads work evenly across available resources - agreed 26 Aug"), Least utilised, Priority order, Nearest first; respect resource priority toggle; allow partial allocation off with its warning. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceAllocationPolicy / DI-497)*
- **Criteria order**: The thirteen criteria as an ordered list (Availability and Qualification fixed at top as mandatory), the rest draggable; weights edited on BO-901. *(source: screens/P08-venue-back-office.yaml#BO-901)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save allocation policy (secondary button) | `setResourceAllocationPolicy` PUT `/resource-allocation-policy` | ResourceAllocationPolicy | ResourceAllocationPolicy | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Policy in force**: Summary sentence "Automatic at payment, rotating; locked 2 h before; reassigned automatically until 4 h before; customer notified". *(source: contracts/satellite/resources.yaml#getResourceAllocationPolicy)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test allocation**: Runs a sample booking in validate-only mode and shows who would be assigned and why; nothing is written. *(source: contracts/satellite/resources.yaml#allocateResources)*
- **Save engine configuration**: Saves the policy; applies to new allocations in every channel (POS, B2C, B2B, API) alike. *(source: screens/P08-venue-back-office.yaml#BO-902 / contracts/satellite/resources.yaml#setResourceAllocationPolicy)*

**Data it reads**: `getResourceAllocationPolicy` (onLoad, The strategy in force)

**Where the user goes next**

- → `BO-893` Experience Resource Requirement Builder: *Back to Experience Resource Requirement Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic resource allocation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic resource allocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic resource allocation configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Lock reached while the assigned resource falls sick**: No automatic change after the lock; the recovery screen raises it for a manager. *(source: screens/P08-venue-back-office.yaml#BO-901 / DI-497)*

#### Consistency with other screens

- Match `BO-901`: BO-900, BO-901 and BO-948 all edit the same allocation policy (VO-R14); draw one editor with sections (Mode and timing, Strategy and scoring, Simulation) and one Save, BO-901 as its home.
- Match `BO-893`: The pre-assigned vs assigned-at-sale model per requirement (DI-482) decides whether this engine runs at all.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  mode: Recommend and confirm
  timing: At payment
  lock: 2 h before
  reassignWindow: until 4 h before
  strategy: Rotate
  partial: false
```

#### Permissions

- `getResourceAllocationPolicy` → `RESOURCE_VIEW` (read) · staff
- `setResourceAllocationPolicy` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resources are one-to-one (dedicated to a booking) or shared (e.g. a meeting room with bookable pods, a vehicle across sequential slots); further sales are blocked once a shared resource's capacity/slot is full and reopened if a booking is cancelled. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-496)*
- Decision: two assignment models — pre-assigned (named vehicle/instructor/room mapped to a time slot in advance) and dynamic (only type + quantity, e.g. "one SUV and one guide", with an available resource auto-assigned at sale). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models; 5. Key Decisions · DI-482)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-900` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-900`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 14: Works in Dynamic Resource Allocation Engine → Configure how TICVAI automatically chooses a resource when a customer or cashier does not make a specific selection.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-900?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save allocation policy.
- [ ] Every transition is wired: `BO-893`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-901` Priority, Scoring & Allocation Policy

**Configure how TICVAI ranks eligible resources when several resources could satisfy the same requirement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-901 |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/priority-scoring-allocation-policy-bo-901` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How eligible resources are ranked when several could do the job: hard rules that can never be broken (availability, mandatory certification, safety qualification) and weighted soft factors (skill match, customer language, same venue, workload balance, customer preference, cost), with a simulation that ranks real candidates for a sample booking and explains each score. The one thing to get right: hard rules are not weights - they sit above the weight table and filter, and the weights total 100%.

**Known correction pending (do not draw the wrong version)**

- **The screen has only Save and Cancel; the gap note says nothing is drawable** Why: The pack lists twelve scoring factors, hard vs soft rules, a worked weighting and a simulation. *(source: screens/P08-venue-back-office.yaml#BO-901; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Validate-only allocation returns the would-be bookings, not scores or a per-factor explanation** Why: The pack requires the system to explain the scoring; nothing returns it. *(source: screens/P08-venue-back-office.yaml#BO-902 / contracts/satellite/resources.yaml#allocateResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **scoringWeights is an untyped map with no factor list** Why: The factors the UI offers are not defined anywhere, so any key could be saved. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceAllocationPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How do strategy (rotate) and weights combine - weights rank and rotation breaks ties, or rotation overrides weights?** → Drawn default accepted: Weights rank; among candidates within 5 points, rotation decides. Show this sentence under the strategy. *(decided by Chinmay, 2026-10-02; DEC-512 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Hard rules**: Fixed list shown as locks - Availability, Mandatory certification, Safety qualification, Capacity; cannot be weighted or switched off. *(source: screens/P08-venue-back-office.yaml#BO-901 / screens/P08-venue-back-office.yaml#BO-902)*
- **Soft factors and weights**: Rows of factor, weight (%) with an impact bar - skill match, certification, customer preference, venue proximity, current workload, equal workload distribution, labour cost, overtime, resource priority, historical assignment, customer continuity, utilisation. Running total must equal 100% before Save; zero removes a factor. *(source: screens/P08-venue-back-office.yaml#BO-901 / contracts/satellite/resources.yaml#/components/schemas/ResourceAllocationPolicy)*
- **Strategy among equals**: Rotate (default) / Least utilised / Priority order / Nearest first, with the 26 August reason under Rotate. *(source: contracts/satellite/resources.yaml#setResourceAllocationPolicy / DI-497)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Simulation result**: For a sample booking (Private Ski Lesson 14:00, Arabic-speaking guest) - ranked candidates with score, rank, and a breakdown per factor ("Skill 30/30, Language 20/20, Same venue 15/15, Workload 12/15"); excluded people listed with the hard rule they fail. *(source: screens/P08-venue-back-office.yaml#BO-901 / screens/P08-venue-back-office.yaml#BO-902)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Simulate**: Runs the sample in validate-only mode; nothing is written. *(source: contracts/satellite/resources.yaml#allocateResources)*
- **Save policy**: Full replace of the venue's allocation policy (VO-R04); "Last changed by" shown. *(source: contracts/satellite/resources.yaml#setResourceAllocationPolicy)*

**Data it reads**: `getResourceAllocationPolicy` (onLoad, Rotation, priority and scoring)

**Where the user goes next**

- → `BO-893` Experience Resource Requirement Builder: *Back to Experience Resource Requirement Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The priority scoring allocation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the priority scoring allocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No priority scoring allocation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the priority scoring allocation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Weights do not total 100%**: Save disabled with "Weights total 95% - add 5%". *(source: designer default)*
- **Policy makes one resource always win (e.g. priority order)**: Note "Cabana 3 will rarely be used under Priority order" from the simulation's utilisation spread. *(source: contracts/satellite/resources.yaml#setResourceAllocationPolicy)*

#### Consistency with other screens

- Match `BO-900`: Same policy record and one editor (VO-R14).
- Match `BO-948`: The policy centre lists this policy and its inheritance; it opens here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
weights:
  skillMatch: 30%
  customerLanguage: 20%
  sameVenue: 15%
  workloadBalance: 15%
  customerPreference: 10%
  cost: 10%
simulation:
- rank: 1
  name: Maria Santos
  score: '97'
  why: Level 3, Arabic, same venue, 4 h today
- rank: 2
  name: Ahmed Al Mansoori
  score: '92'
  why: Level 3, Arabic, 6 h today
- rank: 3
  name: Omar Haddad
  score: '78'
  why: Level 3, Arabic, other venue
```

#### Permissions

- `getResourceAllocationPolicy` → `RESOURCE_VIEW` (read) · staff
- `setResourceAllocationPolicy` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: allocation rotates across all available resources (resource 1, then 2, then 3) rather than reusing the same one; if an assigned resource becomes unavailable the system automatically replaces/reassigns it. *(agreed · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment; 5. Key Decisions · DI-497)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-901` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-901`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 16: Works in Priority, Scoring & Allocation Policy → Configure how TICVAI ranks eligible resources when several resources could satisfy the same requirement.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-901?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-893`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-902` Automatic Replacement & Assignment Recovery

**Detect when an assigned resource becomes unavailable and protect the customer's booking by finding a suitable replacement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-902 |
| Who uses it | venue staff holding `RESOURCE_BOOK` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/automatic-replacement-assignment-recovery-bo-902` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists the bookings affected by a resource becoming unavailable.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** What happens when an assigned resource drops out (sick instructor, broken projector, expired certificate, closed venue): the affected bookings and guests listed, eligible replacements ranked from the approved substitutes, and the recovery mode - automatic, approval required, or manual - with who gets notified. The guest's booking is never lost. The one thing to get right: impact first ("Alex Johnson unavailable - 7 future bookings affected"), then replacements, then one action per booking or for all.

**Known correction pending (do not draw the wrong version)**

- **Automatic / Approval Required / Manual and the four customer-impact options are drawn as eight selectFields** Why: Mode is one choice; notifications are toggles. *(source: screens/P08-venue-back-office.yaml#BO-902; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The screen is entered with one bookingId, but the pack starts from the unavailable resource and its N affected bookings** Why: No read lists the bookings affected by a resource becoming unavailable; recovery is per booking only. *(source: screens/P08-venue-back-office.yaml#BO-902 / contracts/satellite/resources.yaml#replaceResourceAllocation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Recovery mode, notification settings and the recovery audit have no field** Why: replaceResourceAllocation takes a reason and an optional replacement only. *(source: contracts/satellite/resources.yaml#replaceResourceAllocation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The purpose text includes board 6's objective and a list of rental items (CHG-WIR-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Automatic | select field | — | — | — | — | — | — |
| Approval Required | select field | — | — | — | — | — | — |
| Manual | select field | — | — | — | — | — | — |
| Customer Impact | select field | — | — | — | — | — | — |
| Customer notification | select field | — | — | — | — | — | — |
| Updated ticket/booking | select field | — | — | — | — | — | — |
| Employee notification | select field | — | — | — | — | — | — |
| Operational notification | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Recovery mode (configuration)**: One choice - Automatic (replace when all rules are met), Approval required (manager approves the proposal), Manual (manager chooses). *(source: screens/P08-venue-back-office.yaml#BO-902)*
- **Notifications**: Toggles - notify customer, update ticket/booking, notify the new staff member, operational notification; plus "lock replacement N hours before". *(source: screens/P08-venue-back-office.yaml#BO-902)*
- **Reason**: Required for every replacement; prefilled from the trigger (Sick leave, Breakdown, Certification expired). *(source: contracts/satellite/resources.yaml#replaceResourceAllocation)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Trigger and impact**: Trigger chip, the unavailable resource with its status, and counts of affected bookings, customers, experiences, slots and venues; the list of affected bookings by time. *(source: screens/P08-venue-back-office.yaml#BO-902)*
- **Replacements**: Ranked list per booking with facts (Qualified, Available, Same venue, Same language, No overtime) and whether the person is an approved substitute or backup. *(source: screens/P08-venue-back-office.yaml#BO-902 / contracts/satellite/resources.yaml#replaceResourceAllocation)*
- **Recovery audit**: Original resource, trigger, alternatives evaluated, replacement, decided by (person or system), time. *(source: screens/P08-venue-back-office.yaml#BO-902)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Replace (per booking) / Run replacement (all)**: Swaps the resource on each booking keeping the order and guest; omitted replacement lets the platform pick from approved substitutes. *(source: contracts/satellite/resources.yaml#replaceResourceAllocation)*

**Where the user goes next**

- → `BO-893` Experience Resource Requirement Builder: *Back to Experience Resource Requirement Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The automatic replacement recovery configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the automatic replacement recovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No automatic replacement recovery configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No approved substitute is free**: "No approved substitute for 14:00" with options - search all qualified staff (manager), move the guest to another time, or cancel with notice. *(source: screens/P08-venue-back-office.yaml#BO-900 / contracts/satellite/resources.yaml#replaceResourceAllocation)*
- **The guest chose this instructor by name**: Customer approval required before replacing; booking marked "Awaiting guest reply". *(source: screens/P08-venue-back-office.yaml#BO-930 / contracts/satellite/resources.yaml#setResourceSelectionPolicy)*
- **Past the allocation lock**: Automatic mode does not run; the case goes to a manager. *(source: screens/P08-venue-back-office.yaml#BO-901)*

#### Consistency with other screens

- Match `BO-860`: Substitute for / Backup for rules are the approved pool used here.
- Match `BO-930`: Same replacement list and facts as the AI alternative screen.
- Match `BO-910`: A maintenance block on a resource with future bookings opens this screen with the trigger Maintenance.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
trigger: Alex Johnson - Sick leave, Sat 10 Oct 2026
impact:
  bookings: 7
  customers: 9
  experiences: Private lesson x5, Group lesson x2
replacements:
- name: Maria Santos
  facts: Approved substitute, Level 3, available, same venue, no overtime
- name: Ahmed Al Mansoori
  facts: Backup, Level 3, available, 2 h overtime
mode: Approval required
```

#### Permissions

- `replaceResourceAllocation` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: allocation rotates across all available resources (resource 1, then 2, then 3) rather than reusing the same one; if an assigned resource becomes unavailable the system automatically replaces/reassigns it. *(agreed · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment; 5. Key Decisions · DI-497)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-902` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-902`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 5
- Flow F268 *Resource Management Configuration board 5: Experience Resource Requirement …*, step 18: Works in Automatic Replacement & Assignment Recovery → Automatically detect when an assigned resource becomes unavailable and protect the customer's booking by finding a suitable replacement.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-902?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-893`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"allocateResources": {"method":"POST","path":"/resource-allocations","contract":"resources","summary":"Fill a requirement from the pool, rotating rather than repeating","permission":"RESOURCE_BOOK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"createResourcePackage": {"method":"POST","path":"/resource-packages","contract":"resources","summary":"Define a reusable combination","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourcePackage","responds":"ResourcePackage"},
"getExperienceResourceRequirements": {"method":"GET","path":"/experiences/{experienceId}/resource-requirements","contract":"resources","summary":"What an experience needs before it can run","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceRequirement"},
"getResourceAllocationPolicy": {"method":"GET","path":"/resource-allocation-policy","contract":"resources","summary":"How the platform chooses between equally valid resources","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAllocationPolicy"},
"getResourceUtilisation": {"method":"GET","path":"/resource-utilisation","contract":"resources","summary":"How much of each resource's available time was used","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ResourceUtilisation"},
"listResourcePackages": {"method":"GET","path":"/resource-packages","contract":"resources","summary":"Predefined combinations assigned as one","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourcePackage"},
"replaceResourceAllocation": {"method":"POST","path":"/resource-allocations/{bookingId}/replace","contract":"resources","summary":"Swap in a substitute when the allocated resource falls through","permission":"RESOURCE_BOOK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"setExperienceResourceRequirements": {"method":"PUT","path":"/experiences/{experienceId}/resource-requirements","contract":"resources","summary":"Bind resource requirements to an experience","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceRequirement"},
"setResourceAllocationPolicy": {"method":"PUT","path":"/resource-allocation-policy","contract":"resources","summary":"Rotation, priority and scoring","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceAllocationPolicy","responds":"ResourceAllocationPolicy"},
"setResourceSelectionPolicy": {"method":"PUT","path":"/resource-selection-policy","contract":"resources","summary":"Whether the guest may choose the resource, per ticket type","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceSelectionPolicy","responds":null},
"suggestResources": {"method":"GET","path":"/resource-suggestions","contract":"resources","summary":"Resources matching a requirement, by attribute","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceTypeId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"attributes","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"updateResourcePackage": {"method":"PUT","path":"/resource-packages/{packageId}","contract":"resources","summary":"Change a combination","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourcePackage","responds":"ResourcePackage"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true},"resourceTypeId":{"type":"string","format":"uuid","nullable":true,"description":"**The configurable resource type** (`resources.resource_type`, 4 October 2026, CHG-FXC-003). `kind` is the fixed family a type belongs to; this is the tenant's own type within it, and the `resourceTypeId` filter of `suggestResources` and `ResourceRequirement.resourceTypeId` match on it."}}},
"ResourceAllocationPolicy": {"type":"object","x-ticvai-persistence":"resources.allocation_policy","description":"Board 5.08, and the 26 August rotation decision. **Named rather than hidden in the allocator**, so somebody can answer why cabana three never gets used.\n","properties":{"strategy":{"type":"string","enum":["rotate","leastUtilised","priorityOrder","nearestFirst"],"default":"rotate","description":"**`rotate` is the default because 26 August made it one.** *\"rotate across all available resources… rather than repeatedly reusing the same resource, to avoid overburdening any single resource while others remain unused.\"*\n"},"respectResourcePriority":{"type":"boolean","default":true},"scoringWeights":{"type":"object","additionalProperties":{"type":"number"}},"allowPartialAllocation":{"type":"boolean","default":false,"description":"**False by default.** A stage allocated without its sound system is worse than no allocation, because it looks finished.\n"},"scopePath":{"type":"string"}}},
"ResourceBooking": {"type":"object","x-ticvai-persistence":"resources.booking","required":["id","resourceId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/ResourceBookingStatus"},"holdId":{"type":"string","format":"uuid","nullable":true,"description":"The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"},"recurrenceGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"conditionOut":{"type":"string","nullable":true},"conditionIn":{"type":"string","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"}}},
"ResourceBookingStatus": {"type":"string","enum":["reserved","checkedOut","returned","overdue","cancelled","noShow"]},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourcePackage": {"type":"object","x-ticvai-persistence":"resources.resource_package","description":"Board 1.08. **A package may hold placeholders.** \"One technician\" is a slot, and naming a person would make the package unbookable whenever they are off.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"applicableVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"components":{"type":"array","items":{"$ref":"#/components/schemas/ResourceRequirement"}},"allocationPriority":{"type":"integer","default":0},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"minimumMinutes":{"type":"integer","nullable":true},"maximumMinutes":{"type":"integer","nullable":true},"requiresApproval":{"type":"boolean","default":false},"internalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"ResourceRequirement": {"type":"object","x-ticvai-persistence":"resources.resource_requirement","description":"**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n","required":["quantity"],"properties":{"id":{"type":"string","format":"uuid"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"},"quantity":{"type":"integer","default":1},"mandatory":{"type":"boolean","default":true},"requiredQualifications":{"type":"array","items":{"type":"string"}},"requiredAttributes":{"type":"object","additionalProperties":true},"substituteResourceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"},"packageId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The package this requirement is a component of** (4 October 2026, CHG-FXC-003). Written by `updateResourcePackage`, which replaces the package's `components` as these rows; `listResourcePackages` reads them back by it. Null for an experience's own requirement (`productId`)."},"productId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The experience product this requirement belongs to (`setExperienceResourceRequirements`). Exactly one of `packageId` and `productId` is set."}}},
"ResourceSelectionPolicy": {"type":"object","x-ticvai-persistence":"resources.selection_policy","description":"**Whether the guest may choose the resource, per ticket type**: the body of `setResourceSelectionPolicy` and its row, one per ticket type, replaced by each `PUT` (decided 29 September, data model DM4).\n","required":["ticketTypeId","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"ticketTypeId":{"type":"string","format":"uuid","description":"One policy per ticket type; a `PUT` for a ticket type that has one replaces it."},"mode":{"type":"string","enum":["autoAssign","guestMayChoose"]},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"showQualifications":{"type":"boolean","default":false},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `venue` scope."}}},
"ResourceUtilisation": {"type":"object","description":"Board 10.02. **Booked time over available time**, where available knows about schedules, blocks, setup and travel.\n","properties":{"key":{"type":"string"},"label":{"type":"string"},"availableMinutes":{"type":"integer"},"bookedMinutes":{"type":"integer"},"blockedMinutes":{"type":"integer"},"utilisationPercent":{"type":"number"},"bookingCount":{"type":"integer"}}}
}
```
