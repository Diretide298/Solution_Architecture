# WS79 — Game and Ride board 2

**10 screens · 10 operations · 10 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `DEVICE_CONFIGURE, DEVICE_VIEW, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-404` | Reader Management Dashboard | D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-405` | Reader Directory | D | 1 | 42 | 6 | 48 | 0 | 0 | — | notStarted (—) |
| `BO-406` | Reader Profile & Device Setup | D | 19 | 34 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-407` | Reader Credit & Payment Configuration | D | 4 | 28 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-408` | Reader / Attraction Assignment | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-409` | Retap Delay & Transaction Protection | D | 1 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-410` | Free Game Glow & Reader Display Rules | D | 6 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-411` | Reader Theme & Experience Configuration | D | 11 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-412` | Real-Time Tap Validation & Reader Response | D | 15 | 2 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-413` | Balance Check Reader & Device Test Console | D | 0 | 4 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-408, BO-409, BO-412, BO-413 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-404` Reader Management Dashboard

**Provide a centralized operational overview of all game and ride readers deployed across venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-404 |
| Who uses it | venue staff holding `DEVICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/reader-management-dashboard-bo-404` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The command centre for game and ride readers across the venue: KPI tiles, the Reader Status Overview (reader, type, attraction, zone, status, last tap), filters and the board's tiles. For the games technician and duty manager. The one thing to get right: a reader that is online but refusing an unusual share of taps is as much a fault as one that is offline, so Rejected taps sits beside the health tiles and opens the refusals by reader.

**Known correction pending (do not draw the wrong version)**

- **Tap KPIs (Transactions today, Successful taps, Rejected taps) have no bound read** Why: Only listReaders is bound; listGameplayTransactions (from today, by outcome) is needed. *(source: contracts/satellite/games.yaml#listGameplayTransactions / screens/P08-venue-back-office.yaml#BO-404; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The Reader Status Overview table and the five pack actions are not on the screen** Why: Pack p14 gives the table with sample rows and the action list. *(source: screens/P08-venue-back-office.yaml#BO-405; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Last tap and reader type are not on the Reader schema** Why: Last tap must come from transactions or the device heartbeat; reader type has no field anywhere. *(source: contracts/satellite/games.yaml#/components/schemas/Reader; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What rejected-tap rate should raise an alert on a reader?** → Drawn default accepted: Show the rate on each row and an alert above 15% in the last hour, labelled as a default threshold. *(decided by Chinmay, 2026-10-02; DEC-383 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search reader | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, zone, reader type, attraction type, status, assigned / unassigned — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **search / filters**: Search by reader ID, reader name or attraction. Filters Zone, Reader type, Attraction type, Status, Assigned / Unassigned (venue from the switcher, per VO-R09). Status is sent to listReaders. *(source: screens/P08-venue-back-office.yaml#BO-405 / contracts/satellite/games.yaml#listReaders)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Readers** (metric tile)

**Online Readers** (metric tile)

**Offline Readers** (metric tile)

**Readers with Errors** (metric tile)

**Unassigned Readers** (metric tile)

**Transactions Today** (metric tile)

**Successful Taps** (metric tile)

**Rejected Taps** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Eight metric tiles (per VO-R02). Total, Online (status active), Offline, With errors (disabled, unconfigured, or a health warning from the device register), Unassigned (no gameId). Transactions today, Successful taps (outcome allowed), Rejected taps (outcome refused) from today's gameplay transactions; Rejected taps shows the rate as well as the count. *(source: screens/P08-venue-back-office.yaml#BO-404 / contracts/satellite/games.yaml#/components/schemas/Reader / contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*
- **Reader Status Overview**: Reader, Type, Attraction, Zone, Status, Last tap (HH:MM venue time). Offline rows first; a reader whose last tap is far older than its neighbours' is flagged "No taps for 45 min". *(source: screens/P08-venue-back-office.yaml#BO-405)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add Reader / Configure / Test / Disable / View Transactions**: Add opens BO-405's add flow; Configure opens the reader editor (BO-406 onwards) for the row; Test opens BO-413 with the reader selected; Disable sets the reader status disabled with a confirmation naming the attraction that will stop accepting taps; View Transactions opens the transaction monitor filtered to the reader. *(source: screens/P08-venue-back-office.yaml#BO-405 / contracts/satellite/games.yaml#setReaderConfiguration)*

**Data it reads**: `listReaders` (onLoad, Readers and their health)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-405` Reader Directory: *Reader Directory*
- → `BO-406` Reader Profile & Device Setup: *Reader Profile & Device Setup*; carries `deviceId`
- → `BO-407` Reader Credit & Payment Configuration: *Reader Credit & Payment Configuration*
- → `BO-408` Reader / Attraction Assignment: *Reader / Attraction Assignment*
- → `BO-409` Retap Delay & Transaction Protection: *Retap Delay & Transaction Protection*
- → `BO-410` Free Game Glow & Reader Display Rules: *Free Game Glow & Reader Display Rules*
- → `BO-411` Reader Theme & Experience Configuration: *Reader Theme & Experience Configuration*
- → `BO-412` Real-Time Tap Validation & Reader Response: *Real-Time Tap Validation & Reader Response*
- → `BO-413` Balance Check Reader & Device Test Console: *Balance Check Reader & Device Test Console*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reader offline but deciding from its edge package**: Offline chip with "deciding offline, N taps waiting to sync" when the offline queue reports it; not counted as an error until the edge package expires. *(source: contracts/satellite/games.yaml#reportReaderQueue)*

#### Consistency with other screens

- Match `BO-394`: Active readers and Reader faults on the games dashboard equal Online and Readers with errors here.
- Match `BO-466`: Reader & Device Health Monitor (Board 8) shows the same statuses with the same chips.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  total: 48
  online: 45
  offline: 2
  withErrors: 3
  unassigned: 2
  transactionsToday: 3184
  successfulTaps: 3021
  rejectedTaps: 163 (5.1%)
rows:
- reader: R-001
  type: Ride reader
  attraction: Falcon Coaster
  zone: Thrill Zone
  status: Online
  lastTap: '10:42'
- reader: R-014
  type: Video game reader
  attraction: VR Racing 01
  zone: Arcade
  status: Online
  lastTap: '10:41'
- reader: R-023
  type: Skill game reader
  attraction: Basketball Pro 02
  zone: Sports Arcade
  status: Online
  lastTap: '10:40'
- reader: R-031
  type: Redemption game reader
  attraction: Prize Crane 04
  zone: Fun Zone
  status: Offline
  lastTap: '10:15'
```

#### Permissions

- `listReaders` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-404` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-404`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 1: Opens Reader Management Dashboard → Provide a centralized operational overview of all game and ride readers deployed across venues.
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F188 branch at step 1 (expected): when Nothing has been set up on Reader Management Dashboard yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F188 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-404?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-405`, `BO-406`, `BO-407`, `BO-408`, `BO-409`, `BO-410`, `BO-411`, `BO-412`, `BO-413`.
- [ ] Every gated control is gated: `DEVICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-405` Reader Directory

**Maintain the master inventory of physical readers connected to TICVAI. The source requires the ability to define a minimum of three reader types.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-405 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Directory Columns) and no metric row |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/reader-directory-bo-405` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The registry of physical game readers: identity (reader ID, name, type, serial), place (venue, zone, attraction), firmware, connection and configuration status, last communication. A reader is a device in the one device register (tenancy) with a game configuration on it, so this list joins the two. The one thing to get right: Clone configuration - forty identical readers on a row of machines are configured once, and a clone is never deployed by itself.

**Known correction pending (do not draw the wrong version)**

- **Table and detail titled "Every reader" / "The selected reader"; gap says no operation returns a described schema** Why: Generated placeholders (per VO-R12); listReaders returns Reader, and the device columns come from the device register, which must be read alongside. *(source: contracts/satellite/games.yaml#listReaders; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **registerDevice request lists id as required** Why: The operation says the server assigns the id and ignores it on input (per VO-R03). *(source: contracts/spine/tenancy.yaml#registerDevice; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Reader name, reader type, serial, firmware, zone and last communication are not on Reader (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where is reader type stored - a new field on Reader, or derived from the reader profile?** → Drawn default accepted: Draw it as a select on the reader and a column here; mark it pending a contract change. *(decided by Chinmay, 2026-10-02; DEC-384 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |
| Workstation | picker: choose a workstation | — | — | `listDevices` ?workstationId |
| Kind | select | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | `listDevices` ?kind |

**Sent by *Clone Configuration*** (`cloneReaderConfiguration`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target readers `targetReaderIds` | multi-picker: choose target readers | required | — | at least 1; at most 200; no duplicates | — | — | `cloneReaderConfiguration` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add Reader**: Registers the device in the one device register (kind rfidReader or nfcReader, driver, serial, model) and then creates its game configuration. A serial already registered in the tenant is refused. Status, health, firmware and heartbeat are reported by the device, never typed (per VO-R03). *(source: contracts/spine/tenancy.yaml#registerDevice / ADR-0067)*
- **Clone Configuration targets**: Multi-select of readers in the same venue; readers in another venue are not offered (the server refuses them). *(source: contracts/satellite/games.yaml#cloneReaderConfiguration)*

#### Outputs: what the screen shows and produces

**Shown**

**Every reader** (data table)

| Shows | Format | Notes |
|---|---|---|
| Reader ID | text | not in the schema: `Reader ID` |
| Reader name | text | not in the schema: `Reader Name` |
| Reader type | text | not in the schema: `Reader Type` |
| Serial number | text | not in the schema: `Serial Number` |
| Venue | text | not in the schema: `Venue` |
| Zone | text | not in the schema: `Zone` |
| Assigned attraction | text | not in the schema: `Assigned Attraction` |
| Firmware version | text | not in the schema: `Firmware Version` |
| Connection status | text | not in the schema: `Connection Status` |
| Configuration status | text | not in the schema: `Configuration Status` |
| Last communication | text | not in the schema: `Last Communication` |

**Devices** (data table, from `listDevices`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Driver | text | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change … |
| Identifier | text | — |
| Workstation | the name it points at, never the id | Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control … |
| Model | text | — |
| Hardware type | chip: Standard turnstile, Full height turnstile, Tripod turnstile, Speed gate, Wide lane … | The specific hardware under `kind` (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into … |
| Hardware model | the name it points at, never the id | The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it. |
| Serial number | text | The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). |
| Ip network reference | text | Network address or reference the device is reached at (ADR-0067). |
| Configuration version | text | Access configuration version the device reports running (ADR-0067). |
| Local rule version | text | Admission rule package the device reports running (ADR-0067). |
| Credential security package version | text | Credential security package the device reports running (ADR-0067). |
| Scanner health | text | Component health as the device or vendor reports it on its heartbeat (ADR-0067). |
| Controller health | text | — |
| Camera health | text | Where the device has a camera. |
| Connectivity | text | Reported connectivity. |
| Push token | text | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count … |
| Push platform | chip: Ios, Android, Web, Windows | — |

**The selected reader** (detail panel): The pack groups this record's detail under its own headings: “At minimum”, “Page 14 of 105”.

| Shows | Format | Notes |
|---|---|---|
| Reader ID | text | not in the schema: `Reader ID` |
| Reader name | text | not in the schema: `Reader Name` |
| Reader type | text | not in the schema: `Reader Type` |
| Serial number | text | not in the schema: `Serial Number` |
| Venue | text | not in the schema: `Venue` |
| Zone | text | not in the schema: `Zone` |
| Assigned attraction | text | not in the schema: `Assigned Attraction` |
| Firmware version | text | not in the schema: `Firmware Version` |
| Connection status | text | not in the schema: `Connection Status` |
| Configuration status | text | not in the schema: `Configuration Status` |
| Last communication | text | not in the schema: `Last Communication` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add Reader (primary button) | navigation or local | — | — | — | — |
| Edit (secondary button) | navigation or local | — | — | — | — |
| Clone Configuration (secondary button) | `cloneReaderConfiguration` POST `/readers/{readerId}/clone` | inline | Reader | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A target is the source reader, does not exist, or is in another venue. | — |
| Assign (secondary button) | navigation or local | — | — | — | — |
| Unassign (secondary button) | navigation or local | — | — | — | — |
| Disable (destructive button) | navigation or local | — | — | — | — |
| Search (secondary button) | navigation or local | — | — | — | — |
| Export (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Readers table**: The pack's eleven columns, titled "Readers" (not "Every reader", per VO-R12). Connection status from the device register (online, offline, error); Configuration status from the game reader status (unconfigured, active, maintenance, disabled) plus the deployment state (deployed, not deployed, failed). Last communication relative ("2 min ago") with the exact time on hover. *(source: screens/P08-venue-back-office.yaml#BO-405 / contracts/satellite/games.yaml#/components/schemas/Reader / contracts/satellite/games.yaml#/components/schemas/ReaderDeployment)*
- **Reader types**: At minimum Ride reader, Skill game reader, Video game reader; also Redemption game reader and Balance check reader. *(source: screens/P08-venue-back-office.yaml#BO-405 / screens/P08-venue-back-office.yaml#BO-406)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Clone Configuration**: Copies credit and payment settings, retap delay, display, theme and I/O mapping to each target; each keeps its own device and game. Result banner "Copied to 12 readers - not deployed. Deploy now?" with a link to deployment. *(source: contracts/satellite/games.yaml#cloneReaderConfiguration)*
- **Assign / Unassign**: Opens the shared assignment dialog (BO-408); Unassign confirms that the attraction will refuse taps. *(source: contracts/satellite/games.yaml#setReaderConfiguration)*
- **Disable**: Sets the game reader status disabled (reversible by Enable); confirmation names the attraction. Retiring the device itself is device lifecycle on the device register, not here. *(source: contracts/satellite/games.yaml#setReaderConfiguration / contracts/spine/tenancy.yaml#enrolDevice)*
- **Export**: Exports the filtered list with the filters used. *(source: screens/P08-venue-back-office.yaml#BO-406)*

**Data it reads**: `listReaders` (onLoad, The directory); `listDevices` (onLoad, The registered devices behind the readers: serial …)

**Where the user goes next**

- → `BO-404` Reader Management Dashboard: *Back to Reader Management Dashboard*

**What opens over it**

- confirmDialog *Disable*: **Disable on a reader is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 422 A target is the source reader, does not exist, or is in another venue.; 422 `workstationId` missing for a kind other than `mobileHandset`, or given for a `mobileHandset` (18.1.5). |

#### Edge cases to draw

- **Device registered but not enrolled**: Row shows "Registered - not enrolled" and Configure is disabled with the reason until enrolment completes. *(source: contracts/spine/tenancy.yaml#enrolDevice)*
- **Clone target in another venue**: Not selectable; if forced, 422 "R-112 is in Aqua Park; clone only within Summit Peaks". *(source: contracts/satellite/games.yaml#cloneReaderConfiguration)*

#### Consistency with other screens

- Match `BO-036`: Device register (tenancy) owns serial, model, firmware and enrolment (ADR-0067); this list reads them and links there, never edits them.
- Match `BO-404`: Same statuses and reader IDs.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- readerId: R-023
  name: Basketball Pro 02 reader
  type: Skill game reader
  serial: KPT-RF-220913-0023
  venue: Summit Peaks
  zone: Sports Arcade
  attraction: Basketball Pro 02
  firmware: 4.2.1
  connection: Online
  configuration: Active - deployed v14
  lastCommunication: 1 min ago
- readerId: R-031
  name: Prize Crane 04 reader
  type: Redemption game reader
  serial: KPT-RF-220913-0031
  venue: Summit Peaks
  zone: Fun Zone
  attraction: Prize Crane 04
  firmware: 4.1.9
  connection: Offline
  configuration: Active - deployed v13
  lastCommunication: 27 min ago
- readerId: R-040
  name: Arcade entrance balance reader
  type: Balance check reader
  venue: Summit Peaks
  zone: Arcade
  attraction: —
  firmware: 4.2.1
  connection: Online
  configuration: Active
```

