# WS155 — Resource Management Configuration board 1

**10 screens · 28 operations · 21 schemas · 4 permissions**

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
  `APPROVAL_CONFIGURE, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW`. A control nobody can use must say so,
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
| `BO-854` | Resource Management Command Center | B–D | 30 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-855` | Resource Type Configuration | B–D | 13 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-856` | Resource Category Management | B–D | 15 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-857` | Resource Creation & Profile | B–D | 14 | 22 | 6 | 46 | 1 | 0 | — | notStarted (—) |
| `BO-858` | Configurable Attribute Builder | B–D | 15 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-859` | Resource Hierarchy & Parent–Child Relationships | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-860` | Resource Dependency Rules | B–D | 0 | 8 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-861` | Resource Package & Bundle Configuration | A | 59 | 25 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-862` | Multi-Venue Resource Assignment | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-863` | Resource Lifecycle, Governance & Audit | A | 9 | 0 | 6 | 49 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-859, BO-860, BO-862 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-854` Resource Management Command Center

**Provide administrators and operational managers with the main entry point for Resource Management and an instant overview of the organization's complete resource inventory.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-management-command-center-bo-854` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The landing page of resource master data for administrators and operations managers: how big the permitted resource estate is, what state it is in, where configuration is incomplete, and one-click entry to every board 1 screen. It is a dashboard (KPI tiles, resources by type, availability status, smart alerts, recent activity, quick actions), not a form. The one thing to get right: everything is scoped to what the signed-in person may manage, and configuration problems are actionable links, not just counts.

**Known correction pending (do not draw the wrong version)**

