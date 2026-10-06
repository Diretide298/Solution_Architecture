# WS05 — Access Control board 5

**10 screens · 21 operations · 22 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, BIOMETRIC_IMAGE_VIEW, GUEST_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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
| `BO-184` | Biometric Access Command Center | C | 0 | 240 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-185` | Biometric Verification Profile Builder | A | 16 | 4 | 5 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-186` | Face Pass Enrollment Configuration | A | 19 | 8 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-187` | Biometric Consent & Guardian Management | B–D | 84 | 20 | 5 | 17 | 1 | 6 | — | notStarted (generated) |
| `BO-188` | Face Tag Temporary Enrollment | A | 10 | 17 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-189` | Face Matching & Verification Thresholds | A | 21 | 0 | 5 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-190` | Face Change, Re-enrollment & Identity Protection | C | 2 | 16 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-191` | Biometric Validation at Gate | C | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-192` | Biometric Lifecycle, Retention & Deletion | B–D | 9 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-193` | Biometric Simulation, Audit & Publication | C | 7 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**BO-188, BO-191 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-184` Biometric Access Command Center

**Central dashboard for biometric access configuration and operational health.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-184 |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-access-command-center-bo-184` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The command centre is a dashboard (VO-R02); the verification-profile and enrolment writes belong to BO-185 and BO-186, which declare them (ADR-0041; design-notes … Removed 2 October 2026 (CHG-WIR-001): The command centre is a dashboard (VO-R02); the verification-profile and enrolment writes belong to BO-185 and BO-186, which declare them (ADR-0041; design-notes …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The biometric board's command centre: Face Pass and Face Tag counts, enrolments today, verification success and failure, manual reviews, re-enrolment requests, blocked face changes, profiles pending deletion, camera health and alerts; tiles into the nine detail screens. The one thing to get right: Face Pass (persistent) and Face Tag (temporary) are always shown apart, and the face is a verification method, not the ticket.

**Fixed on main** (the package already carries these; draw what it says): Pattern listDetail with an empty "Every biometric access" table, plus writes for verification profile and enrolment settings on the command … (CHG-WIR-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Face Pass Profiles** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Active Face Tags** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Enrollments Today** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Successful Face Verifications** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Failed Verifications** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Manual Reviews** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Re-enrollment Requests** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Blocked Face Changes** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Profiles Pending Deletion** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Camera/Reader Health** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Biometric Security Alerts** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Every biometric access** (data table, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**The selected biometric access** (detail panel): The pack groups this record's detail under its own headings: “Profile Type Credential Venue Status”.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: The eleven pack tiles; Profiles pending deletion and Biometric security alerts show red when non-zero (a pending deletion is a compliance clock). *(source: screens/P08-venue-back-office.yaml#BO-184)*
- **Profile table**: Columns Profile type (Face Pass / Face Tag "Temporary" badge), Credential, Venue, Status - never a face image. *(source: screens/P08-venue-back-office.yaml#BO-184 / screens/P08-venue-back-office.yaml#BO-188)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open detail screens**: Tiles to BO-185 to BO-193 and back. *(source: DI-653)*

**Data it reads**: `listBiometricAccess` (onLoad, Biometric Access Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-185` Biometric Verification Profile Builder: *Works in Biometric Verification Profile Builder*; calls `listBiometricAccess`
- → `BO-186` Face Pass Enrollment Configuration: *Works in Face Pass Enrollment Configuration*; calls `listBiometricAccess`
- → `BO-187` Biometric Consent & Guardian Management: *Works in Biometric Consent & Guardian Management*; calls `listBiometricAccess`
- → `BO-188` Face Tag Temporary Enrollment: *Works in Face Tag Temporary Enrollment*; calls `listBiometricAccess`
- → `BO-189` Face Matching & Verification Thresholds: *Works in Face Matching & Verification Thresholds*; calls `listBiometricAccess`
- → `BO-190` Face Change, Re-enrollment & Identity Protection: *Works in Face Change, Re-enrollment & Identity Protection*; calls `listBiometricAccess`
- → `BO-191` Biometric Validation at Gate: *Works in Biometric Validation at Gate*; calls `listBiometricAccess`
- → `BO-192` Biometric Lifecycle, Retention & Deletion: *Works in Biometric Lifecycle, Retention & Deletion*; calls `listBiometricAccess`
- → `BO-193` Biometric Simulation, Audit & Publication: *Works in Biometric Simulation, Audit & Publication*; calls `listBiometricAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric access yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the biometric access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Biometrics switched off for the venue**: Whole board shows "Biometric access is off for this venue" with the venue setting link. *(source: contracts/spine/tenancy.yaml#/components/schemas/VenueSettings)*

#### Consistency with other screens

- Match `GST-069`: Face Pass wording and retention shown to guests must match the enrolment configuration here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  facePass: 2140
  faceTags: 386
  enrolmentsToday: 74
  verifiedToday: 5120
  failed: 61
  manualReviews: 14
  reEnrolment: 6
  blockedChanges: 2
  pendingDeletion: 9
  cameraHealth: 11/12 online
  alerts: 1
```

#### Permissions

- `listBiometricAccess` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-184` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-184`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 1: Opens Biometric Access Command Center → Central dashboard for biometric access configuration and operational health.
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F115 branch at step 1 (expected): when Nothing has been set up on Biometric Access Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F115 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …
- ADR-0041 *A command centre is a saved dashboard, not a screen* (`docs/adr/0041-a-command-centre-is-a-saved-dashboard.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (240 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-184?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-185`, `BO-186`, `BO-187`, `BO-188`, `BO-189`, `BO-190`, `BO-191`, `BO-192`, `BO-193`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-185` Biometric Verification Profile Builder

**Configure which ticket/credential types can or must use biometric verification. The matrix specifically requires biometric checks to be configurable by ticket type, including memberships, annual passes, multi-day and multi-attraction products.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · ticket #28428 (APP-SETUP-BO-185) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-verification-profile-builder-bo-185` |

**What the spec says about it.** **Bound 4 October 2026 to BiometricVerificationProfileBuilderInput: the eight pack labels are the values of one selectType, not eight fields; venueId comes from the session. The read gap is closed (getBiometricVerificationProfile is bound)** (CHG-FXS-002)

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Decides which tickets and credentials can or must use face verification, and where: a biometric profile picks the model (Face Pass, Face Tag, a future provider), what it applies to (ticket product or type, membership, annual pass, multi-day, multi-attraction, VIP credential, accreditation, customer segments) and the requirement per place - the pack's example "Annual Pass - Main entry Face required, Attractions Credential only, VIP Lounge Face required". The one thing to get right: draw it as a per-location matrix for one credential type, so the manager sees the whole journey's face requirements at once.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Eight selectFields, one per "applies to" kind, and Save changes with no operation; no read (CHG-WIR-004)
- The write has no product, membership or segment ids - only the kind (selectType) (CHG-SBO-005)
- profileId is required and venueId is a required string (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Profile name | text field | optional | — | — | — | — | `BiometricVerificationProfileBuilderInput.name` |
| Applies to | select | optional | — | Ticket product · Ticket type · Membership · Annual pass · Multi day ticket · Multi attraction ticket · Vip credential · Accreditation · Selected customer segments | — | One of ticket product, ticket type, membership, annual pass, multi-day, multi-attraction, VIP credential, accreditation (the pack's eight). | `BiometricVerificationProfileBuilderInput.selectType` |
| Biometric | segmented control | optional | — | Face pass · Face tag · Other provider | — | Biometric model this profile uses | `BiometricVerificationProfileBuilderInput.biometricType` |
| Face check | segmented control | optional | — | Not used · Optional · Required | — | Not used, optional or required. | `BiometricVerificationProfileBuilderInput.faceRequirement` |
| Status | segmented control | optional | Active | Active · Inactive | — | Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass) | `BiometricVerificationProfileBuilderInput.status` |

**Sent by *Save changes*** (`setBiometricVerificationProfile`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Face requirement `faceRequirement` | segmented control | required | — | Not used · Optional · Required | — | Whether face verification is not used, allowed, or required at this location (e.g. | `setBiometricVerificationProfile` body |
| Biometric type `biometricType` | segmented control | required | — | Face pass · Face tag · Other provider | — | Biometric model this profile uses | `setBiometricVerificationProfile` body |
| Profile `profileId` | picker: choose a profile | required | — | — | shows names, sends the id | The profile row's key (access.biometric_profile.id, a UUIDv7); absent creates one (decided 29 September, writers pass) | `setBiometricVerificationProfile` body |
| Select type `selectType` | select | required | — | Ticket product · Ticket type · Membership · Annual pass · Multi day ticket · Multi attraction ticket · Vip credential · Accreditation · Selected customer segments | — | Vocabulary listed under Select. | `setBiometricVerificationProfile` body |
| Venue `venueId` | text field | required | — | — | — | Venue | `setBiometricVerificationProfile` body |
| Park `parkId` | text field | optional | — | — | — | Park | `setBiometricVerificationProfile` body |
| Zone `zoneId` | text field | optional | — | — | — | Zone | `setBiometricVerificationProfile` body |
| Attraction `attractionId` | text field | optional | — | — | — | Attraction | `setBiometricVerificationProfile` body |
| Gate `gateId` | text field | optional | — | — | — | Gate | `setBiometricVerificationProfile` body |
| Name `name` | text field | optional | — | — | — | — | `setBiometricVerificationProfile` body |
| Status `status` | segmented control | optional | Active | Active · Inactive | — | Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass) | `setBiometricVerificationProfile` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **biometricType**: Face Pass (persistent, purple person icon) / Face Tag (temporary, clock icon and "Temporary" badge) / Other provider (greyed until a provider is chosen). *(source: screens/P08-venue-back-office.yaml#BO-185 / screens/P08-venue-back-office.yaml#BO-194 / contracts/spine/access.yaml#setBiometricVerificationProfile)*
- **selectType and the items**: First what kind of thing (Ticket product, Ticket type, Membership, Annual pass, Multi-day ticket, Multi-attraction ticket, VIP credential, Accreditation, Customer segments), then the actual products or segments from a picker. One choice, not eight selectFields. *(source: screens/P08-venue-back-office.yaml#BO-185 / contracts/spine/access.yaml#setBiometricVerificationProfile)*
- **Location matrix (faceRequirement per place)**: Rows are places from the tree (venue, park, zone, attraction, gate); each row Required / Optional / Not used ("Credential only"). Rows not listed inherit from their parent and say so. Saving writes one profile row per place. *(source: screens/P08-venue-back-office.yaml#BO-185 / contracts/spine/access.yaml#setBiometricVerificationProfile)*
- **status**: Active / Inactive; inactive profiles stay for reuse and are applied at no gate. *(source: contracts/spine/access.yaml#setBiometricVerificationProfile)*
- **venueId / profileId**: Not inputs (VO-R03); a new row sends no profileId. *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Load the profile as saved** (detail panel, from `getBiometricVerificationProfile`)

| Shows | Format | Notes |
|---|---|---|
| Face requirement | chip: Not used, Optional, Required | Whether face verification is not used, allowed, or required at this location (e.g. |
| Biometric type | chip: Face pass, Face tag, Other provider | Biometric model this profile uses |
| Select type | chip: Ticket product, Ticket type, Membership, Annual pass, Multi day ticket, Multi … | Vocabulary listed under Select. |
| Name | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | `setBiometricVerificationProfile` PUT `/biometric-verification-profile` | BiometricVerificationProfileBuilderInput | BiometricVerificationProfileBuilderView | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Profile list**: Name, type badge (Face Pass / Face Tag "Temporary"), applies to, places with Required count, status. *(source: screens/P08-venue-back-office.yaml#BO-184 / contracts/spine/access.yaml#listBiometricAccess)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save profile**: One upsert per place row (whole rows, VO-R04); confirmation "Face required at 2 places, optional at 1; applies at the next package". *(source: contracts/spine/access.yaml#setBiometricVerificationProfile)*

**Data it reads**: `getBiometricVerificationProfile` (onLoad, Load the profile as saved)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `setBiometricVerificationProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric verification profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric verification profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric verification profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Face required at a gate without a biometric camera**: Warning naming the gate (the reader configuration, BO-199, has no camera). *(source: screens/P08-venue-back-office.yaml#BO-203 / contracts/spine/access.yaml#setReaderScannerPeripheral)*
- **Biometrics off for the venue**: Screen read-only with "Biometric access is off for this venue". *(source: contracts/spine/tenancy.yaml#/components/schemas/VenueSettings)*

#### Consistency with other screens

- Match `BO-184`: The profile directory there lists these profiles with the same badges.
- Match `BO-147`: An attraction's biometric requirement is this setting; one place to set it.
- Match `BO-177`: Face Pass appears as a verification method only for products a profile covers.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  name: Annual Pass Face
  type: Face Pass
  appliesTo: Annual pass - Summit Peaks Annual Pass, Aqua Park Annual Pass
  status: Active
matrix:
- place: Summit Peaks main entry
  requirement: Required
- place: Summit Peaks attractions
  requirement: Not used (credential only)
- place: VIP Lounge
  requirement: Required
```

#### Permissions

- `setBiometricVerificationProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `getBiometricVerificationProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-185` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-185`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 2: Works in Biometric Verification Profile Builder → Configure which ticket/credential types can or must use biometric verification. The matrix specifically requires biometric checks to be configurable by ticket type, including memberships, annual …

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-185?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-186` Face Pass Enrollment Configuration

**Configure persistent Face Pass registration. The source specifies that Face Pass may be registered through the App, ticket counters or Annual Pass counter.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · ticket #28429 (APP-SETUP-BO-186) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture Required Consent; Capture Face; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/face-pass-enrollment-configuration-bo-186` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of the Face Pass enrolment configuration (setFacePassEnrollment has no get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Configures persistent Face Pass enrolment: the channels (TICVAI app, ticket counter, annual pass counter, self-service kiosk, other authorised channel), the journey (Identify guest > Verify eligible credential > Capture required consent > Capture face > Quality check > Duplicate/identity check > Create biometric profile > Bind virtual credential) and the rules (login, valid pass, ID check, capture attempts, image quality, duplicate face detection, operator verification, enrolment expiry). The one thing to get right: the annual-pass rule "one face, one annual pass" is shown as a fixed safeguard, with the pack's result "DUPLICATE ASSOCIATION BLOCKED".

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write-only (no read of the current configuration) (CHG-WIR-004)

**Fixed on main** (the package already carries these; draw what it says): Enrolment channels include Self-service kiosk and Other authorised channel, and DI-641 adds the turnstile, while enrolFacePass allows only … (CHG-SBO-009); A selectField labelled "→" (an arrow from the pack's journey) and booleans drawn as selectFields; Number of capture attempts as a textField (CHG-SBO-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **May Face Pass be enrolled at a self-service kiosk or at the turnstile on first use, as the MoM records, or only at the app and the two counters, as the contract says?** → Face Pass enrolment: the app, the staffed counters and a self-service kiosk (consent shown); not the turnstile. *(decided by Chinmay, 2026-10-02; DEC-236 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Enrolment channels | multi-select chips | optional | — | Ticvai app · Ticket counter · Annual pass counter · Self service kiosk · Other authorized channel | — | **The app, the staffed ticket and annual-pass counters, and a self-service kiosk with the consent shown; never the turnstile (decided 2 October 2026 by Chinmay, DEC-236; CHG-CSP-021).** The journey … | `FacePassEnrollmentConfigurationInput.enrollmentChannels` |
| Account login required | toggle | optional | — | — | — | Account login required | `FacePassEnrollmentConfigurationInput.accountLoginRequired` |
| Valid ticket/pass required | toggle | optional | — | — | — | Valid ticket/pass required | `FacePassEnrollmentConfigurationInput.validTicketPassRequired` |
| Identity check required | toggle | optional | — | — | — | Identity check required | `FacePassEnrollmentConfigurationInput.identityCheckRequired` |
| Number of capture attempts | number field | optional | — | — | — | Number of capture attempts | `FacePassEnrollmentConfigurationInput.numberOfCaptureAttempts` |
| Minimum image quality | text field | optional | — | — | — | minimum image quality | `FacePassEnrollmentConfigurationInput.minimumImageQuality` |
| Duplicate face detection | toggle | optional | — | — | — | Block a face already associated with another annual pass | `FacePassEnrollmentConfigurationInput.duplicateFaceDetection` |
| Operator verification | toggle | optional | — | — | — | An operator must verify the capture | `FacePassEnrollmentConfigurationInput.operatorVerification` |

**Form: Save Face Pass enrolment** (modal, opened by *Save Face Pass enrolment*; *Save Face Pass enrolment* calls `setFacePassEnrollment`, *Cancel* sends nothing)

**Collects what `setFacePassEnrollment` sends before it is called.** Required: `venueId`. Optional: `enrollmentChannels`, `accountLoginRequired`, `validTicketPassRequired`, `identityCheckRequired`, `numberOfCaptureAttempts`, `minimumImageQuality`, `operatorVerification`, `enrollmentExpiry`, `duplicateFaceDetection`. `venueId` from the session. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | text field | required | — | — | — | Venue this enrolment configuration applies to | `setFacePassEnrollment` body |
| Enrollment channels `enrollmentChannels` | multi-select chips | optional | — | Ticvai app · Ticket counter · Annual pass counter · Self service kiosk · Other authorized channel | — | Channels where Face Pass enrolment is enabled. The app, the staffed counters and a self-service kiosk that shows the consent form; never the turnstile (decided 2 October 2026 … | `setFacePassEnrollment` body |
| Account login required `accountLoginRequired` | toggle | optional | — | — | — | Account login required | `setFacePassEnrollment` body |
| Valid ticket pass required `validTicketPassRequired` | toggle | optional | — | — | — | Valid ticket/pass required | `setFacePassEnrollment` body |
| Identity check required `identityCheckRequired` | toggle | optional | — | — | — | Identity check required | `setFacePassEnrollment` body |
| Number of capture attempts `numberOfCaptureAttempts` | number field | optional | — | — | — | Number of capture attempts | `setFacePassEnrollment` body |
| Minimum image quality `minimumImageQuality` | text field | optional | — | — | — | minimum image quality | `setFacePassEnrollment` body |
| Operator verification `operatorVerification` | toggle | optional | — | — | — | An operator must verify the capture | `setFacePassEnrollment` body |
| Enrollment expiry `enrollmentExpiry` | number field | optional | — | — | — | Days an enrolment stays valid before re-enrolment is needed | `setFacePassEnrollment` body |
| Duplicate face detection `duplicateFaceDetection` | toggle | optional | — | — | — | Block a face already associated with another annual pass | `setFacePassEnrollment` body |
| Status `status` | segmented control | optional | Active | Active · Inactive | — | Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass) | `setFacePassEnrollment` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **enrollmentChannels**: Checkbox cards; see corrections - the enrolment operation allows only the app, ticket counter and annual pass counter, so kiosk and other channels must be resolved before they are offered. *(source: screens/P08-venue-back-office.yaml#BO-186 / contracts/spine/access.yaml#setFacePassEnrollment / contracts/spine/access.yaml#enrolFacePass)*
- **accountLoginRequired / validTicketPassRequired / identityCheckRequired / operatorVerification**: Toggles; valid ticket/pass required defaults on; operator verification forced on for counter channels. *(source: contracts/spine/access.yaml#setFacePassEnrollment)*
- **numberOfCaptureAttempts**: Stepper 1-5, default 3. *(source: contracts/spine/access.yaml#setFacePassEnrollment / designer default)*
- **minimumImageQuality**: Low / Medium / High as in the matching thresholds (BO-189), not free text. *(source: contracts/spine/access.yaml#setFacePassEnrollment / screens/P08-venue-back-office.yaml#BO-189)*
- **duplicateFaceDetection**: Shown on and locked for annual passes ("One face may not be associated with more than one annual pass"); switchable only for other products if the client allows. *(source: screens/P08-venue-back-office.yaml#BO-187 / contracts/spine/access.yaml#enrolFacePass)*
- **enrollmentExpiry**: Days before re-enrolment is needed, empty = no expiry; independent of data retention (BO-192). *(source: contracts/spine/access.yaml#setFacePassEnrollment)*
- **Enrolment channels**: The app, the staffed counters and a self-service kiosk (with the consent shown on the kiosk); never the turnstile on first use. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Outputs: what the screen shows and produces

**Shown**

**Load the configuration as saved** (detail panel, from `getFacePassEnrollmentConfiguration`)

| Shows | Format | Notes |
|---|---|---|
| Enrollment channels | list or chips (count when long) | Channels where Face Pass enrolment is enabled. The app, the staffed counters and a self-service kiosk that shows the consent form; never … |
| Account login required | yes / no (icon or chip) | Account login required |
| Valid ticket pass required | yes / no (icon or chip) | Valid ticket/pass required |
| Identity check required | yes / no (icon or chip) | Identity check required |
| Number of capture attempts | 1,234 | Number of capture attempts |
| Minimum image quality | text | minimum image quality |
| Operator verification | yes / no (icon or chip) | An operator must verify the capture |
| Enrollment expiry | 1,234 | Days an enrolment stays valid before re-enrolment is needed |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save Face Pass enrolment (primary button) | `setFacePassEnrollment` PUT `/face-pass-enrollment` | FacePassEnrollmentConfigurationInput | FacePassEnrollmentConfigurationView | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Enrolment journey strip**: The eight pack steps, with steps switched off by the rules greyed; consent step links to BO-187. *(source: screens/P08-venue-back-office.yaml#BO-186)*
- **Duplicate example**: "Face profile F-8721 already associated with Annual Pass AP-10982 - DUPLICATE ASSOCIATION BLOCKED" as the help example. *(source: screens/P08-venue-back-office.yaml#BO-187)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save enrolment configuration**: Whole-record upsert for the venue (VO-R04); applies to enrolments started after the save. *(source: contracts/spine/access.yaml#setFacePassEnrollment)*

**Data it reads**: `getFacePassEnrollmentConfiguration` (onLoad, Load the configuration as saved)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `setFacePassEnrollment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The face pass enrollment configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the face pass enrollment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No face pass enrollment configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Guest is a minor**: Journey shows the guardian consent branch from BO-187 before capture. *(source: screens/P08-venue-back-office.yaml#BO-187 / contracts/spine/access.yaml#enrolFacePass)*

#### Consistency with other screens

- Match `GST-069`: The guest app's Face Pass enrolment follows this journey and these rules.
- Match `BO-188`: Face Tag enrolment is configured there and may use the entry gate; Face Pass may not.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
config:
  venue: Aqua Park
  channels: TICVAI app, Ticket counter, Annual pass counter
  login: true
  validPass: true
  idCheck: Counter only
  attempts: 3
  quality: Medium
  duplicate: On (locked)
  operatorVerification: true
  expiry: 730 days
  status: Active
```

#### Permissions

- `setFacePassEnrollment` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `getFacePassEnrollmentConfiguration` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-186` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-186`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 4: Works in Face Pass Enrollment Configuration → Configure persistent Face Pass registration. The source specifies that Face Pass may be registered through the App, ticket counters or Annual Pass counter.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-186?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save Face Pass enrolment.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-187` Biometric Consent & Guardian Management

**Manage consent requirements associated with persistent biometric enrollment. The matrix requires App users to provide consent before Face Pass registration and requires guardian consent for minors. On-site enrollment also requires consent before facial data is captured.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `venueId` (session) |
| Route | `/access-venue/biometric-consent-guardian-management-bo-187` |

**What the spec says about it.** **setVenueSettings replaces the whole settings row** (PUT; an omitted property returns to its default). The save sends the VenueSettings that getVenueSettings returned, with only this screen's group changed; nothing else is reset (CHG-FXS-003).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Consent for persistent biometric enrolment: the policy by jurisdiction, tenant, venue, credential, enrolment channel and guest category, the adult journey (Guest identified > Consent presented > Accepted > Facial capture enabled), the minor journey (Minor identified > Guardian required > Guardian identity/relationship > Consent > Verification > Facial capture enabled), and the consent records kept as evidence. The one thing to get right: the pack's critical separation - biometric data and the consent/audit record are different things; after deletion the face is gone but the consent record may stay, and the screen must say which is which.

**Known correction pending (do not draw the wrong version)**

- **Read-only screen; the pack's consent policy configuration has no write** Why: The screen configures consent requirements by jurisdiction, credential, channel and guest category; only the evidence list is readable. *(source: screens/P08-venue-back-office.yaml#BO-187 / contracts/spine/access.yaml#listBiometricConsentGuardian; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Tenant and Venue drawn as selectFields** Why: Session scope (VO-R09); only jurisdiction, credential, channel and guest category are filters. *(source: screens/P08-venue-back-office.yaml#BO-187; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are children's faces enrolled at all, and if so with guardian consent only - and from what age is a guest a minor per jurisdiction?** → Minors: enrolment with guardian consent on the venue's form; the minor age is set per country; the venue can switch minors off. Supersedes the GST-069 default. *(decided by Chinmay, 2026-10-02; DEC-237 / CHG-NOTE-008)*
- **Which reference client's live privacy policy and app should the consent wording model?** → Drawn default accepted: Placeholder consent text marked "Draft - to be replaced". *(decided by Chinmay, 2026-10-02; DEC-238 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Country/Jurisdiction | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Credential | select field | — | — | — | — | — | — |
| Enrollment Channel | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Country jurisdiction | text field | — | — | `listBiometricConsentGuardian` ?countryJurisdiction |
| Credential type | text field | — | — | `listBiometricConsentGuardian` ?credentialType |
| Enrollment channel | text field | — | — | `listBiometricConsentGuardian` ?enrollmentChannel |
| Guest category | text field | — | — | `listBiometricConsentGuardian` ?guestCategory |

**Form: Save minors and consent** (modal, opened by *Save minors and consent*; *Save minors and consent* calls `setVenueSettings`, *Cancel* sends nothing)

**Collects what `setVenueSettings` sends before it is called.** Nothing in the body is required. Optional: `biometrics`. Only the biometrics section: the consent form, the minors switch. Dismissing sends nothing; the screen behind is unchanged. **setVenueSettings replaces the whole settings row** (PUT; an omitted property returns to its default). The save sends the VenueSettings that getVenueSettings returned, with only this screen's group changed; nothing else is reset (CHG-FXS-003).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Calendar day start hour `calendarDayStartHour` | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in … | `setVenueSettings` body |
| Support hours `supportHours` | group | optional | — | — | — | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. | `setVenueSettings` body |
| Mode `supportHours.mode` | radio group | optional | — | Always on · Business hours · Custom · None | — | — | `setVenueSettings` body |
| Timezone `supportHours.timezone` | text field | optional | — | — | — | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. | `setVenueSettings` body |
| Windows `supportHours.windows` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `supportHours.windows[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `supportHours.windows[].from` | text field | optional | — | — | — | Wall-clock time the desk opens. | `setVenueSettings` body |
| To `supportHours.windows[].to` | text field | optional | — | — | — | Wall-clock time the desk closes. | `setVenueSettings` body |
| Out of hours message `supportHours.outOfHoursMessage` | text field | optional | — | — | — | — | `setVenueSettings` body |
| Quiet hours `quietHours` | group | optional | — | — | — | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. | `setVenueSettings` body |
| From `quietHours.from` | text field | optional | — | — | — | Wall-clock time sending stops | `setVenueSettings` body |
| To `quietHours.to` | text field | optional | — | — | — | Wall-clock time sending resumes | `setVenueSettings` body |
| Biometrics `biometrics` | group | optional | — | — | — | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. | `setVenueSettings` body |
| Is enabled `biometrics.isEnabled` | toggle | optional | off | Off by default, and turning it on is refused without the two fields below. | — | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — a DPIA nobody can … | `setVenueSettings` body |
| Dpia reference `biometrics.dpiaReference` | text field | optional | — | max length 200 | — | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is … | `setVenueSettings` body |
| Consent notice acknowledged at `biometrics.consentNoticeAcknowledgedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice … | `setVenueSettings` body |
| Face tag purge minutes after close `biometrics.faceTagPurgeMinutesAfterClose` | number field (minutes) | optional | 0 | — | — | BL-106. How long a same-visit Face Tag survives past the close of the operating day, and zero is the default because that is what 3.2.44 describes. | `setVenueSettings` body |
| Consent form `biometrics.consentFormId` | picker: choose a consent form | optional | — | Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access … | shows names, sends the id | The venue's own consent form, which every biometric capture is taken on (decided 2 October 2026, Chinmay, batch 4, BO-188: "Consent first, on the venue's consent form"; DEC-128 … | `setVenueSettings` body |
| Allow minors `biometrics.allowMinors` | toggle | optional | on | Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method. | — | Whether this venue enrols minors at all (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: "Guardian consent on the venue's form; minor age per country; the … | `setVenueSettings` body |
| Accreditation face matching `biometrics.accreditationFaceMatching` | group | optional | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables it, with applicant …; Enabling it is refused without `legalSignOffReference` … | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables … | `setVenueSettings` body |
| Is enabled `biometrics.accreditationFaceMatching.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettings` body |
| Legal sign off reference `biometrics.accreditationFaceMatching.legalSignOffReference` | text field | optional | — | max length 200 | — | The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when. | `setVenueSettings` body |
| Segregated access `segregatedAccess` | group | optional | — | — | — | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a prayer-time closure. | `setVenueSettings` body |
| Is enabled `segregatedAccess.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettings` body |
| Applies to access points `segregatedAccess.appliesToAccessPointIds` | multi-picker: choose applies to access points | optional | — | — | — | — | `setVenueSettings` body |
| Schedule `segregatedAccess.schedule` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `segregatedAccess.schedule[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `segregatedAccess.schedule[].from` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| To `segregatedAccess.schedule[].to` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| Admits `segregatedAccess.schedule[].admits` | radio group | optional | — | All · Women · Women and children · Families · Members | — | — | `setVenueSettings` body |
| Gender verification `segregatedAccess.genderVerification` | segmented control | optional | Off | Off · Staff assisted · Device assisted; Available only where the driver reports the capability, and the result is advisory to the steward rather than decisive at the turnstile (3. | — | `off` — the entitlement decides and a steward handles exceptions. The default, and what is contracted. | `setVenueSettings` body |
| Override rate alert threshold `segregatedAccess.overrideRateAlertThreshold` | number field | optional | — | — | — | Where `deviceAssisted` is on. An override rate near zero means the steward has stopped deciding, and that is the number that says whether the human safeguard is working or … | `setVenueSettings` body |
| Alerting `alerting` | group | optional | — | The panel is the default and email or WhatsApp only where the matrix names them — an operational alert that arrives by email is an alert nobody sees in time. | — | CF-134. On-platform notification, marked as read. | `setVenueSettings` body |
| Channel `alerting.channel` | segmented control | optional | Dashboard panel | Dashboard panel · Dashboard and email · Dashboard and whatsapp | — | — | `setVenueSettings` body |
| Acknowledgement required `alerting.acknowledgementRequired` | toggle | optional | on | — | — | — | `setVenueSettings` body |
| Escalate after minutes `alerting.escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setVenueSettings` body |
| Display currencies `displayCurrencies` | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `setVenueSettings` body |
| Charge currencies `chargeCurrencies` | list of values (chips) | optional | — | presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. | — | Which currencies a guest may select and pay in (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). | `setVenueSettings` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettings` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettings` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettings` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettings` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettings` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| … 34 more | | | | | | the rest are in `schemas.json` | `setVenueSettings` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender …

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters (countryJurisdiction, credentialType, enrollmentChannel, guestCategory)**: Filters of the consent record list; tenant and venue come from the session (VO-R09), not selects. *(source: contracts/spine/access.yaml#listBiometricConsentGuardian)*
- **Consent policy (per jurisdiction, credential, channel, guest category)**: The pack's configuration: which consent text version applies, whether a guardian is required (minor age per jurisdiction), and what verification the guardian needs. No write exists; draw the policy panel read-only with "Policy set by the privacy team" until one does. Minors: enrolment only with guardian consent on the venue's form; the minor age is set per country; the venue can switch minors off. *(source: screens/P08-venue-back-office.yaml#BO-187 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Outputs: what the screen shows and produces

**Shown**

**Minors and consent** (detail panel, from `getVenueSettings`): **Minors enrol only with a guardian's consent on the venue's own form; the minor age is set per country (`RegionSettings.minorAgeThreshold`); the venue can switch minors off (`biometrics.allowMinors`) (decided 2 October 2026 by Chinmay, DEC-237; supersedes the GST-069 default; CHG-CSP-019).**

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Calendar day start hour | 1,234 | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar … |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Mode | chip: Always on, Business hours, Custom, None | — |
| Timezone | text | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. |
| Windows | list or chips (count when long) | — |
| Day | chip: Mon, Tue, Wed, Thu, Fri, Sat… | — |
| From | text | Wall-clock time the desk opens. |
| To | text | Wall-clock time the desk closes. |
| Out of hours message | text | — |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| From | text | Wall-clock time sending stops |
| To | text | Wall-clock time sending resumes |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Is enabled | yes / no (icon or chip) | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable … |
| Dpia reference | text | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one … |
| Consent notice acknowledged at | 1 Oct 2026, 14:30 | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save minors and consent (secondary button) | `setVenueSettings` PUT `/venues/{venueId}/settings` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Journey strips**: Adult and Minor journeys side by side as the pack draws them; capture is the last step of both and is greyed until consent is recorded. *(source: screens/P08-venue-back-office.yaml#BO-187)*
- **Consent records**: Columns Consent record ID, Policy/version, Time, Channel, Guardian reference, Venue, Operator, Status (Active, Withdrawn, Biometric deleted - consent retained); cursor paging (VO-R12); no face image anywhere. *(source: screens/P08-venue-back-office.yaml#BO-188 / contracts/spine/access.yaml#/components/schemas/BiometricConsentGuardianManagementView)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open consent record**: Shows the evidence fields and the linked enrolment's state; read-only. *(source: contracts/spine/access.yaml#listBiometricConsentGuardian)*

**Data it reads**: `listBiometricConsentGuardian` (onLoad, Biometric Consent & Guardian Management); `getVenueSettings` (onLoad, The venue's minors switch and consent form (DEC-237))

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listBiometricConsentGuardian`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric consent guardian configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric consent guardian untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric consent guardian configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender … |

#### Edge cases to draw

- **Consent withdrawn**: Status Withdrawn and the biometric deletion status beside it; a withdrawn consent with a template still held is flagged red. *(source: screens/P08-venue-back-office.yaml#BO-188 / contracts/spine/access.yaml#revokeFacePass)*
- **Viewer without biometric privacy rights**: Guest and guardian references masked (VO-R08). *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `GST-069`: The consent text the guest accepts and its version must equal the version recorded here; modelled on the reference client's published privacy policy.
- Match `BO-192`: Deletion of biometric data is configured there; the consent record survives it.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
records:
- id: CNS-2026-004812
  policy: Face Pass consent v1.2 (UAE)
  time: 28 Sep 2026 10:14
  channel: TICVAI app
  guardian: '-'
  venue: Aqua Park
  status: Active
- id: CNS-2026-004977
  policy: Face Pass consent v1.2 (UAE)
  time: 30 Sep 2026 15:40
  channel: Annual pass counter
  guardian: Fatima Al Hashimi (mother)
  operator: Maria Santos
  status: Active
- id: CNS-2026-003101
  policy: Face Pass consent v1.1 (UAE)
  channel: TICVAI app
  status: Biometric deleted - consent retained
```

#### Permissions

- `listBiometricConsentGuardian` → `SCOPE_VIEW` (read) · staff
- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `setVenueSettings` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 15.1.32 | Overstock Alerts - System shall generate overstock alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.33 | Stock Shortage Alerts - System shall generate stock shortage alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.34 | Expiry Alerts - System shall generate expiry alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 16.4.23 | Device Alerts - System shall generate device alerts. | Device Management | CONTRACTED | data `VenueSettings` |
| 16.9.58 | Device Incident Management - System shall support device incident management. | Device Management | CONTRACTED | data `VenueSettings` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: use an existing major venue-group client's live app and published privacy policy as the model for how facial-recognition consent, data use and retention are explained to guests. *(client request · MoM 2 Sep 2026, 4.11 Privacy & Biometric Data Retention · DI-642)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-187` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-187`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 6: Works in Biometric Consent & Guardian Management → Manage consent requirements associated with persistent biometric enrollment. The matrix requires App users to provide consent before Face Pass registration and requires guardian consent for minors. …

#### Acceptance for the design

- [ ] Every input above is drawn (84), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-187?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save minors and consent.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-188` Face Tag Temporary Enrollment

**Configure the temporary biometric model separately from Face Pass. The matrix describes Face Tag as temporarily stored facial data, enrollable at ticket counters or entry gates, with biometric data permanently deleted once the associated ticket is fully redeemed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · ticket #28430 (APP-SETUP-BO-188) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Face Captured) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/face-tag-temporary-enrollment-bo-188` |

**What the spec says about it.** **Face Tag has its own enrolment operation (`enrolFaceTag`), separate from Face Pass, and it may capture at the entry gate** as the pack and the minutes say; the "never at a gate" rule is Face Pass's (CHG-CSP-018, DEC-236).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Configures Face Tag, the temporary face credential for one ticket or visit: where it may be captured (ticket counter, entry gate), what it binds to (ticket, visit, temporary credential), when it is deleted (default when the ticket is fully redeemed) and how consent is taken. The one thing to get right: Face Tag looks visibly different from Face Pass ("Temporary") and its deletion trigger is the headline of the screen.

**Fixed on main** (the package already carries these; draw what it says): A selectField labelled "→" and an empty table (CHG-SBO-009); Face Tag capture at the entry gate conflicts with enrolFacePass's "never at a gate" rule (CHG-SBO-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What is the lawful maximum retention for Face Tags and failed captures?** → Biometric capture and retention need the guest's consent first, on the venue's own consent form. Where TICVAI stores the data, the venue is warned that the guest must accept a consent form. *(decided by Chinmay, 2026-10-02; DEC-128 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Form: Save Face Tag profile** (modal, opened by *Save Face Tag profile*; *Save Face Tag profile* calls `setFaceTagTemporaryEnrollment`, *Cancel* sends nothing)

**Collects what `setFaceTagTemporaryEnrollment` sends before it is called.** Required: `venueId`, `name`, `enrollmentChannels`, `bindTo`, `deletionTrigger`. Optional: `profileId`, `retentionThresholdHours`, `consentFormId`, `consentCapture`. `consentFormId` picks one of the venue's consent forms (built in BO-747); `consentCapture` says where the consent is shown. `venueId` from the session. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Profile `profileId` | picker: choose a profile | optional | — | — | shows names, sends the id | Absent creates a Face Tag profile | `setFaceTagTemporaryEnrollment` body |
| Venue `venueId` | text field | required | — | — | — | — | `setFaceTagTemporaryEnrollment` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setFaceTagTemporaryEnrollment` body |
| Enrollment channels `enrollmentChannels` | multi-select chips | required | — | Ticket counter · Entry gate; at least 1 | — | Where a Face Tag may be captured | `setFaceTagTemporaryEnrollment` body |
| Bind to `bindTo` | segmented control | required | Ticket | Ticket · Visit · Temporary credential | — | What the Face Tag is bound to | `setFaceTagTemporaryEnrollment` body |
| Deletion trigger `deletionTrigger` | radio group | required | Ticket fully redeemed | Ticket fully redeemed · End of visit · Ticket expiration · Credential cancellation · Operational retention threshold | — | When the Face Tag is deleted automatically. | `setFaceTagTemporaryEnrollment` body |
| Retention threshold hours `retentionThresholdHours` | number field (hours) | optional | — | min 1; Used only when deletionTrigger is operationalRetentionThreshold, and then required. | — | Used only when deletionTrigger is operationalRetentionThreshold, and then required. | `setFaceTagTemporaryEnrollment` body |
| Consent form `consentFormId` | picker: choose a consent form | optional | — | With neither, the profile is refused `422 consent-form-required`. | shows names, sends the id | The venue's own consent form a Face Tag is captured on (decided 2 October 2026, Chinmay, batch 4, BO-188: "consent first, using a consent form from the venue"; DEC-128, DEC-549 … | `setFaceTagTemporaryEnrollment` body |
| Consent capture `consentCapture` | segmented control | optional | On screen acknowledgement | On screen acknowledgement · Signed form | — | How consent is taken when a Face Tag is captured (3.2.44; added 29 September, build pass). | `setFaceTagTemporaryEnrollment` body |
| Status `status` | segmented control | optional | Active | Active · Inactive | — | Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass) | `setFaceTagTemporaryEnrollment` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 operationalRetentionThreshold chosen with no retentionThresholdHours, or no consent form on the profile or the venue (`consent-form-required`; CHG-CSP-018)

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **enrollmentChannels**: Ticket counter and/or Entry gate (checkboxes); at least one. *(source: contracts/spine/access.yaml#setFaceTagTemporaryEnrollment)*
- **bindTo**: Ticket (default) / Visit / Temporary credential, as radio cards. *(source: contracts/spine/access.yaml#setFaceTagTemporaryEnrollment)*
- **deletionTrigger / retentionThresholdHours**: Default "When the ticket is fully redeemed"; alternatives End of visit, Ticket expiry, Credential cancelled, After N hours. Hours appear only for the last and are then required; no default and no maximum is pre-filled - show the hint that the legal maximum is pending the DPO. *(source: contracts/spine/access.yaml#setFaceTagTemporaryEnrollment / ADR-0063)*
- **consentCapture**: On-screen acknowledgement (default) or Signed form. *(source: contracts/spine/access.yaml#setFaceTagTemporaryEnrollment)*
- **Consent**: Capture and retention need the guest's consent first, on the venue's own consent form. Where TICVAI stores the data, the screen warns the venue that the guest must accept a consent form. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Outputs: what the screen shows and produces

**Shown**

**Consent is required** (banner, from `listFaceTagTemporary`): **Biometric capture and retention need the guest's consent first, on the venue's own consent form (decided 2 October 2026 by Chinmay, DEC-128; CHG-CSP-018).** Where TICVAI holds the templates (`templatesHeldByTicvai`), this banner warns the venue that each guest must accept the consent form. **Minors** enrol only with a guardian's consent on that form; the minor age is set per country and the …

| Shows | Format | Notes |
|---|---|---|
| Templates held by ticvai | yes / no (icon or chip) | Where TICVAI stores the Face Tag templates, the screen warns the venue that every guest must accept the venue's consent form before capture … |
| Consent form | the name it points at, never the id | The venue's consent form this profile captures on (DEC-128; CHG-CSP-018). |
| Enrollment channels | list or chips (count when long) | Where a Face Tag may be captured |
| Bind to | chip: Ticket, Visit, Temporary credential | What the Face Tag is bound to |
| Deletion trigger | chip: Ticket fully redeemed, End of visit, Ticket expiration, Credential cancellation … | When the Face Tag is automatically deleted; default ticketFullyRedeemed |
| Profile | text | — |
| Venue | text | — |
| Name | text | — |
| Retention threshold hours | 1,234 | Used when deletionTrigger is operationalRetentionThreshold. |
| Consent capture | chip: On screen acknowledgement, Signed form | How consent is taken at capture; onScreenAcknowledgement (no form to sign) unless set |

**Face Tag profiles** (data table, from `listFaceTagTemporary`): The journey (consent, capture at the counter or the entry gate, bind to the ticket, delete on exit or close) is a strip above the list, not a field.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Enrollment channels | list or chips (count when long) | Where a Face Tag may be captured |
| Bind to | chip: Ticket, Visit, Temporary credential | What the Face Tag is bound to |
| Deletion trigger | chip: Ticket fully redeemed, End of visit, Ticket expiration, Credential cancellation … | When the Face Tag is automatically deleted; default ticketFullyRedeemed |
| Retention threshold hours | 1,234 | Used when deletionTrigger is operationalRetentionThreshold. |
| Consent form | the name it points at, never the id | The venue's consent form this profile captures on (DEC-128; CHG-CSP-018). |
| Templates held by ticvai | yes / no (icon or chip) | Where TICVAI stores the Face Tag templates, the screen warns the venue that every guest must accept the venue's consent form before capture … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save Face Tag profile (primary button) | `setFaceTagTemporaryEnrollment` PUT `/face-tag-temporary` | FaceTagTemporaryEnrollmentInput | FaceTagTemporaryEnrollmentView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 operationalRetentionThreshold chosen with no retentionThresholdHours, or no consent form on the profile or the … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Journey strip**: Ticket presented > Face captured > Temporary Face Tag > Ticket linked > Access journey > Fully redeemed > Biometric data deleted, with the chosen trigger highlighted. *(source: screens/P08-venue-back-office.yaml#BO-189)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save Face Tag profile**: Whole-profile upsert (VO-R04); inactive profiles stay for reuse. *(source: contracts/spine/access.yaml#setFaceTagTemporaryEnrollment)*

**Data it reads**: `listFaceTagTemporary` (onLoad, Face Tag Temporary Enrollment)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listFaceTagTemporary`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The face tag temporary configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the face tag temporary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No face tag temporary configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 operationalRetentionThreshold chosen with no retentionThresholdHours, or no consent form on the profile or the venue (`consent-form-required`; CHG-CSP-018) |

#### Consistency with other screens

- Match `BO-184`: Face Tags carry the "Temporary" badge everywhere.
- Match `GST-069`: Face Tag is never offered in the guest app.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  name: Day visitors - gate enrolment
  channels: Entry gate, Ticket counter
  bindTo: Ticket
  deletion: When the ticket is fully redeemed
  consent: On-screen acknowledgement
```

#### Permissions

- `listFaceTagTemporary` → `SCOPE_VIEW` (read) · staff
- `setFaceTagTemporaryEnrollment` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-188` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-188`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 8: Works in Face Tag Temporary Enrollment → Configure the temporary biometric model separately from Face Pass. The matrix describes Face Tag as temporarily stored facial data, enrollable at ticket counters or entry gates, with biometric data …

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-188?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save Face Tag profile.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-189` Face Matching & Verification Thresholds

**Configure biometric verification behavior. The source requires a configurable Biometric Check Level determining the scoring of biometric comparison.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · ticket #28431 (APP-SETUP-BO-189) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/face-matching-verification-thresholds-bo-189` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Sets how a face match is judged per access context (main entry, child protection, attraction): decision bands (high confidence = allow if other rules pass; review range = amber operator check; below = deny), liveness, duplicate-face check, image quality, capture timeout, retries, mask handling and operator fallback. The one thing to get right: draw the two thresholds as bands on one 0-100% scale so the gap between them is visible.

**Fixed on main** (the package already carries these; draw what it says): Liveness, duplicate check, quality, timeout, retries and mask handling are all selectFields; the two thresholds are missing from the form (CHG-SBO-009).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| High-confidence match from | stepper or slider | optional | — | min 0; max 1 | — | The decision bands: at or above this, admit. | `FaceMatchingVerificationThresholdsInput.highConfidenceMin` |
| Review range from | stepper or slider | optional | — | min 0; max 1 | — | Between this and the high-confidence band, an operator reviews; below it, refuse. | `FaceMatchingVerificationThresholdsInput.reviewRangeMin` |
| Liveness check | toggle | optional | on | — | — | — | `FaceMatchingVerificationThresholdsInput.livenessCheck` |
| Duplicate-face check | toggle | optional | on | — | — | — | `FaceMatchingVerificationThresholdsInput.duplicateFaceCheck` |
| Image quality | segmented control | optional | Medium | Low · Medium · High | — | Minimum image quality accepted | `FaceMatchingVerificationThresholdsInput.imageQuality` |
| Capture timeout (seconds) | stepper or slider | optional | 10 | min 1; max 60 | — | Seconds | `FaceMatchingVerificationThresholdsInput.captureTimeout` |
| Retries | stepper or slider | optional | 2 | min 0; max 5 | — | — | `FaceMatchingVerificationThresholdsInput.retryQuantity` |
| Mask or obstruction handling | segmented control | optional | Operator review | Deny · Operator review · Fallback method | — | — | `FaceMatchingVerificationThresholdsInput.maskObstructionHandling` |

**Form: Save thresholds** (modal, opened by *Save thresholds*; *Save thresholds* calls `setFaceMatchingVerification`, *Cancel* sends nothing)

**Collects what `setFaceMatchingVerification` sends before it is called.** Required: `venueId`, `accessContext`, `highConfidenceMin`, `reviewRangeMin`. Optional: `profileId`, `retryQuantity`, `livenessCheck`, `duplicateFaceCheck`, `imageQuality`, `captureTimeout`, `maskObstructionHandling`, `operatorFallback`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Profile `profileId` | picker: choose a profile | optional | — | — | shows names, sends the id | Absent creates a threshold profile | `setFaceMatchingVerification` body |
| Venue `venueId` | text field | required | — | — | — | — | `setFaceMatchingVerification` body |
| Access context `accessContext` | text field | required | — | max length 100 | — | Where the thresholds apply, e.g. | `setFaceMatchingVerification` body |
| High confidence min `highConfidenceMin` | stepper or slider | required | — | min 0; max 1 | — | Score at or above which the match is high confidence (allow if every other rule passes) | `setFaceMatchingVerification` body |
| Review range min `reviewRangeMin` | stepper or slider | required | — | min 0; max 1 | — | Score at or above which the match goes to operator review; below it is denied. | `setFaceMatchingVerification` body |
| Retry quantity `retryQuantity` | stepper or slider | optional | 2 | min 0; max 5 | — | — | `setFaceMatchingVerification` body |
| Liveness check `livenessCheck` | toggle | optional | on | — | — | — | `setFaceMatchingVerification` body |
| Duplicate face check `duplicateFaceCheck` | toggle | optional | on | — | — | — | `setFaceMatchingVerification` body |
| Image quality `imageQuality` | segmented control | optional | Medium | Low · Medium · High | — | Minimum image quality accepted | `setFaceMatchingVerification` body |
| Capture timeout `captureTimeout` | stepper or slider | optional | 10 | min 1; max 60 | — | Seconds | `setFaceMatchingVerification` body |
| Mask obstruction handling `maskObstructionHandling` | segmented control | optional | Operator review | Deny · Operator review · Fallback method | — | — | `setFaceMatchingVerification` body |
| Operator fallback `operatorFallback` | toggle | optional | on | — | — | Review-range results go to operator verification | `setFaceMatchingVerification` body |
| Status `status` | segmented control | optional | Active | Active · Inactive | — | Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass) | `setFaceMatchingVerification` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 reviewRangeMin is not below highConfidenceMin

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **highConfidenceMin / reviewRangeMin**: One slider with two handles on 0-100% (stored 0-1); review must be below high confidence, enforced by the handles; band colours green / amber / red with labels Allow / Operator check / Deny. *(source: screens/P08-venue-back-office.yaml#BO-189 / contracts/spine/access.yaml#setFaceMatchingVerification)*
- **accessContext**: Required, e.g. "Main entry", "Child protection exit"; one profile per context. *(source: contracts/spine/access.yaml#setFaceMatchingVerification)*
- **Checks**: Liveness check and Duplicate-face check as toggles (default on); image quality Low/Medium/High (default Medium); capture timeout 1-60 s (default 10); retries 0-5 (default 2); mask/obstruction Deny / Operator review (default) / Fall back to QR or wristband; operator fallback toggle. *(source: contracts/spine/access.yaml#setFaceMatchingVerification)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save thresholds (primary button) | `setFaceMatchingVerification` PUT `/face-matching-verification` | FaceMatchingVerificationThresholdsInput | FaceMatchingVerificationThresholdsView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 reviewRangeMin is not below highConfidenceMin | opens modal first |

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save thresholds**: Whole-profile upsert (VO-R04). *(source: contracts/spine/access.yaml#setFaceMatchingVerification)*

**Data it reads**: `listFaceMatchingVerification` (onLoad, Face Matching & Verification Thresholds)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listFaceMatchingVerification`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The face matching verification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the face matching verification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No face matching verification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 reviewRangeMin is not below highConfidenceMin |

#### Edge cases to draw

- **Face fails at the gate**: Scanner falls back to QR or wristband per DI-641; this screen's mask handling and fallback decide which. *(source: DI-641)*

#### Consistency with other screens

- Match `SCN-003`: The amber "review range" outcome needs an operator-check state on the scanner.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- context: Main entry
  high: 92%
  review: 80%
  liveness: true
  retries: 2
  mask: Operator review
- context: Child protection exit
  high: 96%
  review: 90%
  liveness: true
  retries: 1
  mask: Deny
```

#### Permissions

- `listFaceMatchingVerification` → `SCOPE_VIEW` (read) · staff
- `setFaceMatchingVerification` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-189` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-189`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 10: Works in Face Matching & Verification Thresholds → Configure biometric verification behavior. The source requires a configurable Biometric Check Level determining the scoring of biometric comparison.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-189?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save thresholds.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-190` Face Change, Re-enrollment & Identity Protection

**Prevent guests from replacing a registered biometric identity with another person's face. The source explicitly states that customers may re-register Face Pass, but the system must compare the new facial data with the previous profile. If the difference exceeds an acceptable threshold, the update is blocked and venue assistance is required.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-190 |
| Who uses it | venue staff holding `BIOMETRIC_IMAGE_VIEW`, `GUEST_MANAGE`, `SCOPE_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `attemptId` (navigation) |
| Route | `/access-venue/face-change-re-enrollment-identity-protection-bo-190` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Guards against a guest replacing the face on a credential with someone else's: a re-enrolment is compared with the enrolled face; within policy the update is permitted, a significant difference blocks it and sends it to security or guest service review. This screen is that review queue - existing profile reference, new capture reference, match result, credential, guest, reason, previous changes, operator - with Approve or Block. The one thing to get right: the reviewer decides with evidence and history in front of them, and a block raises a security alert, never silently.

**Known correction pending (do not draw the wrong version)**

- **The pack's identity lock "Maximum self-service re-enrolments, e.g. 1 per 30 days" has no field** Why: Further attempts requiring authorisation cannot be configured. *(source: screens/P08-venue-back-office.yaml#BO-190; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every face change re-enrollment" / "Review face reenrolment"** Why: Generated; "Re-enrolment reviews" and "Review" (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **May the reviewer see the enrolled face and the new capture side by side, or only references and the match result?** → Face re-enrolment review: images behind 'View images (logged)', needing a specific permission; score and references always visible. *(decided by Chinmay, 2026-10-02; DEC-239 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Reason | text area | — | min length 3; max length 300 | `getFaceReenrolmentImages` ?reason |

**Form: Review face reenrolment** (modal, opened by *Review face reenrolment*; *Review face reenrolment* calls `reviewFaceReenrolment`, *Cancel* sends nothing)

**Collects what `reviewFaceReenrolment` sends before it is called.** Required: `decision`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Block | — | — | `reviewFaceReenrolment` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `reviewFaceReenrolment` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `not-pending`: the attempt is not awaiting review.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **decision**: Approve (replaces the enrolled face) or Block (keeps the old one and raises a biometric security alert); two distinct buttons, Block in red. *(source: contracts/spine/access.yaml#reviewFaceReenrolment)*
- **note**: Max 1000 characters; required when blocking (what was checked), optional when approving. *(source: contracts/spine/access.yaml#reviewFaceReenrolment / designer default)*
- **Queue filters**: Outcome (Pending review by default, Updated, Blocked), reason, date; cursor paging (VO-R12). *(source: contracts/spine/access.yaml#/components/schemas/FaceChangeReEnrollmentIdentityProtectionView)*

#### Outputs: what the screen shows and produces

**Shown**

**Every face change re-enrollment** (data table, from `listFaceChangeEnrollment`)

| Shows | Format | Notes |
|---|---|---|
| Existing profile reference | text | Existing profile reference |
| New capture reference | text | New capture reference |
| Match result | chip: Within policy, Significant difference | match result |
| Credential | text | credential |
| Guest | text | guest |
| Reason for re enrollment | chip: Appearance change, Poor original capture, Technical issue, Guest request, Recovery … | reason for re-enrollment |
| Previous changes | 1,234 | previous changes |
| Operator | text | operator |

**The selected face change re-enrollment** (detail panel): The pack groups this record's detail under its own headings: “Current Face”, “SIGNIFICANT IDENTITY DIFFERENCE”, “CHANGE BLOCKED”, “Change Reasons”.

| Shows | Format | Notes |
|---|---|---|
| Existing profile reference | text | Existing profile reference |
| New capture reference | text | New capture reference |
| Match result | chip: Within policy, Significant difference | match result |
| Credential | text | credential |
| Guest | text | guest |
| Reason for re enrollment | chip: Appearance change, Poor original capture, Technical issue, Guest request, Recovery … | reason for re-enrollment |
| Previous changes | 1,234 | previous changes |
| Operator | text | operator |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| View images (logged) (secondary button) | `getFaceReenrolmentImages` GET `/face-reenrolment-attempts/{attemptId}/images` | — | inline | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The attempt is no longer pending review and its … | step-up: mfa (Opens a guest's face images, special-category data under PDPL; every look is logged (DEC-239).) |
| Review face reenrolment (primary button) | `reviewFaceReenrolment` POST `/face-reenrolment-attempts/{attemptId}/review` | inline | AccessFaceReenrolmentAttempt | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Re-enrolment journey**: Current face > New capture > Similarity analysis > Result A "MATCH WITHIN ACCEPTABLE POLICY - Update permitted" or Result B "SIGNIFICANT IDENTITY DIFFERENCE - CHANGE BLOCKED - Security/Guest service review". *(source: screens/P08-venue-back-office.yaml#BO-190)*
- **Review panel**: Existing profile reference and new capture reference (opaque, no template), match result, credential and guest, reason (Appearance change, Poor original capture, Technical issue, Guest request, Recovery, Other), previous changes count with dates, operator, and the audit history of the profile. *(source: screens/P08-venue-back-office.yaml#BO-190 / contracts/spine/access.yaml#/components/schemas/FaceChangeReEnrollmentIdentityProtectionView)*
- **AI fraud signal**: Advisory banner, e.g. "High risk - this credential has attempted three materially different Face Pass registrations within seven days" (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-190)*
- **Images**: The enrolled face and the new capture sit behind "View images (logged)", which needs its own permission; every view is logged. Score and references are always visible. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Approve / Block**: Records the reviewer; Approve sets outcome Updated, Block sets Blocked and raises the alert; an attempt no longer pending shows "Already reviewed by <name>" (409 not-pending). *(source: contracts/spine/access.yaml#reviewFaceReenrolment)*

**Data it reads**: `listFaceChangeEnrollment` (onLoad, Face Change, Re-enrollment & Identity Protection); `getFaceReenrolmentImages` (onLoad, The enrolled and new images, behind a logged view (DEC-239))

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listFaceChangeEnrollment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The face change re-enrollment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the face change re-enrollment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No face change re-enrollment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the face change re-enrollment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The attempt is no longer pending review and its images are purged (`images-purged`).; 409 `not-pending`: the attempt is not awaiting review. |

#### Edge cases to draw

- **Reviewer without guest management rights**: Queue readable, Approve and Block disabled with "Needs guest management rights" (VO-R08). *(source: contracts/spine/access.yaml#reviewFaceReenrolment)*
- **Guest at the gate while review is pending**: The old Face Pass keeps working; the gate falls back to QR or RFID if the face no longer matches. *(source: DI-641)*

#### Consistency with other screens

- Match `BO-189`: The similarity threshold that decides Result A or B is the matching policy there.
- Match `BO-244`: Blocked attempts appear as biometric security alerts on the fraud board.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
attempts:
- attempt: FRA-0192
  guest: Khalid Al Zaabi
  credential: Annual pass AP-10982
  reason: Appearance change
  match: Significant difference
  previousChanges: 2
  operator: Omar Haddad
  outcome: Pending review
  at: 1 Oct 2026 13:20
- attempt: FRA-0187
  guest: Priya Nair
  credential: Annual pass AP-10452
  reason: Poor original capture
  match: Within policy
  outcome: Updated
```

#### Permissions

- `listFaceChangeEnrollment` → `SCOPE_VIEW` (read) · staff
- `reviewFaceReenrolment` → `GUEST_MANAGE` (configure) · staff
- `getFaceReenrolmentImages` → `BIOMETRIC_IMAGE_VIEW` (read) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-190` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-190`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 12: Works in Face Change, Re-enrollment & Identity Protection → Prevent guests from replacing a registered biometric identity with another person's face. The source explicitly states that customers may re-register Face Pass, but the system must compare the new …
- ADR-0063 *Encryption and keys, and biometric templates stay with the biometric vendor* (`docs/adr/0063-encryption-keys-and-biometric-templates.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-190?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: View images (logged), Review face reenrolment.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `BIOMETRIC_IMAGE_VIEW`, `GUEST_MANAGE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-191` Biometric Validation at Gate

**Configure how facial verification interacts with the physical access-control journey.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-191 |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-validation-at-gate-bo-191` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): setBiometricVerificationProfile is the profile write of BO-185 and has no outcome mapping or exit capture; the gate mapping read by listBiometricValidationGate …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Fits face verification into the normal gate journey - guest approaches > camera detects face > face profile resolved > ticket resolved > admission rules evaluated > decision - and maps biometric conditions to the common green / yellow / red gate outcomes: green open gate, yellow operator action (uncertain match, personalised ticket exception, companion verification, eligibility check), red denied (face mismatch, invalid credential, revoked profile, no entitlement). It also switches exit face capture (update journey and exit time). The one thing to get right: the face only identifies; the admission rules still decide, and the result reuses the same gate response.

**Known correction pending (do not draw the wrong version)**

- **conditions is an array of free strings** Why: The conditions need a closed list to drive a gate decision. *(source: contracts/spine/access.yaml#listBiometricValidationGate; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No deny reason for a face mismatch or revoked face profile** Why: DenyReason has neither, so the red outcome cannot be named (VO-R06). *(source: contracts/spine/access.yaml#/components/schemas/DenyReason; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The save is bound to setBiometricVerificationProfile, which has no outcome mapping or exit capture (CHG-WIR-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Outcome mapping**: Rows of biometric condition > outcome (Green / Yellow / Red) > outcome profile picked from BO-198; conditions from a closed list (the pack's examples). *(source: screens/P08-venue-back-office.yaml#BO-191 / contracts/spine/access.yaml#listBiometricValidationGate)*
- **accessPointId**: Gate picker from the tree; empty = all biometric gates of the venue. *(source: contracts/spine/access.yaml#listBiometricValidationGate)*
- **Exit capture**: Three toggles - Exit facial detection, Update guest journey, Update exit time - per exit gate with a camera. *(source: screens/P08-venue-back-office.yaml#BO-192 / contracts/spine/access.yaml#listBiometricValidationGate)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Gate journey**: The six steps as a strip, with "Admission rules decide" highlighted on the fifth. *(source: screens/P08-venue-back-office.yaml#BO-191)*
- **Outcome lanes**: Three columns Green / Yellow / Red listing their conditions, coloured as the gate lights. *(source: screens/P08-venue-back-office.yaml#BO-191)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Should save the mapping and exit capture; no matching write exists (see corrections). *(source: contracts/spine/access.yaml#listBiometricValidationGate)*

**Data it reads**: `listBiometricValidationGate` (onLoad, Biometric Validation at Gate)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listBiometricValidationGate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric validation gate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric validation gate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric validation gate yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the biometric validation gate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Face not matched at the gate**: Falls back to QR or wristband per DI-641; yellow if the match is in the review range (BO-189). *(source: DI-641 / contracts/spine/access.yaml#setFaceMatchingVerification)*
- **Camera unavailable**: Gate falls back to credential-only validation where the profile is Optional; where Required, yellow operator check. *(source: screens/P08-venue-back-office.yaml#BO-193)*

#### Consistency with other screens

- Match `BO-198`: Green / yellow / red outcomes are BO-198's outcome profiles, not a separate biometric response.
- Match `BO-189`: The review range of the thresholds is the yellow uncertain-match condition.
- Match `SCN-003`: Same states on the scanner.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
mapping:
- condition: Match + valid access
  outcome: Green
  profile: Welcome - granted
- condition: Uncertain match
  outcome: Yellow
  profile: Check guest
- condition: Companion verification
  outcome: Yellow
  profile: Verify companion
- condition: Face mismatch
  outcome: Red
  profile: Denied - see staff
exit:
  gate: Main Plaza Exit
  detection: true
  journey: true
  exitTime: true
```

#### Permissions

- `listBiometricValidationGate` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-191` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-191`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 14: Works in Biometric Validation at Gate → Configure how facial verification interacts with the physical access-control journey.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-191?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-192` Biometric Lifecycle, Retention & Deletion

**Manage biometric-data lifecycle and deletion rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_VIEW` (1 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure separately for) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-lifecycle-retention-deletion-bo-192` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Biometric data lifecycle and deletion: Face Pass (Enrolled > Active > Re-enrolled > Suspended > Deletion requested > Deleted) and Face Tag (Captured > Active > Used > Ticket redeemed > Automatically deleted) drawn differently, retention rules per data category (Face Pass, Face Tag, failed enrolment captures, abandoned registrations, temporary captures) with the event that starts the clock, and the Face Pass deletion check. The one thing to get right: the retention period has no default - it is the client counsel's number - and the screen shows the legal limit beside every period.

**Known correction pending (do not draw the wrong version)**

- **Face Pass, Face Tag, Failed enrollment captures and abandoned registrations drawn as four selectFields, and Save has no permission declared** Why: They are rows of one rule table (five categories, temporary captures missing); Save needs ACCESS_POINT_CONFIGURE. *(source: screens/P08-venue-back-office.yaml#BO-192 / contracts/spine/access.yaml#setBiometricLifecycleRetention; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Retention is set per venue here while the 29 September decision makes all data retention tenant configuration, one setting per data class** Why: Two owners for the same period; either the venue rule is bounded by the tenant setting (and says so) or it is removed. *(source: contracts/spine/access.yaml#setBiometricLifecycleRetention / contracts/spine/tenancy.yaml#listDataRetentionSettings / DI-640; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack blocks Face Pass deletion while a Face Pass-verified ticket is active, but revokeFacePass destroys the template whenever the guest withdraws** Why: A guest's withdrawal cannot be refused under PDPL; the pack's block must become "move the ticket to another method, then delete". *(source: screens/P08-venue-back-office.yaml#BO-192 / contracts/spine/access.yaml#revokeFacePass; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Face Pass | select field | — | — | — | — | — | — |
| Face Tag | select field | — | — | — | — | — | — |
| Failed enrollment captures | select field | — | — | — | — | — | — |
| abandoned registrations | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Data class | select | — | Guest profile · Payment record · Financial record · Audit record · Approval record · Compliance inspection · Face tag biometric · Face pass biometric · AI prompts · AI conversations · AI decision records · AI metadata index | `listDataRetentionSettings` ?dataClass |

**Sent by *Save retention rule*** (`setBiometricLifecycleRetention`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policy `policyId` | picker: choose a policy | optional | — | — | shows names, sends the id | Absent creates a retention rule | `setBiometricLifecycleRetention` body |
| Venue `venueId` | text field | required | — | — | — | — | `setBiometricLifecycleRetention` body |
| Data category `dataCategory` | radio group | required | — | Face pass · Face tag · Failed enrollment captures · Abandoned registrations · Temporary captures | — | Biometric data category this rule governs | `setBiometricLifecycleRetention` body |
| Retention days `retentionDays` | number field (days) | required | — | min 0 | — | Maximum retention in days. | `setBiometricLifecycleRetention` body |
| Deletion trigger `deletionTrigger` | select | required | — | Deletion request · Ticket fully redeemed · End of visit · Ticket expiration · Membership ended · Capture failed · Registration abandoned | — | Event that starts the retention clock | `setBiometricLifecycleRetention` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **dataCategory**: One rule per category per venue; the five categories as rows of a table, not five selectFields. *(source: screens/P08-venue-back-office.yaml#BO-193 / contracts/spine/access.yaml#setBiometricLifecycleRetention)*
- **retentionDays**: Required, whole days, minimum 0, empty until entered - no default and no maximum pre-filled; the tenant's legal limit and its basis are shown next to the field from the tenant retention settings. *(source: contracts/spine/access.yaml#setBiometricLifecycleRetention / contracts/spine/tenancy.yaml#listDataRetentionSettings / ADR-0063)*
- **deletionTrigger**: Select of Deletion request, Ticket fully redeemed, End of visit, Ticket expiration, Membership ended, Capture failed, Registration abandoned - filtered to those that make sense for the row (Ticket fully redeemed for Face Tag, Capture failed for failed captures). *(source: contracts/spine/access.yaml#setBiometricLifecycleRetention)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save retention rule (primary button) | `setBiometricLifecycleRetention` PUT `/biometric-lifecycle-retention` | BiometricLifecycleRetentionDeletionInput | BiometricLifecycleRetentionDeletionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A second rule for the same venue and data category; 422 `retentionDays` longer than the tenant's effective … | step-up: mfa (Sets how long biometric data is kept; a wrong value is a data protection breach.) |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lifecycle diagrams**: Face Pass as a persistent profile card chain; Face Tag as a countdown chain ending in an automatic delete icon. *(source: screens/P08-venue-back-office.yaml#BO-192 / screens/P08-venue-back-office.yaml#BO-194)*
- **Deletion check example**: The pack's case - Active credential? YES; Already validated using Face Pass? YES; Result DELETION CURRENTLY BLOCKED with the reason - and the eligible path Delete profile > Remove association > Alternative verification method > Preserve consent record > Record deletion event. *(source: screens/P08-venue-back-office.yaml#BO-192)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save retention rule**: Upsert keyed by policyId (absent creates); step-up authentication on save; confirmation names the category and how many stored items the new period would delete at the next run. *(source: contracts/spine/access.yaml#setBiometricLifecycleRetention)*

**Data it reads**: `listBiometricLifecycleRetention` (onLoad, Biometric Lifecycle, Retention & Deletion); `listDataRetentionSettings` (onLoad, Tenant biometric retention and its legal limit)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listBiometricLifecycleRetention`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric lifecycle retention configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric lifecycle retention untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric lifecycle retention configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A second rule for the same venue and data category; 422 `retentionDays` longer than the tenant's effective `faceTagBiometric` or `facePassBiometric` period (tenancy `setDataRetentionSetting`); a rule here may only … |

#### Edge cases to draw

- **Period entered above the tenant's legal limit**: Refused against the field with the limit and its basis. *(source: contracts/spine/tenancy.yaml#listDataRetentionSettings)*
- **Viewer without configuration rights**: Read-only with "Needs access configuration rights" (VO-R08). *(source: contracts/spine/access.yaml#setBiometricLifecycleRetention)*

#### Consistency with other screens

- Match `BO-188`: Face Tag's deletion trigger there and its retention row here must not disagree; show one from the other.
- Match `BO-187`: Deleting biometric data leaves the consent record.
- Match `GST-069`: Retention wording shown to guests comes from these rules.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- category: Face Pass
  trigger: Membership ended
  days: (counsel to set)
  limit: Tenant limit pending
- category: Face Tag
  trigger: Ticket fully redeemed
  days: 0
- category: Failed enrolment captures
  trigger: Capture failed
  days: (counsel to set)
```

#### Open questions on this screen

Draw the default until it is answered.

- **What are the lawful retention periods per data category and region?** Default: Leave every period empty and required; show "Awaiting counsel" in the limit column. *(source: TRACKER Client Inputs row 49 / TRACKER Actions row 231 / ADR-0063)*

#### Permissions

- `listBiometricLifecycleRetention` → `SCOPE_VIEW` (read) · staff
- `setBiometricLifecycleRetention` → `ACCESS_POINT_CONFIGURE` (configure) · staff · step-up mfa
- `listDataRetentionSettings` → `TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-192` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-192`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 16: Works in Biometric Lifecycle, Retention & Deletion → Manage biometric-data lifecycle and deletion rules.
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-192?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save retention rule.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-193` Biometric Simulation, Audit & Publication

**Test biometric configurations before live deployment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-193 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `AUDIT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-simulation-audit-publication-bo-193` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No operation disables biometrics in an emergency with a fallback method.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Tests biometric configuration before it goes live and audits every biometric event. The manager runs scenarios (valid Face Pass, mismatch, no profile, low confidence, liveness failure, duplicate profile, re-enrolment, child + assigned adult, Face Tag expired or deleted, offline biometric, camera unavailable, fallback) and reads the decision trace; the audit explorer searches by guest, credential, face reference, gate, device, operator, date, result and reason code; publication runs Draft > Test > Privacy/policy validation > Approval > Publish with versioning, scheduled activation, rollback and an emergency disable with fallback. The one thing to get right: simulation rows are visibly simulations and never mixed with real validations.

**Known correction pending (do not draw the wrong version)**

- **Buttons "Low-confidence match" and "Duplicate profile" in the action bar** Why: Scenario values drawn as actions; they are choices of the scenario field. *(source: screens/P08-venue-back-office.yaml#BO-193; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation for emergency disable; approval not bound** Why: The pack requires emergency disable with fallback; the contract lists it as "no operation yet". *(source: contracts/spine/access.yaml#listBiometric; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation exit to BO-184 has no transition** Why: Board screens return to their hub (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-193; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search biometric simulation audit | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by guest, credential, face profile reference, gate, device, operator and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Guest | text field | — | — | `listBiometric` ?guest |
| Credential | text field | — | — | `listBiometric` ?credential |
| Face profile reference | text field | — | — | `listBiometric` ?faceProfileReference |
| Gate | text field | — | — | `listBiometric` ?gate |
| Device | text field | — | — | `listBiometric` ?device |
| Operator | text field | — | — | `listBiometric` ?operator |
| Date | text field | — | — | `listBiometric` ?date |
| Result | text field | — | — | `listBiometric` ?result |
| Reason code | text field | — | — | `listBiometric` ?reasonCode |

**Sent by *Run simulation*** (`simulateBiometricConfiguration`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scenario `scenario` | select | required | — | Valid face pass · Face mismatch · No biometric profile · Low confidence match · Liveness failure · Duplicate profile · Re enrollment attempt · Child assigned adult · Face tag expired · Face tag deleted · Offline biometric · Camera unavailable … | — | — | `simulateBiometricConfiguration` body |
| Venue `venueId` | text field | required | — | — | — | — | `simulateBiometricConfiguration` body |
| Gate group `gateGroupId` | text field | optional | — | — | — | Empty simulates at every gate group of the venue | `simulateBiometricConfiguration` body |
| Credential type `credentialType` | text field | optional | — | — | — | — | `simulateBiometricConfiguration` body |
| Profile `profileId` | text field | optional | — | — | — | The draft biometric verification profile to test; empty tests the published one | `simulateBiometricConfiguration` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **scenario**: Required, chips of the scenarios (the generated "Low-confidence match" and "Duplicate profile" buttons are two of these chips). *(source: screens/P08-venue-back-office.yaml#BO-193 / contracts/spine/access.yaml#simulateBiometricConfiguration)*
- **gateGroupId / credentialType / profileId**: Gate group (empty = every group), credential type, and the draft profile to test (empty = the published one). *(source: contracts/spine/access.yaml#simulateBiometricConfiguration)*
- **Audit search**: The nine search fields as a filter bar; date range defaults to today; cursor paging (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-193 / contracts/spine/access.yaml#listBiometric)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Low-confidence match (primary button) | navigation or local | — | — | — | — |
| Duplicate profile (secondary button) | navigation or local | — | — | — | — |
| Run simulation (primary button) | `simulateBiometricConfiguration` POST `/biometric/simulate` | BiometricSimulationInput | BiometricSimulationAuditPublicationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Simulation result**: "ALLOW ENTRY" or the denial, with the trace - face profile active, verification policy satisfied, match policy satisfied, credential resolved, ticket valid, entitlement valid - as ticks. *(source: screens/P08-venue-back-office.yaml#BO-193 / contracts/spine/access.yaml#/components/schemas/BiometricSimulationAuditPublicationView)*
- **Audit explorer**: Rows with result (Allowed / Review / Denied), reason code, gate, device, operator; simulation rows carry a "Simulation" badge and are filterable out by default. *(source: contracts/spine/access.yaml#listBiometric)*
- **Publication rail**: Draft > Test > Privacy/policy validation > Approval > Publish; scope Tenant, Venue, Park, Credential type, Gate group; Emergency disable separated and red. *(source: screens/P08-venue-back-office.yaml#BO-193)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Run simulation**: Returns the decision; written to the audit trail as a simulation; no guest, gate or credential touched. *(source: contracts/spine/access.yaml#simulateBiometricConfiguration)*
- **Submit for approval / Publish**: Through the approvals engine; publishing is the profile's activation. *(source: contracts/spine/approvals.yaml#createApprovalRequest / contracts/spine/access.yaml#simulateBiometricConfiguration)*
- **Emergency disable biometric verification**: Typed confirmation naming the fallback ("Face gates fall back to QR and wristband at 12 gates"), reason required (VO-R16); not yet backed by an operation. *(source: contracts/spine/access.yaml#listBiometric)*

**Data it reads**: `listBiometric` (onLoad, Biometric Simulation, Audit & Publication)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric simulation audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric simulation audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric simulation audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the biometric simulation audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Viewer with configuration rights but no audit rights**: Simulation available; the audit explorer says "Needs audit view rights" (VO-R08). *(source: contracts/spine/access.yaml#listBiometric)*

#### Consistency with other screens

- Match `BO-173`: Same trace and publication layout as the credential security simulation.
- Match `BO-184`: Command centre tiles exclude simulation rows.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
simulation:
  scenario: Valid Face Pass
  credential: Annual Pass AP-10742
  gate: Main Plaza Gate 4
  result: ALLOW ENTRY
  trace: Face profile active; Verification policy satisfied; Match policy satisfied; Credential resolved; Ticket
    valid; Entitlement valid
audit:
- time: 1 Oct 2026 10:03
  guest: Sara Al Nuaimi
  gate: Main Plaza Gate 4
  result: Allowed
  simulation: false
- time: 1 Oct 2026 10:05
  scenario: Liveness failure
  result: Denied
  reason: liveness
  simulation: true
```

#### Permissions

- `listBiometric` → `AUDIT_VIEW` (read) · staff
- `simulateBiometricConfiguration` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-193` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-193`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 18: Works in Biometric Simulation, Audit & Publication → Test biometric configurations before live deployment.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-193?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Low-confidence match, Duplicate profile, Run simulation.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `AUDIT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getBiometricVerificationProfile": {"method":"GET","path":"/biometric-verification-profile","contract":"access","summary":"The biometric verification profile as saved","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BiometricVerificationProfileBuilderView"},
"getFacePassEnrollmentConfiguration": {"method":"GET","path":"/face-pass-enrollment","contract":"access","summary":"The FacePass enrolment configuration as saved","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"FacePassEnrollmentConfigurationView"},
"getFaceReenrolmentImages": {"method":"GET","path":"/face-reenrolment-attempts/{attemptId}/images","contract":"access","summary":"View the images behind a face re-enrolment review (logged)","permission":"BIOMETRIC_IMAGE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"reason","in":"query","required":true}],"requestBody":null,"responds":null},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listBiometric": {"method":"GET","path":"/biometric","contract":"access","summary":"Biometric Simulation, Audit & Publication","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"guest","in":"query","required":false},{"name":"credential","in":"query","required":false},{"name":"faceProfileReference","in":"query","required":false},{"name":"gate","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"operator","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"result","in":"query","required":false},{"name":"reasonCode","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBiometricAccess": {"method":"GET","path":"/biometric-access","contract":"access","summary":"Biometric Access Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBiometricConsentGuardian": {"method":"GET","path":"/biometric-consent-guardian","contract":"access","summary":"Biometric Consent & Guardian Management","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"countryJurisdiction","in":"query","required":false},{"name":"tenantId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"credentialType","in":"query","required":false},{"name":"enrollmentChannel","in":"query","required":false},{"name":"guestCategory","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBiometricLifecycleRetention": {"method":"GET","path":"/biometric-lifecycle-retention","contract":"access","summary":"Biometric Lifecycle, Retention & Deletion","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BiometricLifecycleRetentionDeletionView"},
"listBiometricValidationGate": {"method":"GET","path":"/biometric-validation-gate","contract":"access","summary":"Biometric Validation at Gate","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BiometricValidationAtGateView"},
"listDataRetentionSettings": {"method":"GET","path":"/data-retention-settings","contract":"tenancy","summary":"How long the tenant keeps each class of data","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"dataClass","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFaceChangeEnrollment": {"method":"GET","path":"/face-change-enrollment","contract":"access","summary":"Face Change, Re-enrollment & Identity Protection","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFaceMatchingVerification": {"method":"GET","path":"/face-matching-verification","contract":"access","summary":"Face Matching & Verification Thresholds","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FaceMatchingVerificationThresholdsView"},
"listFaceTagTemporary": {"method":"GET","path":"/face-tag-temporary","contract":"access","summary":"Face Tag Temporary Enrollment","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FaceTagTemporaryEnrollmentView"},
"reviewFaceReenrolment": {"method":"POST","path":"/face-reenrolment-attempts/{attemptId}/review","contract":"access","summary":"Review a blocked Face Pass re-enrolment","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessFaceReenrolmentAttempt"},
"setBiometricLifecycleRetention": {"method":"PUT","path":"/biometric-lifecycle-retention","contract":"access","summary":"Save a biometric retention rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BiometricLifecycleRetentionDeletionInput","responds":"BiometricLifecycleRetentionDeletionView"},
"setBiometricVerificationProfile": {"method":"PUT","path":"/biometric-verification-profile","contract":"access","summary":"Biometric Verification Profile Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BiometricVerificationProfileBuilderInput","responds":"BiometricVerificationProfileBuilderView"},
"setFaceMatchingVerification": {"method":"PUT","path":"/face-matching-verification","contract":"access","summary":"Save face matching and verification thresholds","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FaceMatchingVerificationThresholdsInput","responds":"FaceMatchingVerificationThresholdsView"},
"setFacePassEnrollment": {"method":"PUT","path":"/face-pass-enrollment","contract":"access","summary":"Face Pass Enrollment Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FacePassEnrollmentConfigurationInput","responds":"FacePassEnrollmentConfigurationView"},
"setFaceTagTemporaryEnrollment": {"method":"PUT","path":"/face-tag-temporary","contract":"access","summary":"Save a Face Tag profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FaceTagTemporaryEnrollmentInput","responds":"FaceTagTemporaryEnrollmentView"},
"setVenueSettings": {"method":"PUT","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Set support hours, quiet hours, segregated access and alerting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"simulateBiometricConfiguration": {"method":"POST","path":"/biometric/simulate","contract":"access","summary":"Run a biometric scenario before publishing","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BiometricSimulationInput","responds":"BiometricSimulationAuditPublicationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessFaceReenrolmentAttempt": {"type":"object","x-ticvai-persistence":"access.face_reenrolment_attempt","description":"One Face Pass re-enrolment attempt - the existing and new capture references (opaque, never templates), the match result, the reason, the operator and the outcome, with the review of a blocked change (declared 29 September, data-model close-out DM1). Written by enrolFacePass when the subject already has a Face Pass; a pendingReview attempt is decided by reviewFaceReenrolment (decided 29 September, writers pass).","required":["id","venueId","scopePath","subjectId","existingProfileReference","newCaptureReference","matchResult","outcome","attemptedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The attemptId the list shows"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"subjectId":{"type":"string","format":"uuid","description":"The guest (pii.subject)"},"entitlementId":{"type":"string","format":"uuid","nullable":true,"description":"The credential the Face Pass belongs to"},"existingProfileReference":{"type":"string","maxLength":200,"description":"Opaque reference to the prior enrolment (pii.subject_biometric)"},"newCaptureReference":{"type":"string","maxLength":200,"description":"Opaque reference to the new capture"},"matchResult":{"type":"string","enum":["withinPolicy","significantDifference"]},"reasonForReEnrollment":{"type":"string","enum":["appearanceChange","poorOriginalCapture","technicalIssue","guestRequest","recovery","other"],"nullable":true},"verificationProcess":{"type":"string","maxLength":200,"nullable":true,"description":"How the guest was verified for the change"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"outcome":{"type":"string","enum":["updated","blocked","pendingReview"]},"reviewedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Security or guest service reviewer of a blocked change (the integrity screen's approval)"},"reviewedAt":{"type":"string","format":"date-time","nullable":true},"attemptedAt":{"type":"string","format":"date-time"}}},
"BiometricAccessCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Access Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"profileId":{"type":"string"},"profileName":{"type":"string","description":"e.g. Annual Pass Face"},"biometricType":{"type":"string","enum":["facePass","faceTag"]},"credentialType":{"type":"string","description":"e.g. Annual Pass, Membership, Day Ticket"},"venueScope":{"type":"string","description":"Venue or 'all parks'"},"status":{"type":"string","enum":["active","inactive"]}}},
"BiometricAccessCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeFacePassProfiles":{"type":"integer","description":"Active Face Pass Profiles"},"activeFaceTags":{"type":"integer","description":"Active Face Tags"},"enrollmentsToday":{"type":"integer","description":"Enrollments Today"},"successfulFaceVerifications":{"type":"integer","description":"Successful Face Verifications"},"failedVerifications":{"type":"integer","description":"Failed Verifications"},"manualReviews":{"type":"integer","description":"Manual Reviews"},"reEnrollmentRequests":{"type":"integer","description":"Re-enrollment Requests"},"blockedFaceChanges":{"type":"integer","description":"Blocked Face Changes"},"profilesPendingDeletion":{"type":"integer","description":"Profiles Pending Deletion"},"cameraReaderHealth":{"type":"string","enum":["healthy","degraded","down"],"description":"Camera/Reader Health"},"biometricSecurityAlerts":{"type":"integer","description":"Biometric Security Alerts"},"ai":{"type":"array","items":{"type":"string"},"description":"Advisory AI findings (abnormal failure rates, suspicious re-enrolments, camera quality). Read-only; AI does not decide access."}}},
"BiometricConsentGuardianManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Consent & Guardian Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue"},"consentRecordId":{"type":"string","description":"Consent record ID"},"policyVersion":{"type":"string","description":"Policy/version"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"channel":{"type":"string","description":"Channel"},"guardianReference":{"type":"string","description":"Guardian reference where applicable"},"operatorId":{"type":"string","description":"Operator where applicable"},"withdrawalDeletionStatus":{"type":"string","enum":["active","withdrawn","biometricDeleted"],"description":"withdrawal/deletion status"},"guestId":{"type":"string"}}},
"BiometricLifecycleRetentionDeletionInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Biometric Lifecycle, Retention & Deletion submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["venueId","dataCategory","retentionDays","deletionTrigger"],"properties":{"policyId":{"type":"string","format":"uuid","description":"Absent creates a retention rule"},"venueId":{"type":"string"},"dataCategory":{"type":"string","enum":["facePass","faceTag","failedEnrollmentCaptures","abandonedRegistrations","temporaryCaptures"],"description":"Biometric data category this rule governs"},"retentionDays":{"type":"integer","minimum":0,"description":"Maximum retention in days. **No default and no maximum here on purpose**: the lawful period per region is the client counsel's value (make-or-break (a), see the operation)"},"deletionTrigger":{"type":"string","enum":["deletionRequest","ticketFullyRedeemed","endOfVisit","ticketExpiration","membershipEnded","captureFailed","registrationAbandoned"],"description":"Event that starts the retention clock"}}},
"BiometricLifecycleRetentionDeletionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Lifecycle, Retention & Deletion displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dataCategory":{"type":"string","enum":["facePass","faceTag","failedEnrollmentCaptures","abandonedRegistrations","temporaryCaptures"],"description":"Biometric data category this retention rule governs"},"policyId":{"type":"string"},"venueId":{"type":"string"},"retentionDays":{"type":"integer","description":"Maximum retention in days; value set per region once confirmed. No default (make-or-break (a), see `setBiometricLifecycleRetention`)"},"deletionTrigger":{"type":"string","enum":["deletionRequest","ticketFullyRedeemed","endOfVisit","ticketExpiration","membershipEnded","captureFailed","registrationAbandoned"],"description":"Event that starts the retention clock (decided 29 September, VM close-out)"}}},
"BiometricSimulationAuditPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Simulation, Audit & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"scenario":{"type":"string","enum":["validFacePass","faceMismatch","noBiometricProfile","lowConfidenceMatch","livenessFailure","duplicateProfile","reEnrollmentAttempt","childAssignedAdult","faceTagExpired","faceTagDeleted","offlineBiometric","cameraUnavailable","alternativeVerificationFallback"],"description":"Simulated scenario (simulation rows only)"},"eventId":{"type":"string"},"occurredAt":{"type":"string","format":"date-time"},"isSimulation":{"type":"boolean"},"guestId":{"type":"string"},"credentialId":{"type":"string"},"faceProfileReference":{"type":"string"},"gateId":{"type":"string"},"deviceId":{"type":"string"},"operatorId":{"type":"string"},"result":{"type":"string","enum":["allowed","review","denied"]},"reasonCode":{"type":"string"},"decisionTrace":{"type":"array","items":{"type":"string"},"description":"Checks passed or failed, e.g. face profile active, match policy satisfied, ticket valid"}}},
"BiometricSimulationInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"One simulated biometric validation, run before a biometric profile is published (decided 29 September, VM close-out).","required":["scenario","venueId"],"properties":{"scenario":{"type":"string","enum":["validFacePass","faceMismatch","noBiometricProfile","lowConfidenceMatch","livenessFailure","duplicateProfile","reEnrollmentAttempt","childAssignedAdult","faceTagExpired","faceTagDeleted","offlineBiometric","cameraUnavailable","alternativeVerificationFallback"]},"venueId":{"type":"string"},"gateGroupId":{"type":"string","description":"Empty simulates at every gate group of the venue"},"credentialType":{"type":"string"},"profileId":{"type":"string","description":"The draft biometric verification profile to test; empty tests the published one"}}},
"BiometricValidationAtGateView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Validation at Gate displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"accessPointId":{"type":"string"},"outcome":{"type":"string","enum":["green","yellow","red"]},"conditions":{"type":"array","items":{"type":"string"},"description":"Conditions that give this outcome, e.g. uncertain match, face mismatch, revoked profile"},"outcomeProfileId":{"type":"string","description":"Gate response profile from the validation outcome designer"},"exitCaptureEnabled":{"type":"boolean","description":"Face capture at exit records exit time"}}},
"BiometricVerificationProfileBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Biometric Verification Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"faceRequirement":{"type":"string","enum":["notUsed","optional","required"],"description":"Whether face verification is not used, allowed, or required at this location (e.g. main entry required, attractions credential only)"},"biometricType":{"type":"string","enum":["facePass","faceTag","otherProvider"],"description":"Biometric model this profile uses"},"profileId":{"type":"string","description":"The profile row's key (access.biometric_profile.id, a UUIDv7); absent creates one (decided 29 September, writers pass)","format":"uuid"},"selectType":{"type":"string","enum":["ticketProduct","ticketType","membership","annualPass","multiDayTicket","multiAttractionTicket","vipCredential","accreditation","selectedCustomerSegments"],"description":"Vocabulary listed under Select."},"venueId":{"type":"string","description":"Venue"},"parkId":{"type":"string","description":"Park"},"zoneId":{"type":"string","description":"Zone"},"attractionId":{"type":"string","description":"Attraction"},"gateId":{"type":"string","description":"Gate"},"name":{"type":"string"},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass)"}},"required":["profileId","venueId","selectType","biometricType","faceRequirement"]},
"BiometricVerificationProfileBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Verification Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"faceRequirement":{"type":"string","enum":["notUsed","optional","required"],"description":"Whether face verification is not used, allowed, or required at this location (e.g. main entry required, attractions credential only)"},"biometricType":{"type":"string","enum":["facePass","faceTag","otherProvider"],"description":"Biometric model this profile uses"},"profileId":{"type":"string","description":"Biometric verification profile identifier"},"selectType":{"type":"string","enum":["ticketProduct","ticketType","membership","annualPass","multiDayTicket","multiAttractionTicket","vipCredential","accreditation","selectedCustomerSegments"],"description":"Vocabulary listed under Select."},"venueId":{"type":"string","description":"Venue"},"parkId":{"type":"string","description":"Park"},"zoneId":{"type":"string","description":"Zone"},"attractionId":{"type":"string","description":"Attraction"},"gateId":{"type":"string","description":"Gate"},"name":{"type":"string"}},"required":["profileId","venueId","selectType","biometricType","faceRequirement"]},
"FaceChangeReEnrollmentIdentityProtectionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Face Change, Re-enrollment & Identity Protection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"existingProfileReference":{"type":"string","description":"Existing profile reference"},"newCaptureReference":{"type":"string","description":"New capture reference"},"matchResult":{"type":"string","enum":["withinPolicy","significantDifference"],"description":"match result"},"credentialId":{"type":"string","description":"credential"},"guestId":{"type":"string","description":"guest"},"reasonForReEnrollment":{"type":"string","enum":["appearanceChange","poorOriginalCapture","technicalIssue","guestRequest","recovery","other"],"description":"reason for re-enrollment"},"previousChanges":{"type":"integer","description":"previous changes"},"operatorId":{"type":"string","description":"operator"},"attemptId":{"type":"string"},"attemptedAt":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["updated","blocked","pendingReview"]}}},
"FaceMatchingVerificationThresholdsInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Face Matching & Verification Thresholds submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back. Proposed defaults are ours (our build plan); the scores are a 0-1 scale whatever the face vendor reports, normalised by the adapter (R077).","required":["venueId","accessContext","highConfidenceMin","reviewRangeMin"],"properties":{"profileId":{"type":"string","format":"uuid","description":"Absent creates a threshold profile"},"venueId":{"type":"string"},"accessContext":{"type":"string","maxLength":100,"description":"Where the thresholds apply, e.g. main entry, child protection"},"highConfidenceMin":{"type":"number","minimum":0,"maximum":1,"description":"Score at or above which the match is high confidence (allow if every other rule passes)"},"reviewRangeMin":{"type":"number","minimum":0,"maximum":1,"description":"Score at or above which the match goes to operator review; below it is denied. Must be below highConfidenceMin"},"retryQuantity":{"type":"integer","minimum":0,"maximum":5,"default":2},"livenessCheck":{"type":"boolean","default":true},"duplicateFaceCheck":{"type":"boolean","default":true},"imageQuality":{"type":"string","enum":["low","medium","high"],"default":"medium","description":"Minimum image quality accepted"},"captureTimeout":{"type":"integer","minimum":1,"maximum":60,"default":10,"description":"Seconds"},"maskObstructionHandling":{"type":"string","enum":["deny","operatorReview","fallbackMethod"],"default":"operatorReview"},"operatorFallback":{"type":"boolean","default":true,"description":"Review-range results go to operator verification"},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass)"}}},
"FaceMatchingVerificationThresholdsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Face Matching & Verification Thresholds displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"livenessCheck":{"type":"boolean","description":"Liveness check"},"duplicateFaceCheck":{"type":"boolean","description":"Duplicate-face check"},"imageQuality":{"type":"string","enum":["low","medium","high"],"description":"Minimum image quality accepted (decided 29 September, VM close-out)"},"captureTimeout":{"type":"integer","description":"Seconds"},"maskObstructionHandling":{"type":"string","enum":["deny","operatorReview","fallbackMethod"],"description":"What a masked or obstructed face leads to (decided 29 September, VM close-out)"},"operatorFallback":{"type":"boolean","description":"Review-range results go to operator verification"},"profileId":{"type":"string"},"venueId":{"type":"string"},"accessContext":{"type":"string","description":"Where the thresholds apply, e.g. main entry, child protection"},"highConfidenceMin":{"type":"number","description":"Score at or above which the match is high confidence (allow if all other rules pass)"},"reviewRangeMin":{"type":"number","description":"Score at or above which the match goes to operator review; below it is denied"},"retryQuantity":{"type":"integer"}}},
"FacePassEnrollmentConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Face Pass Enrollment Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"venueId":{"type":"string","description":"Venue this enrolment configuration applies to"},"enrollmentChannels":{"type":"array","items":{"type":"string","enum":["ticvaiApp","ticketCounter","annualPassCounter","selfServiceKiosk","otherAuthorizedChannel"]},"description":"Channels where Face Pass enrolment is enabled. **The app, the staffed counters and a self-service kiosk that shows the consent form; never the turnstile** (decided 2 October 2026, Chinmay, critical set 1, BO-186; DEC-236; CHG-CSP-021). There is no gate or turnstile value, and `otherAuthorizedChannel` cannot name one."},"accountLoginRequired":{"type":"boolean","description":"Account login required"},"validTicketPassRequired":{"type":"boolean","description":"Valid ticket/pass required"},"identityCheckRequired":{"type":"boolean","description":"Identity check required"},"numberOfCaptureAttempts":{"type":"integer","description":"Number of capture attempts"},"minimumImageQuality":{"type":"string","description":"minimum image quality"},"operatorVerification":{"type":"boolean","description":"An operator must verify the capture"},"enrollmentExpiry":{"type":"integer","description":"Days an enrolment stays valid before re-enrolment is needed"},"duplicateFaceDetection":{"type":"boolean","description":"Block a face already associated with another annual pass"},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass)"}},"required":["venueId"]},
"FacePassEnrollmentConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Face Pass Enrollment Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue this enrolment configuration applies to"},"enrollmentChannels":{"type":"array","items":{"type":"string","enum":["ticvaiApp","ticketCounter","annualPassCounter","selfServiceKiosk","otherAuthorizedChannel"]},"description":"Channels where Face Pass enrolment is enabled. **The app, the staffed counters and a self-service kiosk that shows the consent form; never the turnstile** (decided 2 October 2026, Chinmay, critical set 1, BO-186; DEC-236; CHG-CSP-021). There is no gate or turnstile value, and `otherAuthorizedChannel` cannot name one."},"accountLoginRequired":{"type":"boolean","description":"Account login required"},"validTicketPassRequired":{"type":"boolean","description":"Valid ticket/pass required"},"identityCheckRequired":{"type":"boolean","description":"Identity check required"},"numberOfCaptureAttempts":{"type":"integer","description":"Number of capture attempts"},"minimumImageQuality":{"type":"string","description":"minimum image quality"},"operatorVerification":{"type":"boolean","description":"An operator must verify the capture"},"enrollmentExpiry":{"type":"integer","description":"Days an enrolment stays valid before re-enrolment is needed"},"duplicateFaceDetection":{"type":"boolean","description":"Block a face already associated with another annual pass"}},"required":["venueId"]},
"FaceTagTemporaryEnrollmentInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Face Tag Temporary Enrollment submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["venueId","name","enrollmentChannels","bindTo","deletionTrigger"],"properties":{"profileId":{"type":"string","format":"uuid","description":"Absent creates a Face Tag profile"},"venueId":{"type":"string"},"name":{"type":"string","maxLength":200},"enrollmentChannels":{"type":"array","items":{"type":"string","enum":["ticketCounter","entryGate"]},"minItems":1,"description":"Where a Face Tag may be captured"},"bindTo":{"type":"string","enum":["ticket","visit","temporaryCredential"],"default":"ticket","description":"What the Face Tag is bound to"},"deletionTrigger":{"type":"string","enum":["ticketFullyRedeemed","endOfVisit","ticketExpiration","credentialCancellation","operationalRetentionThreshold"],"default":"ticketFullyRedeemed","description":"When the Face Tag is deleted automatically. The matrix: deleted once the ticket is fully redeemed"},"retentionThresholdHours":{"type":"integer","minimum":1,"description":"Used only when deletionTrigger is operationalRetentionThreshold, and then required. **No default and no maximum here on purpose**: the longest lawful period is the client counsel's value (make-or-break (a), see the operation)"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form a Face Tag is captured on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"consent first, using a consent form from the venue\"; DEC-128, DEC-549; CHG-CSP-018). Null uses the venue's biometric consent form (`tenancy.VenueSettings.biometrics.consentFormId`); either way the form comes from the one consent-form builder in Venue Management. With neither, the profile is refused `422 consent-form-required`."},"consentCapture":{"type":"string","enum":["onScreenAcknowledgement","signedForm"],"default":"onScreenAcknowledgement","description":"How consent is taken when a Face Tag is captured (3.2.44; added 29 September, build pass). `onScreenAcknowledgement` is a tap on the counter or gate screen after the notice: explicit, recorded, and no form to sign, which is what the matrix asks. `signedForm` for a venue that wants one. A notice-only capture is not offered (make-or-break on `enrolFaceTag`, CF-35)."},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass)"}}},
"FaceTagTemporaryEnrollmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Face Tag Temporary Enrollment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**Where TICVAI stores the Face Tag templates, the screen warns the venue** that every guest must accept the venue's consent form before capture (decided 2 October 2026, Chinmay, batch 4, BO-188; DEC-128; CHG-CSP-018). Read from `tenancy.VenueSettings.biometrics.templatesHeldByTicvai`."},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"The venue's consent form this profile captures on (DEC-128; CHG-CSP-018)."},"enrollmentChannels":{"type":"array","items":{"type":"string","enum":["ticketCounter","entryGate"]},"description":"Where a Face Tag may be captured"},"bindTo":{"type":"string","enum":["ticket","visit","temporaryCredential"],"description":"What the Face Tag is bound to"},"deletionTrigger":{"type":"string","enum":["ticketFullyRedeemed","endOfVisit","ticketExpiration","credentialCancellation","operationalRetentionThreshold"],"description":"When the Face Tag is automatically deleted; default ticketFullyRedeemed"},"profileId":{"type":"string"},"venueId":{"type":"string"},"name":{"type":"string"},"retentionThresholdHours":{"type":"integer","description":"Used when deletionTrigger is operationalRetentionThreshold. No default (make-or-break (a), see `setFaceTagTemporaryEnrollment`)"},"consentCapture":{"type":"string","enum":["onScreenAcknowledgement","signedForm"],"description":"How consent is taken at capture; onScreenAcknowledgement (no form to sign) unless set"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"TenantDataRetentionClass": {"type":"string","description":"**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n","enum":["guestProfile","paymentRecord","financialRecord","auditRecord","approvalRecord","complianceInspection","faceTagBiometric","facePassBiometric","aiPrompts","aiConversations","aiDecisionRecords","aiMetadataIndex"]},
"TenantDataRetentionSetting": {"type":"object","x-ticvai-persistence":"tenancy.data_retention_setting","description":"**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n","required":["dataClass"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"x-ticvai-unique":"tenant","description":"One row per class per tenant. On a write it comes from the path; a body value is ignored."},"retainAmount":{"type":"integer","nullable":true,"minimum":0,"description":"The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"},"retainUnit":{"type":"string","nullable":true,"enum":["days","months","years"],"description":"Required with `retainAmount`."},"followsDataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"nullable":true,"description":"Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"},"onExpiry":{"type":"string","enum":["archive","anonymise","delete"],"default":"archive","description":"ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"},"anchor":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["createdAt","lastActivity","decidedAt","ticketExpiry"],"description":"What the period is counted from. Fixed per class by the platform."},"effectiveAmount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"The period actually applied, after follows and defaults are resolved."},"effectiveUnit":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"isDefault":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"True when the tenant has not set this class and the platform default applies."},"defaultAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false},"defaultUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalMinimumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A floor the law sets. A shorter period is refused (`422`)."},"legalMaximumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."},"legalLimitUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalBasis":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"The law or requirement the limit comes from, e.g. `4.3.4`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The tenant. Retention is set at tenant scope only."}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form, which every biometric capture is taken on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"Consent first, on the venue's consent form\"; DEC-128, DEC-549; CHG-CSP-018). A form from the venue's consent-form builder in Venue Management (the one builder Face Pass, Face Tag, marketing and waivers share; marketing-crm `setDigitalWaiverForm`). Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access `enrolFacePass`, `enrolFaceTag`).\n"},"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**True where TICVAI's platform stores this venue's biometric templates** (rather than the venue's own on-premises reader estate). Derived from the venue's access deployment. While true, Venue Management shows the venue a standing warning that every guest must accept the venue's consent form before capture, because the data sits with TICVAI as the venue's processor (decided 2 October 2026, Chinmay, batch 4, BO-188: \"If we store the data, highlight or notify the venue that the client must accept a consent form\"; DEC-128; CHG-CSP-018).\n"},"allowMinors":{"type":"boolean","default":true,"description":"**Whether this venue enrols minors at all** (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: \"Guardian consent on the venue's form; minor age per country; the venue can switch minors off\"; supersedes the GST-069 default; DEC-237; CHG-CSP-019). On: a minor (below `RegionSettings.minorAgeThreshold`) is enrolled only with a guardian's consent on the venue's consent form. Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method.\n"},"accreditationFaceMatching":{"type":"object","nullable":true,"description":"**Face matching to find duplicate accreditation applicants, off unless the venue enables it** (decided 2 October 2026, Chinmay, critical set 3, BO-631: \"Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default\"; DEC-461; CHG-CSP-022). Enabling it is refused without `legalSignOffReference` (`422 legal-sign-off-required`); each applicant matched must have consented on the application (accreditation's own record). Null is off.\n","properties":{"isEnabled":{"type":"boolean","default":false},"legalSignOffReference":{"type":"string","nullable":true,"maxLength":200,"description":"The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"chargeCurrencies":{"type":"array","nullable":true,"description":"**Which currencies a guest may select and pay in** (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). A subset of `displayCurrencies`: each code must also be one the venue's payment provider can charge (`orders.PaymentProvider.presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. Null or empty: guests pay in the trading (base) currency only and the other display currencies stay approximate. The ledger is always in the base currency, with the rate recorded on every payment and refund.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).** The client's policy of 6 October 2026 (tracker answer T10.1, `sources/client/2026-10-06-tracker-answers.md`; CHG-R4-019): the tolerance is configurable, a difference within it closes only with a reason (`shift.giveShiftVarianceReason`), and beyond it needs supervisor or manager approval (OVERSHORT_ACCEPT).\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The most cash a till drawer should hold before some is lifted to the safe** (decided 2 October 2026, Chinmay, batch 6 set 3, BO-042: \"Add drawer limit setting (warn + offer cash lift)\"; DEC-179; CHG-CSP-016; DI-274: on a busy day the cashier unloads excess cash mid-shift and it is reconciled at close). The venue default; a till may set its own (`Workstation.cashDrawerLimit`). When the cash a till has taken since its last count takes the drawer over it, the till warns and offers a cash lift (`shift.createCashMovement` kind `lift`) and BO-042 flags the box (`shift.DepositBox.overDrawerLimit`). A warning, never a block: a sale is not refused because the drawer is full. Null sets no limit. **No proposed default: the client's finance team sets it.**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"tableReservedLeadMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":240,"default":30,"deprecated":true,"description":"**Deprecated (2 October 2026, CHG-CLN-009): `fnb.FnbReservationPolicy.reservedLeadMinutes` is canonical.** The table state model reads the reservation policy (`states/table.yaml`); this venue setting is kept for compatibility, never read, and not drawn. Its former meaning: **How long before a pre-allocated booking its table shows Reserved** (decided 2 October 2026, Chinmay, batch 6 set 6b, EMP-052: \"Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking\"; DEC-202; CHG-CSP-017; DI-689, DI-336). A booking that names its table holds it as Reserved for the booking's whole slot; a booking the host pre-allocated shows its table Reserved from this many minutes before it. Zero shows Reserved only once the booking is due. The fnb table state model applies it (`states/table.yaml`, owned by fnb). Proposed default 30 minutes, client to correct.\n"},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}}
}
```