#### Permissions

- `listReaders` → `DEVICE_VIEW` (read) · staff
- `registerDevice` → `DEVICE_CONFIGURE` (configure) · staff
- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff
- `cloneReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff
- `listDevices` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

48 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.14 | The system should be able to identify each ticketing kiosk individually by an ID, locate it geographically and administer it remotely. The kiosks should include a supervision interface and alert … | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.6 | It is expected that front gate sales can be performed by the operators using a POS having a touch screen. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.7 | The POS can be connected to a keyboard for which the function touches can be setup by the system administrator. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.8 | The POS can be connected to a cash drawer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.9 | The POS can be connected to a BOCA printer (it is expected to have the list of ticket printing hardware compatible) | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.10 | The POS can be connected to a ZEBRA printer or datamax printer or Evolis, for annual pass (it is expected to have the list of plastic card pass printing hardware compatible) | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.11 | The POS can be connected to a Receipt printer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.12 | The POS can be connected to a 2D scanner | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.13 | The POS can be connected to a RFID reader/writer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.14 | The POS can be connected to a Customer display including a double screen allowing the video display | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.15 | The POS can be connected to a camera | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.16 | The POS can be connected to a credit card machine | Ticketing Sales | CONTRACTED | `registerDevice` |
| … 36 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-405` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-405`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 2: Works in Reader Directory → Maintain the master inventory of physical readers connected to TICVAI. The source requires the ability to define a minimum of three reader types.
- ADR-0015 *Standards-First Device Drivers* (`docs/adr/0015-standards-first-device-drivers.md`)
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-405?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add Reader, Edit, Clone Configuration, Assign, Unassign, Disable, Search, Export.
- [ ] Every transition is wired: `BO-404`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-406` Reader Profile & Device Setup

**Configure the technical and operational identity of an individual reader.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-406 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Operational Settings) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `deviceId` (navigation), `readerId` (navigation) |
| Route | `/games-rides/reader-profile-device-setup-bo-406` |

**Known gaps.** **Reader Profile & Device Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … Removed 2 October 2026 (CHG-WIR-001): setReaderProfile writes the shared display and retry profile, not one reader's identity and location; the per-reader write is setReaderConfiguration, with the …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The technical identity of one reader - device information, location, connectivity and operational settings - with Save, Test connection, Synchronize, Restart and Disable. Device identity (manufacturer, model, serial, MAC, firmware, IP, heartbeat) belongs to the one device register and is read-only here; what this screen sets is where the reader is deployed and how it operates. The one thing to get right: make it obvious which values the device reports and which the operator sets.

**Known correction pending (do not draw the wrong version)**

- **Transaction enabled, Offline mode allowed, Logging enabled, terminal location and reader name have no contract field** Why: Reader carries status and game settings only; the pack's operational settings cannot be saved. *(source: screens/P08-venue-back-office.yaml#BO-406 / contracts/satellite/games.yaml#/components/schemas/Reader; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Operational settings drawn as select fields** Why: They are on/off switches. *(source: screens/P08-venue-back-office.yaml#BO-406; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The only bound operation is setReaderProfile, and the gap says the screen declares no write (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "Offline mode allowed" per reader, or only the venue-wide offlineDecisionAllowed rule?** → Drawn default accepted: Show the venue rule read-only with a per-reader switch greyed as pending. *(decided by Chinmay, 2026-10-02; DEC-385 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Enabled | select field | — | — | — | — | — | — |
| Transaction Enabled | select field | — | — | — | — | — | — |
| Offline Mode Allowed | select field | — | — | — | — | — | — |
| Logging Enabled | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |

**Form: Save reader** (modal, opened by *Save reader*; *Save reader* calls `setReaderConfiguration`, *Cancel* sends nothing)

