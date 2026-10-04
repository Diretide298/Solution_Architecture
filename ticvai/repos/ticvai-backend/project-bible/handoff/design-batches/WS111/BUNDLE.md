# WS111 — ACCREDITATION board 4

**9 screens · 10 operations · 6 schemas · 3 permissions**

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
  `ACCREDITATION_CONFIGURE, ACCREDITATION_ISSUE, ACCREDITATION_VIEW`. A control nobody can use must say so,
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
| `BO-644` | Credential Issuance Command Center | D | 0 | 41 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `BO-645` | Credential Generation Workspace | D | 14 | 0 | 6 | 4 | 1 | 0 | — | notStarted (—) |
| `BO-646` | Credential Media Configuration | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-647` | Badge Template Designer | D | 0 | 11 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-648` | Badge Printing & Print Queue | D | 9 | 10 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-649` | Digital & Mobile Credential Management | D | 0 | 13 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-650` | NFC & RFID Credential Encoding | D | 2 | 31 | 6 | 10 | 0 | 0 | — | notStarted (—) |
| `BO-651` | Credential Activation & Delivery | D | 0 | 13 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-653` | Credential Registry & Credential History | D | 0 | 25 | 6 | 3 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-644, BO-645, BO-646, BO-647, BO-648, BO-649, BO-651, BO-653 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-644` Credential Issuance Command Center

