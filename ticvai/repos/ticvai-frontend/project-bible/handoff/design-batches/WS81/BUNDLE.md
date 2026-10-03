# WS81 — Game and Ride board 4

**10 screens · 6 operations · 5 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-424` | Gameplay Validation Command Center | D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-425` | Gameplay Validation Rule Configuration | D | 0 | 6 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-426` | Deduction Priority & Funding Source Rules | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-427` | All Games & Rides Pass Configuration | D | 11 | 15 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-428` | Specific Game/Ride Unlimited Entitlement | D | 9 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-429` | Specific Game/Ride Limited Entitlement | D | 1 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-430` | Game Package Builder | D | 0 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-431` | Entitlement Validity & Activation Rules | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-432` | Real-Time Gameplay Authorization | B | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-433` | Validation Simulator & Exception Analysis | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-425, BO-426, BO-429, BO-430, BO-431, BO-432, BO-433 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-424` Gameplay Validation Command Center

**Provide an operational overview of gameplay authorization across all games and rides.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-424 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/gameplay-validation-command-center-bo-424` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The gameplay validation command centre: KPI tiles for today's gameplay requests and how they were decided (authorized, rejected, entitlement, paid, bonus, free plays, validation errors), a live validation feed, a rejection breakdown, and tiles to the board's nine screens. The one thing to get right: abnormal rejection patterns jump out - a reader or a reason that suddenly refuses many taps - because each guest who is refused just walks away and nobody reports it.

**Known correction pending (do not draw the wrong version)**

