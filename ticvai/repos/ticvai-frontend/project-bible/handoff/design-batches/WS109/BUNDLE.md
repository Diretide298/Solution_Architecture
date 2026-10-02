# WS109 — ACCREDITATION board 2

**10 screens · 9 operations · 5 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `ACCREDITATION_APPLY, ACCREDITATION_APPROVE, ACCREDITATION_MANAGE, ACCREDITATION_VIEW`. A control nobody can use must say so,
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
| `BO-625` | Accreditation Holder Directory | B–D | 0 | 50 | 6 | 3 | 1 | 6 | — | notStarted (—) |
| `BO-626` | Accreditation Holder Profile | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-627` | Identity Details & Verification | B–D | 0 | 18 | 6 | 2 | 2 | 0 | — | notStarted (—) |
| `BO-628` | Photo Management | B–D | 0 | 18 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-629` | Document Repository | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-630` | Document Verification Queue | B–D | 0 | 0 | 6 | 2 | 0 | 6 | — | notStarted (—) |
| `BO-631` | Duplicate & Identity Conflict Detection | B–D | 3 | 0 | 6 | 0 | 2 | 2 | — | notStarted (—) |
| `BO-632` | Organization & Affiliation Management | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-633` | Profile Completeness & Compliance Monitor | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-634` | Profile History & Audit Timeline | B–D | 7 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-625, BO-626, BO-627, BO-628, BO-629, BO-630, BO-631, BO-632, BO-633 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-625` Accreditation Holder Directory

