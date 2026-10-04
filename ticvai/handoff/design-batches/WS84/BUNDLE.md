# WS84 — Game and Ride board 7

**10 screens · 6 operations · 6 schemas · 3 permissions**

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
  `PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_OPERATE`. A control nobody can use must say so,
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
| `BO-454` | Card Lifecycle Command Center | D | 2 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-455` | Card / Credential Profile | D | 0 | 18 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-456` | Card Expiry Rule Configuration | D | 4 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-457` | Last Recharge & Last Activity Tracking | D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-458` | Expiry Monitoring & Upcoming Expiration | B | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-459` | Card Expiry Runtime Validation | D | 7 | 2 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-460` | Card Block, Suspend & Reactivation Control | D | 0 | 8 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-461` | Card Replacement & Wallet Relinking | D | 0 | 4 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-462` | Customer Balance & Credential Status View | D | 0 | 6 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-463` | Card Lifecycle Audit & History | D | 0 | 4 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-455, BO-457, BO-458, BO-459, BO-461, BO-462, BO-463 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-454` Card Lifecycle Command Center

**Give operations and management a central view of all active game cards / RFID credentials and their lifecycle status.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-454 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/games-rides/card-lifecycle-command-center-bo-454` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No staff-audience read of a game card (getGameCard is guest-only; used on BO-396, BO-454, BO-455, BO-457, BO-462, BO-486).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The landing screen of the card lifecycle board: how many game cards are active, used and recharged today, which are about to expire, which are expired, blocked or dormant, and how much value sits on them. Arcade operations and finance use it daily to watch card health and to jump to a single card. The one thing to get right: it is the shared command-centre pattern (KPI tiles, the lifecycle distribution, alerts, then a card search) and every tile opens the board screen behind it.

**Known correction pending (do not draw the wrong version)**

- **The KPI tiles and card table have no operation behind them** Why: The only bound read is getGameCard for one card code; no operation lists cards or counts them by status or expiry. *(source: contracts/satellite/games.yaml#getGameCard; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- getGameCard is a guest-audience reader path with no permission (CHG-WIR-004)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What makes a card "Dormant" (no activity for how long), and is it distinct from "Expiring soon"?** → Drawn default accepted: Dormant = no activity for 90 days and not yet expired; tile footnote states the rule. *(decided by Chinmay, 2026-10-02; DEC-418 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search card lifecycle | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, status, expiry period, last activity, last recharge, customer/card — which are present is a decision the pack already made. | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search card**: One box that accepts a full card number, the last four digits, a guest name or a phone number (DI-538: operations identify the guest by phone or ID). Last four digits alone returns a short list to choose from, never a single guess. *(source: screens/P08-venue-back-office.yaml#BO-455 / DI-538)*
- **Filters**: Status (Active, Expiring soon, Expired, Blocked, Dormant), Expiry period (next 7 / 30 / 60 days), Last activity and Last recharge (date ranges), Customer / card. Venue comes from the top bar, not a filter. *(source: screens/P08-venue-back-office.yaml#BO-455)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Active Cards** (metric tile)

**Cards Used Today** (metric tile)

**Cards Recharged Today** (metric tile)

**Expiring in 30 Days** (metric tile)

**Expired Cards** (metric tile)

**Blocked Cards** (metric tile)

**Dormant Cards** (metric tile)

**Cards with Wallet Balance** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Eight tiles in two rows: Total active cards, Cards used today, Cards recharged today, Expiring in 30 days, Expired cards, Blocked cards, Dormant cards, Cards with wallet balance. Each tile with a delta against yesterday and a click-through (Expiring opens BO-458 pre-filtered; Blocked opens BO-460's list). *(source: screens/P08-venue-back-office.yaml#BO-454)*
- **Lifecycle distribution**: One horizontal stacked bar Active / Expiring soon / Expired / Blocked / Dormant with counts and the value held in each segment ("Expiring soon 312 cards, AED 18,450"). *(source: screens/P08-venue-back-office.yaml#BO-455)*
- **Card activity table**: Columns Card (****4321), Customer (or "Unregistered card"), Balance (AED), Last recharge, Last activity, Expiry, Status chip. Dates in dd MMM yyyy. Sorted by last activity, newest first; cursor paging. *(source: screens/P08-venue-back-office.yaml#BO-455)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **View card**: Opens the card profile (BO-455) carrying the card code. *(source: screens/P08-venue-back-office.yaml#BO-454)*
- **Block, Reactivate**: Row actions open BO-460 with the card chosen; never a one-click block from the table. *(source: screens/P08-venue-back-office.yaml#BO-455)*
- **View wallet**: Opens the guest's wallet record; disabled for unregistered cards with "No guest linked". *(source: screens/P08-venue-back-office.yaml#BO-455)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-455` Card / Credential Profile: *Card / Credential Profile*; carries `cardCode`
- → `BO-456` Card Expiry Rule Configuration: *Card Expiry Rule Configuration*
- → `BO-457` Last Recharge & Last Activity Tracking: *Last Recharge & Last Activity Tracking*; carries `cardCode`
- → `BO-458` Expiry Monitoring & Upcoming Expiration: *Expiry Monitoring & Upcoming Expiration*
- → `BO-459` Card Expiry Runtime Validation: *Card Expiry Runtime Validation*
- → `BO-460` Card Block, Suspend & Reactivation Control: *Card Block, Suspend & Reactivation Control*; carries `cardId`
- → `BO-461` Card Replacement & Wallet Relinking: *Card Replacement & Wallet Relinking*; carries `cardId`
- → `BO-462` Customer Balance & Credential Status View: *Customer Balance & Credential Status View*; carries `cardCode`
- → `BO-463` Card Lifecycle Audit & History: *Card Lifecycle Audit & History*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card lifecycle list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card lifecycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card lifecycle yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card lifecycle are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Card search with the last four digits matches 14 cards**: Show the 14 with masked number, guest and status to choose from. *(source: designer default)*
- **Viewer without wallet rights**: Balances show as "Hidden" with the permission named; lifecycle data still shows (VO-R08). *(source: contracts/satellite/wallet.yaml#getWalletBalance)*

#### Consistency with other screens

- Match `BO-394`: The games operations dashboard and this board landing use the same command-centre tile component and venue scope (VO-R02).
- Match `BO-458`: The Expiring in 30 days tile here must equal the 30-day bucket there.
- Match `BO-414`: Wallet balances shown here are the same values the wallet and credit dashboard shows for the card's wallet.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  active: 48210
  usedToday: 6120
  rechargedToday: 1840
  expiring30: 312
  expired: 2210
  blocked: 87
  dormant: 5420
  withBalance: 31600
cards:
- card: '****4321'
  customer: Khalid Al Zaabi
  balance: AED 125.00
  lastRecharge: 01 Sep 2026
  lastActivity: 08 Sep 2026
  expiry: 08 Mar 2027
  status: Active
- card: '****6215'
  customer: Unregistered card
  balance: AED 35.00
  lastRecharge: 01 Mar 2026
  lastActivity: 04 Mar 2026
  expiry: 04 Sep 2026
  status: Expired
- card: '****1289'
  customer: Priya Nair
  balance: AED 85.00
  lastRecharge: 15 Mar 2026
  lastActivity: 15 Mar 2026
  expiry: 15 Oct 2026
  status: Expiring in 14 days
```

#### Permissions

- `getGameCard` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-454` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-454`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 1: Opens Card Lifecycle Command Center → Give operations and management a central view of all active game cards / RFID credentials and their lifecycle status.
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F193 branch at step 1 (expected): when Nothing has been set up on Card Lifecycle Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F193 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-454?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-455`, `BO-456`, `BO-457`, `BO-458`, `BO-459`, `BO-460`, `BO-461`, `BO-462`, `BO-463`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-455` Card / Credential Profile

**Provide the master backend profile for an individual physical or digital game credential.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-455 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card Information) and no metric row |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/games-rides/card-credential-profile-bo-455` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** One card's master record: which physical or digital credential it is, whose it is, which wallet it draws on, its lifecycle dates and every value attached to it. Arcade supervisors open it from a search, a complaint or a block. The one thing to get right: the card is the credential, not the value; show the card status and the wallet's balances as two distinct blocks so blocking a card visibly leaves the value intact.

**Known correction pending (do not draw the wrong version)**

- **The screen is drawn as a list ("Every card credential profile") with a detail panel** Why: It is reached with one card code and is one record's profile; there is no card list behind it. *(source: screens/P08-venue-back-office.yaml#BO-455; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Card status options differ from the pack** Why: GameCard.status is active, blocked, expired, transferred; the pack lists Active, Blocked, Expired, Suspended, Replaced. Transferred reads as Replaced; Suspended has no state. *(source: screens/P08-venue-back-office.yaml#BO-456 / contracts/satellite/games.yaml#/components/schemas/GameCard; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The card record lacks fields the profile shows** Why: No last recharge date, issue location, wallet id, RFID UID, free plays or entitlements on GameCard; they live on the wallet, the wallet credential and the entitlement records and must be read from there. *(source: contracts/satellite/games.yaml#/components/schemas/GameCard / contracts/satellite/wallet.yaml#linkWalletCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **GameCard holds paid value as whole "credits" while the pack and the wallet show AED. Which does the profile show?** → Drawn default accepted: AED from the wallet when the card is wallet-linked; "credits" only for a stand-alone card, labelled as credits. *(decided by Chinmay, 2026-10-02; DEC-419 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Card (cardCode)**: Arrives from the board landing or a search; the screen is one card, not a list. *(source: screens/P08-venue-back-office.yaml#BO-455)*

#### Outputs: what the screen shows and produces

**Shown**

**Every card credential profile** (data table)

| Shows | Format | Notes |
|---|---|---|
| Card ID | text | not in the schema: `Card ID` |
| RFID UID / credential ID | text | not in the schema: `RFID UID / Credential ID` |
| Card number | text | not in the schema: `Card Number` |
| Customer | text | not in the schema: `Customer` |
| Wallet ID | text | not in the schema: `Wallet ID` |
| Issue date | text | not in the schema: `Issue Date` |
| Issue location | text | not in the schema: `Issue Location` |
| Card type | text | not in the schema: `Card Type` |
| Status | text | not in the schema: `Status` |

**The selected card credential profile** (detail panel): The pack groups this record's detail under its own headings: “Linked Values”, “Page 65 of 105”.

| Shows | Format | Notes |
|---|---|---|
| Card ID | text | not in the schema: `Card ID` |
| RFID UID / credential ID | text | not in the schema: `RFID UID / Credential ID` |
| Card number | text | not in the schema: `Card Number` |
| Customer | text | not in the schema: `Customer` |
| Wallet ID | text | not in the schema: `Wallet ID` |
| Issue date | text | not in the schema: `Issue Date` |
| Issue location | text | not in the schema: `Issue Location` |
| Card type | text | not in the schema: `Card Type` |
| Status | text | not in the schema: `Status` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Card header**: Masked card number large (****4321), status chip, card type (Physical card, Wristband, Digital), issue date and place, guest (or "Unregistered card"), wallet link. Full card number and RFID UID behind a "Show" control that needs the card-management permission and is logged. *(source: screens/P08-venue-back-office.yaml#BO-455)*
- **Lifecycle**: Last recharge, Last activity, Calculated expiry, Days remaining ("152 days"), and the basis in words ("Expires 6 months after the latest of last recharge and last activity"). Days remaining in amber under 30, red under 7. *(source: screens/P08-venue-back-office.yaml#BO-455 / contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules)*
- **Linked values**: Tiles Paid balance (AED), Bonus balance (AED, with its own expiry), Redemption credits (whole number, never AED), Free plays, Active entitlements (list with remaining plays). Money and credits must never share a format. *(source: screens/P08-venue-back-office.yaml#BO-455 / screens/P08-venue-back-office.yaml#BO-456 / contracts/satellite/games.yaml#/components/schemas/GameCard)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Block, Reactivate, Replace**: Open BO-460 / BO-461 with this card; only the actions legal from the current status are enabled (an expired or replaced card offers none, with the reason). *(source: screens/P08-venue-back-office.yaml#BO-456 / contracts/satellite/games.yaml#setGameCardLifecycle)*
- **View wallet, View transactions**: Open the wallet and the card's history (BO-463). *(source: screens/P08-venue-back-office.yaml#BO-456)*

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card credential profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card credential profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card credential profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card credential profile are still there. The pack's own statuses are Last Recharge — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Card code not found**: "No card ****4321 at Summit Peaks"; if the code belongs to another venue, say so and do not switch venue (VO-R09). *(source: contracts/satellite/games.yaml#getGameCard)*
- **Card was replaced**: Status Replaced with "Balance moved to ****9875 on 18 Apr 2026" and a link to the new card. *(source: contracts/satellite/games.yaml#/components/schemas/GameCard)*

#### Consistency with other screens

- Match `BO-462`: The guest-facing balance view shows the same values in the same order (paid, bonus, redemption credits, free plays, entitlements).
- Match `BO-421`: Free plays shown here are the free-game credits managed there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
card:
  card: '****4321'
  type: Wristband
  issued: 01 Mar 2026, Summit Peaks Arcade POS 2
  guest: Khalid Al Zaabi
  status: Active
lifecycle:
  lastRecharge: 01 Sep 2026
  lastActivity: 08 Sep 2026
  expiry: 08 Mar 2027
  daysRemaining: 158
values:
  paid: AED 125.00
  bonus: AED 25.00 (expires 30 Sep 2026)
  redemptionCredits: 2450
  freePlays: 2
  entitlements: All Games Pass (today); VR Racing, 2 plays left
```

#### Permissions

- `getGameCard` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-455` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-455`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 2: Works in Card / Credential Profile → Provide the master backend profile for an individual physical or digital game credential.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-455?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-456` Card Expiry Rule Configuration

**Configure the backend rule that determines when a card expires.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-456 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Rule Configuration; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/card-expiry-rule-configuration-bo-456` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of game card expiry rules.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The rule that decides when a game card expires, calculated by TICVAI and never programmed into a reader. The client's requirement is six months from the last card activity or last recharge; the venue sets the period, the basis, the warnings that go out before, and what happens to value on an expired card. The pack calls this the most important screen of the board. The one thing to get right: show the formula and a worked example live, so whoever saves it sees which date a real card would get.

**Known correction pending (do not draw the wrong version)**

- **"Rule Name: Standard Game Card Expiry" is a field label, and "Last Recharge Date" / "Last Activity Date" are select fields** Why: A sample value used as a label, and the three basis options rendered as three separate controls; they are one choice. *(source: screens/P08-venue-back-office.yaml#BO-456; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The basis cannot express "latest of last recharge or last activity", nor a fixed expiry date** Why: The enum is fromIssue, fromLastActivity, fromLastRecharge; the pack's recommended Max(...) relies on extendOnRecharge, and DI-880 also asks for a fixed-date expiry. *(source: screens/P08-venue-back-office.yaml#BO-456 / contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules / DI-880; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read for the stored rule** Why: setGameCardExpiryRules is a whole-record PUT with no matching GET, so the editor cannot open pre-filled (VO-R04). *(source: contracts/satellite/games.yaml#setGameCardExpiryRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No applicability** Why: The pack scopes the rule by venue, card type, wallet type, product and segment; the record is one per tenant. *(source: screens/P08-venue-back-office.yaml#BO-457 / contracts/satellite/games.yaml#setGameCardExpiryRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **When the rule changes, are existing cards' expiry dates recalculated or only new events?** → Drawn default accepted: Draw a greyed "Recalculate existing cards" checkbox, unchecked, in the confirm. *(decided by Chinmay, 2026-10-02; DEC-420 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rule Name: Standard Game Card Expiry | text field | — | — | — | — | — | — |
| Last Recharge Date | select field | — | — | — | — | — | — |
| Last Activity Date | select field | — | — | — | — | — | — |
| Latest of Last Recharge or Last Activity | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rule name**: Text, default "Standard game card expiry"; the record has no name, so it is a label until it does. *(source: screens/P08-venue-back-office.yaml#BO-456 / contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules)*
- **Expiry period (validityMonths)**: Whole months, minimum 1, default 6; shown as "[6] months". *(source: contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules / MATRIX 10.2.21)*
- **Expiry basis (basis, extendOnRecharge)**: One radio group in the pack's words: Last recharge date, Last activity date, Latest of last recharge or last activity (recommended, pre-selected), plus From issue date. The recommended option is last activity with "a recharge also resets the clock" on. Under it, the sentence "Expiry date = latest of last recharge or last activity + 6 months". *(source: screens/P08-venue-back-office.yaml#BO-456 / contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules)*
- **Warnings (warnBeforeDays, warningChannels)**: Chips for days before expiry (30, 7, 1 suggested; any whole numbers, sorted descending) and channel checkboxes (Email, SMS, App notification). No warning days means guests get no notice; say so in amber. *(source: contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules)*
- **On expiry (onExpiry, holdForClaimDays)**: Closed choice: Forfeit, Hold for claim (default) for [N] days, Transfer to breakage. The days field shows only for Hold for claim and is required there. *(source: contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules)*
- **Applicability (venue, card type, wallet type, product, customer segment)**: Draw greyed (per VO-R13) under "Applies to"; the rule is one per tenant, so show "All venues of Yas Leisure Group" as the only state. *(source: screens/P08-venue-back-office.yaml#BO-456 / screens/P08-venue-back-office.yaml#BO-457 / contracts/satellite/games.yaml#setGameCardExpiryRules)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Worked example**: Two date inputs (Last recharge, Last activity) pre-filled with the pack's example and the result: Last recharge 01 Mar 2026, last activity 20 Apr 2026, expiry 20 Oct 2026. Recalculates as the basis or period changes. *(source: screens/P08-venue-back-office.yaml#BO-456)*
- **Architecture note**: A one-line band: "Readers do not hold this rule. A tap sends the card to TICVAI, which checks status and expiry and answers Approve or Reject." Links to BO-459. *(source: screens/P08-venue-back-office.yaml#BO-454 / screens/P08-venue-back-office.yaml#BO-463)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save expiry rule**: Sends the whole rule (per VO-R04). The confirm states the scope ("Applies to every venue of the tenant") and that readers apply it through TICVAI immediately, since expiry is decided centrally. *(source: contracts/satellite/games.yaml#setGameCardExpiryRules)*

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card expiry rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card expiry rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card expiry rule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Shortening the period from 12 to 6 months**: Confirm names the cards that would expire at once or within 30 days, and whether warnings will still reach them; the confirm carries a "Recalculate existing cards" checkbox, unchecked. *(source: contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **Viewer with venue-level rights only**: The rule is tenant-scoped; read-only with "Changes apply to all venues; needs tenant product configuration rights". *(source: contracts/satellite/games.yaml#setGameCardExpiryRules)*

#### Consistency with other screens

- Match `BO-457`: Which events count as activity or recharge is set there; the basis here names them in the same words.
- Match `BO-458`: The warning days set here are the buckets' natural thresholds.
- Match `BO-480`: The reader message for an expired card ("CARD EXPIRED") is set in the output mapping.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: Standard game card expiry
  months: 6
  basis: Latest of last recharge or last activity
  warnings: 30, 7, 1 days by Email and SMS
  onExpiry: Hold for claim, 90 days
example:
  lastRecharge: 01 Mar 2026
  lastActivity: 20 Apr 2026
  expiry: 20 Oct 2026
```

#### Permissions

- `setGameCardExpiryRules` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-456` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-456`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 4: Works in Card Expiry Rule Configuration → Configure the backend rule that determines when a card expires.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-456?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-457` Last Recharge & Last Activity Tracking

**Maintain the two dates required for lifecycle calculation and show which events update them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-457 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/games-rides/last-recharge-last-activity-tracking-bo-457` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Keeps the two dates the expiry depends on (last recharge, last activity) and lets the venue decide which kinds of event reset the expiry clock. The pack flags that the source never said which activities count, so this is where the client states it. The one thing to get right: a plain table "Activity / Resets the expiry clock?" with one switch per event type, and a per-card view showing the dates and the resulting expiry.

**Known correction pending (do not draw the wrong version)**

- **The screen is one empty detail panel** Why: The pack gives a configuration table and a per-card calculation; neither is drawn. *(source: screens/P08-venue-back-office.yaml#BO-457; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No field holds the qualifying events, and the card has no last-recharge date** Why: GameCard carries lastPlayedAt only; the wallet has lastActivityAt; nothing records the last recharge or which event types count. *(source: contracts/satellite/games.yaml#/components/schemas/GameCard / contracts/satellite/wallet.yaml#getWallet; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should a balance inquiry at a balance reader or kiosk keep a card alive?** → Drawn default accepted: Off, as the pack suggests, with the switch available. *(decided by Chinmay, 2026-10-02; DEC-421 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Qualifying events**: Table with a switch per row: Recharge (POS, kiosk, app and operator top-ups listed under it), Paid game play, Bonus game play, Free game play, Prize redemption, Balance inquiry, Card/reader interaction. Defaults as the pack: all on except Balance inquiry and Card/reader interaction, which are off. *(source: screens/P08-venue-back-office.yaml#BO-457)*
- **Card (cardCode)**: Optional; with a card chosen the right panel shows its current calculation. *(source: screens/P08-venue-back-office.yaml#BO-457)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Current calculation for a card**: Last recharge 01 Sep 2026 (POS top-up, Summit Peaks POS 2), Last activity 08 Sep 2026 (Paid play, VR Racing), Expiry basis Last activity, New expiry 08 Mar 2027. Each date names the event that set it. *(source: screens/P08-venue-back-office.yaml#BO-457)*
- **Recent qualifying events**: The card's last ten events with a tick against those that moved a date. *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save qualifying events**: Greyed until a field exists (per VO-R13); the switches show the pack defaults as a draft. *(source: screens/P08-venue-back-office.yaml#BO-457)*

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The last recharge last list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the last recharge last untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No last recharge last yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the last recharge last are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A play recorded offline yesterday syncs today**: Last activity takes the play's original time, not the sync time, and expiry never moves backwards because an older event arrived late. *(source: DI-065 / contracts/satellite/games.yaml#/components/schemas/RecordPlayRequest)*
- **A refused tap**: Never counts as activity; only allowed plays and completed transactions move the date. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayTransaction)*

#### Consistency with other screens

- Match `BO-456`: The basis options there refer to these two dates by the same names.
- Match `BO-463`: Each date change appears in the card history as "Expiry recalculated" with the event that caused it.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
events:
- activity: Recharge
  resets: 'Yes'
- activity: Paid game play
  resets: 'Yes'
- activity: Bonus game play
  resets: 'Yes'
- activity: Free game play
  resets: 'Yes'
- activity: Prize redemption
  resets: 'Yes'
- activity: Balance inquiry
  resets: 'No'
card:
  card: '****4321'
  lastRecharge: 01 Sep 2026
  lastActivity: 08 Sep 2026
  newExpiry: 08 Mar 2027
```

#### Permissions

- `getGameCard` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-457` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-457`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 6: Works in Last Recharge & Last Activity Tracking → Maintain the two dates required for lifecycle calculation and show which events update them.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-457?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-458` Expiry Monitoring & Upcoming Expiration

**Identify cards approaching expiry so operators can monitor liability and customer impact.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block B · ticket #29131 (VM-BO-458) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/expiry-monitoring-upcoming-expiration-bo-458` |

**What the spec says about it.** View card and View wallet are row actions and Export a toolbar action (the board merged three actions into one label); no staff read of a game card or wallet exists (`getGameCard` is guest-only), so they wait for one (logged, CHG-SBO-005).

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): A monitoring list needs a read of cards by expiry date; setGameCardExpiryRules is the configuration write of BO-456. No read of cards by expiry exists (contract … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists game cards by expiry date with their remaining value.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The watch list of cards approaching expiry and the value on them, so the venue can see liability and the guests about to lose balance. Finance and guest services use it weekly. The one thing to get right: buckets first (today, 7, 30, 60 days, expired) with the money in each, then the cards, filtered to those that actually hold value.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- One primary button labelled "View Card / View Wallet / Export" (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The only bound operation is the expiry rule write (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should warning messages be sent from here (manual nudge) or only by the schedule in the expiry rule?** → Drawn default accepted: Schedule only; the pack defers guest communication to CRM. *(decided by Chinmay, 2026-10-02; DEC-422 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search expiry monitoring upcoming | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by balance > 0, bonus > 0, redemption credits > 0, venue, card type, expiry window — which are present is a decision the pack already made. | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Expiry window**: Bucket chips Expiring today, Within 7 days, Within 30 days, Within 60 days, Expired; one active at a time; default Within 30 days. *(source: screens/P08-venue-back-office.yaml#BO-458)*
- **Value filters**: Toggles Balance above zero (default on), Bonus above zero, Redemption credits above zero; plus Card type. Venue from the top bar. *(source: screens/P08-venue-back-office.yaml#BO-458)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Bucket tiles**: Each bucket shows card count and value (paid and bonus AED, redemption credits separately). The selected bucket is highlighted. *(source: screens/P08-venue-back-office.yaml#BO-458)*
- **Cards table**: Columns Card, Balance (AED), Bonus (AED), Redemption credits, Last activity, Expiry, Days left. Sorted by days left ascending; 0 shows "Today" in red, up to 7 in amber. Cursor paging. *(source: screens/P08-venue-back-office.yaml#BO-458)*
- **Warning status**: Per card, whether the pre-expiry warnings set on BO-456 have gone out ("30-day warning sent 15 Aug"). *(source: contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **View card, View wallet**: Open BO-455 or the wallet for the row. *(source: screens/P08-venue-back-office.yaml#BO-458)*
- **Export**: CSV of the filtered list with the same columns and the bucket in the file name. *(source: screens/P08-venue-back-office.yaml#BO-458)*

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The expiry monitoring upcoming list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the expiry monitoring upcoming untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No expiry monitoring upcoming yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the expiry monitoring upcoming are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A card in the list is recharged**: It leaves the bucket on the next refresh; the list does not keep stale expiry dates. *(source: screens/P08-venue-back-office.yaml#BO-457)*
- **Expired cards under Hold for claim**: The Expired bucket shows "Claimable until 18 Jan 2027" per card when the policy holds value for a period. *(source: contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules)*

#### Consistency with other screens

- Match `BO-454`: Bucket counts match the landing's Expiring in 30 days and Expired tiles.
- Match `BO-1163`: Value on expired cards becomes breakage in wallet finance when the policy is Transfer to breakage; use the same liability figures.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
buckets:
  today: 4 cards, AED 210
  within7: 38 cards, AED 2,140
  within30: 312 cards, AED 18,450
  within60: 655 cards, AED 39,800
  expired: 2,210 cards, AED 61,300
cards:
- card: '****1289'
  balance: AED 85.00
  bonus: AED 10.00
  redemption: 600
  lastActivity: 15 Mar 2026
  expiry: 15 Oct 2026
  daysLeft: 14
- card: '****2182'
  balance: AED 140.00
  bonus: AED 0.00
  redemption: 0
  lastActivity: 20 Mar 2026
  expiry: 20 Oct 2026
  daysLeft: 19
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-458` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-458`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 8: Works in Expiry Monitoring & Upcoming Expiration → Identify cards approaching expiry so operators can monitor liability and customer impact.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-458?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-459` Card Expiry Runtime Validation

**Show how TICVAI automatically handles a card tap when the credential is active or expired.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-459 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§CARD VALID; CARD EXPIRED) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/card-expiry-runtime-validation-bo-459` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): authoriseGameplay decides a real tap now and charges for it; a back-office check uses simulateGameplayAuthorisation, which returns the decision and trace without …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Shows, and lets an administrator test, how a tap is judged when the card is active or expired: the reader sends the credential, TICVAI checks status and calculated expiry, and answers Approve or Reject with a reason the reader displays. It exists so the development team and operators see that expiry is a backend decision. The one thing to get right: the architecture strip (Card, Reader, TICVAI, Approve or Reject, Reader display) is the hero, and testing a card here must never charge it.

**Known correction pending (do not draw the wrong version)**

- **A table titled "Every card expiry runtime" with the column "Expires 08 Mar 2027"** Why: Generated label with a sample value as a column; the screen is an explanatory flow with a test panel. *(source: screens/P08-venue-back-office.yaml#BO-459; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's reason code CARD_EXPIRED and the contract's cardExpired** Why: Same meaning, two spellings; show the plain label and the contract code only. *(source: screens/P08-venue-back-office.yaml#BO-460 / contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): authoriseGameplay is bound to a back-office test (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Form: Test a tap** (modal, opened by *Test a tap*; *Test a tap* calls `simulateGameplayAuthorisation`, *Cancel* sends nothing)

**Collects what `simulateGameplayAuthorisation` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reader `readerId` | picker: choose a reader | required | — | — | shows names, sends the id | — | `simulateGameplayAuthorisation` body |
| Card `cardId` | picker: choose a card | optional | — | — | shows names, sends the id | — | `simulateGameplayAuthorisation` body |
| Credential identifier `credentialIdentifier` | text field | optional | — | — | — | — | `simulateGameplayAuthorisation` body |
| Game `gameId` | picker: choose a game | optional | — | — | shows names, sends the id | — | `simulateGameplayAuthorisation` body |
| At `at` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `simulateGameplayAuthorisation` body |
| Guest height cm `guestHeightCm` | number field | optional | — | — | — | — | `simulateGameplayAuthorisation` body |
| Offline `offline` | toggle | optional | off | — | — | — | `simulateGameplayAuthorisation` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Card, reader, time**: Card number (or credential identifier), reader (select), time (default now). All optional except card. *(source: contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisationRequest)*

#### Outputs: what the screen shows and produces

**Shown**

**Every card expiry runtime** (data table)

| Shows | Format | Notes |
|---|---|---|
| Expires: 08 mar 2027 | text | not in the schema: `Expires: 08 Mar 2027` |

**The selected card expiry runtime** (detail panel): The pack groups this record's detail under its own headings: “Reader Tap”, “Reader sends Credential ID”, “Check Status”, “Check Calculated Expiry”, “Continue to”, “Reason Code”.

| Shows | Format | Notes |
|---|---|---|
| Expires: 08 mar 2027 | text | not in the schema: `Expires: 08 Mar 2027` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Test a tap (secondary button) | `simulateGameplayAuthorisation` POST `/gameplay-authorisations/simulate` | GameplayAuthorisationRequest | GameplayAuthorisation | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Architecture strip**: Card tap, Reader sends credential id, TICVAI retrieves card, Check status, Check calculated expiry, then two branches: CARD VALID "Expires 08 Mar 2027" continuing to Entitlement, Pricing, Balance, Gameplay authorisation; CARD EXPIRED, Reject with reason CARD_EXPIRED, reader shows "CARD EXPIRED". *(source: screens/P08-venue-back-office.yaml#BO-458 / screens/P08-venue-back-office.yaml#BO-460 / screens/P08-venue-back-office.yaml#BO-463)*
- **Test result**: The decision, the guest message the reader would show (in English and Arabic), and the trace with the status and expiry checks highlighted. Reason codes shown in plain words with the code beside ("Card expired, cardExpired"). *(source: contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation)*
- **Recent expired-card refusals**: Below, the last refusals at this venue for expired or blocked cards, with reader and time, linking to the decision trace (BO-467). *(source: contracts/satellite/games.yaml#listGameplayTransactions / DI-881)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test a tap**: Runs the simulation and shows the outcome; nothing is deducted and no play is recorded. *(source: contracts/satellite/games.yaml#simulateGameplayAuthorisation)*

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card expiry runtime list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card expiry runtime untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card expiry runtime yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card expiry runtime are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **The reader is offline and its package was built before the card expired**: The reader may approve from its package; the play is accepted on sync and flagged. Show this branch as a dashed path "Offline decision". *(source: contracts/satellite/games.yaml#/components/schemas/RecordPlayRequest / R106)*
- **Card expires at midnight during the evening**: Expiry is compared in venue local time; a card expiring today still plays until the end of the venue day. *(source: designer default)*

#### Consistency with other screens

- Match `BO-467`: Same trace component; this screen focuses the first three checks.
- Match `BO-480`: The CARD EXPIRED text and red light come from the output mapping there.
- Match `BO-412`: The real-time tap validation screen on board 2 shows the same reader responses.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
valid:
  card: '****4321'
  reader: R-014 VR Racing
  result: CARD VALID
  expires: 08 Mar 2027
expired:
  card: '****6215'
  reader: R-007 Bumper Cars
  result: REJECT
  reason: cardExpired
  readerShows: CARD EXPIRED
```

#### Permissions

- `simulateGameplayAuthorisation` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-459` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-459`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 10: Works in Card Expiry Runtime Validation → Show how TICVAI automatically handles a card tap when the credential is active or expired.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-459?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Test a tap.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-460` Card Block, Suspend & Reactivation Control

**Allow authorized operators to disable a lost, suspicious or invalid card without affecting the underlying wallet record.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-460 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Blocked Card Tap) and no metric row |
| Offline | online only |
| Opens with | `cardId` (navigation) |
| Route | `/games-rides/card-block-suspend-reactivation-control-bo-460` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where an authorised operator blocks a lost, stolen or suspicious card, suspends it, or reactivates it, always with a reason and always without touching the wallet. The one thing to get right: the confirmation says exactly what stops working and what is protected ("Card ****4321 stops working at every reader; AED 125.00 and 2,450 credits stay on the wallet") and when offline readers will learn of it.

**Known correction pending (do not draw the wrong version)**

- **Card status has no Suspended state** Why: setGameCardLifecycle offers suspend but GameCard.status is active, blocked, expired, transferred; a suspended card has nowhere to land. *(source: contracts/satellite/games.yaml#setGameCardLifecycle / contracts/satellite/games.yaml#/components/schemas/GameCard; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Two operations write the same block and unblock** Why: The card state machine moves active to blocked and back through wallet adjustGameCard, while this screen uses games setGameCardLifecycle; one must own the transition. *(source: contracts/satellite/wallet.yaml#adjustGameCard / contracts/satellite/games.yaml#setGameCardLifecycle; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The lifecycle path is keyed by cardId but a card is keyed by cardCode** Why: GameCard has no id property; the screen carries cardCode from the landing, so it cannot call the path. *(source: contracts/satellite/games.yaml#setGameCardLifecycle / contracts/satellite/games.yaml#/components/schemas/GameCard; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Suspend is drawn destructive and Block primary; table columns are the pack's flow arrows** Why: Block is the destructive action (VO-R16); "Reader sends credential" and the other arrows are a diagram, not columns. *(source: screens/P08-venue-back-office.yaml#BO-460; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The reason is free text in the request** Why: The pack gives a closed list of reasons; the request's reason should be that enum so analysis can count them. *(source: screens/P08-venue-back-office.yaml#BO-461 / contracts/satellite/games.yaml#setGameCardLifecycle; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How does Suspend differ from Block (temporary with an end date, no guest-visible message, automatic review)?** → Drawn default accepted: Suspend = temporary hold with an optional "until" date; Block = lost, stolen or fraud. *(decided by Chinmay, 2026-10-02; DEC-423 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Card**: Arrives from the landing, a profile or a search; shown read-only with status and balances. *(source: screens/P08-venue-back-office.yaml#BO-460)*
- **Reason code**: Required select of the pack's set - Lost card, Stolen card, Customer request, Fraud or suspicious activity, Operational issue. Never free text. *(source: screens/P08-venue-back-office.yaml#BO-461)*
- **Comment**: Optional free text, max 500, required when the reason is Operational issue or Fraud. *(source: screens/P08-venue-back-office.yaml#BO-460 / designer default)*
- **Operator, Effective immediately**: Not inputs. The operator is the signed-in person (per ADR-0002) and a block always takes effect at once; show both as text in the confirmation. *(source: ADR-0002 / contracts/satellite/games.yaml#setGameCardLifecycle)*

#### Outputs: what the screen shows and produces

**Shown**

**Every card block suspend** (data table)

| Shows | Format | Notes |
|---|---|---|
| → reader sends credential | text | not in the schema: `→ Reader sends credential` |
| → TICVAI recognizes blocked status | text | not in the schema: `→ TICVAI recognizes blocked status` |
| → transaction rejected | text | not in the schema: `→ Transaction rejected` |
| → wallet remains protected | text | not in the schema: `→ Wallet remains protected` |

**The selected card block suspend** (detail panel): The pack groups this record's detail under its own headings: “Block Form”, “Require”.

| Shows | Format | Notes |
|---|---|---|
| → reader sends credential | text | not in the schema: `→ Reader sends credential` |
| → TICVAI recognizes blocked status | text | not in the schema: `→ TICVAI recognizes blocked status` |
| → transaction rejected | text | not in the schema: `→ Transaction rejected` |
| → wallet remains protected | text | not in the schema: `→ Wallet remains protected` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Block (primary button) | navigation or local | — | — | — | — |
| Suspend (destructive button) | navigation or local | — | — | — | — |
| Reactivate (secondary button) | navigation or local | — | — | — | — |
| Replace Card (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Current state**: Status chip, since when and by whom ("Blocked 17 Apr 2026 by Omar Haddad, Lost card"). *(source: screens/P08-venue-back-office.yaml#BO-461)*
- **Blocked card behaviour**: A small strip - Reader sends credential, TICVAI sees Blocked, Tap rejected, Wallet protected. *(source: screens/P08-venue-back-office.yaml#BO-461)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Block**: Destructive style; confirmation per VO-R16 names the card, the value protected and the reach ("Online readers refuse it now; offline readers after their next configuration deployment"). *(source: contracts/satellite/games.yaml#setGameCardLifecycle / contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Suspend**: Same confirmation, worded as temporary; Suspend is a temporary hold with an optional "until" date, Block is for lost, stolen or fraud. *(source: contracts/satellite/games.yaml#setGameCardLifecycle / DI-880 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **Reactivate**: Needs the reactivation permission, a reason, and is audited; disabled for expired or replaced cards with "Expired and replaced cards cannot be reactivated". *(source: screens/P08-venue-back-office.yaml#BO-461 / contracts/satellite/games.yaml#setGameCardLifecycle)*
- **Replace card**: Opens BO-461 with this card as the old card. *(source: screens/P08-venue-back-office.yaml#BO-460)*

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

**What opens over it**

- confirmDialog *Suspend*: **Suspend on a card block suspend is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card block suspend list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card block suspend untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card block suspend yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card block suspend are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is not a legal move from the card's current status. `expired` and `transferred` are terminal (states/game-card.yaml), so nothing reactivates, blocks … |

#### Edge cases to draw

- **Blocking a card while a guest is mid-game**: The current play finishes; the next tap is refused with "Card blocked, please see guest services". *(source: contracts/satellite/games.yaml#/components/schemas/GameplayAuthorisation)*
- **Action not legal from the current status**: The 409 is shown as a sentence ("This card is already replaced"), and the button that caused it is disabled afterwards. *(source: contracts/satellite/games.yaml#setGameCardLifecycle)*
- **Operator without card-management rights**: Buttons disabled with the permission named (VO-R08). *(source: contracts/satellite/games.yaml#setGameCardLifecycle)*

#### Consistency with other screens

- Match `BO-461`: Replacement blocks the old card as its first step with the same reason list.
- Match `BO-480`: The reader's blocked-card message and light come from the output mapping.
- Match `BO-463`: Every block, suspend and reactivation appears in the card's history with reason and operator.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
card:
  card: '****4321'
  guest: Khalid Al Zaabi
  status: Active
  paid: AED 125.00
  credits: 2450
block:
  reason: Lost card
  comment: Guest reported loss at guest services, ID checked
  operator: Fatima Al Hashimi
```

#### Permissions

- `setGameCardLifecycle` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-460` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-460`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 12: Works in Card Block, Suspend & Reactivation Control → Allow authorized operators to disable a lost, suspicious or invalid card without affecting the underlying wallet record.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-460?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Block, Suspend, Reactivate, Replace Card.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-461` Card Replacement & Wallet Relinking

**Allow a damaged, lost or replaced physical card to be substituted while retaining the customer's wallet and entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-461 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `WALLET_OPERATE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Old Card) and no metric row |
| Offline | online only |
| Opens with | `cardId` (navigation) |
| Route | `/games-rides/card-replacement-wallet-relinking-bo-461` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Swaps a damaged, lost or faulty card for a new one while the guest keeps everything: paid balance, bonus, redemption credits, entitlements and history. The client's own wording (DI-538) is: identify the guest by phone or ID, find the original purchase, move the balance to the replacement. The one thing to get right: one guided flow with one final action, not three separate operations the operator has to chain.

**Known correction pending (do not draw the wrong version)**

- **Three operations can replace a card** Why: games transferGameCard moves balances by card code, games setGameCardLifecycle has action replace with a replacementCardId, and wallet linkWalletCredential records replacedByCredentialId; the screen binds the last two and not the first. One flow, one owner. *(source: contracts/satellite/games.yaml#transferGameCard / contracts/satellite/games.yaml#setGameCardLifecycle / contracts/satellite/wallet.yaml#linkWalletCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The table "Every card replacement wallet" with columns "4321" and an arrow** Why: The pack's flow example parsed as columns; the screen is a stepper. *(source: screens/P08-venue-back-office.yaml#BO-461; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are entitlements held on the card or the wallet, and do they move with the balance?** → Drawn default accepted: Draw them in the "What moves" list as preserved, per the pack. *(decided by Chinmay, 2026-10-02; DEC-424 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Is a replacement-card fee charged for lost (not damaged) cards?** → Drawn default accepted: No fee step drawn; leave space in the summary for a fee line. *(decided by Chinmay, 2026-10-02; DEC-425 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Find the guest or card**: Step 1. Card number, or guest phone or ID number (DI-538); shows the guest's cards with status and balances and the original purchase that issued the card. *(source: screens/P08-venue-back-office.yaml#BO-461 / DI-538)*
- **Replacement reason**: Required select - Damaged, Lost, Faulty, Guest request, Upgrade. *(source: contracts/satellite/games.yaml#transferGameCard)*
- **Replacement card**: Step 2. Tap or scan the new card or wristband, or issue a digital one. Shows "New card ****9875, empty, active" when acceptable. *(source: screens/P08-venue-back-office.yaml#BO-461 / contracts/satellite/games.yaml#transferGameCard)*
- **Operator, date and time**: Not inputs; the signed-in person and the server time, shown on the summary. *(source: ADR-0002)*

#### Outputs: what the screen shows and produces

**Shown**

**Every card replacement wallet** (data table)

| Shows | Format | Notes |
|---|---|---|
| 4321 | text | not in the schema: `4321` |
| ↓ | text | not in the schema: `↓` |

**The selected card replacement wallet** (detail panel): The pack groups this record's detail under its own headings: “Block Old Credential”, “Issue / Scan New Credential”, “Link Existing Wallet”, “Preserve”, “Page 70 of 105”.

| Shows | Format | Notes |
|---|---|---|
| 4321 | text | not in the schema: `4321` |
| ↓ | text | not in the schema: `↓` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **What moves**: Before confirming, a checklist of what is preserved with values - Paid balance AED 125.00, Bonus AED 25.00, Redemption credits 2,450, Entitlements (All Games Pass), Transaction history. Balances move whole; there is no partial transfer. *(source: screens/P08-venue-back-office.yaml#BO-461 / screens/P08-venue-back-office.yaml#BO-462 / contracts/satellite/games.yaml#transferGameCard)*
- **Result**: "Old card ****4321 REPLACED, no longer works" and "New card ****9875 ACTIVE", side by side, with the history reference. *(source: screens/P08-venue-back-office.yaml#BO-462)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Replace card**: One action that blocks the old credential, moves the balances and links the new credential to the same wallet. Confirmation per VO-R16 states the old card stops working immediately and cannot be reactivated. *(source: contracts/satellite/games.yaml#transferGameCard / contracts/satellite/wallet.yaml#linkWalletCredential)*

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card replacement wallet list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card replacement wallet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card replacement wallet yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card replacement wallet are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already bound to another wallet; 409 The action is not a legal move from the card's current status. `expired` and `transferred` are terminal (states/game-card.yaml), so nothing reactivates, blocks … |

#### Edge cases to draw

- **The new card already carries a balance or is not active**: Refused at step 2 with "This card already holds AED 20.00; use an empty card". *(source: contracts/satellite/games.yaml#transferGameCard)*
- **The new credential is already linked to another wallet**: Refused with "This wristband belongs to another guest"; never relinked silently. *(source: contracts/satellite/wallet.yaml#linkWalletCredential)*
- **The old card is expired**: Replacement is not offered (expired is terminal); point to the expiry policy (claim period) instead. *(source: contracts/satellite/games.yaml#setGameCardLifecycle / contracts/satellite/games.yaml#/components/schemas/GameCardExpiryRules)*
- **Offline readers still hold the old card as valid**: Summary warns "Offline readers refuse the old card after their next deployment". *(source: contracts/satellite/games.yaml#deployReaderConfiguration)*

#### Consistency with other screens

- Match `BO-460`: The old card's block uses the same confirmation language.
- Match `BO-179`: Access control's media swap (DI-637) is the same idea for admission media; use the same stepper and words (Old media, New media, What moves).
- Match `POS-002`: The till also transfers cards; the reason list and result wording must match.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
replacement:
  guest: Khalid Al Zaabi, +971 50 123 4567
  oldCard: '****4321'
  newCard: '****9875'
  reason: Damaged
  operator: Rahul Menon
preserved:
  paid: AED 125.00
  bonus: AED 25.00
  redemptionCredits: 2450
  entitlements: All Games Pass
```

#### Permissions

- `setGameCardLifecycle` → `PRODUCT_CONFIGURE` (configure) · staff
- `linkWalletCredential` → `WALLET_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*
- Lost wristband/card: operations identify the guest (phone number or ID), locate the original transaction and transfer the balance to a replacement wristband/card. *(client request · MoM 27 Aug 2026, 4.10 Lost-media recovery · DI-538)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-461` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-461`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 14: Works in Card Replacement & Wallet Relinking → Allow a damaged, lost or replaced physical card to be substituted while retaining the customer's wallet and entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-461?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `WALLET_OPERATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-462` Customer Balance & Credential Status View

**Provide the backend configuration/view that supports balance-check readers, operator kiosks and self-service kiosks. The source requires a dedicated reader for checking customer balance and also requires wallet credits to be viewable at operator and self-service kiosks.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-462 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card Information) and no metric row |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/games-rides/customer-balance-credential-status-view-bo-462` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Defines what card and wallet information the backend presents on each guest-facing channel (balance reader, self-service kiosk, operator kiosk) and previews it. The pack is explicit that this is not another reader-configuration screen: board 2 configures the reader device; this configures the balance and status service the reader or kiosk asks for. The one thing to get right: a channel-by-data matrix plus a customer-view preview, not a reader form.

**Known correction pending (do not draw the wrong version)**

- **Table columns "Status Active", "Card Expiry 08 Mar 2027", "Bonus Expiry 30 Sep 2026"** Why: Sample values used as column labels in a generated "Every customer balance credential" table. *(source: screens/P08-venue-back-office.yaml#BO-462; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only a card read is bound; no per-channel visibility can be saved** Why: Reader displayRules (showBalance, showPrice) are per reader and the kiosk config is per kiosk; nothing holds which data each channel type shows. *(source: contracts/satellite/games.yaml#/components/schemas/Reader / contracts/satellite/games.yaml#/components/schemas/GameKioskConfig; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Visibility matrix**: Rows Paid balance, Bonus balance, Bonus expiry, Redemption credits, Free games, Entitlements, Card status, Card expiry; columns Balance reader, Self-service kiosk, Operator kiosk; a tick per cell. Defaults all on for kiosks; balance reader shows Paid, Bonus and Free games only (a small screen). *(source: screens/P08-venue-back-office.yaml#BO-462 / screens/P08-venue-back-office.yaml#BO-463)*
- **Preview card**: Optional card number to fill the preview with real values; otherwise the sample card. *(source: contracts/satellite/games.yaml#getGameCard)*

#### Outputs: what the screen shows and produces

**Shown**

**Every customer balance credential** (data table)

| Shows | Format | Notes |
|---|---|---|
| Status: active | text | not in the schema: `Status: Active` |
| Card expiry: 08 mar 2027 | text | not in the schema: `Card Expiry: 08 Mar 2027` |
| Bonus expiry: 30 sep 2026 | text | not in the schema: `Bonus Expiry: 30 Sep 2026` |

**The selected customer balance credential** (detail panel): The pack groups this record's detail under its own headings: “Customer View”, “Redemption Credits”, “Free Games”, “Entitlements”.

| Shows | Format | Notes |
|---|---|---|
| Status: active | text | not in the schema: `Status: Active` |
| Card expiry: 08 mar 2027 | text | not in the schema: `Card Expiry: 08 Mar 2027` |
| Bonus expiry: 30 sep 2026 | text | not in the schema: `Bonus Expiry: 30 Sep 2026` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Customer view preview**: Per channel tab, the layout the guest sees - Card ****4321, Paid balance AED 125, Bonus AED 25, Redemption credits 2,450, Free games 2, Entitlements (All Games Pass; VR Racing x2), Status Active, Card expiry 08 Mar 2027, Bonus expiry 30 Sep 2026. Tenant brand with "Powered by TICVAI" (VO-R15). *(source: screens/P08-venue-back-office.yaml#BO-462)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save channel visibility**: Greyed until a field exists (per VO-R13); the preview still works. *(source: DI-653)*

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer balance credential list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer balance credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer balance credential yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer balance credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Balance reader is a public device**: Never shows the guest's name; masked card only. *(source: designer default)*
- **Card read during a network blip**: The reader path is offline-capable and may be stale; channels show "Balance as of 10:41" when served from cache. *(source: contracts/satellite/games.yaml#getGameCard / MATRIX 10.2.20)*

#### Consistency with other screens

- Match `BO-413`: Board 2's balance-check reader configures the device; this screen configures the data. Link both ways and do not repeat device settings here.
- Match `BO-485`: A kiosk's enabled functions there decide which of these data items its journey can reach.
- Match `BO-455`: Same values, same order as the card profile.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
- item: Paid balance
  balanceReader: 'Yes'
  selfServiceKiosk: 'Yes'
  operatorKiosk: 'Yes'
- item: Bonus balance
  balanceReader: 'Yes'
  selfServiceKiosk: 'Yes'
  operatorKiosk: 'Yes'
- item: Redemption credits
  balanceReader: 'No'
  selfServiceKiosk: 'Yes'
  operatorKiosk: 'Yes'
- item: Card expiry
  balanceReader: 'No'
  selfServiceKiosk: 'Yes'
  operatorKiosk: 'Yes'
```

#### Permissions

- `getGameCard` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-462` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-462`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 16: Works in Customer Balance & Credential Status View → Provide the backend configuration/view that supports balance-check readers, operator kiosks and self-service kiosks. The source requires a dedicated reader for checking customer balance and also …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-462?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-463` Card Lifecycle Audit & History

**Maintain full traceability of card lifecycle changes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-463 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card Issued; Card Blocked) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/card-lifecycle-audit-history-bo-463` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The card's history: every lifecycle change with what caused it, who or what did it, and on which device. Used to answer complaints ("my card stopped working") and for audit. The one thing to get right: a single-card timeline of lifecycle events (issued, recharged, expiry recalculated, blocked, replaced), with the hundreds of plays collapsed so they do not bury the events that matter.

**Known correction pending (do not draw the wrong version)**

- **listGameplayTransactions is the only read** Why: It returns taps, not lifecycle events (issued, recharged, blocked, replaced), and it cannot be filtered by card. *(source: contracts/satellite/games.yaml#listGameplayTransactions; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's example timeline puts "15 Oct 2026 Expiry recalculated" between April events** Why: 15 Oct 2026 is the new expiry date, not the event date; the recalculation happened on 15 Apr 2026. Sample data above uses the corrected date. *(source: screens/P08-venue-back-office.yaml#BO-463; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table columns "05 Mar 2026" and "18 Apr 2026"** Why: Sample dates used as column labels in "Every card lifecycle audit". *(source: screens/P08-venue-back-office.yaml#BO-463; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Card**: Card number or guest search; the timeline is per card. *(source: screens/P08-venue-back-office.yaml#BO-463)*
- **Event types**: Chips for the pack's events - Card issued, Recharge, Activity, Expiry recalculated, Expired, Blocked, Reactivated, Replaced, Wallet relinked. Activity off by default. *(source: screens/P08-venue-back-office.yaml#BO-463)*

#### Outputs: what the screen shows and produces

**Shown**

**Every card lifecycle audit** (data table)

| Shows | Format | Notes |
|---|---|---|
| 05 mar 2026 | text | not in the schema: `05 Mar 2026` |
| 18 apr 2026 | text | not in the schema: `18 Apr 2026` |

**The selected card lifecycle audit** (detail panel): The pack groups this record's detail under its own headings: “AED 100 Recharge”, “Game Played”, “Expiry Recalculated”, “Events”, “Page 72 of 105”, “Important architecture for the design”.

| Shows | Format | Notes |
|---|---|---|
| 05 mar 2026 | text | not in the schema: `05 Mar 2026` |
| 18 apr 2026 | text | not in the schema: `18 Apr 2026` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Timeline**: Oldest first, one row per event - date and time, event, previous to new status, operator or system, reason, source device, transaction reference (link). Consecutive plays collapse to "Played 37 times, 15 Apr - 16 Apr" with expand. *(source: screens/P08-venue-back-office.yaml#BO-463)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **View event, View transaction**: Opens the event detail or the originating transaction (sale, top-up, play, redemption). *(source: screens/P08-venue-back-office.yaml#BO-463)*
- **Export audit**: CSV of the card's full history with every audit field. *(source: screens/P08-venue-back-office.yaml#BO-463)*

**Data it reads**: `listGameplayTransactions` (onLoad, Card lifecycle history)

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card lifecycle audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card lifecycle audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card lifecycle audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card lifecycle audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A replaced card**: The timeline continues across the replacement with a divider "Continued on ****9875", so the guest's story is one history. *(source: screens/P08-venue-back-office.yaml#BO-463 / contracts/satellite/games.yaml#transferGameCard)*
- **System events**: Expiry recalculations and expiry show "System" as the actor with the rule that applied. *(source: screens/P08-venue-back-office.yaml#BO-463)*

#### Consistency with other screens

- Match `BO-403`: The attraction audit uses the same timeline component.
- Match `BO-460`: Reasons appear in the same words as the block form.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
timeline:
- at: 01 Mar 2026 11:02
  event: Card issued
  by: Summit Peaks POS 2, Maria Santos
- at: 05 Mar 2026 14:20
  event: Recharge AED 100.00
  by: Kiosk KSK-01
- at: 15 Apr 2026 16:45
  event: Game played (VR Racing)
  by: R-014
- at: 15 Apr 2026 16:45
  event: Expiry recalculated to 15 Oct 2026
  by: System
- at: 17 Apr 2026 10:12
  event: Card blocked, Lost card
  by: Fatima Al Hashimi
- at: 18 Apr 2026 09:30
  event: Replaced by ****9875
  by: Rahul Menon
```

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-463` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-463`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 18: Works in Card Lifecycle Audit & History → Maintain full traceability of card lifecycle changes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-463?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getGameCard": {"method":"GET","path":"/game-cards/{cardCode}","contract":"games","summary":"Read a card's balances","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameCard"},
"linkWalletCredential": {"method":"POST","path":"/wallet-credentials","contract":"wallet","summary":"Bind a wristband, card or device to a wallet","permission":"WALLET_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WalletCredential","responds":"WalletCredential"},
"listGameplayTransactions": {"method":"GET","path":"/gameplay-transactions","contract":"games","summary":"Taps, decisions and what they cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"readerId","in":"query","required":null},{"name":"outcome","in":"query","required":null}],"requestBody":null,"responds":"GameplayTransaction"},
"setGameCardExpiryRules": {"method":"PUT","path":"/game-card-expiry-rules","contract":"games","summary":"When a card lapses, and what warns the guest first","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameCardExpiryRules","responds":"GameCardExpiryRules"},
"setGameCardLifecycle": {"method":"POST","path":"/game-cards/{cardId}/lifecycle","contract":"games","summary":"Block, suspend, reactivate, replace or expire a card","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GameCard"},
"simulateGameplayAuthorisation": {"method":"POST","path":"/gameplay-authorisations/simulate","contract":"games","summary":"What would happen if this card tapped this reader","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameplayAuthorisationRequest","responds":"GameplayAuthorisation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"GameCard": {"x-ticvai-persistence":"games.card","type":"object","required":["cardCode","venueId","credits","bonusCredits","points","status","issuedAt"],"properties":{"cardCode":{"type":"string","description":"**A pre-printed card keeps the code printed on it. A generated code** (a digital card, or a card issued with no printed code) **is the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Each till holds a reserved range of that sequence, so a card issued offline takes its code at once. Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"credits":{"type":"integer","description":"Bought with money. Buys plays."},"bonusCredits":{"type":"integer","description":"From a promotion. Typically non-refundable and spent before paid credits.\n"},"points":{"type":"integer","description":"Won by playing. Buys prizes. **Not interchangeable with credits** — a guest who wins should not simply be able to play more.\n"},"status":{"type":"string","enum":["active","blocked","expired","transferred"]},"blockedReason":{"type":"string","nullable":true},"transferredToCardCode":{"type":"string","nullable":true},"lastPlayedAt":{"type":"string","format":"date-time","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**The card's own id** (4 October 2026, CHG-FXC-006): the `{cardId}` of `setGameCardLifecycle`, which had no column to match, and the `id` of the Wallet view `wallet.loadGameCredits` and `wallet.adjustGameCard` return for a card with no wallet."},"walletId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Where the card's credits are held** (4 October 2026, CHG-FXC-006). Set when the card is registered to a guest who has a wallet: credits loaded to it are wallet credit lots. Null for an anonymous card, whose credits are held on the card row itself (`credits`, `bonusCredits`)."}}},
"GameCardExpiryRules": {"type":"object","x-ticvai-persistence":"games.card_expiry_rules","description":"Boards 7.3 to 7.6. **Measured from last activity, and the warning is part of the rule.**\n","properties":{"basis":{"type":"string","enum":["fromIssue","fromLastActivity","fromLastRecharge"],"default":"fromLastActivity"},"validityMonths":{"type":"integer"},"warnBeforeDays":{"type":"array","items":{"type":"integer"},"description":"**Expiring a balance with no notice is what ends up on social media.**"},"warningChannels":{"type":"array","items":{"type":"string"}},"extendOnRecharge":{"type":"boolean","default":true},"onExpiry":{"type":"string","enum":["forfeit","holdForClaim","transferToBreakage"],"default":"holdForClaim"},"holdForClaimDays":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"GameplayAuthorisation": {"type":"object","x-ticvai-persistence":"games.authorisation","description":"Board 4.9. **The refusal reason is the product.**","properties":{"id":{"type":"string","format":"uuid"},"decision":{"type":"string","enum":["allow","refuse"]},"reason":{"type":"string","nullable":true,"enum":["ok","cardNotFound","cardExpired","cardBlocked","retapTooSoon","heightRestriction","ageRestriction","insufficientFunds","entitlementExhausted","entitlementNotValidHere","cooldownActive","dailyCapReached","readerNotConfigured","gameUnavailable"]},"guestMessage":{"type":"string","nullable":true,"description":"***\"No plays left on your pass\"* rather than *\"Declined\"*.** One is a guest who understands; the other is a member of staff walking over.\n"},"chargedFrom":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementId":{"type":"string","format":"uuid","nullable":true},"remainingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"remainingPlays":{"type":"integer","nullable":true},"trace":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string"},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"decidedOffline":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"GameplayAuthorisationRequest": {"type":"object","required":["readerId"],"properties":{"readerId":{"type":"string","format":"uuid"},"cardId":{"type":"string","format":"uuid","nullable":true},"credentialIdentifier":{"type":"string","nullable":true},"gameId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time","nullable":true},"guestHeightCm":{"type":"integer","nullable":true},"offline":{"type":"boolean","default":false}}},
"GameplayTransaction": {"type":"object","x-ticvai-persistence":"games.gameplay_transaction","description":"Boards 8.2 and 8.5. **The refused ones are the valuable half.**","properties":{"id":{"type":"string","format":"uuid"},"readerId":{"type":"string","format":"uuid"},"gameId":{"type":"string","format":"uuid","nullable":true},"cardId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["allowed","refused","reversed"]},"reason":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargedFrom":{"type":"string","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"ticketsEarned":{"type":"integer","nullable":true},"decidedOffline":{"type":"boolean","default":false},"syncedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"WalletCredential": {"type":"object","x-ticvai-persistence":"wallet.credential","description":"Boards 6.4 and 6.5. **A credential is not the wallet** — a lost wristband is relinked, not refunded.\n","required":["walletId","kind","identifier"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["card","wristband","nfc","rfid","qr","mobileApp","digitalKey"]},"identifier":{"type":"string"},"linkedAt":{"type":"string","format":"date-time"},"unlinkedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","lost","replaced","blocked","expired"]},"replacedByCredentialId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}}
}
```
