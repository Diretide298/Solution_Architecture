# WS04 — Access Control board 4

**10 screens · 14 operations · 18 schemas · 2 permissions**

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
  `ACCESS_POINT_CONFIGURE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-174` | Media & Credential Command Center | C | 2 | 240 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-175` | Media Type & Technology Library | C | 19 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-176` | Virtual Credential & Media Association | C | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-177` | Verification Method Selection & Locking | C | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-178` | Media Issuance & Encoding Profile | C | 9 | 6 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-179` | Media Swap & Replacement | C | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-180` | RFID & NFC Configuration | C | 11 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-181` | External & Partner Credential Mapping | C | 5 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-182` | Hotel, Wallet & External Media Integration | C | 8 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-183` | Media Compatibility, Testing & Publication | C | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-176, BO-177, BO-178, BO-179, BO-182, BO-183 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-174` Media & Credential Command Center

**Central management page for every media and verification technology supported by Access Control.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-174 |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-credential-command-center-bo-174` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): listMediaTypeCredential is the Ticket Media registry of BO-337; the hub needs no media-type catalogue, and the library belongs to BO-175 (VO-R14; design-notes …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The hub of board 4, the media abstraction layer: one view of every media and verification technology Access Control supports - KPI tiles (active media profiles, QR, RFID, NFC, wallet, biometric and external credentials, media swaps today, failed media reads, unknown credentials, verification exceptions), a media directory and AI highlights - with tiles into the nine media screens. The pack names the visual idea the whole board must carry: ONE VIRTUAL TICKET ID - MANY POSSIBLE MEDIA - ONE ACCESS HISTORY - ONE ENTITLEMENT BALANCE. The one thing to get right: never present a QR, a wristband and a face as three tickets.

**Known correction pending (do not draw the wrong version)**

- **A multiSelect "Filter by" with the option "ai"** Why: The AI highlights are a summary field, not a filter; the pack's filters are tenant, venue, media, credential, product, status, integration. *(source: screens/P08-venue-back-office.yaml#BO-174; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table "Every media credential" with no columns** Why: The directory row has five pack columns (VO-R12). *(source: contracts/spine/access.yaml#/components/schemas/MediaCredentialCommandCenterView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): listMediaTypeCredential (the Ticket Media pack's registry, BO-337) is bound here beside listMediaTypeTechnology's own library (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search media credential | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ai — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Media | text field | — | — | `listMediaCredential` ?media |
| Credential type | text field | — | — | `listMediaCredential` ?credentialType |
| Product | text field | — | — | `listMediaCredential` ?productId |
| Status | text field | — | — | `listMediaCredential` ?status |
| Integration | text field | — | — | `listMediaCredential` ?integration |

#### Outputs: what the screen shows and produces

**Shown**

**Active Media Profiles** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**QR Credentials** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**RFID Credentials** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**NFC Credentials** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**Wallet Credentials** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**Biometric Credentials** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**External Credentials** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**Media Swaps Today** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**Failed Media Reads** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**Unknown Credentials** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**Verification Exceptions** (metric tile, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**Every media credential** (data table, from `listMediaCredential`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Media profile | text | Media profile identifier |
| Media profile | text | Media profile name, e.g. |
| Technology | text | Technology, e.g. |
| Credential type | text | Credential type, e.g. |
| Status | chip: Active, Inactive | — |
| Offline support | chip: Yes, No, Conditional | Whether the medium validates offline |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active media profiles | 1,234 | Active Media Profiles |
| QR credentials | 1,234 | QR Credentials |
| RFID credentials | 1,234 | RFID Credentials |
| NFC credentials | 1,234 | NFC Credentials |
| Wallet credentials | 1,234 | Wallet Credentials |
| Biometric credentials | 1,234 | Biometric Credentials |
| External credentials | 1,234 | External Credentials |
| Media swaps today | 1,234 | Media Swaps Today |
| Failed media reads | 1,234 | Failed Media Reads |
| Unknown credentials | 1,234 | Unknown Credentials |

**The selected media credential** (detail panel): The pack groups this record's detail under its own headings: “Media Directory”.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: The eleven pack tiles as metric tiles (VO-R02); Failed media reads, Unknown credentials and Verification exceptions turn amber/red above zero and open the list behind them. *(source: screens/P08-venue-back-office.yaml#BO-174 / contracts/spine/access.yaml#/components/schemas/MediaCredentialCommandCenterViewSummary)*
- **Hero diagram**: A central "virtual ticket" node with QR, Barcode, RFID, NFC, Mobile wallet, Face Pass, Face Tag and External credential around it, each with today's count - the board's design concept. *(source: screens/P08-venue-back-office.yaml#BO-174 / screens/P08-venue-back-office.yaml#BO-183 / DI-652)*
- **Media directory**: Titled "Media profiles"; columns Media profile, Technology, Credential type, Status, Offline (Yes / No / Conditional - Conditional in amber with the reason on hover). *(source: screens/P08-venue-back-office.yaml#BO-174 / contracts/spine/access.yaml#/components/schemas/MediaCredentialCommandCenterView)*
- **Filters**: Media, Credential, Product, Status, Integration; Tenant and Venue come from the session (VO-R09), not filter fields. *(source: contracts/spine/access.yaml#listMediaCredential)*
- **AI highlights**: Advisory findings (failing media profiles, unusual read errors, duplicate identifiers, obsolete media, incompatible device/media combinations) each with the profile and gate (VO-R11). *(source: contracts/spine/access.yaml#/components/schemas/MediaCredentialCommandCenterViewSummary)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open a media screen**: Tiles into BO-175 to BO-183; each returns here. *(source: F114 step 1 / DI-653)*
- **Look up a ticket**: A search box taking a ticket number or any media code opens the virtual credential view (BO-176) on that ticket. *(source: contracts/spine/access.yaml#listVirtualCredentialMedia / DI-180)*

**Data it reads**: `listMediaCredential` (onLoad, Media & Credential Command Center); `listVirtualCredentialMedia` (onLoad, Virtual Credential & Media Association)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-175` Media Type & Technology Library: *Works in Media Type & Technology Library*; calls `listMediaCredential`
- → `BO-176` Virtual Credential & Media Association: *Works in Virtual Credential & Media Association*; calls `listMediaCredential`
- → `BO-177` Verification Method Selection & Locking: *Works in Verification Method Selection & Locking*; calls `listMediaCredential`
- → `BO-178` Media Issuance & Encoding Profile: *Works in Media Issuance & Encoding Profile*; calls `listMediaCredential`
- → `BO-179` Media Swap & Replacement: *Works in Media Swap & Replacement*; calls `listMediaCredential`
- → `BO-180` RFID & NFC Configuration: *Works in RFID & NFC Configuration*; calls `listMediaCredential`
- → `BO-181` External & Partner Credential Mapping: *Works in External & Partner Credential Mapping*; calls `listMediaCredential`
- → `BO-182` Hotel, Wallet & External Media Integration: *Works in Hotel, Wallet & External Media Integration*; calls `listMediaCredential`
- → `BO-183` Media Compatibility, Testing & Publication: *Works in Media Compatibility, Testing & Publication*; calls `listMediaCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media credential list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media credential yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the media credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Unknown credentials rising at one gate**: Highlight names the gate and the most common unrecognised format, linking to partner mapping (BO-181). *(source: screens/P08-venue-back-office.yaml#BO-174)*

#### Consistency with other screens

- Match `BO-334`: The Virtual Ticket command centre shows the same ticket-with-media idea; same diagram and ticket number format.
- Match `BO-337`: The media type registry of the Ticket Media pack reads the same media types as BO-175.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  activeProfiles: 9
  qr: 21480
  rfid: 6320
  nfc: 1140
  wallet: 3870
  biometric: 2526
  external: 410
  swapsToday: 37
  failedReads: 118
  unknown: 12
  exceptions: 6
directory:
- profile: Mobile Dynamic QR
  technology: QR
  type: Digital ticket
  status: Active
  offline: 'Yes'
- profile: RFID Wristband
  technology: RFID
  type: Wristband
  status: Active
  offline: 'Yes'
- profile: Annual Pass NFC
  technology: NFC
  type: Membership
  status: Active
  offline: 'Yes'
- profile: Apple Wallet Pass
  technology: Wallet
  type: Digital pass
  status: Active
  offline: 'Yes'
- profile: Partner QR
  technology: QR
  type: External ticket
  status: Active
  offline: Conditional
```

#### Permissions