- **The 13 KPI widgets, 12 filters and 5 quick actions are all drawn as selectFields or textFields** Why: KPIs are metric tiles (VO-R02), filters are chips, quick actions are buttons; the pack's lists became form fields. *(source: screens/P08-venue-back-office.yaml#BO-854; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Pattern configEditor with template form** Why: The pack and the client visual draw a command centre dashboard (ADR-0041), not a configuration form. *(source: screens/P08-venue-back-office.yaml#BO-854 / ADR-0041; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Reserved vs Assigned, Suspended, and Configuration issues cannot be counted from the reads bound** Why: Resource.status has available, booked, checkedOut, maintenance and retired only, while lifecycle states (suspended, pending approval) live in another machine; no read reports configuration issues or expiring certifications in aggregate. *(source: contracts/satellite/resources.yaml#/components/schemas/Resource / contracts/satellite/resources.yaml#setResourceLifecycleState; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Import resources and Assign resource to venue, Create package, Review configuration warnings have no screen edge or operation** Why: The pack lists eight quick actions; navigation carries only five board screens and no import operation exists. *(source: screens/P08-venue-back-office.yaml#BO-854; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **DI-475 asks for a "switchable revenue view" on the overview; does it belong on this board or on the calendar command centre?** → Drawn default accepted: Put the revenue switch on BO-864 (bookings x revenue per resource) and show only a link here. *(decided by Chinmay, 2026-10-02; DEC-489 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Total active resources | select field | — | — | — | — | — | — |
| Resources by type | select field | — | — | — | — | — | — |
| Resources by venue | select field | — | — | — | — | — | — |
| Available resources | select field | — | — | — | — | — | — |
| Assigned resources | select field | — | — | — | — | — | — |
| Reserved resources | select field | — | — | — | — | — | — |
| Resources under maintenance | select field | — | — | — | — | — | — |
| Suspended resources | select field | — | — | — | — | — | — |
| Retired resources | select field | — | — | — | — | — | — |
| Resources with expiring certifications | text field | — | — | — | — | — | — |
| Resources with unresolved configuration issues | text field | — | — | — | — | — | — |
| Recently created resources | select field | — | — | — | — | — | — |
| Recently modified resources | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Business unit | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Resource type | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Tags | select field | — | — | — | — | — | — |
| Availability status | select field | — | — | — | — | — | — |
| Effective date | select field | — | — | — | — | — | — |
| Create resource | select field | — | — | — | — | — | — |
| Create resource type | select field | — | — | — | — | — | — |
| Create category | select field | — | — | — | — | — | — |
| Import resources | select field | — | — | — | — | — | — |
| Duplicate resource | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `listResources` ?kind |
| Available from | date and time picker | — | — | `listResources` ?availableFrom |
| Available to | date and time picker | — | — | `listResources` ?availableTo |
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Venue comes from the top-bar switcher (VO-R09); Tenant, Business unit and Country appear only for a tenant-level administrator. In-page filter chips for Resource type, Category, Status, Owner, Department, Tags, Availability status and Effective date ("as at" date picker, default today). Filters apply to every tile at once and are kept as a saved view. *(source: screens/P08-venue-back-office.yaml#BO-854 / ADR-0041)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Metric tiles with delta vs last month (VO-R02), in this order - Total active resources, Available, Assigned, Reserved, Under maintenance, Suspended, Retired, Expiring certifications (30 days), Configuration issues, Created this month, Modified this month. Each tile opens the filtered resource list. Never drawn as select or text fields. *(source: screens/P08-venue-back-office.yaml#BO-854 / DI-476)*
- **Resources by type and by venue**: A donut by resource type (type colour from BO-855) with counts and percent, and a bar per venue for multi-venue users; availability status as a bar chart (Available, Reserved, Assigned, Booked, Maintenance). *(source: screens/P08-venue-back-office.yaml#BO-854 / contracts/satellite/resources.yaml#listResourceTypes)*
- **AI summary panel**: Findings as suggestions with a link each (per VO-R11) - Unused resources, Possible duplicates, Missing mandatory attributes, Approaching retirement, Without venue assignment, Unresolved dependencies, e.g. "8 resources have no venue assigned - Assign". Hidden findings never shown as zero. *(source: screens/P08-venue-back-office.yaml#BO-855)*
- **Smart alerts and recent activity**: Alerts such as "12 staff certifications expiring in 30 days"; recent activity rows "Projector P-17 edited by Fatima Al Hashimi, 2 h ago" from the audit trail. *(source: screens/P08-venue-back-office.yaml#BO-854 / contracts/satellite/resources.yaml#getResourceAuditTrail)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Quick actions**: Create resource (BO-857), Create resource type (BO-855), Create category (BO-856), Import resources, Duplicate resource (clone on BO-857), Assign resource to venue (BO-862), Create package (BO-861), Review configuration warnings (filtered list). Each button disabled with the missing permission named for users without configure rights (VO-R08). *(source: screens/P08-venue-back-office.yaml#BO-854)*
- **Customise**: Add, remove and reorder tiles; the layout is the saved dashboard of ADR-0041, seeded with the pack's tiles. *(source: screens/P08-venue-back-office.yaml#BO-854 / ADR-0041)*

**Data it reads**: `listResources` (onLoad, Resources at this venue); `listResourceTypes` (onLoad, Resources by type); `getResourceUtilisation` (onLoad, Utilisation across the estate)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-855` Resource Type Configuration: *Resource Type Configuration*; carries `resourceTypeId`
- → `BO-856` Resource Category Management: *Resource Category Management*
- → `BO-857` Resource Creation & Profile: *Resource Creation & Profile*; carries `resourceId`
- → `BO-858` Configurable Attribute Builder: *Configurable Attribute Builder*
- → `BO-859` Resource Hierarchy & Parent–Child Relationships: *Resource Hierarchy & Parent–Child Relationships*; carries `resourceId`
- → `BO-860` Resource Dependency Rules: *Resource Dependency Rules*; carries `resourceId`
- → `BO-861` Resource Package & Bundle Configuration: *Resource Package & Bundle Configuration*
- → `BO-862` Multi-Venue Resource Assignment: *Multi-Venue Resource Assignment*; carries `resourceId`
- → `BO-863` Resource Lifecycle, Governance & Audit: *Resource Lifecycle, Governance & Audit*; carries `resourceId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **User scoped to one department**: Every count reflects only that department's resources and the header says so ("Showing Ski School resources"). *(source: screens/P08-venue-back-office.yaml#BO-855)*
- **Utilisation read fails while the resource list loads**: Counts render; the utilisation tile shows "Could not load" with retry, the rest of the board stays usable. *(source: designer default)*

#### Consistency with other screens

- Match `BO-864`: The calendar-based booking overview with the revenue switch (DI-475) is the resource calendar command centre; this board links to it rather than embedding a second calendar.
- Match `BO-943`: Same tile component and deltas as the resource analytics command centre; Total active resources must agree for the same scope and date.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scope: Yas Leisure Group - Aqua Park
tiles:
  totalActive: 1,248 (+8.3%)
  available: '862'
  assigned: '324'
  reserved: '41'
  underMaintenance: '18'
  suspended: '3'
  retired: '27'
  expiringCerts: '12'
  configIssues: '8'
byType:
  Staff: 42%
  Rooms: 8%
  Equipment: 21%
  Rental items: 19%
  Vehicles: 4%
  Cabanas: 6%
alerts:
- 12 staff certifications expiring in 30 days
- 8 resources have no venue assigned
- 5 resources out of maintenance today
```

#### Permissions

- `listResources` → `RESOURCE_VIEW` (read) · staff
- `listResourceTypes` → `RESOURCE_VIEW` (read) · staff
- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resource types (rooms, staff, equipment, vehicles, etc.) carry capacity control and a reservable flag; the command centre shows total vs. active/assigned resources and current availability. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-476)*
- Resource management command centre: calendar-based overview of all resources' booking status (e.g. an instructor booked for a lesson, date and time), filterable by resource type and venue, with a switchable revenue view; view by day, week, month or custom period (planner style). *(client request · MoM 26 Aug 2026, 4.1 Resource Management Overview · DI-475)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-854` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-854`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 1: Opens Resource Management Command Center → Provide administrators and operational managers with the main entry point for Resource Management and an instant overview of the organization's complete resource inventory.
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F264 branch at step 1 (expected): when Nothing has been set up on Resource Management Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F264 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-854?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-855`, `BO-856`, `BO-857`, `BO-858`, `BO-859`, `BO-860`, `BO-861`, `BO-862`, `BO-863`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-855` Resource Type Configuration

**Allow administrators to define the different classes of resources supported by the organization without requiring software development.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceTypeId` (navigation) |
| Route | `/rentals/resource-type-configuration-bo-855` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where an administrator defines the classes of resource the tenant uses (Staff, Instructor, Security personnel, Venue, Room, Hall, Area, Cabana, Equipment, Asset, Rental item, Vehicle, Locker) and what each class can do: reservable, rentable, capacity- or schedule-controlled, inventory-controlled, needs staff qualification, maintenance-controlled, check-in/out, deposit, customer selectable. The one thing to get right: the flags decide which sections a resource of this type shows everywhere else, so each flag reads as a consequence, not a checkbox.

**Known correction pending (do not draw the wrong version)**

- **The 13 example types (Staff, Instructor, ... Locker) are drawn as 13 selectFields** Why: They are seed rows of the types table, not fields. *(source: screens/P08-venue-back-office.yaml#BO-855; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A Resource has a fixed kind enum and no resourceTypeId** Why: The configurable types this screen creates cannot be attached to a resource, so "configuration, not code" (the contract's own words) is not true end to end. *(source: contracts/satellite/resources.yaml#/components/schemas/Resource / contracts/satellite/resources.yaml#listResourceTypes; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **API visible flag and the per-type applicable configuration sections are missing** Why: The pack lists API visible yes/no and asks administrators to decide which sections apply per type. *(source: screens/P08-venue-back-office.yaml#BO-856 / contracts/satellite/resources.yaml#/components/schemas/ResourceType; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Write bodies carry id and scopePath** Why: Server-owned (VO-R03). *(source: contracts/satellite/resources.yaml#createResourceType; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do resource type changes need approval under tenant policy (pack Governance)?** → Drawn default accepted: Save directly; show a greyed "Requires approval" badge slot in the editor header. *(decided by Chinmay, 2026-10-02; DEC-490 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Staff | select field | — | — | — | — | — | — |
| Instructor | select field | — | — | — | — | — | — |
| Security personnel | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Room | select field | — | — | — | — | — | — |
| Hall | select field | — | — | — | — | — | — |
| Area | select field | — | — | — | — | — | — |
| Cabana | select field | — | — | — | — | — | — |
| Equipment | select field | — | — | — | — | — | — |
| Asset | select field | — | — | — | — | — | — |
| Rental item | select field | — | — | — | — | — | — |
| Vehicle | select field | — | — | — | — | — | — |
| Locker | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Code / name / description**: Code upper-case short key (e.g. INSTR), unique in the tenant, locked once resources use the type; name with Arabic variant (VO-R10). *(source: contracts/satellite/resources.yaml#createResourceType)*
- **Icon and display colour**: Icon picker from the product icon set and a colour from the calendar palette (no free hex); the colour is the one used for this type on every calendar and chart. *(source: screens/P08-venue-back-office.yaml#BO-855 / contracts/satellite/resources.yaml#/components/schemas/ResourceType)*
- **Nature**: Radio Physical / Human / Virtual. Choosing Human shows a note "Resources of this type are people - they link to a staff record and their rota is managed in Workforce". *(source: contracts/satellite/resources.yaml#createResourceType)*
- **Capability flags**: Toggles grouped as Booking (Reservable, Rentable, Customer selectable), Control (Capacity-controlled, Schedule-controlled, Inventory-controlled), Operations (Staff qualification required, Maintenance-controlled, Check-in/check-out, Deposit applicable). Defaults Reservable and Schedule-controlled on, all others off. Under Customer selectable - "Allows a ticket type to offer a choice; the ticket type decides". *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceType / contracts/satellite/resources.yaml#setResourceSelectionPolicy)*
- **Applicable sections**: A preview of which profile sections a resource of this type will show, driven by the flags (Staff - skills, certifications, shifts, breaks, attendance; Cabana - capacity, location, opening hours, price link, availability; Towel - inventory, checkout, deposit, return, condition). *(source: screens/P08-venue-back-office.yaml#BO-856)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resource types table**: Type (icon and name), Code, Nature chip, Reservable, Rentable, Capacity-controlled ticks, resources using it (count), Active; sorted by name. *(source: screens/P08-venue-back-office.yaml#BO-855 / contracts/satellite/resources.yaml#listResourceTypes)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New type / Save type**: Create, or full replace on edit (VO-R04). On a venue, the editor is read-only with "Defined by Yas Leisure Group" because types are tenant configuration. *(source: contracts/satellite/resources.yaml#createResourceType / contracts/satellite/resources.yaml#updateResourceType)*

**Data it reads**: `listResourceTypes` (onLoad, The classes defined so far)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource type configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource type untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource type configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Resources exist that the new definition would invalidate (ResourceInUseProblem) |

#### Edge cases to draw

- **Turning off check-in/out while resources of the type are checked out**: Save refused; the message names the count and the resources ("6 strollers are checked out - return them first"). *(source: contracts/satellite/resources.yaml#updateResourceType / contracts/satellite/resources.yaml#/components/schemas/ResourceInUseProblem)*
- **A flag change invalidates existing resources (e.g. turning on Staff qualification required)**: Confirm lists how many resources become incomplete; they appear under Configuration issues on BO-854. *(source: screens/P08-venue-back-office.yaml#BO-856 / contracts/satellite/resources.yaml#updateResourceType)*

#### Consistency with other screens

- Match `BO-095`: The kinds on the resource register and the types defined here must be one list.
- Match `BO-897`: Customer selectable here is the ceiling; the per-ticket-type selection policy decides.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
types:
- name: Instructor
  code: INSTR
  nature: Human
  reservable: true
  qualificationRequired: true
  customerSelectable: true
  resources: 64
- name: Cabana
  code: CABANA
  nature: Physical
  reservable: true
  capacityControlled: true
  resources: 34
- name: Stroller
  code: STROLLER
  nature: Physical
  rentable: true
  checkInOut: true
  deposit: true
  resources: 40
- name: Online class room
  code: VROOM
  nature: Virtual
  reservable: true
  resources: 2
```

#### Permissions

- `listResourceTypes` → `RESOURCE_VIEW` (read) · staff
- `createResourceType` → `RESOURCE_CONFIGURE` (configure) · staff
- `updateResourceType` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resources are one-to-one (dedicated to a booking) or shared (e.g. a meeting room with bookable pods, a vehicle across sequential slots); further sales are blocked once a shared resource's capacity/slot is full and reopened if a booking is cancelled. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-496)*
- Resource types (rooms, staff, equipment, vehicles, etc.) carry capacity control and a reservable flag; the command centre shows total vs. active/assigned resources and current availability. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-476)*
- Optional resource module: a template defines the resource types a product needs (e.g. a vehicle and a driver); named resources have an availability calendar/roster; at sale (POS or online) both resource availability and capacity are checked before booking. *(agreed · MoM 7 Aug 2026, 18. Resource Management · DI-175)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-855` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-855`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 2: Works in Resource Type Configuration → Allow administrators to define the different classes of resources supported by the organization without requiring software development.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-855?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-856` Resource Category Management

**Provide a flexible classification structure beneath resource types so resources can be organized, searched, reported, and governed consistently.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `categoryId` (navigation) |
| Route | `/rentals/resource-category-management-bo-856` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The category tree beneath resource types (Staff > Instructor, Operations, Security, Technical crew; Equipment > AV, Lighting, Sound, Furniture; Rental > Towels, Strollers, Lockers, Cabanas) used for search, scheduling filters, reporting and defaults. The one thing to get right: it is a tree with inheritance - a subcategory shows which defaults it takes from its parent and which it overrides.

**Known correction pending (do not draw the wrong version)**

- **The 15 example categories are drawn as selectFields** Why: They are tree nodes (seed data), not fields. *(source: screens/P08-venue-back-office.yaml#BO-856; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Default availability policies has no field** Why: The pack lists it and the contract says availability policies cascade, but ResourceCategory has no availability field. *(source: screens/P08-venue-back-office.yaml#BO-857 / contracts/satellite/resources.yaml#/components/schemas/ResourceCategory; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A Resource has no categoryId** Why: Resources cannot be placed in a category, so search, reporting and the calendar's category filter have nothing to filter on. *(source: contracts/satellite/resources.yaml#/components/schemas/Resource / contracts/satellite/resources.yaml#getResourceCalendar; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Equipment | select field | — | — | — | — | — | — |
| AV | select field | — | — | — | — | — | — |
| Lighting | select field | — | — | — | — | — | — |
| Sound | select field | — | — | — | — | — | — |
| Furniture | select field | — | — | — | — | — | — |
| Staff | select field | — | — | — | — | — | — |
| Instructor | select field | — | — | — | — | — | — |
| Operations | select field | — | — | — | — | — | — |
| Security | select field | — | — | — | — | — | — |
| Technical Crew | select field | — | — | — | — | — | — |
| Rental | select field | — | — | — | — | — | — |
| Towels | select field | — | — | — | — | — | — |
| Strollers | select field | — | — | — | — | — | — |
| Lockers | select field | — | — | — | — | — | — |
| Cabanas | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Parent category**: Picker over the tree; a category cannot be its own ancestor (the picker hides itself and its descendants); empty = top level. *(source: screens/P08-venue-back-office.yaml#BO-857 / contracts/satellite/resources.yaml#createResourceCategory)*
- **Code, name, description, display order**: Code unique per tenant; name with Arabic variant; display order set by dragging in the tree, not typed. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceCategory)*
- **Applicable resource types**: Multi-select chips from BO-855; a child may only narrow its parent's types. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceCategory)*
- **Tags, reporting group, cost centre**: Tags as chips; reporting group from a list (Human Resources, Operations, Rentals...); cost centre code as text with the finance format. *(source: screens/P08-venue-back-office.yaml#BO-857)*
- **Default attributes, default availability policy, default approval workflow**: Default attributes pick attribute definitions (BO-858) with default values; approval workflow from the tenant's workflows; each shows "From parent - Equipment" when inherited, with Override. *(source: screens/P08-venue-back-office.yaml#BO-857 / contracts/satellite/resources.yaml#/components/schemas/ResourceCategory)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Category tree**: Expand/collapse tree with resource count per node and an inactive style for inactive categories; search above it. *(source: screens/P08-venue-back-office.yaml#BO-856 / contracts/satellite/resources.yaml#listResourceCategories)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New category / Save category**: Create, or full replace (VO-R04); category configuration is tenant scope, read-only for venue users. *(source: contracts/satellite/resources.yaml#updateResourceCategory)*
- **Deactivate**: Sets inactive; there is no delete. A category in use asks for confirmation naming the count. *(source: contracts/satellite/resources.yaml#updateResourceCategory)*

**Data it reads**: `listResourceCategories` (onLoad, The classification tree)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource category configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource category untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource category configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The category is in use, and the refusal carries how many resources sit beneath it so the warning can say so. (ResourceInUseProblem) |

#### Edge cases to draw

- **Editing a category used by active resources**: The save comes back refused with the count; the confirm says "Used by 42 active resources - their defaults will change" and resends on confirm. *(source: contracts/satellite/resources.yaml#updateResourceCategory / contracts/satellite/resources.yaml#/components/schemas/ResourceInUseProblem)*
- **Moving a subtree under a new parent**: Preview which inherited defaults change for the moved branch before saving. *(source: contracts/satellite/resources.yaml#listResourceCategories)*

#### Consistency with other screens

- Match `BO-865`: The calendar's category filter uses this tree.
- Match `BO-944`: Utilisation grouped by category uses these categories and reporting groups.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tree:
- Staff > Instructor (64), Operations (210), Security (48), Technical crew (22)
- Equipment > AV (36), Lighting (18), Sound (12), Furniture (140)
- Rental > Towels (pooled), Strollers (40), Lockers (300), Cabanas (34)
category:
  name: Instructor
  code: INSTR
  parent: Staff
  types: Staff, Instructor
  reportingGroup: Human Resources
  costCentre: CC-2041
  defaultAttributes: Skill level, Languages, Certifications
```

#### Permissions

- `listResourceCategories` → `RESOURCE_VIEW` (read) · staff
- `createResourceCategory` → `RESOURCE_CONFIGURE` (configure) · staff
- `updateResourceCategory` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Categories/subcategories are configurable hierarchies (e.g. staff → employee/operations/instructor; equipment → lighting/sound; vehicles → SUV). Resource profile: name, category, capacity, active/inactive, images, category-specific details and custom attributes (e.g. a vehicle's plate number). *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-477)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-856` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-856`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 4: Works in Resource Category Management → Provide a flexible classification structure beneath resource types so resources can be organized, searched, reported, and governed consistently.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-856?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-857` Resource Creation & Profile

**Provide the principal workspace for creating and maintaining an individual resource.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration; Operational Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-creation-profile-bo-857` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The workspace for one resource: identity, organisation, operational settings, location, commercial and integration sections as tabs, plus setup, teardown and the cleaning policy with a day preview, and the lifecycle actions (save draft, submit, activate, suspend, clone, archive, retire). The one thing to get right: a resource cannot become active until its mandatory configuration is complete, and the screen shows what is missing instead of failing on Activate.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Most of the pack's profile (short name, image, barcode/QR, external reference, business unit, department, owner, responsible manager, cost centre, building, floor, zone, GPS, hourly and daily cost, replacement value … (CHG-SBO-005)
- createResource marks id as a required input (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The gap note says the screen declares no write (CHG-SBO-009); Cleaning window from/to are textFields; operational settings are selectFields (CHG-SBO-009); Resource.status (available, booked, checkedOut, maintenance, retired) and the lifecycle state are two different machines with overlapping … (CHG-SBO-009).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Capacity | number field | — | — | — | — | A number with its unit (people or units); the pack drew a drop-down. | — |
| Unit of measure | select field | — | — | — | — | — | — |
| Customer selectable | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Availability mode | select field | — | — | — | — | — | — |
| Scheduling mode | select field | — | — | — | — | — | — |
| Default duration | number field | — | — | — | — | A number with its unit (minutes); the pack drew a drop-down. | — |
| Minimum booking duration | number field | — | — | — | — | A number with its unit (minutes); the pack drew a drop-down. | — |
| Maximum booking duration | number field | — | — | — | — | A number with its unit (minutes); the pack drew a drop-down. | — |
| Cleaning | segmented control | optional | — | After every booking · Times per day | — | **How the room is cleaned between uses** (decided 29 September, W10). *After every booking* blocks a fixed buffer after each booking (e.g. 15 minutes); *N times a day* lets the system place N … | `Resource.cleaningPolicy.mode` |
| Minutes per cleaning | number field (minutes) | optional | — | min 5; max 240 | — | Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct). | `Resource.cleaningPolicy.bufferMinutes` |
| Cleanings per day | stepper or slider | optional | — | min 1; max 24 | — | Shown for *N times a day* only. | `Resource.cleaningPolicy.cleaningsPerDay` |
| Cleaning window from | time picker | optional | — | — | HH:mm, 24-hour | A time of day, HH:MM in venue time (the time-picker mode). | `Resource.cleaningPolicy.windowStart` |
| Cleaning window to | time picker | optional | — | — | HH:mm, 24-hour | A time of day, HH:MM in venue time (the time-picker mode). | `Resource.cleaningPolicy.windowEnd` |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Identity**: Resource type first (it decides which attribute fields and sections appear), then code, name, short name, category, description, image, barcode/QR (generated or scanned), external reference. No id or scopePath fields (VO-R03). For a Human type, pick the staff member (principal); name comes from the staff record. *(source: screens/P08-venue-back-office.yaml#BO-857 / contracts/satellite/resources.yaml#createResource)*
- **Attributes**: The attribute definitions applicable to the type and category (BO-858), with their own controls, mandatory markers and conditional visibility (vehicle shows registration and passenger capacity). *(source: screens/P08-venue-back-office.yaml#BO-859 / contracts/satellite/resources.yaml#listResourceAttributes)*
- **Setup and teardown**: Minutes before and after a booking (0 default), with the one-line preview "Booked 14:00-16:00 means unavailable 13:30-16:30". *(source: contracts/satellite/resources.yaml#/components/schemas/Resource)*
- **Cleaning**: None / After every booking / N times a day. After every booking - minutes per cleaning (5-240, default 15), added after teardown. N times a day - minutes per cleaning, cleanings per day (1-24) and an optional window from-to as time pickers (empty = the resource's opening and closing). Fields appear only for the chosen mode. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceCleaningPolicy / DI-1012)*
- **Deposit and qualifications**: Deposit in AED only for types with deposit applicable; required qualification codes only for types needing staff qualification. *(source: contracts/satellite/resources.yaml#/components/schemas/Resource)*

#### Outputs: what the screen shows and produces

**Shown**

**Lifecycle and status** (detail panel, from `getResource`): The lifecycle state is shown in the header (changed only with `setResourceLifecycleState`); the operational status (available, booked, checked out, maintenance, retired) is read-only, never an input.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Kind | chip: Cabana, Lounger, Locker, Wheelchair, Stroller, Equipment… | BL-135. `locker` was an entitlement kind in `orders` and nothing issued, assigned or released one. |
| Venue | the name it points at, never the id | — |
| Parent resource | the name it points at, never the id | A pool cabana belongs to the pool area; a seat belongs to an auditorium. Booking a parent takes its children with it, which is the … |
| Principal | the name it points at, never the id | For a resource of kind `instructor` or `staff`. `workforce` still owns their rota — this says whether they are qualified and whether they … |
| Attributes | grouped details | Configurable per kind — capacity, size, shade, power, poolside. |
| Setup minutes | 1,234 | Before the booking, not inside it. An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that … |
| Teardown minutes | 1,234 | After the booking. Kept as it is (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added … |
| Cleaning policy | grouped details | How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`. |
| Mode | chip: After every booking, Times per day | — |
| Buffer minutes | 1,234 | Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct). |
| Cleanings per day | 1,234 | Required for `timesPerDay`; ignored for `afterEveryBooking`. |
| Window start | text | Venue-local time the cleaning window opens. Null means the resource's opening time. |
| Window end | text | Venue-local time the cleaning window closes. Null means the resource's closing time. |
| Requires qualification | list or chips (count when long) | Qualification codes a person must hold to be assigned to this. |
| Deposit amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Status | chip: Available, Booked, Checked out, Maintenance, Retired | — |
| Is active | yes / no (icon or chip) | — |

**Day preview** (timeline, from `getResourceAvailability`): **A day preview before saving** (W10): bookings, holds and the cleanings the policy places, as `cleaning` blocked windows, so an operator sees what the policy takes out of availability.

| Shows | Format | Notes |
|---|---|---|
| Free windows | list or chips (count when long) | — |
| Blocked windows | list or chips (count when long) | With a reason, because they are not the same. Booked and under repair need different responses from an operator looking for something free … |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Day preview**: A one-day timeline for a chosen date with bookings, holds, setup/teardown and the cleanings the policy places (dotted bands), recalculated as the policy fields change, before saving. *(source: contracts/satellite/resources.yaml#getResourceAvailability / DI-1012)*
- **Readiness checklist**: Right-hand panel "Before this can be activated" listing missing mandatory attributes, no venue assignment, no schedule, no category; each line links to the section or screen. *(source: screens/P08-venue-back-office.yaml#BO-863)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save draft / Submit for approval**: Create (or full replace on edit, VO-R04) then move the lifecycle to draft or pending approval; approvers are notified. *(source: contracts/satellite/resources.yaml#createResource / contracts/satellite/resources.yaml#setResourceLifecycleState)*
- **Activate / Suspend / Archive / Retire**: State change with reason (required for suspend and retire), effective from, replacement resource on retire; a refused transition says whether it is not allowed from this state or needs approval, and lists the allowed states. *(source: contracts/satellite/resources.yaml#setResourceLifecycleState / contracts/satellite/resources.yaml#/components/schemas/ResourceTransitionProblem)*
- **Clone**: Asks how many and the code pattern (e.g. STR-{nn} from STR-013); copies configuration only - code, serial, barcode cleared, no bookings, history or deposits. "40 strollers created". *(source: contracts/satellite/resources.yaml#cloneResource)*

**Data it reads**: `getResourceQualifications` (onLoad, What the resource is certified to do, and until when)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource creation profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource creation profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource creation profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The transition is not allowed from the current state, or an approval the configuration requires has not been given. (ResourceTransitionProblem); 422 A `cleaningPolicy` with `timesPerDay` and no `cleaningsPerDay`, or whose window ends before it starts (W10, 29 September). |

#### Edge cases to draw

- **N times a day without a count, or a window ending before it starts**: Refused against the field ("Enter how many cleanings a day"; "Window must end after it starts"). *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceCleaningPolicy)*
- **Possible duplicate (same name and type at the venue)**: An AI suggestion banner "Looks like Projector P-17 already exists" with Open and Ignore (VO-R11); never blocks save. *(source: screens/P08-venue-back-office.yaml#BO-858)*

#### Consistency with other screens

- Match `BO-095`: The register's New resource opens this screen; same fields, one editor.
- Match `BO-863`: Lifecycle actions here and the state machine there must show the same nine states and words.
- Match `BO-866`: The cleaning policy appears in the availability preview there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
resource:
  type: Room
  code: MR-A
  name: Meeting Room A
  category: Venue > Rooms
  parent: Aqua Park Conference Centre
  capacity: 20
  setup: 15 min
  teardown: 15 min
  cleaning: After every booking, 15 min
preview: Sat 10 Oct 2026 - Setup 08:45-09:00, Booking 09:00-12:00 Yas Corporate, Teardown 12:00-12:15, Cleaning
  12:15-12:30, Free 12:30-20:00
```

#### Permissions

- `getResourceAvailability` → `RESOURCE_VIEW` (read) · staff, guest
- `getResource` → `RESOURCE_VIEW` (read) · staff
- `getResourceQualifications` → `RESOURCE_VIEW` (read) · staff
- `createResource` → `RESOURCE_MANAGE` (configure) · staff
- `updateResource` → `RESOURCE_MANAGE` (configure) · staff
- `setResourceLifecycleState` → `RESOURCE_MANAGE` (configure) · staff
- `cloneResource` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

46 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.6 | The system should provide a calendar view for all the resources (e.g. instructors) and associated time slots (e.g. ski school session by an instructor). The calendar should support application of … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.7 | The system should show the booked capacity of different time-slots to provide their availability. The capacity can be color-coded to indicate if not busy, moderately busy, or crowded within each … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.13 | Using the calendar view, system should provide an drag and drop interface to reassign the resources from one resource to another available resources. System should automatically assign the next … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.18 | Resource Calendar: Centralized calendar view (daily/weekly/monthly). | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.19 | Availability Management: Check conflicts before assigning resources. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.20 | Recurring Reservations: Block resources for repeated sessions/shows. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.21 | Time Slot Management: Allocate setup, event, teardown, and maintenance times. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.22 | Multi-event Handling: Manage shared resources across parallel events. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.27 | System shall provide centralized resource calendars. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.28 | System shall manage resource time slots and availability. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.29 | System shall manage availability and conflict detection. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.30 | System shall support advance resource reservations. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| … 34 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Categories/subcategories are configurable hierarchies (e.g. staff → employee/operations/instructor; equipment → lighting/sound; vehicles → SUV). Resource profile: name, category, capacity, active/inactive, images, category-specific details and custom attributes (e.g. a vehicle's plate number). *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-477)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-857` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-857`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 6: Works in Resource Creation & Profile → Provide the principal workspace for creating and maintaining an individual resource.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-857?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-858` Configurable Attribute Builder

**Allow customers to extend resource records with their own attributes without changing the core application.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/configurable-attribute-builder-bo-858` |

**Known gaps.** **Configurable Attribute Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Lets the tenant extend resource records with its own typed fields (skill level, languages, seating capacity, serial number, warranty expiry, rental condition) without a release: label, data type, where it applies, validation and whether it can be searched. The one thing to get right: Searchable decides whether skill-based matching can use the attribute, so say so next to the toggle.

**Known correction pending (do not draw the wrong version)**

- **The 15 example attributes are drawn as selectFields and the gap note says nothing writes** Why: They are rows of the attribute list; createResourceAttribute is bound, so the note is stale. *(source: screens/P08-venue-back-office.yaml#BO-858 / contracts/satellite/resources.yaml#createResourceAttribute; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No update or retire operation for an attribute definition** Why: A definition can be created but never corrected or withdrawn. *(source: contracts/satellite/resources.yaml#listResourceAttributes; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Reportable, API exposed, Customer visible, Effective date, Display sequence and conditional rules have no field** Why: The pack requires all six; the definition has mandatory, default, allowed values, min/max, validation and searchable only. *(source: screens/P08-venue-back-office.yaml#BO-859 / contracts/satellite/resources.yaml#/components/schemas/ResourceAttributeDefinition; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Skill level | select field | — | — | — | — | — | — |
| Height | select field | — | — | — | — | — | — |
| Weight | select field | — | — | — | — | — | — |
| Seating capacity | select field | — | — | — | — | — | — |
| Equipment model | select field | — | — | — | — | — | — |
| Serial number | select field | — | — | — | — | — | — |
| Size | select field | — | — | — | — | — | — |
| Manufacturer | select field | — | — | — | — | — | — |
| Color | select field | — | — | — | — | — | — |
| Power requirement | select field | — | — | — | — | — | — |
| Warranty expiry | select field | — | — | — | — | — | — |
| Maximum occupancy | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Certification level | select field | — | — | — | — | — | — |
| Rental condition | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Label and code**: Label with Arabic variant; code generated from the label (SKILL_LEVEL), editable until any resource holds a value. *(source: contracts/satellite/resources.yaml#createResourceAttribute)*
- **Data type**: One choice from Text, Number, Decimal, Currency, Date, Date/time, Boolean, Single select, Multi-select, Lookup, Attachment, URL, Measurement, Formula; the rest of the form adapts (allowed values for selects, min/max for numbers, unit for measurement, expression editor for formula, AED for currency). *(source: screens/P08-venue-back-office.yaml#BO-859 / contracts/satellite/resources.yaml#/components/schemas/ResourceAttributeDefinition)*
- **Applies to**: Resource types and categories as chips; empty means every type. A conditional rule "Show when type is Vehicle" is the pack's conditional attribute. *(source: screens/P08-venue-back-office.yaml#BO-859)*
- **Mandatory, default, allowed values, min/max, validation expression**: Default rendered with the type's own control; allowed values as chips (Beginner, Intermediate, Advanced, Expert); validation expression under Advanced. *(source: contracts/satellite/resources.yaml#createResourceAttribute)*
- **Searchable / Reportable / API exposed / Customer visible**: Toggles; under Searchable "Needed for skill matching and calendar filters". Customer visible warns that the value may appear on guest resource cards (BO-897). *(source: screens/P08-venue-back-office.yaml#BO-859 / contracts/satellite/resources.yaml#createResourceAttribute)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Attribute list**: Label, data type icon, applies to, mandatory, searchable; grouped by type; display sequence by drag. *(source: screens/P08-venue-back-office.yaml#BO-858 / contracts/satellite/resources.yaml#listResourceAttributes)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New attribute / Save**: Creates the definition at tenant scope; the resource profile (BO-857) shows it at once for the matching types. *(source: contracts/satellite/resources.yaml#createResourceAttribute)*

**Data it reads**: `listResourceAttributes` (onLoad, Attributes defined so far)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The configurable attribute configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the configurable attribute untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No configurable attribute configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Making an attribute mandatory when existing resources have no value**: Confirm "34 instructors have no Skill level - they will be flagged as incomplete"; they appear on BO-854's configuration issues. *(source: screens/P08-venue-back-office.yaml#BO-863)*
- **Changing the data type after values exist**: Data type locked with "Values exist on 64 resources". *(source: designer default)*

#### Consistency with other screens

- Match `BO-898`: Searchable attributes are the ones offered as matching criteria there.
- Match `BO-877`: Rule attributes (skill level, language) are these definitions.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
attributes:
- label: Skill level
  code: SKILL_LEVEL
  type: Single select
  values: Level 1, Level 2, Level 3, Level 4
  appliesTo: Instructor
  mandatory: true
  searchable: true
- label: Languages
  code: LANGUAGES
  type: Multi-select
  values: Arabic, English, French, Russian
  appliesTo: Instructor, Staff
  searchable: true
- label: Registration plate
  code: REG_PLATE
  type: Text
  appliesTo: Vehicle
  mandatory: true
  validation: Dubai plate format
- label: Seating capacity
  code: SEATS
  type: Number
  min: 1
  max: 2000
  appliesTo: Room, Hall
```

#### Permissions

- `listResourceAttributes` → `RESOURCE_VIEW` (read) · staff
- `createResourceAttribute` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Categories/subcategories are configurable hierarchies (e.g. staff → employee/operations/instructor; equipment → lighting/sound; vehicles → SUV). Resource profile: name, category, capacity, active/inactive, images, category-specific details and custom attributes (e.g. a vehicle's plate number). *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-477)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-858` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-858`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 8: Works in Configurable Attribute Builder → Allow customers to extend resource records with their own attributes without changing the core application.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-858?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-859` Resource Hierarchy & Parent–Child Relationships

**Represent physical and operational relationships between resources.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-hierarchy-parent-child-relationships-bo-859` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The parent-child tree of resources (Venue > Building > Floor > Hall > Room; AV System > Projector, Screen, Speakers, Microphones) with named relationships. It is load-bearing - booking a parent takes its children, and closing a hall makes its dependent children unavailable. The one thing to get right: show the operational consequence of a move before it is saved, and show a refused cycle as the loop it would create.

**Known correction pending (do not draw the wrong version)**

- **The screen has an empty detail panel and a generic "Save resource hierarchy" button, and the gap note says the pack gives nothing drawable** Why: The pack lists a tree view, expand/collapse, drag-and-drop, parent selection, child assignment, relationship type, effective date, priority and dependency indication. *(source: screens/P08-venue-back-office.yaml#BO-859; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The parent is written in two places (Resource.parentResourceId by updateResource and the hierarchy by setResourceHierarchy)** Why: Two writers for one fact will disagree; one must own the parent. *(source: contracts/satellite/resources.yaml#updateResource / contracts/satellite/resources.yaml#setResourceHierarchy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which writer owns a resource's parent - the profile or the hierarchy?** → Drawn default accepted: Draw the profile's Parent as read-only with "Change in hierarchy". *(decided by Chinmay, 2026-10-02; DEC-491 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Tree**: Expand/collapse tree with search; drag a node onto a new parent to re-parent (with confirm), or use Parent and Add child pickers for keyboard users. *(source: screens/P08-venue-back-office.yaml#BO-859)*
- **Relationship details**: For the selected link - relationship type as one choice (Contains, Belongs to, Located in, Operated by, Supported by, Part of, Dedicated to), effective from (date), priority (number). No id fields. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceRelation)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save resource hierarchy (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Hierarchy preview**: A small diagram of the selected node's ancestors and children (as in the client board), with a dependency icon on nodes that have dependency rules (BO-860). *(source: screens/P08-venue-back-office.yaml#BO-859)*
- **Impact note**: Before saving, "Booking Main Hall will also hold its 4 children; closing it makes them unavailable"; and "2 links added, 1 removed". *(source: contracts/satellite/resources.yaml#getResourceHierarchy)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save hierarchy**: Replaces this resource's ancestors and children as sent (VO-R04); refusals shown inline. *(source: contracts/satellite/resources.yaml#setResourceHierarchy)*

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource hierarchy parent–child list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource hierarchy parent–child untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource hierarchy parent–child yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource hierarchy parent–child are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Circular, invalid, or cross-tenant without authorisation (ResourceHierarchyProblem) |

#### Edge cases to draw

- **Circular hierarchy**: Refused with the loop drawn as a path ("Main Building > Level 1 > Ski School Area > Main Building"); the dragged node snaps back. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceHierarchyProblem)*
- **Invalid parent or a parent in another tenant without authorisation**: Refused with the reason in words ("A room cannot contain a building"; "Needs cross-tenant rights"). *(source: contracts/satellite/resources.yaml#setResourceHierarchy)*
- **Re-parenting a resource with future bookings**: Warn with the count of future bookings whose parent changes. *(source: designer default)*

#### Consistency with other screens

- Match `BO-857`: The profile's Parent field and this tree must show the same parent.
- Match `BO-860`: Dependency rules are a different relationship (requires, conflicts); keep the two editors visually distinct.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tree: Summit Peaks > Main Building > Level 1 > Ski School Area > Training Area A; Level 2 > Equipment Storage
link:
  child: Training Area A
  parent: Ski School Area
  relation: Located in
  effectiveFrom: 1 Oct 2026
  priority: 1
```

#### Permissions

- `getResourceHierarchy` → `RESOURCE_VIEW` (read) · staff
- `setResourceHierarchy` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resources link as main/sub-resources (e.g. "vehicle" with individual vehicles beneath). Dependency rules per product (e.g. a private ski lesson needs at least two resources, or at least one vehicle) are enforced when a resource-linked product is configured or sold. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-478)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-859` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-859`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 10: Works in Resource Hierarchy & Parent–Child Relationships → Represent physical and operational relationships between resources.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-859?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save resource hierarchy, Cancel.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-860` Resource Dependency Rules

**Define operational relationships where one resource requires, depends upon, conflicts with, or influences another resource.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The system shall display) and no metric row |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-dependency-rules-bo-860` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Rules saying what a resource requires, requires one of, conflicts with, cannot run alongside, prefers, substitutes for, backs up, or shares capacity with (Stage A requires Sound System A and Lighting Rig A). They are checked before any assignment is confirmed. The one thing to get right: substitute and backup rows are the approved pool the automatic replacement draws from, so they must be visible as such.

**Known correction pending (do not draw the wrong version)**

- **The table and detail columns are the four conflict counters, titled "Every resource dependency rules"** Why: Those are the conflict panel's headings; the table is the rule rows (kind, target, quantity, mandatory, priority, dates, venue), titled "Dependency rules". *(source: screens/P08-venue-back-office.yaml#BO-860; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Time overlap rules, availability dependency and capacity dependency have no field** Why: The pack lists them as rule properties; ResourceDependency has none of them. *(source: screens/P08-venue-back-office.yaml#BO-860 / contracts/satellite/resources.yaml#/components/schemas/ResourceDependency; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read computes missing dependencies, circular warnings or unavailable dependents** Why: The conflict panel the pack requires has no source; only allocateResources reports a missing dependency, and only at allocation time. *(source: contracts/satellite/resources.yaml#getResourceDependencies / contracts/satellite/resources.yaml#allocateResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's examples are product rules (DI-478 "dependency rules per product") but the operation is per resource** Why: Product-level dependencies belong to experience requirements; this screen should say it is resource-to-resource. *(source: DI-478 / contracts/satellite/resources.yaml#setResourceDependencies; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Primary resource**: The resource the rules belong to (from the entry parameter or a picker); the list at left shows resources with rules. *(source: contracts/satellite/resources.yaml#getResourceDependencies)*
- **Dependency rows**: Each row - kind (one of the nine, as a select with plain labels), target as either a specific resource or a resource type (radio), min and max quantity, mandatory/optional, priority, effective from-to, venue limitation. Requires one of / Requires all group several targets in one row. *(source: screens/P08-venue-back-office.yaml#BO-860 / contracts/satellite/resources.yaml#/components/schemas/ResourceDependency)*

#### Outputs: what the screen shows and produces

**Shown**

**Every resource dependency rules** (data table)

| Shows | Format | Notes |
|---|---|---|
| Missing dependencies | text | not in the schema: `Missing dependencies` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Circular dependency warnings | text | not in the schema: `Circular dependency warnings` |
| Unavailable dependent resources | text | not in the schema: `Unavailable dependent resources` |

**The selected resource dependency rules** (detail panel): The pack groups this record's detail under its own headings: “Private Ski Lesson”.

| Shows | Format | Notes |
|---|---|---|
| Missing dependencies | text | not in the schema: `Missing dependencies` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Circular dependency warnings | text | not in the schema: `Circular dependency warnings` |
| Unavailable dependent resources | text | not in the schema: `Unavailable dependent resources` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Impact preview**: "When Stage A is assigned, these are also required - Sound System A (1), Lighting Rig A (1)"; substitutes listed as "Approved substitutes for Instructor Maria Santos - Ahmed Al Mansoori". *(source: screens/P08-venue-back-office.yaml#BO-860 / contracts/satellite/resources.yaml#replaceResourceAllocation)*
- **Conflict detection**: Four counters with lists - Missing dependencies, Resource conflicts, Circular dependency warnings, Unavailable dependent resources; each item links to the resource. *(source: screens/P08-venue-back-office.yaml#BO-860)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rules**: Replaces the resource's whole rule set (VO-R04); allocation then refuses an assignment that misses a mandatory dependency, naming it. *(source: contracts/satellite/resources.yaml#setResourceDependencies / contracts/satellite/resources.yaml#/components/schemas/ResourceAllocationProblem)*

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource dependency rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource dependency rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource dependency rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource dependency rules are still there. The pack's own statuses are Sound System A — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Rule makes a resource depend on itself through others (A requires B, B requires A)**: Warned as circular before save, with the chain. *(source: screens/P08-venue-back-office.yaml#BO-860)*
- **A required resource is under maintenance today**: Listed under Unavailable dependent resources with its return date; the primary's assignments for that window show at risk. *(source: screens/P08-venue-back-office.yaml#BO-860)*

#### Consistency with other screens

- Match `BO-893`: "Private ski lesson needs one instructor and one training zone" is an experience requirement (BO-893), not a resource dependency; keep the pack's example there.
- Match `BO-902`: Substitute for / Backup for rows feed the automatic replacement.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
primary: Stage A (Summit Peaks Amphitheatre)
rules:
- kind: Requires
  target: Sound System A
  qty: 1
  mandatory: true
- kind: Requires
  target: Lighting Rig A
  qty: 1
  mandatory: true
- kind: Cannot operate simultaneously
  target: Stage B
  mandatory: true
- kind: Backup for
  target: Stage B
  priority: 1
```

#### Permissions

- `getResourceDependencies` → `RESOURCE_VIEW` (read) · staff
- `setResourceDependencies` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resources link as main/sub-resources (e.g. "vehicle" with individual vehicles beneath). Dependency rules per product (e.g. a private ski lesson needs at least two resources, or at least one vehicle) are enforced when a resource-linked product is configured or sold. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-478)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-860` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-860`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 12: Works in Resource Dependency Rules → Define operational relationships where one resource requires, depends upon, conflicts with, or influences another resource.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-860?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-861` Resource Package & Bundle Configuration

**Allow commonly used combinations of resources to be predefined and assigned as a single operational package.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block A · ticket #20729 (APP-SETUP-BO-861) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `packageId` (navigation) |
| Route | `/rentals/resource-package-bundle-configuration-bo-861` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Reusable resource packages: a named combination of fixed resources, resource types with quantities, and skill-based placeholders ("1 x Technician with AV Level 2") that is booked as one (VIP Cabana = cabana + towels + locker + attendant). The one thing to get right: components can be a specific resource, a type, or a qualified-person placeholder, each mandatory or optional with substitutes.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write bodies carry id and scopePath (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Every field (package code, name, description, effective dates, internal cost) is a selectField (CHG-SBO-009).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Code | text field | optional | — | — | — | — | `ResourcePackage.code` |
| Name | text field | optional | — | — | — | — | `ResourcePackage.name` |
| Description | text area | optional | — | — | — | — | `ResourcePackage.description` |
| Applicable venues | multi-picker: choose applicable venues | optional | — | — | — | — | `ResourcePackage.applicableVenueIds` |
| Allocation priority | number field | optional | 0 | — | — | — | `ResourcePackage.allocationPriority` |
| Effective from | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `ResourcePackage.effectiveFrom` |
| Minimum minutes | number field (minutes) | optional | — | — | — | — | `ResourcePackage.minimumMinutes` |
| Requires approval | toggle | optional | off | — | — | — | `ResourcePackage.requiresApproval` |
| Internal cost | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `ResourcePackage.internalCost` |
| Effective to | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `ResourcePackage.effectiveTo` |
| Maximum minutes | number field (minutes) | optional | — | — | — | — | `ResourcePackage.maximumMinutes` |

**Form: Create package** (modal, opened by *Create package*; *Create package* calls `createResourcePackage`, *Cancel* sends nothing)

**Collects what `createResourcePackage` sends before it is called.** Required: `code`, `name`. Optional: `description`, `applicableVenueIds`, `components`, `allocationPriority`, `effectiveFrom`, `effectiveTo`, `minimumMinutes`, `maximumMinutes`, `requiresApproval`, `internalCost`. `id` is a client UUIDv7 generated silently, never asked. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createResourcePackage` body |
| Code `code` | text field | required | — | — | — | — | `createResourcePackage` body |
| Name `name` | text field | required | — | — | — | — | `createResourcePackage` body |
| Description `description` | text area | optional | — | — | — | — | `createResourcePackage` body |
| Applicable venues `applicableVenueIds` | multi-picker: choose applicable venues | optional | — | — | — | — | `createResourcePackage` body |
| Components `components` | repeatable rows | optional | — | — | — | — | `createResourcePackage` body |
| ID `components[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createResourcePackage` body |
| Resource type `components[].resourceTypeId` | picker: choose a resource type | optional | — | — | shows names, sends the id | — | `createResourcePackage` body |
| Category `components[].categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createResourcePackage` body |
| Resource `components[].resourceId` | picker: choose a resource | optional | — | — | shows names, sends the id | A fixed component, and the exception rather than the rule. Meeting Room A really is Meeting Room A; the technician is not. | `createResourcePackage` body |
| Quantity `components[].quantity` | number field | required | 1 | — | — | — | `createResourcePackage` body |
| Mandatory `components[].mandatory` | toggle | optional | on | — | — | — | `createResourcePackage` body |
| Required qualifications `components[].requiredQualifications` | list of values (chips) | optional | — | — | — | — | `createResourcePackage` body |
| Required attributes `components[].requiredAttributes` | key and value settings | optional | — | — | — | — | `createResourcePackage` body |
| Substitute resources `components[].substituteResourceIds` | multi-picker: choose substitute resources | optional | — | — | — | — | `createResourcePackage` body |
| Scope path `components[].scopePath` | text field | optional | — | — | — | — | `createResourcePackage` body |
| Allocation priority `allocationPriority` | number field | optional | 0 | — | — | — | `createResourcePackage` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createResourcePackage` body |
| Effective to `effectiveTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createResourcePackage` body |
| Minimum minutes `minimumMinutes` | number field (minutes) | optional | — | — | — | — | `createResourcePackage` body |
| Maximum minutes `maximumMinutes` | number field (minutes) | optional | — | — | — | — | `createResourcePackage` body |
| Requires approval `requiresApproval` | toggle | optional | off | — | — | — | `createResourcePackage` body |
| Internal cost `internalCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createResourcePackage` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `createResourcePackage` body |

**Form: Save package** (modal, opened by *Save package*; *Save package* calls `updateResourcePackage`, *Cancel* sends nothing)

**Collects what `updateResourcePackage` sends before it is called.** Required: `code`, `name`. Optional: `description`, `applicableVenueIds`, `components`, `allocationPriority`, `effectiveFrom`, `effectiveTo`, `minimumMinutes`, `maximumMinutes`, `requiresApproval`, `internalCost`. `id` is a client UUIDv7 generated silently, never asked. Dismissing sends nothing; the screen behind is unchanged.

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

- **Code, name, description, applicable venues**: Code unique; venues multi-select (a package may span venues). *(source: screens/P08-venue-back-office.yaml#BO-861 / contracts/satellite/resources.yaml#createResourcePackage)*
- **Components**: Rows of component kind (Specific resource / Resource type / Skill-based placeholder), quantity, mandatory or optional, substitutes (alternative resources or types), required qualification for placeholders. *(source: screens/P08-venue-back-office.yaml#BO-861 / screens/P08-venue-back-office.yaml#BO-862 / contracts/satellite/resources.yaml#/components/schemas/ResourcePackage)*
- **Allocation priority, effective dates, minimum/maximum duration, approval requirement, internal cost**: Priority number (higher first), effective from-to dates, duration in minutes or hours, approval toggle, internal cost in AED (not a guest price). *(source: contracts/satellite/resources.yaml#createResourcePackage)*

#### Outputs: what the screen shows and produces

**Shown**

**Packages** (data table, from `listResourcePackages`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Effective from | 1 Oct 2026 | — |
| Effective to | 1 Oct 2026 | — |
| Requires approval | yes / no (icon or chip) | — |

**Components** (data table, from `createResourcePackage`): One row per component: resource or resource type, quantity, mandatory or optional, substitutes (the pack's four separate drop-downs).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Applicable venues | list or chips (count when long) | — |
| Components | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Resource type | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Resource | the name it points at, never the id | A fixed component, and the exception rather than the rule. Meeting Room A really is Meeting Room A; the technician is not. |
| Quantity | 1,234 | — |
| Mandatory | yes / no (icon or chip) | — |
| Required qualifications | list or chips (count when long) | — |
| Required attributes | grouped details | — |
| Substitute resources | list or chips (count when long) | — |
| Allocation priority | 1,234 | — |
| Effective from | 1 Oct 2026 | — |
| Effective to | 1 Oct 2026 | — |
| Minimum minutes | 1,234 | — |
| Maximum minutes | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create package (primary button) | `createResourcePackage` POST `/resource-packages` | ResourcePackage | ResourcePackage | — | opens modal first |
| Save package (secondary button) | `updateResourcePackage` PUT `/resource-packages/{packageId}` | ResourcePackage | ResourcePackage | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Package list**: Code, name, components summary ("Cabana + 2 towels + locker + attendant"), venues, effective dates, approval flag. *(source: contracts/satellite/resources.yaml#listResourcePackages)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save package**: Create or full update (PUT replaces the package, VO-R04). *(source: contracts/satellite/resources.yaml#updateResourcePackage)*

**Data it reads**: `listResourcePackages` (onLoad, The packages)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource package bundle configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource package bundle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource package bundle configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-862`: Dependency rules and packages use the same component picker.
- Match `BO-894`: The resource combination builder for experiences reuses packages.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
packages:
- code: PKG-VIPCAB
  name: VIP Cabana Package
  components: 1 Cabana (Beach, mandatory), 4 Towels, 1 Locker, 1 Service attendant (placeholder)
  cost: AED 140
- code: PKG-CONF
  name: Conference Package
  components: Meeting Room A, Projector, Screen, Microphone, 1 Technician with AV Level 2
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

- Multiple resources can be bundled to one product (e.g. a VIP Cabana package = room + attendant) so the system knows every resource needed when it is booked. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-479)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-861` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-861`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 14: Works in Resource Package & Bundle Configuration → Allow commonly used combinations of resources to be predefined and assigned as a single operational package.

#### Acceptance for the design

- [ ] Every input above is drawn (59), with its required mark, default, format and its error state.
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-861?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Create package, Save package.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-862` Multi-Venue Resource Assignment

**Control where resources may operate and whether they can be shared across venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/multi-venue-resource-assignment-bo-862` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read returns a resource's current venue assignment.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where a resource may operate - its primary venue, any secondary venues, whether it is pooled and bookable across venues, and the travel buffer between venues that the calendar subtracts like setup. The one thing to get right: the sharing model is one plain choice (Venue-exclusive, Venue-shared, Tenant-wide, Temporary transfer, Centrally pooled) and the travel buffer is shown as unavailable time.

**Known correction pending (do not draw the wrong version)**

- **The screen has only Save, Cancel and an empty detail panel; the gap note says the pack gives nothing drawable** Why: The pack lists twelve settings and five sharing models. *(source: screens/P08-venue-back-office.yaml#BO-862; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Department ownership, venue availability, transfer time, venue-specific restrictions and venue-specific cost have no field** Why: The pack requires them; ResourceVenueAssignment has venues, three switches, travel buffer and dates only. *(source: screens/P08-venue-back-office.yaml#BO-862 / contracts/satellite/resources.yaml#/components/schemas/ResourceVenueAssignment; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read returns the current venue assignment** Why: The write is a full replace (VO-R04); without a read the form opens blank and overwrites blind. *(source: contracts/satellite/resources.yaml#setResourceVenueAssignment / contracts/satellite/resources.yaml#getResource; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Sharing model**: One choice of the pack's five; it sets the underlying switches (shared pool, cross-venue booking allowed, transfer required) which are shown read-only beneath for clarity. Temporary transfer requires an effective to-date. *(source: screens/P08-venue-back-office.yaml#BO-862 / contracts/satellite/resources.yaml#/components/schemas/ResourceVenueAssignment)*
- **Primary and secondary venues**: Primary venue required (single); secondary venues as ticked list of the tenant's venues the person may manage; a venue cannot be both. *(source: contracts/satellite/resources.yaml#setResourceVenueAssignment)*
- **Travel buffer, effective dates**: Travel buffer in minutes (0 default) with preview "Booked at Aqua Park until 12:00 - earliest at Summit Peaks 12:40"; effective from-to dates. *(source: contracts/satellite/resources.yaml#setResourceVenueAssignment)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Venue availability**: A week grid per assigned venue showing on which days the resource is available there (as on the client board). *(source: screens/P08-venue-back-office.yaml#BO-862)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save venue assignment**: Replaces the assignment (VO-R04). Refused when existing bookings would overlap once the travel buffer applies; the refusal lists each clash with times and the reason travel buffer. *(source: contracts/satellite/resources.yaml#setResourceVenueAssignment / contracts/satellite/resources.yaml#/components/schemas/ResourceConflictProblem)*

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-venue resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-venue resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-venue resource yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-venue resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Overlapping assignment, or the travel buffer cannot be met (ResourceConflictProblem) |

#### Edge cases to draw

- **Instructor assigned at two venues without venue-specific qualification**: Warn "Not authorised for Summit Peaks slopes"; assignment saves but the instructor is not offered there. *(source: screens/P08-venue-back-office.yaml#BO-863)*
- **Person lacks tenant rights**: Secondary venues outside their scope are not listed; a note explains (VO-R08). *(source: contracts/satellite/resources.yaml#setResourceVenueAssignment)*

#### Consistency with other screens

- Match `BO-864`: The travel buffer shows on the calendar as its own band between bookings at different venues.
- Match `BO-945`: A move between venues is booked as a transfer cost there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
resource: Portable Projector P-17
assignment:
  model: Venue-shared
  primary: Aqua Park
  secondary: Summit Peaks
  travelBuffer: 40 min
  effective: 1 Oct 2026 - open
```

#### Permissions

- `setResourceVenueAssignment` → `RESOURCE_MANAGE` (configure) · staff
- `getResource` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-862` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-862`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 16: Works in Multi-Venue Resource Assignment → Control where resources may operate and whether they can be shared across venues.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-862?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-863` Resource Lifecycle, Governance & Audit

**Manage the entire operational lifecycle of a resource from creation through retirement while maintaining full traceability.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block A · ticket #20708 (APP-SETUP-BO-863) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `RESOURCE_MANAGE`, `RESOURCE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-lifecycle-governance-audit-bo-863` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Creating and editing resources is BO-095 and BO-857; this screen governs the lifecycle (design-notes correction venue-operations BO-863). Removed 2 October 2026 (CHG-WIR-001): Creating and editing resources is BO-095 and BO-857; this screen governs the lifecycle (design-notes correction venue-operations BO-863).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Governs a resource's lifecycle - Draft, Pending approval, Approved, Active, Temporarily unavailable, Under maintenance, Suspended, Retired, Archived - with allowed transitions, approval requirements (maker-checker, manager, finance, operations), reasons, replacement resource, disposal and depreciation references, and the immutable audit trail of every material change. The one thing to get right: show the state machine and the audit timeline, not a form of nine selects.

**Known correction pending (do not draw the wrong version)**

- **Approval stages (Maker-checker, Manager, Finance, Operations approval) and permissions (Create, Edit, Approve, Activate) drawn as eight buttons** Why: They are configuration of who may do what, not actions on this screen. *(source: screens/P08-venue-back-office.yaml#BO-863; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Allowed status transitions" is listed as configurable but no operation stores transition rules** Why: setResourceLifecycleState moves a resource; nothing writes the allowed-transition configuration the pack asks for. *(source: screens/P08-venue-back-office.yaml#BO-863 / contracts/satellite/resources.yaml#setResourceLifecycleState; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): createResource and updateResource bound here (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Allowed status transitions | select field | — | — | — | — | — | — |
| Approval requirements | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Retirement reason | select field | — | — | — | — | — | — |
| Suspension reason | select field | — | — | — | — | — | — |
| Replacement resource | select field | — | — | — | — | — | — |
| Disposal information | select field | — | — | — | — | — | — |
| Depreciation reference | select field | — | — | — | — | — | — |
| Asset-retirement information | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **State change**: Target state from the allowed transitions only, reason (required for suspend and retire), effective from, replacement resource (on retire), disposal details (on retire/archive). *(source: screens/P08-venue-back-office.yaml#BO-863 / contracts/satellite/resources.yaml#setResourceLifecycleState)*
- **Approval controls**: Four-eyes or dual control on resource changes, minimum approvers, approver groups; set once per tenant, shown here read-only with a link. *(source: contracts/spine/approvals.yaml#setApprovalControlPolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Maker-checker approval (primary button) | navigation or local | — | — | — | — |
| Manager approval (secondary button) | navigation or local | — | — | — | — |
| Finance approval (secondary button) | navigation or local | — | — | — | — |
| Operations approval (secondary button) | navigation or local | — | — | — | — |
| Create (secondary button) | navigation or local | — | — | — | — |
| Edit (secondary button) | navigation or local | — | — | — | — |
| Approve (secondary button) | navigation or local | — | — | — | — |
| Activate (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **State diagram**: The nine states as a flow with the current state highlighted and allowed next states clickable. *(source: screens/P08-venue-back-office.yaml#BO-863)*
- **Audit timeline**: Every material change with who, when, before/after and reason; immutable. *(source: contracts/satellite/resources.yaml#getResourceAuditTrail)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Move to state**: Where approval is required, the change goes to Pending approval and the approver is notified. *(source: contracts/satellite/resources.yaml#setResourceLifecycleState / contracts/spine/approvals.yaml#setApprovalMatrix)*

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource lifecycle governance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource lifecycle governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource lifecycle governance configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem); 409 The transition is not allowed from the current … |

#### Consistency with other screens

- Match `BO-069`: Retiring a resource that is also an asset should reflect the asset's retirement (DI-770).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
resource:
  name: SUV 2 (Dubai 45821)
  state: Under maintenance
  next: Active, Suspended, Retired
audit:
- 28 Sep 2026 10:14 - Fatima Al Hashimi - Active > Under maintenance - Tyre replacement
```

#### Permissions

- `getResourceAuditTrail` → `RESOURCE_VIEW` (read) · staff
- `setResourceLifecycleState` → `RESOURCE_MANAGE` (configure) · staff
- `setApprovalControlPolicy` → `APPROVAL_CONFIGURE` (configure) · staff
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

49 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.51 | System shall support reservation approvals. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 1.2.76 | System shall support configurable approval workflows. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 2.12.4 | The system should support configuration of required access level to allow refund, exchange and/or void actions. At minimum, the system should provide: - Ability to enable/disable supervisor access … | Ticketing Sales | CONTRACTED | `setApprovalMatrix` |
| 3.3.31 | Segregation of Duties - System shall enforce segregation of duties in access policies. | Admission and Access | CONTRACTED | `setApprovalMatrix` |
| 7.1.22 | The system shall support approval workflows for user creation, role assignment, permission changes, privileged access requests, and user deactivation. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.1.24 | The system shall support configurable approval requirements for refunds, ticket cancellations, price changes, promotion changes, membership changes, wallet adjustments, and manual overrides. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.5.10 | Support multi-level approval processes for complimentary tickets, VIP invitations and sponsor allocations with full audit history. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 11.1.1 | Provides configurable workflows requiring one or more approvals before sensitive actions can be executed. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.2 | Approval Workflow Configuration System shall allow administrators to configure approval workflows for different business processes. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.3 | Multi-Level Approval System shall support single-level and multi-level approval chains. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.4 | Role-Based Approval Routing System shall automatically route approval requests based on organizational hierarchy and user roles. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.5 | Escalation Rules System shall automatically escalate pending approvals after configurable time thresholds. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| … 37 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-863` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-863`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 18: Works in Resource Lifecycle, Governance & Audit → Manage the entire operational lifecycle of a resource from creation through retirement while maintaining full traceability.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-863?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Maker-checker approval, Manager approval, Finance approval, Operations approval, Create, Edit, Approve, Activate.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cloneResource": {"method":"POST","path":"/resources/{resourceId}/clone","contract":"resources","summary":"Copy a resource and its configuration into new ones","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Resource"},
"createResource": {"method":"POST","path":"/resources","contract":"resources","summary":"Define a bookable resource","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Resource","responds":"Resource"},
"createResourceAttribute": {"method":"POST","path":"/resource-attributes","contract":"resources","summary":"Define a customer attribute","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceAttributeDefinition","responds":"ResourceAttributeDefinition"},
"createResourceCategory": {"method":"POST","path":"/resource-categories","contract":"resources","summary":"Add a category or subcategory","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceCategory","responds":"ResourceCategory"},
"createResourcePackage": {"method":"POST","path":"/resource-packages","contract":"resources","summary":"Define a reusable combination","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourcePackage","responds":"ResourcePackage"},
"createResourceType": {"method":"POST","path":"/resource-types","contract":"resources","summary":"Define a class of resource","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceType","responds":"ResourceType"},
"getResource": {"method":"GET","path":"/resources/{resourceId}","contract":"resources","summary":"One resource, with every configured section","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Resource"},
"getResourceAuditTrail": {"method":"GET","path":"/resources/{resourceId}/audit","contract":"resources","summary":"Every material change, with who and why","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAuditEntry"},
"getResourceAvailability": {"method":"GET","path":"/resources/{resourceId}/availability","contract":"resources","summary":"When it is free, with conflicts already resolved","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"ResourceAvailability"},
"getResourceDependencies": {"method":"GET","path":"/resources/{resourceId}/dependencies","contract":"resources","summary":"What this resource requires, conflicts with, or substitutes for","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceDependency"},
"getResourceHierarchy": {"method":"GET","path":"/resources/{resourceId}/hierarchy","contract":"resources","summary":"What this resource contains, and what contains it","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceHierarchy"},
"getResourceQualifications": {"method":"GET","path":"/resources/{resourceId}/qualifications","contract":"resources","summary":"What an instructor or staff resource is certified to do, and until when — as saved","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Qualification"},
"getResourceUtilisation": {"method":"GET","path":"/resource-utilisation","contract":"resources","summary":"How much of each resource's available time was used","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ResourceUtilisation"},
"listResourceAttributes": {"method":"GET","path":"/resource-attributes","contract":"resources","summary":"The customer-defined fields on a resource","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAttributeDefinition"},
"listResourceCategories": {"method":"GET","path":"/resource-categories","contract":"resources","summary":"The classification tree beneath the types","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceCategory"},
"listResourcePackages": {"method":"GET","path":"/resource-packages","contract":"resources","summary":"Predefined combinations assigned as one","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourcePackage"},
"listResourceTypes": {"method":"GET","path":"/resource-types","contract":"resources","summary":"The classes of resource this organisation supports","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceType"},
"listResources": {"method":"GET","path":"/resources","contract":"resources","summary":"Resources at this venue","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"availableFrom","in":"query","required":null},{"name":"availableTo","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"setApprovalControlPolicy": {"method":"PUT","path":"/approval-control-policies","contract":"approvals","summary":"Require a second, independent pair of eyes","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalControlPolicy","responds":"ApprovalControlPolicy"},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setResourceDependencies": {"method":"PUT","path":"/resources/{resourceId}/dependencies","contract":"resources","summary":"Define what must come with it, and what cannot","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceDependency"},
"setResourceHierarchy": {"method":"PUT","path":"/resources/{resourceId}/hierarchy","contract":"resources","summary":"Re-parent a resource, or attach children to it","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceHierarchy","responds":"ResourceHierarchy"},
"setResourceLifecycleState": {"method":"POST","path":"/resources/{resourceId}/state","contract":"resources","summary":"Move a resource through its lifecycle, with a reason","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Resource"},
"setResourceVenueAssignment": {"method":"PUT","path":"/resources/{resourceId}/venues","contract":"resources","summary":"Where it may operate, and whether it travels","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceVenueAssignment","responds":"ResourceVenueAssignment"},
"updateResource": {"method":"PUT","path":"/resources/{resourceId}","contract":"resources","summary":"Change a resource","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Resource","responds":"Resource"},
"updateResourceCategory": {"method":"PUT","path":"/resource-categories/{categoryId}","contract":"resources","summary":"Change a category","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceCategory","responds":"ResourceCategory"},
"updateResourcePackage": {"method":"PUT","path":"/resource-packages/{packageId}","contract":"resources","summary":"Change a combination","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourcePackage","responds":"ResourcePackage"},
"updateResourceType": {"method":"PUT","path":"/resource-types/{resourceTypeId}","contract":"resources","summary":"Change a class of resource","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceType","responds":"ResourceType"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalControlPolicy": {"type":"object","x-ticvai-persistence":"approvals.control_policy","description":"Approvals boards 6.2 and 6.3. **Which decisions one person may not take alone** — distinct from which roles one person may not hold, which is `identity.setSegregationRules`.\n","required":["code","control"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"appliesAboveValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"control":{"type":"string","enum":["fourEyes","dualControl","separationFromRequester","separationFromExecutor"],"description":"**`fourEyes` is two different people; `dualControl` is two people from different groups.** The second is stronger and is what a finance auditor means, and collapsing them makes the stronger control unexpressible.\n"},"requiredApproverGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minimumApprovers":{"type":"integer","default":2},"requiresStepUp":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"breakGlassAllowed":{"type":"boolean","default":false,"description":"**Whether the control may be overridden in an emergency**, and if so it raises an alert rather than passing quietly. A control with no break-glass will be worked around by hand at three in the morning, which is worse.\n"},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"Qualification": {"type":"object","x-ticvai-persistence":"resources.qualification","description":"1.2.36. **A role is not a skill**, and the check happens before assignment rather than after.\n","required":["code","name"],"properties":{"resourceId":{"type":"string","format":"uuid","readOnly":true,"description":"**The resource that holds this qualification.** Set from the path of `setResourceQualifications`; without it a stored qualification belongs to nobody and the check before assignment has nothing to check against. One row per resource and `code`.\n"},"code":{"type":"string"},"name":{"type":"string"},"issuedAt":{"type":"string","format":"date","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**The field that makes this worth having.** A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one.\n"},"issuer":{"type":"string","nullable":true},"documentAssetId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true}}},
"ResourceAttributeDefinition": {"type":"object","x-ticvai-persistence":"resources.attribute_definition","description":"Board 1.05. **A typed, validated field the customer adds.** The alternative was a column per customer request, which is a release per customer.\n","required":["code","label","dataType"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"label":{"type":"string"},"dataType":{"type":"string","enum":["text","number","decimal","currency","date","dateTime","boolean","singleSelect","multiSelect","lookup","attachment","url","measurement","formula"]},"applicableResourceTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"applicableCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"mandatory":{"type":"boolean","default":false},"defaultValue":{"nullable":true},"allowedValues":{"type":"array","items":{"type":"string"}},"minimum":{"type":"number","nullable":true},"maximum":{"type":"number","nullable":true},"validationExpression":{"type":"string","nullable":true},"searchable":{"type":"boolean","default":false,"description":"**The flag that decides whether `suggestResources` can use it.** An attribute nobody can filter by cannot take part in skill-based matching, which is the main reason the customer defined it.\n"},"scopePath":{"type":"string"}}},
"ResourceAuditEntry": {"type":"object","x-ticvai-persistence":"resources.resource_audit","description":"Board 1.10. **Immutable, and it carries the previous value.**","properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"actorId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"field":{"type":"string","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"sourceChannel":{"type":"string","nullable":true},"apiOrigin":{"type":"string","nullable":true},"correlationId":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"ResourceAvailability": {"type":"object","description":"**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"freeWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"}}}},"blockedWindows":{"type":"array","description":"**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","held","setup","teardown","maintenance","blackout","closed","cleaning"],"description":"`held` is a live `ResourceHold` (rev 3 REV3-15): taken now, free again if it expires. `cleaning` is a cleaning the resource's `cleaningPolicy` places (W10, 29 September).\n"}}}}}},
"ResourceCategory": {"type":"object","x-ticvai-persistence":"resources.resource_category","description":"Board 1.03. Beneath the type — *Equipment → AV → Lighting*, *Rental → Towels*. **Configuration cascades down the tree**, which is the reason it is a tree.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"parentCategoryId":{"type":"string","format":"uuid","nullable":true},"applicableResourceTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"displayOrder":{"type":"integer","default":0},"tags":{"type":"array","items":{"type":"string"}},"reportingGroup":{"type":"string","nullable":true},"costCentre":{"type":"string","nullable":true},"defaultAttributes":{"type":"object","additionalProperties":true},"defaultApprovalWorkflowId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceDependency": {"type":"object","x-ticvai-persistence":"resources.resource_dependency","description":"Board 1.07. **Evaluated before an assignment is confirmed.** *Stage A requires Sound System A and Lighting Rig A.*\n","required":["kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["requires","requiresOneOf","requiresAll","conflictsWith","cannotOperateSimultaneously","preferredWith","substituteFor","backupFor","sharesCapacityWith"]},"targetResourceId":{"type":"string","format":"uuid","nullable":true},"targetResourceTypeId":{"type":"string","format":"uuid","nullable":true},"minimumQuantity":{"type":"integer","default":1},"maximumQuantity":{"type":"integer","nullable":true},"mandatory":{"type":"boolean","default":true},"priority":{"type":"integer","default":0},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ResourceHierarchy": {"type":"object","description":"Board 1.06. Ancestors and the immediate subtree, with the relationship named.","properties":{"resourceId":{"type":"string","format":"uuid"},"ancestors":{"type":"array","items":{"$ref":"#/components/schemas/ResourceRelation"}},"children":{"type":"array","items":{"$ref":"#/components/schemas/ResourceRelation"}}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourceLifecycleState": {"type":"string","description":"Board 1.10. **States of one machine**, whose allowed transitions are configuration.","enum":["draft","pendingApproval","approved","active","temporarilyUnavailable","underMaintenance","suspended","retired","archived"]},
"ResourcePackage": {"type":"object","x-ticvai-persistence":"resources.resource_package","description":"Board 1.08. **A package may hold placeholders.** \"One technician\" is a slot, and naming a person would make the package unbookable whenever they are off.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"applicableVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"components":{"type":"array","items":{"$ref":"#/components/schemas/ResourceRequirement"}},"allocationPriority":{"type":"integer","default":0},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"minimumMinutes":{"type":"integer","nullable":true},"maximumMinutes":{"type":"integer","nullable":true},"requiresApproval":{"type":"boolean","default":false},"internalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"ResourceRelation": {"type":"object","x-ticvai-persistence":"resources.resource_relation","required":["resourceId","relation"],"properties":{"resourceId":{"type":"string","format":"uuid"},"relation":{"type":"string","enum":["contains","belongsTo","locatedIn","operatedBy","supportedBy","partOf","dedicatedTo"]},"effectiveFrom":{"type":"string","format":"date","nullable":true},"priority":{"type":"integer","default":0},"scopePath":{"type":"string"}}},
"ResourceRequirement": {"type":"object","x-ticvai-persistence":"resources.resource_requirement","description":"**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n","required":["quantity"],"properties":{"id":{"type":"string","format":"uuid"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"},"quantity":{"type":"integer","default":1},"mandatory":{"type":"boolean","default":true},"requiredQualifications":{"type":"array","items":{"type":"string"}},"requiredAttributes":{"type":"object","additionalProperties":true},"substituteResourceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"}}},
"ResourceType": {"type":"object","x-ticvai-persistence":"resources.resource_type","description":"Board 1.02. **The class, and the ten switches that decide which parts of the platform a resource of this class touches.** `Resource.kind` was an enum and this is the table behind it — a customer adding \"Golf Buggy\" does not need a release.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"icon":{"type":"string","nullable":true},"displayColour":{"type":"string","nullable":true},"nature":{"type":"string","enum":["physical","human","virtual"],"description":"**Human resources point at a principal and are rostered by `workforce`.** The nature decides which other context owns the thing, which is why it is not a free label.\n"},"reservable":{"type":"boolean","default":true},"rentable":{"type":"boolean","default":false},"capacityControlled":{"type":"boolean","default":false},"scheduleControlled":{"type":"boolean","default":true},"inventoryControlled":{"type":"boolean","default":false},"qualificationRequired":{"type":"boolean","default":false},"maintenanceControlled":{"type":"boolean","default":false},"checkInOutSupported":{"type":"boolean","default":false},"depositApplicable":{"type":"boolean","default":false},"customerSelectable":{"type":"boolean","default":false,"description":"**A ceiling, not a permission.** Whether a guest may actually choose is decided per ticket type by `setResourceSelectionPolicy`; a type with this false can never be choosable, and a type with it true still is not until a product says so.\n"},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"ResourceUtilisation": {"type":"object","description":"Board 10.02. **Booked time over available time**, where available knows about schedules, blocks, setup and travel.\n","properties":{"key":{"type":"string"},"label":{"type":"string"},"availableMinutes":{"type":"integer"},"bookedMinutes":{"type":"integer"},"blockedMinutes":{"type":"integer"},"utilisationPercent":{"type":"number"},"bookingCount":{"type":"integer"}}},
"ResourceVenueAssignment": {"type":"object","x-ticvai-persistence":"resources.venue_assignment","description":"Board 1.09. **The travel buffer is subtracted from availability**, like setup and teardown, so a shared instructor is not double-booked across a journey they cannot make.\n","required":["primaryVenueId"],"properties":{"primaryVenueId":{"type":"string","format":"uuid"},"secondaryVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"sharedPool":{"type":"boolean","default":false},"crossVenueBookingAllowed":{"type":"boolean","default":false},"travelBufferMinutes":{"type":"integer","default":0},"transferRequired":{"type":"boolean","default":false},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}}
}
```
