# WS113 — ACCREDITATION board 6

**10 screens · 10 operations · 7 schemas · 4 permissions**

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
  `ACCREDITATION_APPLY, ACCREDITATION_CONFIGURE, ACCREDITATION_MANAGE, ACCREDITATION_VIEW`. A control nobody can use must say so,
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
| `BO-664` | Accreditation Lifecycle Command Center | B–D | 0 | 0 | 6 | 3 | 1 | 6 | — | notStarted (—) |
| `BO-665` | Accreditation Status Workflow | B–D | 7 | 0 | 6 | 4 | 0 | 6 | — | notStarted (—) |
| `BO-666` | Validity Period Configuration | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-667` | Event & Venue Accreditation Assignment | B–D | 25 | 20 | 6 | 1 | 0 | 6 | — | notStarted (—) |
| `BO-668` | Multi-Venue Accreditation Management | B–D | 0 | 16 | 6 | 6 | 0 | 6 | — | notStarted (—) |
| `BO-669` | Temporary & Seasonal Accreditation | B–D | 3 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-670` | Suspension & Reactivation Management | B–D | 9 | 0 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `BO-671` | Accreditation Revocation Management | B–D | 0 | 0 | 6 | 4 | 0 | 6 | — | notStarted (—) |
| `BO-672` | Expiry Monitor & Expiration Rules | B–D | 0 | 14 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `BO-673` | Accreditation Renewal Workspace | B–D | 0 | 0 | 6 | 4 | 1 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-664, BO-666, BO-667, BO-668, BO-669, BO-671, BO-673 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-664` Accreditation Lifecycle Command Center

**Central operational dashboard for accreditation lifecycle status.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-lifecycle-command-center-bo-664` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The landing page of the lifecycle board: how many accreditations are active, pending activation, expiring, expired, suspended or revoked, with the alerts that need someone today (expiring this week, suspensions due for review, expired accreditations whose credential is still live). Per VO-R02 it is a command-centre dashboard, not a table. The one thing to get right: it surfaces cascade failures (an expired or revoked accreditation with an active credential) as the top alert, because the pack calls independent status a significant security gap.

**Known correction pending (do not draw the wrong version)**