- `listMediaCredential` → `SCOPE_VIEW` (read) · staff
- `listVirtualCredentialMedia` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-174` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-174`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 1: Opens Media & Credential Command Center → Central management page for every media and verification technology supported by Access Control.
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F114 branch at step 1 (expected): when Nothing has been set up on Media & Credential Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F114 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (240 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-174?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-175`, `BO-176`, `BO-177`, `BO-178`, `BO-179`, `BO-180`, `BO-181`, `BO-182`, `BO-183`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-175` Media Type & Technology Library

**Define reusable media technologies. The matrix expects support for linear barcode, two-dimensional codes, magnetic strips, contact/proximity RFID, NFC and biometric readers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-175 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each profile defines) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-type-technology-library-bo-175` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): Merge the two media-type catalogues into one record, one read and one write that every media picker reads (BO-175, BO-337).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The library of media technologies the venue accepts - 1D, 2D and QR barcodes, contact, proximity and ISO 15693 RFID, NFC, app credential, mobile wallet, paper ticket, wristband, plastic card, hotel card, Face Pass, Face Tag, partner QR, external barcode, third-party credential - each with technology, encoding format, reader types, online/offline capability, writable or read-only, security classification and where it applies. New media are added by configuration. The one thing to get right: media are retired, never deleted, because issued credentials still reference them.

**Known correction pending (do not draw the wrong version)**

- **Every property (technology, encoding format, reader types, capability, classification, venues) is a selectField and Save has no permission** Why: Encoding format is text, reader types and venues multi-selects, capability segmented; Save needs ACCESS_POINT_CONFIGURE (VO-R08). *(source: screens/P08-venue-back-office.yaml#BO-175 / contracts/spine/access.yaml#setMediaTypeTechnology; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Two catalogues of media types (listMediaTypeTechnology here, listMediaTypeCredential on BO-337) with different fields (CHG-WIR-004)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| technology | select field | — | — | — | — | — | — |
| encoding format | select field | — | — | — | — | — | — |
| supported reader types | select field | — | — | — | — | — | — |
| online/offline capability | select field | — | — | — | — | — | — |
| writable/read-only | select field | — | — | — | — | — | — |
| security classification | select field | — | — | — | — | — | — |
| applicable venues | select field | — | — | — | — | — | — |

**Sent by *Save media type*** (`setMediaTypeTechnology`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Media type `mediaTypeId` | picker: choose a media type | optional | — | — | shows names, sends the id | Absent adds a media type | `setMediaTypeTechnology` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setMediaTypeTechnology` body |
| Media type `mediaType` | select | required | — | Linear barcode · Two dimensional barcode · QR · RFID contact · RFID proximity · RFID iso15693 · RFID other standard · App credential · Mobile wallet · Paper ticket · Wristband · Plastic card … | — | — | `setMediaTypeTechnology` body |
| Technology `technology` | select | required | — | Barcode · RFID · NFC · Magnetic stripe · Mobile · Physical · Biometric · External | — | — | `setMediaTypeTechnology` body |
| Encoding format `encodingFormat` | text field | optional | — | max length 100 | — | — | `setMediaTypeTechnology` body |
| Supported reader types `supportedReaderTypes` | list of values (chips) | optional | — | — | — | — | `setMediaTypeTechnology` body |
| Online offline capability `onlineOfflineCapability` | segmented control | required | — | Online only · Offline only · Online and offline | — | — | `setMediaTypeTechnology` body |
| Writable read only `writableReadOnly` | segmented control | optional | — | Writable · Read only | — | — | `setMediaTypeTechnology` body |
| Security classification `securityClassification` | text field | optional | — | max length 100 | — | — | `setMediaTypeTechnology` body |
| Applicable venues `applicableVenues` | list of values (chips) | optional | — | — | — | Empty means every venue of the tenant | `setMediaTypeTechnology` body |
| Applicable products `applicableProducts` | list of values (chips) | optional | — | — | — | Empty means every product | `setMediaTypeTechnology` body |
| Active `active` | toggle | optional | on | — | — | False retires the media type: no new credential is issued on it; credentials already issued stay valid until they expire | `setMediaTypeTechnology` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **mediaType**: Grouped select in the pack's families - Barcode, RFID, NFC, Mobile, Physical, Identity, External; the family sets technology automatically (editable). *(source: screens/P08-venue-back-office.yaml#BO-175 / contracts/spine/access.yaml#setMediaTypeTechnology)*
- **name**: Required, max 200, Arabic variant, e.g. "RFID Wristband (ISO 15693)". *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*
- **encodingFormat / supportedReaderTypes**: Encoding format max 100 (e.g. "ISO/IEC 18004 QR, ECC M"); reader types as chips from the reader list of BO-199 (QR/barcode, RFID, NFC, biometric camera). *(source: contracts/spine/access.yaml#setMediaTypeTechnology / screens/P08-venue-back-office.yaml#BO-199)*
- **onlineOfflineCapability / writableReadOnly**: Segmented controls Online only / Offline only / Online and offline (required) and Writable / Read-only. *(source: screens/P08-venue-back-office.yaml#BO-176 / contracts/spine/access.yaml#setMediaTypeTechnology)*
- **securityClassification**: Select (placeholder Low / Standard / High until the client gives a scale), not free text. *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*
- **applicableVenues / applicableProducts**: Multi-selects; empty must read "All venues" / "All products". *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*
- **active**: Shown as status Active / Retired; retiring explains "No new credentials on this media; issued ones stay valid until they expire". *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save media type (primary button) | `setMediaTypeTechnology` PUT `/media-type-technology` | MediaTypeTechnologyLibraryInput | MediaTypeTechnologyLibraryView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Retiring a media type an active encoding profile still uses | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Library list**: Grouped by family with name, technology, offline capability, readers, venues, status; retired rows greyed with the retire date. *(source: contracts/spine/access.yaml#listMediaTypeTechnology)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add / Save media type**: Upsert keyed by mediaTypeId (absent creates); whole record replaced (VO-R04). *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*
- **Retire**: Sets active false after a confirmation naming credentials issued on it; refused (409) while an active encoding profile names it - the message names the profile. *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*

**Data it reads**: `listMediaTypeTechnology` (onLoad, Media Type & Technology Library)

**Where the user goes next**

- → `BO-174` Media & Credential Command Center: *Returns to the board's landing screen*; calls `listMediaTypeTechnology`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media type technology configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media type technology untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media type technology configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Retiring a media type an active encoding profile still uses |

#### Edge cases to draw

- **Adding a media type no reader in the venue supports**: Warn "No registered reader supports this media" with a link to BO-183. *(source: screens/P08-venue-back-office.yaml#BO-183)*

#### Consistency with other screens

- Match `BO-337`: Media Type & Credential Technology Registry (ticket media process) is the same catalogue with a different read (listMediaTypeCredential); one should survive (VO-R14), the other link to it.
- Match `BO-178`: Encoding profiles pick a media type from this library.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
types:
- name: Mobile Dynamic QR
  family: Barcode
  type: QR
  offline: Online and offline
  rw: Read-only
  venues: All
- name: RFID Wristband ISO 15693
  family: RFID
  type: ISO 15693
  offline: Online and offline
  rw: Writable
  venues: Aqua Park
- name: Hotel room card
  family: Physical
  type: Hotel card
  offline: Online only
  status: Active
- name: Paper ticket 1D
  family: Barcode
  type: Linear barcode
  status: Retired 30 Jun 2026
```

#### Permissions

- `listMediaTypeTechnology` → `SCOPE_VIEW` (read) · staff
- `setMediaTypeTechnology` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-175` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-175`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 2: Works in Media Type & Technology Library → Define reusable media technologies. The matrix expects support for linear barcode, two-dimensional codes, magnetic strips, contact/proximity RFID, NFC and biometric readers.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-175?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save media type.
- [ ] Every transition is wired: `BO-174`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-176` Virtual Credential & Media Association

**Associate one virtual ticket identity with its permitted media representations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-176 |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/virtual-credential-media-association-bo-176` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Shows one virtual credential with every medium linked to it and which of them may be used now - the pack's VC-9837241, Adventure Park Annual Pass: Dynamic QR Active, RFID Wristband Active, Mobile Wallet Provisioned, Face Pass Enrolled - and proves that any of them (QR 8X72..., RFID 298173..., Wallet 827...) resolves to the same ticket, guest, entitlements, access history and consumption state. The one thing to get right: linked is not the same as usable; show both, with the verification priority (primary Dynamic QR, alternatives RFID / NFC / Face Pass).

**Known correction pending (do not draw the wrong version)**

- **Content region is an empty unbound table and the read is not attached to it; no search input** Why: The read returns ticket, guest, entitlements, linked and active media; the pack gives a full credential view (p46-47). *(source: screens/P08-venue-back-office.yaml#BO-176 / contracts/spine/access.yaml#listVirtualCredentialMedia; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Verification priority is configured on this pack page but has no write here** Why: The priority belongs to media activation rules (BO-341); link to it rather than a second editor. *(source: screens/P08-venue-back-office.yaml#BO-176 / contracts/spine/access.yaml#listMediaActivationPriority; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search**: One search box accepting a ticket number, a virtual credential id or any media code; the result is always the one virtual credential. *(source: screens/P08-venue-back-office.yaml#BO-176 / screens/P08-venue-back-office.yaml#BO-177)*
- **Verification priority**: Primary method and ordered alternatives, drag to reorder; this is the product's media activation rule (BO-341), shown here read-only with Edit. *(source: screens/P08-venue-back-office.yaml#BO-176 / contracts/spine/access.yaml#listMediaActivationPriority)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Credential card**: Virtual credential id, ticket product, guest, entitlements with balances and consumption state; the ticket number never changes. *(source: contracts/spine/access.yaml#/components/schemas/VirtualCredentialMediaAssociationView / DI-652)*
- **Linked media**: One row per medium with masked code, state (Active, Provisioned, Enrolled, Revoked) and a "Usable now" tick from activeMedia; Face Pass shows "Enrolled", never an image. *(source: screens/P08-venue-back-office.yaml#BO-176 / contracts/spine/access.yaml#/components/schemas/VirtualCredentialMediaAssociationView)*
- **Identity resolution**: The pack's diagram - three media codes arrowing into the one credential, then Ticket, Guest, Entitlements, Access history, Consumption state. *(source: screens/P08-venue-back-office.yaml#BO-177)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open history / Swap media**: History opens the investigation console (BO-226); Swap opens BO-179 with the credential selected. *(source: screens/P08-venue-back-office.yaml#BO-179)*

**Data it reads**: `listVirtualCredentialMedia` (onLoad, Virtual Credential & Media Association)

**Where the user goes next**

- → `BO-174` Media & Credential Command Center: *Returns to the board's landing screen*; calls `listVirtualCredentialMedia`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual credential media list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual credential media untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual credential media yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the virtual credential media are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Code that matches no credential**: "Unknown credential" with the reader-side meaning (Deny or Refer to operator per partner policy) and no partial match list of other guests. *(source: screens/P08-venue-back-office.yaml#BO-181)*
- **Viewer without guest data rights**: Guest name masked; media states still visible (VO-R08). *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-338`: Which media may be linked to which product is set in Multi-Media Binding & Association Rules; this screen shows the result per ticket.
- Match `BO-355`: The 360 workspace shows the same credential card; one component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
credential:
  id: VC-9837241
  ticket: VT0010
  product: Aqua Park Annual Pass
  guest: Sara Al Nuaimi
  entitlements: Park entry 1 per day, Fast Pass 3 left
media:
- medium: Dynamic QR
  code: QR-7F3K-92LD
  state: Active
  usable: true
- medium: RFID wristband
  code: RFID-882910
  state: Active
  usable: true
- medium: Apple Wallet
  code: WAL-827...
  state: Provisioned
  usable: false
- medium: Face Pass
  state: Enrolled
  usable: true
priority: Primary Dynamic QR; alternatives RFID, NFC, Face Pass
```

#### Permissions

- `listVirtualCredentialMedia` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-176` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-176`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 4: Works in Virtual Credential & Media Association → Associate one virtual ticket identity with its permitted media representations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-176?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-174`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-177` Verification Method Selection & Locking

**Control which verification method the guest chooses and when it becomes locked. The matrix specifies that although a ticket may technically support physical card, Dynamic QR, Face Pass and Face Tag, the customer should select one verification method. It may be changed before first successful verification, but after that the guest cannot change it; authorized venue operations may do so when necessary.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-177 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/verification-method-selection-locking-bo-177` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** For each product, which verification methods a guest may choose (dynamic QR, physical card, RFID, Face Pass, Face Tag), that the choice locks on the first successful entry, and who may change it afterwards (nobody, or operations with supervisor approval) for which reasons (lost phone, damaged wristband, accessibility, device failure, guest service, other). The one thing to get right: the journey "Ticket issued > guest selects Dynamic QR > first successful access > verification method locked" and the audited operator change after it.

**Known correction pending (do not draw the wrong version)**

- **The read returns reason as one value per row while the write holds reasonCodes as a list** Why: The policy's reason vocabulary cannot be reopened (VO-R04). *(source: contracts/spine/access.yaml#listVerificationMethodSelection / contracts/spine/access.yaml#setVerificationMethodPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The write requires id and scopePath though it is keyed on productId** Why: Server-owned (VO-R03). *(source: contracts/spine/access.yaml#setVerificationMethodPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation changes a ticket's method after lock** Why: The contract lists it as "no operation yet"; the supervisor-approved change cannot happen. *(source: contracts/spine/access.yaml#listVerificationMethodSelection; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Form: Save verification method policy** (modal, opened by *Save verification method policy*; *Save verification method policy* calls `setVerificationMethodPolicy`, *Cancel* sends nothing)

**Collects what `setVerificationMethodPolicy` sends before it is called.** Required: `id`, `productId`, `availableMethods`, `lockOnFirstSuccessfulAccess`, `changeAfterLock`, `scopePath`. Optional: `reasonCodes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | The policyId of listVerificationMethodSelection | `setVerificationMethodPolicy` body |
| Product `productId` | picker: choose a product | required | — | — | shows names, sends the id | Unique per scope | `setVerificationMethodPolicy` body |
| Available methods `availableMethods` | multi-select chips | required | — | Dynamic QR · Physical card · RFID · Face pass · Face tag | — | — | `setVerificationMethodPolicy` body |
| Lock on first successful access `lockOnFirstSuccessfulAccess` | toggle | required | on | — | — | — | `setVerificationMethodPolicy` body |
| Change after lock `changeAfterLock` | segmented control | required | Supervisor approval | Not allowed · Supervisor approval | — | Who may change the method once locked; guests may not | `setVerificationMethodPolicy` body |
| Reason codes `reasonCodes` | multi-select chips | optional | — | Lost phone · Damaged wristband · Accessibility · Device failure · Guest service · Other | — | Reason vocabulary for a method change after lock | `setVerificationMethodPolicy` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setVerificationMethodPolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 A method named is not enabled at this venue.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **productId**: Picked product; one policy per product (the upsert key). *(source: contracts/spine/access.yaml#setVerificationMethodPolicy)*
- **availableMethods**: Required chips of the five methods; Face Pass only offered for products that allow it (memberships, passes) per BO-185. *(source: screens/P08-venue-back-office.yaml#BO-177 / contracts/spine/access.yaml#setVerificationMethodPolicy)*
- **lockOnFirstSuccessfulAccess**: Default on, with "Guests can change their method until their first successful entry". *(source: screens/P08-venue-back-office.yaml#BO-177 / contracts/spine/access.yaml#setVerificationMethodPolicy)*
- **changeAfterLock**: Not allowed / Supervisor approval (default); guests may never change after lock, so there is no guest option. *(source: contracts/spine/access.yaml#setVerificationMethodPolicy)*
- **reasonCodes**: Multi-select of the six reasons offered to the operator; at least one when changes after lock are allowed. *(source: screens/P08-venue-back-office.yaml#BO-178 / contracts/spine/access.yaml#setVerificationMethodPolicy)*
- **id, scopePath, timestamps**: Not inputs (VO-R03); the product is the key. *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save verification method policy (primary button) | `setVerificationMethodPolicy` PUT `/verification-method-policies` | AccessVerificationMethodPolicy | AccessVerificationMethodPolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 A method named is not enabled at this venue. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lock journey**: Ticket issued > Guest selects > First successful access > Method locked, with Operator change branching off after the lock. *(source: screens/P08-venue-back-office.yaml#BO-177 / screens/P08-venue-back-office.yaml#BO-178)*
- **Policies list**: Product, methods as icons, lock on/off, change rule. *(source: contracts/spine/access.yaml#listVerificationMethodSelection)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save policy**: Upsert keyed by product (whole record, VO-R04). *(source: contracts/spine/access.yaml#setVerificationMethodPolicy)*
- **Change a ticket's method after lock**: An operator flow (supervisor approval, reason, audited); drawn as an action on a ticket, not yet backed by an operation. *(source: contracts/spine/access.yaml#listVerificationMethodSelection / DI-649)*

**Data it reads**: `listVerificationMethodSelection` (onLoad, Verification Method Selection & Locking)

**Where the user goes next**

- → `BO-174` Media & Credential Command Center: *Returns to the board's landing screen*; calls `listVerificationMethodSelection`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The verification method selection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the verification method selection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No verification method selection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the verification method selection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A method named is not enabled at this venue. |

#### Edge cases to draw

- **Guest's locked method fails at the gate (face not matched, phone dead)**: The fallback media of the ticket still admit per DI-641; the lock limits the guest's own changes, not the gate's fallback. *(source: DI-641)*

#### Consistency with other screens

- Match `GST-055`: The guest's method choice and the "locked" state use these method names.
- Match `BO-176`: The ticket hub shows the chosen and fallback methods.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policies:
- product: Summit Peaks Annual Pass
  methods: Dynamic QR, RFID, Face Pass
  lock: true
  afterLock: Supervisor approval
  reasons: Lost phone, Damaged wristband, Accessibility, Device failure
- product: Aqua Park Day Pass
  methods: Dynamic QR, Face Tag
  lock: true
  afterLock: Not allowed
```

#### Permissions

- `listVerificationMethodSelection` → `SCOPE_VIEW` (read) · staff
- `setVerificationMethodPolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-177` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-177`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 6: Works in Verification Method Selection & Locking → Control which verification method the guest chooses and when it becomes locked. The matrix specifies that although a ticket may technically support physical card, Dynamic QR, Face Pass and Face Tag …

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-177?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save verification method policy.
- [ ] Every transition is wired: `BO-174`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-178` Media Issuance & Encoding Profile

**Configure how ticket identity is written or encoded onto each medium. The source requires ticket IDs to be generated as 2D barcode, QR or RFID and requires randomized, always- unique identifiers to reduce fraud.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-178 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-issuance-encoding-profile-bo-178` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Encoding profiles: how a ticket's identity is written onto each medium (the pack's "RFID Wristband - Adventure Park"): credential identifier, randomised media identifier, ticket ID reference, secure token, encoding format, offline payload, checksum or signature, for outputs E-ticket, M-ticket, paper wristband, RFID wristband, physical card, wallet. Uniqueness controls (collision check, randomisation, duplicate prevention) are shown as ENABLED. The one thing to get right: no key material on the page - the signing profile is chosen from the platform's managed list.

**Known correction pending (do not draw the wrong version)**

- **Table columns are only the three uniqueness booleans plus a column literally labelled "Duplicate Prevention - ENABLED"** Why: Sample text used as a label; the read has name, media type, formats and payload profile to list. *(source: screens/P08-venue-back-office.yaml#BO-178 / contracts/spine/access.yaml#/components/schemas/MediaIssuanceEncodingProfileView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **offlinePayloadProfile and checksumSignatureWhereApplicable are free strings** Why: They name a payload design and a managed signing profile; references, not text. *(source: screens/P08-venue-back-office.yaml#BO-179 / contracts/spine/access.yaml#/components/schemas/MediaIssuanceEncodingProfileInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's output profiles (E-ticket, M-ticket, paper wristband ...) have no field** Why: The profile cannot say which output it produces. *(source: screens/P08-venue-back-office.yaml#BO-178 / screens/P08-venue-back-office.yaml#BO-179; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Sent by *Save issuance and encoding profile*** (`setMediaIssuanceEncoding`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Encoding profile `encodingProfileId` | picker: choose an encoding profile | optional | — | — | shows names, sends the id | Absent creates a profile | `setMediaIssuanceEncoding` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setMediaIssuanceEncoding` body |
| Media type `mediaTypeId` | text field | required | — | — | — | The media type this profile encodes (`MediaTypeTechnologyLibraryView.mediaTypeId`) | `setMediaIssuanceEncoding` body |
| Encoding format `encodingFormat` | text field | required | — | max length 100 | — | — | `setMediaIssuanceEncoding` body |
| Offline payload profile `offlinePayloadProfile` | text field | optional | — | — | — | Which entitlement data is embedded for offline validation | `setMediaIssuanceEncoding` body |
| Checksum signature where applicable `checksumSignatureWhereApplicable` | text field | optional | — | — | — | Checksum or signature scheme, where the media carries one | `setMediaIssuanceEncoding` body |
| Randomization enabled `randomizationEnabled` | toggle | optional | on | — | — | Media identifiers are random rather than sequential | `setMediaIssuanceEncoding` body |
| Identifier collision check enabled `identifierCollisionCheckEnabled` | toggle | optional | on | — | — | — | `setMediaIssuanceEncoding` body |
| Duplicate prevention enabled `duplicatePreventionEnabled` | toggle | optional | on | — | — | — | `setMediaIssuanceEncoding` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name / mediaTypeId**: Name required; media type picked from the library (BO-175), active types only. *(source: contracts/spine/access.yaml#setMediaIssuanceEncoding)*
- **encodingFormat**: Required, max 100, prefilled from the media type. *(source: contracts/spine/access.yaml#setMediaIssuanceEncoding)*
- **offlinePayloadProfile**: Picker of payload designs from BO-172, not free text. *(source: contracts/spine/access.yaml#setMediaIssuanceEncoding / screens/P08-venue-back-office.yaml#BO-172)*
- **checksumSignatureWhereApplicable**: Select of the platform's signing profiles by name ("TICVAI managed - ECDSA P-256"); never a key field. *(source: screens/P08-venue-back-office.yaml#BO-179 / contracts/spine/access.yaml#setMediaIssuanceEncoding)*
- **randomizationEnabled / identifierCollisionCheckEnabled / duplicatePreventionEnabled**: Three switches, default on; turning one off needs a confirmation explaining the fraud risk (sequential identifiers can be guessed). *(source: screens/P08-venue-back-office.yaml#BO-179 / contracts/spine/access.yaml#setMediaIssuanceEncoding)*
- **Identifier format**: The virtual ticket ID format (prefix, suffix, length) is set in the ticket media process; show it read-only with a link. *(source: TRACKER Actions row 209 / screens/P08-venue-back-office.yaml#BO-335)*

#### Outputs: what the screen shows and produces

**Shown**

**Every media issuance encoding** (data table, from `listMediaIssuanceEncoding`)

| Shows | Format | Notes |
|---|---|---|
| Identifier collision check enabled | yes / no (icon or chip) | Identifier Collision Check — ENABLED |
| Randomization enabled | yes / no (icon or chip) | Randomization — ENABLED |
| Duplicate prevention — ENABLED | text | not in the schema: `Duplicate Prevention — ENABLED` |

**The selected media issuance encoding** (detail panel): The pack groups this record's detail under its own headings: “Security”, “Security / Signing Profile”.

| Shows | Format | Notes |
|---|---|---|
| Identifier collision check enabled | yes / no (icon or chip) | Identifier Collision Check — ENABLED |
| Randomization enabled | yes / no (icon or chip) | Randomization — ENABLED |
| Duplicate prevention — ENABLED | text | not in the schema: `Duplicate Prevention — ENABLED` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save issuance and encoding profile (primary button) | `setMediaIssuanceEncoding` PUT `/media-issuance-encoding` | MediaIssuanceEncodingProfileInput | MediaIssuanceEncodingProfileView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 The media type is retired or does not exist | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Profile list**: Name, Media type, Output (E-ticket, M-ticket, Paper wristband, RFID wristband, Physical card, Wallet), Uniqueness badges, Media issued on it. *(source: screens/P08-venue-back-office.yaml#BO-179 / contracts/spine/access.yaml#listMediaIssuanceEncoding)*
- **Uniqueness panel**: The pack's three lines "Identifier Collision Check - ENABLED", "Randomization - ENABLED", "Duplicate Prevention - ENABLED", green when on, red when off. *(source: screens/P08-venue-back-office.yaml#BO-179)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save encoding profile**: Upsert keyed by encodingProfileId (absent creates); applies to media issued after the save; media already encoded keep their profile - the confirmation says so. *(source: contracts/spine/access.yaml#setMediaIssuanceEncoding)*

**Data it reads**: `listMediaIssuanceEncoding` (onLoad, Media Issuance & Encoding Profile)

**Where the user goes next**

- → `BO-174` Media & Credential Command Center: *Returns to the board's landing screen*; calls `listMediaIssuanceEncoding`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media issuance encoding list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media issuance encoding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media issuance encoding yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the media issuance encoding are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The media type is retired or does not exist |

#### Edge cases to draw

- **Media type retired after the profile was created**: Profile shown with "Media type retired - no new issuance" and cannot be saved active. *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*

#### Consistency with other screens

- Match `EMP-036`: Issue media on the staff app encodes with these profiles.
- Match `BO-335`: Ticket identifier format and this media identifier are different things; label them "Ticket number" and "Media code".

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- name: RFID Wristband - Aqua Park
  mediaType: RFID Wristband ISO 15693
  output: RFID wristband
  signing: TICVAI managed - ECDSA P-256
  randomised: true
  collision: true
  duplicates: true
  issued: 4180
- name: Mobile dynamic QR
  mediaType: Mobile Dynamic QR
  output: M-ticket
  payload: Day ticket offline payload
```

#### Permissions

- `listMediaIssuanceEncoding` → `SCOPE_VIEW` (read) · staff
- `setMediaIssuanceEncoding` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-178` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-178`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 8: Works in Media Issuance & Encoding Profile → Configure how ticket identity is written or encoded onto each medium. The source requires ticket IDs to be generated as 2D barcode, QR or RFID and requires randomized, always- unique identifiers to …

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-178?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save issuance and encoding profile.
- [ ] Every transition is wired: `BO-174`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-179` Media Swap & Replacement

**Transfer a ticket from one medium to another without changing the underlying virtual ticket. This directly covers the matrix requirement to swap RFID to barcode/QR or vice versa while transferring the attached information.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-179 |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-swap-replacement-bo-179` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Moves a ticket from one medium to another without changing the ticket - the pack's lost RFID wristband: search VC-9837241, current media RFID-882910, Swap media from RFID wristband to Dynamic QR, preserving ticket, guest, remaining entitlements, entry history, re-entry status, Fast Pass balance, reservations and membership; old RFID REVOKED, new QR ACTIVE. Agreed as a zero-value transaction (scan an online QR at a kiosk, get a wristband). The one thing to get right: the preserve checklist is shown ticked before confirming, so the operator sees that nothing is lost, and the swap history below proves it afterwards.

**Known correction pending (do not draw the wrong version)**

- **Read-only screen (swap history) with an empty table and no swap operation** Why: The pack's purpose is to perform the swap; the only replacement write (replaceCredential) is bound to BO-359 under ORDER_EXCHANGE. Bind it here or make this screen the history view of BO-359. *(source: contracts/spine/access.yaml#listMediaSwapReplacement / contracts/spine/access.yaml#replaceCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Media swap, media replacement rules and credential replacement live on three screens (BO-179, BO-342, BO-359)** Why: One transaction, one place to do it (VO-R14); the rules screen configures, one screen performs. *(source: contracts/spine/access.yaml#setMediaReplacementRevocation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Credential search**: Ticket number, virtual credential id or current media code; shows the credential card of BO-176. *(source: screens/P08-venue-back-office.yaml#BO-179)*
- **From / To medium**: From = a currently linked medium (pre-selected when only one is active); To = a medium allowed for the product by its binding rules (BO-338), with the new media code scanned or generated. *(source: screens/P08-venue-back-office.yaml#BO-179 / contracts/spine/access.yaml#setMediaBindingRule)*
- **reason**: Required, one of Lost, Damaged, Device change, Upgrade, Guest request, Operational replacement, Fraud/security, Accessibility. *(source: screens/P08-venue-back-office.yaml#BO-180 / contracts/spine/access.yaml#/components/schemas/MediaSwapReplacementView)*
- **Supervisor approval**: For high-risk swaps (Fraud/security, more than N swaps on one ticket - per the replacement rules of BO-342) a supervisor approves in place (PIN or second sign-in). *(source: screens/P08-venue-back-office.yaml#BO-180 / contracts/spine/access.yaml#setMediaReplacementRevocation)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Preserve checklist**: The pack's eight items, each ticked with its current value ("Fast Pass balance 2", "Re-entry status - inside park"). *(source: screens/P08-venue-back-office.yaml#BO-180)*
- **Result**: Two status lines "Old RFID-882910 - REVOKED" (red) and "New QR-7F3K-92LD - ACTIVE" (green); price line "AED 0.00 - zero-value swap". *(source: screens/P08-venue-back-office.yaml#BO-180 / DI-637)*
- **Swap history**: Time, Ticket, From (type and code), To, Reason, Operator; ticket number column never changes across rows; cursor paging (VO-R12). *(source: contracts/spine/access.yaml#/components/schemas/MediaSwapReplacementView)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Swap media**: Confirmation lists what is preserved and that the old medium stops working at once online and at the next package offline. *(source: screens/P08-venue-back-office.yaml#BO-180)*

**Data it reads**: `listMediaSwapReplacement` (onLoad, Media Swap & Replacement)

**Where the user goes next**

- → `BO-174` Media & Credential Command Center: *Returns to the board's landing screen*; calls `listMediaSwapReplacement`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media swap replacement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media swap replacement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media swap replacement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the media swap replacement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Gate offline when the old wristband is revoked**: Note that offline gates refuse it once their revocation cache refreshes (BO-171 maximum cache age). *(source: contracts/spine/access.yaml#setGateOfflinePolicy)*
- **Guest inside the park at the moment of swap**: Re-entry status carried over; the new medium can exit and re-enter without a fresh entry. *(source: screens/P08-venue-back-office.yaml#BO-180)*

#### Consistency with other screens

- Match `BO-342`: Replacement rules (approval, number of replacements, grace period) are configured there; this screen applies them.
- Match `EMP-036`: The staff app's Issue media / swap at a kiosk or counter does the same transaction with the same reasons.
- Match `KSK-011`: The kiosk swap of an online QR for a wristband (DI-637).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
swap:
  credential: VC-9837241
  ticket: VT0010
  guest: Khalid Al Zaabi
  from: RFID wristband RFID-882910
  to: Dynamic QR QR-7F3K-92LD
  reason: Lost
  operator: Maria Santos
  price: AED 0.00
history:
- time: 1 Oct 2026 12:31
  ticket: VT0010
  from: RFID-882910
  to: QR-7F3K-92LD
  reason: Lost
  operator: Maria Santos
- time: 30 Sep 2026 16:05
  ticket: VT0144
  from: QR-2KD9-11PA
  to: RFID-901244
  reason: Guest request
  operator: Omar Haddad
```

#### Permissions

- `listMediaSwapReplacement` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Media swap: zero-value transaction converting a ticket's media on-site, e.g. scanning an online QR at a kiosk to issue a physical wristband instead. *(client request · MoM 2 Sep 2026, 4.9 Media swap · DI-637)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-179` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-179`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 10: Works in Media Swap & Replacement → Transfer a ticket from one medium to another without changing the underlying virtual ticket. This directly covers the matrix requirement to swap RFID to barcode/QR or vice versa while transferring …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-179?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-174`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-180` RFID & NFC Configuration

**Provide dedicated configuration for proximity credentials. The matrix requires RFID—including ISO 15693—and NFC, as well as multi-range RFID scanning at near, medium and far ranges.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-180 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/rfid-nfc-configuration-bo-180` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): setRfidNfcCard is the physical card and wristband designer of the ticket media pack (BO-349); artwork, printing and deposit do not belong on reader-side RFID … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of RFID and NFC reader profiles (setRfidNfc has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Dedicated configuration for proximity credentials: RFID profiles (standard incl. ISO 15693, tag/card type, frequency/interface, reader compatibility, read/write behaviour, encoding and security profile), read range (near for an attraction, medium for a Fast Pass lane, far for seamless detection) associated with a venue, zone, gate, credential or journey, NFC uses (ticket, membership, mobile device, wallet) and what far-range readers do when several credentials are detected at once. The one thing to get right: range is chosen per place with the pack's examples beside each option.

**Known correction pending (do not draw the wrong version)**

- **Standard, tag type, frequency, read/write, encoding and security profiles are free strings; NFC uses drawn as four separate selectFields** Why: Closed lists and references; NFC uses are values of one field. *(source: contracts/spine/access.yaml#/components/schemas/RfidNfcConfigurationInput / screens/P08-venue-back-office.yaml#BO-180; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write-only; rfidNfcProfileId required; no field for far-range collision handling or for several range associations (CHG-WIR-004)

**Fixed on main** (the package already carries these; draw what it says): setRfidNfcCard (the physical card and wristband designer of the ticket media pack) is bound on this screen (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which RFID standards and tag types will the client's wristbands and readers use?** → Drawn default accepted: List ISO 14443A and ISO 15693 with their common tag types. *(decided by Chinmay, 2026-10-02; DEC-235 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| RFID standard | select field | — | — | — | — | — | — |
| tag/card type | select field | — | — | — | — | — | — |
| frequency/interface profile | select field | — | — | — | — | — | — |
| reader compatibility | select field | — | — | — | — | — | — |
| read/write behavior | select field | — | — | — | — | — | — |
| encoding profile | select field | — | — | — | — | — | — |
| NFC ticket | select field | — | — | — | — | — | — |
| membership | select field | — | — | — | — | — | — |
| mobile device | select field | — | — | — | — | — | — |
| wallet credential | select field | — | — | — | — | — | — |
| supported readers | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **rfidStandard / tagCardType / frequencyInterfaceProfile**: Selects from closed lists (e.g. ISO 14443A, ISO 15693; MIFARE DESFire EV3, ICODE SLIX2; HF 13.56 MHz, UHF 860-960 MHz) rather than text; the lists start with ISO 14443A and ISO 15693 and their common tag types. *(source: screens/P08-venue-back-office.yaml#BO-180 / contracts/spine/access.yaml#setRfidNfc / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **readerCompatibility / supportedReaders**: Multi-select of hardware models from the library (BO-195) that support the chosen standard. *(source: contracts/spine/access.yaml#setRfidNfc / screens/P08-venue-back-office.yaml#BO-195)*
- **readWriteBehavior / encodingProfile / securityProfile**: Read-only / Read-write select; encoding profile from BO-178; security profile from the platform's managed list (no keys). *(source: contracts/spine/access.yaml#setRfidNfc / screens/P08-venue-back-office.yaml#BO-178)*
- **readRange and its place (venueId, zoneId, gateId, credentialType, journey)**: A small table "Range policy": rows of Place (venue, zone, gate, credential or journey) and Range (Near / Medium / Far) with the pack's example under each option. Venue comes from the session. *(source: screens/P08-venue-back-office.yaml#BO-181 / contracts/spine/access.yaml#setRfidNfc)*
- **nfcUses / offlineCapability**: Checkboxes NFC ticket, Membership, Mobile device, Wallet credential; Offline capable switch. *(source: screens/P08-venue-back-office.yaml#BO-181 / contracts/spine/access.yaml#setRfidNfc)*
- **Collision handling (far range)**: Shown for Far only - the pack's chain Identify > Resolve > Validate > Prevent duplicate count with a choice of what happens to unresolved reads; greyed until the contract holds it. *(source: screens/P08-venue-back-office.yaml#BO-181)*
- **rfidNfcProfileId**: Not an input on create (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Profile list**: Name, Standard, Tag type, Frequency, Range (by place), NFC uses, Offline. *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save RFID/NFC profile**: Whole-profile upsert (VO-R04); readers pick it up with their next configuration push. *(source: contracts/spine/access.yaml#setRfidNfc)*

**Where the user goes next**

- → `BO-174` Media & Credential Command Center: *Returns to the board's landing screen*; calls `setRfidNfc`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rfid nfc configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rfid nfc untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rfid nfc configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Far range chosen at a gate whose reader is near-range only**: Warn with the reader model; BO-183 lists it as a compatibility warning. *(source: screens/P08-venue-back-office.yaml#BO-183)*

#### Consistency with other screens

- Match `BO-199`: The RFID range set on a gate's reader there must agree with this policy for the gate.
- Match `BO-178`: Encoding profiles referenced here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- name: Aqua Park wristbands
  standard: ISO 15693
  tag: ICODE SLIX2
  frequency: HF 13.56 MHz
  rw: Read-only
  range: Near at Falcon Coaster entry; Medium at Fast Pass lanes
  offline: true
- name: Annual pass NFC
  standard: ISO 14443A
  tag: MIFARE DESFire EV3
  nfcUses: Membership, Wallet credential
  range: Near
```

#### Permissions

- `setRfidNfc` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-180` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-180`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 12: Works in RFID & NFC Configuration → Provide dedicated configuration for proximity credentials. The matrix requires RFID—including ISO 15693—and NFC, as well as multi-range RFID scanning at near, medium and far ranges.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-180?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-174`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-181` External & Partner Credential Mapping

**Allow TICVAI Access Control to understand credentials generated by other systems. The matrix explicitly requires reading reseller/external partner ticket formats and barcodes generated by other systems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-181 |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/external-partner-credential-mapping-bo-181` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Teaches access control to read credentials it did not issue (reseller and partner QR codes, external barcodes): per partner, the credential format, a field mapping from the partner's fields to TICVAI's (ProductCode to Ticket product, VisitDate to Validity date, GuestType to Guest category, Entitlement to Access entitlement), the validation mode (local mapping, API, token, cached, offline mapping, hybrid), what happens to an unrecognised code (Deny or Refer to operator), and a test bench (upload a sample > decode > map > simulate > validate). The one thing to get right: the mapping is a two-column table with the sample's decoded values shown next to each row.

**Known correction pending (do not draw the wrong version)**

- **Read-only screen with no write for partner mappings, and no operation for the decode/simulate test** Why: The pack configures and tests mappings; nothing can be saved or tried. *(source: screens/P08-venue-back-office.yaml#BO-181 / contracts/spine/access.yaml#listExternalPartnerCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The five validation modes are drawn as five selectFields (Local Mapping, API Validation ...) and Hybrid is missing** Why: They are values of one validationMode field, which has six. *(source: screens/P08-venue-back-office.yaml#BO-181 / contracts/spine/access.yaml#/components/schemas/ExternalPartnerCredentialMappingView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **fieldMappings is an array of strings** Why: A mapping is pairs (external field, TICVAI field) plus value mappings. *(source: contracts/spine/access.yaml#/components/schemas/ExternalPartnerCredentialMappingView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Local Mapping | select field | — | — | — | — | — | — |
| API Validation | select field | — | — | — | — | — | — |
| Token Validation | select field | — | — | — | — | — | — |
| Cached Validation | select field | — | — | — | — | — | — |
| Offline Mapping | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **partnerName / credentialFormat**: Partner picked from the reseller and partner list where one exists (e.g. "Hotel Package Provider"); format as a select (QR, Code 128, PDF417, other). *(source: screens/P08-venue-back-office.yaml#BO-181 / contracts/spine/access.yaml#/components/schemas/ExternalPartnerCredentialMappingView)*
- **fieldMappings**: Rows of External field (from the decoded sample) and TICVAI field (closed list - Ticket product, Validity date, Guest category, Access entitlement, Quantity, Seat), with a value-mapping sub-table for codes (e.g. ADT to Adult). *(source: screens/P08-venue-back-office.yaml#BO-181)*
- **validationMode**: One radio list of the six modes; API and Token modes need a connection (secret reference, as in BO-182); Offline mapping and Cached are the only ones that work with the gate offline - say so. *(source: screens/P08-venue-back-office.yaml#BO-181 / contracts/spine/access.yaml#/components/schemas/ExternalPartnerCredentialMappingView)*
- **unrecognisedOutcome**: Deny / Refer to operator. *(source: screens/P08-venue-back-office.yaml#BO-181 / contracts/spine/access.yaml#/components/schemas/ExternalPartnerCredentialMappingView)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Mapping list**: Partner, Format, Validation mode, Unknown outcome, Status (Draft, Active, Inactive). *(source: contracts/spine/access.yaml#listExternalPartnerCredential)*
- **Test bench**: Upload sample > Decode (raw fields) > Map (TICVAI fields) > Simulate (virtual scan at a chosen gate) > Validate, each step ticked as in BO-163. *(source: screens/P08-venue-back-office.yaml#BO-181 / screens/P08-venue-back-office.yaml#BO-182)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save mapping / Activate**: No write exists (see corrections); draw Save and Activate disabled until bound, Activate only after a passing test. *(source: contracts/spine/access.yaml#listExternalPartnerCredential)*

**Data it reads**: `listExternalPartnerCredential` (onLoad, External & Partner Credential Mapping)

**Where the user goes next**

- → `BO-174` Media & Credential Command Center: *Returns to the board's landing screen*; calls `listExternalPartnerCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The external partner credential configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the external partner credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No external partner credential configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Partner ticket under a dynamic-QR event**: External codes are static; show which events accept them (the B2B exception of DI-633). *(source: DI-633 / TRACKER Client Inputs row 50)*
- **Same external code scanned twice**: Treated like any ticket after mapping (Already used, VO-R06). *(source: contracts/spine/access.yaml#/components/schemas/DenyReason)*

#### Consistency with other screens

- Match `BO-148`: Access points list which external credential sources they accept (externalCredentialSources).
- Match `SCN-003`: Unknown credential outcome matches the scanner's deny or refer state.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
mapping:
  partner: Hotel Package Provider
  format: QR
  mode: Cached validation
  unknown: Refer to operator
  status: Draft
fields:
- external: ProductCode
  ticvai: Ticket product
  sample: HPP-3D-FAM to Aqua Park 3-Day Family
- external: VisitDate
  ticvai: Validity date
  sample: 20261012 to 12 Oct 2026
- external: GuestType
  ticvai: Guest category
  sample: ADT to Adult
- external: Entitlement
  ticvai: Access entitlement
  sample: PARK+FP2
```

#### Permissions

- `listExternalPartnerCredential` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-181` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-181`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 14: Works in External & Partner Credential Mapping → Allow TICVAI Access Control to understand credentials generated by other systems. The matrix explicitly requires reading reseller/external partner ticket formats and barcodes generated by other …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-181?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-174`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-182` Hotel, Wallet & External Media Integration

**Configure specialized external credential ecosystems. The source specifically requires hotel room-card integration at access points and an interface to the hotel's property-management system for room billing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-182 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/hotel-wallet-external-media-integration-bo-182` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Connects external credential ecosystems: hotel room cards and the hotel PMS (room lookup, package mapping, charge to room), digital wallets, and future external media. The pack's example: guest presents a hotel room card; TICVAI resolves Room 1408, package "2 Adults + 2 Children / 3-Day Park Access", and the access decision proceeds normally; where supported, attraction or service charges go to the guest's room through the PMS. The one thing to get right: credentials of the external system are never shown or typed - only a reference to the stored secret - and an integration cannot go Active without one.

**Known correction pending (do not draw the wrong version)**

- **Content is an empty unbound table and Save has no permission declared** Why: Bind listHotelWalletExternal; gate Save on ACCESS_POINT_CONFIGURE. *(source: contracts/spine/access.yaml#listHotelWalletExternal / contracts/spine/access.yaml#setHotelWalletExternal; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's hotel card fields (hotel, card provider, card format, eligible parks, package mapping) have no field** Why: The example's package resolution (Room 1408 to 2 adults + 2 children, 3-day access) cannot be configured. *(source: screens/P08-venue-back-office.yaml#BO-182 / contracts/spine/access.yaml#/components/schemas/HotelWalletExternalMediaIntegrationInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Sent by *Save integration*** (`setHotelWalletExternal`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Integration `integrationId` | picker: choose an integration | optional | — | — | shows names, sends the id | Absent creates an integration | `setHotelWalletExternal` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setHotelWalletExternal` body |
| Integration type `integrationType` | radio group | required | — | Hotel room card · Hotel pms · Digital wallet · Other external | — | — | `setHotelWalletExternal` body |
| External system `externalSystem` | text field | required | — | max length 200 | — | The external system, e.g. | `setHotelWalletExternal` body |
| Connection secret ref `connectionSecretRef` | text field | optional | — | — | — | Reference to the stored credentials of the external system. Never the secret itself. | `setHotelWalletExternal` body |
| Room charge enabled `roomChargeEnabled` | toggle | optional | off | — | — | — | `setHotelWalletExternal` body |
| Maps to virtual credential `mapsToVirtualCredential` | toggle | optional | on | — | — | The external card maps to a TICVAI Virtual Ticket rather than being validated by the external system | `setHotelWalletExternal` body |
| Status `status` | segmented control | optional | Draft | Draft · Active · Inactive | — | — | `setHotelWalletExternal` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **integrationType**: Cards Hotel room card, Hotel PMS, Digital wallet, Other external. *(source: contracts/spine/access.yaml#setHotelWalletExternal)*
- **name / externalSystem**: Name (e.g. "Yas Hotel - Opera PMS") and external system (e.g. "Oracle Opera Cloud"), both required. *(source: contracts/spine/access.yaml#setHotelWalletExternal / DI-638)*
- **connectionSecretRef**: "Connection credentials" as a picker of stored secrets with status (Set / Missing) and "Request from client" - never a password field. *(source: contracts/spine/access.yaml#/components/schemas/HotelWalletExternalMediaIntegrationInput)*
- **roomChargeEnabled**: Switch "Allow charges to the room", only for Hotel PMS; default off. *(source: screens/P08-venue-back-office.yaml#BO-182 / contracts/spine/access.yaml#setHotelWalletExternal)*
- **mapsToVirtualCredential**: Default on, worded "The card maps to a TICVAI ticket" vs off "The external system validates the card". *(source: contracts/spine/access.yaml#setHotelWalletExternal)*
- **Hotel, room card provider, card format, eligible parks, package mapping**: The pack's hotel credential fields; draw them in a "Hotel card" section, greyed until the contract holds them. *(source: screens/P08-venue-back-office.yaml#BO-182)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save integration (primary button) | `setHotelWalletExternal` PUT `/hotel-wallet-external` | HotelWalletExternalMediaIntegrationInput | HotelWalletExternalMediaIntegrationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Activating an integration that has no connectionSecretRef | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Integration list**: Name, Type, External system, Room charge, Status (Draft, Active, Inactive) with "Credentials missing" warning. *(source: contracts/spine/access.yaml#listHotelWalletExternal)*
- **Flow strips**: Room card > Room 1408 resolved > Package 2A+2C / 3-day > Access decision; Billing - Attraction or service > Guest room > PMS > Room charge. *(source: screens/P08-venue-back-office.yaml#BO-182)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save integration**: Upsert keyed by integrationId (absent creates); moving to Active without a secret reference is refused with "Add connection credentials first". *(source: contracts/spine/access.yaml#setHotelWalletExternal)*

**Data it reads**: `listHotelWalletExternal` (onLoad, Hotel, Wallet & External Media Integration)

**Where the user goes next**

- → `BO-174` Media & Credential Command Center: *Returns to the board's landing screen*; calls `listHotelWalletExternal`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hotel wallet external list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hotel wallet external untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hotel wallet external yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hotel wallet external are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Activating an integration that has no connectionSecretRef |

#### Edge cases to draw

- **PMS unreachable at the gate**: Hotel guests are referred to an operator for a zero-value ticket after room lookup and ID check (DI-638), not denied. *(source: DI-638)*
- **Viewer without configuration rights**: Save disabled with "Needs access configuration rights" (VO-R08). *(source: contracts/spine/access.yaml#setHotelWalletExternal)*

#### Consistency with other screens

- Match `POS-005`: Charge to room as a payment uses the same PMS integration and wording.
- Match `BO-181`: Partner barcodes are mapped there; hotel cards here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
integrations:
- name: Yas Hotel - Opera PMS
  type: Hotel PMS
  system: Oracle Opera Cloud
  roomCharge: true
  credentials: Set
  status: Active
- name: Yas Hotel room cards
  type: Hotel room card
  system: Assa Abloy Vostio
  mapsToTicket: true
  status: Draft
- name: Apple Wallet passes
  type: Digital wallet
  system: Apple Wallet
  status: Active
example:
  room: '1408'
  package: 2 Adults + 2 Children / 3-Day Park Access
  charge: AED 145.00 to room 1408
```

#### Permissions

- `listHotelWalletExternal` → `SCOPE_VIEW` (read) · staff
- `setHotelWalletExternal` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Affiliated-hotel guests get a zero-value ticket/wristband after room-number lookup and identity verification, or charge on-site purchases to their room via the same lookup (PMS such as Opera). *(client request · MoM 2 Sep 2026, 4.9 Hotel/PMS integration · DI-638)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-182` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-182`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 16: Works in Hotel, Wallet & External Media Integration → Configure specialized external credential ecosystems. The source specifically requires hotel room-card integration at access points and an interface to the hotel's property-management system for room …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-182?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save integration.
- [ ] Every transition is wired: `BO-174`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-183` Media Compatibility, Testing & Publication

**Ensure that every configured medium works with the intended access-control hardware before deployment. This is particularly important because the matrix says the solution should operate with hardware selected by the venue, while hardware limitations must be highlighted and recommended equipment exposed for procurement decisions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-183 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-compatibility-testing-publication-bo-183` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No operation runs a media compatibility test and returns its results, and no read of the compatibility matrix.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Proves each medium works on the intended hardware before deployment: a compatibility matrix of media (Dynamic QR, RFID, NFC, Face Pass, Partner QR) against device types (Turnstile A, Handheld, VIP gate, Attraction), a test console (media, reader, test credential - Media detected, Identifier decoded, Virtual credential resolved, Entitlement loaded, Access engine reached, Gate response received), hardware limitation warnings ("Reader TRN-14 does not support NFC validation in offline mode") and publication by tenant, venue, park, gate or device group. The one thing to get right: a medium cannot be published to an incompatible device without an explicit, reasoned exception.

**Known correction pending (do not draw the wrong version)**

- **The publish request carries compatibilityWarnings (a test output) and stage, and Publish is bound to no operation** Why: Warnings are produced by the test, not sent by the user; a test operation that returns them is needed and Publish should call the publish write. *(source: contracts/spine/access.yaml#publishMediaCompatibilityTesting / screens/P08-venue-back-office.yaml#BO-183; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read for the compatibility matrix or for test results** Why: The pack's matrix and test console have no source on this screen. *(source: screens/P08-venue-back-office.yaml#BO-183; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **tenantId is an input** Why: Tenant is the session's (VO-R09). *(source: contracts/spine/access.yaml#publishMediaCompatibilityTesting; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **mediaProfileId**: Picked from the media directory (BO-174 profiles); never typed. *(source: contracts/spine/access.yaml#publishMediaCompatibilityTesting)*
- **Target (venueId, parkId, gateId, deviceGroupId)**: Radio Tenant / Venue / Park / Gate / Device group with a picker; venue and tenant from the session (VO-R09). *(source: screens/P08-venue-back-office.yaml#BO-183 / contracts/spine/access.yaml#publishMediaCompatibilityTesting)*
- **Test console (media, reader, credential)**: Media profile, a registered reader (e.g. Main Gate Reader 03), and a test credential issued for testing only. *(source: screens/P08-venue-back-office.yaml#BO-183)*
- **exceptionReason**: Appears only when a target device has a compatibility warning; required, with the warning quoted above it. *(source: screens/P08-venue-back-office.yaml#BO-183 / contracts/spine/access.yaml#publishMediaCompatibilityTesting)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish (primary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Compatibility matrix**: Rows media, columns device types (or models); cells Supported (tick), Supported online only (tick with cloud), Not supported (dash) - never colour alone. *(source: screens/P08-venue-back-office.yaml#BO-183)*
- **Test results**: The six steps ticked in order; the first failure stops and names the step. *(source: screens/P08-venue-back-office.yaml#BO-183)*
- **Warnings and AI**: Hardware limitation warnings, and advisory AI notes such as "Gate 12 receives approximately 2,400 guests/hour. The configured reader profile may create a throughput bottleneck" (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-183)*
- **Lifecycle**: Draft > Compatibility test > Validate > Approval > Publish stepper, as on BO-153 and BO-163. *(source: screens/P08-venue-back-office.yaml#BO-183)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Run test**: Executes the test against the chosen reader and shows the steps; does not consume or admit. *(source: screens/P08-venue-back-office.yaml#BO-183 / DI-639)*
- **Publish**: Publish gate names media, targets and device count; with warnings it requires the exception reason and records it. *(source: contracts/spine/access.yaml#publishMediaCompatibilityTesting)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media compatibility testing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media compatibility testing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media compatibility testing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the media compatibility testing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reader offline during the test**: Test stops at "Media detected" with "Reader offline - last heartbeat 09:12". *(source: designer default)*

#### Consistency with other screens

- Match `BO-203`: Hardware Compatibility, Health, Testing & Deployment uses the same matrix from the device side; one matrix component.
- Match `BO-153`: Same lifecycle stepper and publish gate.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
- media: Dynamic QR
  turnstile: Supported
  handheld: Supported
  vipGate: Supported
  attraction: Supported
- media: NFC
  turnstile: Online only (TRN-14)
  handheld: Supported
  vipGate: Supported
  attraction: Not supported
- media: Face Pass
  turnstile: Not supported
  handheld: Not supported
  vipGate: Supported
  attraction: Supported
test:
  media: RFID wristband
  reader: Main Plaza Gate 3 Reader
  credential: TEST-RFID-0001
  result: All 6 steps passed
```

#### Permissions

- `publishMediaCompatibilityTesting` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Media compatibility testing validates that each supported media type works at each gate/device before go-live. *(client request · MoM 2 Sep 2026, 4.9 Media & Credential Configuration · DI-639)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-183` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS21 Access Control Board 4.dc.html#bo-183`
- Workshop pack: Access Control Module_Reference.pdf board 4
- Flow F114 *Access Control board 4: Media & Credential Command Center*, step 18: Works in Media Compatibility, Testing & Publication → Ensure that every configured medium works with the intended access-control hardware before deployment. This is particularly important because the matrix says the solution should operate with hardware …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-183?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish, What publishing changes.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listExternalPartnerCredential": {"method":"GET","path":"/external-partner-credential","contract":"access","summary":"External & Partner Credential Mapping","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ExternalPartnerCredentialMappingView"},
"listHotelWalletExternal": {"method":"GET","path":"/hotel-wallet-external","contract":"access","summary":"Hotel, Wallet & External Media Integration","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"HotelWalletExternalMediaIntegrationView"},
"listMediaCredential": {"method":"GET","path":"/media-credential","contract":"access","summary":"Media & Credential Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"tenantId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"media","in":"query","required":false},{"name":"credentialType","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"integration","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMediaIssuanceEncoding": {"method":"GET","path":"/media-issuance-encoding","contract":"access","summary":"Media Issuance & Encoding Profile","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaIssuanceEncodingProfileView"},
"listMediaSwapReplacement": {"method":"GET","path":"/media-swap-replacement","contract":"access","summary":"Media Swap & Replacement","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMediaTypeTechnology": {"method":"GET","path":"/media-type-technology","contract":"access","summary":"Media Type & Technology Library","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaTypeTechnologyLibraryView"},
"listVerificationMethodSelection": {"method":"GET","path":"/verification-method-selection","contract":"access","summary":"Verification Method Selection & Locking","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VerificationMethodSelectionLockingView"},
"listVirtualCredentialMedia": {"method":"GET","path":"/virtual-credential-media","contract":"access","summary":"Virtual Credential & Media Association","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishMediaCompatibilityTesting": {"method":"PUT","path":"/media-compatibility-testing","contract":"access","summary":"Media Compatibility, Testing & Publication","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaCompatibilityTestingPublicationInput","responds":"MediaCompatibilityTestingPublicationView"},
"setHotelWalletExternal": {"method":"PUT","path":"/hotel-wallet-external","contract":"access","summary":"Save a hotel, wallet or external media integration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"HotelWalletExternalMediaIntegrationInput","responds":"HotelWalletExternalMediaIntegrationView"},
"setMediaIssuanceEncoding": {"method":"PUT","path":"/media-issuance-encoding","contract":"access","summary":"Save a media issuance and encoding profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaIssuanceEncodingProfileInput","responds":"MediaIssuanceEncodingProfileView"},
"setMediaTypeTechnology": {"method":"PUT","path":"/media-type-technology","contract":"access","summary":"Add, amend or retire a media type","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaTypeTechnologyLibraryInput","responds":"MediaTypeTechnologyLibraryView"},
"setRfidNfc": {"method":"PUT","path":"/rfid-nfc","contract":"access","summary":"RFID & NFC Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RfidNfcConfigurationInput","responds":"RfidNfcConfigurationView"},
"setVerificationMethodPolicy": {"method":"PUT","path":"/verification-method-policies","contract":"access","summary":"Set the verification method policy of a product","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessVerificationMethodPolicy","responds":"AccessVerificationMethodPolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessVerificationMethodPolicy": {"type":"object","x-ticvai-persistence":"access.verification_method_policy","description":"The verification method selection and locking policy for one product - methods the guest may choose, lock on first successful access, who may change it after lock and the reason vocabulary (declared 29 September, data-model close-out DM1).","required":["id","productId","availableMethods","lockOnFirstSuccessfulAccess","changeAfterLock","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The policyId of listVerificationMethodSelection"},"productId":{"type":"string","format":"uuid","description":"Unique per scope"},"availableMethods":{"type":"array","items":{"type":"string","enum":["dynamicQr","physicalCard","rfid","facePass","faceTag"]}},"lockOnFirstSuccessfulAccess":{"type":"boolean","default":true},"changeAfterLock":{"type":"string","enum":["notAllowed","supervisorApproval"],"default":"supervisorApproval","description":"Who may change the method once locked; guests may not"},"reasonCodes":{"type":"array","items":{"type":"string","enum":["lostPhone","damagedWristband","accessibility","deviceFailure","guestService","other"]},"description":"Reason vocabulary for a method change after lock"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ExternalPartnerCredentialMappingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What External & Partner Credential Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"validationMode":{"type":"string","enum":["localMapping","apiValidation","tokenValidation","cachedValidation","offlineMapping","hybrid"],"description":"How the partner credential is validated"},"mappingId":{"type":"string"},"partnerName":{"type":"string","description":"e.g. Hotel Package Provider"},"credentialFormat":{"type":"string","description":"Partner barcode/QR format"},"fieldMappings":{"type":"array","items":{"type":"string"},"description":"Partner field to TICVAI field pairs, e.g. ProductCode, VisitDate, GuestType, Entitlement"},"unrecognisedOutcome":{"type":"string","enum":["deny","referToOperator"],"description":"What happens when a partner credential cannot be resolved"},"status":{"type":"string","enum":["draft","active","inactive"]}}},
"HotelWalletExternalMediaIntegrationInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Hotel, Wallet & External Media Integration submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["name","integrationType","externalSystem"],"properties":{"integrationId":{"type":"string","format":"uuid","description":"Absent creates an integration"},"name":{"type":"string","maxLength":200},"integrationType":{"type":"string","enum":["hotelRoomCard","hotelPms","digitalWallet","otherExternal"]},"externalSystem":{"type":"string","maxLength":200,"description":"The external system, e.g. the hotel PMS product"},"connectionSecretRef":{"type":"string","description":"Reference to the stored credentials of the external system. **Never the secret itself.** The client supplies the account and keys (vendor credential); the reference is set once they are stored"},"roomChargeEnabled":{"type":"boolean","default":false},"mapsToVirtualCredential":{"type":"boolean","default":true,"description":"The external card maps to a TICVAI Virtual Ticket rather than being validated by the external system"},"status":{"type":"string","enum":["draft","active","inactive"],"default":"draft"}}},
"HotelWalletExternalMediaIntegrationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Hotel, Wallet & External Media Integration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"connectionSecretRef":{"type":"string","description":"Reference to the stored credentials of the external system, never the secret itself (decided 29 September, VM close-out)"},"integrationId":{"type":"string"},"integrationType":{"type":"string","enum":["hotelRoomCard","hotelPms","digitalWallet","otherExternal"]},"name":{"type":"string"},"externalSystem":{"type":"string","description":"External system name, e.g. the hotel PMS or wallet provider"},"roomChargeEnabled":{"type":"boolean","description":"Attraction/service may be charged to the guest room via the PMS"},"mapsToVirtualCredential":{"type":"boolean","description":"Credential resolves to a TICVAI virtual credential and follows the normal access decision"},"status":{"type":"string","enum":["draft","active","inactive"]}}},
"MediaCompatibilityTestingPublicationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Media Compatibility, Testing & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"mediaProfileId":{"type":"string","description":"Media profile being published"},"tenantId":{"type":"string","description":"Tenant"},"venueId":{"type":"string","description":"Venue"},"parkId":{"type":"string","description":"Park"},"gateId":{"type":"string","description":"Gate"},"deviceGroupId":{"type":"string","description":"Device group"},"stage":{"type":"string","enum":["draft","compatibilityTest","validate","approval","published"]},"compatibilityWarnings":{"type":"array","items":{"type":"string"},"description":"Warnings from the compatibility test, e.g. a reader that cannot validate NFC offline"},"exceptionReason":{"type":"string","description":"Required when publishing to a device with a compatibility warning"}},"required":["mediaProfileId","venueId"]},
"MediaCompatibilityTestingPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Compatibility, Testing & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"mediaProfileId":{"type":"string","description":"Media profile being published"},"tenantId":{"type":"string","description":"Tenant"},"venueId":{"type":"string","description":"Venue"},"parkId":{"type":"string","description":"Park"},"gateId":{"type":"string","description":"Gate"},"deviceGroupId":{"type":"string","description":"Device group"},"stage":{"type":"string","enum":["draft","compatibilityTest","validate","approval","published"]},"compatibilityWarnings":{"type":"array","items":{"type":"string"},"description":"Warnings from the compatibility test, e.g. a reader that cannot validate NFC offline"},"exceptionReason":{"type":"string","description":"Required when publishing to a device with a compatibility warning"}},"required":["mediaProfileId","venueId"]},
"MediaCredentialCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media & Credential Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"mediaProfileId":{"type":"string","description":"Media profile identifier"},"mediaProfile":{"type":"string","description":"Media profile name, e.g. Mobile Dynamic QR"},"technology":{"type":"string","description":"Technology, e.g. QR, RFID, NFC, Wallet"},"credentialType":{"type":"string","description":"Credential type, e.g. Digital Ticket, Wristband, Membership, External Ticket"},"status":{"type":"string","enum":["active","inactive"]},"offlineSupport":{"type":"string","enum":["yes","no","conditional"],"description":"Whether the medium validates offline"}}},
"MediaCredentialCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeMediaProfiles":{"type":"integer","description":"Active Media Profiles"},"qrCredentials":{"type":"integer","description":"QR Credentials"},"rfidCredentials":{"type":"integer","description":"RFID Credentials"},"nfcCredentials":{"type":"integer","description":"NFC Credentials"},"walletCredentials":{"type":"integer","description":"Wallet Credentials"},"biometricCredentials":{"type":"integer","description":"Biometric Credentials"},"externalCredentials":{"type":"integer","description":"External Credentials"},"mediaSwapsToday":{"type":"integer","description":"Media Swaps Today"},"failedMediaReads":{"type":"integer","description":"Failed Media Reads"},"unknownCredentials":{"type":"integer","description":"Unknown Credentials"},"verificationExceptions":{"type":"integer","description":"Verification Exceptions"},"ai":{"type":"array","items":{"type":"string"},"description":"Advisory AI highlights (failing media profiles, unusual read errors, duplicate identifiers, obsolete media, incompatible device/media combinations). Read-only; AI does not change ticket validity."}}},
"MediaIssuanceEncodingProfileInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Media Issuance & Encoding Profile submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back. The per-credential identifiers the View shows (credential identifier, randomised media identifier, ticket reference, secure token and reference) are generated at issue and are not writable.","required":["name","mediaTypeId","encodingFormat"],"properties":{"encodingProfileId":{"type":"string","format":"uuid","description":"Absent creates a profile"},"name":{"type":"string","maxLength":200},"mediaTypeId":{"type":"string","description":"The media type this profile encodes (`MediaTypeTechnologyLibraryView.mediaTypeId`)"},"encodingFormat":{"type":"string","maxLength":100},"offlinePayloadProfile":{"type":"string","description":"Which entitlement data is embedded for offline validation"},"checksumSignatureWhereApplicable":{"type":"string","description":"Checksum or signature scheme, where the media carries one"},"randomizationEnabled":{"type":"boolean","default":true,"description":"Media identifiers are random rather than sequential"},"identifierCollisionCheckEnabled":{"type":"boolean","default":true},"duplicatePreventionEnabled":{"type":"boolean","default":true}}},
"MediaIssuanceEncodingProfileView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Issuance & Encoding Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialIdentifier":{"type":"string","description":"Credential identifier"},"randomizedMediaIdentifier":{"type":"string","description":"Randomized media identifier"},"ticketIdReference":{"type":"string","description":"Ticket ID reference"},"secureToken":{"type":"string","description":"Secure token"},"secureReference":{"type":"string","description":"Secure reference"},"encodingFormat":{"type":"string","description":"Encoding format"},"offlinePayloadProfile":{"type":"string","description":"Offline payload profile reference"},"checksumSignatureWhereApplicable":{"type":"string","description":"Reference to the signing profile managed by the secure platform layer; no key material"},"identifierCollisionCheckEnabled":{"type":"boolean","description":"Identifier Collision Check — ENABLED"},"randomizationEnabled":{"type":"boolean","description":"Randomization — ENABLED"},"encodingProfileId":{"type":"string","description":"Encoding profile identifier"},"name":{"type":"string","description":"Profile name, e.g. RFID Wristband, Adventure Park"},"mediaTypeId":{"type":"string","description":"Media type this profile encodes"},"duplicatePreventionEnabled":{"type":"boolean","description":"Duplicate prevention"}}},
"MediaSwapReplacementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Swap & Replacement displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reason":{"type":"string","enum":["lost","damaged","deviceChange","upgrade","guestRequest","operationalReplacement","fraudSecurity","accessibility"],"description":"Vocabulary listed under Swap Reasons."},"swapId":{"type":"string"},"virtualTicketId":{"type":"string","description":"Unchanged by the swap"},"fromMediaType":{"type":"string"},"fromMediaId":{"type":"string"},"toMediaType":{"type":"string"},"toMediaId":{"type":"string"},"swappedAt":{"type":"string","format":"date-time"},"operatorId":{"type":"string"}}},
"MediaTypeTechnologyLibraryInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Media Type & Technology Library submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["name","mediaType","technology","onlineOfflineCapability"],"properties":{"mediaTypeId":{"type":"string","format":"uuid","description":"Absent adds a media type"},"name":{"type":"string","maxLength":200},"mediaType":{"type":"string","enum":["linearBarcode","twoDimensionalBarcode","qr","rfidContact","rfidProximity","rfidIso15693","rfidOtherStandard","appCredential","mobileWallet","paperTicket","wristband","plasticCard","hotelCard","facePass","faceTag","partnerQr","externalBarcode","thirdPartyCredential"]},"technology":{"type":"string","enum":["barcode","rfid","nfc","magneticStripe","mobile","physical","biometric","external"]},"encodingFormat":{"type":"string","maxLength":100},"supportedReaderTypes":{"type":"array","items":{"type":"string"}},"onlineOfflineCapability":{"type":"string","enum":["onlineOnly","offlineOnly","onlineAndOffline"]},"writableReadOnly":{"type":"string","enum":["writable","readOnly"]},"securityClassification":{"type":"string","maxLength":100},"applicableVenues":{"type":"array","items":{"type":"string"},"description":"Empty means every venue of the tenant"},"applicableProducts":{"type":"array","items":{"type":"string"},"description":"Empty means every product"},"active":{"type":"boolean","default":true,"description":"False retires the media type: no new credential is issued on it; credentials already issued stay valid until they expire"}}},
"MediaTypeTechnologyLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Type & Technology Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"active":{"type":"boolean","description":"False once retired through `setMediaTypeTechnology`; issued credentials stay valid (decided 29 September, VM close-out)"},"mediaType":{"type":"string","enum":["linearBarcode","twoDimensionalBarcode","qr","rfidContact","rfidProximity","rfidIso15693","rfidOtherStandard","appCredential","mobileWallet","paperTicket","wristband","plasticCard","hotelCard","facePass","faceTag","partnerQr","externalBarcode","thirdPartyCredential"],"description":"The kind of medium this profile defines"},"technology":{"type":"string","enum":["barcode","rfid","nfc","magneticStripe","mobile","physical","biometric","external"],"description":"Technology family"},"encodingFormat":{"type":"string","description":"encoding format"},"supportedReaderTypes":{"type":"array","items":{"type":"string"},"description":"supported reader types"},"onlineOfflineCapability":{"type":"string","enum":["onlineOnly","offlineOnly","onlineAndOffline"],"description":"online/offline capability"},"writableReadOnly":{"type":"string","enum":["writable","readOnly"],"description":"writable/read-only"},"securityClassification":{"type":"string","description":"security classification"},"applicableVenues":{"type":"array","items":{"type":"string"},"description":"Venue ids"},"applicableProducts":{"type":"array","items":{"type":"string"},"description":"Product ids"},"mediaTypeId":{"type":"string","description":"Media type profile identifier"},"name":{"type":"string","description":"Profile name"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RfidNfcConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What RFID & NFC Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"name":{"type":"string"},"rfidNfcProfileId":{"type":"string","description":"RFID/NFC profile identifier"},"rfidStandard":{"type":"string","description":"RFID standard"},"tagCardType":{"type":"string","description":"tag/card type"},"frequencyInterfaceProfile":{"type":"string","description":"frequency/interface profile"},"readerCompatibility":{"type":"array","items":{"type":"string"},"description":"reader compatibility"},"readWriteBehavior":{"type":"string","description":"read/write behavior"},"encodingProfile":{"type":"string","description":"encoding profile"},"securityProfile":{"type":"string","description":"security profile"},"nfcUses":{"type":"array","items":{"type":"string","enum":["nfcTicket","membership","mobileDevice","walletCredential"]},"description":"NFC credential uses enabled by this profile"},"supportedReaders":{"type":"array","items":{"type":"string"},"description":"supported readers"},"offlineCapability":{"type":"boolean","description":"offline capability"},"venueId":{"type":"string","description":"Venue"},"zoneId":{"type":"string","description":"Zone"},"gateId":{"type":"string","description":"Gate"},"credentialType":{"type":"string","description":"Credential"},"journey":{"type":"string","description":"Journey"},"readRange":{"type":"string","enum":["near","medium","far"],"description":"Read range associated with the venue, zone, gate, credential or journey"}},"required":["rfidNfcProfileId","venueId","name"]},
"RfidNfcConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What RFID & NFC Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string"},"rfidNfcProfileId":{"type":"string","description":"RFID/NFC profile identifier"},"rfidStandard":{"type":"string","description":"RFID standard"},"tagCardType":{"type":"string","description":"tag/card type"},"frequencyInterfaceProfile":{"type":"string","description":"frequency/interface profile"},"readerCompatibility":{"type":"array","items":{"type":"string"},"description":"reader compatibility"},"readWriteBehavior":{"type":"string","description":"read/write behavior"},"encodingProfile":{"type":"string","description":"encoding profile"},"securityProfile":{"type":"string","description":"security profile"},"nfcUses":{"type":"array","items":{"type":"string","enum":["nfcTicket","membership","mobileDevice","walletCredential"]},"description":"NFC credential uses enabled by this profile"},"supportedReaders":{"type":"array","items":{"type":"string"},"description":"supported readers"},"offlineCapability":{"type":"boolean","description":"offline capability"},"venueId":{"type":"string","description":"Venue"},"zoneId":{"type":"string","description":"Zone"},"gateId":{"type":"string","description":"Gate"},"credentialType":{"type":"string","description":"Credential"},"journey":{"type":"string","description":"Journey"},"readRange":{"type":"string","enum":["near","medium","far"],"description":"Read range associated with the venue, zone, gate, credential or journey"}},"required":["rfidNfcProfileId","venueId","name"]},
"VerificationMethodSelectionLockingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Verification Method Selection & Locking displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"availableMethods":{"type":"array","items":{"type":"string","enum":["dynamicQr","physicalCard","rfid","facePass","faceTag"]},"description":"Verification methods the guest may choose from"},"reason":{"type":"string","enum":["lostPhone","damagedWristband","accessibility","deviceFailure","guestService","other"],"description":"Reason code vocabulary for a method change; every change is audited"},"policyId":{"type":"string","description":"Verification method policy identifier"},"productId":{"type":"string","description":"Product the policy applies to"},"lockOnFirstSuccessfulAccess":{"type":"boolean","description":"The chosen method locks at the first successful access"},"changeAfterLock":{"type":"string","enum":["notAllowed","supervisorApproval"],"description":"Who may change the method once locked; guests may not"}}},
"VirtualCredentialMediaAssociationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Credential & Media Association displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticketId":{"type":"string","description":"Ticket"},"guestId":{"type":"string","description":"Guest"},"entitlements":{"type":"array","items":{"type":"string"},"description":"Entitlement ids on the ticket"},"consumptionState":{"type":"string","description":"Current consumption state of the entitlement"},"virtualCredentialId":{"type":"string","description":"The single virtual credential every medium resolves to"},"linkedMedia":{"type":"array","items":{"type":"string"},"description":"Media identifiers linked to this credential (QR, RFID, wallet, NFC, Face Pass)"},"activeMedia":{"type":"array","items":{"type":"string"},"description":"Linked media currently allowed to be used; linked does not mean usable at the same time"}}}
}
```
