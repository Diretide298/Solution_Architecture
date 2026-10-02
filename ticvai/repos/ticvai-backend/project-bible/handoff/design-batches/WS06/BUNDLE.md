# WS06 — Access Control board 6

**10 screens · 19 operations · 34 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, DEVICE_CONFIGURE, DEVICE_MANAGE, DEVICE_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-194` | Device & Gate Command Center | B–D | 0 | 294 | 6 | 0 | 6 | 0 | — | notStarted (generated) |
| `BO-195` | Device Type & Hardware Library | B–D | 15 | 0 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-196` | Physical Device Registration & Provisioning | B–D | 74 | 0 | 5 | 45 | 5 | 0 | — | notStarted (generated) |
| `BO-197` | Turnstile & Lane Behavior Configuration | B–D | 14 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-198` | Validation Outcome & Guest Feedback Designer | B–D | 11 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-199` | Reader, Scanner & Peripheral Configuration | B–D | 1 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-200` | Handheld & Mobile Access Device Configuration | B–D | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-201` | Gate Modes, Free Spin & Emergency Controls | A | 15 | 0 | 5 | 0 | 1 | 2 | — | notStarted (generated) |
| `BO-202` | Device Software, Content & Remote Configuration | B–D | 6 | 0 | 5 | 0 | 4 | 0 | — | notStarted (generated) |
| `BO-203` | Hardware Compatibility, Health, Testing & Deployment | B–D | 10 | 0 | 6 | 0 | 8 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-195, BO-199 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-194` Device & Gate Command Center

**Provide the central operational/configuration view of the complete access-control hardware estate.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_VIEW`, `SCOPE_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `accessPointId` (navigation), `deviceId` (navigation), `placementId` (navigation) |
| Route | `/access-venue/device-gate-command-center-bo-194` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The command centre monitors (VO-R02): placement and registration belong to BO-196, gate mode changes to the gate mode screens (BO-201, SCN-016) (design-notes … Removed 2 October 2026 (CHG-WIR-001): The command centre monitors (VO-R02): placement and registration belong to BO-196, gate mode changes to the gate mode screens (BO-201, SCN-016) (design-notes … Removed 2 October 2026 (CHG-WIR-001): The command centre monitors (VO-R02): placement and registration belong to BO-196, gate mode changes to the gate mode screens (BO-201, SCN-016) (design-notes …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The hub of board 6 (devices, turnstiles and gates): every access-control device - turnstiles, VIP and accessible gates, handhelds, readers, cameras, podiums, beacons - with its live state (online, degraded, local mode), the configuration, rule and security package versions it runs, and component health. Thirteen KPI tiles, the pack's device directory (MG-01 Turnstile, Main Gate, Entry, Online, Healthy ... AT-07 Reader, Coaster, Fast Pass, Offline, Local Mode), AI findings and tiles into the nine device screens. The one thing to get right: a device that is behind on its configuration or rule package is as visible as one that is offline.

**Known correction pending (do not draw the wrong version)**

- **A metric tile labelled "Ai" and a table "Every device gate" with only the seven health columns** Why: AI findings are a list, not a number; the directory needs Device, Type, Access point, Mode and Status from the read (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-194 / contracts/spine/access.yaml#/components/schemas/DeviceGateCommandCenterView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The command centre's primary action is "Save access device" (updateAccessDevicePlacement), and registerDevice and setTurnstileMode are … (CHG-WIR-001); Device status vocabulary here (healthy, active, degraded, offline, localMode) differs from the device register's status and health enums (CHG-WIR-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Devices** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Online** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Offline** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Degraded** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Turnstiles** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Handhelds** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Biometric Readers** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**RFID/NFC Readers** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Gates Open** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Gates Closed** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Devices Requiring Sync** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Firmware/Software Exceptions** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Hardware Alerts** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Ai** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Every device gate** (data table, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |

**The selected device gate** (detail panel): The pack groups this record's detail under its own headings: “Device Directory”.

| Shows | Format | Notes |
|---|---|---|
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Total devices, Online, Offline, Degraded, Turnstiles, Handhelds, Biometric readers, RFID/NFC readers, Gates open, Gates closed, Devices requiring sync, Firmware/software exceptions, Hardware alerts. Offline, Degraded, Requiring sync, Firmware exceptions and Hardware alerts are action tiles (amber/red above zero) that filter the directory. *(source: screens/P08-venue-back-office.yaml#BO-194 / contracts/spine/access.yaml#/components/schemas/DeviceGateCommandCenterViewSummary)*
- **Device directory**: Columns Device, Type, Access point, Mode, Connectivity, Status as the pack draws them, then Last heartbeat (relative, "42 s ago") and three version columns (configuration, local rules, security package) with an amber "Behind" chip when not the published version (BO-153). Status chips Healthy, Active, Degraded, Offline, Local mode (amber, "validating offline"). Cursor paging (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-194 / contracts/spine/access.yaml#/components/schemas/DeviceGateCommandCenterView)*
- **Device detail (live health)**: Connectivity, last heartbeat, versions, scanner health, controller health, camera health where applicable, and a link "Placement and registration" to BO-196. *(source: screens/P08-venue-back-office.yaml#BO-194)*
- **AI findings**: Advisory list using the pack's examples "Gate MG-04 has a scan-failure rate 4.7x higher than neighbouring gates" and "Three handhelds are running an outdated configuration package", each with Open (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-194 / contracts/spine/access.yaml#/components/schemas/DeviceGateCommandCenterViewSummary)*
- **Board tiles**: Device library, Registration, Turnstile behaviour, Guest feedback, Readers, Handhelds, Gate modes, Software and content, Compatibility and health (BO-195 to BO-203), each returning here. *(source: DI-653 / F116 step 1)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open device**: Opens BO-196 with placementId (the navigation edge carries it); mode changes go to the gate mode screens, not here. *(source: screens/P08-venue-back-office.yaml#BO-194 / contracts/spine/access.yaml#setTurnstileMode)*

**Data it reads**: `listDeviceGate` (onLoad, Device & Gate Command Center); `listAccessPoints` (onLoad, The gates and turnstiles whose mode is set)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-195` Device Type & Hardware Library: *Works in Device Type & Hardware Library*; calls `listDeviceGate`
- → `BO-197` Turnstile & Lane Behavior Configuration: *Works in Turnstile & Lane Behavior Configuration*; calls `listDeviceGate`
- → `BO-198` Validation Outcome & Guest Feedback Designer: *Works in Validation Outcome & Guest Feedback Designer*; calls `listDeviceGate`
- → `BO-199` Reader, Scanner & Peripheral Configuration: *Works in Reader, Scanner & Peripheral Configuration*; calls `listDeviceGate`
- → `BO-200` Handheld & Mobile Access Device Configuration: *Works in Handheld & Mobile Access Device Configuration*; calls `listDeviceGate`
- → `BO-201` Gate Modes, Free Spin & Emergency Controls: *Works in Gate Modes, Free Spin & Emergency Controls*; calls `listDeviceGate`
- → `BO-202` Device Software, Content & Remote Configuration: *Works in Device Software, Content & Remote Configuration*; calls `listDeviceGate`
- → `BO-203` Hardware Compatibility, Health, Testing & Deployment: *Works in Hardware Compatibility, Health, Testing & Deployment*; carries `deviceId`; calls `listDeviceGate`
- → `BO-196` Physical Device Registration & Provisioning: *Works in Physical Device Registration & Provisioning*; carries `placementId`; calls `listDeviceGate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device gate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device gate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device gate yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the device gate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Device reports a status the directory does not know**: Shown as Unknown (grey) with the raw value in the detail, never hidden. *(source: contracts/spine/tenancy.yaml#registerDevice)*
- **Critical device offline (main-entrance controller)**: Pinned to the top with severity Critical; the operations team is notified as agreed. *(source: DI-625 / DI-906)*

#### Consistency with other screens

- Match `BO-144`: Devices online/offline and gates open/closed equal the access command centre's tiles.
- Match `BO-153`: The published configuration version is what "Behind" is measured against.
- Match `BO-224`: Live operations shows the same gate status colours.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  total: 148
  online: 139
  offline: 3
  degraded: 6
  turnstiles: 64
  handhelds: 18
  biometric: 12
  rfidNfc: 30
  gatesOpen: 51
  gatesClosed: 9
  requiringSync: 4
  firmwareExceptions: 2
  hardwareAlerts: 3
devices:
- device: MG-01
  type: Turnstile
  accessPoint: Main Plaza Gate 1
  mode: Entry
  connectivity: Online
  status: Healthy
  config: v14
  rules: P-2026-10-01-07
- device: VIP-01
  type: VIP gate
  accessPoint: VIP Entrance
  mode: Entry/Exit
  connectivity: Online
  status: Healthy
- device: HH-14
  type: Handheld
  accessPoint: Group Lane
  mode: Mobile
  connectivity: Wi-Fi
  status: Active
  config: v13 (Behind)
- device: AT-07
  type: Reader
  accessPoint: Falcon Coaster
  mode: Fast Pass
  connectivity: Offline
  status: Local mode
```

#### Permissions