**Collects what `setReaderConfiguration` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | `tenancy.RegisteredDevice`. Enrolment, firmware and tamper state live there. | `setReaderConfiguration` body |
| Game `gameId` | picker: choose a game | optional | — | — | shows names, sends the id | — | `setReaderConfiguration` body |
| Reader profile `readerProfileId` | picker: choose a reader profile | optional | — | — | shows names, sends the id | — | `setReaderConfiguration` body |
| Accepted credit types `acceptedCreditTypeIds` | multi-picker: choose accepted credit types | optional | — | — | — | — | `setReaderConfiguration` body |
| Accepts direct pay `acceptsDirectPay` | toggle | optional | off | — | — | — | `setReaderConfiguration` body |
| Retap delay seconds `retapDelaySeconds` | number field (seconds) | optional | 3 | — | — | The setting that stops a guest paying twice for one go. A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest. | `setReaderConfiguration` body |
| Display rules `displayRules` | group | optional | — | — | — | — | `setReaderConfiguration` body |
| Free game glow `displayRules.freeGameGlow` | toggle | optional | on | — | — | What tells a guest their entitlement was used rather than their money. Without it the complaint arrives at the desk. | `setReaderConfiguration` body |
| Show balance `displayRules.showBalance` | toggle | optional | on | — | — | — | `setReaderConfiguration` body |
| Show price `displayRules.showPrice` | toggle | optional | on | — | — | — | `setReaderConfiguration` body |
| Theme code `displayRules.themeCode` | text field | optional | — | — | — | — | `setReaderConfiguration` body |
| Languages `displayRules.languages` | list of values (chips) | optional | — | — | — | — | `setReaderConfiguration` body |
| Io mapping `ioMapping` | key and value settings | optional | — | — | — | Board 9.6. Which output starts the game, which input reports it finished. | `setReaderConfiguration` body |
| Status `status` | radio group | optional | — | Unconfigured · Active · Offline · Maintenance · Disabled | — | — | `setReaderConfiguration` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setReaderConfiguration` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **reader name, reader type**: Name with Arabic variant (shown on the reader display); type from the five reader types. *(source: screens/P08-venue-back-office.yaml#BO-406)*
- **location (client, venue, zone, attraction, terminal location)**: Client and venue come from the session and are shown, not chosen (per VO-R09); zone from the venue topology; attraction through the assignment dialog (BO-408); terminal location free text ("left of cabinet, 1.1 m"). *(source: screens/P08-venue-back-office.yaml#BO-406)*
- **operational settings**: Enabled, Transaction enabled, Offline mode allowed, Logging enabled as switches (the generator drew selects). Offline mode allowed shows the venue's offline maximum value from the validation rules. *(source: screens/P08-venue-back-office.yaml#BO-406 / contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Reader** (data table, from `listReaders`)

| Shows | Format | Notes |
|---|---|---|
| Device | the name it points at, never the id | `tenancy.RegisteredDevice`. Enrolment, firmware and tamper state live there. |
| Game | the name it points at, never the id | — |
| Reader profile | the name it points at, never the id | — |
| Accepted credit types | list or chips (count when long) | — |
| Accepts direct pay | yes / no (icon or chip) | — |
| Retap delay seconds | 1,234 | The setting that stops a guest paying twice for one go. A wristband held against a reader for a second and a half is two taps to the … |
| Display rules | grouped details | — |
| Free game glow | yes / no (icon or chip) | What tells a guest their entitlement was used rather than their money. Without it the complaint arrives at the desk. |
| Show balance | yes / no (icon or chip) | — |
| Show price | yes / no (icon or chip) | — |
| Theme code | text | — |
| Languages | list or chips (count when long) | — |
| Io mapping | grouped details | Board 9.6. Which output starts the game, which input reports it finished. |
| Status | chip: Unconfigured, Active, Offline, Maintenance, Disabled | — |

**Device** (detail panel, from `getDevice`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Driver | text | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change … |
| Identifier | text | — |
| Workstation | the name it points at, never the id | Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control … |
| Model | text | — |
| Hardware type | chip: Standard turnstile, Full height turnstile, Tripod turnstile, Speed gate, Wide lane … | The specific hardware under `kind` (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into … |
| Hardware model | the name it points at, never the id | The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it. |
| Serial number | text | The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). |
| Ip network reference | text | Network address or reference the device is reached at (ADR-0067). |
| Configuration version | text | Access configuration version the device reports running (ADR-0067). |
| Local rule version | text | Admission rule package the device reports running (ADR-0067). |
| Credential security package version | text | Credential security package the device reports running (ADR-0067). |
| Scanner health | text | Component health as the device or vendor reports it on its heartbeat (ADR-0067). |
| Controller health | text | — |
| Camera health | text | Where the device has a camera. |
| Connectivity | text | Reported connectivity. |
| Push token | text | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count … |
| Push platform | chip: Ios, Android, Web, Windows | — |
| Push failure count | 1,234 | Consecutive failures. A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save reader (secondary button) | `setReaderConfiguration` PUT `/readers/{readerId}` | Reader | Reader | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Device information (read-only)**: Manufacturer, model, serial, MAC / device identifier, firmware version as reported, with "Reported 10:40". *(source: screens/P08-venue-back-office.yaml#BO-406 / contracts/spine/tenancy.yaml#registerDevice / ADR-0067)*
- **Connectivity (read-only)**: Connection type, IP address, port, online/offline, last heartbeat, last synchronization (last acknowledged deployment and its version). *(source: screens/P08-venue-back-office.yaml#BO-406 / contracts/satellite/games.yaml#/components/schemas/ReaderDeployment)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves the reader's game configuration (whole row, per VO-R04). *(source: contracts/satellite/games.yaml#setReaderConfiguration)*
- **Test Connection**: Runs testReader and shows the connectivity check first. *(source: contracts/satellite/games.yaml#testReader)*
- **Synchronize**: Deploys the configuration and offline rule package; shows queued / sent / acknowledged / failed with the failure reason. *(source: contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Restart**: A device command through the vendor adaptor; disabled with "Not supported by this reader model" where the driver does not report the capability. *(source: contracts/spine/tenancy.yaml#registerDevice)*
- **Disable**: As BO-405 Disable. *(source: contracts/satellite/games.yaml#setReaderConfiguration)*

**Data it reads**: `listReaders` (onLoad, The reader being set up)

**Where the user goes next**

- → `BO-404` Reader Management Dashboard: *Back to Reader Management Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader profile device configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader profile device untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader profile device configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Synchronize fails**: Status failed with the reason; the reader keeps running its previous package until that package's expiry, shown as a date. *(source: contracts/satellite/games.yaml#/components/schemas/ReaderDeployment)*

#### Consistency with other screens

- Match `BO-036`: Device facts identical to the device register's 360 view; edit links go there.
- Match `BO-407`: BO-406, BO-407, BO-409, BO-410 and BO-411 all write the same Reader row; draw them as tabs of one reader editor (Device, Credit & payment, Retap, Display, Theme) with one Save (per VO-R14), board entries as anchors.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
device:
  readerId: R-023
  name: Basketball Pro 02 reader
  type: Skill game reader
  manufacturer: Kaptur
  model: KR-200 RFID
  serial: KPT-RF-220913-0023
  mac: 00:1B:44:11:3A:B7
  firmware: 4.2.1
location:
  client: Yas Leisure Group
  venue: Summit Peaks
  zone: Sports Arcade
  attraction: Basketball Pro 02
  terminal: Left of cabinet, 1.1 m
connectivity:
  type: Ethernet
  ip: 10.20.4.123
  port: 7001
  status: Online
  heartbeat: '10:40:12'
  lastSync: 01 Oct 2026 06:02 (v14)
settings:
  enabled: true
  transactionEnabled: true
  offlineModeAllowed: true
  loggingEnabled: true
```

#### Permissions