**Central searchable directory of all accreditation holders.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each holder record shall display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-holder-directory-bo-625` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The directory of every accredited person, across programmes, events and venues: one row per person, not per application, because the holder profile is the single source of truth for that person. Staff search it to answer "is this person accredited, for what, and is it still valid". The one thing to get right: rows open the person's record with the holderId, and the record's board-2 screens open as tabs of that one record rather than as separate destinations from this list.

**Known correction pending (do not draw the wrong version)**

- **Edges to BO-626, BO-627, BO-628, BO-629, BO-632, BO-633 carry nothing** Why: Each of those screens needs holderId; the edges must carry it. *(source: screens/P08-venue-back-office.yaml#BO-625; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Applicant type, identity verification status, active credentials, event or venue and last updated are not on AccreditationHolder** Why: The holder has category but not applicant type, a yes/no identityDocumentVerified instead of the pack's six states, no credential count, no event and no updatedAt; the directory needs a joined read. *(source: screens/P08-venue-back-office.yaml#BO-626 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No search and no paging on listAccreditationHolders** Why: It filters by programme, organisation, status and expiry only and returns an unpaged array. *(source: contracts/satellite/accreditation.yaml#listAccreditationHolders; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table columns list Name and Email twice after Last updated date (search keys turned into columns), label "Every accreditation holder"** Why: Search keys are not columns; generated label is a placeholder. *(source: screens/P08-venue-back-office.yaml#BO-626; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the directory tenant-wide (one person across venues) or per venue?** → Drawn default accepted: Per the venue switcher, with a tenant-wide toggle for tenant-scope users. *(decided by Chinmay, 2026-10-02; DEC-455 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationHolders` ?programmeId |
| Organisation | picker: choose an organisation | — | — | `listAccreditationHolders` ?organisationId |
| Status | text field | — | — | `listAccreditationHolders` ?status |
| Expiring within days | number field (days) | — | — | `listAccreditationHolders` ?expiringWithinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search**: Name, holder ID (accreditation number), email, mobile, organisation, accreditation ID or credential ID in one box. Passport or ID number search is a separate exact-match field shown only to users permitted to search by it, and each use is logged. *(source: screens/P08-venue-back-office.yaml#BO-626 / ADR-0063)*
- **Filters**: Category, Applicant type, Event, Venue, Organisation, Verification status, Accreditation status, Credential status, Expiring within (7, 30, 90 days). *(source: screens/P08-venue-back-office.yaml#BO-626 / contracts/satellite/accreditation.yaml#listAccreditationHolders)*

#### Outputs: what the screen shows and produces

**Shown**

**Every accreditation holder** (data table)

| Shows | Format | Notes |
|---|---|---|
| Holder ID | text | not in the schema: `Holder ID` |
| Profile photograph | text | not in the schema: `Profile photograph` |
| Full name | text | not in the schema: `Full name` |
| Accreditation category | text | not in the schema: `Accreditation category` |
| Applicant type | text | not in the schema: `Applicant type` |
| Organization/company | text | not in the schema: `Organization/company` |
| Current accreditation status | text | not in the schema: `Current accreditation status` |
| Identity verification status | text | not in the schema: `Identity verification status` |
| Active credentials | text | not in the schema: `Active credentials` |
| Linked event/venue | text | not in the schema: `Linked event/venue` |
| Expiry status | text | not in the schema: `Expiry status` |
| Last updated date | text | not in the schema: `Last updated date` |
| Name | text | not in the schema: `Name` |
| Email | text | not in the schema: `Email` |
| Mobile | text | not in the schema: `Mobile` |
| Passport/id number where permitted | text | not in the schema: `Passport/ID number where permitted` |
| Organization | text | not in the schema: `Organization` |
| Accreditation ID | text | not in the schema: `Accreditation ID` |
| Credential ID | text | not in the schema: `Credential ID` |
| Category | text | not in the schema: `Category` |
| Event | text | not in the schema: `Event` |
| Venue | text | not in the schema: `Venue` |
| Verification status | text | not in the schema: `Verification status` |
| Accreditation status | text | not in the schema: `Accreditation status` |
| Credential status | text | not in the schema: `Credential status` |

**The selected accreditation holder** (detail panel): The pack groups this record's detail under its own headings: “Scope of Work”.

| Shows | Format | Notes |
|---|---|---|
| Holder ID | text | not in the schema: `Holder ID` |
| Profile photograph | text | not in the schema: `Profile photograph` |
| Full name | text | not in the schema: `Full name` |
| Accreditation category | text | not in the schema: `Accreditation category` |
| Applicant type | text | not in the schema: `Applicant type` |
| Organization/company | text | not in the schema: `Organization/company` |
| Current accreditation status | text | not in the schema: `Current accreditation status` |
| Identity verification status | text | not in the schema: `Identity verification status` |
| Active credentials | text | not in the schema: `Active credentials` |
| Linked event/venue | text | not in the schema: `Linked event/venue` |
| Expiry status | text | not in the schema: `Expiry status` |
| Last updated date | text | not in the schema: `Last updated date` |
| Name | text | not in the schema: `Name` |
| Email | text | not in the schema: `Email` |
| Mobile | text | not in the schema: `Mobile` |
| Passport/id number where permitted | text | not in the schema: `Passport/ID number where permitted` |
| Organization | text | not in the schema: `Organization` |
| Accreditation ID | text | not in the schema: `Accreditation ID` |
| Credential ID | text | not in the schema: `Credential ID` |
| Category | text | not in the schema: `Category` |
| Event | text | not in the schema: `Event` |
| Venue | text | not in the schema: `Venue` |
| Verification status | text | not in the schema: `Verification status` |
| Accreditation status | text | not in the schema: `Accreditation status` |
| Credential status | text | not in the schema: `Credential status` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Holders table**: Columns: Holder ID (accreditation number, not the uuid), Photo, Full name (English, Arabic beneath), Category, Applicant type, Organisation, Accreditation status (Active, Suspended, Revoked, Expired, Archived), Identity verification, Active credentials (count with kind icons), Event or venue, Expiry ("Expires in 12 days" amber inside 30 days, red when expired), Last updated. Title "Accreditation holders". Cursor paging. *(source: screens/P08-venue-back-office.yaml#BO-625 / screens/P08-venue-back-office.yaml#BO-626 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder)*
- **Readiness indicator**: A small ring with completenessPercent beside the name, coloured by the BO-633 readiness state. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open**: Opens the holder record (BO-626) with holderId; tabs inside it are Identity, Photo, Documents, Organisation, Readiness, History. *(source: DI-671)*
- **Suspend**: For permitted users, opens the suspension dialog (reason required, review date optional) naming what stops working. *(source: screens/P08-venue-back-office.yaml#BO-626 / contracts/satellite/accreditation.yaml#setAccreditationStatus)*
- **Verification queue / Possible duplicates**: Two buttons in the header with counts, opening BO-630 and BO-631; these are cross-holder work queues, not tabs of one record. *(source: screens/P08-venue-back-office.yaml#BO-630)*

**Data it reads**: `listAccreditationHolders` (onLoad, The holder directory)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-626` Accreditation Holder Profile: *Accreditation Holder Profile*
- → `BO-627` Identity Details & Verification: *Identity Details & Verification*
- → `BO-628` Photo Management: *Photo Management*
- → `BO-629` Document Repository: *Document Repository*
- → `BO-630` Document Verification Queue: *Document Verification Queue*
- → `BO-631` Duplicate & Identity Conflict Detection: *Duplicate & Identity Conflict Detection*
- → `BO-632` Organization & Affiliation Management: *Organization & Affiliation Management*
- → `BO-633` Profile Completeness & Compliance Monitor: *Profile Completeness & Compliance Monitor*
- → `BO-634` Profile History & Audit Timeline: *Profile History & Audit Timeline*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation holder list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation holder untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation holder yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation holder are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Holder whose accreditations have all expired**: Still listed (status Expired); the profile persists across programmes. *(source: screens/P08-venue-back-office.yaml#BO-627)*
- **Search by passport number without permission**: The field is shown disabled with the permission named (per VO-R08). *(source: ADR-0063)*

#### Consistency with other screens

- Match `BO-297`: The 7 September decision makes accreditation-holder monitoring a filtered view of general entitlement monitoring; this directory is the record list, while monitoring of holders lives there with an "Accredited" filter.
- Match `BO-616`: Same search box behaviour and status chips.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- holderId: SP26-CON-00318
  name: Rahul Menon
  category: Contractor
  type: Rigging crew
  organisation: Falcon Stage Rigging LLC
  status: Active
  identity: Verified
  credentials: 1 mobile, 1 printed
  event: Winter Festival 2026
  expiry: Expires in 64 days
  updated: 09 Oct 2026
- holderId: SP26-MED-00041
  name: Sara Al Nuaimi
  category: Media
  type: Photographer
  organisation: Gulf Lens Media
  status: Active
  identity: Pending
  credentials: '0'
  event: Winter Festival 2026
  expiry: '-'
  updated: 11 Oct 2026
- holderId: AP27-CON-00007
  name: Omar Haddad
  category: Contractor
  type: Pool maintenance
  organisation: Falcon Stage Rigging LLC
  status: Suspended
  identity: Verified
  credentials: 1 printed (suspended)
  event: Aqua Park
  expiry: Expires in 9 days
  updated: 05 Oct 2026
```

#### Permissions

- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Accreditation-holder monitoring is a filtered view inside the general entitlement monitoring, not a separate platform, so staff can quickly distinguish and support large accredited groups. *(agreed · MoM 7 Sep 2026, 4.10 Entitlements Lifecycle, Consumption Monitoring & Screen Consolidation · DI-672)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-625` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-625`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 1: Opens Accreditation Holder Directory → Central searchable directory of all accreditation holders.
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F218 branch at step 1 (expected): when Nothing has been set up on Accreditation Holder Directory yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F218 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (50 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-625?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-626`, `BO-627`, `BO-628`, `BO-629`, `BO-630`, `BO-631`, `BO-632`, `BO-633`, `BO-634`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-626` Accreditation Holder Profile

**Master profile screen for an accredited person.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/accreditation-holder-profile-bo-626` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The holder record: one person, with identity, photo, organisation, current accreditations, credentials, access rights, documents, verification state, renewal history and audit history, kept even after every accreditation has expired. It is the container for the board-2 screens, drawn as one record with tabs (per VO-R14). The one thing to get right: the header always answers "can this person get in, where, until when", before any detail.

**Known correction pending (do not draw the wrong version)**

- **getAccreditationHolder is triggered onAction** Why: The profile is a read on load. *(source: screens/P08-venue-back-office.yaml#BO-626 / contracts/satellite/accreditation.yaml#getAccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **getAccreditationHolder promises "identity, documents, access and history" but returns AccreditationHolder only** Why: Documents, credentials, access, applications and audit each need their own read (listAccreditationDocuments, listAccreditationCredentials, HolderAccess, listAccreditationAudit), none bound here. *(source: contracts/satellite/accreditation.yaml#getAccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Preferred name, gender, address, job title, department, emergency contact, internal notes and external reference IDs have no field** Why: AccreditationHolder holds fullName, date of birth, nationality, email, phone and affiliationRole only. *(source: screens/P08-venue-back-office.yaml#BO-627 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **An empty detailPanel; gap says nothing can be drawn** Why: The pack lists fifteen profile fields and eight summary areas. *(source: screens/P08-venue-back-office.yaml#BO-626 / screens/P08-venue-back-office.yaml#BO-627; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The holder carries a single programmeId, categoryCode, validFrom and validTo** Why: The pack makes the profile the single source of truth across programmes, events and venues; one programme per holder record forces a second record for the same person in the next programme, which is the duplicate the board exists to prevent. *(source: screens/P08-venue-back-office.yaml#BO-625 / screens/P08-venue-back-office.yaml#BO-633 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Can a holder have accreditations in two programmes at once (one record, two programmeIds)?** → Drawn default accepted: Yes in the design (one record listing several accreditations). *(decided by Chinmay, 2026-10-02; DEC-456 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Profile fields (Edit)**: Full legal name, preferred display name, date of birth, nationality where applicable, gender where required, email, mobile (E.164), address where configured, job title, department, emergency contact where configured, internal notes (staff only, never on a badge), external reference IDs. Fields marked "where configured" appear only if the programme's form defines them. *(source: screens/P08-venue-back-office.yaml#BO-626 / screens/P08-venue-back-office.yaml#BO-627 / contracts/satellite/accreditation.yaml#updateAccreditationHolder)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Header**: Photo, name (English and Arabic), accreditation number, status chip, category colour, organisation, "Valid 01-14 Dec 2026", and a one-line access summary ("Opens Main stage build area, Loading dock, Crew catering"). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess)*
- **Summary cards**: Current accreditations, Credentials (kind, status), Access rights (zones, exceptions with end dates), Verification (identity, documents verified x of y), Documents (expiring soon highlighted), Events and venues, Renewal history, Audit history (last five, link to the History tab). *(source: screens/P08-venue-back-office.yaml#BO-627)*
- **Tabs**: Overview, Identity (BO-627), Photo (BO-628), Documents (BO-629), Organisation (BO-632), Readiness (BO-633), History (BO-634). *(source: DI-671)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Suspend / Reactivate / Revoke**: Status dialog with reason (required) and optional review date; revoke states every credential stops working now. *(source: contracts/satellite/accreditation.yaml#setAccreditationStatus)*
- **Renew**: Opens a renewal application prefilled from the holder and documents still in date. *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*
- **Issue credential**: Opens BO-645 for this holder when an approved accreditation exists; otherwise disabled with the reason. *(source: screens/P08-venue-back-office.yaml#BO-645)*

**Where the user goes next**

- → `BO-625` Accreditation Holder Directory: *Back to Accreditation Holder Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation holder profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation holder profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation holder profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation holder profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **All accreditations expired**: The record stays; header says "No current accreditation - last valid to 14 Dec 2025" and offers Renew. *(source: screens/P08-venue-back-office.yaml#BO-627)*
- **Holder archived by a duplicate merge**: A banner "Merged into SP26-CON-00211 on 03 Oct 2026" with a link; the record is read-only. *(source: contracts/satellite/accreditation.yaml#resolveIdentityConflict)*

#### Consistency with other screens

- Match `BO-625`: Opened from the directory with holderId; Back returns with filters kept.
- Match `ACC-007`: The reviewer's "History with this venue" draws from the same history.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holder:
  accreditationNumber: SP26-CON-00318
  name: Rahul Menon
  preferredName: Rahul
  organisation: Falcon Stage Rigging LLC
  category: Contractor
  status: Active
  valid: 01-14 Dec 2026
  access: Main stage build area, Loading dock, Crew catering
  completeness: 92
```

#### Permissions

- `getAccreditationHolder` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-626` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-626`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 2: Works in Accreditation Holder Profile → Master profile screen for an accredited person.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-626?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-625`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-627` Identity Details & Verification

**Capture identity data and verify the holder before approval.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/identity-details-verification-bo-627` |

**What the spec says about it.** **UAE Pass and the ICP identity check are integrated in release 1, needing the client's access (decided 2 October 2026 by Chinmay, DEC-457; CHG-CSP-034, CHG-CSA-031).** The holder's verification shows which service verified it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Identity tab of the holder record: the person's identity document details, captured by OCR from the uploaded Emirates ID or passport and confirmed by staff, and the verification of that identity before approval. The one thing to get right: the document number is entered or read once, stored encrypted, shown masked thereafter, and checked for uniqueness so the same person cannot hold two records.

**Known correction pending (do not draw the wrong version)**

- **AccreditationHolder has no identity document fields** Why: Passport number, national ID, Emirates ID, issuing country, issue and expiry dates, verification status, method, source, reference, verifier and time have nowhere to be saved; only a yes/no identityDocumentVerified exists. DI-691 requires them as structured fields. *(source: screens/P08-venue-back-office.yaml#BO-627 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder / DI-691; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No encrypted storage or blind index for the number** Why: ADR-0063 requires application-level encryption of identity document numbers with a keyed hash for lookup, which is also what the duplicate block needs. *(source: ADR-0063 / DI-692; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Button "Save accreditation holder"** Why: Generated label; on this tab it is "Save identity". *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which third-party identity or government verification services are in scope (for example UAE Pass or ICP checks)?** → UAE Pass and ICP verification integrated in release 1 (needs client access). *(decided by Chinmay, 2026-10-02; DEC-457 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Document type**: Closed set (Emirates ID, Passport, National ID, Residence permit, Other), chips not free text. *(source: screens/P08-venue-back-office.yaml#BO-627 / contracts/spine/identity.yaml#/components/schemas/IdentityGuestDocumentSubmission)*
- **Document number**: Emirates ID 784-YYYY-NNNNNNN-C with check digit; passport 6-9 letters and digits. After save shown as "Emirates ID ending 5671"; a Reveal action exists only for permitted users, is logged, and hides again after 30 seconds. *(source: ADR-0063 / DI-692)*
- **Issuing country, issue date, expiry date, date of birth, legal name**: Country as a select; issue date not in the future; expiry after issue; legal name as on the document (may differ from preferred name). An expiry before the end of the person's event shows a red flag "Expires before the event". *(source: screens/P08-venue-back-office.yaml#BO-627 / DI-663)*
- **OCR read**: "Read from document" on upload fills the fields; each OCR value shows its confidence and a "Confirm" tick; low-confidence values are left blank. The original image stays beside the fields for comparison. *(source: DI-658 / DI-691 / TRACKER Actions row 240)*
- **Verification**: Status (Not started, Pending, Verified, Failed, Manual review, Expired), method (Manual review, Third-party identity check, Document validation service, Government or authority check), source and reference; Failed and Manual review require a reason. UAE Pass and ICP checks are integrated in release 1 (the client provides the access). *(source: screens/P08-venue-back-office.yaml#BO-628 / MATRIX 12.1.19 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Outputs: what the screen shows and produces

**Shown**

**Holder** (detail panel, from `getAccreditationHolder`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save accreditation holder (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Verification record**: "Verified by Ahmed Al Mansoori, 09 Oct 2026 11:20, manual review against original" kept as a history list, newest first. *(source: screens/P08-venue-back-office.yaml#BO-628)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save identity**: Writes the holder (the whole record, per VO-R04; status and other tabs' fields sent unchanged). Confirmation only when the number changes ("Changing the document number re-runs the duplicate check"). *(source: contracts/satellite/accreditation.yaml#updateAccreditationHolder)*
- **Mark verified / failed**: Records the outcome with method and reason; Verified sets the holder's identity as verified and clears the approval blocker. *(source: screens/P08-venue-back-office.yaml#BO-628 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder)*

**Data it reads**: `getAccreditationHolder` (onLoad, The holder as saved, to edit)

**Where the user goes next**

- → `BO-625` Accreditation Holder Directory: *Back to Accreditation Holder Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The identity details verification list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the identity details verification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No identity details verification yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the identity details verification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Number matches another holder**: Save refused with a link to the other record and to BO-631; nothing is saved. *(source: DI-692 / DI-659)*
- **Document expires before the event**: A resubmission request to the holder is offered ("Ask for a renewed Emirates ID by 01 Feb"); the credential is blocked if unresolved. *(source: DI-663 / MoM 2026-09-07 4.6)*

#### Consistency with other screens

- Match `ACC-002`: The applicant sees the same fields and masked format; the OCR tag reads the same.
- Match `BO-630`: Verifying the identity document in the queue and here is the same act and shows the same record.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
document:
  type: Emirates ID
  number: ending 5671
  issuingCountry: United Arab Emirates
  issued: 03 Feb 2022
  expires: 02 Feb 2027
  legalName: Rahul Menon Kumar
  dateOfBirth: 14 Mar 1991
verification:
  status: Verified
  method: Manual review
  by: Ahmed Al Mansoori
  at: 09 Oct 2026 11:20
```

#### Permissions

- `updateAccreditationHolder` → `ACCREDITATION_MANAGE` (configure) · staff
- `getAccreditationHolder` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.16 | Profile Management - System shall maintain detailed accreditation holder profiles. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |
| 12.1.17 | Photo Management - System shall support accreditation holder photographs. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*
- Allam asked, Chinmay confirmed: uploading an ID (e.g. Emirates ID image or PDF from phone or laptop) auto-fills form fields (ID number, expiry) via OCR; data is stored as structured fields to track expiry and prompt renewal. *(agreed · MoM 7 Sep 2026, 4.3 OCR Auto-Fill / 5. Key Decisions · DI-658)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-627` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-627`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 4: Works in Identity Details & Verification → Capture identity data and verify the holder before approval.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-627?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save accreditation holder, Cancel.
- [ ] Every transition is wired: `BO-625`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-628` Photo Management

**Manage accreditation holder photographs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/photo-management-bo-628` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Photo tab of the holder record: upload or capture the badge photo, crop it for the badge, check it against the venue's photo rules, and approve or reject it, with the history of earlier photos. The one thing to get right: replacing an approved photo on a person whose badge is already printed means a reprint, and the screen says so before saving.

**Known correction pending (do not draw the wrong version)**

- **The contract holds only photoAssetId** Why: Approval status, approving user, rejection reason, upload metadata, photo history and the photo rules have no fields or operations. *(source: screens/P08-venue-back-office.yaml#BO-628 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder / MATRIX 12.1.17; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Button "Save accreditation holder"** Why: On this tab the actions are Approve photo, Reject photo and Replace photo. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Saving a photo writes the whole holder (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How recent must a photo be (the pack's recency rule)?** → Drawn default accepted: 12 months, shown as a configurable rule. *(decided by Chinmay, 2026-10-02; DEC-458 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Photo source**: Upload (JPEG or PNG) or Capture from an authorised desk camera; the camera list comes from the device register. *(source: screens/P08-venue-back-office.yaml#BO-628 / ADR-0067)*
- **Crop**: Fixed badge aspect from the category's badge template, with face guide lines (eyes on the upper third), rotate and zoom. *(source: screens/P08-venue-back-office.yaml#BO-628 / contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate)*
- **Photo rules (settings link)**: Accepted format, minimum resolution, maximum size, background, face visibility, recency; each check shown pass or fail under the preview. *(source: screens/P08-venue-back-office.yaml#BO-628)*
- **Rejection reason**: Closed set (Face not visible, Background not plain, Too old, Low resolution, Not the applicant) plus a note; the applicant reads the reason. *(source: screens/P08-venue-back-office.yaml#BO-628)*

#### Outputs: what the screen shows and produces

**Shown**

**Holder** (detail panel, from `getAccreditationHolder`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save accreditation holder (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Preview on badge**: The cropped photo inside a miniature of the holder's badge template, so staff see it as printed. *(source: contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate)*
- **Photo history**: Earlier photos with upload date, uploaded by, approval status and approving user. *(source: screens/P08-venue-back-office.yaml#BO-629)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Approve photo / Reject photo**: Approve sets it as the holder's photo; Reject keeps the previous approved photo and notifies the applicant with the reason. *(source: screens/P08-venue-back-office.yaml#BO-628)*
- **Replace photo**: When a printed badge exists, confirmation says "The printed badge SP26-B-00318 will need replacing (reason Photo change)" and offers to queue the replacement. *(source: contracts/satellite/accreditation.yaml#replaceAccreditationCredential)*

**Data it reads**: `getAccreditationHolder` (onLoad, The holder as saved, with the current photo)

**Where the user goes next**

- → `BO-625` Accreditation Holder Directory: *Back to Accreditation Holder Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The photo list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the photo untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No photo yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the photo are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Face Pass enabled at the venue**: The approved photo can be referenced by the face credential only with the person's consent; the photo is not a biometric template, which stays with the biometric vendor. *(source: screens/P08-venue-back-office.yaml#BO-629 / ADR-0063)*
- **Camera offline**: Capture greyed with "Desk camera not connected"; Upload still works. *(source: designer default)*

#### Consistency with other screens

- Match `BO-647`: Crop aspect and preview use the badge template's size.
- Match `ACC-002`: The applicant's photo guide states the same rules.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
current:
  uploaded: 07 Oct 2026 21:14
  by: Applicant (portal)
  status: Approved
  approvedBy: Maria Santos
history:
- uploaded: 02 Oct 2025
  status: Approved
  note: Winter Festival 2025
```

#### Permissions

- `updateAccreditationHolder` → `ACCREDITATION_MANAGE` (configure) · staff
- `getAccreditationHolder` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.16 | Profile Management - System shall maintain detailed accreditation holder profiles. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |
| 12.1.17 | Photo Management - System shall support accreditation holder photographs. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-628` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-628`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 6: Works in Photo Management → Manage accreditation holder photographs.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-628?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save accreditation holder, Cancel.
- [ ] Every transition is wired: `BO-625`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-629` Document Repository

**Store and manage accreditation-related supporting documents.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_APPLY`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/document-repository-bo-629` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Documents tab of the holder record: every document the person has supplied, each against the requirement it satisfies, with its expiry, verification state and versions; staff can upload on the person's behalf. The one thing to get right: a document is always tied to a named requirement, and a document that lapses before the person's accreditation does is shown as the limit on that accreditation.

**Known correction pending (do not draw the wrong version)**

- **No holderId entry parameter** Why: The repository is per holder (listAccreditationDocuments by holderId); the screen must receive it. *(source: screens/P08-venue-back-office.yaml#BO-629 / contracts/satellite/accreditation.yaml#listAccreditationDocuments; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Issue date, uploaded by, notes and version history have no field** Why: AccreditationDocument carries submittedAt, status, verifier, rejection reason and expiry only. *(source: screens/P08-venue-back-office.yaml#BO-629 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationDocument; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Upload uses ACCREDITATION_APPLY and download has no permission distinction** Why: The pack requires role permissions for viewing or downloading sensitive files; there is no separate permission to gate them. *(source: screens/P08-venue-back-office.yaml#BO-629 / contracts/satellite/accreditation.yaml#submitAccreditationDocument; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Buttons "Submit" and "Cancel"** Why: The action is "Upload document". *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Application | picker: choose an application | — | — | `listAccreditationDocuments` ?applicationId |
| Holder | picker: choose a holder | — | — | `listAccreditationDocuments` ?holderId |
| Requirement code | text field | — | — | `listAccreditationDocuments` ?requirementCode |
| Status | radio group | — | Submitted · Verified · Rejected · Expired | `listAccreditationDocuments` ?status |
| Expiring within days | number field (days) | — | min 0 | `listAccreditationDocuments` ?expiringWithinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Requirement**: Select from the requirement rows that apply to this holder's category and applicant type (closed list); never a free "document type". *(source: contracts/satellite/accreditation.yaml#submitAccreditationDocument / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*
- **File**: PDF, JPEG or PNG within the size limit, refused at upload with the limit named. *(source: DI-657)*
- **Issue date, expiry date, notes**: Expiry required for requirements with an expiry; issue date and notes optional. *(source: screens/P08-venue-back-office.yaml#BO-629 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationDocument)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Documents table**: Columns Document (requirement label), File name, Issued, Expires ("Expires before accreditation ends" in red when earlier than validTo), Verification (Submitted, Verified, Rejected with reason, Expired), Uploaded by, Uploaded at, Versions (count). Filter "Expiring within 30 days". *(source: screens/P08-venue-back-office.yaml#BO-629 / contracts/satellite/accreditation.yaml#listAccreditationDocuments)*
- **Viewer**: Opens the file inline for permitted users; downloading sensitive documents (passport, ID) needs its own permission and is logged. *(source: screens/P08-venue-back-office.yaml#BO-629)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Upload document**: Submits against the requirement; the row appears as Submitted and enters the verification queue (BO-630). *(source: contracts/satellite/accreditation.yaml#submitAccreditationDocument)*
- **Upload new version**: Supersedes the previous file for that requirement; earlier versions remain in the version list. *(source: screens/P08-venue-back-office.yaml#BO-629)*

**Data it reads**: `listAccreditationDocuments` (onLoad, Documents stored, by holder or application)

**Where the user goes next**

- → `BO-625` Accreditation Holder Directory: *Back to Accreditation Holder Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The document repository list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the document repository untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No document repository yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the document repository are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Insurance certificate lapses mid-accreditation**: The accreditation's effective end is shown as the certificate's expiry, and the holder is listed in the expiry monitor. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationDocument / DI-663)*
- **Viewer lacks permission to see identity documents**: The row shows "Restricted" with the permission named; metadata still visible. *(source: screens/P08-venue-back-office.yaml#BO-629)*

#### Consistency with other screens

- Match `BO-630`: Verification states and refusal reasons are the same as in the queue.
- Match `ACC-004`: An applicant adding a requested document creates a row here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
documents:
- document: Emirates ID
  file: rahul-eid-front.jpg
  expires: 02 Feb 2027
  verification: Verified
  uploadedBy: Applicant
  at: 07 Oct 2026 21:10
  versions: 1
- document: Contractor authorisation
  file: falcon-authorisation.pdf
  expires: 31 Dec 2026
  verification: Submitted
  uploadedBy: Fatima Al Hashimi
  at: 08 Oct 2026 10:02
  versions: 2
- document: Public liability insurance
  file: falcon-insurance-2026.pdf
  expires: 05 Dec 2026
  verification: Verified
  note: Expires before accreditation ends
```

#### Open questions on this screen

Draw the default until it is answered.

- **How long are rejected and superseded document files kept?** Default: Show "Kept until the programme's retention date" without a date. *(source: screens/P08-venue-back-office.yaml#BO-633)*

#### Permissions

- `submitAccreditationDocument` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `listAccreditationDocuments` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.18 | Document Management - System shall support storage of accreditation-related documents. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |
| 12.1.19 | Identity Verification - System shall support identity verification before accreditation approval. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam asked, Chinmay confirmed: uploading an ID (e.g. Emirates ID image or PDF from phone or laptop) auto-fills form fields (ID number, expiry) via OCR; data is stored as structured fields to track expiry and prompt renewal. *(agreed · MoM 7 Sep 2026, 4.3 OCR Auto-Fill / 5. Key Decisions · DI-658)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-629` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-629`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 8: Works in Document Repository → Store and manage accreditation-related supporting documents.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-629?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Submit, Cancel.
- [ ] Every transition is wired: `BO-625`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-630` Document Verification Queue

**Operational review queue for uploaded accreditation documentation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `documentId` (navigation) |
| Route | `/access-venue/document-verification-queue-bo-630` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The cross-holder queue of documents waiting to be checked, oldest first, for document reviewers who verify that each file is the right document, legible and valid. The one thing to get right: the reviewer sees the file, the requirement it claims to satisfy and the extracted values side by side, and every refusal carries a reason code that tells the applicant what to do.

**Known correction pending (do not draw the wrong version)**

- **Pack actions Request replacement, Escalate and Add comment have no operation** Why: verifyAccreditationDocument records verified, rejected, illegible, wrongDocument or expired only. *(source: screens/P08-venue-back-office.yaml#BO-630 / contracts/satellite/accreditation.yaml#verifyAccreditationDocument; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Assigned reviewer and SLA ageing have no source** Why: Documents carry no assignee and there is no document SLA setting. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationDocument; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Buttons "Verify" and "Cancel" only** Why: The outcomes are Approve and Reject with a reason; the screen is a queue with a review pane. *(source: screens/P08-venue-back-office.yaml#BO-630; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation only back to BO-625** Why: It is a cross-holder work queue; it should also be reachable from BO-615 alerts and BO-623. *(source: screens/P08-venue-back-office.yaml#BO-624; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What is the document review SLA, and is it per requirement?** → Drawn default accepted: One programme-wide target (2 working days), shown in the column caption. *(decided by Chinmay, 2026-10-02; DEC-460 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Application | picker: choose an application | — | — | `listAccreditationDocuments` ?applicationId |
| Holder | picker: choose a holder | — | — | `listAccreditationDocuments` ?holderId |
| Requirement code | text field | — | — | `listAccreditationDocuments` ?requirementCode |
| Status | radio group | — | Submitted · Verified · Rejected · Expired | `listAccreditationDocuments` ?status |
| Expiring within days | number field (days) | — | min 0 | `listAccreditationDocuments` ?expiringWithinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Requirement (document type), Programme, Category, Organisation, Submitted between, Expiring within, Assigned to me. *(source: screens/P08-venue-back-office.yaml#BO-630 / contracts/satellite/accreditation.yaml#listAccreditationDocuments)*
- **Outcome**: Approve (Verified), or Reject with a reason code (Illegible, Wrong document, Expired, Other) and optional reviewer notes; the reason is required for every refusal. *(source: screens/P08-venue-back-office.yaml#BO-630 / contracts/satellite/accreditation.yaml#verifyAccreditationDocument)*
- **Expiry on verify**: Pre-filled from OCR or the applicant; the reviewer confirms or corrects it, since it limits the accreditation. *(source: contracts/satellite/accreditation.yaml#verifyAccreditationDocument)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Verify (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Queue table**: Columns Holder, Document, Related application (reference), Submitted, Expiry, Status, Assigned reviewer, Waiting (ageing: "2 days", amber after the document SLA, red when overdue). Oldest first. Cursor paging. *(source: screens/P08-venue-back-office.yaml#BO-630 / contracts/satellite/accreditation.yaml#listAccreditationDocuments)*
- **Review pane**: File viewer (zoom, rotate) on the left; requirement label and description, extracted fields and the holder's photo on the right. *(source: DI-659 / DI-658)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Approve**: Marks Verified with the reviewer and time; the next document opens. *(source: contracts/satellite/accreditation.yaml#verifyAccreditationDocument)*
- **Reject**: Marks refused with the reason; the application's checklist shows the requirement unmet and the applicant is told what to replace. *(source: contracts/satellite/accreditation.yaml#verifyAccreditationDocument / DI-663)*
- **Request replacement / Escalate / Add comment**: Drawn per the pack; greyed with "Not yet supported" until the contract carries them (per VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-630)*
- **Bulk approve**: For permitted reviewers on selected rows of the same requirement; results reported per row ("12 verified, 1 failed - already decided"). *(source: screens/P08-venue-back-office.yaml#BO-630)*

**Data it reads**: `listAccreditationDocuments` (onLoad, The queue: status=submitted, oldest first)

**Where the user goes next**

- → `BO-625` Accreditation Holder Directory: *Back to Accreditation Holder Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The document verification queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the document verification queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No document verification queue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the document verification queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Document decided by another reviewer**: The row leaves the queue with "Verified by Maria Santos 14:02". *(source: designer default)*
- **OCR expiry disagrees with what the applicant typed**: Both values shown, the difference highlighted, the reviewer chooses. *(source: DI-658)*

#### Consistency with other screens

- Match `ACC-007`: The same verify control and reason codes appear inside the application review.
- Match `BO-627`: Verifying an identity document here updates the holder's identity verification shown there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- holder: Sara Al Nuaimi
  document: Media identification
  application: ACR-2026-004390
  submitted: 08 Oct 2026
  expiry: 31 Mar 2027
  waiting: 3 days
- holder: James Carter
  document: Passport
  application: ACR-2026-004402
  submitted: 09 Oct 2026
  expiry: 19 Jun 2031
  waiting: 2 days
- holder: Priya Nair
  document: Employment letter
  application: ACR-2026-004411
  submitted: 10 Oct 2026
  expiry: '-'
  waiting: 1 day
```

#### Permissions

- `verifyAccreditationDocument` → `ACCREDITATION_APPROVE` (operate) · staff
- `listAccreditationDocuments` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.18 | Document Management - System shall support storage of accreditation-related documents. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |
| 12.1.19 | Identity Verification - System shall support identity verification before accreditation approval. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-630` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-630`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 10: Works in Document Verification Queue → Operational review queue for uploaded accreditation documentation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-630?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Verify, Cancel.
- [ ] Every transition is wired: `BO-625`.
- [ ] Every gated control is gated: `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-631` Duplicate & Identity Conflict Detection

**Prevent duplicate holder records and potential identity conflicts.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `conflictId` (navigation) |
| Route | `/access-venue/duplicate-identity-conflict-detection-bo-631` |

**What the spec says about it.** **Face matching for accreditation duplicates runs only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default (decided 2 October 2026 by Chinmay, DEC-461; CHG-CSP-022, `biometrics.accreditationFaceMatching`).**

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): resolveIdentityConflict has no link or escalate outcome.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The cross-holder queue of suspected duplicates: pairs of holder records that may be the same person, found by name and date of birth, email, mobile, organisation or face match, with a confidence. A reviewer decides: the same person (merge, keeping one record) or different people (dismiss, never raised again). The one thing to get right: merging invalidates the other record's credentials at every gate at once, and the confirm says exactly which credentials stop working.

**Known correction pending (do not draw the wrong version)**

- **The duplicate rule is enforced only as a pending conflict** Why: The application is accepted and a conflict queued, whereas the client agreed an identical passport or Emirates ID is blocked at submission; this queue should hold fuzzy matches only. *(source: contracts/satellite/accreditation.yaml#createAccreditationApplication / DI-692; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The list read has no status filter or paging, and the dataTable has no columns** Why: Pending and resolved need separating; columns come from AccreditationIdentityConflict. *(source: contracts/satellite/accreditation.yaml#listAccreditationIdentityConflicts; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Pack actions Confirm duplicate, Link records and Escalate for investigation (CHG-WIR-004)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is face matching legally enabled for accreditation duplicates?** → Face matching for accreditation duplicates only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default. *(decided by Chinmay, 2026-10-02; DEC-461 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Form: Resolve identity conflict** (modal, opened by *Resolve identity conflict*; *Resolve identity conflict* calls `resolveIdentityConflict`, *Cancel* sends nothing)

**Collects what `resolveIdentityConflict` sends before it is called.** Required: `outcome`, `reason`. Optional: `survivingHolderId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | segmented control | required | — | Merged · Rejected | — | — | `resolveIdentityConflict` body |
| Surviving holder `survivingHolderId` | picker: choose a surviving holder | optional | — | — | shows names, sends the id | Required when outcome is merged; one of the conflict's holderIds | `resolveIdentityConflict` body |
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | — | `resolveIdentityConflict` body |

Errors to draw in the form: 409 The conflict is already merged or rejected; 422 survivingHolderId missing for merged, or not one of the conflict's holders

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Outcome**: Merge (same person) or Dismiss (different people); Merge requires choosing which record survives. *(source: contracts/satellite/accreditation.yaml#resolveIdentityConflict)*
- **Surviving record**: Radio between the records, defaulting to the one with an active accreditation; must be one of the pair. *(source: contracts/satellite/accreditation.yaml#resolveIdentityConflict)*
- **Reason**: Required, 1 to 500 characters (e.g. "Same Emirates ID, name transliterated differently"). *(source: contracts/satellite/accreditation.yaml#resolveIdentityConflict)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Resolve identity conflict (primary button) | `resolveIdentityConflict` POST `/accreditation-identity-conflicts/{conflictId}/resolve` | inline | AccreditationIdentityConflict | 409 The conflict is already merged or rejected; 422 survivingHolderId missing for merged, or not one of the conflict's holders | gated `ACCREDITATION_MANAGE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Conflicts list**: Columns: Records (two names and photos), Matched on (chips: Name and date of birth, Email, Mobile, Organisation, Face), Confidence (High 90 percent and above, Medium, Low, with the number), Different access (warning icon), Detected. Pending first; a Resolved tab lists merged and dismissed pairs with who and why. *(source: screens/P08-venue-back-office.yaml#BO-630 / contracts/satellite/accreditation.yaml#listAccreditationIdentityConflicts)*
- **Compare view**: The two records side by side, differing fields highlighted, each with its accreditations, credentials and access. *(source: screens/P08-venue-back-office.yaml#BO-630 / screens/P08-venue-back-office.yaml#BO-632)*
- **Face match**: Offered only where the venue has enabled face matching for duplicates, with applicant consent and the venue's legal sign-off; off by default. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Merge records**: Confirm per VO-R16: "Keep SP26-CON-00211. SP26-CON-00318 is archived; its 2 credentials stop working at every gate now; its 1 application and 3 documents move to the kept record." Where access differed, the next step opens access assignment for the kept record; access is never added together. *(source: contracts/satellite/accreditation.yaml#resolveIdentityConflict)*
- **Dismiss (different people)**: The pair is marked dismissed with the reason and is not raised again by later applications or imports. *(source: contracts/satellite/accreditation.yaml#resolveIdentityConflict)*

**Data it reads**: `listAccreditationIdentityConflicts` (onLoad, Possible duplicates)

**Where the user goes next**

- → `BO-625` Accreditation Holder Directory: *Back to Accreditation Holder Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The duplicate identity conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the duplicate identity conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No duplicate identity conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the duplicate identity conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The conflict is already merged or rejected; 422 survivingHolderId missing for merged, or not one of the conflict's holders |

#### Edge cases to draw

- **Already resolved by someone else**: 409 shown as "Resolved by Ahmed Al Mansoori at 10:14 - merged", the pair moves to Resolved. *(source: contracts/satellite/accreditation.yaml#resolveIdentityConflict)*
- **Identical passport or Emirates ID**: Should not reach this queue; an identical number is blocked at submission. If one appears, it is shown at the top as "Same identity number" with High confidence. *(source: DI-692 / DI-659)*

#### Consistency with other screens

- Match `ACC-007`: The reviewer's red banner for a pending duplicate links here.
- Match `BO-623`: The Duplicate candidates tile counts this queue's pending rows.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
conflicts:
- records: Mohammed Al Mansouri / Mohamed Almansoori
  matchedOn:
  - Name and date of birth
  - Mobile
  confidence: High 0.94
  differentAccess: true
  detected: 10 Oct 2026
- records: Priya Nair / Priya N.
  matchedOn:
  - Email
  confidence: Medium 0.71
  differentAccess: false
  detected: 11 Oct 2026
```

#### Permissions

- `listAccreditationIdentityConflicts` → `ACCREDITATION_MANAGE` (configure) · staff
- `resolveIdentityConflict` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*
- Duplicate-profile detection and merge (common because of name transliteration variants) merging two profiles with their combined transaction history; account activate/deactivate. *(agreed · MoM 7 Aug 2026, 19. Maintenance Tools · DI-176)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-631` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-631`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 12: Works in Duplicate & Identity Conflict Detection → Prevent duplicate holder records and potential identity conflicts.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-631?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Resolve identity conflict.
- [ ] Every transition is wired: `BO-625`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-632` Organization & Affiliation Management

**Link holders to their employer, contractor, media organization, government authority or sponsor.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/organization-affiliation-management-bo-632` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Organisations and their people: the employer, contractor, media outlet, authority, sponsor or production company each holder belongs to, with its contact, contract and validity, and all its holders in one list. Organisation relationships later drive approval routing and access. The one thing to get right: the organisation is a record in its own right (the partner account of the 7 September meeting), not a text field on each person.

**Known correction pending (do not draw the wrong version)**

- **No organisation record exists in any contract** Why: organisationId points at nothing that can be listed, created or edited; organisation name, type, contacts, contract, validity, status and partner-account users have no home. *(source: screens/P08-venue-back-office.yaml#BO-632 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder / DI-655; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A holder has one organisationId** Why: The pack requires association with one or more organisations. *(source: screens/P08-venue-back-office.yaml#BO-632; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Button "Save accreditation holder"** Why: Generated label; the screen saves organisations and affiliations. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which contract owns organisations and partner accounts, accreditation or the CRM's company accounts?** → Drawn default accepted: Draw the organisation editor with fields greyed per VO-R13 and the holder affiliation live. *(decided by Chinmay, 2026-10-02; DEC-462 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Organisation details**: Name (English and Arabic), type (closed set: Internal staff, Contractor, Vendor, Media organisation, Government authority, Sponsor, Partner, Production company), registration or trade licence number, primary contact, sponsor contact, contract reference, valid from and to, status (Active, Suspended, Expired). *(source: screens/P08-venue-back-office.yaml#BO-632)*
- **Holder affiliation**: On a holder, organisation (search-select) and role in it (job title); "Add another organisation" for people affiliated with more than one. *(source: screens/P08-venue-back-office.yaml#BO-632 / contracts/satellite/accreditation.yaml#updateAccreditationHolder)*
- **Partner account users**: Main account and sub-account users who may submit for the organisation's members, with their email; a sub-account sees only what it submitted. *(source: DI-655 / DI-660)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save accreditation holder (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Organisations list**: Columns Organisation, Type, Holders (active of total), Pending applications, Contract valid to (amber inside 30 days), Status. *(source: screens/P08-venue-back-office.yaml#BO-632)*
- **Organisation detail**: Details, its holders with status and credentials, its applications by status (approved, rejected, needs resubmission), and its partner-account users. *(source: screens/P08-venue-back-office.yaml#BO-632 / DI-660)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Change a holder's organisation**: Writes the holder (full record, per VO-R04); if a printed badge shows the organisation, the confirm offers a replacement badge. *(source: contracts/satellite/accreditation.yaml#updateAccreditationHolder / contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate)*
- **Suspend organisation**: Drawn greyed until supported; would name the holders affected. *(source: DI-653 / screens/P08-venue-back-office.yaml#BO-033)*

**Where the user goes next**

- → `BO-625` Accreditation Holder Directory: *Back to Accreditation Holder Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The organization affiliation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the organization affiliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No organization affiliation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the organization affiliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Organisation contract expires before its holders' accreditations**: Amber flag on the organisation and on each holder's readiness. *(source: screens/P08-venue-back-office.yaml#BO-632)*

#### Consistency with other screens

- Match `ACC-004`: A coordinator's view of "applications by my organisation" mirrors the organisation detail's application list.
- Match `BO-617`: The organisation picker there is this list.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
organisations:
- name: Falcon Stage Rigging LLC
  type: Contractor
  licence: CN-2245817
  contact: Maria Santos
  holders: 212 of 230
  pending: 9
  contractTo: 31 Dec 2026
  status: Active
- name: Gulf Lens Media
  type: Media organisation
  holders: 88 of 90
  pending: 4
  contractTo: '-'
  status: Active
- name: Abu Dhabi Civil Defence
  type: Government authority
  holders: 14 of 14
  pending: 1
  status: Active
```

#### Permissions

- `updateAccreditationHolder` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A main account holder (company/agent) sees the status of every application under their organisation (approved, rejected, requires resubmission), whether the credential is collected physically or sent as a soft copy by email. *(client request · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-660)*
- The venue creates a partner/company account (main or sub-accounts) whose users log in and submit accreditation for their members; entry can be done by the end user or by the admin team on their behalf. *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-655)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-632` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-632`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 14: Works in Organization & Affiliation Management → Link holders to their employer, contractor, media organization, government authority or sponsor.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-632?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save accreditation holder, Cancel.
- [ ] Every transition is wired: `BO-625`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-633` Profile Completeness & Compliance Monitor

**Show whether a holder profile is ready to proceed to accreditation approval.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/profile-completeness-compliance-monitor-bo-633` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Readiness tab of the holder record, and a readiness column in the directory: whether this person is ready to go to approval, and if not, exactly what is missing or failed. The one thing to get right: one overall state (Ready, Incomplete, Attention required, Blocked) derived by fixed rules from a nine-item checklist, each item linking to the tab that fixes it.

**Known correction pending (do not draw the wrong version)**

- **Only completenessPercent exists** Why: The four-state readiness and the nine checklist items are not returned by any read; computing them needs documents, conflicts and verification data not bound here. *(source: screens/P08-venue-back-office.yaml#BO-633 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **getAccreditationHolder triggered onAction and an empty detailPanel** Why: It is a read on load, and the pack gives the checklist and states. *(source: screens/P08-venue-back-office.yaml#BO-633; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should readiness be stored on the holder (filterable in the directory) or computed on display?** → Drawn default accepted: Stored, so the directory can filter by it. *(decided by Chinmay, 2026-10-02; DEC-463 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Overall state**: Blocked (red) when a duplicate alert is unresolved, a mandatory document has expired or identity verification failed; Attention required (amber) when items are supplied but unverified or rejected; Incomplete (grey) when items are missing; Ready (green) when all pass. Beside it the completeness percentage. *(source: screens/P08-venue-back-office.yaml#BO-633 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder)*
- **Checklist**: Personal information complete, Valid photograph, Mandatory documents uploaded, Mandatory documents verified, Identity verification completed, Organisation confirmed, Consent and declarations accepted, No unresolved duplicate alert, No expired mandatory document. Each row: state icon, one-line detail ("2 of 3 verified"), Fix link to Identity, Photo, Documents, Organisation or BO-631. *(source: screens/P08-venue-back-office.yaml#BO-633)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Fix**: Opens the tab or queue that resolves the item; returning refreshes the state. *(source: screens/P08-venue-back-office.yaml#BO-633)*
- **Send to approval**: Shown only when Ready and an application is waiting; opens the application in the review workspace. *(source: screens/P08-venue-back-office.yaml#BO-633)*

**Where the user goes next**

- → `BO-625` Accreditation Holder Directory: *Back to Accreditation Holder Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The profile completeness compliance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the profile completeness compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No profile completeness compliance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the profile completeness compliance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Requirements change after the holder was Ready**: The state recalculates and the checklist names the new item. *(source: contracts/satellite/accreditation.yaml#setAccreditationRequirements)*

#### Consistency with other screens

- Match `BO-625`: The directory's readiness ring uses these four colours and words.
- Match `ACC-006`: The queue's Approve availability follows the same rules.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
state: Attention required
completeness: 78
items:
- item: Mandatory documents verified
  detail: 2 of 3 verified - Contractor authorisation waiting
  fix: Documents
- item: No unresolved duplicate alert
  detail: Clear
  fix: '-'
```

#### Permissions

- `getAccreditationHolder` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-633` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-633`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 16: Works in Profile Completeness & Compliance Monitor → Show whether a holder profile is ready to proceed to accreditation approval.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-633?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-625`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-634` Profile History & Audit Timeline

**Provide a complete historical record of holder profile changes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each audit event shall capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/profile-history-audit-timeline-bo-634` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The History tab of the holder record: an immutable, chronological timeline of everything that happened to this person's profile and accreditation, with who did it, before and after values, and the reason. Read-only for everyone; exportable for compliance staff. The one thing to get right: it is a timeline with filters, not a form, and a record whose integrity check fails is shown as such, loudly.

**Known correction pending (do not draw the wrong version)**

- **Pattern configEditor with selectFields User, Date/time, Action, Previous value, New value, Source/channel and a textField Related accreditation or event** Why: These are the pack's audit event attributes drawn as inputs; the screen is a read-only timeline with filters. *(source: screens/P08-venue-back-office.yaml#BO-633 / contracts/satellite/accreditation.yaml#listAccreditationAudit; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Source/channel and related accreditation or event have no field** Why: AccreditationAuditRecord has actor, action, values, reason and approvalRequestId only. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationAuditRecord; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **States speak of "configuration as saved" and "create action"** Why: Generated for an editor; there is nothing to configure or create. *(source: screens/P08-venue-back-office.yaml#BO-634; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listAccreditationAudit has no paging and no action filter** Why: Holder and from-date only, unpaged. *(source: contracts/satellite/accreditation.yaml#listAccreditationAudit; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who counts as "authorised compliance personnel" for export?** → Drawn default accepted: A dedicated export permission, named on the disabled button. *(decided by Chinmay, 2026-10-02; DEC-464 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| User | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |
| Action | select field | — | — | — | — | — | — |
| Previous value | select field | — | — | — | — | — | — |
| New value | select field | — | — | — | — | — | — |
| Source/channel | select field | — | — | — | — | — | — |
| Related accreditation or event | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationAudit` ?holderId |
| From | date and time picker | — | — | `listAccreditationAudit` ?from |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Action type (Profile, Photo, Documents, Identity, Organisation, Merge, Accreditation, Status), User, From date. These are filters, not fields of a record. *(source: screens/P08-venue-back-office.yaml#BO-633 / contracts/satellite/accreditation.yaml#listAccreditationAudit)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Timeline**: Newest first; each entry: time (venue time), user, action in words ("Changed organisation"), previous to new value as a compact diff, reason, and a link to the approval where one exists. Sensitive values (identity numbers) appear masked in the diff. *(source: screens/P08-venue-back-office.yaml#BO-633 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationAuditRecord / ADR-0063)*
- **Integrity**: Each entry carries a small shield (Intact). Broken shows a red banner "This history does not verify from 03 Oct 2026; report to compliance"; Unverifiable shows grey. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationAuditRecord / MATRIX 12.1.58)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Export**: For compliance users only (others see it disabled with the permission named); exports the filtered timeline. *(source: screens/P08-venue-back-office.yaml#BO-633)*

**Data it reads**: `listAccreditationAudit` (onLoad, Profile history)

**Where the user goes next**

- → `BO-625` Accreditation Holder Directory: *Back to Accreditation Holder Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The profile history audit configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the profile history audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No profile history audit configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Long history (a holder accredited for five seasons)**: Load more by date; the list never pages by number. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039)*

#### Consistency with other screens

- Match `BO-643`: Approval decisions appear here and in the approval decision history with the same wording.
- Match `BO-626`: The profile's audit summary card shows the last five entries of this timeline.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entries:
- at: 11 Oct 2026 09:41
  user: Ahmed Al Mansoori
  action: Identity verified
  change: Pending > Verified
  reason: Manual check against original
  integrity: Intact
- at: 10 Oct 2026 16:05
  user: Fatima Al Hashimi
  action: Changed organisation
  change: Desert Events LLC > Falcon Stage Rigging LLC
  reason: Employer change confirmed by letter
  integrity: Intact
- at: 07 Oct 2026 21:16
  user: Applicant (portal)
  action: Document uploaded
  change: Emirates ID
  integrity: Intact
```

#### Permissions

- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-634` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-634`
- Workshop pack: ACCREDITATION.pdf board 2
- Flow F218 *ACCREDITATION board 2: Accreditation Holder Directory*, step 18: Works in Profile History & Audit Timeline → Provide a complete historical record of holder profile changes.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-634?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-625`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getAccreditationHolder": {"method":"GET","path":"/accreditation-holders/{holderId}","contract":"accreditation","summary":"One holder — identity, documents, access and history","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccreditationHolder"},
"listAccreditationAudit": {"method":"GET","path":"/accreditation-audit","contract":"accreditation","summary":"The immutable record of who granted what to whom","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"holderId","in":"query","required":null},{"name":"from","in":"query","required":null}],"requestBody":null,"responds":"AccreditationAuditRecord"},
"listAccreditationDocuments": {"method":"GET","path":"/accreditation-documents","contract":"accreditation","summary":"Documents supplied, by holder, application, requirement or state","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"applicationId","in":"query","required":null},{"name":"holderId","in":"query","required":null},{"name":"requirementCode","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccreditationHolders": {"method":"GET","path":"/accreditation-holders","contract":"accreditation","summary":"Everybody accredited, and what state they are in","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"organisationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"listAccreditationIdentityConflicts": {"method":"GET","path":"/accreditation-identity-conflicts","contract":"accreditation","summary":"People who may already be accredited under another record","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccreditationIdentityConflict"},
"resolveIdentityConflict": {"method":"POST","path":"/accreditation-identity-conflicts/{conflictId}/resolve","contract":"accreditation","summary":"Decide whether two accreditation records are the same person","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationIdentityConflict"},
"submitAccreditationDocument": {"method":"POST","path":"/accreditation-documents","contract":"accreditation","summary":"Supply a document against a requirement","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationDocument","responds":"AccreditationDocument"},
"updateAccreditationHolder": {"method":"PUT","path":"/accreditation-holders/{holderId}","contract":"accreditation","summary":"Amend identity, affiliation or contact details","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationHolder","responds":"AccreditationHolder"},
"verifyAccreditationDocument": {"method":"POST","path":"/accreditation-documents/{documentId}/verify","contract":"accreditation","summary":"Accept or refuse a submitted document","permission":"ACCREDITATION_APPROVE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationDocument"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationAuditRecord": {"type":"object","x-ticvai-persistence":"accreditation.audit","description":"Board 8.7. **Who gave this person access to that place, when, and on whose authority.**\n","properties":{"id":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"holderId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"previousRecordHash":{"type":"string","nullable":true},"recordHash":{"type":"string"},"integrity":{"type":"string","readOnly":true,"enum":["intact","broken","unverifiable"]},"scopePath":{"type":"string"}}},
"AccreditationDocument": {"type":"object","x-ticvai-persistence":"accreditation.document","description":"Board 2.5. **Submitted against a named requirement, not into a folder.**","required":["requirementCode","assetId"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid","nullable":true},"applicationId":{"type":"string","format":"uuid","nullable":true},"requirementCode":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"submittedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["submitted","verified","rejected","expired"]},"verifiedBy":{"type":"string","format":"uuid","nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**An insurance certificate valid until March accredits somebody until March**, whatever the programme says.\n"},"scopePath":{"type":"string"}}},
"AccreditationHolder": {"type":"object","x-ticvai-persistence":"accreditation.holder","description":"**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n","required":["id","fullName"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true},"nationality":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true,"description":"12.1.16. The holder's own address — where a mobile credential and renewal notices go"},"phone":{"type":"string","nullable":true,"description":"12.1.16. E.164"},"identityDocumentVerified":{"type":"boolean","default":false},"organisationId":{"type":"string","format":"uuid","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","suspended","revoked","expired","archived"]},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"completenessPercent":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationIdentityConflict": {"type":"object","x-ticvai-persistence":"accreditation.identity_conflict","description":"Board 2.7. **One badge revoked and the other still opening doors.**\n\n**`matchedOn` names `face` only where the programme's `faceMatching` is enabled** and both applicants consented (workbook Q461; CHG-CSA-031).\n\n**Stored, not recomputed on each read** (data model for the agreed operations, 29 September): a suspected pair is raised by `createAccreditationApplication` and `importAccreditationHolders` using `marketing-crm`'s identity resolution, and keeps its id and status while somebody decides it, so a pair rejected as two different people is not raised again on the next import. Resolved by `resolveIdentityConflict` (`pending` to `merged` or `rejected`, decided 29 September, writers pass); lifecycle in `states/accreditation-identity-conflict.yaml`.","required":["id","holderIds","status"],"properties":{"id":{"type":"string","format":"uuid"},"holderIds":{"type":"array","items":{"type":"string","format":"uuid"}},"score":{"type":"number"},"matchedOn":{"type":"array","items":{"type":"string"}},"differingAccess":{"type":"boolean"},"status":{"type":"string","enum":["pending","merged","rejected"]},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"survivingHolderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The holder kept when the conflict was merged"},"resolutionReason":{"type":"string","maxLength":500,"nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