- `listDeviceGate` → `DEVICE_VIEW` (read) · staff
- `listAccessPoints` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Device incidents get automatic severity (e.g. main-entrance controller outage = critical); adding a device goes through an approval workflow; webhooks notify external systems when a critical device goes offline. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-906)*
- Device analytics: total/active/inactive devices across venues (multi-tenant) with location breakdown; health, availability, fault rate and top failure reasons (communication timeout, device offline, invalid response, power issue, firmware error); SLA tracking for devices in extended maintenance. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-905)*
- One screen shows live online/offline status of every workstation and device (printers, turnstiles, handheld scanners); a 360 health view shows connectivity, CPU/memory, storage and temperature. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-899)*
- Inventory counts by status (assigned, under maintenance, in stock) - e.g. 15 receipt printers broken down by ticketing, retail, F&B and in store. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-894)*
- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-194` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-194`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 1: Opens Device & Gate Command Center → Provide the central operational/configuration view of the complete access-control hardware estate.
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F116 branch at step 1 (expected): when Nothing has been set up on Device & Gate Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F116 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (294 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-194?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-195`, `BO-197`, `BO-198`, `BO-199`, `BO-200`, `BO-201`, `BO-202`, `BO-203`, `BO-196`.
- [ ] Every gated control is gated: `DEVICE_VIEW`, `SCOPE_VIEW`.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-195` Device Type & Hardware Library

**Create reusable hardware definitions independently from physical deployed devices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/device-type-hardware-library-bo-195` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The tenant's catalogue of supported hardware models, independent of deployed units: turnstiles (standard, full height, tripod, speed gate, wide lane), special gates (accessible/POD, buggy, VIP, staff), mobile (Android handheld, iOS, tablet), readers (QR/barcode, RFID, NFC, multi-technology, biometric) and others (podium, counter, beacon, camera/controller, external device), each with manufacturer, model, technologies, connectivity, offline, screen, sound, light, relay and payment capability, firmware, and a certification status. The one thing to get right: the library is shared by every venue of the tenant, so an edit shows how many deployed devices it touches.

**Known correction pending (do not draw the wrong version)**

- **Content is an empty unbound table while listDeviceTypeHardware is the read** Why: Bind the read to the library list (the pack gives the full category list and profile fields on p72-73). *(source: contracts/spine/access.yaml#listDeviceTypeHardware; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Certification status (Certified, Compatible, Conditional, Unsupported) has no field** Why: The pack lists it; procurement decisions depend on it. *(source: screens/P08-venue-back-office.yaml#BO-196; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Body requires id and scopePath** Why: Server-owned (VO-R03). *(source: contracts/spine/access.yaml#setHardwareModel; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Form: Save hardware model** (modal, opened by *Save hardware model*; *Save hardware model* calls `setHardwareModel`, *Cancel* sends nothing)

**Collects what `setHardwareModel` sends before it is called.** Required: `id`, `manufacturer`, `model`, `deviceCategory`, `hardwareType`, `scopePath`. Optional: `supportedTechnologies`, `connectivity`, `offlineCapability`, `screenCapability`, `soundCapability`, `lightCapability`, `relayControllerSupport`, `paymentCapability`, `firmwareSoftwareInformation`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setHardwareModel` body |
| Manufacturer `manufacturer` | text field | required | — | — | — | — | `setHardwareModel` body |
| Model `model` | text field | required | — | — | — | — | `setHardwareModel` body |
| Device category `deviceCategory` | radio group | required | — | Turnstile · Special gate · Mobile · Reader · Other | — | — | `setHardwareModel` body |
| Hardware type `hardwareType` | select | required | — | Standard turnstile · Full height turnstile · Tripod turnstile · Speed gate · Wide lane · Accessible pod gate · Buggy gate · Vip gate · Staff gate · Android handheld · Ios device · Tablet … | — | The specific hardware under a device's `kind` (ADR-0067, accepted 1 October: one device register). | `setHardwareModel` body |
| Supported technologies `supportedTechnologies` | list of values (chips) | optional | — | — | — | — | `setHardwareModel` body |
| Connectivity `connectivity` | list of values (chips) | optional | — | — | — | — | `setHardwareModel` body |
| Offline capability `offlineCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Screen capability `screenCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Sound capability `soundCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Light capability `lightCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Relay controller support `relayControllerSupport` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Payment capability `paymentCapability` | toggle | optional | off | — | — | Payment capability where available | `setHardwareModel` body |
| Firmware software information `firmwareSoftwareInformation` | text field | optional | — | — | — | — | `setHardwareModel` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setHardwareModel` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **deviceCategory / hardwareType**: Category first (Turnstile, Special gate, Mobile, Reader, Other), then the hardware type filtered to it, with icons. *(source: screens/P08-venue-back-office.yaml#BO-195 / contracts/spine/access.yaml#setHardwareModel)*
- **manufacturer / model**: Required text; manufacturer offered from those already in the library to avoid "Gunnebo" and "GUNNEBO" twice. *(source: contracts/spine/access.yaml#setHardwareModel)*
- **supportedTechnologies / connectivity**: Chips from closed lists - QR, 1D barcode, 2D barcode, RFID ISO 14443, RFID ISO 15693, NFC, Face; Ethernet, Wi-Fi, 4G/5G, Bluetooth, RS-485 - not free text. *(source: screens/P08-venue-back-office.yaml#BO-196 / contracts/spine/access.yaml#setHardwareModel)*
- **offline / screen / sound / light / relay / payment capability**: Six capability switches as icon toggles; these drive warnings elsewhere (e.g. a gate without sound cannot play the success tone of BO-198). *(source: contracts/spine/access.yaml#setHardwareModel / screens/P08-venue-back-office.yaml#BO-198)*
- **firmwareSoftwareInformation**: Text, e.g. "Firmware 4.2.1, OSDP v2.2"; the driver is built into the TICVAI app, never installed on a workstation. *(source: contracts/spine/access.yaml#setHardwareModel / DI-897)*
- **Certification status**: Certified / Compatible / Conditional / Unsupported, as the pack lists; no field in the contract (see corrections). *(source: screens/P08-venue-back-office.yaml#BO-196)*
- **id, scopePath, createdAt, updatedAt**: Not inputs (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save hardware model (primary button) | `setHardwareModel` PUT `/hardware-models` | AccessHardwareModel | AccessHardwareModel | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `DEVICE_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Library**: Grouped by category; columns Manufacturer, Model, Type, Technologies (chips), Capabilities (icons), Certification, Devices deployed (count across venues). *(source: screens/P08-venue-back-office.yaml#BO-195 / contracts/spine/access.yaml#listDeviceTypeHardware)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save hardware model**: Upsert (VO-R04) at tenant scope; the confirmation names the deployed devices and venues that use the model. *(source: contracts/spine/access.yaml#setHardwareModel)*

**Data it reads**: `listDeviceTypeHardware` (onLoad, Device Type & Hardware Library)

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `listDeviceTypeHardware`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device type hardware list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device type hardware untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device type hardware yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the device type hardware are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Venue-level user editing a tenant library**: Read-only with "The hardware library is managed by the tenant" unless the user holds tenant device rights (VO-R08). *(source: contracts/spine/access.yaml#setHardwareModel)*
- **Capability switched off on a model in use**: Warn with the configurations that depend on it (e.g. 12 gates use the light tower). *(source: designer default)*

#### Consistency with other screens

- Match `BO-196`: Registration picks the hardware model from this library.
- Match `BO-203`: Compatibility and certification shown there come from these capabilities.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
models:
- manufacturer: Gunnebo
  model: SpeedStile FP
  category: Turnstile
  type: Speed gate
  tech: QR, RFID ISO 15693, NFC
  connectivity: Ethernet, RS-485
  capabilities: Offline, Screen, Sound, Light, Relay
  certification: Certified
  deployed: 24
- manufacturer: Zebra
  model: TC58
  category: Mobile
  type: Android handheld
  tech: QR, 1D, NFC
  connectivity: Wi-Fi, 4G
  certification: Certified
  deployed: 18
- manufacturer: Generic
  model: BLE iBeacon
  category: Other
  type: Beacon
  certification: Conditional
```

#### Permissions

- `listDeviceTypeHardware` → `DEVICE_VIEW` (read) · staff
- `setHardwareModel` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*
- Configuration template library: a template per model (e.g. a specific Epson receipt printer) auto-attaches the right drivers when a device of that type is added. Template attribute list pending from Allam. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-896)*
- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-195` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-195`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 2: Works in Device Type & Hardware Library → Create reusable hardware definitions independently from physical deployed devices.
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-195?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save hardware model.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-196` Physical Device Registration & Provisioning

**Register actual deployed hardware and connect it to the Board 1 topology.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_MANAGE`, `DEVICE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `deviceId` (session), `placementId` (navigation) |
| Route | `/access-venue/physical-device-registration-provisioning-bo-196` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Registers real hardware and puts it in the topology, in two steps (ADR-0067): register the device in the one platform register (kind, hardware type, model, serial, network reference), then place it in Access (park, zone, access point, lane, role, controller, installation date). The provisioning journey follows: Register > Assign hardware profile > Assign location > Authenticate > Download configuration > Download security package > Connectivity test > Activate. The one thing to get right: replacing a failed unit keeps the placement - gate assignment, configuration, rules, media profiles and mode stay with the access point.

**Known correction pending (do not draw the wrong version)**

- **Device ID, Serial Number, Hardware Model, Manufacturer, Tenant, Venue, IP and controller reference are all selectFields** Why: Device id is server-assigned (VO-R03), serial and IP are text, manufacturer follows the model, tenant and venue are the session's. *(source: screens/P08-venue-back-office.yaml#BO-196 / contracts/spine/tenancy.yaml#registerDevice; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's device authentication statuses (Provisioned, Pending, Suspended, Revoked) do not match the register's enrolmentState (registered, enrolled, provisioned, active, deactivated, retired) or the placement's provisioning stages** Why: Three vocabularies for one device's life; pick the register's and map the pack's words to it. *(source: screens/P08-venue-back-office.yaml#BO-197 / contracts/spine/tenancy.yaml#registerDevice / contracts/spine/access.yaml#/components/schemas/PhysicalDeviceRegistrationProvisioningView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Entry parameter deviceId is taken from the session** Why: A device is chosen by navigation (placementId from BO-194), not session state. *(source: screens/P08-venue-back-office.yaml#BO-196; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **placeAccessDevice and updateAccessDevicePlacement bodies require id and scopePath** Why: Server-owned (VO-R03). *(source: contracts/spine/access.yaml#placeAccessDevice; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does adding an access device need an approval step and a secure enrolment code, as the 15 September minutes ask?** → Adding an access device needs a secure enrolment code and a pending-approval stage. *(decided by Chinmay, 2026-10-02; DEC-241 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Device ID | select field | — | — | — | — | — | — |
| Serial Number | select field | — | — | — | — | — | — |
| Hardware Model | select field | — | — | — | — | — | — |
| Manufacturer | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Park | select field | — | — | — | — | — | — |
| Zone | select field | — | — | — | — | — | — |
| Access Point | select field | — | — | — | — | — | — |
| Gate/Lane | select field | — | — | — | — | — | — |
| IP/network reference | select field | — | — | — | — | — | — |
| controller reference | select field | — | — | — | — | — | — |

**Form: Register device** (modal, opened by *Register device*; *Register device* calls `registerDevice`, *Cancel* sends nothing)

**Collects what `registerDevice` sends before it is called** (tenancy, the one device register, ADR-0067). Required: `kind`, `driver`. Optional: `hardwareType`, `hardwareModelId`, `serialNumber`, `model`, `identifier`, `ipNetworkReference`. An access-control device binds to no workstation. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | — | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation. | `registerDevice` body |
| Driver `driver` | text field | required | — | — | — | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015). | `registerDevice` body |
| Identifier `identifier` | text field | optional | — | — | — | — | `registerDevice` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is … | `registerDevice` body |
| Model `model` | text field | optional | — | — | — | — | `registerDevice` body |
| Hardware type `hardwareType` | select | optional | — | Standard turnstile · Full height turnstile · Tripod turnstile · Speed gate · Wide lane · Accessible pod gate · Buggy gate · Vip gate · Staff gate · Android handheld · Ios device · Tablet … | — | The specific hardware under `kind` (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. | `registerDevice` body |
| Hardware model `hardwareModelId` | picker: choose a hardware model | optional | — | — | shows names, sends the id | The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it. | `registerDevice` body |
| Serial number `serialNumber` | text field | optional | — | max length 100; A serial already registered in the tenant is refused `409` by `registerDevice`. | — | The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). | `registerDevice` body |
| Ip network reference `ipNetworkReference` | text field | optional | — | — | — | Network address or reference the device is reached at (ADR-0067). | `registerDevice` body |
| Push token `pushToken` | text field | optional | — | Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has … | — | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told … | `registerDevice` body |
| Push platform `pushPlatform` | radio group | optional | — | Ios · Android · Web · Windows | — | — | `registerDevice` body |
| Offline scope `offlineScope` | radio group | optional | — | None · Read only · Sell and scan · Full venue | — | BL-163. What this device may do with no connection, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled. | `registerDevice` body |
| Is required `isRequired` | toggle | optional | — | — | — | True blocks shift open when the device is unreachable. | `registerDevice` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 422 `workstationId` missing for a kind other than `mobileHandset`, or given for a `mobileHandset` (18.1.5).

**Form: Register access device** (modal, opened by *Register access device*; *Register access device* calls `placeAccessDevice`, *Cancel* sends nothing)

**Collects what `placeAccessDevice` sends before it is called.** Required: `id`, `venueId`, `deviceId`, `role`, `isActive`, `scopePath`. Optional: `accessAreaId`, `accessPointId`, `gateLaneId`, `name`, `deviceGroupId`, `controllerReference`, `proximityThresholdMeters`, `installationDate`. The device itself (serial, hardware model, versions) is registered in `platform.device` first, with tenancy `registerDevice` (ADR-0067). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order, and minted by the service with the … | `placeAccessDevice` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `placeAccessDevice` body |
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | The registered device placed here (`platform.device`, tenancy `registerDevice`). | `placeAccessDevice` body |
| Access area `accessAreaId` | picker: choose an access area | optional | — | — | shows names, sends the id | Most specific park, zone or attraction the device sits in (access.access_area) | `placeAccessDevice` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | Access point (gate) the device serves | `placeAccessDevice` body |
| Gate lane `gateLaneId` | picker: choose a gate lane | optional | — | — | shows names, sends the id | Lane the device is mounted on (access.gate_lane) | `placeAccessDevice` body |
| Role `role` | select | required | Entry and exit | Entry · Exit · Entry and exit · Validation only · Proximity · Monitoring | — | What the device does at this place. `proximity` is a beacon; `monitoring` a camera controller that decides nothing. | `placeAccessDevice` body |
| Name `name` | text field | optional | — | — | — | Label at this place, e.g. | `placeAccessDevice` body |
| Device group `deviceGroupId` | text field | optional | — | — | — | Device group the placement belongs to, as targeted by hardware deployments and device configurations | `placeAccessDevice` body |
| Controller reference `controllerReference` | text field | optional | — | — | — | — | `placeAccessDevice` body |
| Proximity threshold meters `proximityThresholdMeters` | number field | optional | — | min 0 | — | Beacons only: activation distance in metres | `placeAccessDevice` body |
| Installation date `installationDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `placeAccessDevice` body |
| Provisioning checklist `provisioningChecklist` | group | optional | — | — | — | Access's provisioning stages, as a checklist on the placement (ADR-0067). Each item is the time the step was confirmed, null until it is. | `placeAccessDevice` body |
| Hardware profile assigned at `provisioningChecklist.hardwareProfileAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Location assigned at `provisioningChecklist.locationAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Authenticated at `provisioningChecklist.authenticatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Configuration downloaded at `provisioningChecklist.configurationDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Security package downloaded at `provisioningChecklist.securityPackageDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Connectivity tested at `provisioningChecklist.connectivityTestedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Is active `isActive` | toggle | required | on | A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | — | Whether this placement is in use (beacons: activeInactive). A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | `placeAccessDevice` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `placeAccessDevice` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 `device-already-placed`: the device already has an active placement. Move it with `updateAccessDevicePlacement`, or set that placement `isActive: false` first.; 422 `device-not-registered`: `deviceId` names no device in `platform.device`, or one that is `deactivated` or `retired` there (ADR-0067).

**Form: Save access device** (modal, opened by *Save access device*; *Save access device* calls `updateAccessDevicePlacement`, *Cancel* sends nothing)

**Collects what `updateAccessDevicePlacement` sends before it is called.** Required: `id`, `venueId`, `deviceId`, `role`, `isActive`, `scopePath`. Optional: `accessAreaId`, `accessPointId`, `gateLaneId`, `name`, `deviceGroupId`, `controllerReference`, `proximityThresholdMeters`, `installationDate`. The device itself (serial, hardware model, versions) is registered in `platform.device` first, with tenancy `registerDevice` (ADR-0067). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order, and minted by the service with the … | `updateAccessDevicePlacement` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `updateAccessDevicePlacement` body |
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | The registered device placed here (`platform.device`, tenancy `registerDevice`). | `updateAccessDevicePlacement` body |
| Access area `accessAreaId` | picker: choose an access area | optional | — | — | shows names, sends the id | Most specific park, zone or attraction the device sits in (access.access_area) | `updateAccessDevicePlacement` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | Access point (gate) the device serves | `updateAccessDevicePlacement` body |
| Gate lane `gateLaneId` | picker: choose a gate lane | optional | — | — | shows names, sends the id | Lane the device is mounted on (access.gate_lane) | `updateAccessDevicePlacement` body |
| Role `role` | select | required | Entry and exit | Entry · Exit · Entry and exit · Validation only · Proximity · Monitoring | — | What the device does at this place. `proximity` is a beacon; `monitoring` a camera controller that decides nothing. | `updateAccessDevicePlacement` body |
| Name `name` | text field | optional | — | — | — | Label at this place, e.g. | `updateAccessDevicePlacement` body |
| Device group `deviceGroupId` | text field | optional | — | — | — | Device group the placement belongs to, as targeted by hardware deployments and device configurations | `updateAccessDevicePlacement` body |
| Controller reference `controllerReference` | text field | optional | — | — | — | — | `updateAccessDevicePlacement` body |
| Proximity threshold meters `proximityThresholdMeters` | number field | optional | — | min 0 | — | Beacons only: activation distance in metres | `updateAccessDevicePlacement` body |
| Installation date `installationDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAccessDevicePlacement` body |
| Provisioning checklist `provisioningChecklist` | group | optional | — | — | — | Access's provisioning stages, as a checklist on the placement (ADR-0067). Each item is the time the step was confirmed, null until it is. | `updateAccessDevicePlacement` body |
| Hardware profile assigned at `provisioningChecklist.hardwareProfileAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Location assigned at `provisioningChecklist.locationAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Authenticated at `provisioningChecklist.authenticatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Configuration downloaded at `provisioningChecklist.configurationDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Security package downloaded at `provisioningChecklist.securityPackageDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Connectivity tested at `provisioningChecklist.connectivityTestedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Is active `isActive` | toggle | required | on | A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | — | Whether this placement is in use (beacons: activeInactive). A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | `updateAccessDevicePlacement` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `updateAccessDevicePlacement` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `device-not-registered`: `deviceId` names no device in `platform.device`, or one that is `deactivated` or `retired` there (ADR-0067).

**Form: Enrol with code** (modal, opened by *Enrol with code*; *Enrol with code* calls `enrolDevice`, *Cancel* sends nothing)

**Collects what `enrolDevice` sends before it is called.** Required: `state`. Optional: `configurationProfileId`, `reason`, `enrolmentCode`, `testResult`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| State `state` | radio group | required | — | Enrolled · Provisioned · Active · Deactivated · Retired | — | The target state, not the current one. `registered` is absent because `registerDevice` is what produces it and nothing transitions back to it. | `enrolDevice` body |
| Configuration profile `configurationProfileId` | picker: choose a configuration profile | optional | — | — | shows names, sends the id | — | `enrolDevice` body |
| Reason `reason` | text area | optional | — | — | — | Recorded on the `tenancy.device_audit` row, not on the device. Required in practice for `deactivated` and `retired`, where an investigation six months later needs to know why a … | `enrolDevice` body |
| Enrolment code `enrolmentCode` | text field | optional | — | max length 12 | — | The one-time code `registerDevice` issued, as the device presents it (DEC-241; CHG-CSP-011). | `enrolDevice` body |
| Test result `testResult` | group | optional | — | — | — | The acceptance test, recorded on the move to `provisioned` (DEC-245; CHG-CSP-011). | `enrolDevice` body |
| Passed `testResult.passed` | toggle | optional | — | — | — | Whether the device passed; always sent with `testResult` (422 otherwise). | `enrolDevice` body |
| Notes `testResult.notes` | text area | optional | — | max length 1000 | — | — | `enrolDevice` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The transition is not allowed from the current state, or the move to `active` comes before the device is approved (`device-approval-required`; CHG-CSP-011).; 422 The enrolment code is wrong, already used or expired (`enrolment-code-invalid`; CHG-CSP-011).

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Step 1 - Register (kind, hardwareType, hardwareModelId, serialNumber, ipNetworkReference)**: Hardware model picked from BO-195 (manufacturer and type follow from it); serial number text max 100, unique in the tenant; IP or network reference text. The device id is the server's; the heartbeat-reported fields (status, health, versions, battery) are never inputs. *(source: contracts/spine/tenancy.yaml#registerDevice / ADR-0067)*
- **Step 2 - Place (accessAreaId, accessPointId, gateLaneId, role, name, controllerReference, installationDate)**: Cascading pickers Park > Zone > Access point > Gate/lane from the topology; role Entry / Exit / Entry and exit (default) / Validation only / Proximity (beacons) / Monitoring (cameras); label at the place (e.g. "MG-01", "HH-14"); proximity threshold only for beacons. *(source: screens/P08-venue-back-office.yaml#BO-196 / contracts/spine/access.yaml#placeAccessDevice)*
- **Tenant / Venue**: From the session (VO-R09), not selects. *(source: ADR-0030)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Register device (secondary button) | `registerDevice` POST `/devices` | RegisteredDevice | RegisteredDevice | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here … | gated `DEVICE_CONFIGURE`; opens modal first |
| Register access device (primary button) | `placeAccessDevice` POST `/device-placements` | AccessDevicePlacement | AccessDevicePlacement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 `device-already-placed`: the device already has an active placement. Move it with `updateAccessDevicePlacement`, or set that … | gated `DEVICE_CONFIGURE`; opens modal first |
| Save access device (secondary button) | `updateAccessDevicePlacement` PUT `/device-placements/{placementId}` | AccessDevicePlacement | AccessDevicePlacement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `DEVICE_CONFIGURE`; opens modal first |
| Enrol with code (secondary button) | `enrolDevice` POST `/devices/{deviceId}/enrolment` | DeviceEnrolment | RegisteredDevice | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The transition is not allowed from the current state, or the move to `active` comes before the device is … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Provisioning stepper**: The pack's eight steps with the time each was confirmed (provisioning checklist) and the current stage highlighted; a failed connectivity test shows its error. *(source: screens/P08-venue-back-office.yaml#BO-197 / contracts/spine/access.yaml#/components/schemas/PhysicalDeviceRegistrationProvisioningView)*
- **Registered devices**: Device, Serial, Model, Access point, Gate/lane, IP, Installation date, Provisioning stage; filter by stage. *(source: contracts/spine/access.yaml#listPhysicalDeviceRegistration)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Register device / Place device**: Two buttons in order; Place is enabled once the device exists in the register; a serial already registered is refused with the venue and device that hold it. *(source: contracts/spine/tenancy.yaml#registerDevice / contracts/spine/access.yaml#placeAccessDevice)*
- **Replace device**: Registers the new unit and gives this placement the new deviceId; confirmation lists what is preserved (gate assignment, configuration, access rules, media profiles, operating mode) and that the old unit is deactivated. *(source: screens/P08-venue-back-office.yaml#BO-197 / contracts/spine/access.yaml#updateAccessDevicePlacement)*
- **Save placement**: Whole-placement replace (VO-R04); deactivating a placement asks for a reason. *(source: contracts/spine/access.yaml#updateAccessDevicePlacement)*

**Data it reads**: `listPhysicalDeviceRegistration` (onLoad, Physical Device Registration & Provisioning)

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; carries `accessPointId`, `deviceId`, `placementId`; calls `listPhysicalDeviceRegistration`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The physical device registration configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the physical device registration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No physical device registration configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 409 The transition is not allowed from the current state, or the move to `active` comes before the device is approved (`device-approval-required`; CHG-CSP-011).; 409 `device-already-placed`: the device already has an … |

#### Edge cases to draw

- **Device retired or deactivated in the register but its placement still active**: Row shows "Refused at the gate - device deactivated" in red. *(source: contracts/spine/access.yaml#placeAccessDevice)*
- **Adding a device needs approval**: A secure enrolment code is shown after Register, and the device waits in a Pending approval stage between Register and Assign location until approved. *(source: DI-906 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Consistency with other screens

- Match `BO-194`: Opened from the command centre with placementId; returns with it.
- Match `BO-149`: Lanes picked here are those configured there.
- Match `BO-036`: Device Registry shows the same tenancy register record (ADR-0067); the maintenance asset record is separate.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
device:
  serial: GNB-SS-2024-008812
  model: Gunnebo SpeedStile FP
  kind: turnstileController
  ip: 10.20.4.31
  label: MG-04
  accessPoint: Main Plaza Gate 1
  lane: Lane 4
  role: Entry and exit
  installed: 15 Sep 2026
  stage: Configuration downloaded
```

#### Permissions

- `listPhysicalDeviceRegistration` → `DEVICE_VIEW` (read) · staff
- `registerDevice` → `DEVICE_CONFIGURE` (configure) · staff
- `placeAccessDevice` → `DEVICE_CONFIGURE` (configure) · staff
- `updateAccessDevicePlacement` → `DEVICE_CONFIGURE` (configure) · staff
- `enrolDevice` → `DEVICE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

45 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 33 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Device incidents get automatic severity (e.g. main-entrance controller outage = critical); adding a device goes through an approval workflow; webhooks notify external systems when a critical device goes offline. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-906)*
- Asset record: purchase date, warranty status/expiry, supplier, serial, manufacturer; ownership and responsibility shown separately (venue owns, operations responsible); a visual map shows installation location. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-895)*
- 360 device view shows status and workstation; reassign to another workstation or deactivate with a logged reason; lifecycle view tracks registration -> enrolment -> assignment -> reassignment. *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-893)*
- Device directory: search and add devices (printers, scanners, customer displays, cash drawers, turnstiles, handhelds, mobile POS) capturing serial number, type and model; adding generates a secure enrolment code; devices are assigned to workstations (e.g. A has ticket printer, receipt printer and cash drawer). *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-892)*
- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-196` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-196`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 4: Works in Physical Device Registration & Provisioning → Register actual deployed hardware and connect it to the Board 1 topology.
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)
- ADR-0015 *Standards-First Device Drivers* (`docs/adr/0015-standards-first-device-drivers.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (74), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-196?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Register device, Register access device, Save access device, Enrol with code.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_MANAGE`, `DEVICE_VIEW`.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-197` Turnstile & Lane Behavior Configuration

**Configure how each turnstile or lane behaves. The matrix specifically requires software on turnstiles to behave differently according to card/ticket type and supports different operating modes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/turnstile-lane-behavior-configuration-bo-197` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of turnstile and lane behaviour (setTurnstileLaneBehavior has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How each turnstile or lane physically behaves once a credential is accepted: unlock duration, pass-through timeout, relock and incomplete-passage behaviour, how unlocking differs by lane (single guest one rotation, group N admissions, accessible gate extended opening, buggy gate wide opening) and by credential (adult normal unlock, child yellow indicator and normal unlock, POD yellow and operator assistance, VIP workflow, group mode). The one thing to get right: the pack's "gate mode" list mixes three things - direction (BO-148), lane type (BO-149) and operating mode - and this screen only sets the default operating mode and the physical timings.

**Known correction pending (do not draw the wrong version)**

- **Twelve selectFields named after the pack's gate modes (Entry, Exit, Entry/Exit, Re-entry, Crossover, Fast Pass, Attraction, Group, Count Only, Free Spin, Closed) plus unlock duration, pass-through timeout and relock as selectFields** Why: Directions, lane types and operating modes are different fields on different screens (R221); timings are numbers. *(source: screens/P08-venue-back-office.yaml#BO-197 / R221; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **One unlockDuration per access point; no per-lane-type or per-credential unlock (group N admissions, accessible extended, buggy wide)** Why: The pack's unlock behaviour table cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-197 / contracts/spine/access.yaml#/components/schemas/TurnstileLaneBehaviorConfigurationInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- relockBehavior and incompletePassageBehavior are free strings; write-only screen (CHG-WIR-004)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Entry | select field | — | — | — | — | — | — |
| Exit | select field | — | — | — | — | — | — |
| Entry/Exit | select field | — | — | — | — | — | — |
| Re-entry | select field | — | — | — | — | — | — |
| Crossover | select field | — | — | — | — | — | — |
| Fast Pass | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Group | select field | — | — | — | — | — | — |
| Count Only | select field | — | — | — | — | — | — |
| Free Spin | select field | — | — | — | — | — | — |
| Closed | select field | — | — | — | — | — | — |
| Unlock duration | select field | — | — | — | — | — | — |
| pass-through timeout | select field | — | — | — | — | — | — |
| relock behavior | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **accessPointId**: Picked from the access point list (arrives from BO-194 with the access point); never typed. *(source: contracts/spine/access.yaml#setTurnstileLaneBehavior)*
- **mode (default)**: Select of the operating modes Normal, Free flow, Drop arm, Closed, Podium, Maintenance, with the pack's words (Count only, Free spin, Emergency) as helper text; the live mode is the podium's. *(source: screens/P08-venue-back-office.yaml#BO-197 / contracts/spine/access.yaml#setTurnstileLaneBehavior / R221)*
- **unlockDuration / passThroughTimeout**: Seconds, whole numbers (e.g. unlock 5 s, pass-through 8 s); accessible and buggy lanes show a separate extended value (see corrections). *(source: screens/P08-venue-back-office.yaml#BO-197 / contracts/spine/access.yaml#setTurnstileLaneBehavior)*
- **relockBehavior / incompletePassageBehavior**: Closed choices, not text - Relock after passage / Relock after timeout; incomplete passage: Relock and keep the entry used (default) / Relock and alert the operator. No option restores the entry: a successful scan is used whether or not the guest passed. *(source: contracts/spine/access.yaml#setTurnstileLaneBehavior / DI-627 / TRACKER Actions row 221)*
- **Credential-based behaviour**: Shown as a read-only table of guest types and the outcome profile each uses, linking to BO-198 where it is configured (adult green, child yellow indicator with normal unlock, POD yellow with operator assistance). *(source: screens/P08-venue-back-office.yaml#BO-197 / DI-644)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lane behaviour card**: A timeline "Scan accepted > Unlock 5 s > Pass-through window 8 s > Relock" with the incomplete-passage branch. *(source: screens/P08-venue-back-office.yaml#BO-197 / designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save lane behaviour**: Whole-record upsert (VO-R04); pushed to the gate's controller with the next configuration. *(source: contracts/spine/access.yaml#setTurnstileLaneBehavior)*

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; carries `accessPointId`; calls `setTurnstileLaneBehavior`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The turnstile lane behavior configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the turnstile lane behavior untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No turnstile lane behavior configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Guest scanned but turned back (stroller, turnstile re-locked)**: The ticket stays used; help text points to resolving it from the scan history. *(source: DI-627)*
- **Group ticket at a standard turnstile**: Unlock repeats N times or the lane switches to group mode; warn if the lane is not a group lane (BO-149). *(source: screens/P08-venue-back-office.yaml#BO-197)*

#### Consistency with other screens

- Match `BO-149`: Lane type (accessible, buggy, group) decides which unlock profile applies.
- Match `BO-198`: Credential-based light and sound live in outcome profiles.
- Match `BO-201`: Free flow and Drop arm names and colours as in the gate mode policy.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
behaviour:
  accessPoint: Main Plaza Gate 1
  defaultMode: Normal
  unlock: 5 s
  passThrough: 8 s
  relock: Relock after passage
  incomplete: Relock and keep the entry used
  accessibleLane: unlock 12 s
```

#### Permissions

- `setTurnstileLaneBehavior` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Turnstile light/sound feedback is configurable: e.g. green light for an adult ticket, orange for a child ticket as a quick visual fraud check; some models play audio, including celebratory sounds (e.g. birthday visit). *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-644)*
- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-197` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-197`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 6: Works in Turnstile & Lane Behavior Configuration → Configure how each turnstile or lane behaves. The matrix specifically requires software on turnstiles to behave differently according to card/ticket type and supports different operating modes.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-197?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-198` Validation Outcome & Guest Feedback Designer

**Configure what the physical access device does and displays after validation. The matrix explicitly requires valid/non-valid messages, lights, pictograms and sounds, including green/yellow/red behavior.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/validation-outcome-guest-feedback-designer-bo-198` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of validation outcome and guest feedback profiles (setValidationOutcomeGuest has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Designs what a gate does and shows after every decision: GREEN - access granted (green light, gate opens, success tone, tick pictogram, custom message "WELCOME - ACCESS GRANTED"), YELLOW - operator action (yellow light, alert sound, gate stays controlled, operator prompt "CHECK ID", "VERIFY COMPANION", "MANUAL ELIGIBILITY CHECK"), RED - access denied (red light, denial sound, gate stays locked, reason "TICKET EXPIRED"), with different responses for adult, child, VIP, POD, membership, invalid credential, wrong verification method, biometric review and re-entry exception, in Arabic and English. The one thing to get right: a live preview of the reader display and light, because this is the only thing a guest sees of all the rules.

**Known correction pending (do not draw the wrong version)**

- **Eleven selectFields named after the pack's options (Green light, Gate open, Success tone, tick pictogram, Custom message, Yellow light, Alert sound ...)** Why: They are values of light, gate action, sound, pictogram and message fields for each outcome. *(source: screens/P08-venue-back-office.yaml#BO-198 / contracts/spine/access.yaml#setValidationOutcomeGuest; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **One message and one language per record** Why: Arabic and English must be authored together for the same response; one record per language invites a missing translation. *(source: contracts/spine/access.yaml#/components/schemas/ValidationOutcomeGuestFeedbackDesignerInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **reasonCode is free text and the sound list has no celebratory sound** Why: Deny reasons are a closed vocabulary (VO-R06); the client asked for celebratory sounds (birthday visit). *(source: contracts/spine/access.yaml#setValidationOutcomeGuest / DI-644; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- outcomeProfileId required; write-only screen (CHG-WIR-004)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Green light | select field | — | — | — | — | — | — |
| Gate open | select field | — | — | — | — | — | — |
| Success tone | select field | — | — | — | — | — | — |
| ✓ pictogram | select field | — | — | — | — | — | — |
| Custom message | select field | — | — | — | — | — | — |
| Yellow light | select field | — | — | — | — | — | — |
| Alert sound | select field | — | — | — | — | — | — |
| Gate remains controlled | select field | — | — | — | — | — | — |
| Red light | select field | — | — | — | — | — | — |
| Denial sound | select field | — | — | — | — | — | — |
| Gate remains locked | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **appliesTo / outcome**: A grid - rows the nine guest types or cases, columns Granted / Operator action / Denied; clicking a cell edits that response. Every row has all three cells (defaults from the outcome column). *(source: screens/P08-venue-back-office.yaml#BO-198 / screens/P08-venue-back-office.yaml#BO-199 / contracts/spine/access.yaml#setValidationOutcomeGuest)*
- **lightColour / gateAction / sound**: Light Green / Yellow / Red, independent of the outcome so a child can be Granted with a yellow (orange) indicator as agreed; gate action Open / Remains controlled / Remains locked, locked for Denied; sound Success tone / Alert / Denial (plus the celebratory sound requested, see corrections). *(source: screens/P08-venue-back-office.yaml#BO-197 / contracts/spine/access.yaml#setValidationOutcomeGuest / DI-644)*
- **pictogram**: Picker of a small pictogram set (tick, cross, exclamation, person-check, child, wheelchair), not free text. *(source: contracts/spine/access.yaml#setValidationOutcomeGuest)*
- **customMessage / operatorPrompt / language**: Message per language side by side (English, Arabic, plus venue languages), max length shown against the reader's display; the operator prompt is shown to staff on the podium or handheld, not to the guest. *(source: screens/P08-venue-back-office.yaml#BO-199 / contracts/spine/access.yaml#setValidationOutcomeGuest)*
- **reasonCode**: For Denied, a select of the deny reasons (Already used, Re-entry limit reached, Wrong gate, Not yet valid, Expired, Venue full ...) with their plain-language labels (VO-R06), not typed. *(source: contracts/spine/access.yaml#setValidationOutcomeGuest)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Reader preview**: A turnstile display mock showing light colour, pictogram, message in the chosen language, the tenant's logo and "Powered by TICVAI" (guest surface), and a podium mock for the operator prompt. *(source: screens/P08-venue-back-office.yaml#BO-198 / DI-645)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save outcome profile**: Upsert per profile (VO-R04); gates use it after their next configuration push; the confirmation lists gates whose hardware cannot show light, sound or text (capabilities from BO-195). *(source: contracts/spine/access.yaml#setValidationOutcomeGuest / screens/P08-venue-back-office.yaml#BO-195)*

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `setValidationOutcomeGuest`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validation outcome guest configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validation outcome guest untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validation outcome guest configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Gate model without a screen or speaker**: Preview marks the missing parts "Not shown on Speed Gate model X"; the profile still saves. *(source: contracts/spine/access.yaml#setHardwareModel)*
- **Arabic message missing**: Warn; the reader falls back to English, never to an empty display. *(source: ADR-0011 / DI-019)*

#### Consistency with other screens

- Match `BO-191`: Biometric green/yellow/red use these profiles.
- Match `SCN-003`: The handheld shows the same message and reason labels as the gate display.
- Match `BO-197`: Credential-based behaviour there reads from these profiles.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
responses:
- appliesTo: Adult
  outcome: Granted
  light: Green
  gate: Open
  sound: Success tone
  message: WELCOME - ACCESS GRANTED
  messageAr: أهلاً وسهلاً - تم السماح بالدخول
- appliesTo: Child
  outcome: Granted
  light: Yellow
  gate: Open
  sound: Success tone
  message: WELCOME
- appliesTo: POD
  outcome: Operator action
  light: Yellow
  gate: Remains controlled
  prompt: VERIFY COMPANION
- appliesTo: Invalid credential
  outcome: Denied
  light: Red
  gate: Remains locked
  sound: Denial
  reason: Expired
  message: TICKET EXPIRED
```

#### Permissions

- `setValidationOutcomeGuest` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A custom welcome message and the venue's branding/logo show on the reader on a successful scan. *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-645)*
- Turnstile light/sound feedback is configurable: e.g. green light for an adult ticket, orange for a child ticket as a quick visual fraud check; some models play audio, including celebratory sounds (e.g. birthday visit). *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-644)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-198` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-198`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 8: Works in Validation Outcome & Guest Feedback Designer → Configure what the physical access device does and displays after validation. The matrix explicitly requires valid/non-valid messages, lights, pictograms and sounds, including green/yellow/red …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-198?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-199` Reader, Scanner & Peripheral Configuration

**Configure the technologies attached to a gate/device.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/reader-scanner-peripheral-configuration-bo-199` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Says which readers and peripherals a gate has (QR, 1D/2D barcode, RFID, NFC, biometric camera, height sensor, display, speaker, light tower, printer, payment reader), in what order it tries verification methods (Face Pass, Dynamic QR, RFID, NFC - or Auto detect), its RFID range, and sensor conditions such as the junior height check (automatic with a supported height sensor, otherwise yellow for operator verification). The one thing to get right: capability detection - "Height verification is configured, but Gate 14 does not have a supported height sensor" - shown as soon as the configuration asks for something the hardware cannot do.

**Known correction pending (do not draw the wrong version)**

- **capabilityWarnings is a field of the write request; the content shows an empty scanTarget component and unbound Save and Cancel** Why: Warnings are the system's output; a scan target has no place on a configuration screen; the editor needs a read. *(source: contracts/spine/access.yaml#setReaderScannerPeripheral / screens/P08-venue-back-office.yaml#BO-199; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **readers and verificationPriority are free string arrays; no Auto detect option** Why: Closed component and method lists; the pack offers Auto detect as the alternative to an order. *(source: screens/P08-venue-back-office.yaml#BO-200 / contracts/spine/access.yaml#/components/schemas/ReaderScannerPeripheralConfigurationInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **When a gate's verification order and a product's media activation priority (BO-341) differ, which wins?** → Drawn default accepted: The product's priority among the methods the gate supports; the gate order breaks ties. *(decided by Chinmay, 2026-10-02; DEC-242 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **accessPointId**: Arrives from BO-194; never typed. *(source: contracts/spine/access.yaml#setReaderScannerPeripheral)*
- **readers**: Derived from the devices placed at the gate (BO-196) and shown as component icons; an extra peripheral not registered as a device is added from the closed component list, not typed. *(source: screens/P08-venue-back-office.yaml#BO-199 / contracts/spine/access.yaml#setReaderScannerPeripheral)*
- **verificationPriority**: Drag-ordered list of methods the gate's readers support, or an "Auto detect" switch that hides the order. *(source: screens/P08-venue-back-office.yaml#BO-199 / screens/P08-venue-back-office.yaml#BO-200 / contracts/spine/access.yaml#setReaderScannerPeripheral)*
- **rfidRange**: Near / Medium / Far, shown only when an RFID reader is present; must match the RFID range policy for the gate (BO-180). *(source: contracts/spine/access.yaml#setReaderScannerPeripheral / screens/P08-venue-back-office.yaml#BO-180)*
- **heightVerificationEnabled**: Switch with the outcome explained - with a sensor, automatic; without, Yellow - operator verification. *(source: screens/P08-venue-back-office.yaml#BO-200 / contracts/spine/access.yaml#setReaderScannerPeripheral)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Gate component diagram**: The gate drawn with its components as icons in place (reader, camera, light tower, display, speaker, height sensor), each with health from the device register. *(source: screens/P08-venue-back-office.yaml#BO-199 / designer default)*
- **Capability warnings**: Computed by the system and shown in amber with the pack's wording; never entered by the user. *(source: screens/P08-venue-back-office.yaml#BO-200)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save gate peripherals**: Whole-record upsert (VO-R04); pushed with the next configuration. *(source: contracts/spine/access.yaml#setReaderScannerPeripheral)*

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; carries `accessPointId`; calls `setReaderScannerPeripheral`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader scanner peripheral list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader scanner peripheral untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader scanner peripheral yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader scanner peripheral are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Priority lists Face Pass first but the gate has no camera**: Face Pass row disabled with "No biometric camera at this gate". *(source: screens/P08-venue-back-office.yaml#BO-200)*
- **Product-level media priority differs from the gate's order**: Show both orders side by side when they differ. *(source: contracts/spine/access.yaml#listMediaActivationPriority)*

#### Consistency with other screens

- Match `BO-147`: An attraction's minimum height relies on this sensor setting.
- Match `BO-195`: Supported components come from the hardware model's capabilities.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
gate:
  accessPoint: Falcon Coaster Entry
  readers: QR reader, RFID reader, Biometric camera, Height sensor, Light tower, Display
  priority: Face Pass, Dynamic QR, RFID, NFC
  rfidRange: Near
  height: On - sensor present
warning: Height verification is configured, but Main Plaza Gate 3 does not have a supported height sensor.
```

#### Permissions

- `setReaderScannerPeripheral` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-199` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-199`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 10: Works in Reader, Scanner & Peripheral Configuration → Configure the technologies attached to a gate/device.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-199?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-200` Handheld & Mobile Access Device Configuration

**Configure mobile access-control devices used by staff. The matrix explicitly requires handheld devices and Android/iOS dedicated mobile applications.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/handheld-mobile-access-device-configuration-bo-200` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of handheld device configurations and no remote-revoke operation for a lost device.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Profiles for staff handhelds and phones used as scanners: device type and platform, assigned venue, zone and operator group, permitted operating modes, offline capability, scanner source (camera or built-in scanner), biometric capability, and which operator functions the device shows (scan, search, entry, exit, re-entry, crossover, group admission, manual attendance, override, view history, change device mode), plus the offline package status and remote revoke for a lost device. The one thing to get right: a device profile can hide or restrict functions but never grants them - what a person may do comes from their role (ADR-0002); the pack's "Supervisor: scan + override + mode change" is a role, not a device.

**Known correction pending (do not draw the wrong version)**

- **Scan Ticket, Search Ticket, Entry, Manual Attendance, Override (destructive, with a confirm dialog) and View History are drawn as action-bar buttons** Why: They are values of enabledFunctions (which functions the device shows), not actions of the configuration screen. *(source: screens/P08-venue-back-office.yaml#BO-200 / contracts/spine/access.yaml#setHandheldMobileAccess; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's restricted functions make Override a property of a device profile ("Supervisor - Scan + Override + Mode change")** Why: ADR-0002 - authorisation follows the person's role, never the device; a profile may only hide functions. *(source: screens/P08-venue-back-office.yaml#BO-201 / ADR-0002; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Remote revoke device has no operation; assigned venue, zone and operator group are free strings; profileId required; write-only screen** Why: The pack's lost-device action needs a write; the others are references (VO-R03) and the editor needs a read. *(source: screens/P08-venue-back-office.yaml#BO-201 / contracts/spine/access.yaml#/components/schemas/HandheldMobileAccessDeviceConfigurationInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Device type | select field | — | — | — | — | — | — |
| Android/iOS | select field | — | — | — | — | — | — |
| assigned venue | select field | — | — | — | — | — | — |
| assigned zone | select field | — | — | — | — | — | — |
| assigned operator group | select field | — | — | — | — | — | — |
| permitted operating modes | select field | — | — | — | — | — | — |
| offline capability | select field | — | — | — | — | — | — |
| scanner source | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name / deviceType / platform**: Profile name (e.g. "Standard attendant handheld"), device type from the hardware library (Android handheld, iOS device, tablet), platform Android / iOS. *(source: screens/P08-venue-back-office.yaml#BO-200 / contracts/spine/access.yaml#setHandheldMobileAccess)*
- **assignedVenue / assignedZone / assignedOperatorGroup**: Venue from the session; zone from the topology; operator group from the staff groups - pickers, not text. *(source: contracts/spine/access.yaml#setHandheldMobileAccess)*
- **permittedOperatingModes / scannerSource / offlineCapability / biometricCapabilityWhereSupported**: Modes as chips (Entry, Exit, Re-entry, Crossover, Group); scanner source Camera / Built-in scanner / Bluetooth scanner; offline and biometric switches, biometric only on models with a camera. *(source: screens/P08-venue-back-office.yaml#BO-200 / contracts/spine/access.yaml#setHandheldMobileAccess)*
- **enabledFunctions**: Checkbox list of the eleven functions headed "Functions shown on this device"; under it, the line "Staff still need the role permission for each function (Override needs supervisor rights)". Override and Change device mode carry a lock icon showing the permission they need. *(source: contracts/spine/access.yaml#setHandheldMobileAccess / ADR-0002)*
- **profileId**: Not an input on create (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Scan Ticket (primary button) | navigation or local | — | — | — | — |
| Search Ticket (secondary button) | navigation or local | — | — | — | — |
| Entry (secondary button) | navigation or local | — | — | — | — |
| Manual Attendance (secondary button) | navigation or local | — | — | — | — |
| Override (destructive button) | navigation or local | — | — | — | — |
| View History (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Offline package panel**: Last sync 09:42, Rules valid until 18:00, Revocation package Current/Stale - per device using this profile, amber when stale. *(source: screens/P08-venue-back-office.yaml#BO-201)*
- **Devices on this profile**: Device label, operator signed in, last sync, package state, with Remote revoke. *(source: screens/P08-venue-back-office.yaml#BO-201)*
- **Phone preview**: The handheld home screen with only the enabled functions, as SCN and EMP scan screens would show it. *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save handheld profile**: Whole-record upsert (VO-R04); devices pick it up at next sync. *(source: contracts/spine/access.yaml#setHandheldMobileAccess)*
- **Remote revoke device**: Typed confirmation naming the device and its last operator; afterwards the device can make no trusted access transactions and its journal is flagged for review. No operation is bound (see corrections). *(source: screens/P08-venue-back-office.yaml#BO-201)*

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `setHandheldMobileAccess`

**What opens over it**

- confirmDialog *Override*: **Override on a handheld mobile access is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The handheld mobile access configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the handheld mobile access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No handheld mobile access configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Lost device holding unsynced scans**: Revoke warns "12 scans not yet synced will be lost unless the device reconnects"; reconciliation lists them if it does. *(source: F06 step 6)*
- **Function enabled on the profile but the signed-in person lacks the permission**: Shown disabled on the device with the missing permission named (VO-R08). *(source: ADR-0002)*

#### Consistency with other screens

- Match `SCN-003`: The scanner's functions are the enabled ones here, filtered by the person's role.
- Match `EMP-010`: The staff app's scan function uses the same profile.
- Match `BO-036`: Handhelds are registered once in the device register (mobileHandset or handheldScanner).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- name: Standard attendant handheld
  device: Zebra TC58
  platform: Android
  zone: Main Plaza
  group: Gate attendants
  modes: Entry, Exit
  offline: true
  functions: Scan ticket, Group admission
- name: Supervisor handheld
  device: Zebra TC58
  platform: Android
  group: Gate supervisors
  functions: Scan ticket, Search ticket, Override, View history, Change device mode
package:
  device: HH-14
  lastSync: 09:42
  rulesValidUntil: '18:00'
  revocation: Current
```

#### Permissions

- `setHandheldMobileAccess` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-200` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-200`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 12: Works in Handheld & Mobile Access Device Configuration → Configure mobile access-control devices used by staff. The matrix explicitly requires handheld devices and Android/iOS dedicated mobile applications.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-200?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Scan Ticket, Search Ticket, Entry, Manual Attendance, Override, View History.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-201` Gate Modes, Free Spin & Emergency Controls

**Manage non-standard operational modes. The source specifically requires Free Spin and Drop Arm/Emergency behavior.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20679 (APP-SETUP-BO-201) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/gate-modes-free-spin-emergency-controls-bo-201` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Governs the non-standard gate modes: Free flow (free spin - reading off, turnstile still counts), Drop arm (emergency - validation off, counting off, gate released) and, by extension, Closed and Count only. For each it sets who may activate it, on which gate group, whether a reason and an emergency code are needed, and whether activation notifies people and opens an incident. The pack also wants a bulk command ("Main Entrance - 18 gates - Activate emergency mode"). The one thing to get right: emergency controls are fast to reach and impossible to trigger by accident.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Bulk activation across a gate group has no operation (CHG-SBO-005)
- Body requires id and scopePath (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): All six controls are selectFields (reason, emergency code, automatic notification) (CHG-SBO-009).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Who can activate | list of values (chips) | optional | — | — | — | Roles allowed to activate this mode | `AccessGateModePolicy.whoCanActivate` |
| Gate group | picker: choose an access point group | optional | — | — | shows names, sends the id | Gate group the policy applies to (access.access_point_group); null for the whole venue | `AccessGateModePolicy.accessPointGroupId` |
| Reason required | toggle | optional | on | — | — | — | `AccessGateModePolicy.reasonRequired` |
| Emergency code | text field | optional | — | — | — | Masked; never shown back once saved. | `AccessGateModePolicy.emergencyCode` |
| Notify automatically | toggle | optional | off | — | — | — | `AccessGateModePolicy.automaticNotification` |

**Form: Save gate mode policy** (modal, opened by *Save gate mode policy*; *Save gate mode policy* calls `setGateModePolicy`, *Cancel* sends nothing)

**Collects what `setGateModePolicy` sends before it is called.** Required: `id`, `venueId`, `mode`, `scopePath`. Optional: `whoCanActivate`, `accessPointGroupId`, `reasonRequired`, `emergencyCode`, `automaticNotification`, `createsIncident`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setGateModePolicy` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setGateModePolicy` body |
| Mode `mode` | segmented control | required | — | Free flow · Drop arm | — | Non-standard operating mode governed (R221 vocabulary) | `setGateModePolicy` body |
| Who can activate `whoCanActivate` | list of values (chips) | optional | — | — | — | Roles allowed to activate this mode | `setGateModePolicy` body |
| Access point group `accessPointGroupId` | picker: choose an access point group | optional | — | — | shows names, sends the id | Gate group the policy applies to (access.access_point_group); null for the whole venue | `setGateModePolicy` body |
| Reason required `reasonRequired` | toggle | optional | on | — | — | — | `setGateModePolicy` body |
| Emergency code `emergencyCode` | text field | optional | — | — | — | — | `setGateModePolicy` body |
| Automatic notification `automaticNotification` | toggle | optional | off | — | — | — | `setGateModePolicy` body |
| Creates incident `createsIncident` | toggle | optional | off | — | — | Activation creates an incident record | `setGateModePolicy` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setGateModePolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **mode**: Policy per mode, Free flow or Drop arm, shown as two cards with what each does to reading and counting (pack wording). *(source: screens/P08-venue-back-office.yaml#BO-201 / contracts/spine/access.yaml#setGateModePolicy)*
- **whoCanActivate**: Multi-select of roles from the role list (not free text); suggest Supervisor and Duty manager for Drop arm. *(source: screens/P08-venue-back-office.yaml#BO-201 / contracts/spine/access.yaml#setGateModePolicy / designer default)*
- **accessPointGroupId**: Gate group picker from BO-151; empty means the whole venue and must say "Whole venue". *(source: contracts/spine/access.yaml#/components/schemas/AccessGateModePolicy)*
- **reasonRequired, emergencyCode, automaticNotification, createsIncident**: Toggles with defaults reason on, notification off, incident off; emergency code is a short code staff type to confirm (masked), required for Drop arm. *(source: screens/P08-venue-back-office.yaml#BO-201 / contracts/spine/access.yaml#/components/schemas/AccessGateModePolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save gate mode policy (primary button) | `setGateModePolicy` PUT `/gate-mode-policies` | AccessGateModePolicy | AccessGateModePolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Policies by mode**: For each mode, the roles, gate group, safeguards; and the current live mode of each gate in that group (from the live gate mode read) so an active emergency is visible. *(source: contracts/spine/access.yaml#listGateModeFree / contracts/spine/access.yaml#listLiveGateMode)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save policy**: Whole-policy upsert (VO-R04); enforced when anyone sets a gate mode (refused if role not allowed or reason missing). *(source: contracts/spine/access.yaml#setGateModePolicy)*
- **Activate on group (bulk command)**: Pack asks for "Select Main Entrance - 18 gates - Activate emergency mode" with explicit authorisation and an immutable audit record; the contract has only the per-gate setTurnstileMode, so draw it with a typed confirmation and flag it. *(source: screens/P08-venue-back-office.yaml#BO-201 / contracts/spine/access.yaml#setTurnstileMode)*

**Data it reads**: `listGateModeFree` (onLoad, Gate Modes, Free Spin & Emergency Controls)

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `listGateModeFree`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gate modes free configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gate modes free untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gate modes free configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Drop arm while offline**: Gate mode setting is offline-capable at the podium; the back office shows the change when it syncs. *(source: contracts/spine/access.yaml#setTurnstileMode)*
- **Scheduled mode change**: A future effective time shows as Pending with Cancel. *(source: contracts/spine/access.yaml#setTurnstileMode / contracts/spine/access.yaml#cancelGateModeChange)*

#### Consistency with other screens

- Match `SCN-016`: Same mode names and colours (Drop arm green everybody-through, Closed red) per VO-R16.
- Match `BO-224`: Live operations shows the mode each gate is in.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policies:
- mode: Drop arm
  who: Duty manager, Security supervisor
  group: Main Entrance (18 gates)
  reason: required
  code: required
  notify: Ops team, Security
  incident: true
- mode: Free flow
  who: Supervisor
  group: Whole venue
  reason: required
  notify: false
  incident: false
```

#### Permissions

- `listGateModeFree` → `SCOPE_VIEW` (read) · staff
- `setGateModePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-201` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-201`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 14: Works in Gate Modes, Free Spin & Emergency Controls → Manage non-standard operational modes. The source specifically requires Free Spin and Drop Arm/Emergency behavior.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-201?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save gate mode policy.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-202` Device Software, Content & Remote Configuration

**Centrally control access-control device software and guest-facing configuration. The source requires the ability to configure/manage software on turnstiles, add external webpages on supported screens, and enable payment technologies where available.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/device-software-content-remote-configuration-bo-202` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of the device software package, its versions or its rollout progress, and no rollback.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The configuration package and guest-facing screen content for a group of gate devices, deployed remotely in stages (Draft > Test device > Device group > Venue rollout) instead of configuring each turnstile by hand. An access systems administrator edits one versioned package (device and reader settings, default gate mode, media and outcome profiles, languages, local rules, offline security) and the reader screen content (welcome page with the venue's branding, instructions, ticket status, reason message, promotion, an approved web page, emergency information). The one thing to get right: this is a versioned package that moves through stages with visible progress and a way back, not a settings form that changes live gates on Save.

**Known correction pending (do not draw the wrong version)**

- **Write-only screen; no read of the current package, its versions or its rollout progress** Why: The form cannot open pre-filled (VO-R04), versions cannot be compared and the pack's "78 / 80 devices updated" has nothing to read. *(source: screens/P08-venue-back-office.yaml#BO-203 / contracts/spine/access.yaml#setDeviceSoftwareContent; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **All 19 configuration and content properties are free strings; the screen draws six of them as selectFields with no options** Why: Gate mode is a closed set, media and outcome profiles are references, content is per-language text; free strings cannot be validated or previewed. *(source: contracts/spine/access.yaml#setDeviceSoftwareContent / contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **`localRules` is a free-text string** Why: The gate must evaluate the same active policy version as the cloud, in the closed JSON rule format; a device-local free-text rule reopens what ADR-0068 closed. *(source: ADR-0068; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Emergency information, payment capability and rollback are in the pack and the minutes but not on the screen (payment and rollback not in the contract)** Why: The pack lists emergency information and payment Enabled/Disabled; MoM 15 Sep asks for versions to be compared and rolled back. *(source: screens/P08-venue-back-office.yaml#BO-202 / DI-898; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Body requires venueId and configurationId as typed inputs** Why: Venue comes from the session and the package id from the server (VO-R03). *(source: contracts/spine/access.yaml#setDeviceSoftwareContent; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does this screen also deploy firmware and app software (package library, compatibility rules, phased rollout per DI-903), or only configuration and content?** → Drawn default accepted: Configuration and content only; show the firmware version per device read-only from the device register with a link to device management. *(decided by Chinmay, 2026-10-02; DEC-243 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Which hardware actually supports an external web page and payment at the gate?** → Drawn default accepted: Draw both sections greyed with "Depends on device model" until the hardware library says which models support them. *(decided by Chinmay, 2026-10-02; DEC-244 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Welcome page | select field | — | — | — | — | — | — |
| Instructions | select field | — | — | — | — | — | — |
| Ticket status | select field | — | — | — | — | — | — |
| Reason message | select field | — | — | — | — | — | — |
| Promotional information | select field | — | — | — | — | — | — |
| External approved webpage | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **deviceGroupId**: "Target device group" picker from the gate groups (BO-151), showing the device count and how many of those devices have a screen and a payment terminal ("18 devices, 12 with a screen, 0 with payment"). Required. Content fields for a capability no device in the group has are shown greyed with that reason. *(source: screens/P08-venue-back-office.yaml#BO-202 / contracts/spine/access.yaml#setDeviceSoftwareContent)*
- **venueId / configurationId**: Never inputs: the venue is the top-bar venue (VO-R03); the configuration id is the package being edited, chosen from the package list on the left, and a new package gets its id from the server. *(source: contracts/spine/access.yaml#setJourneySequenceRule / ADR-0030)*
- **version**: Read-only label assigned on each save ("v12"), with "Compare with" and the previous versions listed, so a rollback has something to pick; not a text field. *(source: contracts/spine/access.yaml#setDeviceSoftwareContent / DI-898)*
- **gateMode**: Labelled "Mode at start-up" and limited to the gate mode list (Normal, Free flow, Closed, Podium, Maintenance; Drop arm is never a start-up mode). Live mode changes during the day stay on BO-230 and the podium (SCN-016); say so under the field. *(source: contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode / R221 / DI-648)*
- **mediaProfiles / outcomeProfiles**: Multi-selects of the media profiles (BO-175) and the outcome profiles designed on BO-198 (green/amber/red, light, sound, message), never typed names. At least one of each before the package can leave Draft. *(source: contracts/spine/access.yaml#setDeviceSoftwareContent / DI-644)*
- **language**: Languages the reader shows, English and Arabic chips with one marked default; every content field then has one tab per chosen language and Arabic renders right to left. *(source: contracts/spine/access.yaml#setDeviceSoftwareContent)*
- **localRules / offlineSecurityConfiguration**: Not free text. Local rules are shown read-only as "Guest admission policy version 3.5 (active)" because the package carries the active policy version and the gate evaluates it, never rules of its own; the offline security reference is a picker of the offline cryptographic profiles (BO-171). *(source: ADR-0068 / contracts/spine/access.yaml#getOfflinePackage)*
- **welcomePage / instructions / ticketStatus / reasonMessage / promotionalInformation / emergencyInformation**: Short text per language with a live reader-screen preview beside them, in the tenant's brand with "Powered by TICVAI" and the venue logo. The welcome message may use the guest's first name and a birthday variant. Reason messages default to the deny reason labels and are edited there, not per device (the preview shows "Already used - please see a steward"). *(source: DI-645 / DI-644)*
- **externalApprovedWebpage**: Pick from an approved web page list (https only); a typed URL that is not on the list cannot be saved. Shown only for devices with a screen. *(source: screens/P08-venue-back-office.yaml#BO-202 / designer default)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Package list**: Left list of packages per device group with version, stage (Draft, Test device, Device group, Venue rollout) and "Last changed by <name>, <time>". *(source: contracts/spine/access.yaml#setDeviceSoftwareContent)*
- **Rollout progress**: When a stage is under way: "78 / 80 devices updated", failures named ("2 devices offline: VIP-01, HH-04") with Retry when they reconnect. *(source: screens/P08-venue-back-office.yaml#BO-203 / contracts/spine/access.yaml#publishHardwareDeployment)*
- **Reader preview**: A device-shaped preview for each content type (welcome, ticket status, reason, emergency), switchable between English and Arabic. *(source: DI-645 / designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save draft**: Saves the whole package (per VO-R04) as a new version in Draft; nothing reaches a gate. 422 errors show against the field. *(source: contracts/spine/access.yaml#setDeviceSoftwareContent)*
- **Promote to next stage**: Draft > Test device (one named device) > Device group > Venue rollout; each step names the devices it reaches and runs through publishHardwareDeployment, so devices that fail the compatibility test are skipped and listed. Devices pick it up at their next package refresh. *(source: screens/P08-venue-back-office.yaml#BO-202 / contracts/spine/access.yaml#publishHardwareDeployment)*
- **Roll back to version N**: Confirmation names the version and the devices it reaches; drawn but greyed until an operation exists (see corrections). *(source: DI-898 / DI-903)*

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `setDeviceSoftwareContent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device software content configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device software content untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device software content configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Devices offline during rollout**: They stay "Pending" with the time they were last seen; the stage completes for the rest and the count says "78 / 80". *(source: screens/P08-venue-back-office.yaml#BO-203)*
- **Payment capability**: Shown as Enabled / Disabled with the pack's use cases (entitlement upgrade, Fast Pass purchase, parking, supplemental access) and the note that payment runs through the TICVAI payment layer; greyed because the write has no field for it. *(source: screens/P08-venue-back-office.yaml#BO-202)*
- **New hardware model**: No driver install step; a new model is supported by a back-end driver update, so the screen never asks for a driver file. *(source: DI-897)*

#### Consistency with other screens

- Match `BO-203`: Uses the same deployment operation and the same target words (pilot, selected gates, device group, venue) and progress wording.
- Match `BO-198`: Outcome profiles (colours, sounds, messages) are designed there and only chosen here.
- Match `BO-230`: The start-up mode here and the live mode there use the same gate mode names and colours (VO-R16).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
packages:
- group: Main Plaza Gates 1-3
  version: v12
  stage: Device group
  progress: 78 / 80 devices updated
  failures: '2 offline: VIP-01, HH-04'
  changed: Rahul Menon, 30 Sep 2026 22:10
- group: Summit Peaks attraction readers
  version: v4
  stage: Draft
  changed: Maria Santos, 1 Oct 2026 09:12
content:
  welcome:
    en: Welcome to Aqua Park, Sara!
    ar: أهلاً بك في أكوا بارك، سارة
  reason: Already used at 09:58, Main Plaza Gate 1 - please see a steward
  emergency: Please follow staff to the nearest exit
```

#### Permissions

- `setDeviceSoftwareContent` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Firmware: package library per device; compatibility rules limit deployment to compatible models; update wizard with phased/scheduled rollout; live monitor flags failures (e.g. device offline at deployment); rollback and update history. *(client request · MoM 15 Sep 2026, 4.7 Firmware & Software Management · DI-903)*
- Remote configuration deploys a device type's settings (e.g. receipt printers) to many workstations in one action; configuration versions can be compared and rolled back. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-898)*
- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*
- A custom welcome message and the venue's branding/logo show on the reader on a successful scan. *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-645)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-202` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-202`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 16: Works in Device Software, Content & Remote Configuration → Centrally control access-control device software and guest-facing configuration. The source requires the ability to configure/manage software on turnstiles, add external webpages on supported …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-202?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-203` Hardware Compatibility, Health, Testing & Deployment

**Provide the final testing and governance layer before hardware is used in production. The matrix says venues may select their hardware, while the provider must expose hardware limitations and recommendations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `DEVICE_MANAGE`, `DEVICE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `deviceId` (navigation) |
| Route | `/access-venue/hardware-compatibility-health-testing-deployment-bo-203` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The go-live gate for access hardware: a capability matrix (which device can do Dynamic QR, RFID, NFC, Face Pass, offline, height check), a hardware test bench run with a test credential, the certification stage of each device, and deployment of a configuration version to a pilot, selected gates, a device group or the venue. The one thing to get right: no device reaches production without a passed test, and every deployment says which devices will be skipped and why before it starts.

**Known correction pending (do not draw the wrong version)**

- **Action bar buttons "Selected gates", "device group" and "venue"** Why: These are the values of the deployment target, turned into buttons; draw one target choice inside the deploy dialog. *(source: contracts/spine/access.yaml#publishHardwareDeployment / screens/P08-venue-back-office.yaml#BO-203; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **lifecycleStatus registered > configured > tested > approved > production is a second device lifecycle** Why: ADR-0067 keeps one lifecycle in the platform device register and turns Access's stages into a checklist on the placement; show certification as that checklist. *(source: ADR-0067 / contracts/spine/access.yaml#listHardwareCompatibilityHealth; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation runs a hardware test or stores its result, and the matrix has no "required by configuration" mark** Why: The pack's test bench and the "Compatibility gap" example need both; MoM 2 Sep asks for media testing per gate before go-live. *(source: screens/P08-venue-back-office.yaml#BO-203 / DI-639; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Rollback is in the pack's deployment support list but has no operation** Why: Needed to undo a bad rollout. *(source: screens/P08-venue-back-office.yaml#BO-203 / DI-903; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who approves a device into production (Approved stage), and is it a separate person from the one who tested it?** → A device's approver into production must differ from the person who tested it. *(decided by Chinmay, 2026-10-02; DEC-245 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Form: Approve into production** (modal, opened by *Approve into production*; *Approve into production* calls `approveDevice`, *Cancel* sends nothing)

**Collects what `approveDevice` sends before it is called.** Required: `decision`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Reject | — | — | `approveDevice` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required to reject. | `approveDevice` body |

Errors to draw in the form: 403 The caller recorded the device's acceptance test or registered it (`approver-is-tester`).; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The device is not awaiting approval (`device-not-pending-approval`), or has no recorded acceptance test yet (`device-not-tested`).

**Sent by *Deploy configuration version*** (`publishHardwareDeployment`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated deployment id | `publishHardwareDeployment` body |
| Configuration version `configurationVersion` | text field | required | — | — | — | The access configuration version being deployed | `publishHardwareDeployment` body |
| Target scope `targetScope` | radio group | required | — | Pilot · Selected gates · Device group · Venue | — | — | `publishHardwareDeployment` body |
| Venue `venueId` | text field | required | — | — | — | — | `publishHardwareDeployment` body |
| Gates `gateIds` | list of values (chips) | optional | — | — | — | Required for pilot and selectedGates | `publishHardwareDeployment` body |
| Device group `deviceGroupId` | text field | optional | — | — | — | Required for deviceGroup | `publishHardwareDeployment` body |
| Run compatibility test first `runCompatibilityTestFirst` | toggle | optional | on | — | — | Devices that fail the compatibility test are skipped and named in the result | `publishHardwareDeployment` body |
| Scheduled at `scheduledAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Empty deploys now | `publishHardwareDeployment` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Deployment target (targetScope, gateIds, deviceGroupId)**: A segmented choice Pilot / Selected gates / Device group / Venue; gates are picked on the topology tree (required for Pilot and Selected gates), a device group from BO-151 (required for Device group); Venue needs nothing more. *(source: contracts/spine/access.yaml#publishHardwareDeployment)*
- **configurationVersion**: Picker of saved configuration versions (from BO-202), newest first, with its stage; not typed. *(source: contracts/spine/access.yaml#publishHardwareDeployment)*
- **runCompatibilityTestFirst / scheduledAt**: "Test compatibility first" on by default and only switchable off by someone with access configuration rights, with a warning; "When" = Now or a date and time in venue time (scheduled rollout). *(source: screens/P08-venue-back-office.yaml#BO-203 / contracts/spine/access.yaml#publishHardwareDeployment)*
- **id**: The deployment id is generated by the screen once per attempt (so a double click cannot deploy twice); never shown. *(source: contracts/spine/access.yaml#publishHardwareDeployment)*
- **Test credential**: For the test bench: pick a test ticket (a test product's ticket, never a live guest's) and the tests to run (Reader, Gate open/close, Light, Sound, Display, RFID, NFC, Biometric, Offline, Emergency mode, End to end). *(source: screens/P08-venue-back-office.yaml#BO-203)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Selected gates (primary button) | navigation or local | — | — | — | — |
| device group (secondary button) | navigation or local | — | — | — | — |
| venue (secondary button) | navigation or local | — | — | — | — |
| Deploy configuration version (publish gate) | `publishHardwareDeployment` POST `/hardware-deployments` | HardwareDeploymentInput | HardwareDeploymentView | 409 A deployment to an overlapping target set is still queued or in progress; 422 gateIds or deviceGroupId missing for the chosen targetScope | — |
| Approve into production (primary button) | `approveDevice` POST `/devices/{deviceId}/approval` | inline | RegisteredDevice | 403 The caller recorded the device's acceptance test or registered it (`approver-is-tester`).; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The device is … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Compatibility matrix**: Capabilities as rows, devices as columns (Gate A, Gate B, HH-01, VIP-01), a tick, a dash for not supported, and an amber mark where a configured rule needs a capability the device lacks ("Face Pass policy at Falcon Coaster gate - reader has no camera"). Never a flat table of device rows. *(source: screens/P08-venue-back-office.yaml#BO-203 / contracts/spine/access.yaml#listHardwareCompatibilityHealth)*
- **End-to-end test result**: The nine steps as a vertical checklist (Credential read, Virtual credential resolved, Access rule evaluated, Entitlement checked, Decision returned, Light/sound triggered, Gate opened, Attendance updated, Audit created) with time per step and the failing step in red. *(source: screens/P08-venue-back-office.yaml#BO-203)*
- **Certification stage**: Per device a stage chip and the last test date; Approved needs a passed test, Production needs Approved. *(source: screens/P08-venue-back-office.yaml#BO-203 / contracts/spine/access.yaml#listHardwareCompatibilityHealth)*
- **Health**: Connectivity, average validation time against target ("1.8 s vs 0.9 s target"), CPU, memory, storage, temperature and battery where the vendor SDK provides it, read from the one device register. *(source: DI-899 / DI-901 / DI-900 / ADR-0067)*
- **AI hardware advisor**: Suggestions with their reason (throughput risk, compatibility gap) and an Open device action; nothing changes on its own. *(source: screens/P08-venue-back-office.yaml#BO-203)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Run tests**: Runs the selected tests against the device with the test credential; no guest attendance is recorded. Drawn greyed (no operation). *(source: screens/P08-venue-back-office.yaml#BO-203 / DI-639)*
- **Deploy configuration version**: Confirmation names the version, the target and the devices that failed compatibility and will be skipped; afterwards progress "78 / 80 devices updated, 2 devices offline". A deployment is a new record each time, so redeploying the same version keeps both in the history. *(source: screens/P08-venue-back-office.yaml#BO-203 / contracts/spine/access.yaml#publishHardwareDeployment)*

**Data it reads**: `listHardwareCompatibilityHealth` (onLoad, Hardware Compatibility, Health, Testing & Deployment)

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Device & Gate Command Center*; carries `deviceId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hardware compatibility health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hardware compatibility health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hardware compatibility health yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hardware compatibility health are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A deployment to an overlapping target set is still queued or in progress; 409 The device is not awaiting approval (`device-not-pending-approval`), or has no recorded acceptance test yet (`device-not-tested`).; 422 gateIds or deviceGroupId missing for the chosen targetScope |

#### Edge cases to draw

- **Device fails compatibility during a deployment**: It is skipped and named in the result (failedDeviceIds) with the failing capability; the rest proceed. *(source: contracts/spine/access.yaml#publishHardwareDeployment)*
- **Scheduled deployment**: Shows as Scheduled with its time and Cancel; devices take it at their next package refresh after that time. *(source: contracts/spine/access.yaml#publishHardwareDeployment)*
- **Battery not readable for a model**: Show "Not reported by this model" rather than 0% or empty. *(source: DI-900)*
- **The tester tries to approve the device**: Refused: the approver into production must differ from the person who tested it. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

#### Consistency with other screens

- Match `BO-194`: Device health and status come from the same device register and use the same words.
- Match `BO-183`: Media compatibility testing per gate (DI-639) and this matrix should be one matrix; this screen is the device side.
- Match `BO-202`: Same deployment operation and target words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
- capability: Dynamic QR
  gateA: true
  gateB: true
  HH-01: true
  VIP-01: true
- capability: Face Pass
  gateA: true
  gateB: '-'
  HH-01: true
  VIP-01: true
- capability: Height check
  gateA: '-'
  gateB: true
  HH-01: '-'
  VIP-01: '-'
deployment:
  version: Main Plaza v12
  target: Device group Main Plaza Gates 1-3
  scheduled: 2 Oct 2026 02:00
  skipped: MG-06 (no NFC reader)
advisor: Gate MG-06 averages 1.8 s per QR validation against the 0.9 s target
```

#### Permissions

- `listHardwareCompatibilityHealth` → `DEVICE_VIEW` (read) · staff
- `publishHardwareDeployment` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `approveDevice` → `DEVICE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Device analytics: total/active/inactive devices across venues (multi-tenant) with location breakdown; health, availability, fault rate and top failure reasons (communication timeout, device offline, invalid response, power issue, firmware error); SLA tracking for devices in extended maintenance. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-905)*
- **Open question.** Open (Allam): physical tamper detection - lock out communication if a device is opened, as bank payment terminals do - worth evaluating per device type; not a requirement for every device. *(open · MoM 15 Sep 2026, 4.8 Device Security & Governance · DI-904)*
- Device maintenance: preventive cycles (quarterly, half-yearly, seasonal) on a calendar by device type; staff log faulty devices which raise work orders; diagnostic workspace for the engineer; warranty and maintenance history; return to service. *(client request · MoM 15 Sep 2026, 4.6 Device Maintenance & Lifecycle Servicing · DI-902)*
- Performance monitoring shows successful vs failed validations and scan response time; configurable alert rules (e.g. low battery, device offline) with escalation for unresolved alerts. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-901)*
- **Open question.** Open: can health metrics such as handheld battery be read via the manufacturer's SDK in-app rather than by physical inspection? Depends on each vendor SDK; to confirm during integration. *(open · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-900)*
- One screen shows live online/offline status of every workstation and device (printers, turnstiles, handheld scanners); a 360 health view shows connectivity, CPU/memory, storage and temperature. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-899)*
- Media compatibility testing validates that each supported media type works at each gate/device before go-live. *(client request · MoM 2 Sep 2026, 4.9 Media & Credential Configuration · DI-639)*
- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-203` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-203`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 18: Works in Hardware Compatibility, Health, Testing & Deployment → Provide the final testing and governance layer before hardware is used in production. The matrix says venues may select their hardware, while the provider must expose hardware limitations and …

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-203?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Selected gates, device group, venue, Deploy configuration version, Approve into production.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `DEVICE_MANAGE`, `DEVICE_VIEW`.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
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

**33 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveDevice": {"method":"POST","path":"/devices/{deviceId}/approval","contract":"tenancy","summary":"Approve a device into production, or reject it","permission":"DEVICE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RegisteredDevice"},
"enrolDevice": {"method":"POST","path":"/devices/{deviceId}/enrolment","contract":"tenancy","summary":"Take a registered device through enrolment to activation","permission":"DEVICE_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceEnrolment","responds":"RegisteredDevice"},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDeviceGate": {"method":"GET","path":"/device-gate","contract":"access","summary":"Device & Gate Command Center","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDeviceTypeHardware": {"method":"GET","path":"/device-type-hardware","contract":"access","summary":"Device Type & Hardware Library","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeviceTypeHardwareLibraryView"},
"listGateModeFree": {"method":"GET","path":"/gate-mode-free","contract":"access","summary":"Gate Modes, Free Spin & Emergency Controls","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GateModesFreeSpinEmergencyControlsView"},
"listHardwareCompatibilityHealth": {"method":"GET","path":"/hardware-compatibility-health","contract":"access","summary":"Hardware Compatibility, Health, Testing & Deployment","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPhysicalDeviceRegistration": {"method":"GET","path":"/physical-device-registration","contract":"access","summary":"Physical Device Registration & Provisioning","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"placeAccessDevice": {"method":"POST","path":"/device-placements","contract":"access","summary":"Place a registered device in the gate topology","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessDevicePlacement","responds":"AccessDevicePlacement"},
"publishHardwareDeployment": {"method":"POST","path":"/hardware-deployments","contract":"access","summary":"Deploy a gate configuration version","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"HardwareDeploymentInput","responds":"HardwareDeploymentView"},
"registerDevice": {"method":"POST","path":"/devices","contract":"tenancy","summary":"Register a device","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegisteredDevice","responds":"RegisteredDevice"},
"setDeviceSoftwareContent": {"method":"PUT","path":"/device-software-content","contract":"access","summary":"Device Software, Content & Remote Configuration","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceSoftwareContentRemoteConfigurationInput","responds":"DeviceSoftwareContentRemoteConfigurationView"},
"setGateModePolicy": {"method":"PUT","path":"/gate-mode-policies","contract":"access","summary":"Set a policy for a non-standard gate mode","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessGateModePolicy","responds":"AccessGateModePolicy"},
"setHandheldMobileAccess": {"method":"PUT","path":"/handheld-mobile-access","contract":"access","summary":"Handheld & Mobile Access Device Configuration","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"HandheldMobileAccessDeviceConfigurationInput","responds":"HandheldMobileAccessDeviceConfigurationView"},
"setHardwareModel": {"method":"PUT","path":"/hardware-models","contract":"access","summary":"Create or replace a hardware model in the library","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessHardwareModel","responds":"AccessHardwareModel"},
"setReaderScannerPeripheral": {"method":"PUT","path":"/reader-scanner-peripheral","contract":"access","summary":"Reader, Scanner & Peripheral Configuration","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReaderScannerPeripheralConfigurationInput","responds":"ReaderScannerPeripheralConfigurationView"},
"setTurnstileLaneBehavior": {"method":"PUT","path":"/turnstile-lane-behavior","contract":"access","summary":"Turnstile & Lane Behavior Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TurnstileLaneBehaviorConfigurationInput","responds":"TurnstileLaneBehaviorConfigurationView"},
"setValidationOutcomeGuest": {"method":"PUT","path":"/validation-outcome-guest","contract":"access","summary":"Validation Outcome & Guest Feedback Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ValidationOutcomeGuestFeedbackDesignerInput","responds":"ValidationOutcomeGuestFeedbackDesignerView"},
"updateAccessDevicePlacement": {"method":"PUT","path":"/device-placements/{placementId}","contract":"access","summary":"Replace a device's placement","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessDevicePlacement","responds":"AccessDevicePlacement"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessDevicePlacement": {"type":"object","x-ticvai-persistence":"access.device_placement","description":"**Where one registered device is placed in the gate topology, and nothing else about it** (ADR-0067, accepted 1 October). The device itself (kind and hardware type, hardware model, serial, every version, health, heartbeat and its one lifecycle) is `platform.device`, the only device register, owned and migrated by Tenancy and registered with tenancy `registerDevice`. This row names that device (`deviceId`) and says which access area, access point and lane it serves, in what role, at what proximity threshold for a beacon, and through which controller. Access reads device facts only through what Tenancy publishes (`getDevice`, `listDevices`), never with its own SQL.\n\n**Access's provisioning stages are a checklist on the placement, not a second lifecycle** (`provisioningChecklist`). Placed with `placeAccessDevice` and changed with `updateAccessDevicePlacement`. Was `access.access_device` (renamed 1 October, ADR-0067), which repeated the register's serial, versions, health and lifecycle; `device.enrolmentChanged` no longer keeps two registers in step. Not `access.device_binding`, which binds a guest's phone to an entitlement. `deviceGroupId` is a free deployment label, not a key (decided 29 September, writers pass).","required":["id","venueId","deviceId","role","isActive","scopePath"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"venueId":{"type":"string","format":"uuid"},"deviceId":{"type":"string","format":"uuid","x-ticvai-references":"platform.device","description":"The registered device placed here (`platform.device`, tenancy `registerDevice`). One active placement per device; replacing a failed unit gives its placement the new `deviceId`."},"accessAreaId":{"type":"string","format":"uuid","nullable":true,"description":"Most specific park, zone or attraction the device sits in (access.access_area)"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Access point (gate) the device serves"},"gateLaneId":{"type":"string","format":"uuid","nullable":true,"description":"Lane the device is mounted on (access.gate_lane)"},"role":{"type":"string","enum":["entry","exit","entryAndExit","validationOnly","proximity","monitoring"],"default":"entryAndExit","description":"What the device does at this place. `proximity` is a beacon; `monitoring` a camera controller that decides nothing."},"name":{"type":"string","nullable":true,"description":"Label at this place, e.g. Gate A, HH-01"},"deviceGroupId":{"type":"string","nullable":true,"description":"Device group the placement belongs to, as targeted by hardware deployments and device configurations"},"controllerReference":{"type":"string","nullable":true},"proximityThresholdMeters":{"type":"integer","minimum":0,"nullable":true,"description":"Beacons only: activation distance in metres"},"installationDate":{"type":"string","format":"date","nullable":true},"provisioningChecklist":{"type":"object","description":"**Access's provisioning stages, as a checklist on the placement** (ADR-0067). Each item is the time the step was confirmed, null until it is. The device's lifecycle (registered, enrolled, provisioned, active, deactivated, retired) is `platform.device.enrolment_state`, not this.","properties":{"hardwareProfileAssignedAt":{"type":"string","format":"date-time","nullable":true},"locationAssignedAt":{"type":"string","format":"date-time","nullable":true},"authenticatedAt":{"type":"string","format":"date-time","nullable":true},"configurationDownloadedAt":{"type":"string","format":"date-time","nullable":true},"securityPackageDownloadedAt":{"type":"string","format":"date-time","nullable":true},"connectivityTestedAt":{"type":"string","format":"date-time","nullable":true}}},"isActive":{"type":"boolean","default":true,"description":"Whether this placement is in use (beacons: activeInactive). A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says."},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessGateModePolicy": {"type":"object","x-ticvai-persistence":"access.gate_mode_policy","description":"One policy for a non-standard gate mode (free spin or count only as freeFlow, emergency as dropArm): who may activate it, on which gate group, whether a reason is required, emergency code, notification and incident creation (declared 29 September, data-model close-out DM1)","required":["id","venueId","mode","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"mode":{"type":"string","enum":["freeFlow","dropArm"],"description":"Non-standard operating mode governed (R221 vocabulary)"},"whoCanActivate":{"type":"array","items":{"type":"string"},"description":"Roles allowed to activate this mode"},"accessPointGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Gate group the policy applies to (access.access_point_group); null for the whole venue"},"reasonRequired":{"type":"boolean","default":true},"emergencyCode":{"type":"string","nullable":true},"automaticNotification":{"type":"boolean","default":false},"createsIncident":{"type":"boolean","default":false,"description":"Activation creates an incident record"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessHardwareModel": {"type":"object","x-ticvai-persistence":"access.hardware_model","description":"One hardware model in the reusable library, independent of deployed devices: manufacturer, model, category and type, supported technologies, connectivity, capability flags and firmware information (declared 29 September, data-model close-out DM1)","required":["id","manufacturer","model","deviceCategory","hardwareType","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"manufacturer":{"type":"string"},"model":{"type":"string"},"deviceCategory":{"type":"string","enum":["turnstile","specialGate","mobile","reader","other"]},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType"},"supportedTechnologies":{"type":"array","items":{"type":"string"}},"connectivity":{"type":"array","items":{"type":"string"}},"offlineCapability":{"type":"boolean","default":false},"screenCapability":{"type":"boolean","default":false},"soundCapability":{"type":"boolean","default":false},"lightCapability":{"type":"boolean","default":false},"relayControllerSupport":{"type":"boolean","default":false},"paymentCapability":{"type":"boolean","default":false,"description":"Payment capability where available"},"firmwareSoftwareInformation":{"type":"string","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n\n**R221 amended 2 October 2026: a gate's direction can be switched live** (Chinmay, critical set 1, BO-230: \"Live direction switch with permission, logged\"; DEC-255; CHG-CSP-032; DI-648: more entry gates in the morning, more exit gates in the evening). `setAccessPointDirection` switches it from Live Gate Mode & Lane Control (BO-230) or the scanner's gate mode screen (SCN-016) for a holder of the configuration right, logged; the podium's `setTurnstileMode` still never touches it.\n"},"temporaryClosure":{"type":"object","nullable":true,"description":"**What the access point does while its attraction is temporarily closed** (decided 2 October 2026, Chinmay, batch 6 set 9, BO-147: \"Deny + reopening time + a virtual-queue return window where enabled\"; DEC-228; CHG-CSP-026). While `isClosed`, every scan is denied (`ValidationResult.denyCause` `attractionTemporarilyClosed`) with the reopening time when it is known; where the venue offers it and the attraction has a virtual queue, the guest is offered a return window (`queue.joinQueue`) instead of being turned away empty-handed. Set with `updateAccessPoint`; null when open. Travels in the offline package, so an offline gate denies the same way.","properties":{"isClosed":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":200,"nullable":true,"description":"Shown to staff; the guest sees \"Attraction temporarily closed\"."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When it is expected to reopen; shown to the guest when known."},"offerVirtualQueueReturn":{"type":"boolean","default":false,"description":"Offer a virtual-queue return window at the denied scan, where the attraction has a queue."},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The virtual queue the return window is taken in."}}},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"DeviceApprovalStatus": {"type":"string","description":"Whether a registered device may go into production (DEC-241, DEC-245; CHG-CSP-011). The model is `states/registered-device-approval.yaml`.\n","enum":["pendingApproval","approved","rejected"]},
"DeviceCapability": {"type":"string","description":"BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n","enum":["genderClassification","dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},
"DeviceEnrolment": {"x-ticvai-persistence":"platform.device","type":"object","description":"BL-160. **The body `enrolDevice` accepts, named so that it writes.**\nIt was an anonymous inline object, and `derive-lineage` reads writes from the schema an operation accepts — so the one operation that moves a device through its whole lifecycle recorded no writes at all, and `platform.device` looked like a table only `registerDevice` touched.\n**Provisioning is inside enrolment rather than beside it**, which is why `configurationProfileId` is here: a device that is enrolled but unprovisioned is a device that will fail at the gate on its first morning.\n","required":["state"],"properties":{"state":{"type":"string","enum":["enrolled","provisioned","active","deactivated","retired"],"description":"**The target state, not the current one.** `registered` is absent because `registerDevice` is what produces it and nothing transitions back to it.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true,"description":"**Recorded on the `tenancy.device_audit` row, not on the device.** Required in practice for `deactivated` and `retired`, where an investigation six months later needs to know why a gate stopped working.\n"},"enrolmentCode":{"type":"string","nullable":true,"maxLength":12,"writeOnly":true,"description":"**The one-time code `registerDevice` issued, as the device presents it** (DEC-241; CHG-CSP-011). Needed on the move to `enrolled`; a wrong or expired code is `422 enrolment-code-invalid`, and the code is spent on success.\n"},"testResult":{"type":"object","nullable":true,"description":"**The acceptance test, recorded on the move to `provisioned`** (DEC-245; CHG-CSP-011). The caller is recorded as `RegisteredDevice.testedByPrincipalId` and may not approve the device.\n","properties":{"passed":{"type":"boolean","description":"Whether the device passed; always sent with `testResult` (422 otherwise)."},"notes":{"type":"string","maxLength":1000,"nullable":true}}}}},
"DeviceGateCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Device & Gate Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"connectivity":{"type":"string","description":"connectivity"},"lastHeartbeat":{"type":"string","format":"date-time","description":"last heartbeat"},"configurationVersion":{"type":"string","description":"configuration version"},"localRuleVersion":{"type":"string","description":"local rule version"},"credentialSecurityPackageVersion":{"type":"string","description":"credential/security package version"},"scannerHealth":{"type":"string","description":"scanner health"},"controllerHealth":{"type":"string","description":"controller health"},"cameraHealthWhereApplicable":{"type":"string","description":"camera health where applicable"},"deviceId":{"type":"string"},"deviceType":{"type":"string","description":"e.g. Turnstile, VIP Gate, Handheld, Reader"},"accessPointId":{"type":"string"},"mode":{"type":"string","description":"Current operating mode"},"status":{"type":"string","enum":["healthy","active","degraded","offline","localMode"]}}},
"DeviceGateCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"totalDevices":{"type":"integer","description":"Total Devices"},"online":{"type":"integer","description":"Online"},"offline":{"type":"integer","description":"Offline"},"degraded":{"type":"integer","description":"Degraded"},"turnstiles":{"type":"integer","description":"Turnstiles"},"handhelds":{"type":"integer","description":"Handhelds"},"biometricReaders":{"type":"integer","description":"Biometric Readers"},"rfidNfcReaders":{"type":"integer","description":"RFID/NFC Readers"},"gatesOpen":{"type":"integer","description":"Gates Open"},"gatesClosed":{"type":"integer","description":"Gates Closed"},"devicesRequiringSync":{"type":"integer","description":"Devices Requiring Sync"},"firmwareSoftwareExceptions":{"type":"integer","description":"Firmware/Software Exceptions"},"hardwareAlerts":{"type":"integer","description":"Hardware Alerts"},"ai":{"type":"array","items":{"type":"string"},"description":"Advisory AI findings, e.g. a gate with a high scan-failure rate. Read-only."}}},
"DeviceKind": {"type":"string","enum":["receiptPrinter","ticketPrinter","labelPrinter","cashDrawer","barcodeScanner","rfidReader","nfcReader","cardReader","idReader","biometricReader","accessReader","paymentTerminal","customerDisplay","signageDisplay","kitchenDisplay","turnstileController","wristbandEncoder","signaturePad","scale","camera","mobileHandset","handheldScanner","accessPodium","bleBeacon"],"description":"`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"},
"DeviceSoftwareContentRemoteConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Device Software, Content & Remote Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"deviceGroupId":{"type":"string","description":"Target device group"},"venueId":{"type":"string"},"configurationId":{"type":"string"},"deviceSettings":{"type":"string","description":"Device settings"},"gateMode":{"type":"string","description":"Gate mode"},"readerSettings":{"type":"string","description":"Reader settings"},"mediaProfiles":{"type":"array","items":{"type":"string"},"description":"Media profiles"},"outcomeProfiles":{"type":"array","items":{"type":"string"},"description":"Outcome profiles"},"language":{"type":"string","description":"Language"},"uiContent":{"type":"string","description":"UI content"},"localRules":{"type":"string","description":"Local rules"},"offlineSecurityConfiguration":{"type":"string","description":"Offline security package reference"},"welcomePage":{"type":"string","description":"Welcome page"},"instructions":{"type":"string","description":"Instructions"},"ticketStatus":{"type":"string","description":"Ticket status"},"reasonMessage":{"type":"string","description":"Reason message"},"promotionalInformation":{"type":"string","description":"Promotional information"},"externalApprovedWebpage":{"type":"string","description":"External approved webpage"},"emergencyInformation":{"type":"string","description":"Emergency information"},"version":{"type":"string","description":"Configuration version, for rollback"},"deploymentStage":{"type":"string","enum":["draft","testDevice","deviceGroup","venueRollout"]}},"required":["configurationId","venueId","deviceGroupId"]},
"DeviceSoftwareContentRemoteConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Device Software, Content & Remote Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"deviceGroupId":{"type":"string","description":"Target device group"},"venueId":{"type":"string"},"configurationId":{"type":"string"},"deviceSettings":{"type":"string","description":"Device settings"},"gateMode":{"type":"string","description":"Gate mode"},"readerSettings":{"type":"string","description":"Reader settings"},"mediaProfiles":{"type":"array","items":{"type":"string"},"description":"Media profiles"},"outcomeProfiles":{"type":"array","items":{"type":"string"},"description":"Outcome profiles"},"language":{"type":"string","description":"Language"},"uiContent":{"type":"string","description":"UI content"},"localRules":{"type":"string","description":"Local rules"},"offlineSecurityConfiguration":{"type":"string","description":"Offline security package reference"},"welcomePage":{"type":"string","description":"Welcome page"},"instructions":{"type":"string","description":"Instructions"},"ticketStatus":{"type":"string","description":"Ticket status"},"reasonMessage":{"type":"string","description":"Reason message"},"promotionalInformation":{"type":"string","description":"Promotional information"},"externalApprovedWebpage":{"type":"string","description":"External approved webpage"},"emergencyInformation":{"type":"string","description":"Emergency information"},"version":{"type":"string","description":"Configuration version, for rollback"},"deploymentStage":{"type":"string","enum":["draft","testDevice","deviceGroup","venueRollout"]}},"required":["configurationId","venueId","deviceGroupId"]},
"DeviceTypeHardwareLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Device Type & Hardware Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"hardwareType":{"type":"string","enum":["standardTurnstile","fullHeightTurnstile","tripodTurnstile","speedGate","wideLane","accessiblePodGate","buggyGate","vipGate","staffGate","androidHandheld","iosDevice","tablet","qrBarcodeReader","rfidReader","nfcReader","multiTechnologyReader","biometricReader","podium","counter","beacon","cameraController","externalAccessDevice"],"description":"Specific hardware type within the device category"},"manufacturer":{"type":"string","description":"Manufacturer"},"model":{"type":"string","description":"Model"},"deviceCategory":{"type":"string","enum":["turnstile","specialGate","mobile","reader","other"],"description":"Device Category"},"supportedTechnologies":{"type":"array","items":{"type":"string"},"description":"Supported technologies"},"connectivity":{"type":"array","items":{"type":"string"},"description":"Connectivity"},"offlineCapability":{"type":"boolean","description":"Offline capability"},"screenCapability":{"type":"boolean","description":"Screen capability"},"soundCapability":{"type":"boolean","description":"Sound capability"},"lightCapability":{"type":"boolean","description":"Light capability"},"relayControllerSupport":{"type":"boolean","description":"Relay/controller support"},"paymentCapabilityWhereAvailable":{"type":"boolean","description":"payment capability where available"},"firmwareSoftwareInformation":{"type":"string","description":"firmware/software information"},"hardwareModelId":{"type":"string"}}},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"GateModesFreeSpinEmergencyControlsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Gate Modes, Free Spin & Emergency Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"whoCanActivate":{"type":"array","items":{"type":"string"},"description":"Roles allowed to activate this mode"},"venueScope":{"type":"string","description":"Venue scope"},"gateGroup":{"type":"string","description":"Gate group"},"reasonRequired":{"type":"string","description":"reason"},"emergencyCode":{"type":"string","description":"emergency code"},"automaticNotification":{"type":"boolean","description":"automatic notification"},"incidentRecord":{"type":"boolean","description":"Activation creates an incident record"},"policyId":{"type":"string"},"mode":{"type":"string","enum":["freeFlow","dropArm"],"description":"Non-standard operating mode this policy governs (R221 vocabulary): freeFlow covers free spin and count only, dropArm is the emergency mode"}}},
"HandheldMobileAccessDeviceConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Handheld & Mobile Access Device Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"name":{"type":"string","description":"e.g. Standard Attendant, Supervisor"},"profileId":{"type":"string","description":"Handheld configuration profile identifier"},"deviceType":{"type":"string","description":"Device type"},"platform":{"type":"string","enum":["android","ios"],"description":"Android/iOS"},"assignedVenue":{"type":"string","description":"assigned venue"},"assignedZone":{"type":"string","description":"assigned zone"},"assignedOperatorGroup":{"type":"string","description":"assigned operator group"},"permittedOperatingModes":{"type":"array","items":{"type":"string"},"description":"permitted operating modes"},"offlineCapability":{"type":"boolean","description":"offline capability"},"scannerSource":{"type":"string","description":"scanner source"},"biometricCapabilityWhereSupported":{"type":"boolean","description":"biometric capability where supported"},"enabledFunctions":{"type":"array","items":{"type":"string","enum":["scanTicket","searchTicket","entry","exit","reEntry","crossover","groupAdmission","manualAttendance","override","viewHistory","changeDeviceMode"]},"description":"Functions enabled for this device role"}},"required":["profileId","name"]},
"HandheldMobileAccessDeviceConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Handheld & Mobile Access Device Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"e.g. Standard Attendant, Supervisor"},"profileId":{"type":"string","description":"Handheld configuration profile identifier"},"deviceType":{"type":"string","description":"Device type"},"platform":{"type":"string","enum":["android","ios"],"description":"Android/iOS"},"assignedVenue":{"type":"string","description":"assigned venue"},"assignedZone":{"type":"string","description":"assigned zone"},"assignedOperatorGroup":{"type":"string","description":"assigned operator group"},"permittedOperatingModes":{"type":"array","items":{"type":"string"},"description":"permitted operating modes"},"offlineCapability":{"type":"boolean","description":"offline capability"},"scannerSource":{"type":"string","description":"scanner source"},"biometricCapabilityWhereSupported":{"type":"boolean","description":"biometric capability where supported"},"enabledFunctions":{"type":"array","items":{"type":"string","enum":["scanTicket","searchTicket","entry","exit","reEntry","crossover","groupAdmission","manualAttendance","override","viewHistory","changeDeviceMode"]},"description":"Functions enabled for this device role"}},"required":["profileId","name"]},
"HardwareCompatibilityHealthTestingDeploymentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Hardware Compatibility, Health, Testing & Deployment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"deviceId":{"type":"string","description":"Device identifier"},"capabilities":{"type":"array","items":{"type":"string","enum":["dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},"description":"Capabilities this device supports, from the compatibility matrix"},"rolloutScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"],"description":"How far the production rollout of this device reaches"},"deviceName":{"type":"string","description":"Device or gate name, e.g. Gate A, HH-01"},"lifecycleStatus":{"type":"string","enum":["registered","configured","tested","approved","production"],"description":"Certification stage; no device enters production until validated"}},"required":["deviceId"]},
"HardwareDeploymentInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Deploy one gate configuration version to a target set (decided 29 September, VM close-out).","required":["id","configurationVersion","targetScope","venueId"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated deployment id"},"configurationVersion":{"type":"string","description":"The access configuration version being deployed"},"targetScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"]},"venueId":{"type":"string"},"gateIds":{"type":"array","items":{"type":"string"},"description":"Required for pilot and selectedGates"},"deviceGroupId":{"type":"string","description":"Required for deviceGroup"},"runCompatibilityTestFirst":{"type":"boolean","default":true,"description":"Devices that fail the compatibility test are skipped and named in the result"},"scheduledAt":{"type":"string","format":"date-time","description":"Empty deploys now"}}},
"HardwareDeploymentView": {"type":"object","x-ticvai-persistence":"access.hardware_deployment","description":"**One rollout of one gate configuration version to one target set** (decided 29 September, VM close-out). The lifecycle is the one `tenancy.ProfileDeployment` uses for configuration profiles, so a partial failure is visible and retried or rolled back, never an end state.","required":["id","configurationVersion","targetScope","status"],"properties":{"id":{"type":"string","format":"uuid"},"configurationVersion":{"type":"string"},"targetScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"]},"venueId":{"type":"string"},"gateIds":{"type":"array","items":{"type":"string"}},"deviceGroupId":{"type":"string"},"status":{"type":"string","enum":["queued","inProgress","completed","partiallyFailed","rolledBack"]},"devicesTargeted":{"type":"integer"},"devicesAcknowledged":{"type":"integer"},"failedDeviceIds":{"type":"array","items":{"type":"string"},"description":"Devices that failed the compatibility test or did not acknowledge"},"requestedByPrincipalId":{"type":"string"},"requestedAt":{"type":"string","format":"date-time"},"scheduledAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"The partition key (ADR-0005). Written at venue scope"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PhysicalDeviceRegistrationProvisioningView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Physical Device Registration & Provisioning displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"deviceId":{"type":"string","description":"Device ID"},"serialNumber":{"type":"string","description":"Serial Number"},"hardwareModel":{"type":"string","description":"Hardware Model"},"manufacturer":{"type":"string","description":"Manufacturer"},"tenantId":{"type":"string","description":"Tenant"},"venueId":{"type":"string","description":"Venue"},"parkId":{"type":"string","description":"Park"},"zoneId":{"type":"string","description":"Zone"},"accessPointId":{"type":"string","description":"Access Point"},"gateLane":{"type":"string","description":"Gate/Lane"},"ipNetworkReference":{"type":"string","description":"IP/network reference"},"controllerReference":{"type":"string","description":"controller reference"},"installationDate":{"type":"string","format":"date","description":"installation date"},"provisioningStage":{"type":"string","enum":["registered","hardwareProfileAssigned","locationAssigned","authenticated","configurationDownloaded","securityPackageDownloaded","connectivityTested","active"]}}},
"ReaderScannerPeripheralConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Reader, Scanner & Peripheral Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"accessPointId":{"type":"string","description":"Gate or device the peripherals attach to"},"readers":{"type":"array","items":{"type":"string"},"description":"Attached readers, e.g. qrBarcode, rfid, nfc, biometricCamera, paymentReader, heightSensor"},"verificationPriority":{"type":"array","items":{"type":"string"},"description":"Order methods are tried, e.g. facePass, dynamicQr, rfid, nfc"},"rfidRange":{"type":"string","enum":["near","medium","far"]},"heightVerificationEnabled":{"type":"boolean","description":"Height check for junior tickets; without a supported sensor the result is yellow for operator verification"},"capabilityWarnings":{"type":"array","items":{"type":"string"},"description":"Configured checks the attached hardware cannot perform"}},"required":["accessPointId"]},
"ReaderScannerPeripheralConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Reader, Scanner & Peripheral Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"accessPointId":{"type":"string","description":"Gate or device the peripherals attach to"},"readers":{"type":"array","items":{"type":"string"},"description":"Attached readers, e.g. qrBarcode, rfid, nfc, biometricCamera, paymentReader, heightSensor"},"verificationPriority":{"type":"array","items":{"type":"string"},"description":"Order methods are tried, e.g. facePass, dynamicQr, rfid, nfc"},"rfidRange":{"type":"string","enum":["near","medium","far"]},"heightVerificationEnabled":{"type":"boolean","description":"Height check for junior tickets; without a supported sensor the result is yellow for operator verification"},"capabilityWarnings":{"type":"array","items":{"type":"string"},"description":"Configured checks the attached hardware cannot perform"}},"required":["accessPointId"]},
"RegisteredDevice": {"x-ticvai-persistence":"platform.device","type":"object","description":"**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n","required":["id","kind","driver"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"},"identifier":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"},"model":{"type":"string","nullable":true},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType","nullable":true,"description":"**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"},"hardwareModelId":{"type":"string","format":"uuid","nullable":true,"description":"The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"},"serialNumber":{"type":"string","nullable":true,"maxLength":100,"description":"The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"},"ipNetworkReference":{"type":"string","nullable":true,"description":"Network address or reference the device is reached at (ADR-0067)."},"configurationVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Access configuration version the device reports running (ADR-0067)."},"localRuleVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Admission rule package the device reports running (ADR-0067)."},"credentialSecurityPackageVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Credential security package the device reports running (ADR-0067)."},"scannerHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Component health as the device or vendor reports it on its heartbeat (ADR-0067)."},"controllerHealth":{"type":"string","nullable":true,"readOnly":true},"cameraHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Where the device has a camera."},"connectivity":{"type":"string","nullable":true,"readOnly":true,"description":"Reported connectivity."},"pushToken":{"type":"string","format":"password","nullable":true,"writeOnly":true,"description":"BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"},"pushPlatform":{"type":"string","nullable":true,"enum":["ios","android","web","windows"]},"pushFailureCount":{"type":"integer","default":0,"readOnly":true,"description":"**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"},"offlineScope":{"type":"string","nullable":true,"enum":["none","readOnly","sellAndScan","fullVenue"],"description":"BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"},"firmwareVersion":{"type":"string","nullable":true,"readOnly":true,"description":"As the device last reported it on its heartbeat."},"isRequired":{"type":"boolean","description":"True blocks shift open when the device is unreachable."},"status":{"type":"string","readOnly":true,"enum":["online","offline","error","consumableLow","needsAttention","localMode","unknown"],"description":"What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"},"batteryPercent":{"type":"integer","nullable":true,"readOnly":true,"minimum":0,"maximum":100,"description":"Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"},"health":{"type":"string","enum":["healthy","warning","degraded","offline","unknown"],"default":"unknown","readOnly":true,"description":"**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"capabilities":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/DeviceCapability"},"description":"BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"},"enrolmentState":{"type":"string","enum":["registered","enrolled","provisioned","active","deactivated","retired"],"default":"registered","readOnly":true,"description":"BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"},"retiredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"},"approvalStatus":{"allOf":[{"$ref":"#/components/schemas/DeviceApprovalStatus"}],"default":"pendingApproval","readOnly":true,"description":"**A new device waits for approval before it may go live** (decided 2 October 2026, Chinmay, critical set 1, BO-196: \"Secure enrolment code + pending approval\"; DEC-241; CHG-CSP-011; MoM 15 September, DI-892, DI-906). Every device registers `pendingApproval`. It may enrol and be provisioned and tested, but `enrolDevice` refuses `active` until `approveDevice` approves it (`409 device-approval-required`). A separate axis from `enrolmentState`, which keeps its r1 values; the model is `states/registered-device-approval.yaml`.\n"},"enrolmentCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":12,"description":"**A one-time code the device must present to enrol** (DEC-241; CHG-CSP-011). Issued by `registerDevice` and returned once, in its response only; every later read returns null. The installer enters it on the device, and `enrolDevice` to `enrolled` must carry the same code before `enrolmentCodeExpiresAt` (`422 enrolment-code-invalid`). A device that never presents it never gets an identity, so a box plugged into the venue network cannot claim to be a reader.\n"},"enrolmentCodeExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the enrolment code stops working (24 hours after registration, proposed; client to correct)."},"testedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who recorded the device's acceptance test (`DeviceEnrolment.testResult` on the move to `provisioned`). The approver must be someone else (DEC-245).\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who approved the device into production, never the person who tested it** (decided 2 October 2026, Chinmay, critical set 1, BO-203: \"Approver must differ from the tester\"; DEC-245; CHG-CSP-011). `approveDevice` refuses the tester with `403 approver-is-tester`.\n"},"approvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"TurnstileLaneBehaviorConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Turnstile & Lane Behavior Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"accessPointId":{"type":"string","description":"Turnstile or lane being configured"},"mode":{"type":"string","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"],"description":"Default operating mode of the lane (AccessPointOperatingMode, R221). Direction is fixed per access point; re-entry, crossover, fast pass and group are admission rules, not lane modes"},"passThroughTimeout":{"type":"integer","description":"Seconds"},"relockBehavior":{"type":"string","description":"relock behavior"},"incompletePassageBehavior":{"type":"string","description":"incomplete passage behavior"},"unlockDuration":{"type":"integer","description":"Seconds"}},"required":["accessPointId","mode"]},
"TurnstileLaneBehaviorConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Turnstile & Lane Behavior Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"accessPointId":{"type":"string","description":"Turnstile or lane being configured"},"mode":{"type":"string","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"],"description":"Default operating mode of the lane (AccessPointOperatingMode, R221). Direction is fixed per access point; re-entry, crossover, fast pass and group are admission rules, not lane modes"},"passThroughTimeout":{"type":"integer","description":"Seconds"},"relockBehavior":{"type":"string","description":"relock behavior"},"incompletePassageBehavior":{"type":"string","description":"incomplete passage behavior"},"unlockDuration":{"type":"integer","description":"Seconds"}},"required":["accessPointId","mode"]},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]},
"ValidationOutcomeGuestFeedbackDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Validation Outcome & Guest Feedback Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"appliesTo":{"type":"string","enum":["adult","child","vip","pod","membership","invalidCredential","wrongVerificationMethod","biometricReview","reEntryException"],"description":"Guest type or case this response is for"},"outcome":{"type":"string","enum":["granted","operatorAction","denied"]},"venueId":{"type":"string"},"outcomeProfileId":{"type":"string"},"lightColour":{"type":"string","enum":["green","yellow","red"],"description":"Light shown"},"gateAction":{"type":"string","enum":["open","remainsControlled","remainsLocked"],"description":"What the gate does"},"sound":{"type":"string","enum":["successTone","alertSound","denialSound"],"description":"Sound played"},"pictogram":{"type":"string","description":"✓ pictogram"},"customMessage":{"type":"string","description":"Custom message"},"operatorPrompt":{"type":"string","description":"operator prompt"},"reasonCode":{"type":"string","description":"reason code"},"language":{"type":"string","description":"Message language, e.g. ar, en"}},"required":["outcomeProfileId","venueId","outcome","appliesTo"]},
"ValidationOutcomeGuestFeedbackDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Validation Outcome & Guest Feedback Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"appliesTo":{"type":"string","enum":["adult","child","vip","pod","membership","invalidCredential","wrongVerificationMethod","biometricReview","reEntryException"],"description":"Guest type or case this response is for"},"outcome":{"type":"string","enum":["granted","operatorAction","denied"]},"venueId":{"type":"string"},"outcomeProfileId":{"type":"string"},"lightColour":{"type":"string","enum":["green","yellow","red"],"description":"Light shown"},"gateAction":{"type":"string","enum":["open","remainsControlled","remainsLocked"],"description":"What the gate does"},"sound":{"type":"string","enum":["successTone","alertSound","denialSound"],"description":"Sound played"},"pictogram":{"type":"string","description":"✓ pictogram"},"customMessage":{"type":"string","description":"Custom message"},"operatorPrompt":{"type":"string","description":"operator prompt"},"reasonCode":{"type":"string","description":"reason code"},"language":{"type":"string","description":"Message language, e.g. ar, en"}},"required":["outcomeProfileId","venueId","outcome","appliesTo"]}
}
```