- `listReaders` → `DEVICE_VIEW` (read) · staff
- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff
- `getDevice` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-406` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-406`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 4: Works in Reader Profile & Device Setup → Configure the technical and operational identity of an individual reader.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-406?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save reader.
- [ ] Every transition is wired: `BO-404`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-407` Reader Credit & Payment Configuration

**Define exactly what type of wallet value a reader accepts and how much is required to start the game or ride. This directly implements requirement 10.2.6, which requires configurable: Credit type accepted Credit amount required Attraction type linked to the reader.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-407 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW`, `PRICE_VIEW`, `PRODUCT_VIEW` (1 configure, 3 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration; Configuration Source) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/reader-credit-payment-configuration-bo-407` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Enrolment belongs to the device register; this screen sets acceptance and price source and needs the reader, the effective price and the validation rules to show …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** What value a reader accepts and how much it takes to start the game (requirement 10.2.6 - credit type accepted, credit amount required, attraction type linked). For reader R-023 on Basketball Pro - which of paid wallet credit, bonus credit, free game credit, game entitlement and ride entitlement it accepts, the required price ("AED 20 / 20 credits"), the deduction priority it follows, and where the price comes from. The one thing to get right: Bonus is priority 1 among money sources (DI-865, 10.2.7), and the priority shown here is the venue rule from BO-426, not a second copy edited per reader.

**Known correction pending (do not draw the wrong version)**

- **setReaderConfiguration is bound with purpose "Profile and device setup"** Why: The binding purposes on BO-407 to BO-412 are shifted by one screen (BO-408 says "Credit and payment acceptance", BO-409 "Which attraction it opens", BO-410 "Retap delay", BO-411 "Free-game glow and display", BO-412 "Theme and experience"); each screen's purpose must be its own. *(source: screens/P08-venue-back-office.yaml#BO-407 / screens/P08-venue-back-office.yaml#BO-408 / screens/P08-venue-back-office.yaml#BO-412; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The reader is drawn as a text field labelled "Reader R-023 - Basketball Skill Game"** Why: A sample value used as a label; it is the editor's read-only header. *(source: screens/P08-venue-back-office.yaml#BO-407; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **acceptedCreditTypeIds holds wallet credit types, but entitlements are not credit types** Why: Game entitlement and Ride entitlement acceptance cannot be stored as credit-type ids; ReaderProfile.entitlementProductIds lists products, not an accept switch. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / contracts/satellite/games.yaml#/components/schemas/ReaderProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Configuration source (reader-specific / attraction price / pricing profile) has no contract field** Why: Reader has no price or price-source field; a reader-specific price cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-407 / contracts/satellite/games.yaml#/components/schemas/Reader; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): enrolDevice (device lifecycle) is bound on this screen (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a reader-specific price really wanted, given that pricing resolves by game and guest tier?** → Drawn default accepted: Draw Attraction price and Pricing profile; grey Reader-specific as pending. *(decided by Chinmay, 2026-10-02; DEC-386 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Reader: R-023 – Basketball Skill Game | text field | — | — | — | — | — | — |
| Reader-specific | select field | — | — | — | — | — | — |
| Attraction price | select field | — | — | — | — | — | — |
| Pricing profile | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |
| Game | picker: choose a game | — | — | `getGamePricing` ?gameId |
| Reader | picker: choose a reader | — | — | `getGamePricing` ?readerId |
| At | date and time picker | — | — | `getGamePricing` ?at |
| Guest tier | text field | — | — | `getGamePricing` ?guestTier |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **accepted value types**: A switch per value type - Paid wallet credit, Bonus credit, Free game credit, Game entitlement, Ride entitlement. A type the attraction or its type does not allow is disabled with the reason. Ride entitlement is offered only on ride readers. *(source: screens/P08-venue-back-office.yaml#BO-407 / contracts/satellite/games.yaml#/components/schemas/Reader)*
- **accepts direct pay**: Switch "Accept bank card tap directly", shown only where the attraction type has direct pay. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / contracts/satellite/games.yaml#/components/schemas/AttractionType)*
- **configuration source**: A single choice - Attraction price (default), Pricing profile, Reader-specific - where the generator drew three select fields. Reader-specific needs a reason; it overrides the pricing board for this reader only. *(source: screens/P08-venue-back-office.yaml#BO-407)*

#### Outputs: what the screen shows and produces

**Shown**

**Reader** (data table, from `listReaders`)

| Shows | Format | Notes |
|---|---|---|
| Device | the name it points at, never the id | `tenancy.RegisteredDevice`. Enrolment, firmware and tamper state live there. |
| Game | the name it points at, never the id | — |
| Reader profile | the name it points at, never the id | — |
| Accepted credit types | list or chips (count when long) | — |
| Accepts direct pay | yes / no (icon or chip) | — |
| Retap delay seconds | 1,234 | The setting that stops a guest paying twice for one go. A wristband held against a reader for a second and a half is two taps to the … |
| Display rules | grouped details | — |
| Free game glow | yes / no (icon or chip) | What tells a guest their entitlement was used rather than their money. Without it the complaint arrives at the desk. |
| Show balance | yes / no (icon or chip) | — |
| Show price | yes / no (icon or chip) | — |
| Theme code | text | — |
| Languages | list or chips (count when long) | — |
| Io mapping | grouped details | Board 9.6. Which output starts the game, which input reports it finished. |
| Status | chip: Unconfigured, Active, Offline, Maintenance, Disabled | — |

**Price in force** (detail panel, from `getGamePricing`)

| Shows | Format | Notes |
|---|---|---|
| Game | the name it points at, never the id | — |
| Effective price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied rule | text | — |
| Trace | list or chips (count when long) | — |
| Rule | text | — |
| Applied | yes / no (icon or chip) | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Skipped because | text | — |

**Validation rules** (detail panel, from `getGameplayValidationRules`)

| Shows | Format | Notes |
|---|---|---|
| Deduction order | list or chips (count when long) | — |
| Check order | list or chips (count when long) | — |
| Allow partial entitlement | yes / no (icon or chip) | Whether an entitlement covering part of the price may be topped up with credit. Usually no, because a guest who thinks they have a pass … |
| Refuse below balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Offline decision allowed | yes / no (icon or chip) | — |
| Offline maximum value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Required credit**: The effective price resolved for this reader now ("Standard play price AED 20.00 / 20 credits", applied rule, link to the pricing trace), read from getGamePricing with readerId. *(source: screens/P08-venue-back-office.yaml#BO-407 / contracts/satellite/games.yaml#getGamePricing)*
- **Deduction priority (read-only here)**: "1 Bonus credit, 2 Paid credit, 3 Free credit / entitlement as applicable" as the venue rule, with "Change on Deduction Priority (BO-426)". Value types switched off on this reader are struck out. *(source: screens/P08-venue-back-office.yaml#BO-407 / DI-865 / contracts/satellite/games.yaml#getGameplayValidationRules)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves the reader configuration (whole Reader row, per VO-R04), then offers Deploy, because a change not deployed has not happened. *(source: contracts/satellite/games.yaml#setReaderConfiguration / contracts/satellite/games.yaml#deployReaderConfiguration)*

**Data it reads**: `listReaders` (onLoad, The reader whose acceptance is set); `getGamePricing` (onLoad, The effective price at this reader, and why); `getGameplayValidationRules` (onLoad, What a tap is checked against)

**Where the user goes next**

- → `BO-404` Reader Management Dashboard: *Back to Reader Management Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader credit payment configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader credit payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader credit payment configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No value type accepted**: Save blocked with "This reader would refuse every tap - accept at least one value type". *(source: designer default)*
- **Reader accepts bonus but the bonus usage restriction excludes this attraction type**: Warn "BONUS25 cannot be used at Skill game readers (Bonus Usage Restrictions)"; the reader will show BONUS NOT ACCEPTED and fall back to the next source. *(source: screens/P08-venue-back-office.yaml#BO-420 / contracts/satellite/wallet.yaml#setCreditEligibilityRules)*

#### Consistency with other screens

- Match `BO-399`: Wallet & Credit Acceptance Mapping sets acceptance per attraction; this is the same choice per reader. Default the reader from its attraction and mark overrides.
- Match `BO-426`: Priority wording and order identical.
- Match `BO-435`: Required credit is the price from the pricing board; same money format.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reader: R-023 - Basketball Pro 02
accepted:
  paidWalletCredit: true
  bonusCredit: true
  freeGameCredit: true
  gameEntitlement: true
  rideEntitlement: — (not a ride)
requiredCredit: AED 20.00 / 20 credits (Standard price)
priority:
- 1 Bonus credit
- 2 Paid credit
- 3 Free credit / entitlement as applicable
configurationSource: Attraction price
```

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff
- `listReaders` → `DEVICE_VIEW` (read) · staff
- `getGamePricing` → `PRICE_VIEW` (read) · staff
- `getGameplayValidationRules` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-407` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-407`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 6: Works in Reader Credit & Payment Configuration → Define exactly what type of wallet value a reader accepts and how much is required to start the game or ride. This directly implements requirement 10.2.6, which requires configurable: Credit type …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-407?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-404`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`, `PRICE_VIEW`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-408` Reader / Attraction Assignment

**Assign a physical reader to the appropriate game, ride, or attraction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-408 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/reader-attraction-assignment-bo-408` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Assign a physical reader to a game or ride from the reader side, with an effective period and a compatibility check before save ("Ride reader cannot be assigned to this Video game under the selected configuration profile"). It edits the same reader-to-game link as BO-400. The one thing to get right: Validate shows the compatibility verdict before Assign is enabled.

**Known correction pending (do not draw the wrong version)**