- **Pattern listDetail with an empty data table** Why: The pack page is a KPI-card dashboard with alerts and quick actions; per VO-R02 it is a command centre. *(source: screens/P08-venue-back-office.yaml#BO-664; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Pending activation, Expiring, Renewal eligible and Renewal pending are not holder statuses** Why: AccreditationHolder.status is active, suspended, revoked, expired, archived; these tiles must be derived (credential activatedAt empty, validTo within N days, open renewal application), and need a count read rather than the full holder list. *(source: screens/P08-venue-back-office.yaml#BO-664 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listAccreditationHolders returns a plain array with no paging** Why: A dashboard over thousands of holders needs counts (getKpiValues or a summary) and lists need cursor paging (VO-R12). *(source: contracts/satellite/accreditation.yaml#listAccreditationHolders; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

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

- **filters (Event, Venue, Programme, Category, Organisation, Accreditation type, Status, Validity period)**: Filter bar above the tiles. Status and Accreditation type (Temporary, Seasonal, Event, Permanent) are chips; Validity period is a date range. Venue from the top bar (VO-R09). *(source: screens/P08-venue-back-office.yaml#BO-665)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Active, Pending activation, Expiring soon (7 days), Expired, Suspended, Revoked, Renewal eligible, Renewal pending, Temporary, Seasonal, each with count and change since yesterday, each opening the matching filtered list (Expiring soon opens BO-672, Suspended opens BO-670 list, Renewal opens BO-673). *(source: screens/P08-venue-back-office.yaml#BO-664 / screens/P08-venue-back-office.yaml#BO-665)*
- **Alerts**: In this order: Expired accreditation with active credential (red, security), Lifecycle synchronisation exceptions, Suspensions requiring review (reviewAt today or past), Temporary credentials nearing expiry, Upcoming expirations, Pending renewals. Each row names the holder and offers its action. *(source: screens/P08-venue-back-office.yaml#BO-665 / screens/P08-venue-back-office.yaml#BO-673)*
- **Document expiry before event**: A tile or alert "Documents expiring before the event" (e.g. Emirates ID expiring before 15 Dec) that opens BO-672's document bucket; per DI-663 these raise a resubmission and block the credential if unresolved. *(source: DI-663 / contracts/satellite/accreditation.yaml#listAccreditationDocuments)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Quick actions**: Suspend, Reactivate, Revoke, Renew, Extend validity, View expiring; the first four open a holder picker then the shared status dialog (BO-670/671) or BO-673. *(source: screens/P08-venue-back-office.yaml#BO-665)*

**Data it reads**: `listAccreditationHolders` (onLoad, Lifecycle at a glance)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-665` Accreditation Status Workflow: *Accreditation Status Workflow*; carries `holderId`
- → `BO-666` Validity Period Configuration: *Validity Period Configuration*
- → `BO-667` Event & Venue Accreditation Assignment: *Event & Venue Accreditation Assignment*; carries `programmeId`
- → `BO-668` Multi-Venue Accreditation Management: *Multi-Venue Accreditation Management*
- → `BO-669` Temporary & Seasonal Accreditation: *Temporary & Seasonal Accreditation*
- → `BO-670` Suspension & Reactivation Management: *Suspension & Reactivation Management*; carries `holderId`
- → `BO-671` Accreditation Revocation Management: *Accreditation Revocation Management*; carries `holderId`
- → `BO-672` Expiry Monitor & Expiration Rules: *Expiry Monitor & Expiration Rules*; carries `holderId`
- → `BO-673` Accreditation Renewal Workspace: *Accreditation Renewal Workspace*; carries `holderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation lifecycle list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation lifecycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation lifecycle yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation lifecycle are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Nightly expiry job has not run**: Show "Automatic expiry last ran 01:00 today"; if older than a day, an amber alert, since the pack requires expiry without manual intervention. *(source: screens/P08-venue-back-office.yaml#BO-669 / screens/P08-venue-back-office.yaml#BO-672)*
- **Holder list large (thousands)**: Tiles come from counts, never by loading every holder into the page. *(source: contracts/satellite/accreditation.yaml#listAccreditationHolders)*

#### Consistency with other screens

- Match `BO-654`: Suspended and Revoked counts match the access board for the same filters.
- Match `BO-615`: Same command-centre pattern and filter bar.
- Match `BO-684`: Executive dashboard status tiles use the same status names and counts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  active: 1186
  pendingActivation: 54
  expiringSoon: 61
  expired: 140
  suspended: 4
  revoked: 2
  renewalEligible: 88
  renewalPending: 17
  temporary: 233
  seasonal: 412
alerts:
- 3 expired accreditations still have an active credential (Al Noor Contracting)
- Suspension review due today for James Carter (Security investigation)
- 12 Emirates IDs expire before Summit Peaks Winter Festival 2026
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

- Lifecycle: activation, expiry, renewal, suspension; if a document (e.g. Emirates ID) expires before the event, a resubmission request is raised and the credential is blocked if unresolved. Applicants are notified at each status change (approved, rejected, needs validation). *(client request · MoM 7 Sep 2026, 4.6 / 4.7 Lifecycle & Notifications · DI-663)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-664` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-664`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 1: Opens Accreditation Lifecycle Command Center → Central operational dashboard for accreditation lifecycle status.
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F222 branch at step 1 (expected): when Nothing has been set up on Accreditation Lifecycle Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F222 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-664?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-665`, `BO-666`, `BO-667`, `BO-668`, `BO-669`, `BO-670`, `BO-671`, `BO-672`, `BO-673`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-665` Accreditation Status Workflow

**Configure and manage the accreditation lifecycle statuses.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each transition may define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/accreditation-status-workflow-bo-665` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The accreditation lifecycle as a workflow: the statuses (Draft to Closed) and which transitions are allowed, with what permission, approval, reason, notification and credential/access action each one triggers. The pack asks for configuration; the contract has a fixed lifecycle and one call that moves a holder. The one thing to get right: draw the lifecycle as a state diagram that shows the cascade (accreditation > credential > access) for each transition, with the rules the client can configure clearly separated from the ones the platform fixes.

**Known correction pending (do not draw the wrong version)**

- **The screen is a configuration editor but the only bound call moves one holder (setAccreditationStatus)** Why: No contract stores lifecycle statuses, permitted transitions or per-transition rules; MATRIX 12.1.32 is met by fixed statuses, the pack asks for configurable ones. *(source: screens/P08-venue-back-office.yaml#BO-666 / contracts/satellite/accreditation.yaml#setAccreditationStatus / MATRIX 12.1.32; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Select fields "Key requirement 12.1.32", "Notification", "Credential action", "Access-right action" generated as plain selects** Why: The first is pack prose, not a field; the others belong to a transition, not to the screen. *(source: screens/P08-venue-back-office.yaml#BO-665; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's statuses Expiring, Renewal Pending, Renewed and Closed have no contract value** Why: Holder status has active, suspended, revoked, expired, archived only; they must be derived or added. *(source: screens/P08-venue-back-office.yaml#BO-665 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a fixed lifecycle with per-transition permissions acceptable for the first release, or must the client add their own statuses?** → Drawn default accepted: Draw the fixed diagram with editable per-transition rules greyed. *(decided by Chinmay, 2026-10-02; DEC-482 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Required permission | select field | — | — | — | — | — | — |
| Approval requirement | select field | — | — | — | — | — | — |
| Reason requirement | select field | — | — | — | — | — | — |
| Notification | select field | — | — | — | — | — | — |
| Credential action | select field | — | — | — | — | — | — |
| Access-right action | select field | — | — | — | — | — | — |
| Key requirement: 12.1.32 | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **transition rule (per arrow)**: Click an arrow to edit Required permission (select of roles/permissions), Approval requirement (None / One approver / Two approvers), Reason requirement (Required / Optional), Notification (link to a BO-675 rule for that trigger), Credential action (None / Suspend / Reactivate / Revoke / Expire), Access-right action (None / Disable / Restore / Remove). These six are the pack's list. *(source: screens/P08-venue-back-office.yaml#BO-666)*
- **allowed transitions**: Fixed and shown locked: Active > Suspended > Active, Active > Revoked, Active > Expired. Revoked > Active is never drawn as available; the pack allows it only through an authorised exceptional process, shown as a dashed arrow "Exceptional - needs configuration". *(source: screens/P08-venue-back-office.yaml#BO-666)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lifecycle diagram**: Three swim lanes so the three records stop being confused: Application (Draft, Submitted, Under review, Information requested, Approved, Rejected, Withdrawn), Accreditation (Active, Suspended, Expiring, Expired, Renewal pending, Renewed, Revoked, Closed/Archived) and Credential (Pending print, Issued, Active, Lost, Replaced, Revoked, Expired). Cascade arrows between lanes per the pack's critical behaviour. *(source: screens/P08-venue-back-office.yaml#BO-665 / screens/P08-venue-back-office.yaml#BO-673 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication / …)*
- **Status label map**: Pack label against contract value (e.g. "Credential Pending" = application approved, credential pendingPrint; "Closed" = archived), so the client sees the mapping. *(source: screens/P08-venue-back-office.yaml#BO-665 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save transition rules**: Greyed "Not yet supported" until a workflow configuration contract exists (VO-R13); the diagram itself is read-only reference. *(source: DI-653)*

**Where the user goes next**

- → `BO-664` Accreditation Lifecycle Command Center: *Back to Accreditation Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation status workflow configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation status workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation status workflow configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Opened with a holderId (as the navigation passes)**: Show that holder's current position highlighted on the diagram and only the transitions available from it, each opening the shared status dialog. *(source: screens/P08-venue-back-office.yaml#BO-665 / contracts/satellite/accreditation.yaml#setAccreditationStatus)*

#### Consistency with other screens

- Match `BO-670`: Suspend/reactivate from the diagram use the shared status dialog.
- Match `BO-671`: Revoke from the diagram uses the shared dialog; the diagram's locked Revoked > Active matches BO-671's "permanent" wording.
- Match `BO-643`: Approval requirements per transition should reuse the approval policy vocabulary of the approvals board.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
transitions:
- from: Active
  to: Suspended
  permission: Accreditation manager
  approval: None
  reason: Required
  notify: Accreditation suspended (holder, organisation)
  credential: Suspend
  access: Disable
- from: Suspended
  to: Active
  permission: Accreditation manager
  approval: One approver
  reason: Required
  notify: Accreditation reactivated
  credential: Reactivate
  access: Restore
- from: Active
  to: Revoked
  permission: Security manager
  approval: One approver
  reason: Required
  notify: Accreditation revoked
  credential: Revoke
  access: Remove
```

#### Permissions

- `setAccreditationStatus` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.30 | Access Revocation - System shall support immediate revocation of accreditation access rights. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |
| 12.1.32 | Accreditation Status Workflow - System shall support accreditation lifecycle statuses. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |
| 12.1.34 | Accreditation Suspension - System shall support temporary suspension of accreditations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |
| 12.1.35 | Accreditation Revocation - System shall support permanent revocation of accreditations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-665` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-665`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 2: Works in Accreditation Status Workflow → Configure and manage the accreditation lifecycle statuses.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-665?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-664`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-666` Validity Period Configuration

**Configure how long an accreditation remains valid.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/validity-period-configuration-bo-666` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of AccreditationValidity.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How long an accreditation lasts, per programme: event duration, fixed period, seasonal, rolling or permanent; what happens at expiry (access revoked, grace period, auto-renew); and when renewal opens. Per VO-R14 BO-666, BO-669 (temporary and seasonal) and the rules half of BO-672/BO-673 all write the same validity record and are one "Validity and renewal" editor per programme. The one thing to get right: expiry is never "never" by accident; permanent needs a permission and a visible warning.

**Known correction pending (do not draw the wrong version)**

- **Write bound with no read** Why: There is no get operation for AccreditationValidity; a PUT that replaces the record cannot be edited safely without the current values (VO-R04). *(source: contracts/satellite/accreditation.yaml#setAccreditationValidity; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Start/end date and start/end time of validity, and per-holder override, have no field in AccreditationValidity** Why: The pack lists them; holders carry validFrom and validTo as dates only, with no times. *(source: screens/P08-venue-back-office.yaml#BO-666 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Same record written by BO-666, BO-669 and BO-673** Why: Per VO-R14 one editor, one Save; the board entries become anchors. *(source: DI-671 / DI-987; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **With onExpiry autoRenew and renewalRequiresReverification true, does access continue while the renewal is under review?** → Drawn default accepted: Draw auto-renew as "opens a renewal automatically; access ends at expiry unless approved in time". *(decided by Chinmay, 2026-10-02; DEC-483 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **programme**: Picked first (validity is per programme); shows the programme's events, venues and application window as context. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationValidity)*
- **validityKind**: Five cards: Event duration (from the first event's start to the last event's end), Fixed period (validity months), Seasonal (season dates), Rolling (months from approval), Permanent. Permanent is disabled with "Needs permanent accreditation rights" for users without them, and shows an amber "Access never expires" when chosen. *(source: screens/P08-venue-back-office.yaml#BO-666 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationValidity)*
- **validityMonths**: Shown only for Fixed period and Rolling; whole months, min 1. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationValidity)*
- **onExpiry / gracePeriodDays**: "When it expires" with Revoke access (default), Grace period (then days, required, min 1) and Auto-renew. Grace days shown as "Access continues 3 days after expiry". *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationValidity)*
- **renewalWindowDays / renewalRequiresReverification**: "Renewal opens [30] days before expiry" and "Renewal needs review and re-verification" (default on). Turning it off shows "Renewals will be approved automatically". *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationValidity)*
- **start and end time**: The pack's start/end date and time per programme are greyed (see corrections); holder dates show on BO-626. *(source: screens/P08-venue-back-office.yaml#BO-666)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Timeline preview**: A horizontal timeline for a sample holder approved today: valid from, renewal window opens, expiry, grace ends, with dates ("Valid 12 Dec 2026 - 20 Dec 2026; renewal from 20 Nov; access ends 20 Dec"). *(source: screens/P08-venue-back-office.yaml#BO-666)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save validity**: Sends the whole record (per VO-R04). Confirm states it applies to new approvals and renewals; existing holders keep their validTo. *(source: contracts/satellite/accreditation.yaml#setAccreditationValidity)*

**Where the user goes next**

- → `BO-664` Accreditation Lifecycle Command Center: *Back to Accreditation Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validity period list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validity period untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validity period yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validity period are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Auto-renew chosen with re-verification on**: Explain the contradiction ("Auto-renew opens a renewal that still needs review"); auto-renew opens a renewal automatically, and access ends at expiry unless it is approved in time. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationValidity / contracts/satellite/accreditation.yaml#renewAccreditation / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **Event duration with no events on the programme**: Block save with "Add events to the programme first (BO-667)". *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*

#### Consistency with other screens

- Match `BO-669`: Same record; Temporary and Seasonal are presets of this editor.
- Match `BO-672`: Expiry behaviour shown on the expiry monitor reads from here.
- Match `BO-673`: Renewal window and re-verification shown in the renewal workspace read from here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programme: Summit Peaks Winter Festival 2026 - Media
validity:
  kind: Event duration
  onExpiry: Revoke access
  renewalWindowDays: 30
  reverification: 'On'
contractor:
  kind: Rolling
  validityMonths: 6
  onExpiry: Grace period
  graceDays: 3
```

#### Permissions

- `setAccreditationValidity` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.6 | Expiration Management System shall support temporary and permanent accreditation validity periods. | Accreditation & Credential Management | CONTRACTED | `setAccreditationValidity` |
| 12.1.41 | Temporary Event Accreditation - System shall support temporary event credentials. | Accreditation & Credential Management | CONTRACTED | `setAccreditationValidity` |
| 12.1.42 | Seasonal Accreditation - System shall support seasonal accreditation programs. | Accreditation & Credential Management | CONTRACTED | `setAccreditationValidity` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-666` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-666`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 4: Works in Validity Period Configuration → Configure how long an accreditation remains valid.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-666?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-664`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-667` Event & Venue Accreditation Assignment

**Determine the event and venue scope of an accreditation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `programmeId` (navigation) |
| Route | `/access-venue/event-venue-accreditation-assignment-bo-667` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): Assigning scope edits an existing programme (the screen opens with a programmeId); it needs the programme read and updateAccreditationProgramme, not a create …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Ties a programme to its events and venues: event-specific, venue-specific or event plus venue. It is how a Media accreditation for the Winter Festival stops working at Aqua Park. The one thing to get right: the scope is the programme's events and venues, chosen once, checked against existing access assignments before it is changed, and cloning last season's programme is the normal way to start.

**Known correction pending (do not draw the wrong version)**

- **The create overlay lists id, status and scopePath as fields** Why: Server-owned (VO-R03). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Bound to createAccreditationProgramme only, with a "Create" button, while the screen opens with a programmeId (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Is template | toggle | — | — | `listAccreditationProgrammes` ?isTemplate |

**Form: Save scope** (modal, opened by *Save scope*; *Save scope* calls `updateAccreditationProgramme`, *Cancel* sends nothing)

**Collects what `updateAccreditationProgramme` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `updateAccreditationProgramme` body |
| Code `code` | text field | required | — | — | — | — | `updateAccreditationProgramme` body |
| Name `name` | text field | required | — | — | — | — | `updateAccreditationProgramme` body |
| Venues `venueIds` | multi-picker: choose venues | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Events `eventIds` | multi-picker: choose events | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Categories `categories` | repeatable rows | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Code `categories[].code` | text field | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Name `categories[].name` | text field | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Default access profile `categories[].defaultAccessProfileId` | picker: choose a default access profile | optional | — | — | shows names, sends the id | — | `updateAccreditationProgramme` body |
| Quota `categories[].quota` | number field | optional | — | — | — | A cap on how many may be accredited in this category. Without one, a category is a promise nobody counted. | `updateAccreditationProgramme` body |
| Badge template `categories[].badgeTemplateId` | picker: choose a badge template | optional | — | — | shows names, sends the id | The badge printed for this category; travels with the category when a programme is cloned | `updateAccreditationProgramme` body |
| Applicant types `applicantTypes` | list of values (chips) | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Applications open at `applicationsOpenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccreditationProgramme` body |
| Applications close at `applicationsCloseAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccreditationProgramme` body |
| Approval workflow `approvalWorkflowId` | picker: choose an approval workflow | optional | — | — | shows names, sends the id | — | `updateAccreditationProgramme` body |
| Form `formId` | picker: choose a form | optional | — | — | shows names, sends the id | 12.1.2. The `marketing-crm` form definition (`createForm`, BO-618) the applicant fills in. | `updateAccreditationProgramme` body |
| Is template `isTemplate` | toggle | optional | off | — | — | 12.1.56. A reusable programme template: never opened for applications, and what `cloneAccreditationProgramme` copies its categories, requirements, validity, notification rules and … | `updateAccreditationProgramme` body |
| Status `status` | radio group | optional | — | Draft · Open · Closed · Archived | — | — | `updateAccreditationProgramme` body |
| Face matching `faceMatching` | group | optional | — | Face matching for duplicate applicants: only where the venue enables it, with each applicant's consent and the venue's legal sign-off; off by default (Chinmay, 2 October, workbook Q461; ADR-0063 …; Enabling needs `legalSignOffRef` (the venue's legal sign-off … | — | Face matching for duplicate applicants: only where the venue enables it, with each applicant's consent and the venue's legal sign-off; off by default (Chinmay, 2 October, workbook … | `updateAccreditationProgramme` body |
| Enabled `faceMatching.enabled` | toggle | optional | off | — | — | — | `updateAccreditationProgramme` body |
| Legal sign off ref `faceMatching.legalSignOffRef` | text field | optional | — | — | — | The venue's legal sign-off document (a stored file reference). | `updateAccreditationProgramme` body |
| Identity verification `identityVerification` | group | optional | — | — | — | UAE Pass and ICP verification, in release 1 (Chinmay, 2 October, workbook Q457; CHG-CSA-031). | `updateAccreditationProgramme` body |
| Methods `identityVerification.methods` | multi-select chips | optional | — | Uae pass · Icp · Manual review | — | — | `updateAccreditationProgramme` body |
| Required `identityVerification.required` | toggle | optional | off | — | — | Whether an application is blocked from approval until a listed check passes. | `updateAccreditationProgramme` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `updateAccreditationProgramme` body |

Errors to draw in the form: 409 A template cannot be opened for applications

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **scope type**: Three cards from the pack: Event-specific (events chosen, venues follow from the events), Venue-specific (venues chosen, no events), Event + Venue (both). The choice decides which pickers show. *(source: screens/P08-venue-back-office.yaml#BO-667)*
- **eventIds / venueIds**: Event picker lists the venue's catalogue events with dates; venue picker defaults to the top-bar venue and lists only venues in the user's scope. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **clone from**: "Start from" a template or last season's programme, with What to copy (Categories, Requirements, Validity, Notification rules, Form; all ticked by default). Never applications, holders or credentials; say so under the list. *(source: contracts/satellite/accreditation.yaml#cloneAccreditationProgramme / MATRIX 12.1.56)*
- **validity period / applicable credential / access profile**: Shown as read-only summaries with links (validity editor, credential media BO-646, category default profiles), not re-entered here. *(source: screens/P08-venue-back-office.yaml#BO-667)*

#### Outputs: what the screen shows and produces

**Shown**

**Programme** (data table, from `listAccreditationProgrammes`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venues | list or chips (count when long) | — |
| Events | list or chips (count when long) | — |
| Categories | list or chips (count when long) | — |
| Code | text | — |
| Name | text | — |
| Default access profile | the name it points at, never the id | — |
| Quota | 1,234 | A cap on how many may be accredited in this category. Without one, a category is a promise nobody counted. |
| Badge template | the name it points at, never the id | The badge printed for this category; travels with the category when a programme is cloned |
| Applicant types | list or chips (count when long) | — |
| Applications open at | 1 Oct 2026, 14:30 | — |
| Applications close at | 1 Oct 2026, 14:30 | — |
| Approval workflow | the name it points at, never the id | — |
| Form | the name it points at, never the id | 12.1.2. The `marketing-crm` form definition (`createForm`, BO-618) the applicant fills in. |
| Is template | yes / no (icon or chip) | 12.1.56. A reusable programme template: never opened for applications, and what `cloneAccreditationProgramme` copies its categories … |
| Template programme | the name it points at, never the id | The programme or template this one was cloned from |
| Status | chip: Draft, Open, Closed, Archived | — |
| Face matching | grouped details | Face matching for duplicate applicants: only where the venue enables it, with each applicant's consent and the venue's legal sign-off; off … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save scope (secondary button) | `updateAccreditationProgramme` PUT `/accreditation-programmes/{programmeId}` | AccreditationProgramme | AccreditationProgramme | 409 A template cannot be opened for applications | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scope summary**: A sentence: "Valid for Summit Peaks Winter Festival 2026 (12-20 Dec) at Summit Peaks only." *(source: screens/P08-venue-back-office.yaml#BO-667)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save scope**: Updates the programme's events and venues. If a venue is removed, first list holders and access profiles that reference it ("64 holders have access at Aqua Park through Contractor - Operational Areas"). *(source: screens/P08-venue-back-office.yaml#BO-667 / contracts/satellite/accreditation.yaml#updateAccreditationProgramme)*
- **Clone programme**: Creates a new programme (or template) with the chosen parts and opens it; status Draft. *(source: contracts/satellite/accreditation.yaml#cloneAccreditationProgramme)*

**Data it reads**: `listAccreditationProgrammes` (onLoad, The programme and its event and venue scope)

**Where the user goes next**

- → `BO-664` Accreditation Lifecycle Command Center: *Back to Accreditation Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event venue accreditation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event venue accreditation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event venue accreditation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event venue accreditation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A programme with this code already exists at this scope; 409 A template cannot be opened for applications |

#### Edge cases to draw

- **Event cancelled or moved after holders were approved**: Show an alert on the programme with the count of holders whose validity follows that event. *(source: screens/P08-venue-back-office.yaml#BO-667)*
- **Programme is a template**: Scope is optional for a template and the screen says templates never open for applications. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*

#### Consistency with other screens

- Match `BO-620`: Programme setup on Board 1 creates the same record; this screen edits only its scope. Same programme header.
- Match `BO-668`: Multi-venue is the Venue-specific or Event + Venue case with more than one venue.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programme:
  name: Summit Peaks Winter Festival 2026 - Media
  code: SPWF26-MEDIA
  scope: Event + Venue
  events:
  - Winter Festival Opening Night, 12 Dec 2026
  - Winter Festival Finale, 20 Dec 2026
  venues:
  - Summit Peaks
clonedFrom: Summit Peaks Winter Festival 2025 - Media
```

#### Permissions

- `cloneAccreditationProgramme` → `ACCREDITATION_CONFIGURE` (configure) · staff
- `listAccreditationProgrammes` → `ACCREDITATION_VIEW` (read) · staff
- `updateAccreditationProgramme` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.56 | Accreditation Templates - System shall support reusable accreditation templates. | Accreditation & Credential Management | CONTRACTED | `cloneAccreditationProgramme` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-667` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-667`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 6: Works in Event & Venue Accreditation Assignment → Determine the event and venue scope of an accreditation.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-667?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save scope.
- [ ] Every transition is wired: `BO-664`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-668` Multi-Venue Accreditation Management

**Allow one accreditation to operate across multiple approved venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/multi-venue-accreditation-management-bo-668` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** One accreditation valid at several venues (Regional Operations Staff at Summit Peaks, Aqua Park and the Fan Zone), each venue with its own dates, profile, zones, credential and status. The one thing to get right: the pack shows this per holder and per venue (Fan Zone Restricted while the others are Active), and removing a venue must visibly take that venue's access away from the gates.

**Known correction pending (do not draw the wrong version)**

- **Per-venue validity dates and per-venue status cannot be stored** Why: AccessProfile.venueIds and AccreditationProgramme.venueIds are plain lists; the holder has one validFrom/validTo. The pack's table needs per-venue rows on the holder. *(source: screens/P08-venue-back-office.yaml#BO-667 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Write bound with no read; primaryButton "Save access profile" (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is multi-venue set per accreditation holder (the pack's table) or only per profile and programme (the contract)?** → Drawn default accepted: Draw the per-holder table read-only from profile venues, with per-venue dates greyed. *(decided by Chinmay, 2026-10-02; DEC-484 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **venues**: Multi-select limited to venues in the user's scope; a venue the user cannot see in another tenant region is never listed. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*
- **per-venue profile**: For each venue, Common profile (one profile covering all venues) or Venue-specific profile (a picker per venue), as the pack allows. *(source: screens/P08-venue-back-office.yaml#BO-669)*

#### Outputs: what the screen shows and produces

**Shown**

**Access profiles** (data table, from `listAccessProfiles`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Zones | list or chips (count when long) | — |
| Venues | list or chips (count when long) | — |
| Operational areas | list or chips (count when long) | — |
| Schedule | list or chips (count when long) | Zone, date and time are three dimensions and all three are needed. |
| Zone | the name it points at, never the id | — |
| Days of week | list or chips (count when long) | — |
| Date from | 1 Oct 2026 | — |
| Date to | 1 Oct 2026 | — |
| From | text | — |
| To | text | — |
| Event phase | chip: Build, Rehearsal, Doors open, Live show, Breakdown | — |
| Escort required | yes / no (icon or chip) | — |
| Holder count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save access profile (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Venue table**: Columns Venue, Valid from/to, Access profile, Permitted zones (count with hover list), Credential, Current status (Active / Restricted / Suspended), one row per venue. *(source: screens/P08-venue-back-office.yaml#BO-667 / screens/P08-venue-back-office.yaml#BO-669)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Remove venue**: Confirmation per VO-R16 naming holders and zones losing access; then impact preview and save; gates at that venue stop admitting. *(source: screens/P08-venue-back-office.yaml#BO-669 / contracts/satellite/accreditation.yaml#previewAccessImpact)*
- **Save**: Saves the profile(s) in full (VO-R04). *(source: contracts/satellite/accreditation.yaml#setAccessProfile)*

**Data it reads**: `listAccessProfiles` (onLoad, Profiles and the venues they cover)

**Where the user goes next**

- → `BO-664` Accreditation Lifecycle Command Center: *Back to Accreditation Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-venue accreditation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-venue accreditation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-venue accreditation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-venue accreditation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **User scoped to one venue opens a multi-venue profile**: Other venues' rows are read-only with "Managed by Aqua Park team"; the user can change only their venue's row. *(source: ADR-0018)*

#### Consistency with other screens

- Match `BO-655`: Venues tab of the same profile editor.
- Match `BO-667`: Programme venues bound the venues available here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holder: Regional Operations Staff - Maria Santos
venues:
- venue: Summit Peaks
  valid: 1 Oct 2026 - 30 Sep 2027
  profile: Staff - Full Venue
  zones: 12
  credential: RFID card RF-77C1
  status: Active
- venue: Aqua Park
  valid: 1 Oct 2026 - 30 Sep 2027
  profile: Staff - Full Venue
  zones: 9
  credential: RFID card RF-77C1
  status: Active
- venue: Fan Zone
  valid: 12 Dec 2026 - 20 Dec 2026
  profile: Staff - Public Areas
  zones: 2
  credential: RFID card RF-77C1
  status: Restricted
```

#### Permissions

- `setAccessProfile` → `ACCREDITATION_CONFIGURE` (configure) · staff
- `listAccessProfiles` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.25 | Zone-Based Access - System shall assign access rights by venue zone. | Accreditation & Credential Management | CONTRACTED | `setAccessProfile` |
| 12.1.26 | Area-Based Permissions - System shall assign permissions for specific operational areas. | Accreditation & Credential Management | CONTRACTED | `setAccessProfile` |
| 12.1.27 | Time-Based Access Rights - System shall support time-based accreditation permissions. | Accreditation & Credential Management | CONTRACTED | `setAccessProfile` |
| 12.1.28 | Date-Based Access Rights - System shall support date-based accreditation permissions. | Accreditation & Credential Management | CONTRACTED | `setAccessProfile` |
| 12.1.29 | Access Schedule Management - System shall support configurable access schedules. | Accreditation & Credential Management | CONTRACTED | `setAccessProfile` |
| 12.1.40 | Multi-Venue Accreditation - System shall support accreditations valid across multiple venues. | Accreditation & Credential Management | CONTRACTED | `setAccessProfile` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-668` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-668`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 8: Works in Multi-Venue Accreditation Management → Allow one accreditation to operate across multiple approved venues.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-668?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save access profile, Cancel.
- [ ] Every transition is wired: `BO-664`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-669` Temporary & Seasonal Accreditation

**Manage short-duration and recurring accreditation programs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/temporary-seasonal-accreditation-bo-669` |

**What the spec says about it.** **Merged into BO-666** (decided 2 October 2026, Chinmay: fix the wrong wiring now; CHG-WIR-001). BO-669 binds the same single operation (setAccreditationValidity) on the same record as BO-666 Validity Period Configuration; temporary and seasonal periods are presets inside the validity editor (VO-R14; DI-671, DI-987; design-notes correction venue-operations BO-669). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-666, and nothing on it is built separately. Dates follow from the validity kind and the programme; events and venues are the programme's scope (BO-667); access profiles are category defaults (design-note correction).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Presets for short and recurring accreditations: one-day events, contractors, media visits (temporary) and sports or exhibition seasons, annual operations (seasonal). Per VO-R14 it is the preset picker at the top of the validity editor (BO-666), not a separate record. The one thing to get right: temporary accreditations expire on their own, with no manual step, and the screen says when.

**Fixed on main** (the package already carries these; draw what it says): Select fields "Start/end date", "Events", "Venues", "Access profile" are drawn as inputs (CHG-SBO-016); Duplicate of BO-666 (same operation, same record) (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Accreditation type | select field | — | — | — | — | — | — |
| Automatic expiry | select field | — | — | — | — | — | — |
| Renewal eligibility | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **accreditation type**: Temporary (event duration or a fixed number of days) or Seasonal (season dates or a fixed number of months), each with the pack's examples as preset tiles (One-day event, Contractor, Media visit, Sports season, Annual venue operations). *(source: screens/P08-venue-back-office.yaml#BO-669 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationValidity)*
- **automatic expiry**: Always on for Temporary and shown locked with "Expires automatically"; for Seasonal it follows onExpiry. *(source: screens/P08-venue-back-office.yaml#BO-669)*
- **renewal eligibility**: Maps to renewal window days (empty = not renewable; "Temporary accreditations are not renewable" as the default for one-day events). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationValidity)*
- **events / venues / access profile**: Read-only summaries with links to BO-667 and the category defaults; not re-entered here. *(source: screens/P08-venue-back-office.yaml#BO-669)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Expiry statement**: "Holders in this programme lose access automatically at 23:59 on 20 Dec 2026" under the form. *(source: screens/P08-venue-back-office.yaml#BO-669)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Whole-record save of the programme's validity (VO-R04). *(source: contracts/satellite/accreditation.yaml#setAccreditationValidity)*

**Where the user goes next**

- → `BO-664` Accreditation Lifecycle Command Center: *Back to Accreditation Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The temporary seasonal accreditation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the temporary seasonal accreditation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No temporary seasonal accreditation configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Seasonal accreditation spanning a season break**: The validity is continuous; access during the break is controlled by profile schedules, say so with a link to BO-659. *(source: screens/P08-venue-back-office.yaml#BO-669)*

#### Consistency with other screens

- Match `BO-666`: Same record and editor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
presets:
- type: Temporary
  preset: Media visit
  kind: Event duration
  renewable: 'No'
- type: Temporary
  preset: Contractor
  kind: Fixed period
  months: 1
  renewable: Yes, 7 days before
- type: Seasonal
  preset: Annual venue operations
  kind: Seasonal
  renewable: Yes, 30 days before
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-669` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-669`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 10: Works in Temporary & Seasonal Accreditation → Manage short-duration and recurring accreditation programs.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-669?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-664`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-670` Suspension & Reactivation Management

**Temporarily disable accreditation without permanently terminating it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§The operator shall specify) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/suspension-reactivation-management-bo-670` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Suspending an accreditation for a reason (compliance review, security investigation, missing or expired document) and bringing it back later. Suspension keeps the record, stops the credential and disables access, and has an expected end. The one thing to get right: the reason is from a closed list, the impact on credential and access is stated before confirm, and reactivation is an explicit act after the conditions are met.

**Known correction pending (do not draw the wrong version)**

- **"Credential → Suspended" (select field) and "Access Rights → Disabled" (text field) are drawn as inputs** Why: They are the pack's impact statement, read-only outputs. *(source: screens/P08-venue-back-office.yaml#BO-670; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Select field "Key requirement 12.1.34"** Why: Pack prose turned into a field; remove. *(source: screens/P08-venue-back-office.yaml#BO-670; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Supporting evidence and approver have no field; reason is free text with no reason code** Why: The pack lists them; reporting on suspension reasons (BO-689) needs a code, not prose. *(source: screens/P08-venue-back-office.yaml#BO-670 / contracts/satellite/accreditation.yaml#setAccreditationStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The "Reactivated" notification trigger does not exist** Why: AccreditationNotificationRules events have suspended and revoked but no reactivated, which the pack and DI-663 expect. *(source: screens/P08-venue-back-office.yaml#BO-676 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationNotificationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Suspension reason | select field | — | — | — | — | — | — |
| Effective date/time | select field | — | — | — | — | — | — |
| Expected end date where applicable | text field | — | — | — | — | — | — |
| Notes | select field | — | — | — | — | — | — |
| Supporting evidence | select field | — | — | — | — | — | — |
| Approver where required | select field | — | — | — | — | — | — |
| Credential → Suspended | select field | — | — | — | — | — | — |
| Access Rights → Disabled | text field | — | — | — | — | — | — |
| Key requirement: 12.1.34 | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **suspension reason**: Select from the pack's list: Compliance review, Security investigation, Employment status, Contractor issue, Missing/expired document, Temporary restriction, Operational decision; plus Other with required text. Sent as the reason string. *(source: screens/P08-venue-back-office.yaml#BO-670 / contracts/satellite/accreditation.yaml#setAccreditationStatus)*
- **effective date/time**: Now (default) or a future date-time in venue time; never in the past. *(source: contracts/satellite/accreditation.yaml#setAccreditationStatus)*
- **expected end date**: Optional date, stored as reviewAt; labelled "Review on" because the suspension does not lift by itself. *(source: screens/P08-venue-back-office.yaml#BO-670 / contracts/satellite/accreditation.yaml#setAccreditationStatus)*
- **notes / supporting evidence / approver**: Notes free text; evidence as file attachments; approver where configured. Evidence and approver have no field (see corrections) and are drawn greyed. *(source: screens/P08-venue-back-office.yaml#BO-670)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Impact statement**: Two lines, as the pack: "Credential: 2 credentials suspended" and "Access rights: disabled at 5 zones"; read-only, not inputs. *(source: screens/P08-venue-back-office.yaml#BO-670 / screens/P08-venue-back-office.yaml#BO-673)*
- **Suspended list**: Holder, reason, since, review on (red when past), suspended by; the reactivation queue. *(source: contracts/satellite/accreditation.yaml#listAccreditationHolders)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Suspend**: Confirmation per VO-R16; holder becomes Suspended, credentials stop at the gates, holder and organisation notified per BO-675. *(source: contracts/satellite/accreditation.yaml#setAccreditationStatus / DI-663)*
- **Reactivate**: Sets status active with a reason. If the suspension reason was Missing/expired document, Reactivate is disabled until the document is re-verified ("Emirates ID awaiting verification"). *(source: screens/P08-venue-back-office.yaml#BO-670 / DI-663 / contracts/satellite/accreditation.yaml#setAccreditationStatus)*

**Where the user goes next**

- → `BO-664` Accreditation Lifecycle Command Center: *Back to Accreditation Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The suspension reactivation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the suspension reactivation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No suspension reactivation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Accreditation expires while suspended**: It becomes Expired; Reactivate is replaced by Renew, and renewal is refused while suspended (409), so say "Reactivate before renewing". *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*
- **Document expiry raises an automatic suspension**: Reason shows Missing/expired document with "Raised automatically" as the actor. *(source: DI-663)*

#### Consistency with other screens

- Match `BO-662`: Same dialog and reason list.
- Match `BO-675`: Suspended and Reactivated notifications use these reasons in the message.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
suspended:
- holder: James Carter
  reason: Security investigation
  since: 13 Dec 2026 10:42
  reviewOn: 16 Dec 2026
  by: Ahmed Al Mansoori
- holder: Priya Nair
  reason: Missing/expired document
  since: 10 Dec 2026 01:00
  reviewOn: ''
  by: System
```

#### Permissions

- `setAccreditationStatus` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.30 | Access Revocation - System shall support immediate revocation of accreditation access rights. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |
| 12.1.32 | Accreditation Status Workflow - System shall support accreditation lifecycle statuses. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |
| 12.1.34 | Accreditation Suspension - System shall support temporary suspension of accreditations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |
| 12.1.35 | Accreditation Revocation - System shall support permanent revocation of accreditations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-670` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-670`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 12: Works in Suspension & Reactivation Management → Temporarily disable accreditation without permanently terminating it.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-670?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-664`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-671` Accreditation Revocation Management

**Permanently terminate an accreditation.**

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
| Route | `/access-venue/accreditation-revocation-management-bo-671` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Permanent termination of an accreditation for security violation, misuse, termination, fraud or credential sharing. The record and its history stay; every credential stops at once and access is blocked without deactivating anything by hand. The one thing to get right: the impact is shown and confirmed before execution, and the screen makes clear there is no way back (a revoked holder applies afresh).

**Known correction pending (do not draw the wrong version)**

- **primaryButton "Save accreditation status"** Why: A permanent destructive act is labelled by what it does, "Revoke accreditation". *(source: screens/P08-venue-back-office.yaml#BO-671; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Reason is free text in the contract** Why: The pack gives a closed list; a reason code is needed for audit reporting. *(source: screens/P08-venue-back-office.yaml#BO-672 / contracts/satellite/accreditation.yaml#setAccreditationStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **revocation reason**: Select from the pack's list: Security violation, Accreditation misuse, Employment termination, Contractor termination, Fraud, Credential sharing, Policy breach, Management decision, Other (text required). *(source: screens/P08-venue-back-office.yaml#BO-670 / screens/P08-venue-back-office.yaml#BO-672)*
- **effective from**: Now by default; a future time allowed only with a reason (e.g. end of contract at 18:00). *(source: contracts/satellite/accreditation.yaml#setAccreditationStatus)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save accreditation status (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Impact panel**: Three lines from the pack: "Accreditation: Revoked", "Credential: 2 revoked (BDG-001877-1, RF-31A0)", "Access rights: removed and blocked". *(source: screens/P08-venue-back-office.yaml#BO-672)*
- **Revoked history**: Revoked holders stay listed (status Revoked, reason, by, when) and remain reportable; never deleted. *(source: screens/P08-venue-back-office.yaml#BO-672 / screens/P08-venue-back-office.yaml#BO-673)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Revoke accreditation**: Red confirm per VO-R16 with the holder's name typed to confirm; status revoked; credentials invalidated and pushed to gates in the same act; offline devices at next package refresh (VO-R07). *(source: contracts/satellite/accreditation.yaml#setAccreditationStatus)*

**Where the user goes next**

- → `BO-664` Accreditation Lifecycle Command Center: *Back to Accreditation Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation revocation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation revocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation revocation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation revocation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Holder has an open renewal application**: The confirm says the renewal will be closed as well. *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*
- **Revoke from a holder's organisation account (P11)**: Not offered; an organisation can withdraw an application but only staff revoke. *(source: contracts/satellite/accreditation.yaml#setAccreditationStatus)*

#### Consistency with other screens

- Match `BO-662`: Same dialog and wording.
- Match `BO-687`: Later scan attempts with the revoked credential appear as denied "Accreditation revoked" in access activity.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holder:
  name: James Carter
  accreditationNumber: ACC-2026-001877
  organisation: Al Noor Contracting
reason: Credential sharing
credentials:
- BDG-001877-1
- RF-31A0
```

#### Permissions

- `setAccreditationStatus` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.30 | Access Revocation - System shall support immediate revocation of accreditation access rights. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |
| 12.1.32 | Accreditation Status Workflow - System shall support accreditation lifecycle statuses. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |
| 12.1.34 | Accreditation Suspension - System shall support temporary suspension of accreditations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |
| 12.1.35 | Accreditation Revocation - System shall support permanent revocation of accreditations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationStatus` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-671` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-671`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 14: Works in Accreditation Revocation Management → Permanently terminate an accreditation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-671?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save accreditation status, Cancel.
- [ ] Every transition is wired: `BO-664`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-672` Expiry Monitor & Expiration Rules

**Proactively manage accreditations approaching expiry.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_APPLY`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/expiry-monitor-expiration-rules-bo-672` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The expiry watch list: accreditations expiring today, within 7 and 30 days, expired today and recently, with renewal available or already started, plus documents (Emirates ID, passport) that expire before the event. Used weekly by the accreditation team and daily in event week. The one thing to get right: per DI-663 a document expiring before the event is its own bucket that leads to a resubmission request, not just a date in a column.

**Known correction pending (do not draw the wrong version)**

- **The pack's expiration rules (automatic status change, credential deactivation, access termination, grace, renewal eligibility, notification trigger) are configured here but no write is bound** Why: setAccreditationValidity is bound on BO-673 instead; the rules belong to the validity editor (BO-666) and this screen should show them read-only with a link. *(source: screens/P08-venue-back-office.yaml#BO-672 / screens/P08-venue-back-office.yaml#BO-673; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Buckets Expired today, Recently expired and Renewal started have no query** Why: listAccreditationHolders filters by status and expiringWithinDays only, with no validTo range and no open-renewal flag. *(source: contracts/satellite/accreditation.yaml#listAccreditationHolders; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Data table and primary button have empty labels** Why: Generated placeholders; the table is "Expiring accreditations" and the action "Start renewal". *(source: screens/P08-venue-back-office.yaml#BO-672; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): listAccreditationDocuments (expiringWithinDays) is not bound (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationHolders` ?programmeId |
| Organisation | picker: choose an organisation | — | — | `listAccreditationHolders` ?organisationId |
| Status | text field | — | — | `listAccreditationHolders` ?status |
| Expiring within days | number field (days) | — | — | `listAccreditationHolders` ?expiringWithinDays |
| Application | picker: choose an application | — | — | `listAccreditationDocuments` ?applicationId |
| Holder | picker: choose a holder | — | — | `listAccreditationDocuments` ?holderId |
| Requirement code | text field | — | — | `listAccreditationDocuments` ?requirementCode |
| Status | radio group | — | Submitted · Verified · Rejected · Expired | `listAccreditationDocuments` ?status |
| Expiring within days | number field (days) | — | min 0 | `listAccreditationDocuments` ?expiringWithinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **bucket**: Tabs with counts: Expiring today, Within 7 days, Within 30 days, Expired today, Recently expired (30 days), Renewal available, Renewal started, Documents expiring before event. *(source: screens/P08-venue-back-office.yaml#BO-672 / DI-663)*
- **filters**: Programme, organisation, category; venue from the top bar. *(source: contracts/satellite/accreditation.yaml#listAccreditationHolders)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Expiring documents** (data table, from `listAccreditationDocuments`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Holder | the name it points at, never the id | — |
| Application | the name it points at, never the id | — |
| Requirement code | text | — |
| Asset | the image or video | — |
| Submitted at | 1 Oct 2026, 14:30 | — |
| Status | chip: Submitted, Verified, Rejected, Expired | — |
| Verified by | the name it points at, never the id | — |
| Verified at | 1 Oct 2026, 14:30 | — |
| Rejection reason | text | — |
| Expires at | 1 Oct 2026 | An insurance certificate valid until March accredits somebody until March, whatever the programme says. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Holder rows**: Photo, name, organisation, category, valid to (with "in 5 days" relative), renewal state, and for the document bucket the document type and its expiry. Sorted by validTo ascending. *(source: contracts/satellite/accreditation.yaml#listAccreditationHolders / contracts/satellite/accreditation.yaml#listAccreditationDocuments)*
- **Expiry behaviour**: A read-only strip from the programme's validity: "At expiry: access revoked; grace 0 days; renewal opens 30 days before" with a link to edit (BO-666). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationValidity)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start renewal**: Opens a renewal for the holder (staff-initiated); with re-verification it is Submitted for review, without it is approved and validTo extends at once. 409 shows "Outside the renewal window" or "A renewal is already open". *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*
- **Request resubmission (document bucket)**: Asks the holder to upload a new document; the credential is blocked if unresolved by the event. *(source: DI-663)*
- **Bulk remind**: Opens BO-679 with the selected holders as recipients. *(source: screens/P08-venue-back-office.yaml#BO-680)*

**Data it reads**: `listAccreditationHolders` (onLoad, Expiring soon); `listAccreditationDocuments` (onLoad, Documents expiring before the event)

**Where the user goes next**

- → `BO-664` Accreditation Lifecycle Command Center: *Back to Accreditation Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The expiry expiration rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the expiry expiration rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No expiry expiration rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the expiry expiration rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Outside the renewal window, the holder is revoked, suspended or archived, or a renewal is already open |

#### Edge cases to draw

- **Holder suspended**: Start renewal disabled with "Reactivate before renewing". *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*
- **Holder revoked**: Not in renewal buckets; a revoked holder applies afresh. *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*

#### Consistency with other screens

- Match `BO-676`: Reminders scheduled there are shown here as "Reminder 2 sent 4 Dec" on each row.
- Match `BO-630`: Resubmitted documents land in the document verification queue.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
buckets:
  today: 3
  within7: 18
  within30: 61
  expiredToday: 2
  recentlyExpired: 47
  renewalAvailable: 88
  renewalStarted: 17
  documentsBeforeEvent: 12
rows:
- holder: Sara Al Nuaimi
  organisation: Gulf Media Network
  category: Media
  validTo: 18 Dec 2026
  renewal: Available
- holder: Khalid Al Zaabi
  organisation: Gulf Media Network
  category: Media
  document: Emirates ID
  documentExpires: 10 Dec 2026
  event: 12 Dec 2026
```

#### Permissions

- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `renewAccreditation` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `listAccreditationDocuments` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.37 | Accreditation Renewal - System shall support accreditation renewal workflows. | Accreditation & Credential Management | CONTRACTED | `renewAccreditation` |
| 12.1.18 | Document Management - System shall support storage of accreditation-related documents. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |
| 12.1.19 | Identity Verification - System shall support identity verification before accreditation approval. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-672` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-672`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 16: Works in Expiry Monitor & Expiration Rules → Proactively manage accreditations approaching expiry.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-672?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-664`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-673` Accreditation Renewal Workspace

**Manage accreditation renewal without unnecessarily recreating the holder or application.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_APPLY`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/accreditation-renewal-workspace-bo-673` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): setAccreditationValidity is programme-level rule configuration; the screen renews one holder, and the validity rules belong in BO-666 (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Renewing one holder without recreating them: a side-by-side of the current period and the proposed one (category, organisation, event/venue, validity, credential, access, documents, identity verification), with what the renewal rules require. The one thing to get right: renewal keeps the same holder and credential, opens a renewal application that is reviewed like any other where re-verification is on, and the relationship between periods is visible.

**Known correction pending (do not draw the wrong version)**

- **The pack's "Issue New Credential" contradicts the contract, where renewal keeps the same credentials** Why: renewAccreditation says credentials stay the same and wallet passes are re-pushed; a new credential is only issued through replacement. *(source: screens/P08-venue-back-office.yaml#BO-673 / contracts/satellite/accreditation.yaml#renewAccreditation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Renewal cannot change event/venue or access profile** Why: The request takes categoryCode and changed answers only, while the pack compares New Event/Venue and Proposed Access. *(source: screens/P08-venue-back-office.yaml#BO-673 / contracts/satellite/accreditation.yaml#renewAccreditation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): setAccreditationValidity (programme-level rule configuration) is bound to a per-holder renewal workspace (CHG-WIR-001); primaryButton "Save" (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **On renewal, should a new physical badge be printed (new validity printed on the card) or does the existing badge carry over?** → Drawn default accepted: Keep the credential; show "Reprint badge with new dates" as an optional follow-up link to BO-648. *(decided by Chinmay, 2026-10-02; DEC-485 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

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

- **proposed category**: A select of the programme's categories, defaulting to the current one; changing it shows the new default access profile in the Access row. *(source: screens/P08-venue-back-office.yaml#BO-673 / contracts/satellite/accreditation.yaml#renewAccreditation)*
- **changed answers**: Only fields that changed since the last period (job title, contact) are editable, pre-filled from the holder. *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Comparison table**: Two columns Current and Renewal for the pack's nine rows: Category, Organisation, Event/Venue, Validity, Credential, Access profile, Documents (Current / Expired, red when expired), Identity verification (Valid / Reverification required). Changed rows highlighted. *(source: screens/P08-venue-back-office.yaml#BO-673)*
- **Requirements checklist**: Updated photograph, New documents, Identity reverification, Organisation confirmation, Manager approval, Security approval, Access-right review, each ticked or outstanding. *(source: screens/P08-venue-back-office.yaml#BO-673)*
- **Renewal chain**: A small timeline of the holder's periods (2025 - 2026 - 2027 renewal) linking to each renewal application. *(source: screens/P08-venue-back-office.yaml#BO-673 / contracts/satellite/accreditation.yaml#renewAccreditation)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start renewal**: Opens the renewal application; with re-verification it goes to review (BO-636), without it validTo extends at once and the screen says "Renewed to 20 Dec 2027". *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*
- **Request updates**: Asks the holder (and organisation) for a new photo or documents through the notification engine. *(source: screens/P08-venue-back-office.yaml#BO-673 / DI-663)*
- **Approve renewal**: Not here; approval happens in the application review workspace like any application. Show a link. *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*

**Data it reads**: `listAccreditationHolders` (onLoad, Holders inside the renewal window (expiringWithinDays))

**Where the user goes next**

- → `BO-664` Accreditation Lifecycle Command Center: *Back to Accreditation Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation renewal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation renewal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation renewal yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation renewal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Outside the renewal window, the holder is revoked, suspended or archived, or a renewal is already open |

#### Edge cases to draw

- **Outside the renewal window**: Start renewal disabled with "Renewal opens on 20 Nov 2026". *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*
- **Renewal already open**: Show its status and a link instead of a second Start renewal. *(source: contracts/satellite/accreditation.yaml#renewAccreditation)*

#### Consistency with other screens

- Match `BO-672`: Start renewal there opens this workspace.
- Match `ACC-005`: The applicant can renew their own accreditation on P11 with the same comparison wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holder: Sara Al Nuaimi
current:
  category: Media
  organisation: Gulf Media Network
  validity: 1 Jan 2026 - 31 Dec 2026
  credential: Mobile credential MC-5521
  documents: Emirates ID expires 2 Feb 2027
  identity: Valid
renewal:
  category: Media
  validity: 1 Jan 2027 - 31 Dec 2027
  credential: Same credential, new validity
  documents: Emirates ID - reverification required
  identity: Reverification required
```

#### Permissions

- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `renewAccreditation` → `ACCREDITATION_APPLY` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.37 | Accreditation Renewal - System shall support accreditation renewal workflows. | Accreditation & Credential Management | CONTRACTED | `renewAccreditation` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Lifecycle: activation, expiry, renewal, suspension; if a document (e.g. Emirates ID) expires before the event, a resubmission request is raised and the credential is blocked if unresolved. Applicants are notified at each status change (approved, rejected, needs validation). *(client request · MoM 7 Sep 2026, 4.6 / 4.7 Lifecycle & Notifications · DI-663)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-673` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-673`
- Workshop pack: ACCREDITATION.pdf board 6
- Flow F222 *ACCREDITATION board 6: Accreditation Lifecycle Command Center*, step 18: Works in Accreditation Renewal Workspace → Manage accreditation renewal without unnecessarily recreating the holder or application.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-673?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-664`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cloneAccreditationProgramme": {"method":"POST","path":"/accreditation-programmes/{programmeId}/clone","contract":"accreditation","summary":"Start a programme from a template or last season's programme","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationProgramme"},
"listAccessProfiles": {"method":"GET","path":"/accreditation-access-profiles","contract":"accreditation","summary":"Named bundles of zones, dates and times","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccessProfile"},
"listAccreditationDocuments": {"method":"GET","path":"/accreditation-documents","contract":"accreditation","summary":"Documents supplied, by holder, application, requirement or state","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"applicationId","in":"query","required":null},{"name":"holderId","in":"query","required":null},{"name":"requirementCode","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccreditationHolders": {"method":"GET","path":"/accreditation-holders","contract":"accreditation","summary":"Everybody accredited, and what state they are in","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"organisationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"listAccreditationProgrammes": {"method":"GET","path":"/accreditation-programmes","contract":"accreditation","summary":"Programmes, their categories and their applicant types","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"isTemplate","in":"query","required":null}],"requestBody":null,"responds":"AccreditationProgramme"},
"renewAccreditation": {"method":"POST","path":"/accreditation-holders/{holderId}/renew","contract":"accreditation","summary":"Renew a holder's accreditation for another period","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"setAccessProfile": {"method":"PUT","path":"/accreditation-access-profiles","contract":"accreditation","summary":"Define which zones, on which dates, at which times","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessProfile","responds":"AccessProfile"},
"setAccreditationStatus": {"method":"POST","path":"/accreditation-holders/{holderId}/status","contract":"accreditation","summary":"Suspend, reactivate, revoke or expire an accreditation","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"setAccreditationValidity": {"method":"PUT","path":"/accreditation-validity","contract":"accreditation","summary":"Validity periods, renewal windows and expiry behaviour","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationValidity","responds":"AccreditationValidity"},
"updateAccreditationProgramme": {"method":"PUT","path":"/accreditation-programmes/{programmeId}","contract":"accreditation","summary":"Amend a programme, link its registration form, or mark it a template","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationProgramme","responds":"AccreditationProgramme"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessProfile": {"type":"object","x-ticvai-persistence":"accreditation.access_profile","description":"Board 5.2. **How an estate stays governable.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"zoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"operationalAreas":{"type":"array","items":{"type":"string"}},"schedule":{"type":"array","description":"**Zone, date and time are three dimensions and all three are needed.**","items":{"type":"object","properties":{"zoneId":{"type":"string","format":"uuid","nullable":true},"daysOfWeek":{"type":"array","items":{"type":"string"}},"dateFrom":{"type":"string","format":"date","nullable":true},"dateTo":{"type":"string","format":"date","nullable":true},"from":{"type":"string","nullable":true},"to":{"type":"string","nullable":true},"eventPhase":{"type":"string","nullable":true,"enum":["build","rehearsal","doorsOpen","liveShow","breakdown"]}}}},"escortRequired":{"type":"boolean","default":false},"holderCount":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationApplication": {"type":"object","x-ticvai-persistence":"accreditation.application","description":"Board 1.3. **Usually submitted by an organisation on behalf of its people.**","required":["programmeId"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"applicantType":{"type":"string"},"submittedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"subject":{"type":"object","additionalProperties":true,"description":"Name, date of birth, nationality, contact — shaped by the requirements matrix."},"requirementStatus":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"requirementCode":{"type":"string"},"satisfied":{"type":"boolean"},"documentId":{"type":"string","format":"uuid","nullable":true}}}},"status":{"type":"string","enum":["draft","submitted","underReview","informationRequested","approved","rejected","withdrawn","expired"]},"decisionReason":{"type":"string","nullable":true},"missingRequirements":{"type":"array","readOnly":true,"description":"The requirement codes a reviewer returned the application for, or rejected it over — what the applicant must change before resubmitting","items":{"type":"string"}},"decisionDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a decision is due — the approvals request's SLA. **A date, not a queue position**"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"holderId":{"type":"string","format":"uuid","nullable":true},"renewsHolderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.37. Set by `renewAccreditation`; approval extends this holder rather than creating one"},"resubmissionOfApplicationId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.33. The rejected application this one resubmits, so the rejection stays in the record"},"resubmissionNote":{"type":"string","maxLength":1000,"nullable":true,"readOnly":true,"description":"What the applicant changed, from `resubmitAccreditationApplication`"},"submittedAt":{"type":"string","format":"date-time","nullable":true},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"AccreditationDocument": {"type":"object","x-ticvai-persistence":"accreditation.document","description":"Board 2.5. **Submitted against a named requirement, not into a folder.**","required":["requirementCode","assetId"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid","nullable":true},"applicationId":{"type":"string","format":"uuid","nullable":true},"requirementCode":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"submittedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["submitted","verified","rejected","expired"]},"verifiedBy":{"type":"string","format":"uuid","nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**An insurance certificate valid until March accredits somebody until March**, whatever the programme says.\n"},"scopePath":{"type":"string"}}},
"AccreditationHolder": {"type":"object","x-ticvai-persistence":"accreditation.holder","description":"**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n","required":["id","fullName"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true},"nationality":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true,"description":"12.1.16. The holder's own address — where a mobile credential and renewal notices go"},"phone":{"type":"string","nullable":true,"description":"12.1.16. E.164"},"identityDocumentVerified":{"type":"boolean","default":false},"organisationId":{"type":"string","format":"uuid","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","suspended","revoked","expired","archived"]},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"completenessPercent":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationProgramme": {"type":"object","x-ticvai-persistence":"accreditation.programme","description":"Boards 1.5 and 1.6. **The thing an application is made against.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"eventIds":{"type":"array","items":{"type":"string","format":"uuid"}},"categories":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"defaultAccessProfileId":{"type":"string","format":"uuid","nullable":true},"quota":{"type":"integer","nullable":true,"description":"**A cap on how many may be accredited in this category.** Without one, a category is a promise nobody counted.\n"},"badgeTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"The badge printed for this category; travels with the category when a programme is cloned"}}}},"applicantTypes":{"type":"array","items":{"type":"string"}},"applicationsOpenAt":{"type":"string","format":"date-time","nullable":true},"applicationsCloseAt":{"type":"string","format":"date-time","nullable":true},"approvalWorkflowId":{"type":"string","format":"uuid","nullable":true},"formId":{"type":"string","format":"uuid","nullable":true,"description":"12.1.2. The `marketing-crm` form definition (`createForm`, BO-618) the applicant fills in. The requirements matrix's `field` rows name the form fields they check, so the form is configured without software development and what blocks approval stays in one place.\n"},"isTemplate":{"type":"boolean","default":false,"description":"12.1.56. **A reusable programme template**: never opened for applications, and what `cloneAccreditationProgramme` copies its categories, requirements, validity, notification rules and form link from.\n"},"templateProgrammeId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The programme or template this one was cloned from"},"status":{"type":"string","enum":["draft","open","closed","archived"]},"faceMatching":{"type":"object","description":"**Face matching for duplicate applicants: only where the venue enables it, with each applicant's consent and the venue's legal sign-off; off by default** (Chinmay, 2 October, workbook Q461; ADR-0063; CHG-CSA-031). With `enabled` false, identity conflicts are raised on names, dates of birth and documents only and never on a face, and BO-631 shows no Face chip. Enabling needs `legalSignOffRef` (the venue's legal sign-off, recorded with who gave it and when), and a face is compared only for an applicant whose application carries a face-matching consent (the programme's consent form, CHG-CSA-026).","properties":{"enabled":{"type":"boolean","default":false},"legalSignOffRef":{"type":"string","nullable":true,"description":"The venue's legal sign-off document (a stored file reference)."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},"identityVerification":{"type":"object","description":"**UAE Pass and ICP verification, in release 1** (Chinmay, 2 October, workbook Q457; CHG-CSA-031). Which government identity checks an applicant passes through: UAE Pass sign-in (identity `guestUaePassLogin`) and the ICP identity check (access's verification adaptor). **Both need the client's access to the government services** (an external dependency); until it is granted, `methods` may name them but the check answers `manualReview`.","properties":{"methods":{"type":"array","items":{"type":"string","enum":["uaePass","icp","manualReview"]}},"required":{"type":"boolean","default":false,"description":"Whether an application is blocked from approval until a listed check passes."}}},"scopePath":{"type":"string"}}},
"AccreditationValidity": {"type":"object","x-ticvai-persistence":"accreditation.validity","description":"Board 6.3. **The control most often configured as never.**","properties":{"programmeId":{"type":"string","format":"uuid"},"validityKind":{"type":"string","enum":["eventDuration","fixedPeriod","seasonal","rolling","permanent"]},"validityMonths":{"type":"integer","nullable":true},"renewalWindowDays":{"type":"integer","nullable":true},"renewalRequiresReverification":{"type":"boolean","default":true,"description":"**The point of an expiry is that somebody looks again.**"},"onExpiry":{"type":"string","enum":["revokeAccess","gracePeriod","autoRenew"],"default":"revokeAccess"},"gracePeriodDays":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