**Central operational dashboard for accreditation credential issuance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-644 |
| Who uses it | venue staff holding `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-issuance-command-center-bo-644` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): listCredentialGenerationIssuance is the guest ticket-media generation monitor; accreditation credentials live in the accreditation contract (design-notes …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The hub of the accreditation credential board (Accreditation board 4): real-time counts of approved applications awaiting a credential, credentials generated, awaiting printing, printed, awaiting collection, digital credentials delivered, active, failed issuance, replacement requests and revoked, with filters and quick actions (Issue credential, Print queue, Bulk issue, Replace credential, Credential search) and the board's screens. The one thing to get right: these are accreditation badges and digital credentials for people (media, contractors, partners), not guest ticket media - and issuance is blocked until the accreditation is approved.

**Known correction pending (do not draw the wrong version)**

- **Content region is an empty table and the gap says the pack gives nothing to draw** Why: The pack lists ten counts, seven filters and five quick actions for this screen. *(source: screens/P08-venue-back-office.yaml#BO-644 / screens/P08-venue-back-office.yaml#BO-645; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The board's "Credential Replacement & Reissue" exit goes to BO-027 (Reissue & Media Replacement, orders)** Why: BO-027 replaces guest ticket media; accreditation replacement is replaceAccreditationCredential and needs its own screen on this board. *(source: screens/P08-venue-back-office.yaml#BO-644 / contracts/satellite/accreditation.yaml#replaceAccreditationCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Placed in process-module Admission & Access Control** Why: It is the accreditation board's hub (Accreditation module). *(source: screens/P08-venue-back-office.yaml#BO-644; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Bound to listCredentialGenerationIssuance, the guest ticket-media generation monitor (CHG-WIR-001); The counts have no operation (no summary of credentials by issuance status) (CHG-WIR-001); The accreditation operations that should feed the board exist but no Board 4 hub reads them (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationCredentials` ?holderId |
| Status | text field | — | — | `listAccreditationCredentials` ?status |
| Programme | picker: choose a programme | — | — | `listAccreditationHolders` ?programmeId |
| Organisation | picker: choose an organisation | — | — | `listAccreditationHolders` ?organisationId |
| Status | text field | — | — | `listAccreditationHolders` ?status |
| Expiring within days | number field (days) | — | — | `listAccreditationHolders` ?expiringWithinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Event, Venue (switcher), Accreditation programme, Category (Media, Corporate, Contractor...), Organisation, Credential type (Printed badge, QR, Mobile, NFC card, RFID card, Wristband), Issuance status. *(source: screens/P08-venue-back-office.yaml#BO-645 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential)*
- **Credential search**: Holder name, accreditation id, credential serial or encoded identifier; opens BO-653 with the result. *(source: screens/P08-venue-back-office.yaml#BO-645 / contracts/satellite/accreditation.yaml#listAccreditationCredentials)*

#### Outputs: what the screen shows and produces

**Shown**

**Credentials** (data table, from `listAccreditationCredentials`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Holder | the name it points at, never the id | — |
| Kind | chip: Printed badge, Mobile credential, QR, NFC card, RFID card, Wristband | — |
| Symbology | chip: QR, Data matrix, Pdf417, Aztec, Code128, NFC ndef… | 12.1.22. How `encodedIdentifier` is carried, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a … |
| Serial number | text | — |
| Encoded identifier | text | — |
| Badge template | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Issued by | the name it points at, never the id | — |
| Activated at | 1 Oct 2026, 14:30 | — |
| Status | chip: Pending print, Issued, Active, Lost, Replaced, Revoked… | — |
| Replaces credential | the name it points at, never the id | — |
| Replacement count | 1,234 | — |

**Holders** (data table, from `listAccreditationHolders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Accreditation number | text | — |
| Full name | text | — |
| Photo image | the image or video | — |
| Date of birth | 1 Oct 2026 | — |
| Nationality | text | — |
| Email | email, tap to write | 12.1.16. |
| Phone | +971 50 123 4567 | 12.1.16. |
| Identity document verified | yes / no (icon or chip) | — |
| Organisation | the name it points at, never the id | — |
| Affiliation role | text | — |
| Programme | the name it points at, never the id | — |
| Category code | text | — |
| Status | chip: Active, Suspended, Revoked, Expired, Archived | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Completeness percent | 1,234 | — |

**Print queue** (data table, from `listBadgePrintJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Credentials | list or chips (count when long) | — |
| Printer device | the name it points at, never the id | — |
| Queued at | 1 Oct 2026, 14:30 | — |
| Status | chip: Queued, Printing, Completed, Partially failed, Failed | — |
| Printed | 1,234 | — |
| Failed | 1,234 | — |
| Failures | list or chips (count when long) | — |
| Credential | the name it points at, never the id | — |
| Reason | text | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Ten tiles per VO-R02 in issuance order - Awaiting issuance, Generated, Awaiting printing, Printed, Awaiting collection, Digital delivered, Active - then problems Failed issuance, Replacement requests, Revoked (red/amber when non-zero). Each opens the matching board screen filtered. *(source: screens/P08-venue-back-office.yaml#BO-644 / screens/P08-venue-back-office.yaml#BO-645)*
- **Work queue**: Title "Credentials to issue". Approved holders without a credential first (holder, photo thumbnail, category, organisation, event, approved on), then failed issuance; each row's primary action is Issue. *(source: contracts/satellite/accreditation.yaml#listAccreditationHolders / contracts/satellite/accreditation.yaml#listAccreditationCredentials)*
- **Board tiles**: Generation workspace (BO-645), Media configuration (BO-646), Badge designer (BO-647), Printing and print queue (BO-648), Digital and mobile (BO-649), NFC/RFID encoding (BO-650), Activation and delivery (BO-651), Replacement and reissue, Registry and history (BO-653). *(source: screens/P08-venue-back-office.yaml#BO-644 / DI-653)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Issue credential**: Opens BO-645 with the holder; refused for a holder whose accreditation is not approved ("Approval not complete"). *(source: screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#issueAccreditationCredential)*
- **Print queue / Bulk issue**: Print queue opens BO-648; Bulk issue issues credentials for a filtered set of approved holders (no bulk operation; draw disabled "Not available yet"). *(source: screens/P08-venue-back-office.yaml#BO-645 / contracts/satellite/accreditation.yaml#createBadgePrintJob)*
- **Replace credential**: Opens the accreditation replacement (replaceAccreditationCredential), which invalidates the old credential in the same act. *(source: contracts/satellite/accreditation.yaml#replaceAccreditationCredential)*

**Data it reads**: `listAccreditationCredentials` (onLoad, Accreditation credentials issued); `listAccreditationHolders` (onLoad, Approved holders awaiting a credential); `listBadgePrintJobs` (onLoad, The print queue, and what failed)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-645` Credential Generation Workspace: *Credential Generation Workspace*
- → `BO-646` Credential Media Configuration: *Credential Media Configuration*
- → `BO-647` Badge Template Designer: *Badge Template Designer*
- → `BO-648` Badge Printing & Print Queue: *Badge Printing & Print Queue*
- → `BO-649` Digital & Mobile Credential Management: *Digital & Mobile Credential Management*; carries `credentialId`
- → `BO-650` NFC & RFID Credential Encoding: *NFC & RFID Credential Encoding*; carries `credentialId`
- → `BO-651` Credential Activation & Delivery: *Credential Activation & Delivery*; carries `credentialId`
- → `BO-027` Reissue & Media Replacement: *Credential Replacement & Reissue (BO-027, absorbed BO-652, audit R276)*
- → `BO-653` Credential Registry & Credential History: *Credential Registry & Credential History*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential issuance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential issuance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential issuance yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential issuance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Accreditation suspended after a badge was printed**: The badge counts under Revoked or Suspended and the status reaches Access Control; the tile explains "Suspended with the accreditation". *(source: screens/P08-venue-back-office.yaml#BO-653 / DI-663)*
- **User without ACCREDITATION_ISSUE**: Counts visible; Issue, Bulk issue and Replace disabled with "Needs accreditation issuing rights" (VO-R08). *(source: contracts/satellite/accreditation.yaml#issueAccreditationCredential)*

#### Consistency with other screens

- Match `BO-654`: The accreditation access hub (zones) is the next board; same holder card component.
- Match `BO-354`: The guest credential hub is a different estate; similar layout, different data - do not reuse its read.
- Match `ACC-008`: The portal's credential register (organisation view) reads the same accreditation credentials.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  awaitingIssuance: 46
  generated: 1210
  awaitingPrinting: 84
  printed: 1020
  awaitingCollection: 312
  digitalDelivered: 640
  active: 1388
  failedIssuance: 3
  replacementRequests: 7
  revoked: 12
queue:
- holder: Omar Haddad
  category: Media
  organisation: Gulf News
  event: Summer Concert - Etihad Park
  approved: 29 Sep 2026
  credential: Not issued
- holder: Maria Santos
  category: Contractor
  organisation: Bright Stage Productions
  approved: 30 Sep 2026
  credential: Issuance failed - photo missing
```

#### Permissions

- `listAccreditationCredentials` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `listBadgePrintJobs` → `ACCREDITATION_ISSUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.22 | QR Credential Support - System shall support QR-based accreditation credentials. | Accreditation & Credential Management | CONTRACTED | data `AccreditationCredential` |
| 12.1.16 | Profile Management - System shall maintain detailed accreditation holder profiles. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |
| 12.1.17 | Photo Management - System shall support accreditation holder photographs. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-644` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-644`
- Workshop pack: ACCREDITATION.pdf board 4
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 1: Opens Credential Issuance Command Center → Central operational dashboard for accreditation credential issuance.
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F220 branch at step 1 (expected): when Nothing has been set up on Credential Issuance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F220 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-644?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-645`, `BO-646`, `BO-647`, `BO-648`, `BO-649`, `BO-650`, `BO-651`, `BO-027`, `BO-653`.
- [ ] Every gated control is gated: `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-645` Credential Generation Workspace

**Convert an approved accreditation into an operational credential.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-645 |
| Who uses it | venue staff holding `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-generation-workspace-bo-645` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where an operator turns an approved accreditation into one or more credentials: confirms the holder's details, chooses the media the programme allows (printed badge, QR, mobile, NFC, RFID), and generates, prints or sends. The one thing to get right: generation is possible only for an eligible accreditation, and the screen says why when it is not.

**Known correction pending (do not draw the wrong version)**

- **Primary button labelled "Key requirement - 12.1.4"** Why: Pack text as a label; the actions are Generate, Generate and print, Generate and send digital, Save pending. *(source: screens/P08-venue-back-office.yaml#BO-646; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Wristband is a credential kind but is not in the pack's media list** Why: Either the pack's list or the enum is incomplete; draw wristband only if enabled for the programme. *(source: screens/P08-venue-back-office.yaml#BO-645 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Only listAccreditationCredentials is bound; the issue operation is bound to BO-646 (CHG-WIR-001); issueAccreditationCredential's description says revoking access is done by revokeAccreditation (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Can one accreditation hold several active credentials (badge and mobile) at once?** → Drawn default accepted: Yes, one per kind. *(decided by Chinmay, 2026-10-02; DEC-469 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationCredentials` ?holderId |
| Status | text field | — | — | `listAccreditationCredentials` ?status |

**Form: Generate credential** (modal, opened by *Generate credential*; *Generate credential* calls `issueAccreditationCredential`, *Cancel* sends nothing)

**Collects what `issueAccreditationCredential` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `issueAccreditationCredential` body |
| Holder `holderId` | picker: choose a holder | required | — | — | shows names, sends the id | — | `issueAccreditationCredential` body |
| Kind `kind` | select | required | — | Printed badge · Mobile credential · QR · NFC card · RFID card · Wristband | — | — | `issueAccreditationCredential` body |
| Symbology `symbology` | select | optional | — | QR · Data matrix · Pdf417 · Aztec · Code128 · NFC ndef · RFID epc · None | — | 12.1.22. How `encodedIdentifier` is carried, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a `mobileCredential`, a barcode where a printed … | `issueAccreditationCredential` body |
| Serial number `serialNumber` | text field | optional | — | — | — | — | `issueAccreditationCredential` body |
| Encoded identifier `encodedIdentifier` | text field | optional | — | — | — | — | `issueAccreditationCredential` body |
| Badge template `badgeTemplateId` | picker: choose a badge template | optional | — | — | shows names, sends the id | — | `issueAccreditationCredential` body |
| Issued at `issuedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `issueAccreditationCredential` body |
| Issued by `issuedBy` | picker: choose an issued by | optional | — | — | shows names, sends the id | — | `issueAccreditationCredential` body |
| Activated at `activatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `issueAccreditationCredential` body |
| Status `status` | select | optional | — | Pending print · Issued · Active · Lost · Replaced · Revoked · Expired | — | — | `issueAccreditationCredential` body |
| Replaces credential `replacesCredentialId` | picker: choose a replaces credential | optional | — | — | shows names, sends the id | — | `issueAccreditationCredential` body |
| Replacement count `replacementCount` | number field | optional | 0 | — | — | — | `issueAccreditationCredential` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `issueAccreditationCredential` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Holder**: Search by name, accreditation number or application reference; only holders with an approved, active accreditation are selectable, others shown with the reason ("Suspended", "Awaiting approval"). *(source: screens/P08-venue-back-office.yaml#BO-645 / screens/P08-venue-back-office.yaml#BO-646)*
- **Credential media**: Tick boxes for the media enabled for the programme (Printed badge, QR, Mobile, NFC, RFID); disabled media show "Not enabled for this programme". NFC and RFID continue to encoding (BO-650). *(source: screens/P08-venue-back-office.yaml#BO-645 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential)*
- **Badge template**: Pre-filled from the category; changeable among templates allowed for the category; preview shows this holder on it. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme / contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate)*
- **Identifier, serial, issued by, status**: Never inputs; the server generates the unique identifier and serial (per VO-R03) and shows them after generation. *(source: screens/P08-venue-back-office.yaml#BO-646)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Key requirement: 12.1.4 (primary button) | navigation or local | — | — | — | — |
| Generate credential (secondary button) | `issueAccreditationCredential` POST `/accreditation-credentials` | AccreditationCredential | AccreditationCredential | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Holder card**: Name, photo, holder ID, accreditation ID, category, organisation, event, venue, validity period, assigned access profile with zones. *(source: screens/P08-venue-back-office.yaml#BO-645)*
- **Existing credentials**: The holder's current credentials with status, so a second active credential of the same kind is visible before generating. *(source: contracts/satellite/accreditation.yaml#listAccreditationCredentials)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Generate**: Creates the credentials; printed badges go to Pending print. *(source: contracts/satellite/accreditation.yaml#issueAccreditationCredential)*
- **Generate and print**: Generates and queues a print job on the selected printer; opens the print queue entry. *(source: contracts/satellite/accreditation.yaml#issueAccreditationCredential / contracts/satellite/accreditation.yaml#createBadgePrintJob)*
- **Generate and send digital**: Generates and sends to the holder's own email, SMS or app; refused with "No email or mobile on the holder record" where missing. *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*
- **Save pending**: Keeps the selection for later without generating; drawn greyed until supported (per VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-646)*

**Data it reads**: `listAccreditationCredentials` (onLoad, Credentials issued)

**Where the user goes next**

- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential generation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential generation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential generation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential generation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Holder already has an active credential of that kind**: Warn and offer Replace instead (old one stops working in the same act). *(source: contracts/satellite/accreditation.yaml#replaceAccreditationCredential)*
- **No approved photo and the template prints a photo**: Printed badge disabled with "No approved photo"; QR and mobile still possible. *(source: contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate)*
- **Identity document expired since approval**: Generation blocked with the document named. *(source: DI-663)*

#### Consistency with other screens

- Match `BO-644`: Opened from the credential issuance command centre and returns to it.
- Match `ACC-005`: A mobile credential generated here is what the holder sees there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holder:
  name: Sara Al Nuaimi
  holderId: SP26-MED-00041
  category: Media
  organisation: Gulf Lens Media
  validity: 01-14 Dec 2026
  access: Media - all public zones and press centre
media:
- Printed badge
- Mobile
template: Media orange
```

#### Permissions

- `listAccreditationCredentials` → `ACCREDITATION_VIEW` (read) · staff
- `issueAccreditationCredential` → `ACCREDITATION_ISSUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.25 | System shall support allocation and management of accreditation passes for staff, media, VIPs, contractors and performers. | Ticketing Catalogue | CONTRACTED | `issueAccreditationCredential` |
| 12.1.4 | Credential Generation System shall generate accreditation IDs, QR codes, NFC cards or digital credentials. | Accreditation & Credential Management | CONTRACTED | `issueAccreditationCredential` |
| 12.1.23 | NFC Credential Support - System shall support NFC accreditation credentials. | Accreditation & Credential Management | CONTRACTED | `issueAccreditationCredential` |
| 12.1.24 | RFID Credential Support - System shall support RFID accreditation credentials. | Accreditation & Credential Management | CONTRACTED | `issueAccreditationCredential` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-645` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-645`
- Workshop pack: ACCREDITATION.pdf board 4
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 2: Works in Credential Generation Workspace → Convert an approved accreditation into an operational credential.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-645?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Key requirement: 12.1.4, Generate credential.
- [ ] Every transition is wired: `BO-644`.
- [ ] Every gated control is gated: `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-646` Credential Media Configuration

**Configure the credential technologies available for each accreditation program.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block B · ticket #29134 (VM-BO-646) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-media-configuration-bo-646` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): Issuing a credential is BO-645's act; this screen configures media and has no operation in the contract yet (contract gap CHG-WIR-004) (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Programme-level configuration of the credential technologies: which media are enabled (physical badge, QR static or dynamic, mobile, NFC, RFID) and, for each, the identifier format, activation method, issuance channel, replacement policy, expiry behaviour and how it reaches access control. The one thing to get right: QR security and gate behaviour are not configured here; they are the access module's, and this screen only says which of the access module's credential types accreditation uses.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No media configuration exists in the contract (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): issueAccreditationCredential is bound to a configuration screen (CHG-WIR-001); Primary button has no label (CHG-SBO-016).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is media configuration per programme or per category (media all zones on mobile, contractors printed only)?** → Drawn default accepted: Per programme, with a per-category override drawn greyed. *(decided by Chinmay, 2026-10-02; DEC-470 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Media cards**: Five cards (Physical badge, QR, Mobile, NFC, RFID) each with an Active switch; a disabled card collapses. *(source: screens/P08-venue-back-office.yaml#BO-646)*
- **Per-medium settings**: Identifier format (closed set: Accreditation number, Random 12-character, Card UID), activation method (At issue, On first scan, On delivery opened), issuance channel (Desk collection, Organisation representative, Email, SMS, Holder app), replacement policy (free, fee, reason required), expiry behaviour (Expires with accreditation, Expires with event), access control integration (read-only: the access credential type it maps to). *(source: screens/P08-venue-back-office.yaml#BO-646 / contracts/satellite/accreditation.yaml#deliverAccreditationCredential / contracts/satellite/accreditation.yaml#replaceAccreditationCredential)*
- **QR mode**: Static or Dynamic; Dynamic follows the access module's credential security settings and links there. *(source: screens/P08-venue-back-office.yaml#BO-646 / screens/P08-venue-back-office.yaml#BO-624)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Summary line per card**: "Mobile - active on delivery opened, sent by email or SMS, expires with accreditation". *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save media settings**: Drawn per the pack; greyed (per VO-R13) because the contract has no media configuration to write. *(source: DI-653)*

**Where the user goes next**

- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential media list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential media untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential media yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential media are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A medium is disabled while credentials of that kind exist**: Confirm names the count ("212 printed badges stay valid; no new ones can be issued"). *(source: screens/P08-venue-back-office.yaml#BO-033)*

#### Consistency with other screens

- Match `BO-645`: Only media enabled here are offered at generation.
- Match `BO-650`: NFC and RFID encoding follow the identifier format set here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cards:
- medium: Physical badge
  active: true
  identifier: Accreditation number
  activation: At issue
  channel: Desk collection
  replacement: Reason required, AED 50 fee for loss
- medium: QR
  active: true
  mode: Dynamic
  activation: On delivery opened
- medium: Mobile
  active: true
  channel: Email, SMS
  expiry: Expires with accreditation
- medium: NFC
  active: false
- medium: RFID
  active: true
  identifier: Card UID
  channel: Desk collection
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-646` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-646`
- Workshop pack: ACCREDITATION.pdf board 4
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 4: Works in Credential Media Configuration → Configure the credential technologies available for each accreditation program.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-646?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-644`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-647` Badge Template Designer

**Design physical accreditation badges.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-647 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/badge-template-designer-bo-647` |

**Known gaps.** **Badge Template Designer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The visual designer for printed accreditation badges, front and back: photo, name, organisation, job title, category, accreditation ID, event, venue, validity, QR, colour stripe, zone indicators, logos, sponsor branding, security marks and custom fields, with templates varying by tenant, event, venue, category and programme. The one thing to get right: the colour stripe and zone indicators are security controls a steward reads at ten metres, so each colour is paired with a word, never colour alone.

**Known correction pending (do not draw the wrong version)**

- **BadgeTemplate has no layout, back side, element positions, logos, sponsor branding, QR placement or custom fields** Why: Only four show-switches, size, stripe colour, background and security features exist; a visual designer has nothing to save positions to. *(source: screens/P08-venue-back-office.yaml#BO-648 / contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Templates varying by tenant, event, venue, category and programme** Why: The template has no scope fields; only categories point at templates. *(source: screens/P08-venue-back-office.yaml#BO-648 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Gap says the designer declares no write operation (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which card printers and card sizes does the client use?** → Drawn default accepted: CR80 only, other sizes greyed. *(decided by Chinmay, 2026-10-02; DEC-471 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Name and code**: Code unique (MEDIA-OR), name shown in pickers. *(source: contracts/satellite/accreditation.yaml#setBadgeTemplate)*
- **Size**: Closed set of card sizes (CR80 85.6 x 54 mm portrait or landscape, A6); not free text. *(source: contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate)*
- **Elements**: A palette of the pack's elements dragged onto a front and a back canvas; Show photo, zones, organisation and validity are on by default. Text elements render Arabic right-to-left beside English. *(source: screens/P08-venue-back-office.yaml#BO-646 / screens/P08-venue-back-office.yaml#BO-648)*
- **Colour stripe**: A colour plus its category word printed inside the stripe ("MEDIA"); contrast checked against white text. *(source: contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate)*
- **Background and security features**: Background image upload (tenant branding); security features as chips (Hologram overlay, Microtext, UV ink, Guilloche). *(source: contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate / MATRIX 12.1.57)*

#### Outputs: what the screen shows and produces

**Shown**

**Badge templates** (data table, from `listBadgeTemplates`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Size | text | — |
| Show photo | yes / no (icon or chip) | — |
| Show zones | yes / no (icon or chip) | — |
| Colour stripe | text | What a security officer checks at a glance. The stripe is the control that works at ten metres in the dark. |
| Show organisation | yes / no (icon or chip) | — |
| Show validity | yes / no (icon or chip) | — |
| Background image | the image or video | — |
| Security features | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save badge template (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Live preview**: Front and back with a sample holder (switchable between a long Arabic name and a short English one) at actual size. *(source: designer default)*
- **Used by**: Programmes and categories that use this template, and how many badges were printed with it. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save badge template**: Writes the whole template (per VO-R04); confirmation says badges already printed are unchanged and future prints use the new design. *(source: contracts/satellite/accreditation.yaml#setBadgeTemplate)*
- **Duplicate template**: Opens a copy as a new template for another category or event. *(source: MATRIX 12.1.56)*

**Data it reads**: `listBadgeTemplates` (onLoad, Badge designs to open)

**Where the user goes next**

- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The badge template designer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the badge template designer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No badge template designer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the badge template designer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **QR placed too small or too near the edge**: Warning on the canvas ("QR below 20 mm may not scan"). *(source: designer default)*

#### Consistency with other screens

- Match `BO-619`: The category colour is this stripe colour.
- Match `ACC-005`: The mobile badge mirrors this template's fields and colour.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
template:
  code: MEDIA-OR
  name: Media orange
  size: CR80 portrait
  stripe: Orange - MEDIA
  showPhoto: true
  showZones: true
  securityFeatures:
  - Hologram overlay
  - Microtext
  usedBy: Winter Festival 2026 - Media
```

#### Permissions

- `setBadgeTemplate` → `ACCREDITATION_CONFIGURE` (configure) · staff
- `listBadgeTemplates` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.57 | Accreditation Branding - System shall support tenant-specific accreditation branding. | Accreditation & Credential Management | CONTRACTED | `setBadgeTemplate` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-647` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-647`
- Workshop pack: ACCREDITATION.pdf board 4
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 6: Works in Badge Template Designer → Design physical accreditation badges.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-647?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save badge template, Cancel.
- [ ] Every transition is wired: `BO-644`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-648` Badge Printing & Print Queue

**Manage physical accreditation badge production.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-648 |
| Who uses it | venue staff holding `ACCREDITATION_ISSUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/badge-printing-print-queue-bo-648` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): The badge-template read and write belong to the designer BO-647; the print queue needs listBadgePrintJobs and createBadgePrintJob, which were bound to BO-649 …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Physical badge production: the queue of badges to print, which printer, how many copies, who asked, and what happened, including which badges in a batch failed. The one thing to get right: a batch that fails half-way shows exactly which badges printed and offers to reprint only the failed ones, never the whole run.

**Known correction pending (do not draw the wrong version)**

- **Pack statuses and fields do not match BadgePrintJob** Why: The job has queued, printing, completed, partiallyFailed and failed at job level, with no per-badge Printed, Reprint required or Cancelled, and no copies, requested by or cancel operation. *(source: screens/P08-venue-back-office.yaml#BO-649 / contracts/satellite/accreditation.yaml#/components/schemas/BadgePrintJob; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): listBadgeTemplates and setBadgeTemplate are bound here, with a "Save badge template" button (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does every reprint need a reason, or only above a count per holder?** → Drawn default accepted: Every reprint asks for a reason. *(decided by Chinmay, 2026-10-02; DEC-472 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Form: Print badges** (modal, opened by *Print badges*; *Print badges* calls `createBadgePrintJob`, *Cancel* sends nothing)

**Collects what `createBadgePrintJob` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createBadgePrintJob` body |
| Credentials `credentialIds` | multi-picker: choose credentials | optional | — | — | — | — | `createBadgePrintJob` body |
| Printer device `printerDeviceId` | picker: choose a printer device | optional | — | — | shows names, sends the id | — | `createBadgePrintJob` body |
| Queued at `queuedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createBadgePrintJob` body |
| Status `status` | radio group | optional | — | Queued · Printing · Completed · Partially failed · Failed | — | — | `createBadgePrintJob` body |
| Failures `failures` | repeatable rows | optional | — | — | — | — | `createBadgePrintJob` body |
| Credential `failures[].credentialId` | picker: choose a credential | optional | — | — | shows names, sends the id | — | `createBadgePrintJob` body |
| Reason `failures[].reason` | text area | optional | — | — | — | — | `createBadgePrintJob` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `createBadgePrintJob` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Printer**: Select from card printers in the device register, with status (Ready, Offline, Out of cards); offline printers are not selectable. *(source: contracts/satellite/accreditation.yaml#/components/schemas/BadgePrintJob / ADR-0067)*
- **Copies**: Whole number, default 1. *(source: screens/P08-venue-back-office.yaml#BO-648)*
- **Reprint reason**: Required where the security policy asks (Damaged, Misprint, Lost - replaced); a lost badge goes through Replace credential instead. *(source: screens/P08-venue-back-office.yaml#BO-649 / contracts/satellite/accreditation.yaml#replaceAccreditationCredential)*

#### Outputs: what the screen shows and produces

**Shown**

**Print queue** (data table, from `listBadgePrintJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Credentials | list or chips (count when long) | — |
| Printer device | the name it points at, never the id | — |
| Queued at | 1 Oct 2026, 14:30 | — |
| Status | chip: Queued, Printing, Completed, Partially failed, Failed | — |
| Printed | 1,234 | — |
| Failed | 1,234 | — |
| Failures | list or chips (count when long) | — |
| Credential | the name it points at, never the id | — |
| Reason | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Print badges (secondary button) | `createBadgePrintJob` POST `/badge-print-jobs` | BadgePrintJob | BadgePrintJob | — | opens modal first; produces a document or message: Queue badges for printing |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Print queue table**: Columns Holder (photo, name), Accreditation ID, Badge template, Printer, Status (Queued, Printing, Printed, Failed, Reprint required, Cancelled), Copies, Requested by, Requested at. Batch rows expand to their badges. Title "Print queue". *(source: screens/P08-venue-back-office.yaml#BO-648 / screens/P08-venue-back-office.yaml#BO-649)*
- **Batch result**: "Batch of 40: 37 printed, 3 failed (card jam)" with the three listed and a "Reprint 3 failed" button. *(source: contracts/satellite/accreditation.yaml#listBadgePrintJobs)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Print / Batch print**: Queues the selected credentials on the printer; the rows go to Queued. *(source: contracts/satellite/accreditation.yaml#createBadgePrintJob)*
- **Preview badge**: Shows the badge as it will print using its template. *(source: screens/P08-venue-back-office.yaml#BO-649)*
- **Reprint failed**: Queues only the failed credentials of the batch. *(source: contracts/satellite/accreditation.yaml#listBadgePrintJobs)*
- **Cancel job**: Drawn per the pack; greyed until supported (per VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-649)*

**Data it reads**: `listBadgePrintJobs` (onLoad, The print queue, and what failed)

**Where the user goes next**

- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The badge printing print list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the badge printing print untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No badge printing print yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the badge printing print are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Printer goes offline mid-batch**: The job shows Partly failed with the remaining badges listed as not printed. *(source: contracts/satellite/accreditation.yaml#/components/schemas/BadgePrintJob)*
- **Holder suspended while queued**: The badge is skipped with "Holder suspended" in the failures. *(source: contracts/satellite/accreditation.yaml#setAccreditationStatus)*

#### Consistency with other screens

- Match `BO-645`: Generate and print lands here.
- Match `BO-644`: The command centre's "Awaiting printing" and failed issuance tiles count these rows.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
jobs:
- batch: Gulf Lens Media - 40 badges
  printer: Accreditation desk printer 1
  status: Partly failed (37 printed, 3 failed)
  requestedBy: Maria Santos
  at: 11 Oct 2026 10:15
- holder: Khalid Al Zaabi
  accreditationId: SP26-GOV-00009
  template: Authority red
  printer: Accreditation desk printer 2
  status: Queued
  copies: 1
  requestedBy: Fatima Al Hashimi
```

#### Permissions

- `listBadgePrintJobs` → `ACCREDITATION_ISSUE` (operate) · staff
- `createBadgePrintJob` → `ACCREDITATION_ISSUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.20 | Credential Printing - System shall support printing of accreditation badges. | Accreditation & Credential Management | CONTRACTED | `createBadgePrintJob` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-648` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-648`
- Workshop pack: ACCREDITATION.pdf board 4
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 8: Works in Badge Printing & Print Queue → Manage physical accreditation badge production.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-648?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Print badges.
- [ ] Every transition is wired: `BO-644`.
- [ ] Every gated control is gated: `ACCREDITATION_ISSUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-649` Digital & Mobile Credential Management

**Manage credentials delivered electronically to accreditation holders.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-649 |
| Who uses it | venue staff holding `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `credentialId` (navigation) |
| Route | `/access-venue/digital-mobile-credential-management-bo-649` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): Print jobs belong to BO-648; this screen delivers mobile credentials (deliverAccreditationCredential) and lists the digital ones (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Mobile and digital credentials delivered to holders: what each shows, whether it was sent, delivered and opened, and the controls to send, resend, activate, deactivate, refresh or revoke. The one thing to get right: a credential is only ever sent to the holder's own email or mobile on their record, never to an address typed at the counter, and a resend kills the previous link.

**Known correction pending (do not draw the wrong version)**

- **Delivery status is tracked but cannot be read** Why: AccreditationCredentialDelivery records each send, but no operation lists deliveries, so the Delivery column has no source. *(source: screens/P08-venue-back-office.yaml#BO-649 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredentialDelivery; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Activate, Deactivate and Refresh have no operation** Why: Activation exists only as activateOnDelivery; there is no deactivate or refresh of a credential. *(source: screens/P08-venue-back-office.yaml#BO-649 / contracts/satellite/accreditation.yaml#deliverAccreditationCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): createBadgePrintJob and listBadgePrintJobs are bound here with a "Create badge print job" button (CHG-WIR-001); No list of digital credentials is bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should Refresh rotate the credential's identifier (as a dynamic QR does) or only re-push the wallet pass?** → Drawn default accepted: Re-push only; rotation belongs to the access module's dynamic QR. *(decided by Chinmay, 2026-10-02; DEC-473 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationCredentials` ?holderId |
| Status | text field | — | — | `listAccreditationCredentials` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Channel**: Email, SMS or Holder app; channels the holder has no address for are disabled with "No mobile on record". *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*
- **Activate on delivery**: Switch, default off; when on the credential becomes active when the holder opens it. *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*

#### Outputs: what the screen shows and produces

**Shown**

**Digital credentials** (data table, from `listAccreditationCredentials`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Holder | the name it points at, never the id | — |
| Kind | chip: Printed badge, Mobile credential, QR, NFC card, RFID card, Wristband | — |
| Symbology | chip: QR, Data matrix, Pdf417, Aztec, Code128, NFC ndef… | 12.1.22. How `encodedIdentifier` is carried, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a … |
| Serial number | text | — |
| Encoded identifier | text | — |
| Badge template | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Issued by | the name it points at, never the id | — |
| Activated at | 1 Oct 2026, 14:30 | — |
| Status | chip: Pending print, Issued, Active, Lost, Replaced, Revoked… | — |
| Replaces credential | the name it points at, never the id | — |
| Replacement count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Digital credentials table**: Columns Holder, Credential ID, Category, Event, Validity, Status, Delivery (Queued, Sent, Delivered, Opened, Failed with reason, Superseded), Channel with masked destination ("s***@gulflens.ae"), Wallet (Apple, Google, none). *(source: screens/P08-venue-back-office.yaml#BO-649 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredentialDelivery)*
- **Credential preview**: The holder's credential as ACC-005 renders it (photo, name, category, organisation, credential ID, event, validity, QR, status). *(source: screens/P08-venue-back-office.yaml#BO-649)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Send / Resend**: Sends to the holder's own address; resending supersedes the previous link and says so in the confirm. *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*
- **Activate / Deactivate / Refresh / Revoke**: Revoke routes to replacing the credential or changing the accreditation status, named as such (per VO-R16); Activate, Deactivate and Refresh are drawn greyed until supported (per VO-R13). *(source: contracts/satellite/accreditation.yaml#replaceAccreditationCredential / contracts/satellite/accreditation.yaml#setAccreditationStatus)*

**Data it reads**: `listAccreditationCredentials` (onLoad, Digital and mobile credentials (mobile and QR kinds))

**Where the user goes next**

- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital mobile credential list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital mobile credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital mobile credential yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital mobile credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not a mobile or QR credential, or not issued or active; 422 The holder has no email or phone for the chosen channel |

#### Edge cases to draw

- **Holder has no email or mobile**: Send refused (422) shown as "Add an email or mobile on the holder record first" with a link to the profile. *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*
- **Credential is not issued or active**: Send disabled with the status named. *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*
- **Holder suspended after adding to wallet**: The wallet pass updates by push; the Wallet column shows "Updated 14:02". *(source: contracts/satellite/accreditation.yaml#issueMyAccreditationWalletPass)*

#### Consistency with other screens

- Match `ACC-005`: The preview is exactly what the holder sees.
- Match `BO-651`: Activation and delivery tracking for all media; the delivery statuses are the same words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- holder: Sara Al Nuaimi
  credential: SP26-M-00041
  category: Media
  validity: 01-14 Dec 2026
  status: Issued
  delivery: Opened 11 Oct 2026 20:14
  channel: Email s***@gulflens.ae
  wallet: Apple
- holder: Priya Nair
  credential: SP26-M-00057
  category: Media
  status: Issued
  delivery: Failed - mailbox full
  channel: Email p***@outlook.com
  wallet: none
```

#### Permissions

- `deliverAccreditationCredential` → `ACCREDITATION_ISSUE` (operate) · staff
- `listAccreditationCredentials` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.22 | QR Credential Support - System shall support QR-based accreditation credentials. | Accreditation & Credential Management | CONTRACTED | data `AccreditationCredential` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-649` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-649`
- Workshop pack: ACCREDITATION.pdf board 4
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 10: Works in Digital & Mobile Credential Management → Manage credentials delivered electronically to accreditation holders.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-649?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-644`.
- [ ] Every gated control is gated: `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-650` NFC & RFID Credential Encoding

**Associate physical NFC/RFID media with an accreditation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-650 |
| Who uses it | venue staff holding `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `credentialId` (navigation) |
| Route | `/access-venue/nfc-rfid-credential-encoding-bo-650` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The encoding desk: an accreditation officer with a desktop NFC/RFID encoder takes a blank card or wristband, ties it to one approved holder, writes and reads back the identifier, and records it against the credential so a gate reader can resolve it. It is a guided, one-holder-at-a-time workspace (holder on the left, live reader panel on the right), not a form. The one thing to get right: the card's identifier is recorded and checked for uniqueness before the card leaves the desk, because an encoded card nothing can resolve, or one that resolves to two people, is worse than no card.

**Known correction pending (do not draw the wrong version)**

- **The issue call on this screen is labelled "Digital and mobile credentials", while BO-651 labels the same call "NFC and RFID encoding"** Why: The purposes are swapped between the two screens; encoding belongs here and delivery on BO-651. *(source: screens/P08-venue-back-office.yaml#BO-650 / screens/P08-venue-back-office.yaml#BO-651; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The contract states no uniqueness rule for encodedIdentifier or serialNumber across active holders** Why: The pack requires the system to prevent the same media being assigned to several active holders; the issue call needs a 409 for a card already active elsewhere. *(source: screens/P08-venue-back-office.yaml#BO-650 / contracts/satellite/accreditation.yaml#issueAccreditationCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Primary button has an empty label** Why: Generated placeholder; the action is "Encode and assign". *(source: screens/P08-venue-back-office.yaml#BO-650; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The issue description says revoking access is done by `revokeAccreditation`** Why: No such operation exists; revocation is setAccreditationStatus with status revoked. *(source: contracts/satellite/accreditation.yaml#issueAccreditationCredential / contracts/satellite/accreditation.yaml#setAccreditationStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): No read is bound (no holder search, no list of the holder's existing credentials), and replaceAccreditationCredential is not bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which desktop encoders must be supported, and is the encoder registered in the device register (ADR-0067) so a workstation knows it has one?** → Drawn default accepted: Draw a reader picker in the strip header ("Encoder - Accreditation Desk 1") fed from the device register, greyed when only one exists. *(decided by Chinmay, 2026-10-02; DEC-474 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Is an NFC/RFID credential active the moment it is encoded, or does it wait for collection (BO-651)?** → Drawn default accepted: Active on successful encode for desk-collected cards; show the Activate button only for programmes set to activate on collection. *(decided by Chinmay, 2026-10-02; DEC-475 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationHolders` ?programmeId |
| Organisation | picker: choose an organisation | — | — | `listAccreditationHolders` ?organisationId |
| Status | text field | — | — | `listAccreditationHolders` ?status |
| Expiring within days | number field (days) | — | — | `listAccreditationHolders` ?expiringWithinDays |

**Form: Replace medium** (modal, opened by *Replace medium*; *Replace medium* calls `replaceAccreditationCredential`, *Cancel* sends nothing)

**Collects what `replaceAccreditationCredential` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Lost · Stolen · Damaged · Name change · Photo change · Access change | — | — | `replaceAccreditationCredential` body |
| Charge fee `chargeFee` | toggle | optional | off | — | — | — | `replaceAccreditationCredential` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **holder**: First step is "Select holder": search by name, accreditation number or organisation, showing photo, category and accreditation status. Only holders whose accreditation is approved and active can be picked; others show greyed with the reason ("Accreditation suspended", "Approval not complete"). Opening from a holder (BO-626 or BO-645) skips this step with the holder pre-selected. *(source: screens/P08-venue-back-office.yaml#BO-650 / screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#listAccreditationHolders)*
- **kind**: A choice of the physical media enabled for this programme in Credential Media Configuration (BO-646) only, normally NFC card, RFID card or Wristband; printed badge, QR and mobile credential are issued elsewhere and never offered here. *(source: screens/P08-venue-back-office.yaml#BO-646 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential)*
- **symbology**: Not typed. Derived from the kind (NFC card gives nfcNdef, RFID card or wristband gives rfidEpc) and shown read-only as "Encoding: NFC NDEF" so the reader and the gate agree. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential)*
- **serialNumber / encodedIdentifier**: Never typed by hand. serialNumber is the card UID captured by the reader on "Card detected"; encodedIdentifier is what the system writes to the card and reads back on "Verification". Both shown monospaced, read-only, with a copy icon. A manual-entry fallback, if the venue wants one, sits behind a disclosure and needs the same verification read. *(source: screens/P08-venue-back-office.yaml#BO-650 / contracts/satellite/accreditation.yaml#issueAccreditationCredential)*
- **id, issuedAt, issuedBy, status, replacementCount, scopePath**: Never inputs (per VO-R03); the server stamps them on issue. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential)*

#### Outputs: what the screen shows and produces

**Shown**

**Holders** (data table, from `listAccreditationHolders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Accreditation number | text | — |
| Full name | text | — |
| Photo image | the image or video | — |
| Date of birth | 1 Oct 2026 | — |
| Nationality | text | — |
| Email | email, tap to write | 12.1.16. |
| Phone | +971 50 123 4567 | 12.1.16. |
| Identity document verified | yes / no (icon or chip) | — |
| Organisation | the name it points at, never the id | — |
| Affiliation role | text | — |
| Programme | the name it points at, never the id | — |
| Category code | text | — |
| Status | chip: Active, Suspended, Revoked, Expired, Archived | — |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Completeness percent | 1,234 | — |

**Existing credentials** (data table, from `listAccreditationCredentials`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Holder | the name it points at, never the id | — |
| Kind | chip: Printed badge, Mobile credential, QR, NFC card, RFID card, Wristband | — |
| Symbology | chip: QR, Data matrix, Pdf417, Aztec, Code128, NFC ndef… | 12.1.22. How `encodedIdentifier` is carried, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a … |
| Serial number | text | — |
| Encoded identifier | text | — |
| Badge template | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Issued by | the name it points at, never the id | — |
| Activated at | 1 Oct 2026, 14:30 | — |
| Status | chip: Pending print, Issued, Active, Lost, Replaced, Revoked… | — |
| Replaces credential | the name it points at, never the id | — |
| Replacement count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Replace medium (secondary button) | `replaceAccreditationCredential` POST `/accreditation-credentials/{credentialId}/replace` | inline | AccreditationCredential | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reader status strip**: A six-step horizontal stepper with the pack's own words, Reader connected > Card detected > Encoding > Verification > Successful, with Failed as a red terminal state that names the step that failed and a Retry. The strip is live device feedback from the encoder, not a server state; the server only sees the final issue call. *(source: screens/P08-venue-back-office.yaml#BO-650)*
- **Holder card**: Photo, full name, accreditation number, category colour stripe, organisation, validity dates and the list of the holder's existing credentials with status chips (Active, Lost, Replaced, Revoked), so the officer sees a live card before encoding a second one. *(source: screens/P08-venue-back-office.yaml#BO-650 / contracts/satellite/accreditation.yaml#listAccreditationCredentials)*
- **Result**: On success: "NFC card NFC-04A2-91F3 encoded for Fatima Al Hashimi, active at the gates" with the activation state; the next holder can be scanned straight away (batch desk rhythm). *(source: contracts/satellite/accreditation.yaml#issueAccreditationCredential)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Encode and assign**: Writes the card, reads it back, then calls issue with holderId, kind, symbology, serialNumber and encodedIdentifier. The credential publishes to Access so the gate can resolve the identifier. If the read-back differs from what was written, nothing is sent to the server and the strip shows Failed at Verification. *(source: contracts/satellite/accreditation.yaml#issueAccreditationCredential / F220 step 12)*
- **Replace existing media**: Shown when the holder already has an active physical credential. Opens the replacement path (reason Lost, Stolen, Damaged, Failed NFC/RFID...) which invalidates the old card in the same act and encodes the new one; never issues a second live card beside the first. *(source: screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#replaceAccreditationCredential)*
- **Activate credential**: Only where the programme does not activate on issue; otherwise the card is active on success and the button is not shown. *(source: screens/P08-venue-back-office.yaml#BO-650 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

**Data it reads**: `listAccreditationHolders` (onLoad, Select the holder)

**Where the user goes next**

- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The nfc rfid credential list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the nfc rfid credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No nfc rfid credential yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the nfc rfid credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Card already assigned to another active holder**: Stop at Card detected with "This card is already active for Omar Haddad (ACC-2026-003117)"; offer Use another card. Only where configuration explicitly allows shared media may it proceed, and then with a reason. *(source: screens/P08-venue-back-office.yaml#BO-650)*
- **Encoder disconnected or driver missing**: Strip stays at Reader connected in red with "No encoder found on this workstation"; holder selection still works, Encode is disabled with the reason (per VO-R08 style). *(source: screens/P08-venue-back-office.yaml#BO-650)*
- **Accreditation suspended or revoked between selection and encode**: The issue call is refused; show "Fatima Al Hashimi's accreditation was suspended at 10:42; nothing was encoded" and clear the card. *(source: screens/P08-venue-back-office.yaml#BO-653)*
- **User without issue rights**: Workspace read-only, Encode disabled with "Needs credential issue rights". *(source: contracts/satellite/accreditation.yaml#issueAccreditationCredential)*

#### Consistency with other screens

- Match `BO-645`: Credential Generation Workspace issues printed badges and QR; this screen is its physical-media sibling. Same holder card, same status chips, same "issue" vocabulary.
- Match `BO-653`: Every card encoded here appears in the Credential Registry with its Printed/Encoded lifecycle step; the replacement link (replacesCredentialId) is drawn the same way in both.
- Match `SCN-003`: The scanner resolves the encodedIdentifier through verifyAccreditationCredential; the identifier format shown here is what a steward sees in a lookup.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holder:
  name: Fatima Al Hashimi
  accreditationNumber: ACC-2026-004812
  category: Media
  organisation: Gulf Media Network
  validity: 12 Dec 2026 - 20 Dec 2026
card:
  kind: NFC card
  uid: 04:A2:91:F3:7C:22:80
  encodedIdentifier: NFC-04A2-91F3
  symbology: NFC NDEF
existingCredentials:
- kind: Printed badge
  serial: BDG-004812-1
  status: Active
- kind: NFC card
  serial: NFC-03B9-77E1
  status: Lost
```

#### Permissions

- `issueAccreditationCredential` → `ACCREDITATION_ISSUE` (operate) · staff
- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationCredentials` → `ACCREDITATION_VIEW` (read) · staff
- `replaceAccreditationCredential` → `ACCREDITATION_ISSUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.25 | System shall support allocation and management of accreditation passes for staff, media, VIPs, contractors and performers. | Ticketing Catalogue | CONTRACTED | `issueAccreditationCredential` |
| 12.1.4 | Credential Generation System shall generate accreditation IDs, QR codes, NFC cards or digital credentials. | Accreditation & Credential Management | CONTRACTED | `issueAccreditationCredential` |
| 12.1.23 | NFC Credential Support - System shall support NFC accreditation credentials. | Accreditation & Credential Management | CONTRACTED | `issueAccreditationCredential` |
| 12.1.24 | RFID Credential Support - System shall support RFID accreditation credentials. | Accreditation & Credential Management | CONTRACTED | `issueAccreditationCredential` |
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.22 | QR Credential Support - System shall support QR-based accreditation credentials. | Accreditation & Credential Management | CONTRACTED | data `AccreditationCredential` |
| 12.1.16 | Profile Management - System shall maintain detailed accreditation holder profiles. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |
| 12.1.17 | Photo Management - System shall support accreditation holder photographs. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-650` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-650`
- Workshop pack: ACCREDITATION.pdf board 4
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 12: Works in NFC & RFID Credential Encoding → Associate physical NFC/RFID media with an accreditation.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-650?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, Replace medium.
- [ ] Every transition is wired: `BO-644`.
- [ ] Every gated control is gated: `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-651` Credential Activation & Delivery

**Control when an issued credential becomes operational.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-651 |
| Who uses it | venue staff holding `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `credentialId` (navigation) |
| Route | `/access-venue/credential-activation-delivery-bo-651` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): The issue call here was labelled "NFC and RFID encoding"; encoding is BO-650's job. This screen activates and delivers, and needs the credential list with …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Fulfilment tracking for issued credentials: where each badge, card or mobile credential is between generation and first use, how it reaches the holder, and when it starts working at the gates. Used by the accreditation desk on collection days and by the team chasing "I never got it". The one thing to get right: activation is a separate, visible moment that switches gate access on, and delivery of a mobile credential only ever goes to the holder's own email or phone.

**Known correction pending (do not draw the wrong version)**

- **The pack's delivery methods (Badge collection, Accreditation desk, Authorised organisation representative) and the collection fields (Collected by, Collection date/time, Issued by, Collection point, Acknowledgement) have no contract home** Why: deliverAccreditationCredential covers only email, sms and holderApp for mobile and QR credentials; physical hand-over cannot be recorded, so the Delivered stage is unreachable for badges and cards. *(source: screens/P08-venue-back-office.yaml#BO-650 / screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#deliverAccreditationCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **There is no operation to activate a credential, and the status enum has no Delivered state** Why: The pack makes activation a controlled step synchronised to Access Control (Generated > Produced > Delivered > Activated > Active); the contract only sets activatedAt at issue or on opening a delivered link. *(source: screens/P08-venue-back-office.yaml#BO-650 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Primary button has an empty label** Why: Generated placeholder; the actions are "Send to holder" and "Record collection". *(source: screens/P08-venue-back-office.yaml#BO-651; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The issue call here is labelled "NFC and RFID encoding", and no read (listAccreditationCredentials) is bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is BO-651 a separate screen from BO-649 Digital & Mobile Credential Management, or should delivery and activation be one fulfilment screen for all media?** → Drawn default accepted: Draw one fulfilment screen with a media filter (Physical / Digital) and keep BO-649 and BO-651 as anchors into it (per VO-R14). *(decided by Chinmay, 2026-10-02; DEC-476 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationCredentials` ?holderId |
| Status | text field | — | — | `listAccreditationCredentials` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **channel (digital delivery)**: Email, SMS or Holder app, offered only for a mobile or QR credential that is Issued or Active. The destination is never typed: show the holder's own address masked ("j***@gulfmedia.ae") and grey a channel the holder has no address for, with "No mobile number on file". *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*
- **activateOnDelivery**: A switch "Activate when the holder opens it" (default off = active from issue). Explain under it that gates admit the credential only after activation. *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*
- **physical collection**: For badges and cards handed over at a desk, capture Collected by (holder or authorised organisation representative, picked from the organisation's users), collection point (Accreditation desk, Badge collection point), issued by (the signed-in officer, not editable), date and time (now, not editable), and an optional acknowledgement (signature or tick). *(source: screens/P08-venue-back-office.yaml#BO-650 / screens/P08-venue-back-office.yaml#BO-653)*

#### Outputs: what the screen shows and produces

**Shown**

**Credentials** (data table, from `listAccreditationCredentials`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Holder | the name it points at, never the id | — |
| Kind | chip: Printed badge, Mobile credential, QR, NFC card, RFID card, Wristband | — |
| Symbology | chip: QR, Data matrix, Pdf417, Aztec, Code128, NFC ndef… | 12.1.22. How `encodedIdentifier` is carried, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a … |
| Serial number | text | — |
| Encoded identifier | text | — |
| Badge template | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Issued by | the name it points at, never the id | — |
| Activated at | 1 Oct 2026, 14:30 | — |
| Status | chip: Pending print, Issued, Active, Lost, Replaced, Revoked… | — |
| Replaces credential | the name it points at, never the id | — |
| Replacement count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Fulfilment pipeline**: Column or chip track with the pack's five stages, Generated > Produced > Delivered > Activated > Active, with counts per stage for the programme and a per-credential row showing which stage it is in and since when. Map contract states: pendingPrint = Generated, issued = Produced (or Delivered once a delivery is recorded), active = Active. *(source: screens/P08-venue-back-office.yaml#BO-650 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential)*
- **Delivery attempts**: For digital delivery, each send with channel, masked destination, status (Queued, Sent, Delivered, Opened, Failed, Superseded) and failure reason; a resend marks the previous link Superseded. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredentialDelivery)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Send to holder**: Queues the delivery and adds a row "Queued" that updates to Sent/Delivered/Opened. 409 shows "Only an issued or active mobile or QR credential can be sent"; 422 shows "Holder has no email for this channel - update the holder profile". *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*
- **Resend**: Confirmation "The previous link will stop working"; then sends a new one and supersedes the old. *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*
- **Record collection**: Marks a physical credential Delivered with who collected it, where and when; activation follows per the programme rule and is synchronised to Access. *(source: screens/P08-venue-back-office.yaml#BO-653)*

**Data it reads**: `listAccreditationCredentials` (onLoad, Issued credentials and their delivery state)

**Where the user goes next**

- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential activation delivery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential activation delivery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential activation delivery yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential activation delivery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not a mobile or QR credential, or not issued or active; 422 The holder has no email or phone for the chosen channel |

#### Edge cases to draw

- **Collection by an organisation representative for many members**: Allow multi-select of the organisation's ready badges and one collection record per badge with the same representative; the count is shown before confirm. *(source: screens/P08-venue-back-office.yaml#BO-650 / DI-660)*
- **Holder's accreditation suspended after the credential was produced**: Row shows Produced with a red "Accreditation suspended" chip; Send and Record collection are disabled with that reason. *(source: screens/P08-venue-back-office.yaml#BO-673)*
- **Link opened after resend**: The old link shows "This link has been replaced" on the holder's side; the row here stays Superseded. *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*

#### Consistency with other screens

- Match `BO-649`: Digital & Mobile Credential Management sends and resends the same deliveries; same delivery status chips and wording.
- Match `ACC-005`: The applicant's badge view on P11 shows the holder side of the same delivery (link opened, wallet added).
- Match `BO-644`: Board 4 command centre tiles for "Ready for collection" and "Delivery failed" open this screen filtered.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pipeline:
  generated: 214
  produced: 188
  delivered: 141
  activated: 133
  active: 133
rows:
- holder: Sara Al Nuaimi
  credential: Mobile credential
  stage: Delivered
  channel: Email
  destination: s***@yasmedia.ae
  status: Opened
  at: 14 Dec 2026 09:12
- holder: Rahul Menon
  credential: Printed badge
  stage: Produced
  collectionPoint: Accreditation desk
  status: Awaiting collection
- holder: James Carter
  credential: Mobile credential
  stage: Produced
  channel: SMS
  status: Failed
  failureReason: Number unreachable
```

#### Permissions

- `deliverAccreditationCredential` → `ACCREDITATION_ISSUE` (operate) · staff
- `listAccreditationCredentials` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.22 | QR Credential Support - System shall support QR-based accreditation credentials. | Accreditation & Credential Management | CONTRACTED | data `AccreditationCredential` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-651` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-651`
- Workshop pack: ACCREDITATION.pdf board 4
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 14: Works in Credential Activation & Delivery → Control when an issued credential becomes operational.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-651?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-644`.
- [ ] Every gated control is gated: `ACCREDITATION_ISSUE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-653` Credential Registry & Credential History

**Maintain the authoritative record of every credential issued by TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-653 |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-registry-credential-history-bo-653` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): listCredential is the guest credential operations list; accreditation credentials are read by listAccreditationCredentials and their lifecycle timeline by …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The authoritative register of every accreditation credential issued: credential id, holder, accreditation id, media type, event, venue, category, issue, activation and expiry dates, current status and its replacement relationship; opening one shows its lifecycle (Created > Generated > Printed / encoded > Delivered > Activated > Modified > Suspended / Revoked / Expired / Replaced). The one thing to get right: the replacement chain is visible both ways (this replaced X; replaced by Y), and every event is auditable.

**Known correction pending (do not draw the wrong version)**

- **Credential statuses disagree with the pack** Why: The accreditation credential has pendingPrint, issued, active, lost, replaced, revoked, expired; the pack lists Pending, Generated, Printed, Delivered, Active, Suspended, Expired, Revoked, Replaced (no suspended or delivered in the contract; lost is not a pack status). *(source: screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The register's event, venue, category, expiry and accreditation id are not on the credential record** Why: They come from the holder and programme; the list needs them joined or the columns cannot be filled. *(source: screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Placed in process-module Admission & Access Control; the gap says the pack gives nothing to draw** Why: It is accreditation board 4 screen 10, and the pack lists the columns, statuses and timeline. *(source: screens/P08-venue-back-office.yaml#BO-653; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Bound to listCredential, the guest credential operations list (CHG-WIR-001); The registry timeline needs the accreditation audit, not the guest credential list (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationCredentials` ?holderId |
| Status | text field | — | — | `listAccreditationCredentials` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Holder (search), accreditation id, credential type, status, event, category, issue date range. *(source: screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#listAccreditationCredentials)*

#### Outputs: what the screen shows and produces

**Shown**

**Credential registry** (data table, from `listAccreditationCredentials`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Holder | the name it points at, never the id | — |
| Kind | chip: Printed badge, Mobile credential, QR, NFC card, RFID card, Wristband | — |
| Symbology | chip: QR, Data matrix, Pdf417, Aztec, Code128, NFC ndef… | 12.1.22. How `encodedIdentifier` is carried, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a … |
| Serial number | text | — |
| Encoded identifier | text | — |
| Badge template | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Issued by | the name it points at, never the id | — |
| Activated at | 1 Oct 2026, 14:30 | — |
| Status | chip: Pending print, Issued, Active, Lost, Replaced, Revoked… | — |
| Replaces credential | the name it points at, never the id | — |
| Replacement count | 1,234 | — |

**History** (data table, from `listAccreditationAudit`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| At | 1 Oct 2026, 14:30 | — |
| Holder | the name it points at, never the id | — |
| Action | text | — |
| Actor principal | the name it points at, never the id | — |
| Previous value | text | — |
| New value | text | — |
| Reason | text | — |
| Approval request | the name it points at, never the id | — |
| Previous record hash | text | — |
| Record hash | text | — |
| Integrity | chip: Intact, Broken, Unverifiable | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Registry**: Title "Credential register". Columns Credential ID (serial), Holder (photo thumbnail + name), Accreditation ID, Media type, Event, Venue, Category, Issued, Activated, Expiry, Status, Replacement ("Replaces C-1042" / "Replaced by C-1188"). Cursor paging. *(source: screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential)*
- **Lifecycle timeline**: The pack's chain as a timeline with actor and time per step; encoded identifiers masked. *(source: screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#listAccreditationAudit)*
- **Status chips**: Pending, Generated, Printed, Delivered, Active, Suspended, Expired, Revoked, Replaced - the pack's nine. *(source: screens/P08-venue-back-office.yaml#BO-653)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open holder**: Opens the accreditation holder profile (getAccreditationHolder) with all their credentials. *(source: contracts/satellite/accreditation.yaml#getAccreditationHolder)*
- **Replace**: Starts replacement with a reason; the old credential is invalidated in the same act. *(source: contracts/satellite/accreditation.yaml#replaceAccreditationCredential)*

**Data it reads**: `listAccreditationCredentials` (onLoad, Every accreditation credential issued)

**Where the user goes next**

- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential registry credential list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential registry credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential registry credential yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential registry credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Holder with several active credentials (badge + mobile)**: Both rows active under one accreditation identity, grouped by holder when filtered to one person. *(source: screens/P08-venue-back-office.yaml#BO-644)*
- **Accreditation revoked**: All the holder's credentials show Revoked with "Accreditation revoked"; revoking a credential alone does not revoke access. *(source: screens/P08-venue-back-office.yaml#BO-653 / contracts/satellite/accreditation.yaml#issueAccreditationCredential)*

#### Consistency with other screens

- Match `BO-644`: Credential search on the hub opens this register.
- Match `ACC-008`: The portal's credential register shows the organisation's subset with the same status words.
- Match `BO-362`: Guest credential evidence is a separate register; same timeline component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- credential: C-1188
  holder: Omar Haddad
  accreditation: ACR-2026-0412
  type: Printed badge + QR
  event: Summer Concert - Etihad Park
  category: Media
  issued: 1 Oct 2026
  status: Active
  replaces: C-1042
- credential: C-1042
  holder: Omar Haddad
  type: Printed badge
  status: Replaced
  replacedBy: C-1188
  reason: Damaged
- credential: C-1203
  holder: Fatima Al Hashimi
  type: Mobile credential
  category: Corporate
  status: Delivered
```

#### Permissions

- `listAccreditationCredentials` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.22 | QR Credential Support - System shall support QR-based accreditation credentials. | Accreditation & Credential Management | CONTRACTED | data `AccreditationCredential` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-653` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-653`
- Workshop pack: ACCREDITATION.pdf board 4
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 18: Works in Credential Registry & Credential History → Maintain the authoritative record of every credential issued by TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-653?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-644`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createBadgePrintJob": {"method":"POST","path":"/badge-print-jobs","contract":"accreditation","summary":"Queue badges for printing","permission":"ACCREDITATION_ISSUE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BadgePrintJob","responds":"BadgePrintJob"},
"deliverAccreditationCredential": {"method":"POST","path":"/accreditation-credentials/{credentialId}/deliver","contract":"accreditation","summary":"Send a mobile credential to its holder","permission":"ACCREDITATION_ISSUE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationCredentialDelivery"},
"issueAccreditationCredential": {"method":"POST","path":"/accreditation-credentials","contract":"accreditation","summary":"Produce a badge, a mobile credential, or both","permission":"ACCREDITATION_ISSUE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationCredential","responds":"AccreditationCredential"},
"listAccreditationAudit": {"method":"GET","path":"/accreditation-audit","contract":"accreditation","summary":"The immutable record of who granted what to whom","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"holderId","in":"query","required":null},{"name":"from","in":"query","required":null}],"requestBody":null,"responds":"AccreditationAuditRecord"},
"listAccreditationCredentials": {"method":"GET","path":"/accreditation-credentials","contract":"accreditation","summary":"Badges and digital credentials issued","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"holderId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"AccreditationCredential"},
"listAccreditationHolders": {"method":"GET","path":"/accreditation-holders","contract":"accreditation","summary":"Everybody accredited, and what state they are in","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"organisationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"listBadgePrintJobs": {"method":"GET","path":"/badge-print-jobs","contract":"accreditation","summary":"The print queue, and what failed","permission":"ACCREDITATION_ISSUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BadgePrintJob"},
"listBadgeTemplates": {"method":"GET","path":"/badge-templates","contract":"accreditation","summary":"Badge designs, and what prints on each","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BadgeTemplate"},
"replaceAccreditationCredential": {"method":"POST","path":"/accreditation-credentials/{credentialId}/replace","contract":"accreditation","summary":"Reissue after loss, damage or a name change","permission":"ACCREDITATION_ISSUE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationCredential"},
"setBadgeTemplate": {"method":"PUT","path":"/badge-templates","contract":"accreditation","summary":"Design a badge","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BadgeTemplate","responds":"BadgeTemplate"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationAuditRecord": {"type":"object","x-ticvai-persistence":"accreditation.audit","description":"Board 8.7. **Who gave this person access to that place, when, and on whose authority.**\n","properties":{"id":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"holderId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"previousRecordHash":{"type":"string","nullable":true},"recordHash":{"type":"string"},"integrity":{"type":"string","readOnly":true,"enum":["intact","broken","unverifiable"]},"scopePath":{"type":"string"}}},
"AccreditationCredential": {"type":"object","x-ticvai-persistence":"accreditation.credential","description":"Board 4. **Not the accreditation** — reissuing one re-vets nobody.","required":["holderId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["printedBadge","mobileCredential","qr","nfcCard","rfidCard","wristband"]},"symbology":{"type":"string","nullable":true,"description":"12.1.22. **How `encodedIdentifier` is carried**, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a `mobileCredential`, a barcode where a printed badge carries one, `nfcNdef` or `rfidEpc` for an encoded card, `none` where nothing is encoded.\n","enum":["qr","dataMatrix","pdf417","aztec","code128","nfcNdef","rfidEpc","none"]},"serialNumber":{"type":"string","nullable":true},"encodedIdentifier":{"type":"string","nullable":true},"badgeTemplateId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"issuedBy":{"type":"string","format":"uuid"},"activatedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["pendingPrint","issued","active","lost","replaced","revoked","expired"]},"replacesCredentialId":{"type":"string","format":"uuid","nullable":true},"replacementCount":{"type":"integer","default":0},"scopePath":{"type":"string"}}},
"AccreditationCredentialDelivery": {"type":"object","x-ticvai-persistence":"accreditation.mobile_credential_delivery","description":"12.1.21. **Issuing a mobile credential and getting it onto a phone are two acts**, and the second is recorded so *\"I never got it\"* has an answer. Written by `deliverAccreditationCredential` (the accreditation team sends it) and `issueMyAccreditationWalletPass` (the holder adds it to a wallet).\n","required":["credentialId","channel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"credentialId":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid","readOnly":true},"channel":{"type":"string","enum":["email","sms","holderApp","appleWallet","googleWallet"]},"destinationMasked":{"type":"string","nullable":true,"readOnly":true,"description":"The address or number used, masked (`j***@agency.com`). Always the holder's own"},"walletPassSerial":{"type":"string","nullable":true,"readOnly":true},"walletPassUrl":{"type":"string","nullable":true,"readOnly":true,"description":"Signed and expiring; adds the pass to the wallet"},"status":{"type":"string","readOnly":true,"enum":["queued","sent","delivered","opened","failed","superseded"]},"failureReason":{"type":"string","nullable":true,"readOnly":true},"requestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time","readOnly":true},"deliveredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationHolder": {"type":"object","x-ticvai-persistence":"accreditation.holder","description":"**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n","required":["id","fullName"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true},"nationality":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true,"description":"12.1.16. The holder's own address — where a mobile credential and renewal notices go"},"phone":{"type":"string","nullable":true,"description":"12.1.16. E.164"},"identityDocumentVerified":{"type":"boolean","default":false},"organisationId":{"type":"string","format":"uuid","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","suspended","revoked","expired","archived"]},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"completenessPercent":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"BadgePrintJob": {"type":"object","x-ticvai-persistence":"accreditation.print_job","description":"Board 4.5. **Printing fails mid-batch and the operator needs to know which landed.**","properties":{"id":{"type":"string","format":"uuid"},"credentialIds":{"type":"array","items":{"type":"string","format":"uuid"}},"printerDeviceId":{"type":"string","format":"uuid","nullable":true},"queuedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["queued","printing","completed","partiallyFailed","failed"]},"printed":{"type":"integer","readOnly":true},"failed":{"type":"integer","readOnly":true},"failures":{"type":"array","items":{"type":"object","properties":{"credentialId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}}},"scopePath":{"type":"string"}}},
"BadgeTemplate": {"type":"object","x-ticvai-persistence":"accreditation.badge_template","description":"Board 4.4. **A security artefact as much as a printed card.**","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"size":{"type":"string","nullable":true},"showPhoto":{"type":"boolean","default":true},"showZones":{"type":"boolean","default":true},"colourStripe":{"type":"string","nullable":true,"description":"**What a security officer checks at a glance.** The stripe is the control that works at ten metres in the dark.\n"},"showOrganisation":{"type":"boolean","default":true},"showValidity":{"type":"boolean","default":true},"backgroundAssetId":{"type":"string","format":"uuid","nullable":true},"securityFeatures":{"type":"array","items":{"type":"string"}},"scopePath":{"type":"string"}}}
}
```