- **GameplayTransaction.reason is a free string, while GameplayAuthorisation.reason is an enum** Why: The rejection breakdown groups by reason; the transaction must carry the same enum or the bars cannot be counted. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Reasons "Entitlement expired" and "Game not included" have no enum value** Why: The enum has entitlementExhausted and entitlementNotValidHere only. *(source: screens/P08-venue-back-office.yaml#BO-425 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The live feed and rejection breakdown are missing; only tiles and a filter are on the screen** Why: Pack p34 gives the feed columns with four sample rows and the seven-reason breakdown. *(source: screens/P08-venue-back-office.yaml#BO-425; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listGameplayTransactions has no attraction or zone filter and no cursor** Why: The pack filters by zone and attraction; the read takes from, readerId and outcome only. *(source: contracts/satellite/games.yaml#listGameplayTransactions; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which refusal reasons count as "Validation errors" (configuration faults) rather than ordinary rejections?** → Drawn default accepted: readerNotConfigured and gameUnavailable. *(decided by Chinmay, 2026-10-02; DEC-394 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search gameplay validation | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, zone, attraction, validation type, result, date/time — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **filters**: Zone, Attraction, Validation type (Entitlement, Paid, Bonus, Free), Result (Authorized, Rejected, Reversed), Date/time range (default today); venue from the switcher. Result and from-time are sent to listGameplayTransactions. *(source: screens/P08-venue-back-office.yaml#BO-425 / contracts/satellite/games.yaml#listGameplayTransactions)*

#### Outputs: what the screen shows and produces

**Shown**

**Gameplay Requests Today** (metric tile)

**Authorized Plays** (metric tile)

**Rejected Plays** (metric tile)

**Entitlement Plays** (metric tile)

**Paid Plays** (metric tile)

**Bonus Plays** (metric tile)

**Free Plays** (metric tile)

**Validation Errors** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Eight metric tiles (per VO-R02) from today's transactions - requests (all), authorized (allowed), rejected (refused), and authorized split by chargedFrom into entitlement, paid, bonus and free plays; validation errors = refusals for configuration reasons (reader not configured, game unavailable). *(source: screens/P08-venue-back-office.yaml#BO-424 / contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*
- **Live validation feed**: Time, guest card masked to last four (****4321), attraction, validation (AED 20 / All Games Pass / 1 play), source (Bonus / Entitlement / Package / Wallet), result. Newest on top, cursor-paged (per VO-R12); rows decided offline carry an "offline" mark and their sync time. *(source: screens/P08-venue-back-office.yaml#BO-425 / contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*
- **Rejection breakdown**: A bar per reason - Insufficient balance, Entitlement invalid, Game not included, Entitlement expired, Usage limit reached, Card expired, Retap protection - with count and share; clicking filters the feed. *(source: screens/P08-venue-back-office.yaml#BO-425)*
- **Rules in force**: A small card with the current deduction order and check order from the validation rules, linking to BO-425 / BO-426. *(source: contracts/satellite/games.yaml#getGameplayValidationRules)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open a feed row**: Opens the decision trace for that transaction on BO-432. *(source: screens/P08-venue-back-office.yaml#BO-432)*
- **Tiles to BO-425 to BO-433**: Each opens its screen and returns here (per VO-R13). *(source: DI-653)*

**Data it reads**: `getGameplayValidationRules` (onLoad, Rules in force); `listGameplayTransactions` (onLoad, What they produced)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-425` Gameplay Validation Rule Configuration: *Gameplay Validation Rule Configuration*
- → `BO-426` Deduction Priority & Funding Source Rules: *Deduction Priority & Funding Source Rules*
- → `BO-427` All Games & Rides Pass Configuration: *All Games & Rides Pass Configuration*
- → `BO-428` Specific Game/Ride Unlimited Entitlement: *Specific Game/Ride Unlimited Entitlement*
- → `BO-429` Specific Game/Ride Limited Entitlement: *Specific Game/Ride Limited Entitlement*
- → `BO-430` Game Package Builder: *Game Package Builder*
- → `BO-431` Entitlement Validity & Activation Rules: *Entitlement Validity & Activation Rules*
- → `BO-432` Real-Time Gameplay Authorization: *Real-Time Gameplay Authorization*
- → `BO-433` Validation Simulator & Exception Analysis: *Validation Simulator & Exception Analysis*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gameplay validation list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gameplay validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gameplay validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gameplay validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Rejections spike on one reader**: An alert "R-023 refused 38% of taps in the last hour (Game not included)" with a link to the simulator for that reader; any AI explanation is a suggestion (per VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-433 / contracts/satellite/games.yaml#listGameplayTransactions)*
- **Offline decisions not yet synced**: KPI tiles say "plus N decisions waiting to sync from 2 readers". *(source: contracts/satellite/games.yaml#getGameplaySyncStatus)*

#### Consistency with other screens

- Match `BO-394`: Gameplay requests today equals Transactions today on the games dashboard.
- Match `BO-412`: Rejection reason labels identical.
- Match `BO-468`: Rejected Transaction & Reason Analysis (Board 8) is the deep version of this breakdown; same reasons and colours.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  requests: 3184
  authorized: 3021
  rejected: 163
  entitlementPlays: 1240
  paidPlays: 1102
  bonusPlays: 512
  freePlays: 167
  validationErrors: 9
feed:
- time: '10:42'
  card: '****4321'
  attraction: VR Racing 01
  validation: AED 20.00
  fundingSource: Bonus
  result: Authorized
- time: '10:41'
  card: '****7621'
  attraction: Falcon Coaster
  validation: All Games Pass
  fundingSource: Entitlement
  result: Authorized
- time: '10:40'
  card: '****9902'
  attraction: Basketball Pro 02
  validation: 1 play
  fundingSource: Package
  result: Authorized
- time: '10:39'
  card: '****1128'
  attraction: Bumper Cars
  validation: AED 15.00
  fundingSource: Wallet
  result: Rejected - Insufficient balance
```

#### Permissions

- `getGameplayValidationRules` → `PRODUCT_VIEW` (read) · staff
- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-424` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-424`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 1: Opens Gameplay Validation Command Center → Provide an operational overview of gameplay authorization across all games and rides.
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F190 branch at step 1 (expected): when Nothing has been set up on Gameplay Validation Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F190 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-424?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-425`, `BO-426`, `BO-427`, `BO-428`, `BO-429`, `BO-430`, `BO-431`, `BO-432`, `BO-433`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-425` Gameplay Validation Rule Configuration

**Configure the checks TICVAI performs before allowing a game or ride to start. The source requires validation before game start against balance, bonus and applicable entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-425 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/gameplay-validation-rule-configuration-bo-425` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The checks TICVAI runs before a game or ride starts and their order: Credential (exists, active, not expired), Attraction (game active, reader valid, attraction included), Entitlement (exists, active, within validity, usage remaining), Value (bonus, paid balance, required price) - then determine the payment source and authorize or reject. The one thing to get right: the sequence is visible as one ordered list the venue can test before activating, with rule-level on/off only where turning a check off is safe.

**Known correction pending (do not draw the wrong version)**

- **Gap says the pack gives this screen nothing that can be drawn; only Save and Cancel are on it** Why: Pack p34-p35 list thirteen checks in four groups, the nine-step rule sequence and five actions. *(source: screens/P08-venue-back-office.yaml#BO-425 / screens/P08-venue-back-office.yaml#BO-426; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Pack checks "Reader valid", "Attraction included", "Entitlement active", "Within validity" have no distinct check in checkOrder** Why: The contract folds them into entitlementAvailable and restrictionsMet; the screen can group them but cannot order them separately. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No draft / activate state on the rules** Why: The pack's Save then Activate needs a draft; the PUT is live on save. *(source: screens/P08-venue-back-office.yaml#BO-426 / contracts/satellite/games.yaml#setGameplayValidationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): setGameplayValidationRules is bound without its read (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are validation rules venue-wide only, or can they differ by attraction type?** → Drawn default accepted: Venue-wide, as the contract has it. *(decided by Chinmay, 2026-10-02; DEC-395 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **check order**: Drag-to-reorder list of the contract's checks (Card valid, Card not expired, Card not blocked, Restrictions met - height and age, Retap window, Entitlement available, Funds sufficient), grouped under the pack's four headings. Credential checks are locked first; Funds sufficient is locked last. *(source: screens/P08-venue-back-office.yaml#BO-425 / screens/P08-venue-back-office.yaml#BO-426 / contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*
- **allow partial entitlement**: Switch, default Off, with the help "If on, an entitlement that covers part of the price is topped up from credit - a pass holder may be charged". *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*
- **refuse below balance**: Money (AED), optional - refuse a tap when the wallet would fall below this. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*
- **offline decisions**: Switch "Readers may decide offline" (default On) and "Offline maximum value" in AED, shown only when on. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Validation rules** (detail panel, from `getGameplayValidationRules`)

| Shows | Format | Notes |
|---|---|---|
| Deduction order | list or chips (count when long) | — |
| Check order | list or chips (count when long) | — |
| Allow partial entitlement | yes / no (icon or chip) | Whether an entitlement covering part of the price may be topped up with credit. Usually no, because a guest who thinks they have a pass … |
| Refuse below balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Offline decision allowed | yes / no (icon or chip) | — |
| Offline maximum value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rule sequence**: The pack's flow Tap - Validate credential - Validate attraction - Find entitlement - Check usage / validity - Check bonus - Check paid balance - Determine payment source - Authorize / Reject, drawn from the saved check order so it always matches what the engine runs. *(source: screens/P08-venue-back-office.yaml#BO-426)*
- **Last changed**: Last changed by and when (per VO-R05). *(source: contracts/spine/access.yaml#/info / DI-629)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save / Activate**: Save sends the whole rule set (PUT, per VO-R04) together with the deduction order from BO-426 - they are one record; draw both screens as one "Validation rules" editor with two tabs. Activate makes it live at the next reader deployment and says so. *(source: contracts/satellite/games.yaml#setGameplayValidationRules)*
- **Test Rule**: Opens the in-screen simulator (BO-433 component) against the draft, before Activate (per VO-R05). *(source: screens/P08-venue-back-office.yaml#BO-426)*

**Data it reads**: `getGameplayValidationRules` (onLoad, The rules in force, to edit)

**Where the user goes next**

- → `BO-424` Gameplay Validation Command Center: *Back to Gameplay Validation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gameplay validation rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gameplay validation rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gameplay validation rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gameplay validation rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Offline decisions allowed with no maximum value**: Warn "Readers offline could authorise any amount"; suggest a maximum. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*
- **Retap window placed after Funds sufficient**: Blocked - a retap must be caught before money is checked, or a second tap could be charged. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules / DI-867)*

#### Consistency with other screens

- Match `BO-426`: Same record (GameplayValidationRules); one Save across both tabs.
- Match `BO-412`: The nine-step tap flow on Board 2 is this sequence drawn for the reader.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
checkOrder:
- Card valid
- Card not expired
- Card not blocked
- Retap window
- Restrictions met
- Entitlement available
- Funds sufficient
allowPartialEntitlement: false
refuseBelowBalance: AED 0.00
offline:
  allowed: true
  maximumValue: AED 50.00
```

#### Permissions

- `setGameplayValidationRules` → `PRODUCT_CONFIGURE` (configure) · staff
- `getGameplayValidationRules` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-425` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-425`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 2: Works in Gameplay Validation Rule Configuration → Configure the checks TICVAI performs before allowing a game or ride to start. The source requires validation before game start against balance, bonus and applicable entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-425?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-424`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-426` Deduction Priority & Funding Source Rules

**Determine which wallet/value source TICVAI consumes when more than one valid funding source is available. Requirement 10.2.7 explicitly states: “Bonus deduction should be done first.”**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-426 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/deduction-priority-funding-source-rules-bo-426` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Which value TICVAI consumes when more than one is valid. The pack locks Bonus credit as Priority 1 ("Bonus deduction should be done first", 10.2.7; DI-865 bonus, then prepaid, then others), with drag-to-reorder, enable/disable per source, scope by attraction, attraction type or product, and split deduction (AED 8 bonus + AED 12 paid for an AED 20 game). The one thing to get right: entitlements are a right to play, decided before any money is touched; the priority list orders the money sources, and the screen must show both so nobody is charged on a pass.

**Known correction pending (do not draw the wrong version)**

- **The pack's own priority table puts Package/Entitlement 4th, after money, while its tap flows check entitlement first** Why: Pack p35 lists Bonus 1, Paid 2, Free 3, Entitlement 4; pack p20 and p40 check entitlement before bonus, and the contract says an entitlement is consumed before money. Read "Bonus first" as first among money sources. *(source: screens/P08-venue-back-office.yaml#BO-426 / screens/P08-venue-back-office.yaml#BO-412 / screens/P08-venue-back-office.yaml#BO-432 / contracts/satellite/games.yaml#listGameEntitlements; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The wallet's consumption policy defaults to expiringFirst** Why: DI-865 agreed bonus first, then prepaid; wallet's default would spend whichever expires first and can contradict this screen at the same tap. *(source: contracts/satellite/wallet.yaml#/components/schemas/CreditConsumptionPolicy / DI-865; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Apply by attraction / attraction type / product has no contract field** Why: deductionOrder is one venue-wide list. *(source: screens/P08-venue-back-office.yaml#BO-426 / contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Split deduction has no field in the games rules** Why: Only wallet's allowSplitTender and games' allowPartialEntitlement exist; neither is "several money sources for one play". *(source: contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules / contracts/satellite/wallet.yaml#/components/schemas/CreditConsumptionPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Bound without getGameplayValidationRules; only Save and Cancel on the screen** Why: The PUT needs the read (per VO-R04), and the pack gives the priority table, five controls and the split example. *(source: screens/P08-venue-back-office.yaml#BO-426 / contracts/satellite/games.yaml#getGameplayValidationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **When the wallet policy (BO-1107) and this game deduction order disagree, which applies at a game reader?** → Drawn default accepted: This screen at game readers; show the wallet policy read-only with that statement. *(decided by Chinmay, 2026-10-02; DEC-396 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **priority list**: Two bands. Top band, locked and labelled "Play rights - checked first": Package / entitlement, Free game credit. Money band, drag to reorder: 1 Bonus credit (default first), 2 Paid wallet credit, then promotional and other game credits, Direct pay last. Each row has an Enabled switch. *(source: screens/P08-venue-back-office.yaml#BO-426 / screens/P08-venue-back-office.yaml#BO-412 / DI-865 / contracts/satellite/games.yaml#/components/schemas/GameplayValidationRules)*
- **apply by**: Venue default, with exceptions by attraction, attraction type or product / package listed beneath; an exception shows which rows differ from the default. *(source: screens/P08-venue-back-office.yaml#BO-426)*
- **split deduction**: Switch "Allow multiple value sources for one transaction", default On, with the worked example recalculating live. *(source: screens/P08-venue-back-office.yaml#BO-427 / contracts/satellite/wallet.yaml#/components/schemas/CreditConsumptionPolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Worked example**: Game price AED 20.00 - Bonus available AED 8.00 - Paid wallet AED 50.00 - Result AED 8.00 Bonus + AED 12.00 Paid credit; recalculated from the current order and split setting. *(source: screens/P08-venue-back-office.yaml#BO-427)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves deductionOrder as part of the one validation rule set (whole record, per VO-R04); one Save shared with BO-425. *(source: contracts/satellite/games.yaml#setGameplayValidationRules)*
- **Test**: Runs the simulator on a sample card with the draft order. *(source: contracts/satellite/games.yaml#simulateGameplayAuthorisation)*

**Where the user goes next**

- → `BO-424` Gameplay Validation Command Center: *Back to Gameplay Validation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deduction priority funding list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deduction priority funding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deduction priority funding yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deduction priority funding are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Someone drags Paid credit above Bonus**: Allowed only with a reason and a warning "The contract requirement is bonus first (10.2.7)"; shown as an exception in the audit. *(source: screens/P08-venue-back-office.yaml#BO-433 / DI-865)*
- **Bonus not allowed at this attraction type (bonus usage restriction)**: Bonus is skipped and the next source used; the example shows "Bonus not accepted here". *(source: screens/P08-venue-back-office.yaml#BO-420)*

#### Consistency with other screens

- Match `BO-1107`: The wallet's Consumption Priority Engine orders credit types for all spending; this screen orders game value at the reader. State on both which wins at a game reader (this one).
- Match `BO-407`: The reader screen shows this order read-only.
- Match `BO-399`: Wallet & Credit Acceptance Mapping's Priority column is this order per attraction.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
playRights:
- Package / entitlement
- Free game credit
money:
- priority: 1
  fundingSource: Bonus credit
  enabled: true
- priority: 2
  fundingSource: Paid wallet credit
  enabled: true
- priority: 3
  fundingSource: Promotional credit
  enabled: true
- priority: 4
  fundingSource: Direct pay
  enabled: false
split:
  allowed: true
  example: AED 8.00 Bonus + AED 12.00 Paid credit
```

#### Permissions

- `setGameplayValidationRules` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per game: which credit types are accepted (cash/wallet, bonus, redemption) and a configurable consumption priority (bonus first, then prepaid/cash, then others). *(agreed · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-865)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-426` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-426`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 4: Works in Deduction Priority & Funding Source Rules → Determine which wallet/value source TICVAI consumes when more than one valid funding source is available. Requirement 10.2.7 explicitly states: “Bonus deduction should be done first.”

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-426?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-424`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-427` All Games & Rides Pass Configuration

**Configure a ticket/product that permits the guest to play all games/rides in the amusement park. This directly represents requirement 10.2.8.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-427 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Pass Setup; Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/all-games-rides-pass-configuration-bo-427` |

**What the spec says about it.** **An all-games pass covers games added after sale unless the venue says not; type-based passes cover new games by default (decided 2 October 2026 by Chinmay, DEC-397; CHG-CSA-028, `includesGamesAddedLater`).**

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No get, update or deactivate operation for a game entitlement.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** An all games and rides pass (requirement 10.2.8): one product that lets the guest play every applicable attraction without paid-wallet deductions - included attraction types, excluded attractions, unlimited or a limited total of plays, validity and activation. The reader shows "INCLUDED IN YOUR PASS - TAP ACCEPTED". The one thing to get right: it must look different from BO-428 and BO-429 (pack p42) - this one is "everything except", the others are "only these".

**Known correction pending (do not draw the wrong version)**

- **Every field drawn as a select, including Pass name, Valid from / until and Unlimited / Limited total plays as two separate selects** Why: Name is text, dates are pickers, and the access model is one choice with a conditional count. *(source: screens/P08-venue-back-office.yaml#BO-427; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Excluded attractions has no contract field** Why: GameEntitlement has gameIds and attractionTypeIds (inclusion only); "all rides except premium cranes" cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-427 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Valid from / until dates have no field** Why: Only validityKind and validityDays exist. *(source: contracts/satellite/games.yaml#/components/schemas/GameEntitlement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Only createGameEntitlement exists for passes - no read of one, no update, no deactivate (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does an all games pass cover attractions added after it was sold?** → Whether an all-games pass covers games added after sale: the venue configures it; default yes (type-based passes cover new games). *(decided by Chinmay, 2026-10-02; DEC-397 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Pass Name | select field | — | — | — | — | — | — |
| Product Code | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Valid From | select field | — | — | — | — | — | — |
| Valid Until | select field | — | — | — | — | — | — |
| Activation Method | select field | — | — | — | — | — | — |
| Included Attraction Types | select field | — | — | — | — | — | — |
| Excluded Attractions | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Unlimited | select field | — | — | — | — | — | — |
| Limited Total Plays | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **pass name / product code / venue**: Name with Arabic variant; product code is the catalogue product it is sold as (picker), not a free text; venue from the switcher. *(source: screens/P08-venue-back-office.yaml#BO-427 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*
- **included attraction types**: Chips (Rides, Video games, Skill games, Redemption games); at least one. *(source: screens/P08-venue-back-office.yaml#BO-427)*
- **excluded attractions**: Multi-select of individual attractions within the included types ("Premium Crane Games"). *(source: screens/P08-venue-back-office.yaml#BO-427)*
- **access model**: Unlimited (default) or Limited total plays with a count; Unlimited offers daily cap and cooldown ("Unlimited does not mean continuous"). *(source: screens/P08-venue-back-office.yaml#BO-427 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*
- **validity and activation**: As BO-431 (the shared validity block); default activation On first use. *(source: contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*

#### Outputs: what the screen shows and produces

**Shown**

**Passes** (data table, from `listGameEntitlements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Kind | chip: All games pass, Unlimited single game, Limited single game, Package, Free play | — |
| Games | list or chips (count when long) | — |
| Attraction types | list or chips (count when long) | — |
| Includes games added later | yes / no (icon or chip) | Whether a pass sold today covers a game added tomorrow (Chinmay, 2 October, workbook Q397: "venue configures; default yes"; CHG-CSA-028). |
| Play count | 1,234 | For `limitedSingleGame` and `package`. Null means unlimited. |
| Validity kind | chip: Same day, Days, Until date, Until used | — |
| Validity days | 1,234 | — |
| Activation kind | chip: On purchase, On first use, On date | On first use is what a guest expects from a day pass bought the night before. On purchase is what a venue defaults to by accident, and it … |
| Daily play cap | 1,234 | — |
| Cooldown minutes | 1,234 | Unlimited does not mean continuous. A cooldown is how one child does not hold a popular ride all afternoon. |
| Linked product | the name it points at, never the id | — |
| Is active | yes / no (icon or chip) | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Coverage summary**: "Covers 31 of 34 attractions - excludes Prize Crane 04, Prize Crane 05, Mega Claw" recalculated live. *(source: screens/P08-venue-back-office.yaml#BO-427)*
- **Reader preview**: INCLUDED IN YOUR PASS / TAP ACCEPTED in the free play state. *(source: screens/P08-venue-back-office.yaml#BO-428)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Creates the entitlement (kind allGamesPass). Editing an existing pass needs an update operation the contract lacks. *(source: contracts/satellite/games.yaml#createGameEntitlement)*

**Data it reads**: `listGameEntitlements` (onLoad, All-games passes already defined)

**Where the user goes next**

- → `BO-424` Gameplay Validation Command Center: *Back to Gameplay Validation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The all games rides configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the all games rides untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No all games rides configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **New attraction added later of an included type**: Covered automatically (type-based), and the coverage summary says so. *(source: contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*

#### Consistency with other screens

- Match `BO-428`: Shares the validity block and reader preview; layout makes the inclusion model visibly different.
- Match `BO-431`: Validity and activation are the same component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pass:
  name: Ultimate Park Pass
  nameAr: تذكرة المنتزه الشاملة
  product: UPP-DAY - Ultimate Park Pass (AED 199.00)
  venue: Summit Peaks
  types:
  - Rides
  - Video games
  - Skill games
  excluded:
  - Premium crane games
  model: Unlimited
  cooldownMinutes: 10
  validity: Visit date 09 Sep 2026
  activation: On first use
  status: Active
```

#### Permissions

- `createGameEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff
- `listGameEntitlements` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Entitlements: unlimited all games for a validity period, unlimited on a specific game, limited counted plays on a specific game; a package builder bundles several games and their entitlements into one product. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-875)*
- Five gaming product types, configurable per product: pay-per-play from wallet; free play on a specific set of games; unlimited play on any game; per-game play counts (e.g. 2 on A, 5 on B, unlimited on C, none on D unless paid); fully free game. *(client request · MoM 11 Sep 2026, 4.5 Gaming Module - Concept & Use Cases · DI-861)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-427` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-427`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 6: Works in All Games & Rides Pass Configuration → Configure a ticket/product that permits the guest to play all games/rides in the amusement park. This directly represents requirement 10.2.8.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-427?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-424`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-428` Specific Game/Ride Unlimited Entitlement

**Configure products that provide unlimited free usage of selected games or rides. This directly implements requirement 10.2.11.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-428 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Entitlement Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/specific-game-ride-unlimited-entitlement-bo-428` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** A product giving unlimited free use of selected games or rides while it is valid (requirement 10.2.11), for example Kids Unlimited Ride Pass on Bumper Cars, Carousel, Mini Coaster and Kids Train. The reader shows "FREE PLAY - Included in your pass." The one thing to get right: usage is fixed at UNLIMITED on this screen (no count field), and the attraction checklist is the main element.

**Known correction pending (do not draw the wrong version)**

- **kind unlimitedSingleGame allows one game, but the pack's product covers several selected attractions** Why: Kids Unlimited Ride Pass names four rides; the contract kinds are allGamesPass, unlimitedSingleGame, limitedSingleGame, package, freePlay. Either unlimitedSingleGame takes several gameIds or a package with playCount null is used - the contract must say which. *(source: screens/P08-venue-back-office.yaml#BO-428 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement / DI-875; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Unlimited Usage = ON" drawn as a text field; Included games and Included rides as two selects** Why: Unlimited is fixed on this screen; attractions are one grouped checklist. *(source: screens/P08-venue-back-office.yaml#BO-428; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No update or deactivate for an existing entitlement** Why: Only create and list exist. *(source: contracts/satellite/games.yaml#createGameEntitlement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should one unlimited entitlement cover several selected attractions (pack) or exactly one game (contract kind name)?** → Drawn default accepted: Several attractions, as the pack and DI-875 describe. *(decided by Chinmay, 2026-10-02; DEC-398 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Entitlement Name | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Included Games | select field | — | — | — | — | — | — |
| Included Rides | select field | — | — | — | — | — | — |
| Validity | select field | — | — | — | — | — | — |
| Activation | select field | — | — | — | — | — | — |
| Unlimited Usage = ON | text field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **entitlement name / product / venue**: Name with Arabic variant; Product is the catalogue product (picker); venue from the switcher. *(source: screens/P08-venue-back-office.yaml#BO-428)*
- **included games / included rides**: One checklist of attractions grouped by type (games, rides) with search; at least one. Not two separate selects. *(source: screens/P08-venue-back-office.yaml#BO-428)*
- **usage**: Shown as a fixed "Usage limit UNLIMITED" badge, not a text field "Unlimited Usage = ON". Optional daily cap and cooldown minutes beneath it. *(source: screens/P08-venue-back-office.yaml#BO-428 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*
- **validity / activation**: The shared validity block (BO-431). *(source: screens/P08-venue-back-office.yaml#BO-428)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reader result preview**: FREE PLAY / Included in your pass - in the free game state colour. *(source: screens/P08-venue-back-office.yaml#BO-428)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Creates the entitlement. One selected attraction maps to unlimitedSingleGame; several need a kind the contract lacks (see corrections). *(source: contracts/satellite/games.yaml#createGameEntitlement)*

**Where the user goes next**

- → `BO-424` Gameplay Validation Command Center: *Back to Gameplay Validation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The specific game ride configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the specific game ride untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No specific game ride configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Cooldown active on a repeat tap**: The reader refuses with "Cooldown - try again in 8 minutes" (cooldownActive), not "Not included". *(source: contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation)*

#### Consistency with other screens

- Match `BO-427`: Same validity block and reader preview; this screen picks attractions, BO-427 picks types and exclusions.
- Match `BO-410`: The FREE PLAY reader state comes from the free game display rules.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entitlement:
  name: Kids Unlimited Ride Pass
  nameAr: تذكرة الألعاب غير المحدودة للأطفال
  product: KURP - Kids Unlimited Ride Pass (AED 95.00)
  venue: Summit Peaks
  attractions:
  - Bumper Cars
  - Carousel
  - Mini Coaster
  - Kids Train
  usage: UNLIMITED
  cooldownMinutes: 5
  validity: Same day
  activation: On first use
  status: Active
```

#### Permissions

- `createGameEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Entitlements: unlimited all games for a validity period, unlimited on a specific game, limited counted plays on a specific game; a package builder bundles several games and their entitlements into one product. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-875)*
- Five gaming product types, configurable per product: pay-per-play from wallet; free play on a specific set of games; unlimited play on any game; per-game play counts (e.g. 2 on A, 5 on B, unlimited on C, none on D unless paid); fully free game. *(client request · MoM 11 Sep 2026, 4.5 Gaming Module - Concept & Use Cases · DI-861)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-428` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-428`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 8: Works in Specific Game/Ride Unlimited Entitlement → Configure products that provide unlimited free usage of selected games or rides. This directly implements requirement 10.2.11.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-428?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-424`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-429` Specific Game/Ride Limited Entitlement

**Configure products providing a defined number of free plays on specific attractions. This directly implements requirement 10.2.12.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-429 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/specific-game-ride-limited-entitlement-bo-429` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** A product giving a defined number of free plays on specific attractions (requirement 10.2.12), either per attraction (VR Racing 2, Basketball Pro 3, Bumper Cars 1) or as a shared pool (5 plays across the selected attractions). Each successful play reduces the allowance and further plays are refused at zero ("PLAY AUTHORIZED - Remaining plays 0", then refused). The one thing to get right: the Per attraction / Shared pool choice, because it changes what the guest can do with the same number.

**Known correction pending (do not draw the wrong version)**

- **Per-attraction play counts cannot be stored** Why: GameEntitlement has one playCount for all its gameIds, so "VR 2, Basketball 3, Bumper 1" (and DI-861's "2 on A, 5 on B") is a shared pool only. *(source: screens/P08-venue-back-office.yaml#BO-430 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement / DI-861; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The screen has only Entitlement Name and a "Create game entitlement" button** Why: Pack p38 lists product, included attractions, number of plays, usage scope, validity and status, plus the two usage models. *(source: screens/P08-venue-back-office.yaml#BO-430; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No update or deactivate for an existing entitlement** Why: Only create and list exist. *(source: contracts/satellite/games.yaml#createGameEntitlement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is per-attraction counting needed at launch, or is a shared pool enough?** → Drawn default accepted: Draw both; mark Per attraction as pending the contract change. *(decided by Chinmay, 2026-10-02; DEC-399 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Entitlement Name | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **entitlement name / product**: Name with Arabic variant; Product picker from the catalogue. *(source: screens/P08-venue-back-office.yaml#BO-428 / screens/P08-venue-back-office.yaml#BO-430)*
- **usage scope**: A choice - Per attraction (a plays column appears beside each selected attraction) or Shared pool (one total across the selection). *(source: screens/P08-venue-back-office.yaml#BO-430)*
- **included attractions and number of plays**: Attraction checklist; plays whole numbers at least 1. *(source: screens/P08-venue-back-office.yaml#BO-430 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement)*
- **validity, status**: The shared validity block (BO-431); status Active / Inactive. *(source: screens/P08-venue-back-office.yaml#BO-430)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create game entitlement (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Real-time usage example**: Basketball Pro - Allowed 3 - Used 2 - Remaining 1, as a small meter, to show what the guest and the reader see. *(source: screens/P08-venue-back-office.yaml#BO-430)*
- **Reader preview**: PLAY AUTHORIZED - Remaining plays 0, and the refusal that follows ("No plays left on your pass"). *(source: screens/P08-venue-back-office.yaml#BO-430 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Create game entitlement**: Creates kind limitedSingleGame (one attraction) or package (several, shared pool); the label should read "Save entitlement". *(source: contracts/satellite/games.yaml#createGameEntitlement)*

**Where the user goes next**

- → `BO-424` Gameplay Validation Command Center: *Back to Gameplay Validation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The specific game ride configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the specific game ride untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No specific game ride configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A play is reversed (machine fault)**: The play is returned to the allowance and the history shows the reversal. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*
- **Two taps race on the last play from two readers**: Only one is authorised; the other is refused "No plays left on your pass". *(source: contracts/satellite/games.yaml#authoriseGameplay)*

#### Consistency with other screens

- Match `BO-430`: Per-attraction plays here and in the package builder use the same row component.
- Match `BO-428`: Visibly different from the unlimited screen (pack p42).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
perAttraction:
  name: Arcade Starter 6
  product: ARC-6 - Arcade Starter (AED 75.00)
  rows:
  - attraction: VR Racing 01
    plays: 2
  - attraction: Basketball Pro 02
    plays: 3
  - attraction: Bumper Cars
    plays: 1
sharedPool:
  name: Fun Zone 5
  attractions:
  - VR Racing 01
  - Basketball Pro 02
  - Bumper Cars
  plays: 5
usage:
  attraction: Basketball Pro 02
  allowed: 3
  used: 2
  remaining: 1
```

#### Permissions

- `createGameEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Entitlements: unlimited all games for a validity period, unlimited on a specific game, limited counted plays on a specific game; a package builder bundles several games and their entitlements into one product. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-875)*
- Five gaming product types, configurable per product: pay-per-play from wallet; free play on a specific set of games; unlimited play on any game; per-game play counts (e.g. 2 on A, 5 on B, unlimited on C, none on D unless paid); fully free game. *(client request · MoM 11 Sep 2026, 4.5 Gaming Module - Concept & Use Cases · DI-861)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-429` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-429`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 10: Works in Specific Game/Ride Limited Entitlement → Configure products providing a defined number of free plays on specific attractions. This directly implements requirement 10.2.12.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-429?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Create game entitlement, Cancel.
- [ ] Every transition is wired: `BO-424`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-430` Game Package Builder

**Create a package containing a specific collection of games/rides. Requirement 10.2.7 explicitly requires: Create a package with specific games. Define validity for the game entitlement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-430 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/game-package-builder-bo-430` |

**Known gaps.** **Game Package Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The package builder: create a reusable package of specific games and rides, each with its own usage (VR Racing 2, Basketball Pro 3, Bumper Cars unlimited, Space Shooter 1), validity and consumption group, then validate and publish. The pack insists this screen visibly shows several attractions being added with individual allowances, not a generic form. The one thing to get right: the contents table is the screen - add rows, set limited / unlimited and plays per row, preview what the guest gets.

**Known correction pending (do not draw the wrong version)**

- **Per-attraction usage, per-row validity and consumption groups cannot be stored** Why: A package is one GameEntitlement with gameIds and a single playCount; the pack's contents table (2 / 3 / Unlimited / 1) is the screen's purpose. *(source: screens/P08-venue-back-office.yaml#BO-431 / screens/P08-venue-back-office.yaml#BO-433 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gap says the screen declares no write and the pack gives nothing to draw** Why: createGameEntitlement is bound; the pack gives the header fields, the contents table and six actions. *(source: screens/P08-venue-back-office.yaml#BO-430 / screens/P08-venue-back-office.yaml#BO-431; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Effective dates and description have no contract field; no draft, update or publish state** Why: GameEntitlement has no dates, description or lifecycle beyond isActive. *(source: contracts/satellite/games.yaml#/components/schemas/GameEntitlement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What does "Consumption group" mean - rows sharing one pool of plays, or rows consumed in a fixed order?** → Drawn default accepted: Rows sharing one pool. *(decided by Chinmay, 2026-10-02; DEC-400 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **package header**: Package name (Arabic variant), package code (unique), venue (from the switcher), description, effective dates (from / to pickers), status. *(source: screens/P08-venue-back-office.yaml#BO-430)*
- **contents rows**: Per attraction - Include / Exclude, Limited / Unlimited, Number of plays (only when Limited), Validity (inherit package or own), Consumption group (rows in the same group share one pool). Add game / Add ride open a picker filtered by type. *(source: screens/P08-venue-back-office.yaml#BO-431)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create game entitlement (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Package contents table**: Attraction, Type, Usage ("2", "Unlimited") with the type icon; total paid value of the plays shown as "worth AED 160.00 at standard prices". *(source: screens/P08-venue-back-office.yaml#BO-431 / contracts/satellite/games.yaml#getGamePricing)*
- **Existing packages**: List of packages (kind package) with contents count, validity, status; selecting one opens it read-only until an update exists. *(source: contracts/satellite/games.yaml#listGameEntitlements)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add Game / Add Ride / Remove**: Adds or removes a contents row. *(source: screens/P08-venue-back-office.yaml#BO-431)*
- **Preview**: Shows what the guest sees in the app and at a reader for each included attraction. *(source: screens/P08-venue-back-office.yaml#BO-431)*
- **Validate**: Checks every attraction is in service and priced, and no row has zero plays. *(source: contracts/satellite/games.yaml#validateGameConfiguration)*
- **Publish**: Creates the package; confirmation names the product it is linked to and that it can then be sold. *(source: contracts/satellite/games.yaml#createGameEntitlement)*

**Data it reads**: `listGameEntitlements` (onLoad, Existing packages)

**Where the user goes next**

- → `BO-424` Gameplay Validation Command Center: *Back to Gameplay Validation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game package list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game package untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game package yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game package are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Same attraction added twice**: Refused; edit the existing row. *(source: designer default)*
- **Package with an out-of-service attraction**: Warning (not block) "Bumper Cars is out of service until 14:00". *(source: contracts/satellite/games.yaml#/components/schemas/GameStatus)*

#### Consistency with other screens

- Match `BO-401`: Packages built here are what Game Package & Entitlement Association lists per attraction.
- Match `BO-429`: Same per-attraction plays row.
- Match `BO-431`: Validity column uses the shared validity block.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
header:
  name: Arcade Adventure
  nameAr: مغامرة الألعاب
  code: ARC-ADV-4H
  venue: Summit Peaks
  description: Four arcade games, 4 hours from first tap
  effective: 01 Oct 2026 - 31 Dec 2026
  status: Draft
contents:
- attraction: VR Racing 01
  type: Video game
  usage: 2
- attraction: Basketball Pro 02
  type: Skill game
  usage: 3
- attraction: Bumper Cars
  type: Ride
  usage: Unlimited
- attraction: Space Shooter
  type: Video game
  usage: 1
```

#### Permissions

- `createGameEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff
- `listGameEntitlements` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Entitlements: unlimited all games for a validity period, unlimited on a specific game, limited counted plays on a specific game; a package builder bundles several games and their entitlements into one product. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-875)*
- Five gaming product types, configurable per product: pay-per-play from wallet; free play on a specific set of games; unlimited play on any game; per-game play counts (e.g. 2 on A, 5 on B, unlimited on C, none on D unless paid); fully free game. *(client request · MoM 11 Sep 2026, 4.5 Gaming Module - Concept & Use Cases · DI-861)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-430` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-430`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 12: Works in Game Package Builder → Create a package containing a specific collection of games/rides. Requirement 10.2.7 explicitly requires: Create a package with specific games. Define validity for the game entitlement.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-430?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create game entitlement, Cancel.
- [ ] Every transition is wired: `BO-424`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-431` Entitlement Validity & Activation Rules

**Control when a gameplay entitlement becomes valid and when it expires. The source specifically requires the ability to define validity for game entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-431 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/entitlement-validity-activation-rules-bo-431` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** When a gameplay entitlement becomes valid and when it expires: activation (at purchase, at first game tap, fixed date, visit date - and per DI-874 from first top-up), validity (same day, fixed start/end, X hours or X days from activation), expiry behaviour and an optional grace period. Worked example: Arcade Adventure, activated at first tap 14:00, valid 4 hours, expires 18:00. The one thing to get right: a live example line under the controls that computes the real expiry, because "4 hours from first tap" and "same day" are easy to confuse.

**Known correction pending (do not draw the wrong version)**

- **X hours from activation, Fixed start / end, Visit date activation and grace period have no contract value** Why: validityKind is sameDay / days / untilDate / untilUsed and activationKind onPurchase / onFirstUse / onDate; the pack's own example (4 hours) cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-431 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The screen's only action is "Create game entitlement"** Why: This is a block of the entitlement editor, not a separate entitlement. *(source: screens/P08-venue-back-office.yaml#BO-431; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gap says the pack gives nothing to draw** Why: Pack p39-p40 give four activation methods, four validity methods, a worked example, expiry behaviour and grace period. *(source: screens/P08-venue-back-office.yaml#BO-431 / screens/P08-venue-back-office.yaml#BO-432; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "from first top-up" (DI-874) an activation method for game entitlements or only for the card?** → Drawn default accepted: Card only (Board 7); not offered here. *(decided by Chinmay, 2026-10-02; DEC-401 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **activation method**: At purchase / At first game tap (default) / Fixed date / Visit date. A help line explains that On first use is what a guest expects from a pass bought the night before. *(source: screens/P08-venue-back-office.yaml#BO-431 / contracts/satellite/games.yaml#/components/schemas/GameEntitlement / DI-874)*
- **validity method**: Same day (until venue closing), Fixed start / end (date-time pickers), X hours from activation, X days from activation; the number appears only for the last two. *(source: screens/P08-venue-back-office.yaml#BO-431)*
- **grace period**: Optional minutes after expiry during which a tap is still accepted (e.g. a guest already in the queue). *(source: screens/P08-venue-back-office.yaml#BO-432)*
- **expiry behaviour**: Shown as fixed statements (reject further usage, keep transaction history, mark entitlement Expired), not options. *(source: screens/P08-venue-back-office.yaml#BO-431 / screens/P08-venue-back-office.yaml#BO-432)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create game entitlement (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Live example**: "First tap 14:00 - expires 18:00 (+15 min grace)" computed from the selected rule and today's venue hours. *(source: screens/P08-venue-back-office.yaml#BO-431)*
- **Applies to**: The list of entitlements and packages using this validity, since validity sits on each entitlement. *(source: contracts/satellite/games.yaml#listGameEntitlements)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves validity and activation as part of the entitlement being edited (BO-427 to BO-430), not as a separate rule. *(source: contracts/satellite/games.yaml#createGameEntitlement)*

**Where the user goes next**

- → `BO-424` Gameplay Validation Command Center: *Back to Gameplay Validation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entitlement validity activation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entitlement validity activation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entitlement validity activation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entitlement validity activation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Same day validity on a pass activated at 21:50 with closing at 22:00**: The example warns "Activated 10 minutes before closing - valid 10 minutes". *(source: designer default)*
- **Expired entitlement tapped**: Refused with a plain reason ("Your pass expired at 18:00"); history kept. *(source: screens/P08-venue-back-office.yaml#BO-432)*

#### Consistency with other screens

- Match `BO-430`: One validity component reused in BO-427, BO-428, BO-429 and BO-430 (per VO-R14); this board entry is its explanation and anchors into the entitlement editors.
- Match `BO-459`: Card expiry runtime validation (Board 7) uses the same activation words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example:
  package: Arcade Adventure
  activation: At first game tap
  validity: 4 hours from activation
  firstTap: '14:00'
  expiry: '18:00'
  graceMinutes: 15
```

#### Permissions

- `createGameEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-431` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-431`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 14: Works in Entitlement Validity & Activation Rules → Control when a gameplay entitlement becomes valid and when it expires. The source specifically requires the ability to define validity for game entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-431?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create game entitlement, Cancel.
- [ ] Every transition is wired: `BO-424`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-432` Real-Time Gameplay Authorization

**Provide the operational transaction view showing exactly how TICVAI evaluates a customer tap. Requirement 10.2.13 requires the system to validate the balance/card, bonus and entitlement in real time and deduct the applicable amount before gameplay.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block B · task VM-BO-432 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/real-time-gameplay-authorization-bo-432` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): authoriseGameplay (ACCESS_VALIDATE) decides and charges a live tap at a reader; calling it from the back office would charge a guest. The stored decision trace …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The operational transaction view that shows exactly how TICVAI decided one tap: reader R-014, game VR Racing, card ****4321 - card status, attraction status, entitlement check, bonus balance, paid balance, game price, deduction (Bonus AED 10 + Paid AED 10), result PLAY AUTHORIZED with remaining paid balance AED 65 - or the entitlement path (Package Arcade Adventure, remaining plays 1). The one thing to get right: it is a read-only trace of a decision that already happened; nothing on this back-office screen authorises or charges a guest.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The trace is not readable after the fact (CHG-SBO-005)
- An unlabelled primary button and Cancel are the only components; gap says the pack gives nothing to draw (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The screen binds authoriseGameplay (ACCESS_VALIDATE) onAction (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How long are full decision traces kept for investigation?** → Drawn default accepted: Show trace where available, else "Trace not retained" with the summary row. *(decided by Chinmay, 2026-10-02; DEC-402 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **find a transaction**: By card (last four or full number), reader, attraction and time; or arrive from a feed row on BO-424. *(source: screens/P08-venue-back-office.yaml#BO-432 / contracts/satellite/games.yaml#listGameplayTransactions)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Decision trace**: Numbered steps 1 Card status, 2 Attraction status, 3 Entitlement check, 4 Bonus balance, 5 Paid balance, 6 Game price, 7 Deduction - each with its value and a pass / fail mark; the failing step of a refusal is highlighted with the guest message that was shown. *(source: screens/P08-venue-back-office.yaml#BO-432 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation)*
- **Result card**: PLAY AUTHORIZED / REJECTED, funding source(s), amount consumed, remaining balance or remaining plays, decided online or offline (and sync time). *(source: screens/P08-venue-back-office.yaml#BO-432 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Re-run as simulation**: Opens BO-433 with the same card, reader and time pre-filled, to see whether today's configuration would decide the same. *(source: contracts/satellite/games.yaml#simulateGameplayAuthorisation)*
- **Reverse play**: Not on this screen; reversals belong to the transaction monitor with a reason (link). *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*

**Where the user goes next**

- → `BO-424` Gameplay Validation Command Center: *Back to Gameplay Validation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The real-time gameplay authorization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the real-time gameplay authorization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No real-time gameplay authorization yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the real-time gameplay authorization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Decided offline**: Banner "Decided by the reader offline at 10:41, synced 10:58"; the balance shown is what the reader knew then. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*

#### Consistency with other screens

- Match `BO-412`: Same step names as the Board 2 tap flow.
- Match `BO-467`: Tap Validation & Decision Trace (Board 8) is the monitoring version of this trace; one trace component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
transaction:
  reader: R-014
  game: VR Racing 01
  card: '****4321'
  at: 01 Oct 2026 10:42:05
steps:
- step: Card status
  value: Active
  passed: true
- step: Attraction status
  value: Available
  passed: true
- step: Entitlement check
  value: No applicable entitlement
  passed: true
- step: Bonus balance
  value: AED 10.00
  passed: true
- step: Paid balance
  value: AED 75.00
  passed: true
- step: Game price
  value: AED 20.00
  passed: true
- step: Deduction
  value: Bonus AED 10.00 + Paid AED 10.00
  passed: true
result:
  decision: PLAY AUTHORIZED
  remainingPaid: AED 65.00
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-432` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-432`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 16: Works in Real-Time Gameplay Authorization → Provide the operational transaction view showing exactly how TICVAI evaluates a customer tap. Requirement 10.2.13 requires the system to validate the balance/card, bonus and entitlement in real time …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-432?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-424`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-433` Validation Simulator & Exception Analysis

**Allow administrators to test entitlement and payment configurations before deployment and investigate rejected gameplay transactions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-433 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/validation-simulator-exception-analysis-bo-433` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Two tools: a simulator that tests entitlement and payment configuration before activation (card, reader, attraction, date/time, package, entitlement, paid and bonus balance -> decision trace and result "AUTHORIZED - Source Arcade Package - Remaining plays after transaction 0" or "REJECTED - ENTITLEMENT EXHAUSTED"), and exception investigation of real rejected transactions (transaction id, reader, card, rule evaluated, failed condition, rejection code, time). The one thing to get right: the trace shows the rules that did not fire as well as the one that did, because silent misconfiguration is the failure mode.

**Known correction pending (do not draw the wrong version)**

- **Simulation inputs Package, Entitlement, Paid balance and Bonus balance cannot be passed** Why: The simulate request takes readerId, cardId, credentialIdentifier, gameId, at, guestHeightCm and offline only; a what-if on balances is impossible without a real card holding them. *(source: screens/P08-venue-back-office.yaml#BO-433 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisationRequest; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Exception investigation has no bound read and no rule-evaluated / failed-condition fields** Why: listGameplayTransactions (outcome refused) must be bound; GameplayTransaction has only a free-text reason. *(source: contracts/satellite/games.yaml#listGameplayTransactions / contracts/satellite/games.yaml#/components/schemas/GameplayTransaction; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Unlabelled primary button and Cancel only; gap says the pack gives nothing to draw** Why: Pack p41-p42 give eight inputs, the seven-step trace, results, seven investigation columns and five actions. *(source: screens/P08-venue-back-office.yaml#BO-433; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the simulator test a draft configuration (not yet activated) as the pack's "before activation" implies?** → Drawn default accepted: Test the live configuration; show "Draft testing pending" on BO-425/426. *(decided by Chinmay, 2026-10-02; DEC-403 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **simulation inputs**: Customer / card (test card or a real card read-only), Reader, Attraction (filled from the reader), Date / time (default now, venue time), Package, Entitlement, Paid balance, Bonus balance (AED) - the last four as optional overrides of the card's real values, marked "simulated". *(source: screens/P08-venue-back-office.yaml#BO-433 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisationRequest)*
- **guest height**: Optional cm, to test height restrictions. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisationRequest)*
- **offline**: Switch "Simulate as an offline reader" to test the edge-package decision and offline maximum value. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisationRequest)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Decision trace**: 1 Credential, 2 Reader, 3 Attraction, 4 Package, 5 Validity, 6 Usage remaining, 7 Authorization - each pass / fail with detail; rules that were evaluated and skipped shown greyed with why. *(source: screens/P08-venue-back-office.yaml#BO-433 / contracts/satellite/games.yaml#simulateGameplayAuthorisation)*
- **Exception investigation**: Table of real refusals (cursor-paged, per VO-R12) - Transaction ID, Reader, Card (masked), Rule evaluated, Failed condition, Rejection code, Timestamp; selecting one shows its trace. *(source: screens/P08-venue-back-office.yaml#BO-433 / contracts/satellite/games.yaml#listGameplayTransactions)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Simulate**: Runs the simulation; nothing is charged or recorded against the card; the result is labelled SIMULATION. *(source: contracts/satellite/games.yaml#simulateGameplayAuthorisation)*
- **View Rule / View Wallet / View Entitlement**: Open BO-425/426, the wallet view and the entitlement editor and return here. *(source: screens/P08-venue-back-office.yaml#BO-433)*
- **Export Trace**: Exports the trace as PDF/CSV with inputs, time and who ran it. *(source: screens/P08-venue-back-office.yaml#BO-433)*

**Where the user goes next**

- → `BO-424` Gameplay Validation Command Center: *Back to Gameplay Validation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validation simulator exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validation simulator exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validation simulator exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validation simulator exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **AI-assisted diagnosis (pack enhancement)**: Likely configuration error shown as a suggestion with its reason and an explicit Open fix action (per VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-433)*
- **Simulating a time in the past**: Uses today's configuration, not the configuration at that time; say so. *(source: contracts/satellite/games.yaml#simulateGameplayAuthorisation)*

#### Consistency with other screens

- Match `BO-413`: Same simulation and result component as the reader test console.
- Match `BO-402`: Health check tests the whole set-up; link "Check all attractions" there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
simulation:
  card: TEST-001
  reader: R-014
  game: VR Racing 01
  at: 01 Oct 2026 15:30
  entitlement: Arcade Adventure
  remainingUses: 1
trace:
- Credential - pass
- Reader - pass
- Attraction - pass
- Package - pass (Arcade Adventure)
- Validity - pass (expires 18:00)
- Usage remaining - pass (1)
- Authorization - AUTHORIZED
result:
  decision: AUTHORIZED
  fundingSource: Arcade Package
  remainingAfter: 0
rejected:
  transactionId: GTX-20261001-018342
  reader: R-023
  card: '****5517'
  rule: Usage remaining
  failed: remaining plays = 0
  code: entitlementExhausted
  at: 01 Oct 2026 10:12:44
```

#### Permissions

- `simulateGameplayAuthorisation` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-433` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS61 Game and Ride Board 4.dc.html#bo-433`
- Workshop pack: Game_and_Ride_Module.pdf board 4
- Flow F190 *Game and Ride board 4: Gameplay Validation Command Center*, step 18: Works in Validation Simulator & Exception Analysis → Allow administrators to test entitlement and payment configurations before deployment and investigate rejected gameplay transactions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-433?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-424`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**14 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createGameEntitlement": {"method":"POST","path":"/game-entitlements","contract":"games","summary":"Define a pass, package or per-game entitlement","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameEntitlement","responds":"GameEntitlement"},
"getGameplayValidationRules": {"method":"GET","path":"/gameplay-validation-rules","contract":"games","summary":"What a tap is checked against, and in what order","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameplayValidationRules"},
"listGameEntitlements": {"method":"GET","path":"/game-entitlements","contract":"games","summary":"Passes, packages and per-game entitlements","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameEntitlement"},
"listGameplayTransactions": {"method":"GET","path":"/gameplay-transactions","contract":"games","summary":"Taps, decisions and what they cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"readerId","in":"query","required":null},{"name":"outcome","in":"query","required":null}],"requestBody":null,"responds":"GameplayTransaction"},
"setGameplayValidationRules": {"method":"PUT","path":"/gameplay-validation-rules","contract":"games","summary":"Deduction priority and the order of checks","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameplayValidationRules","responds":"GameplayValidationRules"},
"simulateGameplayAuthorisation": {"method":"POST","path":"/gameplay-authorisations/simulate","contract":"games","summary":"What would happen if this card tapped this reader","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameplayAuthorisationRequest","responds":"GameplayAuthorisation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"GameEntitlement": {"type":"object","x-ticvai-persistence":"games.entitlement","description":"Board 4. **A right to play, not money** — consumed before money is.","required":["code","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["allGamesPass","unlimitedSingleGame","limitedSingleGame","package","freePlay"]},"gameIds":{"type":"array","items":{"type":"string","format":"uuid"}},"attractionTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"includesGamesAddedLater":{"type":"boolean","default":true,"description":"**Whether a pass sold today covers a game added tomorrow** (Chinmay, 2 October, workbook Q397: \"venue configures; default yes\"; CHG-CSA-028). True, the default: an `allGamesPass`, or a pass bound by `attractionTypeIds`, covers games added after it was sold that match it; the coverage summary says so. False: it covers only the games that existed at sale. A pass listing `gameIds` covers those games only, whatever this says."},"playCount":{"type":"integer","nullable":true,"description":"For `limitedSingleGame` and `package`. Null means unlimited."},"validityKind":{"type":"string","enum":["sameDay","days","untilDate","untilUsed"]},"validityDays":{"type":"integer","nullable":true},"activationKind":{"type":"string","enum":["onPurchase","onFirstUse","onDate"],"default":"onFirstUse","description":"**On first use is what a guest expects from a day pass bought the night before.** On purchase is what a venue defaults to by accident, and it costs them a day.\n"},"dailyPlayCap":{"type":"integer","nullable":true},"cooldownMinutes":{"type":"integer","nullable":true,"description":"**Unlimited does not mean continuous.** A cooldown is how one child does not hold a popular ride all afternoon.\n"},"linkedProductId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"GameplayAuthorisation": {"type":"object","x-ticvai-persistence":"games.authorisation","description":"Board 4.9. **The refusal reason is the product.**","properties":{"id":{"type":"string","format":"uuid"},"decision":{"type":"string","enum":["allow","refuse"]},"reason":{"type":"string","nullable":true,"enum":["ok","cardNotFound","cardExpired","cardBlocked","retapTooSoon","heightRestriction","ageRestriction","insufficientFunds","entitlementExhausted","entitlementNotValidHere","cooldownActive","dailyCapReached","readerNotConfigured","gameUnavailable"]},"guestMessage":{"type":"string","nullable":true,"description":"***\"No plays left on your pass\"* rather than *\"Declined\"*.** One is a guest who understands; the other is a member of staff walking over.\n"},"chargedFrom":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementId":{"type":"string","format":"uuid","nullable":true},"remainingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"remainingPlays":{"type":"integer","nullable":true},"trace":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string"},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"decidedOffline":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"GameplayAuthorisationRequest": {"type":"object","required":["readerId"],"properties":{"readerId":{"type":"string","format":"uuid"},"cardId":{"type":"string","format":"uuid","nullable":true},"credentialIdentifier":{"type":"string","nullable":true},"gameId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time","nullable":true},"guestHeightCm":{"type":"integer","nullable":true},"offline":{"type":"boolean","default":false}}},
"GameplayTransaction": {"type":"object","x-ticvai-persistence":"games.gameplay_transaction","description":"Boards 8.2 and 8.5. **The refused ones are the valuable half.**","properties":{"id":{"type":"string","format":"uuid"},"readerId":{"type":"string","format":"uuid"},"gameId":{"type":"string","format":"uuid","nullable":true},"cardId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["allowed","refused","reversed"]},"reason":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargedFrom":{"type":"string","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"ticketsEarned":{"type":"integer","nullable":true},"decidedOffline":{"type":"boolean","default":false},"syncedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"GameplayValidationRules": {"type":"object","x-ticvai-persistence":"games.validation_rules","description":"Boards 4.2 and 4.3. **Must be an answer, stated once**, rather than whatever the firmware happens to do.\n","properties":{"deductionOrder":{"type":"array","items":{"type":"string","enum":["entitlement","freePlay","bonusCredit","promotionalCredit","gameCredit","cashCredit","directPay"]}},"checkOrder":{"type":"array","items":{"type":"string","enum":["cardValid","cardNotExpired","cardNotBlocked","restrictionsMet","retapWindow","entitlementAvailable","fundsSufficient"]}},"allowPartialEntitlement":{"type":"boolean","default":false,"description":"**Whether an entitlement covering part of the price may be topped up with credit.** Usually no, because a guest who thinks they have a pass does not expect a charge.\n"},"refuseBelowBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"offlineDecisionAllowed":{"type":"boolean","default":true},"offlineMaximumValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}}
}
```