- **Gap says the pack gives this screen nothing that can be drawn; only Save and Cancel are on it** Why: Pack p17 gives the nine-field assignment form, a valid and an invalid compatibility example and five actions. *(source: screens/P08-venue-back-office.yaml#BO-408; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Effective from / to has no contract field** Why: Reader.gameId is a single current value; scheduled or time-boxed assignments cannot be stored. *(source: contracts/satellite/games.yaml#/components/schemas/Reader; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Bound purpose "Credit and payment acceptance"** Why: Shifted binding purpose (see BO-407); here it is the reader-to-game assignment. *(source: screens/P08-venue-back-office.yaml#BO-408; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Button "Save reader configuration"** Why: Generated label; the pack's actions are Assign / Replace Reader / Unassign / Validate / Save. *(source: screens/P08-venue-back-office.yaml#BO-408; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are scheduled assignments (effective from in the future) needed at launch?** → Drawn default accepted: Draw From/To; From defaults to now and future dates are greyed as pending. *(decided by Chinmay, 2026-10-02; DEC-387 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **reader, attraction**: Reader pre-selected from navigation; Reader type, Venue and Zone shown from the reader, not re-entered. Attraction picker filtered to the reader's zone first, then all zones; Attraction type shown from the attraction. *(source: screens/P08-venue-back-office.yaml#BO-408)*
- **effective from / to**: Date-time in venue time; From defaults to now; To optional (open-ended). A future From schedules the change. *(source: screens/P08-venue-back-office.yaml#BO-408)*
- **status**: Assignment status Active / Scheduled / Ended is shown, not typed. *(source: screens/P08-venue-back-office.yaml#BO-408)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save reader configuration (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Compatibility panel**: Reader R-023, Skill game reader, to Basketball Pro, Skill game: "Valid" in green, or the refusal sentence in red naming the rule broken. *(source: screens/P08-venue-back-office.yaml#BO-408)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validate**: Runs the compatibility check without saving. *(source: screens/P08-venue-back-office.yaml#BO-408)*
- **Assign / Replace Reader / Save**: Writes gameId on the reader (setReaderConfiguration); Replace frees the previous reader. Then offers Deploy. *(source: contracts/satellite/games.yaml#setReaderConfiguration / contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Unassign**: Clears gameId; confirmation names the attraction that will refuse taps. *(source: contracts/satellite/games.yaml#setReaderConfiguration)*

**Where the user goes next**

- → `BO-404` Reader Management Dashboard: *Back to Reader Management Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader attraction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader attraction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader attraction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader attraction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reader disabled or offline**: Assigning an inactive reader is refused ("R-031 is disabled - enable it first"); offline is allowed with a warning that the change deploys when it reconnects. *(source: screens/P08-venue-back-office.yaml#BO-401 / contracts/satellite/games.yaml#deployReaderConfiguration)*

#### Consistency with other screens

- Match `BO-400`: One assignment dialog shared with Attraction / Reader Mapping (per VO-R14); same compatibility sentence.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
valid:
  reader: R-023
  readerType: Skill game reader
  venue: Summit Peaks
  zone: Sports Arcade
  attraction: Basketball Pro 02
  attractionType: Skill game
  from: 01 Oct 2026 12:00
  to: ''
  compatibility: Valid
invalid:
  reader: R-001
  readerType: Ride reader
  attraction: VR Racing 01
  attractionType: Video game
  compatibility: Ride reader cannot be assigned to this Video game under the selected configuration profile.
```

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-408` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-408`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 8: Works in Reader / Attraction Assignment → Assign a physical reader to the appropriate game, ride, or attraction.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-408?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save reader configuration, Cancel.
- [ ] Every transition is wired: `BO-404`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-409` Retap Delay & Transaction Protection

**Prevent accidental repeated deductions when a customer taps the card multiple times within a short period. The requirement explicitly states that a configurable delay—example 5 seconds—must exist between the first tap and subsequent taps.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-409 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/retap-delay-transaction-protection-bo-409` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Retap protection: a configurable delay after a tap during which further taps of the same card on the same reader are not charged again. The reader shows "PLEASE WAIT - Previous transaction already processed. Try again in 3 seconds." The one thing to get right: one guest intention is one charge - the delay and the message are visibly linked, with a preview counting down the configured seconds.

**Known correction pending (do not draw the wrong version)**

- **Two contract fields hold the same setting - Reader.retapDelaySeconds and ReaderProfile.rePlayWindowSeconds** Why: Both say a second tap inside the window is the same play; one must own it or the reader has two answers. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / contracts/satellite/games.yaml#/components/schemas/ReaderProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Apply to (paid / bonus / free / entitlement plays), On/Off and the reader message have no contract field** Why: Only retapDelaySeconds exists; Off can only be 0 seconds and the message cannot be configured. *(source: screens/P08-venue-back-office.yaml#BO-408 / contracts/satellite/games.yaml#/components/schemas/Reader; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Retap Protection drawn as a select labelled "Retap Protection ON/OFF"** Why: It is a switch; ON/OFF is the value set, not the label. *(source: screens/P08-venue-back-office.yaml#BO-408; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Bound purpose "Which attraction it opens"** Why: Shifted binding purpose (see BO-407). *(source: screens/P08-venue-back-office.yaml#BO-409; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The pack's example says 5 seconds, the contract default and the agreed message say 3 - which is the default?** → Drawn default accepted: 3 seconds, per DI-867 and the contract. *(decided by Chinmay, 2026-10-02; DEC-388 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Retap Protection: ON/OFF | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **retap protection on/off**: A switch (not the select the generator drew), default On. Turning it off needs a reason and warns "Guests may be charged twice for one go". *(source: screens/P08-venue-back-office.yaml#BO-408 / DI-867)*
- **delay duration**: Whole seconds, 1 to 60, default 3 (the contract default and the agreed message). The pack's 5 seconds is an example, not the default. *(source: screens/P08-venue-back-office.yaml#BO-408 / contracts/satellite/games.yaml#/components/schemas/Reader / DI-867)*
- **apply to**: Chips - All transactions (default), or any of Paid plays, Bonus plays, Free plays, Entitlement plays. *(source: screens/P08-venue-back-office.yaml#BO-408 / screens/P08-venue-back-office.yaml#BO-410)*
- **reader response during delay**: Message lines in English and Arabic with a {seconds} placeholder that counts down ("Try again in {seconds} seconds"); live preview on a reader mock-up. *(source: screens/P08-venue-back-office.yaml#BO-410 / DI-867)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save reader configuration (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Logging note**: States what is recorded for each blocked retap - first tap, blocked retap, reader, card / wallet reference, timestamp - and links to refusals with reason "Retap too soon" in the transaction monitor. *(source: screens/P08-venue-back-office.yaml#BO-410 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation)*
- **Scope banner**: Applies to: this reader, with "Copy to other readers" using Clone configuration. *(source: contracts/satellite/games.yaml#cloneReaderConfiguration)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves retapDelaySeconds on the reader (whole row, per VO-R04) and offers Deploy. *(source: contracts/satellite/games.yaml#setReaderConfiguration)*
- **Test retap**: Opens BO-413 with Test Retap selected. *(source: screens/P08-venue-back-office.yaml#BO-413)*

**Where the user goes next**

- → `BO-404` Reader Management Dashboard: *Back to Reader Management Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The retap delay transaction configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the retap delay transaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No retap delay transaction configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Delay longer than a short game's cycle**: Warn "Delay 10 s is longer than an 8 s game - a real second play would be refused". *(source: contracts/satellite/games.yaml#/components/schemas/GameOperationalConfig)*
- **Retap while the reader is offline**: The reader enforces the delay from its edge package; the blocked retap is journalled and syncs later. *(source: contracts/satellite/games.yaml#deployReaderConfiguration)*

#### Consistency with other screens

- Match `BO-412`: The "Retap too soon" response on the tap validation screen uses this message.
- Match `BO-440`: Retry pricing is the opposite intention (a deliberate second go at a lower price); its offer window starts after the retap delay. Show both values side by side on BO-440.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
config:
  protection: true
  delaySeconds: 3
  applyTo: All transactions
  messageEn: PLEASE WAIT - Previous transaction already processed. Try again in 3 seconds.
  messageAr: يرجى الانتظار - تمت معالجة العملية السابقة. حاول مرة أخرى بعد 3 ثوانٍ
log:
- at: '10:40:02'
  event: First tap
  reader: R-023
  card: '****4321'
- at: '10:40:03'
  event: Blocked retap
  reader: R-023
  card: '****4321'
```

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retap protection: a configurable delay stops a card being charged again while a game is in progress; the reader shows e.g. "please retry again in 3 seconds". *(agreed · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-867)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-409` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-409`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 10: Works in Retap Delay & Transaction Protection → Prevent accidental repeated deductions when a customer taps the card multiple times within a short period. The requirement explicitly states that a configurable delay—example 5 seconds—must exist …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-409?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save reader configuration, Cancel.
- [ ] Every transition is wired: `BO-404`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-410` Free Game Glow & Reader Display Rules

**Configure how the reader visually communicates that a game or ride is available free of charge. The source specifically requires free games to display a different color on the reader, allowing the customer to recognize that the game is free.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-410 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration; Display Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/free-game-glow-reader-display-rules-bo-410` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How the reader shows that a game is free for this guest - a distinct colour (free game glow), text, icon, animation and sound - and what triggers it (free game promotion, free game credit, package entitlement, unlimited pass, operator override). The one thing to get right: a side-by-side preview of the Normal state and the Free game state, because the guest reads a light, not a message.

**Known correction pending (do not draw the wrong version)**

- **Reader.displayRules holds only freeGameGlow true/false; colour, text, icon, animation, sound and triggers are not stored** Why: The per-outcome look lives on ReaderProfile.displayBehaviour (untyped strings) while this screen writes Reader; neither holds triggers. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / contracts/satellite/games.yaml#/components/schemas/ReaderProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Free Game Indicator: Enabled" drawn as a text field and the display items as select fields** Why: A switch plus pickers; the label carries a sample value. *(source: screens/P08-venue-back-office.yaml#BO-410; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Bound purpose "Retap delay"** Why: Shifted binding purpose (see BO-407). *(source: screens/P08-venue-back-office.yaml#BO-410; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the free-game look set per reader, per reader profile or per theme?** → Drawn default accepted: Per theme with a per-reader override, previewed here. *(decided by Chinmay, 2026-10-02; DEC-389 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Free Game Indicator: Enabled | text field | — | — | — | — | — | — |
| Free Game Glow | select field | — | — | — | — | — | — |
| Display Text | select field | — | — | — | — | — | — |
| Icon | select field | — | — | — | — | — | — |
| Animation | select field | — | — | — | — | — | — |
| Sound | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **free game indicator**: A switch, default On (contract default freeGameGlow true); the generator drew a text field with the value in its label. *(source: screens/P08-venue-back-office.yaml#BO-410 / contracts/satellite/games.yaml#/components/schemas/Reader)*
- **trigger**: Chips (multi-select) - Free game promotion, Free game credit, Package entitlement, Unlimited pass, Operator override. *(source: screens/P08-venue-back-office.yaml#BO-410)*
- **display configuration**: Glow colour (limited to colours the reader model supports), display text (English and Arabic, preset "FREE PLAY / TAP TO PLAY"), icon, animation, sound - each a picker from the reader model's capabilities; unsupported ones disabled with "Not supported by KR-200". *(source: screens/P08-venue-back-office.yaml#BO-410 / screens/P08-venue-back-office.yaml#BO-411 / DI-884)*
- **other outcome states**: The same controls for Accepted, Insufficient credit, Card blocked and Read error, because display behaviour is per outcome and insufficient credit also needs its own colour. *(source: contracts/satellite/games.yaml#/components/schemas/ReaderProfile)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Preview**: Two reader mock-ups side by side - NORMAL STATE ("AED 20 - TAP TO PLAY") and FREE GAME STATE ("FREE PLAY - TAP TO PLAY" in the glow colour), English and Arabic. *(source: screens/P08-venue-back-office.yaml#BO-410 / screens/P08-venue-back-office.yaml#BO-411)*
- **Hardware note**: "Exact LED behaviour depends on the reader hardware" under the preview. *(source: screens/P08-venue-back-office.yaml#BO-411)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves display rules (whole row, per VO-R04) and offers Deploy. *(source: contracts/satellite/games.yaml#setReaderConfiguration)*
- **Test display**: Runs testReader's display and sound checks on the physical reader. *(source: contracts/satellite/games.yaml#testReader)*

**Where the user goes next**

- → `BO-404` Reader Management Dashboard: *Back to Reader Management Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The free game glow configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the free game glow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No free game glow configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Glow colour the same as the refusal colour**: Blocked "Free game and Refused must look different". *(source: DI-868)*
- **Colour-blind guests**: The free state carries text and an icon as well as colour. *(source: designer default)*

#### Consistency with other screens

- Match `BO-411`: The theme's Free play state and this screen's free game state are one setting; the theme supplies the default and the reader may override it.
- Match `BO-428`: The reader result "FREE PLAY - Included in your pass" on the unlimited entitlement screen is this state.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
config:
  indicator: true
  triggers:
  - Free game credit
  - Package entitlement
  - Unlimited pass
  glow: 'Green #00C389'
  text: FREE PLAY / TAP TO PLAY
  textAr: لعب مجاني / انقر للعب
  icon: star
  animation: pulse
  sound: chime-free
states:
  accepted: blue
  freeGame: green
  insufficientCredit: amber
  cardBlocked: red
  readError: white flash
```

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Free-game display: a distinct reader colour/theme for free games so guests recognise them immediately; reader response configuration defines what the reader shows after a validated tap. *(client request · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-868)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-410` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-410`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 12: Works in Free Game Glow & Reader Display Rules → Configure how the reader visually communicates that a game or ride is available free of charge. The source specifically requires free games to display a different color on the reader, allowing the …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-410?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-404`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-411` Reader Theme & Experience Configuration

**Configure different visual experiences for reader categories. The source requires custom themes controlled from BOS, with skill games and rides able to have different reader themes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-411 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Theme Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/reader-theme-experience-configuration-bo-411` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** A library of reader themes by category (Ride, Skill game, Video game, Redemption) controlled from the back office: background, logo, screen layout, icons, messages, animation, sound and the Success, Failure and Free play states, with a live reader preview, publish and assignment to reader types. The one thing to get right: the preview and the assignment count ("Skill Game Theme - 42 Skill game readers"), because publishing a theme changes every machine in a category.

**Known correction pending (do not draw the wrong version)**

- **No operation creates, edits or publishes a reader theme; setReaderConfiguration only stores a themeCode string** Why: The theme library, its assets and states have no contract; white-label setTheme is the guest-app brand theme, not a reader theme. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / contracts/satellite/white-label.yaml#setTheme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Eleven theme properties drawn as select fields** Why: Name is text; background, logo and icons are uploads; layout a thumbnail choice; states are grouped colour-text-sound sets. *(source: screens/P08-venue-back-office.yaml#BO-411; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Bound purpose "Free-game glow and display"** Why: Shifted binding purpose (see BO-407). *(source: screens/P08-venue-back-office.yaml#BO-411; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are reader themes per venue or tenant-wide (one Skill Game Theme for every park)?** → Drawn default accepted: Tenant-wide library, assigned per venue. *(decided by Chinmay, 2026-10-02; DEC-390 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Theme Name | select field | — | — | — | — | — | — |
| Background | select field | — | — | — | — | — | — |
| Logo | select field | — | — | — | — | — | — |
| Reader Screen Layout | select field | — | — | — | — | — | — |
| Icons | select field | — | — | — | — | — | — |
| Display Messages | select field | — | — | — | — | — | — |
| Animation | select field | — | — | — | — | — | — |
| Sound Profile | select field | — | — | — | — | — | — |
| Success State | select field | — | — | — | — | — | — |
| Failure State | select field | — | — | — | — | — | — |
| Free Play State | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **theme name**: Text with Arabic variant, unique in the venue. *(source: screens/P08-venue-back-office.yaml#BO-411)*
- **background, logo, icons**: Uploads at the reader's resolution; the tenant's brand logo by default with "Powered by TICVAI" on guest-facing readers. *(source: screens/P08-venue-back-office.yaml#BO-411)*
- **reader screen layout**: A choice among layouts the reader model supports, shown as thumbnails. *(source: screens/P08-venue-back-office.yaml#BO-411)*
- **display messages and Success / Failure / Free play states**: Per-state message (English and Arabic), colour and sound; failure messages use the same plain reasons as tap validation (Insufficient balance, Game not included, Retap too soon). *(source: screens/P08-venue-back-office.yaml#BO-411 / screens/P08-venue-back-office.yaml#BO-412)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Theme library**: Cards per theme with a thumbnail, category, status (Draft / Published) and "Assigned to 42 readers". *(source: screens/P08-venue-back-office.yaml#BO-411)*
- **Preview**: Reader mock-up switching between Idle, Success, Failure and Free play, in English and in Arabic (right-to-left). *(source: screens/P08-venue-back-office.yaml#BO-411)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Create Theme / Edit / Preview**: Draft themes are editable without touching readers. *(source: screens/P08-venue-back-office.yaml#BO-411)*
- **Publish**: Confirmation names the readers that will change and that they get it on the next deployment. *(source: screens/P08-venue-back-office.yaml#BO-411 / contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Assign**: Assigns a theme to a reader type (all readers of that type) or to selected readers; per reader this writes displayRules.themeCode. *(source: contracts/satellite/games.yaml#/components/schemas/Reader)*

**Where the user goes next**

- → `BO-404` Reader Management Dashboard: *Back to Reader Management Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader theme experience configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader theme experience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader theme experience configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Theme assigned to a reader model that cannot show animation or sound**: The preview marks the parts that model will drop. *(source: DI-884)*

#### Consistency with other screens

- Match `BO-410`: Free play state shared with the free game glow screen.
- Match `BO-480`: Reader screen, LED and sound output mapping (Board 9) is the hardware side of the same outputs.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
themes:
- name: Skill Game Theme
  category: Skill game
  status: Published
  readers: 42
  background: Summit Peaks arcade purple
  success: blue
  failure: red
  freePlay: green
- name: Ride Theme
  category: Ride
  status: Published
  readers: 14
- name: National Day 2026
  category: All
  status: Draft
  readers: 0
```

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Free-game display: a distinct reader colour/theme for free games so guests recognise them immediately; reader response configuration defines what the reader shows after a validated tap. *(client request · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-868)*
- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-411` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-411`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 14: Works in Reader Theme & Experience Configuration → Configure different visual experiences for reader categories. The source requires custom themes controlled from BOS, with skill games and rides able to have different reader themes.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-411?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-404`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-412` Real-Time Tap Validation & Reader Response

**Define and visualize what occurs when a customer taps their card/device before gameplay. This screen directly addresses requirement 10.2.13: the system must validate the customer's credit/card balance, bonus and entitlements in real time before the game starts.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-412 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify Card / Wallet) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/real-time-tap-validation-reader-response-bo-412` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): Per-outcome responses (what the reader shows and does) live on ReaderProfile.displayBehaviour, written by setReaderProfile; the screen was bound to the …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Explains and configures what happens when a guest taps - Customer tap, Identify card / wallet, Check entitlement, Check bonus, Check paid balance, Apply pricing, Authorize / Reject, Deduct value, Start game - and what the reader shows on success ("PLAY AUTHORIZED - Game price AED 20 - Bonus used AED 10 - Wallet used AED 10 - Remaining AED 85"), for an entitlement ("INCLUDED IN YOUR PASS - Remaining plays 2") and for each rejection. The one thing to get right: each rejection reason is a plain guest message and a configured reader response, never "Declined".

**Known correction pending (do not draw the wrong version)**

- **The pack's rejections and the contract's reason enum differ** Why: Invalid card, Wallet blocked and Reader offline map to cardNotFound, cardBlocked or nothing; Entitlement expired and Game not included are not distinct reasons, so the reader cannot say which. *(source: screens/P08-venue-back-office.yaml#BO-412 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **ReaderProfile.displayBehaviour has five outcomes only (accepted, freeGame, insufficientCredit, cardBlocked, readError)** Why: Not enough for the pack's eight rejections and two successes. *(source: contracts/satellite/games.yaml#/components/schemas/ReaderProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The screen is a data table "Every real-time tap validation" with no read, and a write bound as setReaderConfiguration with purpose "Theme … (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the success response show the money split (bonus used, wallet used) or only the remaining balance?** → Drawn default accepted: Show the split, as in the pack. *(decided by Chinmay, 2026-10-02; DEC-391 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Form: Save reader responses** (modal, opened by *Save reader responses*; *Save reader responses* calls `setReaderProfile`, *Cancel* sends nothing)

**Collects what `setReaderProfile` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setReaderProfile` body |
| Name `name` | text field | required | — | — | — | — | `setReaderProfile` body |
| Display behaviour `displayBehaviour` | group | optional | — | — | — | What the reader shows, per outcome. Colour and tone, because the guest is looking at a machine rather than a screen. | `setReaderProfile` body |
| Accepted `displayBehaviour.accepted` | text field | optional | — | — | — | — | `setReaderProfile` body |
| Free game `displayBehaviour.freeGame` | text field | optional | — | — | — | — | `setReaderProfile` body |
| Insufficient credit `displayBehaviour.insufficientCredit` | text field | optional | — | — | — | — | `setReaderProfile` body |
| Card blocked `displayBehaviour.cardBlocked` | text field | optional | — | — | — | — | `setReaderProfile` body |
| Read error `displayBehaviour.readError` | text field | optional | — | — | — | — | `setReaderProfile` body |
| Retry pricing `retryPricing` | group | optional | — | — | — | A retry after a machine fault is not a second play. Without this a guest whose game crashed pays twice, and the attendant refunds by hand — which is how an arcade loses money and … | `setReaderProfile` body |
| Is free `retryPricing.isFree` | toggle | optional | on | — | — | — | `setReaderProfile` body |
| Within seconds `retryPricing.withinSeconds` | number field (seconds) | optional | 60 | — | — | — | `setReaderProfile` body |
| Max retries `retryPricing.maxRetries` | number field | optional | 1 | — | — | — | `setReaderProfile` body |
| Re play window seconds `rePlayWindowSeconds` | number field (seconds) | optional | — | — | — | A second tap within this window is the same play, not a new one. A guest tapping twice because nothing appeared to happen should not be charged twice. | `setReaderProfile` body |
| Entitlement products `entitlementProductIds` | multi-picker: choose entitlement products | optional | — | — | — | Per-game entitlement. A pass that includes ten specific rides needs the reader to know which, and a card that works everywhere is a different product. | `setReaderProfile` body |
| Scope path `scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `setReaderProfile` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **reader response per outcome**: For each of the pack's eight rejections (Insufficient balance, Invalid card, Expired card, Entitlement not valid, Game not included, Retap too soon, Reader offline, Wallet blocked) and the two successes - the guest message (English and Arabic) and the display state. Defaults are the contract's guest messages ("No plays left on your pass" rather than "Declined"). *(source: screens/P08-venue-back-office.yaml#BO-412 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation / DI-868)*

#### Outputs: what the screen shows and produces

**Shown**

**Every real-time tap validation** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**The selected real-time tap validation** (detail panel): The pack groups this record's detail under its own headings: “Customer Tap”, “Check Entitlement”, “Check Bonus”, “Check Paid Balance”, “Apply Pricing”, “Authorize / Reject”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save reader responses (secondary button) | `setReaderProfile` PUT `/reader-profiles` | ReaderProfile | ReaderProfile | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validation flow**: A step diagram of the nine steps (right-to-left in Arabic); each step links to the screen that configures it (entitlements BO-427 to BO-431, deduction priority BO-426, pricing BO-434, retap BO-409). *(source: screens/P08-venue-back-office.yaml#BO-412)*
- **Response previews**: Reader mock-ups for PLAY AUTHORIZED (with the money split), INCLUDED IN YOUR PASS (remaining plays) and each rejection. *(source: screens/P08-venue-back-office.yaml#BO-412)*
- **Recent taps on this reader**: Optional strip of the latest taps on the selected reader with outcome and reason, cursor-paged (per VO-R12). *(source: contracts/satellite/games.yaml#listGameplayTransactions)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save responses**: Saves the per-outcome messages and states on the reader profile (every reader using it) and offers Deploy. *(source: contracts/satellite/games.yaml#setReaderProfile / contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Simulate a tap**: Opens BO-433 with this reader selected. *(source: contracts/satellite/games.yaml#simulateGameplayAuthorisation)*

**Where the user goes next**

- → `BO-404` Reader Management Dashboard: *Back to Reader Management Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The real-time tap validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the real-time tap validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No real-time tap validation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the real-time tap validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reader offline**: The platform cannot refuse "Reader offline"; it is what the reader shows when it cannot decide (edge package expired). Draw it as the reader's own state. *(source: contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Entitlement covers only part of the price**: Refused, not topped up from credit, unless partial entitlement is allowed on BO-425. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*

#### Consistency with other screens

- Match `BO-432`: The authorisation trace on BO-432 uses the same nine step names.
- Match `BO-424`: Rejection labels identical to the command centre's rejection breakdown.
- Match `BO-409`: The Retap too soon message comes from BO-409.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
authorized:
  title: PLAY AUTHORIZED
  gamePrice: AED 20.00
  bonusUsed: AED 10.00
  walletUsed: AED 10.00
  remaining: AED 85.00
entitlement:
  title: INCLUDED IN YOUR PASS
  remainingPlays: 2
rejections:
- reason: Insufficient balance
  guestMessage: Not enough credit - top up at any kiosk
  guestMessageAr: الرصيد غير كافٍ - اشحن من أي كشك
- reason: Game not included
  guestMessage: This game is not in your pass
- reason: Retap too soon
  guestMessage: Please wait - try again in 3 seconds
```

#### Permissions

- `setReaderProfile` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Free-game display: a distinct reader colour/theme for free games so guests recognise them immediately; reader response configuration defines what the reader shows after a validated tap. *(client request · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-868)*
- Retap protection: a configurable delay stops a card being charged again while a game is in progress; the reader shows e.g. "please retry again in 3 seconds". *(agreed · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-867)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-412` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-412`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 16: Works in Real-Time Tap Validation & Reader Response → Define and visualize what occurs when a customer taps their card/device before gameplay. This screen directly addresses requirement 10.2.13: the system must validate the customer's credit/card …

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-412?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save reader responses.
- [ ] Every transition is wired: `BO-404`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-413` Balance Check Reader & Device Test Console

**Configure dedicated balance-check readers and provide administrators with a test environment for deployed reader configurations. Requirement 10.2.20 specifically requires a reader through which the customer can check their balance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-413 |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/balance-check-reader-device-test-console-bo-413` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Two jobs on one screen: configure dedicated balance-check readers (what a guest sees on tap - paid credit, bonus, free games, entitlements, bonus expiry, card expiry - without starting a game), and an administrator's test console that runs test taps against a deployed reader configuration and shows the validation result, deduction source, price, remaining balance, reader response and response time. The one thing to get right: a test never charges a real guest - it runs on a test card or a simulated balance and is labelled TEST everywhere.

**Known correction pending (do not draw the wrong version)**

- **testReader takes no request body** Why: The pack's console selects a test card, attraction, simulated balance, entitlement and seven test types; testReader runs hardware checks only, so the logic tests need simulateGameplayAuthorisation, which is not bound here. *(source: contracts/satellite/games.yaml#testReader / contracts/satellite/games.yaml#simulateGameplayAuthorisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Nothing marks a reader as a balance-check reader or stores which balance items it shows** Why: Reader and ReaderProfile have no function or display-items field, so requirement 10.2.20 cannot be configured. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / DI-869; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **simulateGameplayAuthorisation cannot take a simulated balance or entitlement** Why: Its request carries readerId, cardId, credentialIdentifier, gameId, at, guestHeightCm and offline only. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisationRequest; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table labelled "Every balance check reader" with columns Validation result and Deduction source** Why: Those are test-result fields, not reader columns; placeholder label (per VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-413; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How are test cards created and kept out of revenue reports?** → Drawn default accepted: Draw a "Test cards" list with a TEST badge; issuing them is pending. *(decided by Chinmay, 2026-10-02; DEC-392 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **reader function**: Balance check or Gameplay for the selected reader; DI-869 allows the gameplay reader itself to show the balance too. *(source: screens/P08-venue-back-office.yaml#BO-413 / DI-869)*
- **customer display items**: Ticks for the pack's six items, in order; Valid until in the region's date format (31 Mar 2027). *(source: screens/P08-venue-back-office.yaml#BO-413)*
- **test console selection**: Reader, Test card / wallet (test cards only), Attraction, Simulated balance (paid and bonus amounts), Entitlement. Simulated balance and entitlement are optional overrides of the test card's values. *(source: screens/P08-venue-back-office.yaml#BO-413)*

#### Outputs: what the screen shows and produces

**Shown**

**Every balance check reader** (data table)

| Shows | Format | Notes |
|---|---|---|
| Validation result | text | not in the schema: `Validation result` |
| Deduction source | text | not in the schema: `Deduction source` |

**The selected balance check reader** (detail panel): The pack groups this record's detail under its own headings: “Upon tap, display”, “YOUR BALANCE”, “Test Actions”, “Page 21 of 105”, “Requirement coverage”, “Page 22 of 105”.

| Shows | Format | Notes |
|---|---|---|
| Validation result | text | not in the schema: `Validation result` |
| Deduction source | text | not in the schema: `Deduction source` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Balance preview**: YOUR BALANCE - Paid credit AED 125.00 - Bonus credit AED 25.00 - Free games 2 - Valid until 31 Mar 2027, in English and Arabic. *(source: screens/P08-venue-back-office.yaml#BO-413)*
- **Test result**: Validation result, deduction source, price, remaining balance, reader response (as the reader would show it), response time in ms against the one-second target; plus the hardware checks (connectivity, card read, balance check, display, sound, game trigger, game complete) each pass or fail with detail and an overall pass / partial / fail. *(source: screens/P08-venue-back-office.yaml#BO-413 / contracts/satellite/games.yaml#/components/schemas/ReaderTestResult / contracts/satellite/games.yaml#authoriseGameplay)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test Tap / Test Paid Play / Test Bonus / Test Entitlement / Test Free Play / Test Retap / Test Rejection**: Logic tests run simulateGameplayAuthorisation for the reader and test card (nothing is charged); hardware tests run testReader on the device. Each result is appended to a session log with its time. *(source: screens/P08-venue-back-office.yaml#BO-413 / contracts/satellite/games.yaml#simulateGameplayAuthorisation / contracts/satellite/games.yaml#testReader)*

**Where the user goes next**

- → `BO-404` Reader Management Dashboard: *Back to Reader Management Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The balance check reader list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the balance check reader untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No balance check reader yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the balance check reader are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reader offline during a hardware test**: Connectivity fails first and the other checks show "Not run". *(source: contracts/satellite/games.yaml#/components/schemas/ReaderTestResult)*
- **Someone picks a real guest card**: Not possible; the picker lists test cards only. *(source: designer default)*

#### Consistency with other screens

- Match `BO-433`: The logic test is the same simulation and decision trace as the Validation Simulator; share the result component.
- Match `BO-490`: The kiosk's "What can I play?" and the balance reader show the same balance items in the same order.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
balance:
  paidCredit: AED 125.00
  bonusCredit: AED 25.00
  freeGames: 2
  entitlements: Arcade Adventure - 1 play left
  bonusExpiry: 30 Oct 2026
  cardExpiry: 31 Mar 2027
test:
  reader: R-023
  card: TEST-001
  attraction: Basketball Pro 02
  simulatedBalance: Paid AED 50.00, Bonus AED 8.00
  action: Test paid play
  result: Authorized
  deductionSource: AED 8.00 bonus + AED 12.00 paid
  price: AED 20.00
  remaining: AED 38.00
  responseMs: 412
```

#### Permissions

- `testReader` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A balance-check reader (the gameplay reader or a dedicated one) lets a guest tap to see their current balance without playing. *(client request · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-869)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-413` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS59 Game and Ride Board 2.dc.html#bo-413`
- Workshop pack: Game_and_Ride_Module.pdf board 2
- Flow F188 *Game and Ride board 2: Reader Management Dashboard*, step 18: Works in Balance Check Reader & Device Test Console → Configure dedicated balance-check readers and provide administrators with a test environment for deployed reader configurations. Requirement 10.2.20 specifically requires a reader through which the …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-413?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-404`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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
"cloneReaderConfiguration": {"method":"POST","path":"/readers/{readerId}/clone","contract":"games","summary":"Copy one reader's configuration onto other readers","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Reader"},
"getDevice": {"method":"GET","path":"/devices/{deviceId}","contract":"tenancy","summary":"Read one registered device","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RegisteredDevice"},
"getGamePricing": {"method":"GET","path":"/game-pricing","contract":"games","summary":"The effective price at a reader, and why","permission":"PRICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"gameId","in":"query","required":true},{"name":"readerId","in":"query","required":null},{"name":"at","in":"query","required":null},{"name":"guestTier","in":"query","required":null}],"requestBody":null,"responds":"GamePriceResolution"},
"getGameplayValidationRules": {"method":"GET","path":"/gameplay-validation-rules","contract":"games","summary":"What a tap is checked against, and in what order","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameplayValidationRules"},
"listDevices": {"method":"GET","path":"/devices","contract":"tenancy","summary":"List registered devices","permission":"DEVICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReaders": {"method":"GET","path":"/readers","contract":"games","summary":"Readers, their attractions and their health","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Reader"},
"registerDevice": {"method":"POST","path":"/devices","contract":"tenancy","summary":"Register a device","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegisteredDevice","responds":"RegisteredDevice"},
"setReaderConfiguration": {"method":"PUT","path":"/readers/{readerId}","contract":"games","summary":"What this reader charges, opens, shows and refuses","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Reader","responds":"Reader"},
"setReaderProfile": {"method":"PUT","path":"/reader-profiles","contract":"games","summary":"How a reader behaves and what it shows","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReaderProfile","responds":"ReaderProfile"},
"testReader": {"method":"POST","path":"/readers/{readerId}/test","contract":"games","summary":"Prove a reader works before a guest finds out it does not","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReaderTestResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"DeviceApprovalStatus": {"type":"string","description":"Whether a registered device may go into production (DEC-241, DEC-245; CHG-CSP-011). The model is `states/registered-device-approval.yaml`.\n","enum":["pendingApproval","approved","rejected"]},
"DeviceCapability": {"type":"string","description":"BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n","enum":["genderClassification","dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},
"DeviceKind": {"type":"string","enum":["receiptPrinter","ticketPrinter","labelPrinter","cashDrawer","barcodeScanner","rfidReader","nfcReader","cardReader","idReader","biometricReader","accessReader","paymentTerminal","customerDisplay","signageDisplay","kitchenDisplay","turnstileController","wristbandEncoder","signaturePad","scale","camera","mobileHandset","handheldScanner","accessPodium","bleBeacon"],"description":"`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"},
"GamePriceResolution": {"type":"object","description":"Board 5.9. **What will this actually charge.**","properties":{"gameId":{"type":"string","format":"uuid"},"effectivePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedRule":{"type":"string"},"trace":{"type":"array","items":{"type":"object","properties":{"rule":{"type":"string"},"applied":{"type":"boolean"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"skippedBecause":{"type":"string","nullable":true}}}}}},
"GameplayValidationRules": {"type":"object","x-ticvai-persistence":"games.validation_rules","description":"Boards 4.2 and 4.3. **Must be an answer, stated once**, rather than whatever the firmware happens to do.\n","properties":{"deductionOrder":{"type":"array","items":{"type":"string","enum":["entitlement","freePlay","bonusCredit","promotionalCredit","gameCredit","cashCredit","directPay"]}},"checkOrder":{"type":"array","items":{"type":"string","enum":["cardValid","cardNotExpired","cardNotBlocked","restrictionsMet","retapWindow","entitlementAvailable","fundsSufficient"]}},"allowPartialEntitlement":{"type":"boolean","default":false,"description":"**Whether an entitlement covering part of the price may be topped up with credit.** Usually no, because a guest who thinks they have a pass does not expect a charge.\n"},"refuseBelowBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"offlineDecisionAllowed":{"type":"boolean","default":true},"offlineMaximumValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Reader": {"type":"object","x-ticvai-persistence":"games.reader","description":"Board 2. **A `tenancy` device with a game configuration on it.**","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"`tenancy.RegisteredDevice`. **Enrolment, firmware and tamper state live there.**\n"},"gameId":{"type":"string","format":"uuid","nullable":true},"readerProfileId":{"type":"string","format":"uuid","nullable":true},"acceptedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"acceptsDirectPay":{"type":"boolean","default":false},"retapDelaySeconds":{"type":"integer","default":3,"description":"**The setting that stops a guest paying twice for one go.** A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest.\n"},"displayRules":{"type":"object","properties":{"freeGameGlow":{"type":"boolean","default":true,"description":"**What tells a guest their entitlement was used rather than their money.** Without it the complaint arrives at the desk.\n"},"showBalance":{"type":"boolean","default":true},"showPrice":{"type":"boolean","default":true},"themeCode":{"type":"string","nullable":true},"languages":{"type":"array","items":{"type":"string"}}}},"ioMapping":{"type":"object","additionalProperties":true,"description":"Board 9.6. Which output starts the game, which input reports it finished. **Deliberately open.** The keys are the reader model's own I/O lines, so the shape belongs to the vendor adaptor for that model (game readers are a driver, not a build — ADR-0012, ADR-0015), not to this contract.\n"},"status":{"type":"string","enum":["unconfigured","active","offline","maintenance","disabled"]},"scopePath":{"type":"string"}}},
"ReaderProfile": {"type":"object","x-ticvai-persistence":"games.reader_profile","description":"BL-153. **`games` is well built on the money and what is missing sits at the reader.**\n10.2.14 and 10.2.17 want a different colour for a free game and a different one for insufficient credit — **because a guest at an arcade machine cannot read a message, they can only see a light.** The whole interaction is a second long and happens across a noisy room.\n","required":["id","name"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"displayBehaviour":{"type":"object","description":"**What the reader shows, per outcome.** Colour and tone, because the guest is looking at a machine rather than a screen.\n","properties":{"accepted":{"type":"string"},"freeGame":{"type":"string"},"insufficientCredit":{"type":"string"},"cardBlocked":{"type":"string"},"readError":{"type":"string"}}},"retryPricing":{"type":"object","nullable":true,"description":"**A retry after a machine fault is not a second play.** Without this a guest whose game crashed pays twice, and the attendant refunds by hand — which is how an arcade loses money and goodwill at once.\n","properties":{"isFree":{"type":"boolean","default":true},"withinSeconds":{"type":"integer","default":60},"maxRetries":{"type":"integer","default":1}}},"rePlayWindowSeconds":{"type":"integer","nullable":true,"description":"**A second tap within this window is the same play, not a new one.** A guest tapping twice because nothing appeared to happen should not be charged twice.\n"},"entitlementProductIds":{"type":"array","description":"**Per-game entitlement.** A pass that includes ten specific rides needs the reader to know which, and a card that works everywhere is a different product.\n","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ReaderTestResult": {"type":"object","description":"Boards 2.10 and 9.9. **Each check separately**, because they send an engineer to different places.\n","properties":{"readerId":{"type":"string","format":"uuid"},"testedAt":{"type":"string","format":"date-time"},"checks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["connectivity","cardRead","balanceCheck","display","sound","gameTrigger","gameCompleteSignal"]},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"overall":{"type":"string","enum":["pass","partial","fail"]}}},
"RegisteredDevice": {"x-ticvai-persistence":"platform.device","type":"object","description":"**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n","required":["id","kind","driver"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"},"identifier":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"},"model":{"type":"string","nullable":true},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType","nullable":true,"description":"**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"},"hardwareModelId":{"type":"string","format":"uuid","nullable":true,"description":"The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"},"serialNumber":{"type":"string","nullable":true,"maxLength":100,"description":"The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"},"ipNetworkReference":{"type":"string","nullable":true,"description":"Network address or reference the device is reached at (ADR-0067)."},"configurationVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Access configuration version the device reports running (ADR-0067)."},"localRuleVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Admission rule package the device reports running (ADR-0067)."},"credentialSecurityPackageVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Credential security package the device reports running (ADR-0067)."},"scannerHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Component health as the device or vendor reports it on its heartbeat (ADR-0067)."},"controllerHealth":{"type":"string","nullable":true,"readOnly":true},"cameraHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Where the device has a camera."},"connectivity":{"type":"string","nullable":true,"readOnly":true,"description":"Reported connectivity."},"pushToken":{"type":"string","format":"password","nullable":true,"writeOnly":true,"description":"BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"},"pushPlatform":{"type":"string","nullable":true,"enum":["ios","android","web","windows"]},"pushFailureCount":{"type":"integer","default":0,"readOnly":true,"description":"**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"},"offlineScope":{"type":"string","nullable":true,"enum":["none","readOnly","sellAndScan","fullVenue"],"description":"BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"},"firmwareVersion":{"type":"string","nullable":true,"readOnly":true,"description":"As the device last reported it on its heartbeat."},"isRequired":{"type":"boolean","description":"True blocks shift open when the device is unreachable."},"status":{"type":"string","readOnly":true,"enum":["online","offline","error","consumableLow","needsAttention","localMode","unknown"],"description":"What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"},"batteryPercent":{"type":"integer","nullable":true,"readOnly":true,"minimum":0,"maximum":100,"description":"Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"},"health":{"type":"string","enum":["healthy","warning","degraded","offline","unknown"],"default":"unknown","readOnly":true,"description":"**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"capabilities":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/DeviceCapability"},"description":"BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"},"enrolmentState":{"type":"string","enum":["registered","enrolled","provisioned","active","deactivated","retired"],"default":"registered","readOnly":true,"description":"BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"},"retiredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"},"approvalStatus":{"allOf":[{"$ref":"#/components/schemas/DeviceApprovalStatus"}],"default":"pendingApproval","readOnly":true,"description":"**A new device waits for approval before it may go live** (decided 2 October 2026, Chinmay, critical set 1, BO-196: \"Secure enrolment code + pending approval\"; DEC-241; CHG-CSP-011; MoM 15 September, DI-892, DI-906). Every device registers `pendingApproval`. It may enrol and be provisioned and tested, but `enrolDevice` refuses `active` until `approveDevice` approves it (`409 device-approval-required`). A separate axis from `enrolmentState`, which keeps its r1 values; the model is `states/registered-device-approval.yaml`.\n"},"enrolmentCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":12,"description":"**A one-time code the device must present to enrol** (DEC-241; CHG-CSP-011). Issued by `registerDevice` and returned once, in its response only; every later read returns null. The installer enters it on the device, and `enrolDevice` to `enrolled` must carry the same code before `enrolmentCodeExpiresAt` (`422 enrolment-code-invalid`). A device that never presents it never gets an identity, so a box plugged into the venue network cannot claim to be a reader.\n"},"enrolmentCodeExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the enrolment code stops working (24 hours after registration, proposed; client to correct)."},"testedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who recorded the device's acceptance test (`DeviceEnrolment.testResult` on the move to `provisioned`). The approver must be someone else (DEC-245).\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who approved the device into production, never the person who tested it** (decided 2 October 2026, Chinmay, critical set 1, BO-203: \"Approver must differ from the tester\"; DEC-245; CHG-CSP-011). `approveDevice` refuses the tester with `403 approver-is-tester`.\n"},"approvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}
}
```
