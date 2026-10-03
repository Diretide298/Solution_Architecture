# WS61 — Ticket Media   Credential Management board 3

**10 screens · 19 operations · 22 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, ORDER_EXCHANGE, ORDER_REPRINT, ORDER_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW, TICKET_LOOKUP`. A control nobody can use must say so,
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
| `BO-354` | Credential Operations Command Center | B–D | 2 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-355` | Virtual Ticket & Credential 360° Workspace | B–D | 0 | 46 | 6 | 2 | 3 | 0 | — | notStarted (generated) |
| `BO-356` | Credential Generation & Issuance Monitor | B–D | 10 | 28 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-357` | Credential Delivery & Distribution Operations | B–D | 5 | 20 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-358` | Media Binding, Activation & Assignment Operations | B–D | 0 | 34 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `BO-359` | Credential Replacement, Reissue, Revocation & Recovery | B–D | 11 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-360` | Failed Generation, Delivery & Credential Exception Management | B–D | 4 | 22 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-361` | Credential Usage & Cross-Media Traceability | B–D | 11 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-362` | Credential Security, Audit & Operational Evidence | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-363` | Ticket Media Analytics & AI Operations Intelligence | B–D | 2 | 42 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-362 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-354` Credential Operations Command Center

**Provide Operations, Ticketing, Customer Service and Technical teams with a real-time command center covering all issued credential media. This is the operational starting point for Area 15.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-operations-command-center-bo-354` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The operational hub for issued credential media (board 15.3): one live view of every credential's generation, delivery, binding and activation state, the exceptions, and the health of each provider, for operations, ticketing, customer service and technical teams. It opens the nine operational screens. The one thing to get right: problems first - failed generation and delivery, tickets without active media for tomorrow's events, and degraded providers sit at the top; a row always opens its ticket.

**Known correction pending (do not draw the wrong version)**

- **Operational health indicators are not returned** Why: The contract removed the sample percentages and with them the indicator itself; a per-provider health figure is needed for the pack's health panel. *(source: screens/P08-venue-back-office.yaml#BO-354 / contracts/spine/access.yaml#listCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation declares transitions only to BO-355, 356, 358, 360, 361 though exits list BO-357, 359, 362, 363** Why: All nine board screens are reached from the hub (DI-653). *(source: screens/P08-venue-back-office.yaml#BO-354 / DI-653; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The contract says Resend has no operation** Why: deliverCredential now exists (29 September close-out); bind Resend to it. *(source: contracts/spine/access.yaml#listCredential / contracts/spine/access.yaml#deliverCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every credential operations", "The selected credential operations" and the permissions banner** Why: Generated placeholders (VO-R12); permissions become per-action enablement (VO-R08). *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039 / ADR-0002 / DI-387; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search credential operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by brand, venue, event, product, date, media and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | text field | — | — | `listCredential` ?brand |
| Venue | text field | — | — | `listCredential` ?venue |
| Date | text field | — | — | `listCredential` ?date |
| Media | text field | — | — | `listCredential` ?media |
| Status | text field | — | — | `listCredential` ?status |
| Channel | text field | — | — | `listCredential` ?channel |
| Customer | text field | — | — | `listCredential` ?customer |
| Event | text field | — | — | `listCredential` ?event |
| Product | text field | — | — | `listCredential` ?product |
| Provider | text field | — | — | `listCredential` ?provider |
| Exception | text field | — | — | `listCredential` ?exception |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search credential operations**: Virtual Ticket ID, credential id or media code, holder name; a media code resolves to its ticket (as BO-334). *(source: contracts/spine/access.yaml#listCredential / contracts/spine/access.yaml#lookupTicket)*
- **Filter by**: Brand, Venue (from the switcher), Event, Product, Date (default today and tomorrow), Media, Provider, Status, Channel, Exception (has / none), Customer; the first five as chips. *(source: screens/P08-venue-back-office.yaml#BO-354 / contracts/spine/access.yaml#listCredential)*

#### Outputs: what the screen shows and produces

**Shown**

**Virtual Tickets Issued** (metric tile)

**Credentials Generated** (metric tile)

**Active Credentials** (metric tile)

**Pending Generation** (metric tile)

**Pending Delivery** (metric tile)

**Pending Binding** (metric tile)

**Pending Activation** (metric tile)

**Suspended** (metric tile)

**Revoked** (metric tile)

**Expired** (metric tile)

**Failed Generation** (metric tile)

**Failed Delivery** (metric tile)

**Synchronization Exceptions** (metric tile)

**Multi-Media Virtual Tickets** (metric tile)

**Virtual Tickets Without Active Media** (metric tile)

**Every credential operations** (data table, from `listCredential`)

| Shows | Format | Notes |
|---|---|---|
| Media type | text | Media Type |
| Customer participant | text | Customer / Participant |
| Credential status | chip: Pending generation, Generated, Pending activation, Active, Suspended, Revoked… | Credential status |
| Delivery status | chip: Not required, Pending, Sent, Delivered, Opened downloaded, Completed… | Delivery status (15.3.4) |
| Activation status | chip: Pending, Scheduled, Active, Not required | Activation status |
| Binding status | chip: Pending, Bound, Unbound, Failed | Binding status |

**The selected credential operations** (detail panel): The pack groups this record's detail under its own headings: “Display credentials by”, “Provide indicators such as”.

| Shows | Format | Notes |
|---|---|---|
| Media type | text | Media Type |
| Customer participant | text | Customer / Participant |
| Product | text | Product |
| Event | text | Event |
| Credential status | chip: Pending generation, Generated, Pending activation, Active, Suspended, Revoked… | Credential status |
| Delivery status | chip: Not required, Pending, Sent, Delivered, Opened downloaded, Completed… | Delivery status (15.3.4) |
| Activation status | chip: Pending, Scheduled, Active, Not required | Activation status |
| Binding status | chip: Pending, Bound, Unbound, Failed | Binding status |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Open Virtual Ticket, Generate Credential, Resend, Activate, Suspend Media, Replace, Revoke, Diagnose, View History. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Fifteen tiles per VO-R02 in three rows - volume (Virtual Tickets issued, Credentials generated, Active), pipeline (Pending generation, delivery, binding, activation) and problems (Failed generation, Failed delivery, Synchronisation exceptions, Without active media, Suspended, Revoked, Expired, Multi-media). Problem tiles red when non-zero and filter the queue. *(source: screens/P08-venue-back-office.yaml#BO-354 / contracts/spine/access.yaml#/components/schemas/CredentialOperationsCommandCenterViewSummary)*
- **Media breakdown**: A horizontal bar of credentials by medium (Dynamic QR, Barcode, PDF, Apple Wallet, Google Wallet, RFID, NFC, Face reference, Card, Wristband, Other), not a table. *(source: screens/P08-venue-back-office.yaml#BO-354 / contracts/spine/access.yaml#/components/schemas/CredentialOperationsCommandCenterViewSummary)*
- **Operational health**: One line per provider capability with a status (QR generation 99.98% Healthy; RFID encoding 98.7% Healthy; Apple Wallet updates Attention; Google Wallet Healthy). *(source: screens/P08-venue-back-office.yaml#BO-354)*
- **Operational queue**: Title "Credentials". Columns Virtual Ticket, Credential, Media, Customer / participant, Product, Event, then four status pills (Credential, Delivery, Activation, Binding), Provider, Last activity, Exception, Owner. Default sort: rows with an exception first, then event date. Cursor paging. *(source: contracts/spine/access.yaml#/components/schemas/CredentialOperationsCommandCenterView)*
- **AI priorities**: Top-of-page advisory line in the pack's style ("84 Apple Wallet credentials for tomorrow's event have not received the latest performance-time update") with Show these. *(source: screens/P08-venue-back-office.yaml#BO-355)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Row quick actions**: Open Virtual Ticket and View history open BO-355; Resend opens the send dialog (deliverCredential, ORDER_REPRINT); Activate goes to BO-358; Replace to BO-359; Suspend media to the lock manager BO-247. Generate credential, Revoke and Diagnose have no operation and are drawn disabled "Not available yet". *(source: contracts/spine/access.yaml#listCredential / contracts/spine/access.yaml#deliverCredential / contracts/spine/access.yaml#lockIdentity)*
- **Board tiles**: Nine tiles to BO-355 to BO-363, each returning here (VO-R13). *(source: DI-653)*

**Data it reads**: `listCredential` (onLoad, Credential Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-355` Virtual Ticket & Credential 360° Workspace: *Works in Virtual Ticket & Credential 360° Workspace*; calls `listCredential`
- → `BO-356` Credential Generation & Issuance Monitor: *Works in Credential Generation & Issuance Monitor*; calls `listCredential`
- → `BO-358` Media Binding, Activation & Assignment Operations: *Works in Media Binding, Activation & Assignment Operations*; calls `listCredential`
- → `BO-360` Failed Generation, Delivery & Credential Exception Management: *Works in Failed Generation, Delivery & Credential Exception Management*; calls `listCredential`
- → `BO-361` Credential Usage & Cross-Media Traceability: *Works in Credential Usage & Cross-Media Traceability*; calls `listCredential`
- → `BO-362` Credential Security, Audit & Operational Evidence: *Works in Credential Security, Audit & Operational Evidence*; calls `listCredential`
- → `BO-363` Ticket Media Analytics & AI Operations Intelligence: *Works in Ticket Media Analytics & AI Operations Intelligence*; calls `listCredential`
- → `BO-357` Credential Delivery & Distribution Operations: *Works in Credential Delivery & Distribution Operations*; carries `credentialId`; calls `listCredential`
- → `BO-359` Credential Replacement, Reissue, Revocation & Recovery: *Works in Credential Replacement, Reissue, Revocation & Recovery*; carries `credentialId`; calls `listCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Provider outage (for example the wallet service)**: Health line red, a banner with the count of affected credentials and "Use fallback" leading to BO-360 filtered to the provider. *(source: screens/P08-venue-back-office.yaml#BO-354 / contracts/spine/access.yaml#resolveCredentialException)*
- **Customer service agent without configuration rights**: Can resend (ORDER_REPRINT) but not activate or bind; those actions are disabled with the reason (VO-R08). *(source: contracts/spine/access.yaml#deliverCredential)*

#### Consistency with other screens

- Match `BO-334`: Same status words and media icons; BO-334 per ticket, this per credential.
- Match `BO-644`: The accreditation credential hub is a different estate (badges); do not merge.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  ticketsIssued: 18420
  generated: 31260
  active: 27410
  pendingGeneration: 42
  pendingDelivery: 310
  pendingBinding: 1210
  pendingActivation: 880
  suspended: 6
  revoked: 14
  expired: 120
  failedGeneration: 9
  failedDelivery: 37
  syncExceptions: 4
  multiMedia: 6120
  withoutActiveMedia: 128
queue:
- ticket: VT-2026-009821
  credential: RF-10452
  media: RFID wristband
  customer: Sara Al Nuaimi
  event: Sat 10 Oct
  credentialStatus: Active
  delivery: Not required
  activation: Active
  binding: Bound
  provider: HID
- ticket: VT-2026-012230
  credential: AW-55321
  media: Apple Wallet
  customer: James Carter
  event: Sun 11 Oct
  credentialStatus: Generated
  delivery: Failed
  exception: Wallet update failed
  owner: Maria Santos
```

#### Permissions

- `listCredential` → `SCOPE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-354` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-354`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 1: Opens Credential Operations Command Center → Provide Operations, Ticketing, Customer Service and Technical teams with a real-time command center covering all issued credential media. This is the operational starting point for Area 15.
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F170 branch at step 1 (expected): when Nothing has been set up on Credential Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F170 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-354?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-355`, `BO-356`, `BO-358`, `BO-360`, `BO-361`, `BO-362`, `BO-363`, `BO-357`, `BO-359`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-355` Virtual Ticket & Credential 360° Workspace

**Provide a complete operational view of one Virtual Ticket and every media credential currently or historically associated with it. This is one of the most important operational screens.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display; Identify) and a per-row directory (§For each media show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `entitlementId` (navigation) |
| Route | `/access-venue/virtual-ticket-credential-360-workspace-bo-355` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The 360 workspace was bound to setVirtualTicketCredential, a PUT, as its data; the contract itself says the screen writes nothing. It reads the entitlement, its …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Everything about one Virtual Ticket and every medium it has ever had: a header with the ticket (ID, holder, participant, product, event, performance, venue, seat, order, status, usage, validity, remaining entitlements), a credential wallet listing each medium with its role and status (including revoked history), one chronological timeline, and the operational actions. Customer service and operations open it from any row in BO-334 or BO-354. The one thing to get right: it is one ticket - media are rows inside it, revoked media stay visible as history, and the ticket ID at the top never changes through replacements, transfers or resale.

**Known correction pending (do not draw the wrong version)**

- **Header fields drawn as eighteen metric tiles (Virtual Ticket ID, Holder, Seat, Primary, Fallback...)** Why: They are record fields and media roles, not KPIs (VO-R02 tiles are for command centres). *(source: screens/P08-venue-back-office.yaml#BO-355; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No entry parameter for the ticket** Why: The workspace is about one ticket; it must receive virtualTicketId from BO-334 and BO-354. *(source: screens/P08-venue-back-office.yaml#BO-355; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The screen is bound to setVirtualTicketCredential, a PUT, as its data (CHG-WIR-001); "Save changes" button (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Rotate | toggle | off | — | `getEntitlementCredential` ?rotate |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **virtualTicketId (entry)**: The screen opens with a ticket id from the calling row; without one it shows a lookup box (ticket id or media code) rather than an empty page. *(source: contracts/spine/access.yaml#lookupTicket / screens/P08-venue-back-office.yaml#BO-355)*

#### Outputs: what the screen shows and produces

**Shown**

**Virtual Ticket ID** (metric tile)

**Ticket Holder** (metric tile)

**Participant** (metric tile)

**Product** (metric tile)

**Event** (metric tile)

**Performance** (metric tile)

**Venue** (metric tile)

**Seat** (metric tile)

**Order** (metric tile)

**Ticket Status** (metric tile)

**Usage Status** (metric tile)

**Validity** (metric tile)

**Entitlements** (metric tile)

**Primary** (metric tile)

**Secondary** (metric tile)

**Fallback** (metric tile)

**Temporary** (metric tile)

**Revoked historical media** (metric tile)

**The ticket** (detail panel, from `getEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | A UUIDv7, matching `TicketStatus.ticketId` — stable for the life of the ticket and independent of the media carrying it. |
| Template | the name it points at, never the id | The definition it was issued against. Pinned at issue — a template edited next month must not change what this guest bought. |
| Product | the name it points at, never the id | — |
| Order | the name it points at, never the id | The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). |
| Order line | the name it points at, never the id | — |
| Subject | the name it points at, never the id | Who holds it. Null is legitimate — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is … |
| Venue | the name it points at, never the id | — |
| Media code | text | What is scanned — a QR payload, a wristband serial, a card number. Rotatable without reissuing, because a guest whose wristband broke … |
| Status | chip: Issued, Partially consumed, Fully consumed, Expired, Cancelled, Surrendered | What the storage layer holds, and what a guest is shown. `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot … |
| Status note | text | Not `TicketStatus` — that is a validation result with a misleading name, computed at scan time and carrying `isValid` and `isInsideVenue`. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Resolved at issue from the template, then owned here. A freeze extends it, a reissue replaces it, and neither reaches back to the template. |
| Entries used | 1,234 | The number `validateAccess` decrements and nothing was decrementing. A ten-entry pass with no counter is a ten-entry pass that admits … |
| Entries allowed | 1,234 | — |
| Last entry at | 1 Oct 2026, 14:30 | `recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. |
| First entry at | 1 Oct 2026, 14:30 | `recordedAt` of the first admission, written by the same writes as `lastEntryAt`; it starts a time-bound entitlement's window (DEC-232 … |
| Time bound until | 1 Oct 2026, 14:30 | Where the template is time-bound, when its window closes: `firstEntryAt` plus the validity rule's `minutesAfterFirstScan` (decided 2 … |
| Lifecycle label | chip: Created, Pending fulfillment, Active, Partially used, Used, Expired… | The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model (decided 2 October 2026, Chinmay, critical set 2 … |
| Cancellation kind | chip: Voided, Refunded, Performance cancelled, Superseded | Which act cancelled the entitlement, so the pack's Voided, Refunded and Reissued / superseded are told apart while `status` keeps the one … |
| Frozen days | 1,234 | Days added by a freeze. Maintained on write by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by … |

**Credential** (detail panel, from `getEntitlementCredential`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Payload | text | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Rotation | grouped details | The time-based seed the rotating code is derived from (audit R230). Null for a credential that does not rotate (a wristband serial, a … |
| Secret | text | Base32 shared secret. Held on the device and in the gates' offline package; replaced by `rotate=true`. |
| Time step seconds | 1,234 | 30 seconds for an admission QR (Chinmay, 3 October 2026, Block A business rules: GST-055's admission QR rotates every 30 seconds … |
| Digits | 1,234 | — |
| Algorithm | chip: SHA1, SHA256, SHA512 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | The seed stops verifying after this. The app fetches a fresh one whenever it is online before then. |

**History** (data table, from `getEntitlementHistory`)

| Shows | Format | Notes |
|---|---|---|
| At | 1 Oct 2026, 14:30 | — |
| Kind | chip: Issued, Scanned, Denied, Frozen, Unfrozen, Shared… | — |
| Access point name | text | — |
| Deny reason | text | — |
| By principal name | text | — |

**The selected virtual ticket credential** (detail panel): The pack groups this record's detail under its own headings: “Credential Wallet”, “Media Status”, “Dynamic QR Active”, “Apple Wallet Active”, “Old RFID RF-88410”, “Provide one chronological timeline”.

| Shows | Format | Notes |
|---|---|---|
| Binding | text | Binding ID |
| Media type | text | Media type |
| Provider | text | Provider |
| Issued | 1 Oct 2026, 14:30 | Issued |
| Delivered | 1 Oct 2026, 14:30 | Delivered |
| Activated | 1 Oct 2026, 14:30 | Activated |
| Valid from/to | text | not in the schema: `Valid From/To` |
| Last update | 1 Oct 2026, 14:30 | Last update |
| Last presentation/use | text | not in the schema: `Last presentation/use` |
| Device reference where appropriate | text | Device/reference where appropriate |
| Status | chip: Pending, Active, Suspended, Revoked, Expired | Medium status |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Generate Additional Media, Bind RFID, Add Wallet Pass, Initiate Face Enrollment, Replace Media, Suspend, Revoke, Resend, Refresh, Diagnose. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ticket header**: A header card, not KPI tiles: Virtual Ticket ID large and copyable, status and usage pills, holder and participant, product, event / performance, venue, seat, order (link), validity. Remaining entitlements as small meters (Main admission used; Guest admissions 1 of 2 left; Parking 3 of 5 left; F&B benefit 10%). *(source: screens/P08-venue-back-office.yaml#BO-355 / screens/P08-venue-back-office.yaml#BO-341 / contracts/spine/access.yaml#getEntitlement)*
- **Credential wallet**: Title "Media on this ticket". Columns Media, Credential (masked), Role (Primary / Secondary / Fallback / Temporary / Revoked history), Provider, Issued, Delivered, Activated, Valid from-to, Last update, Last presented (where), Device or reference, Status. Revoked media at the bottom, greyed, with reason and date, never removed. *(source: screens/P08-venue-back-office.yaml#BO-355 / contracts/spine/access.yaml#/components/schemas/VirtualTicketCredential360WorkspaceView)*
- **Timeline**: One list, newest first, mixing media and ticket events in plain words (Ticket created; QR generated; Apple Wallet added; RFID assigned at Main Plaza desk; Face enrolled; Entered via Face at Gate 2; RFID replaced - Lost), with actor names and venue time; denials use VO-R06 words. *(source: screens/P08-venue-back-office.yaml#BO-356 / contracts/spine/access.yaml#getEntitlementHistory)*
- **Ownership history**: Original purchaser and each transfer or resale against the same ID (VT0010 - Qossai > Allam > Chinmay style), with dates. *(source: DI-620 / DI-669)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Bind RFID / Generate additional media**: Opens BO-358 with this ticket pre-selected; refused there if the binding rule's maximum is reached. *(source: contracts/spine/access.yaml#setMediaBindingActivation / contracts/spine/access.yaml#setMediaBindingRule)*
- **Add wallet pass**: Issues an Apple or Google Wallet pass for the ticket and sends it (Resend dialog); hidden for dynamic-QR events until activated in the app. *(source: contracts/spine/orders.yaml#issueWalletPass / DI-635)*
- **Initiate face enrolment**: Starts Face Pass enrolment on the counter channel with the guest's consent step; only for products that allow Face Pass. *(source: contracts/spine/access.yaml#enrolFacePass / DI-640 / DI-641)*
- **Replace media**: Opens BO-359 with the selected medium. *(source: contracts/spine/access.yaml#replaceCredential)*
- **Suspend / Revoke**: Suspend opens the lock manager (BO-247) with lock scope "medium only" and reason; Revoke has no operation and is disabled "Not available yet". *(source: contracts/spine/access.yaml#lockIdentity)*
- **Resend**: Send dialog (channel, recipient role, recipient) - see BO-357; needs ORDER_REPRINT. *(source: contracts/spine/access.yaml#deliverCredential)*
- **Refresh dynamic code**: Replaces the rotation seed (rotate) so codes on a lost phone stop scanning once gates take the new package; confirmation says so. *(source: contracts/spine/access.yaml#getEntitlementCredential)*
- **Diagnose**: No operation; disabled "Not available yet". *(source: contracts/spine/access.yaml#setVirtualTicketCredential)*

**Data it reads**: `getEntitlement` (onLoad, The virtual ticket: one entitlement, with what remains on it); `getEntitlementCredential` (onLoad, Its current credential, masked); `getEntitlementHistory` (onLoad, Every scan, freeze, share and reissue against it)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `getEntitlement`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket credential list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket credential yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the virtual ticket credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Ticket transferred or resold**: Header shows the current holder with "Transferred from Khalid Al Zaabi on 2 Oct"; the old holder's media show Revoked in the wallet; ID unchanged. *(source: DI-620 / DI-636)*
- **Ticket of another venue**: Shown read-only with "Belongs to Summit Peaks" (VO-R09). *(source: ADR-0030)*
- **Agent without credential rights**: Read-only view; credential values always masked (only the last 4 characters). *(source: contracts/spine/access.yaml#getEntitlementCredential)*

#### Consistency with other screens

- Match `GST-013`: The guest's ticket detail shows the same media list and history wording.
- Match `SUP-010`: Customer service's ticket view should open this workspace or share its components (cross-process, support).
- Match `BO-361`: The usage trace for the same ticket is a filter of the timeline here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ticket:
  id: VT-2026-009821
  status: Active
  usage: Partly used
  holder: Sara Al Nuaimi
  product: Summit Peaks Annual Pass
  venue: Summit Peaks
  valid: 1 Oct 2026 - 30 Sep 2027
  entitlements: Main admission unlimited; Guest admissions 1 of 2 left; Parking 3 of 5 left; F&B 10%
media:
- media: Face
  credential: BIO-7721
  role: Primary
  status: Active
  lastPresented: 3 Oct 18:03 Gate 2
- media: RFID wristband
  credential: RF-10452
  role: Secondary
  status: Active
- media: Dynamic QR
  credential: QR-****8721
  role: Fallback
  status: Active
- media: Apple Wallet
  credential: AW-55321
  role: Secondary
  status: Active
- media: Old RFID
  credential: RF-88410
  role: Revoked history
  status: Revoked - Lost, 28 Sep 2026
```

#### Permissions

- `getEntitlement` → `ORDER_VIEW` (read) · staff, guest
- `getEntitlementCredential` → `ORDER_VIEW` (read) · staff, guest
- `getEntitlementHistory` → `ORDER_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.14.10 | Manage entitlement balances and usage limits. | Ticketing Sales | CONTRACTED | data `Entitlement` |
| 2.16.15 | The system shall support replacement of lost, damaged, or stolen media while automatically disabling previous media and preserving entitlement history. | Ticketing Sales | CONTRACTED | data `Entitlement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A purchased ticket can be transferred to another guest (e.g. a friend); the system keeps the original purchaser and full transfer history. *(client request · MoM 7 Sep 2026, 4.9 Ownership and transfer · DI-669)*
- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*
- Resale keeps the original virtual ticket ID; only owner name and media (QR) change. An ownership change log shows the history against one ID (e.g. VT0010: Qossai > Allam > Chinmay). *(agreed · MoM 1 Sep 2026, 4.14 Decision (ticket ID on resale) · DI-620)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-355` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-355`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 2: Works in Virtual Ticket & Credential 360° Workspace → Provide a complete operational view of one Virtual Ticket and every media credential currently or historically associated with it. This is one of the most important operational screens.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-355?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-356` Credential Generation & Issuance Monitor

**Manage and monitor generation of credential instances from approved Board 2 media templates.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show; Display) and no metric row |
| Offline | online only |
| Opens with | `exceptionId` (navigation) |
| Route | `/access-venue/credential-generation-issuance-monitor-bo-356` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Monitors credential generation from approved templates: every request's journey through the pipeline (Requested > Queued > Template resolved > Data mapped > Generated > Bound > Ready > Delivered), its trigger, template and version, and failures with their reason, plus the automatic retry policy and manual retry. The one thing to get right: retry is offered only where it can work - "Template missing" and "Required data missing" need a fix first and say which.

**Known correction pending (do not draw the wrong version)**

- **Pipeline stage names drawn as a column ("→ Bound → Ready → Delivered")** Why: A fragment of the pack's pipeline sentence; stages are the status values. *(source: screens/P08-venue-back-office.yaml#BO-356; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Automatic Retry" drawn as a primary action button** Why: It is the policy toggle; system behaviour, not a button. *(source: contracts/spine/access.yaml#setCredentialIssuanceRetryPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The list operation's note says Manual Retry, Retry Selected, Retry All Eligible and Escalate have no operation** Why: retryCredentialGeneration and resolveCredentialException now exist; the note is stale. *(source: contracts/spine/access.yaml#listCredentialGenerationIssuance / contracts/spine/access.yaml#retryCredentialGeneration; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Escalate on the generation monitor calls resolveCredentialException, which is keyed by exceptionId** Why: Monitor rows carry requestId; a failed request has no exception until escalateAfterAttempts is reached, so Escalate on a row has nothing to call. *(source: contracts/spine/access.yaml#resolveCredentialException / contracts/spine/access.yaml#/components/schemas/CredentialGenerationIssuanceMonitorView / …; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listCredentialGenerationIssuance` ?status |
| Trigger | text field | — | — | `listCredentialGenerationIssuance` ?trigger |
| Event | text field | — | — | `listCredentialGenerationIssuance` ?event |
| Venue | text field | — | — | `listCredentialGenerationIssuance` ?venue |

**Sent by *Manual Retry*** (`retryCredentialGeneration`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope `scope` | segmented control | required | — | Selected · All eligible | — | — | `retryCredentialGeneration` body |
| Requests `requestIds` | list of values (chips) | optional | — | at most 500 | — | The failed generation requests (`CredentialGenerationIssuanceMonitorView.requestId`); required for selected | `retryCredentialGeneration` body |

**Sent by *Escalate*** (`resolveCredentialException`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Retry · Regenerate · Use fallback · Escalate · Assign owner · Open technical case | — | — | `resolveCredentialException` body |
| Owner `ownerId` | text field | optional | — | — | — | Required for assignOwner and escalate | `resolveCredentialException` body |
| Fallback media kind `fallbackMediaKind` | radio group | optional | — | QR · Pdf · Printed ticket · RFID card · Wristband | — | Required for useFallback | `resolveCredentialException` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `resolveCredentialException` body |

**Sent by *Save retry policy*** (`setCredentialIssuanceRetryPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Automatic retry `automaticRetry` | toggle | required | on | — | — | — | `setCredentialIssuanceRetryPolicy` body |
| Max attempts `maxAttempts` | stepper or slider | optional | 3 | min 1; max 10 | — | — | `setCredentialIssuanceRetryPolicy` body |
| Backoff minutes `backoffMinutes` | number field (minutes) | optional | 5 | min 1; max 240 | — | Wait before the first retry; doubles on each attempt | `setCredentialIssuanceRetryPolicy` body |
| Escalate after attempts `escalateAfterAttempts` | stepper or slider | optional | 3 | min 1; max 10 | — | After this many failures the request becomes a credential exception with an owner; not more than maxAttempts | `setCredentialIssuanceRetryPolicy` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters (status, trigger, event, venue)**: Status as the pipeline stages plus Failed; trigger chips (Order confirmation, Ticket issuance, Membership activation, Customer request, Staff action, RFID collection, Wallet request, Face enrolment, API, Bulk operation, Scheduled process). *(source: screens/P08-venue-back-office.yaml#BO-356 / contracts/spine/access.yaml#listCredentialGenerationIssuance)*
- **Retry policy (automaticRetry, maxAttempts, backoffMinutes, escalateAfterAttempts)**: A small "Retry policy" card: Automatic retry on/off (default on); attempts 1-10 (default 3); first wait 1-240 minutes (default 5) with "doubles on each attempt" and a preview "5, 10, 20 min"; escalate after 1-10 attempts, not more than max attempts. Opens with the stored or default values. *(source: contracts/spine/access.yaml#setCredentialIssuanceRetryPolicy / contracts/spine/access.yaml#getCredentialIssuanceRetryPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every credential generation issuance** (data table, from `listCredentialGenerationIssuance`)

| Shows | Format | Notes |
|---|---|---|
| → bound → ready → delivered | text | not in the schema: `→ Bound → Ready → Delivered` |
| Request | text | Request ID |
| Virtual ticket | text | Virtual Ticket |
| Media | text | Media |
| Template | text | Template |
| Template version | text | Template Version |
| Product | text | Product |
| Customer | text | Customer |
| Trigger | text | not in the schema: `Trigger` |
| Provider | text | Provider |
| Requested at | 1 Oct 2026, 14:30 | Requested At |
| Generated at | 1 Oct 2026, 14:30 | Generated At |
| Status | chip: Requested, Queued, Template resolved, Data mapped, Credential generated, Bound… | Generation stage |
| Error | text | Error |

**The selected credential generation issuance** (detail panel): The pack groups this record's detail under its own headings: “Generation Sources”, “Template Resolution”, “Bulk Generation”, “Failures may include”.

| Shows | Format | Notes |
|---|---|---|
| → bound → ready → delivered | text | not in the schema: `→ Bound → Ready → Delivered` |
| Request | text | Request ID |
| Virtual ticket | text | Virtual Ticket |
| Media | text | Media |
| Template | text | Template |
| Template version | text | Template Version |
| Product | text | Product |
| Customer | text | Customer |
| Trigger | text | not in the schema: `Trigger` |
| Provider | text | Provider |
| Requested at | 1 Oct 2026, 14:30 | Requested At |
| Generated at | 1 Oct 2026, 14:30 | Generated At |
| Status | chip: Requested, Queued, Template resolved, Data mapped, Credential generated, Bound… | Generation stage |
| Error | text | Error |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Automatic Retry (primary button) | navigation or local | — | — | — | — |
| Manual Retry (secondary button) | `retryCredentialGeneration` POST `/credential-generation-issuance/retry` | CredentialGenerationRetryInput | CredentialGenerationRetryResult | 422 scope selected with no requestIds | — |
| Retry Selected (secondary button) | `retryCredentialGeneration` POST `/credential-generation-issuance/retry` | CredentialGenerationRetryInput | CredentialGenerationRetryResult | 422 scope selected with no requestIds | — |
| Retry All Eligible (secondary button) | `retryCredentialGeneration` POST `/credential-generation-issuance/retry` | CredentialGenerationRetryInput | CredentialGenerationRetryResult | 422 scope selected with no requestIds | — |
| Escalate (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Save retry policy (primary button) | `setCredentialIssuanceRetryPolicy` PUT `/credential-issuance-retry-policy` | CredentialIssuanceRetryPolicyInput | CredentialIssuanceRetryPolicyView | 422 escalateAfterAttempts greater than maxAttempts | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Pipeline strip**: The eight stages as a horizontal strip with counts in each and Failed below; clicking a stage filters the list. *(source: screens/P08-venue-back-office.yaml#BO-356 / contracts/spine/access.yaml#/components/schemas/CredentialGenerationIssuanceMonitorView)*
- **Generation list**: Title "Generation requests". Columns Request, Virtual Ticket, Media, Template (and version), Product, Customer, Trigger, Provider, Requested, Generated, Stage, Error (failure reason in words). Cursor paging. *(source: contracts/spine/access.yaml#/components/schemas/CredentialGenerationIssuanceMonitorView)*
- **Template resolution**: In the detail, why this template was chosen (brand, venue, product, event, media, channel, language, customer context). *(source: screens/P08-venue-back-office.yaml#BO-356 / contracts/spine/access.yaml#/components/schemas/CredentialGenerationIssuanceMonitorView)*
- **AI failure pattern**: Advisory line ("RFID issuance failure increased from 0.8% to 7.2% after Encoder Profile v4.1 was activated"). *(source: screens/P08-venue-back-office.yaml#BO-356)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Retry selected / Retry all eligible**: Retries failed requests whose reason is retryable; the result names any skipped and why ("3 skipped - template missing"). Manual Retry on one row is Retry selected with one id. *(source: contracts/spine/access.yaml#retryCredentialGeneration)*
- **Escalate**: Acts on the request's credential exception (owner required) - the same action as BO-360. *(source: contracts/spine/access.yaml#resolveCredentialException)*
- **Save retry policy**: Whole-policy PUT (VO-R04); 422 when escalate-after exceeds max attempts, shown on the field. *(source: contracts/spine/access.yaml#setCredentialIssuanceRetryPolicy)*
- **Bulk generate**: The pack's bulk runs (5,000 event QR tickets; 2,000 school-camp wristbands; 750 membership cards) have no operation; draw disabled "Not available yet". *(source: screens/P08-venue-back-office.yaml#BO-356 / contracts/spine/access.yaml#listCredentialGenerationIssuance)*

**Data it reads**: `listCredentialGenerationIssuance` (onLoad, Credential Generation & Issuance Monitor); `getCredentialIssuanceRetryPolicy` (onLoad, The retry policy the monitor applies)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialGenerationIssuance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential generation issuance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential generation issuance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential generation issuance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential generation issuance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The exception is already resolved; 422 escalateAfterAttempts greater than maxAttempts; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind missing for useFallback; 422 scope selected with no requestIds |

#### Edge cases to draw

- **Failure reason Template missing**: Row action "Open Media Design Studio" instead of Retry. *(source: contracts/spine/access.yaml#retryCredentialGeneration)*
- **Opened from an exception (exceptionId)**: The list opens filtered to that request with its exception panel. *(source: screens/P08-venue-back-office.yaml#BO-356)*

#### Consistency with other screens

- Match `BO-360`: Same failure reason words and the same exception actions.
- Match `BO-644`: Accreditation issuance is a different pipeline (badges); BO-644 must not reuse this list.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pipeline:
  requested: 12
  queued: 40
  templateResolved: 8
  dataMapped: 5
  generated: 3
  bound: 2
  ready: 210
  delivered: 18110
  failed: 9
rows:
- request: GEN-88120
  ticket: VT-2026-012230
  media: Apple Wallet
  template: Aqua Park Wallet v4
  trigger: Order confirmation
  provider: Apple
  requested: 1 Oct 2026 09:12
  stage: Failed
  error: Wallet generation failure
- request: GEN-88121
  ticket: VT-2026-012231
  media: RFID wristband
  template: Kids Wristband v2
  trigger: RFID collection
  stage: Failed
  error: Encoder unavailable
policy:
  automatic: true
  attempts: 3
  firstWait: 5 min
  escalateAfter: 3
```

#### Permissions

- `listCredentialGenerationIssuance` → `SCOPE_VIEW` (read) · staff
- `getCredentialIssuanceRetryPolicy` → `SCOPE_VIEW` (read) · staff
- `setCredentialIssuanceRetryPolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `retryCredentialGeneration` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `resolveCredentialException` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-356` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-356`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 4: Works in Credential Generation & Issuance Monitor → Manage and monitor generation of credential instances from approved Board 2 media templates.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-356?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Automatic Retry, Manual Retry, Retry Selected, Retry All Eligible, Escalate, Save retry policy.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-357` Credential Delivery & Distribution Operations

**Manage how generated ticket media are delivered or made available to customers, participants and operational staff.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_REPRINT`, `SCOPE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `credentialId` (navigation) |
| Route | `/access-venue/credential-delivery-distribution-operations-bo-357` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Tracks how generated media reach people - e-mail, SMS link, WhatsApp, B2C account, app, download, Apple and Google Wallet, POS, box office, kiosk, group portal, API, physical collection - with each attempt's status (Pending > Sent > Delivered > Opened / downloaded > Completed, or Failed, Bounced, Expired, Cancelled), and sends or re-sends. The one thing to get right: each send is a new attempt in the history; a resend never issues new media (that is a replacement), and destinations are masked.

**Known correction pending (do not draw the wrong version)**

- **Channels drawn as eight action buttons ("SMS Link" primary, "WhatsApp integration", "Download"...)** Why: They are values of the channel field in one Send dialog. *(source: contracts/spine/access.yaml#deliverCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The send write accepts 9 channels; the list reports 14 (adds B2C account, mobile app, box office, kiosk, group portal)** Why: A resend through a listed channel would be refused; align the enums. *(source: contracts/spine/access.yaml#deliverCredential / contracts/spine/access.yaml#/components/schemas/CredentialDeliveryDistributionOperationsView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The list's note says Send and resend have no operation** Why: deliverCredential exists (29 September close-out); only the bulk actions lack one. *(source: contracts/spine/access.yaml#listCredentialDeliveryDistribution; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listCredentialDeliveryDistribution` ?channel |
| Status | text field | — | — | `listCredentialDeliveryDistribution` ?status |

**Sent by *Send credential*** (`deliverCredential`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated delivery attempt id | `deliverCredential` body |
| Channel `channel` | select | required | — | Email · SMS link · Whatsapp · Download · Apple wallet · Google wallet · POS · API · Physical collection | — | — | `deliverCredential` body |
| Recipient `recipient` | text area | optional | — | max length 320 | — | Email address, phone number or collection point; empty sends to the recipient already on the credential | `deliverCredential` body |
| Recipient role `recipientRole` | select | optional | Ticket holder | Purchaser · Ticket holder · Participant · Guardian · Group leader · Authorized recipient | — | — | `deliverCredential` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `deliverCredential` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters (channel, status)**: Channel chips and status chips; "Problems" quick filter = Failed + Bounced + Expired. *(source: contracts/spine/access.yaml#listCredentialDeliveryDistribution)*
- **Send dialog (channel, recipientRole, recipient, note)**: Channel select; recipient role Purchaser / Ticket holder (default) / Participant / Guardian / Group leader / Authorised recipient; recipient empty = the address on the credential (shown masked), else an e-mail or +971 mobile; note max 300. The attempt id is generated by the client silently, never shown. *(source: screens/P08-venue-back-office.yaml#BO-358 / contracts/spine/access.yaml#deliverCredential)*

#### Outputs: what the screen shows and produces

**Shown**

**Every credential delivery distribution** (data table, from `listCredentialDeliveryDistribution`)

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket |
| Media | text | Media |
| Recipient | text | Recipient |
| Channel | chip: Email, SMS link, Whatsapp, B2C account, Mobile app, Download… | Delivery channel |
| Destination | text | Destination, masked |
| Sent at | 1 Oct 2026, 14:30 | Sent At |
| Delivered at | 1 Oct 2026, 14:30 | Delivered At |
| Opened downloaded | 1 Oct 2026, 14:30 | When opened or downloaded |
| Attempt | 1,234 | Attempt |
| Status | chip: Not required, Pending, Sent, Delivered, Opened downloaded, Completed… | Delivery status |

**The selected credential delivery distribution** (detail panel): The pack groups this record's detail under its own headings: “Alternative states”, “Where allowed, support”.

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket |
| Media | text | Media |
| Recipient | text | Recipient |
| Channel | chip: Email, SMS link, Whatsapp, B2C account, Mobile app, Download… | Delivery channel |
| Destination | text | Destination, masked |
| Sent at | 1 Oct 2026, 14:30 | Sent At |
| Delivered at | 1 Oct 2026, 14:30 | Delivered At |
| Opened downloaded | 1 Oct 2026, 14:30 | When opened or downloaded |
| Attempt | 1,234 | Attempt |
| Status | chip: Not required, Pending, Sent, Delivered, Opened downloaded, Completed… | Delivery status |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| SMS Link (primary button) | navigation or local | — | — | — | — |
| WhatsApp integration (secondary button) | navigation or local | — | — | — | — |
| Download (secondary button) | navigation or local | — | — | — | — |
| Apple Wallet (secondary button) | navigation or local | — | — | — | — |
| Google Wallet (secondary button) | navigation or local | — | — | — | — |
| POS (secondary button) | navigation or local | — | — | — | — |
| API (secondary button) | navigation or local | — | — | — | — |
| Physical Collection (secondary button) | navigation or local | — | — | — | — |
| Send credential (primary button) | `deliverCredential` POST `/credentials/{credentialId}/deliveries` | CredentialDeliveryInput | CredentialDeliveryDistributionOperationsView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The credential is revoked or expired; 422 The channel does not suit the media type (a wallet pass for an RFID … | gated `ORDER_REPRINT` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Delivery list**: Title "Deliveries". Columns Virtual Ticket, Media, Recipient (role and name), Channel, Destination (masked: s***@gmail.com, +971 50 *** 4471), Sent, Delivered, Opened / downloaded, Attempt, Status. A ticket's attempts group under it, newest first. *(source: screens/P08-venue-back-office.yaml#BO-357 / contracts/spine/access.yaml#/components/schemas/CredentialDeliveryDistributionOperationsView)*
- **Status lifecycle**: The pack's chain drawn as a legend (Not required > Pending > Sent > Delivered > Opened / downloaded > Completed; alternatives Failed, Bounced, Expired, Cancelled). *(source: screens/P08-venue-back-office.yaml#BO-357)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Send credential**: Creates a new delivery attempt (Pending); the list shows it immediately; 409/422 messages against the field (invalid destination, channel not available for this medium). *(source: contracts/spine/access.yaml#deliverCredential)*
- **Bulk (Send all, Send selected, Resend pending, Resend failed, Send group, Export status)**: No operation; draw in a "Bulk" menu, disabled "Not available yet". *(source: screens/P08-venue-back-office.yaml#BO-358 / contracts/spine/access.yaml#listCredentialDeliveryDistribution)*

**Data it reads**: `listCredentialDeliveryDistribution` (onLoad, Credential Delivery & Distribution Operations)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialDeliveryDistribution`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential delivery distribution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential delivery distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential delivery distribution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential delivery distribution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission: reading needs SCOPE_VIEW; **sending a credential needs ORDER_REPRINT** (K1, 29 September), and the Send action is hidden without it. Never an empty table. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The credential is revoked or expired; 422 The channel does not suit the media type (a wallet pass for an RFID card) |

#### Edge cases to draw

- **Deferred seat assignment**: Tickets show "Not required yet - seats to be released"; the later bulk QR e-mail with final seats appears as attempts here. *(source: DI-423)*
- **Dynamic-QR event delivered by e-mail**: The e-mail carries "Open the app to activate", not a working code; the channel list says so. *(source: DI-635)*
- **User lacks ORDER_REPRINT**: Send disabled with "Needs reprint rights" (VO-R08); viewing allowed. *(source: contracts/spine/access.yaml#deliverCredential)*

#### Consistency with other screens

- Match `BO-355`: The Resend action there opens this send dialog.
- Match `BO-651`: Accreditation credential delivery (deliverAccreditationCredential) is a separate list; same status words where they overlap.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- ticket: VT-2026-009821
  media: PDF ticket
  recipient: Ticket holder - Sara Al Nuaimi
  channel: Email
  destination: s***@gmail.com
  sent: 1 Oct 09:14
  delivered: 1 Oct 09:14
  opened: 1 Oct 09:30
  attempt: 1
  status: Completed
- ticket: VT-2026-012230
  media: Apple Wallet
  recipient: Purchaser - James Carter
  channel: SMS link
  destination: +971 55 *** 2290
  attempt: 2
  status: Failed
```

#### Permissions

- `listCredentialDeliveryDistribution` → `SCOPE_VIEW` (read) · staff
- `deliverCredential` → `ORDER_REPRINT` (operate) · staff

**A refused user sees:** Names the missing permission: reading needs SCOPE_VIEW; **sending a credential needs ORDER_REPRINT** (K1, 29 September), and the Send action is hidden without it. Never an empty table.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: deferred seat assignment — sale confirmed at purchase as section + quantity; seats allocated internally; closer to the event ops/admin trigger a bulk e-mail issuing QR tickets with final seats. Immediate seat assignment remains for venues that need it. *(agreed · MoM 21 Aug 2026, 4.7 Deferred Seat Assignment Model; 5. Key Decisions · DI-423)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-357` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-357`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 6: Works in Credential Delivery & Distribution Operations → Manage how generated ticket media are delivered or made available to customers, participants and operational staff.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-357?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: SMS Link, WhatsApp integration, Download, Apple Wallet, Google Wallet, POS, API, Physical Collection, Send credential.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ORDER_REPRINT`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-358` Media Binding, Activation & Assignment Operations

**Manage credentials that require operational assignment or activation after ticket issuance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `TICKET_LOOKUP` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-binding-activation-assignment-operations-bo-358` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists media bindings pending assignment or activation.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The counter and back-office workspace for media that must be assigned after the ticket exists - RFID and NFC cards and wristbands, physical cards, face, temporary credentials: scan the guest's ticket QR, choose the medium, scan or tap its UID, see the ticket it resolves to, bind and activate (now, scheduled, on first use, on collection or temporarily). The one thing to get right: a UID already bound to another ticket is stopped before binding ("This RFID credential is already bound to VT-008882") and needs an authorised resolution.

**Known correction pending (do not draw the wrong version)**

- **Capture methods and activation modes drawn as seven action buttons (Scan, Batch assignment, Activate Now, Schedule...)** Why: They are values of captureMethod and activationMode in one bind flow. *(source: contracts/spine/access.yaml#/components/schemas/MediaBindingActivationAssignmentOperationsInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Binding needs ACCESS_POINT_CONFIGURE** Why: Counter staff who hand out wristbands should not need gate configuration rights; the same reasoning moved resend to ORDER_REPRINT and replace to ORDER_EXCHANGE. *(source: contracts/spine/access.yaml#setMediaBindingActivation / contracts/spine/access.yaml#deliverCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **setMediaBindingActivation declares only 200 and 429 responses** Why: Its description says a medium already bound to another ticket is refused, and the pack's duplicate detection ("This RFID credential is already bound to VT-008882") needs a declared 409 the screen can show. *(source: screens/P08-venue-back-office.yaml#BO-359 / contracts/spine/access.yaml#setMediaBindingActivation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The table is bound to the write setMediaBindingActivation; there is no read (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which permission should media binding at a counter need?** → Drawn default accepted: Draw it enabled for counter roles; flag ACCESS_POINT_CONFIGURE as under review. *(decided by Chinmay, 2026-10-02; DEC-272 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **virtualTicketId**: Step 1 "Scan the ticket" - scan the guest's QR or search the ticket; shows customer, product and existing media before anything is bound. *(source: screens/P08-venue-back-office.yaml#BO-358 / contracts/spine/access.yaml#/components/schemas/MediaBindingActivationAssignmentOperationsInput)*
- **mediaKind**: Step 2 choice - RFID, NFC, Wristband, Physical card, Face recognition, Temporary credential - limited to what the ticket's binding rule allows (BO-338) and greyed with the reason otherwise. *(source: contracts/spine/access.yaml#/components/schemas/MediaBindingActivationAssignmentOperationsInput / contracts/spine/access.yaml#setMediaBindingRule)*
- **credentialIdUid / captureMethod**: Step 3 "Scan wristband" - the UID fills in from the reader (Scan, Tap) or the encoder (Encoder assignment); Manual lookup only for users allowed it; Batch assignment for school and group bands. For face, the field holds the biometric provider reference, never an image. *(source: screens/P08-venue-back-office.yaml#BO-358 / contracts/spine/access.yaml#/components/schemas/MediaBindingActivationAssignmentOperationsInput)*
- **activationMode / scheduledAt**: Step 4 - Activate now (default), Schedule (date-time in venue time), On first use, On collection, Temporary (with the duration from BO-341). *(source: screens/P08-venue-back-office.yaml#BO-359 / contracts/spine/access.yaml#/components/schemas/MediaBindingActivationAssignmentOperationsInput)*

#### Outputs: what the screen shows and produces

**Shown**

**Every media binding activation** (data table, from `setMediaBindingActivation`)

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket |
| Customer | text | Customer |
| Product | text | Product |
| Existing media | text | Existing Media |
| Credential ID uid | text | Credential ID / UID |
| Provider | text | Provider |
| Activation mode | chip: Activate now, Schedule, Activate on first use, Activate on collection, Temporary … | When the bound medium becomes active |
| Validity | text | Validity |
| Binding rule | text | Binding Rule |

**Find ticket** (detail panel, from `lookupTicket`)

| Shows | Format | Notes |
|---|---|---|
| Ticket | the name it points at, never the id | Stable for the life of the ticket, independent of the media carrying it. |
| Media code | text | — |
| Product name | text | — |
| Holder name | text | Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder. |
| Is valid | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Performance | the name it points at, never the id | — |
| Entries used | 1,234 | — |
| Entries allowed | 1,234 | Null means unlimited. |
| Reentry allowed | yes / no (icon or chip) | — |
| Is inside venue | yes / no (icon or chip) | Derived from the last scan. Drives anti-passback evaluation. |
| Issuing cell | text | Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). |
| Guest link | text | Pseudonymous cross-region guest reference. Present only on delegated rights. |
| Admission rules | the name it points at, never the id | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |

**The selected media binding activation** (detail panel): The pack groups this record's detail under its own headings: “This is especially important for”, “Scan Virtual Ticket QR”, “Scan Wristband UID”, “Resolve Virtual Ticket”, “Bind”, “Activate”.

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket |
| Customer | text | Customer |
| Product | text | Product |
| Existing media | text | Existing Media |
| Credential ID uid | text | Credential ID / UID |
| Provider | text | Provider |
| Activation mode | chip: Activate now, Schedule, Activate on first use, Activate on collection, Temporary … | When the bound medium becomes active |
| Validity | text | Validity |
| Binding rule | text | Binding Rule |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Scan (primary button) | navigation or local | — | — | — | — |
| Batch assignment (secondary button) | navigation or local | — | — | — | — |
| Encoder assignment (secondary button) | navigation or local | — | — | — | — |
| Activate Now (secondary button) | navigation or local | — | — | — | — |
| Schedule (secondary button) | navigation or local | — | — | — | — |
| Activate on First Use (secondary button) | navigation or local | — | — | — | — |
| Activate on Collection (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Binding workspace**: A guided four-step panel (Scan ticket > Choose medium > Scan medium > Bind and activate) with the resolved ticket card always visible: Virtual Ticket, customer, product, existing media, binding rule that applies, validity. Ends on "Ready" with the new medium in the ticket's media list. *(source: screens/P08-venue-back-office.yaml#BO-358)*
- **Pending assignments**: List of tickets whose rule requires a physical medium not yet bound (today's arrivals first). *(source: contracts/spine/access.yaml#/components/schemas/CredentialOperationsCommandCenterView)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Bind and activate**: Binds the medium to the ticket and applies the activation mode; the medium appears in BO-355. Refused when the UID is bound to another active ticket (shows that ticket, masked holder) or when the rule's maximum is reached. *(source: screens/P08-venue-back-office.yaml#BO-359 / contracts/spine/access.yaml#setMediaBindingActivation)*

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `setMediaBindingActivation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media binding activation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media binding activation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media binding activation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the media binding activation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied |

#### Edge cases to draw

- **Reader not connected**: Step 3 shows "Reader not detected" with Retry; manual entry only with permission. *(source: designer default)*
- **Exclusive activation (RFID revokes the temporary paper ticket)**: Confirmation names the medium that will be revoked. *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#setMediaBindingRule)*
- **Wallet balance on the ticket**: The new wristband pays from the same stored value; show the balance carried by the ticket. *(source: TRACKER Actions row 232 / DI-538)*

#### Consistency with other screens

- Match `BO-179`: The on-site media swap (QR to wristband, DI-637) is the same flow; kiosks and the Staff App reuse the four steps.
- Match `BO-650`: Accreditation NFC/RFID encoding shows the same reader states (Reader connected, Card detected, Encoding, Verification, Successful, Failed).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
binding:
  ticket: VT-2026-009821
  customer: Sara Al Nuaimi
  product: Aqua Park Day Pass
  existing: Dynamic QR (active)
  medium: RFID wristband
  uid: 04:A2:5C:91:7E
  capture: Scan
  provider: HID
  activation: Activate now
  rule: Aqua Park Day Pass - RFID required, max 2
refusal: This RFID credential is already bound to VT-2026-008882 (K***** Al Zaabi).
```

#### Permissions

- `setMediaBindingActivation` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.17 | The system should have the ability to scan a ticket into a POS terminal and display record of ticket’s history: transaction time, clerk, payment method, etc. | Admission and Access | CONTRACTED | `lookupTicket` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-358` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-358`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 8: Works in Media Binding, Activation & Assignment Operations → Manage credentials that require operational assignment or activation after ticket issuance.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-358?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Scan, Batch assignment, Encoder assignment, Activate Now, Schedule, Activate on First Use, Activate on Collection.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-359` Credential Replacement, Reissue, Revocation & Recovery

**Manage operational credential changes while preserving the underlying Virtual Ticket.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_EXCHANGE`, `SCOPE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `credentialId` (navigation) |
| Route | `/access-venue/credential-replacement-reissue-revocation-recovery-bo-359` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The counter workflow for replacing, reissuing, revoking and recovering a guest's medium while the ticket stays the same: locate the ticket, pick the medium, choose the reason, verify the customer, apply the policy from BO-342, get approval if required, revoke or suspend the old medium, bind the new one, activate, confirm. The one thing to get right: before the operator confirms, the screen states exactly what will happen - old medium revoked now or after N minutes, fee, replacements left - and afterwards shows the same ticket ID with the new medium.

**Known correction pending (do not draw the wrong version)**

- **replaceCredential names only the Virtual Ticket (credentialId is the ticket), not which medium is replaced** Why: A ticket with QR, RFID and wallet needs the binding id of the medium being replaced. *(source: contracts/spine/access.yaml#replaceCredential / contracts/spine/access.yaml#bindCredentialDevice; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Policy fields (immediate revocation, grace period, maximum, identity, supervisor, reason codes) drawn as editable selects** Why: The policy is BO-342's write; here it is read-only, and the two reads name the same fields differently (immediateOldMediaRevocation vs oldMediaAutomaticallyRevoked, maximumReplacements vs numberOfReplacements). *(source: contracts/spine/access.yaml#listCredentialReplacementReissue / contracts/spine/access.yaml#listMediaReplacementRevocation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No field records identity verification, and no operation recovers a suspended credential or revokes without replacing** Why: The pack's flow (Verify customer, Recovery) and the Lost/Stolen immediate revoke need them. *(source: screens/P08-venue-back-office.yaml#BO-360 / contracts/spine/access.yaml#replaceCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Immediate old-media revocation | select field | — | — | — | — | — | — |
| Grace period | select field | — | — | — | — | — | — |
| Maximum replacements | select field | — | — | — | — | — | — |
| Identity verification | select field | — | — | — | — | — | — |
| Supervisor approval | select field | — | — | — | — | — | — |
| Reason codes | select field | — | — | — | — | — | — |

**Sent by *Replace credential*** (`replaceCredential`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Lost · Stolen · Damaged · Compromised · Customer changed phone · RFID failure · Wristband replacement · QR compromise · Wallet replacement · Face re enrollment · Incorrect assignment | — | — | `replaceCredential` body |
| New media kind `newMediaKind` | text field | optional | — | — | — | Media type of the replacement (`MediaTypeTechnologyLibraryView.mediaType`); empty keeps the current kind | `replaceCredential` body |
| New media code `newMediaCode` | text field | optional | — | — | — | Code of the new physical media where one is encoded at the counter | `replaceCredential` body |
| Approval request `approvalRequestId` | picker: choose an approval request | optional | — | — | shows names, sends the id | The granted approval, where the replacement rule requires one | `replaceCredential` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `replaceCredential` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ticket and medium**: Opened with the ticket (and medium) from BO-355 or BO-354; otherwise "Locate ticket" by ID, media code or the guest's phone or ID (DI-538). Shows the existing credential before anything else. *(source: screens/P08-venue-back-office.yaml#BO-359 / contracts/spine/access.yaml#lookupTicket / DI-538)*
- **reason**: Select of the 11 reasons (Lost, Stolen, Damaged, Compromised, Customer changed phone, RFID failure, Wristband replacement, QR compromise, Wallet replacement, Face re-enrolment, Incorrect assignment); the generated buttons for four of them are this field. *(source: screens/P08-venue-back-office.yaml#BO-359 / contracts/spine/access.yaml#replaceCredential)*
- **Identity verification**: Shown when the rule requires it - a checklist "ID checked (Emirates ID / passport)" with the last 4 digits recorded; the contract has no field to record it (see corrections). *(source: screens/P08-venue-back-office.yaml#BO-359 / contracts/spine/access.yaml#listCredentialReplacementReissue)*
- **newMediaKind / newMediaCode**: New medium kind (default = same as old); the new code is scanned at the counter for physical media, empty for generated media (QR, wallet). *(source: contracts/spine/access.yaml#replaceCredential)*
- **approvalRequestId / note**: When the rule requires approval, a "Request approval" step; Confirm stays disabled until granted. Note max 500. *(source: contracts/spine/access.yaml#replaceCredential)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Customer changed phone (primary button) | navigation or local | — | — | — | — |
| Wristband replacement (secondary button) | navigation or local | — | — | — | — |
| Wallet replacement (secondary button) | navigation or local | — | — | — | — |
| Incorrect assignment (secondary button) | navigation or local | — | — | — | — |
| Replace credential (primary button) | `replaceCredential` POST `/credentials/{credentialId}/replace` | CredentialReplacementInput | CredentialOperationsCommandCenterView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 replacement-limit, or approval-required, or the credential is revoked | step-up: mfa (Moves a paid ticket onto new media; the old one stops working.); gated `ORDER_EXCHANGE` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Policy panel**: Read-only, from the reason's rule: replacements used / allowed ("1 of 2"), fee ("AED 25.00, charged at POS"), checks required, old medium "Revoked immediately" or "Works 15 more minutes". *(source: contracts/spine/access.yaml#listCredentialReplacementReissue / contracts/spine/access.yaml#setMediaReplacementRevocation)*
- **Result card**: The pack's example - Virtual Ticket VT-009821 ACTIVE; Old RFID RF-88721 REVOKED; New RFID RF-99211 ACTIVE; QR QR-55128 ACTIVE - "The Virtual Ticket remains unchanged." *(source: screens/P08-venue-back-office.yaml#BO-360)*
- **Flow rail**: The ten pack steps as a rail with the current step highlighted. *(source: screens/P08-venue-back-office.yaml#BO-359)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Replace credential**: Confirmation with step-up authentication (ORDER_EXCHANGE). Errors in words - "Replacement limit reached (2 of 2)" (409 replacement-limit), "Approval required" (409 approval-required). *(source: contracts/spine/access.yaml#replaceCredential)*
- **Recover suspended credential**: Restores a suspended medium only where policy permits; suspension follows identity locks, so this is a release on the lock manager (BO-247). *(source: screens/P08-venue-back-office.yaml#BO-360 / contracts/spine/access.yaml#listCredentialReplacementReissue)*

**Data it reads**: `listCredentialReplacementReissue` (onLoad, Credential Replacement, Reissue, Revocation & Recovery)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialReplacementReissue`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential replacement reissue configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential replacement reissue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential replacement reissue configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission: reading needs SCOPE_VIEW; **replacing a credential needs ORDER_EXCHANGE with step-up (mfa)** (K1, 29 September), and the Replace action is hidden without it. Never an empty table. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 replacement-limit, or approval-required, or the credential is revoked |

#### Edge cases to draw

- **Lost wristband with stored value**: The balance stays on the ticket and is usable on the new wristband; show "Balance AED 140.00 carried over". *(source: DI-538 / TRACKER Actions row 232)*
- **Ticket holds several media of the same kind**: The operator must pick which one; the contract cannot say which (see corrections). *(source: contracts/spine/access.yaml#replaceCredential)*

#### Consistency with other screens

- Match `BO-342`: The policy shown here is BO-342's rule for the reason; same words.
- Match `BO-027`: Reissue & Media Replacement (orders board) reads the same policy; one of the two is the counter screen (VO-R14).
- Match `POS-027`: The POS media replacement step should use this flow (cross-process, POS).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
replacement:
  ticket: VT-2026-009821
  holder: Sara Al Nuaimi
  old: RF-88721 RFID wristband
  reason: Lost
  verified: Emirates ID ending 4471
  used: 1 of 2
  fee: AED 25.00
  oldMedium: Revoked immediately
  new: RF-99211
  balance: AED 140.00 carried over
```

#### Permissions

- `listCredentialReplacementReissue` → `SCOPE_VIEW` (read) · staff
- `replaceCredential` → `ORDER_EXCHANGE` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission: reading needs SCOPE_VIEW; **replacing a credential needs ORDER_EXCHANGE with step-up (mfa)** (K1, 29 September), and the Replace action is hidden without it. Never an empty table.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Lost wristband/card: operations identify the guest (phone number or ID), locate the original transaction and transfer the balance to a replacement wristband/card. *(client request · MoM 27 Aug 2026, 4.10 Lost-media recovery · DI-538)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-359` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-359`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 10: Works in Credential Replacement, Reissue, Revocation & Recovery → Manage operational credential changes while preserving the underlying Virtual Ticket.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-359?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Customer changed phone, Wristband replacement, Wallet replacement, Incorrect assignment, Replace credential.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ORDER_EXCHANGE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-360` Failed Generation, Delivery & Credential Exception Management

**Provide one dedicated operational queue for credential-related failures.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `exceptionId` (navigation) |
| Route | `/access-venue/failed-generation-delivery-credential-exception-manageme-bo-360` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** One queue for every credential failure - generation, binding, activation, delivery, wallet, RFID encoding, duplicate credential, invalid token, provider, synchronisation, missing template or data, expired, mapping, unknown credential - prioritised by how soon it hurts a guest at the gate, with the fix actions. The one thing to get right: severity order (event proximity, arrival time, tickets affected, no alternative media, VIP, access impact, provider outage) and every action leaves a visible trail on the exception.

**Known correction pending (do not draw the wrong version)**

- **The queue has no exception status (Open, In progress, Escalated, Resolved)** Why: The view has lastAction and retryStatus only; the queue cannot separate open from resolved work. *(source: contracts/spine/access.yaml#/components/schemas/FailedGenerationDeliveryCredentialExceptionManagemenView / contracts/spine/access.yaml#resolveCredentialException; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's Resend, Rebind and Switch media are not actions of the exception operation** Why: Draw them as links to BO-357 and BO-358; Switch media is Use fallback. *(source: screens/P08-venue-back-office.yaml#BO-360 / contracts/spine/access.yaml#resolveCredentialException; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The list operation's note says every fix has no operation** Why: resolveCredentialException covers six of them; the note is stale. *(source: contracts/spine/access.yaml#listFailedGenerationDelivery; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Severity | text field | — | — | `listFailedGenerationDelivery` ?severity |
| Failure type | text field | — | — | `listFailedGenerationDelivery` ?failureType |

**Sent by *Retry*** (`resolveCredentialException`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Retry · Regenerate · Use fallback · Escalate · Assign owner · Open technical case | — | — | `resolveCredentialException` body |
| Owner `ownerId` | text field | optional | — | — | — | Required for assignOwner and escalate | `resolveCredentialException` body |
| Fallback media kind `fallbackMediaKind` | radio group | optional | — | QR · Pdf · Printed ticket · RFID card · Wristband | — | Required for useFallback | `resolveCredentialException` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `resolveCredentialException` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters (severity, failureType)**: Severity chips Critical / High / Medium / Low; failure type grouped (Generation, Delivery, Binding and activation, Provider and sync, Data and template); plus Owner = me. *(source: contracts/spine/access.yaml#listFailedGenerationDelivery / contracts/spine/access.yaml#/components/schemas/FailedGenerationDeliveryCredentialExceptionManagemenView)*
- **Action inputs (ownerId, fallbackMediaKind, note)**: Owner picker (required for Assign owner and Escalate), fallback medium QR / PDF / Printed ticket / RFID card / Wristband (required for Use fallback), note max 500. *(source: contracts/spine/access.yaml#resolveCredentialException)*

#### Outputs: what the screen shows and produces

**Shown**

**Every failed generation delivery** (data table, from `listFailedGenerationDelivery`)

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Low, Medium, High, Critical | Severity, weighted by event proximity, arrival time, affected tickets, fallback availability, VIP and access impact |
| Virtual ticket | text | Virtual Ticket |
| Credential | text | Credential |
| Media | text | Media |
| Customer | text | Customer |
| Event | text | Event |
| Failure | text | Failure |
| Time | 1 Oct 2026, 14:30 | Time |
| Operational impact | text | Operational Impact |
| Retry status | text | not in the schema: `Retry Status` |
| Owner | text | Owner |

**The selected failed generation delivery** (detail panel): The pack groups this record's detail under its own headings: “Include”, “Consider”.

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Low, Medium, High, Critical | Severity, weighted by event proximity, arrival time, affected tickets, fallback availability, VIP and access impact |
| Virtual ticket | text | Virtual Ticket |
| Credential | text | Credential |
| Media | text | Media |
| Customer | text | Customer |
| Event | text | Event |
| Failure | text | Failure |
| Time | 1 Oct 2026, 14:30 | Time |
| Operational impact | text | Operational Impact |
| Retry status | text | not in the schema: `Retry Status` |
| Owner | text | Owner |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Retry (primary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Regenerate (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Use Fallback (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Escalate (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Assign Owner (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Open Technical Case (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Exception queue**: Title "Credential exceptions". Columns Severity (coloured), Virtual Ticket, Credential, Media, Customer, Event (with "in 3 h" proximity), Failure (words), Since, Operational impact ("No alternative media - guest arrives 10:00"), Retry status, Owner, Last action. Sorted by severity then event time; cursor paging. *(source: screens/P08-venue-back-office.yaml#BO-360 / contracts/spine/access.yaml#/components/schemas/FailedGenerationDeliveryCredentialExceptionManagemenView)*
- **AI root cause**: Advisory correlation ("91% of today's RFID encoding failures originate from Encoder Group 3 after firmware update 6.2") with Show affected. *(source: screens/P08-venue-back-office.yaml#BO-361)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Retry / Regenerate / Use fallback / Escalate / Assign owner / Open technical case**: One action per call, recorded on the exception with the actor; the row moves to In progress or Escalated and resolves when the job sees the step succeed. A resolved exception refuses further action (409) - show it read-only. *(source: contracts/spine/access.yaml#resolveCredentialException)*
- **Resend / Rebind**: Resend opens the BO-357 send dialog; Rebind opens BO-358 with the ticket. Switch media is Use fallback. *(source: contracts/spine/access.yaml#deliverCredential / contracts/spine/access.yaml#setMediaBindingActivation)*

**Data it reads**: `listFailedGenerationDelivery` (onLoad, Failed Generation, Delivery & Credential Exception …)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listFailedGenerationDelivery`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The failed generation delivery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the failed generation delivery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No failed generation delivery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the failed generation delivery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind missing for useFallback |

#### Edge cases to draw

- **Provider outage affecting hundreds of tickets**: Grouped row "Apple Wallet - 212 tickets" with bulk Use fallback (QR) per ticket; bulk has no operation today. *(source: screens/P08-venue-back-office.yaml#BO-360 / contracts/spine/access.yaml#resolveCredentialException)*
- **Exception resolved by automatic retry while open on screen**: Row updates to Resolved with "Resolved by automatic retry". *(source: contracts/spine/access.yaml#setCredentialIssuanceRetryPolicy)*

#### Consistency with other screens

- Match `BO-356`: Same failure words and the same actions.
- Match `BO-354`: The hub's problem tiles open this queue filtered.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- severity: Critical
  ticket: VT-2026-012230
  media: Apple Wallet
  customer: James Carter
  event: Today 19:30 (in 3 h)
  failure: Wallet failure
  impact: No alternative media
  retry: 3 of 3 failed
  owner: Maria Santos
- severity: High
  ticket: VT-2026-012231
  media: RFID wristband
  failure: RFID encoding failure
  impact: Group of 40 arriving 10:00
  owner: Rahul Menon
```

#### Permissions

- `listFailedGenerationDelivery` → `SCOPE_VIEW` (read) · staff
- `resolveCredentialException` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-360` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-360`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 12: Works in Failed Generation, Delivery & Credential Exception Management → Provide one dedicated operational queue for credential-related failures.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-360?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Retry, Regenerate, Use Fallback, Escalate, Assign Owner, Open Technical Case.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-361` Credential Usage & Cross-Media Traceability

**Provide end-to-end visibility into how the different media attached to one Virtual Ticket have been presented or used. This screen is for credential traceability, while Area 16 remains responsible for the actual access-control decision.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `TICKET_LOOKUP` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-usage-cross-media-traceability-bo-361` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The usage trace of one Virtual Ticket across its media - which medium was presented, when, where, on which device or external system, what it resolved to, what access decided and what happened to the master entitlement. It records and displays credential events; Access Control decides admission. The one thing to get right: a timeline per ticket, read-only, answering "which medium, when, where, which ticket, what happened to the entitlement".

**Known correction pending (do not draw the wrong version)**

- **Drawn as a configuration form of eleven selectFields (Virtual Ticket, Credential, Presentation timestamp, Result...)** Why: These are the columns of a read-only trace; nothing is configured here. *(source: contracts/spine/access.yaml#/components/schemas/CredentialUsageCrossMediaTraceabilityView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"What happened to the master entitlement?" drawn as a primary button** Why: A pack question that the entitlement-impact column answers. *(source: screens/P08-venue-back-office.yaml#BO-362; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Result and transaction type are free strings** Why: The access result must use the DenyReason / ScanOutcome vocabulary so it reads the same as the scanner (VO-R06). *(source: contracts/spine/access.yaml#/components/schemas/CredentialUsageCrossMediaTraceabilityView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Virtual Ticket | select field | — | — | — | — | — | — |
| Credential | select field | — | — | — | — | — | — |
| Media | select field | — | — | — | — | — | — |
| Presentation timestamp | select field | — | — | — | — | — | — |
| Location | select field | — | — | — | — | — | — |
| Device | select field | — | — | — | — | — | — |
| External system | select field | — | — | — | — | — | — |
| Transaction type | select field | — | — | — | — | — | — |
| Result | select field | — | — | — | — | — | — |
| Entitlement impact | select field | — | — | — | — | — | — |
| Synchronization status | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Virtual ticket | text field | — | — | `listCredentialUsageCross` ?virtualTicket |
| Media | text field | — | — | `listCredentialUsageCross` ?media |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Virtual Ticket / media**: Opens with a ticket id (from BO-355 or BO-354) or asks for one (ticket id or media code); media filter chips narrow the timeline. *(source: contracts/spine/access.yaml#listCredentialUsageCross / contracts/spine/access.yaml#lookupTicket)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What happened to the master entitlement? (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Usage timeline**: The pack's example as the layout - 09:02 Apple Wallet added; 14:15 RFID bound; 17:51 Mobile QR presented at Kiosk; 18:03 Face presented at Gate 2; 18:03 Access result Allowed; 18:04 Virtual Ticket usage updated; 18:22 RFID presented at VIP Lounge. Each line shows medium icon, location, device, transaction type, result in VO-R06 words, entitlement impact ("1 entry used, 0 left") and sync status (Synced / Was offline, synced 18:40). *(source: screens/P08-venue-back-office.yaml#BO-361 / contracts/spine/access.yaml#/components/schemas/CredentialUsageCrossMediaTraceabilityView)*
- **Boundary note**: "Area 15 records the credential event (RFID RF-10028 > VT-009821); Access Control decides admission (VT-009821, Gate 4, Allow)." as a small caption. *(source: screens/P08-venue-back-office.yaml#BO-362)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open scan in Scan Activity**: An access result line opens the scan record in BO-034 (the admission decision of record). *(source: contracts/spine/access.yaml#lookupTicket / designer default)*

**Data it reads**: `listCredentialUsageCross` (onLoad, Credential Usage & Cross-Media Traceability)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialUsageCross`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential usage cross-media configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential usage cross-media untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential usage cross-media configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Offline scans synced later**: Lines show the original time with "recorded offline, synced 18:40" (both times). *(source: DI-065)*
- **Used without passing (stroller)**: The access line says Allowed and used; no un-use action - resolution is from the scan history. *(source: DI-627)*

#### Consistency with other screens

- Match `BO-355`: Same timeline component and wording.
- Match `SCN-009`: The scanner's ticket lookup history uses the same deny reasons.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
trace:
- 09:02 - Apple Wallet added
- 14:15 - RFID RF-10452 bound at Main Plaza desk
- 17:51 - Mobile QR presented at Kiosk K2
- 18:03 - Face presented at Main Plaza Gate 2 - Allowed - 1 entry used
- 18:22 - RFID presented at VIP Lounge - Allowed
```

#### Permissions

- `listCredentialUsageCross` → `TICKET_LOOKUP` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-361` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-361`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 14: Works in Credential Usage & Cross-Media Traceability → Provide end-to-end visibility into how the different media attached to one Virtual Ticket have been presented or used. This screen is for credential traceability, while Area 16 remains responsible …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-361?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What happened to the master entitlement?.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-362` Credential Security, Audit & Operational Evidence

**Maintain complete evidence of credential creation and lifecycle activity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-security-audit-operational-evidence-bo-362` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The evidence store for credential lifecycle actions - requested, generated, bound, delivered, activated, updated, presented, suspended, reactivated, replaced, revoked, expired, rebound, regenerated, deleted - each with before/after, actor, source, device, time, reason, approval, provider reference and related transaction, plus security monitoring flags and evidence export for disputes, investigations and audits. The one thing to get right: the credential chain (RFID-1001 Lost > Revoked > RFID-1057 Active) must be reconstructable at a glance, and access to it follows role, tenant, venue and data sensitivity.

**Known correction pending (do not draw the wrong version)**

- **Table bound to one column (anomalyFlags)** Why: The read returns the full record; the pack's audit record fields are the columns. *(source: contracts/spine/access.yaml#/components/schemas/CredentialSecurityAuditOperationalEvidenceView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Evidence export has no operation** Why: The pack requires it for disputes and fraud investigations. *(source: screens/P08-venue-back-office.yaml#BO-362 / contracts/spine/access.yaml#listCredentialSecurityOperational; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Virtual ticket | text field | — | — | `listCredentialSecurityOperational` ?virtualTicket |
| Action | text field | — | — | `listCredentialSecurityOperational` ?action |
| Actor | text field | — | — | `listCredentialSecurityOperational` ?actor |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters (virtualTicket, action, actor)**: Ticket id or media code, action chips (the 15 actions), actor picker, date range; plus "Flagged only". *(source: contracts/spine/access.yaml#listCredentialSecurityOperational)*
- **Evidence export**: Purpose required (Customer dispute, Operational investigation, Fraud investigation, Audit, Compliance) and a reference; the export carries the chosen ticket's full chain. *(source: screens/P08-venue-back-office.yaml#BO-362)*

#### Outputs: what the screen shows and produces

**Shown**

**Every credential security audit** (data table, from `listCredentialSecurityOperational`)

| Shows | Format | Notes |
|---|---|---|
| Anomaly flags | list or chips (count when long) | Suspicious patterns flagged on this entry |

**The selected credential security audit** (detail panel): The pack groups this record's detail under its own headings: “Record”, “RFID-1001”, “Access Control”, “Evidence Export”.

| Shows | Format | Notes |
|---|---|---|
| Anomaly flags | list or chips (count when long) | Suspicious patterns flagged on this entry |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Audit list**: Title "Credential evidence". Columns When, Virtual Ticket, Credential (masked), Media, Action, Actor (name), Source, Device, Reason, Approval, Flags. Before/after as a diff on selection. Cursor paging, newest first. *(source: contracts/spine/access.yaml#/components/schemas/CredentialSecurityAuditOperationalEvidenceView)*
- **Credential chain**: For a selected ticket, a vertical chain per medium lineage (RFID-1001 > Lost > Revoked > Replacement > RFID-1057 Active). *(source: screens/P08-venue-back-office.yaml#BO-362)*
- **Security monitoring**: Flag badges - Excessive regeneration, Repeated replacement, Suspicious rebinding, Multiple credential assignments, Unexpected provider/token changes, Unauthorised administrative actions - with counts at the top. *(source: screens/P08-venue-back-office.yaml#BO-362 / contracts/spine/access.yaml#/components/schemas/CredentialSecurityAuditOperationalEvidenceView)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Export evidence**: No operation; draw disabled "Not available yet". When added, the export itself is logged. *(source: contracts/spine/access.yaml#listCredentialSecurityOperational)*

**Data it reads**: `listCredentialSecurityOperational` (onLoad, Credential Security, Audit & Operational Evidence)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialSecurityOperational`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential security audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential security audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential security audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential security audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **User without AUDIT_VIEW**: "Needs audit rights" empty state, never an empty table (VO-R08). *(source: contracts/spine/access.yaml#listCredentialSecurityOperational)*
- **Deleted credential (where legally permitted)**: The row stays with "Deleted - personal data removed"; the chain keeps the gap visible. *(source: screens/P08-venue-back-office.yaml#BO-362)*

#### Consistency with other screens

- Match `BO-173`: Credential Security Simulation, Audit & Publication (access board) binds the same read; one evidence view (VO-R14).
- Match `BO-247`: A suspicious-rebinding flag offers "Lock" into the lock manager.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
chain: 'VT-2026-009821: RFID-1001 issued 3 Sep > Lost 28 Sep (Rahul Menon, counter) > Revoked 28 Sep > RFID-1057
  bound 28 Sep > Active'
rows:
- when: 28 Sep 2026 16:12
  ticket: VT-2026-009821
  credential: RF-****1001
  action: Revoked
  actor: Rahul Menon
  source: POS Main Plaza
  reason: Lost
  approval: Not required
- when: 28 Sep 2026 16:13
  ticket: VT-2026-009821
  credential: RF-****1057
  action: Bound
  actor: Rahul Menon
  flags: Repeated replacement (3 in 30 days)
```

#### Permissions

- `listCredentialSecurityOperational` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-362` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-362`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 16: Works in Credential Security, Audit & Operational Evidence → Maintain complete evidence of credential creation and lifecycle activity.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-362?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `AUDIT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-363` Ticket Media Analytics & AI Operations Intelligence

**Provide management and operations with analytics and AI intelligence across Virtual Tickets and credential media. This should be a serious operational intelligence layer—not simply a chatbot.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze; Compare) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/ticket-media-analytics-ai-operations-intelligence-bo-363` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Analytics and AI intelligence over credentials: generation, delivery and activation success, adoption of wallet, RFID, face and multiple media, replacement and revocation rates, generation and resolution times, provider reliability, predictions (failure risk, media demand, wristband stock, on-site replacement volumes), natural-language questions and recommendations. The one thing to get right: it is a dashboard, not a table - and AI explains and recommends but never creates entitlement, marks tickets used, rebinds credentials or overrides access.

**Known correction pending (do not draw the wrong version)**

- **KPIs drawn as 21 columns of a data table with a detail panel** Why: The read returns one object; draw tiles and charts (VO-R02). *(source: contracts/spine/access.yaml#listTicketMedia; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Adoption per medium is only partly returned (wallet, RFID, face, multi-media) and mediaUsageDistribution is a list of strings** Why: The pack's adoption chart needs a number per medium (Mobile QR, Apple Wallet, Google Wallet separately). *(source: screens/P08-venue-back-office.yaml#BO-363 / contracts/spine/access.yaml#/components/schemas/TicketMediaAnalyticsAiOperationsIntelligenceView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation has no transition back to BO-354, and the purpose note carries "Board 3 — Final Screen Register"** Why: Board screens return to the hub (VO-R13); the note is pack text leaked into the definition. *(source: screens/P08-venue-back-office.yaml#BO-363; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search ticket media analytics | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by brand, venue, event, product, channel, media and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | text field | — | — | `listTicketMedia` ?brand |
| Venue | text field | — | — | `listTicketMedia` ?venue |
| Event | text field | — | — | `listTicketMedia` ?event |
| Product | text field | — | — | `listTicketMedia` ?product |
| Channel | text field | — | — | `listTicketMedia` ?channel |
| Media | text field | — | — | `listTicketMedia` ?media |
| Provider | text field | — | — | `listTicketMedia` ?provider |
| Device | text field | — | — | `listTicketMedia` ?device |
| Customer segment | text field | — | — | `listTicketMedia` ?customerSegment |
| Time period | text field | — | — | `listTicketMedia` ?timePeriod |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Analyse by**: Brand, Venue, Event, Product, Channel, Media, Provider, Device, Customer segment, Time period (default last 30 days). *(source: screens/P08-venue-back-office.yaml#BO-363 / contracts/spine/access.yaml#listTicketMedia)*
- **Ask a question**: A question box with the pack's examples as chips ("Which credential type had the most failures yesterday?"); no operation, so greyed "Not available yet". *(source: screens/P08-venue-back-office.yaml#BO-363 / contracts/spine/access.yaml#listTicketMedia)*

#### Outputs: what the screen shows and produces

**Shown**

**Every ticket media analytics** (data table, from `listTicketMedia`)

| Shows | Format | Notes |
|---|---|---|
| Credentials generated | 1,234 | Credentials Generated |
| Generation success | 1,234.5 | Generation Success % |
| Delivery success | 1,234.5 | Delivery Success % |
| Activation | 1,234.5 | Activation % |
| Wallet adoption | 1,234.5 | Percent |
| RFID adoption | 1,234.5 | Percent |
| Face credential adoption | 1,234.5 | Percent |
| Multi media adoption | 1,234.5 | Percent |
| Replacement rate | 12.5% | Replacement Rate |
| Revocation rate | 12.5% | Revocation Rate |
| Generation failure | 1,234.5 | Generation Failure % |
| Delivery failure | 1,234.5 | Delivery Failure % |
| Average generation time | 1,234.5 | Seconds |
| Average resolution time | 1,234.5 | Seconds |
| Media usage distribution | list or chips (count when long) | Share of eligible customers per media type; may exceed 100% in total |
| Provider uptime | 1,234.5 | Percent |
| Generation failures | 1,234 | Generation failures |
| Encoding failures | 1,234 | Encoding failures |
| Delivery failures | 1,234 | Delivery failures |
| Synchronization delay | 1,234.5 | Seconds |
| Replacement frequency | 1,234.5 | Replacement frequency |

**The selected ticket media analytics** (detail panel): The pack groups this record's detail under its own headings: “Eligible customers”, “Backend Screen”, “Credential Operations Command Center”, “Operational exceptions”, “ONE VIRTUAL TICKET”.

| Shows | Format | Notes |
|---|---|---|
| Credentials generated | 1,234 | Credentials Generated |
| Generation success | 1,234.5 | Generation Success % |
| Delivery success | 1,234.5 | Delivery Success % |
| Activation | 1,234.5 | Activation % |
| Wallet adoption | 1,234.5 | Percent |
| RFID adoption | 1,234.5 | Percent |
| Face credential adoption | 1,234.5 | Percent |
| Multi media adoption | 1,234.5 | Percent |
| Replacement rate | 12.5% | Replacement Rate |
| Revocation rate | 12.5% | Revocation Rate |
| Generation failure | 1,234.5 | Generation Failure % |
| Delivery failure | 1,234.5 | Delivery Failure % |
| Average generation time | 1,234.5 | Seconds |
| Average resolution time | 1,234.5 | Seconds |
| Media usage distribution | list or chips (count when long) | Share of eligible customers per media type; may exceed 100% in total |
| Provider uptime | 1,234.5 | Percent |
| Generation failures | 1,234 | Generation failures |
| Encoding failures | 1,234 | Encoding failures |
| Delivery failures | 1,234 | Delivery failures |
| Synchronization delay | 1,234.5 | Seconds |
| Replacement frequency | 1,234.5 | Replacement frequency |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Fourteen metric tiles (Credentials generated, Generation success %, Delivery success %, Activation %, Wallet / RFID / Face / Multi-media adoption, Replacement rate, Revocation rate, Generation failure %, Delivery failure %, Average generation time, Average resolution time) with deltas (VO-R02). *(source: contracts/spine/access.yaml#/components/schemas/TicketMediaAnalyticsAiOperationsIntelligenceView)*
- **Media adoption chart**: Horizontal bars per medium of eligible customers (Mobile QR 78%, Apple Wallet 31%, Google Wallet 22%, RFID 18%, Face 12%) with the pack's note "one ticket may have several media, so percentages do not total 100%". *(source: screens/P08-venue-back-office.yaml#BO-363)*
- **Reliability comparison**: Per provider - uptime, generation failures, encoding failures, delivery failures, sync delay, replacement frequency. *(source: screens/P08-venue-back-office.yaml#BO-363 / contracts/spine/access.yaml#/components/schemas/TicketMediaAnalyticsAiOperationsIntelligenceView)*
- **Predictions and recommendations**: Prediction cards (credential failure risk, delivery failure probability, media demand for upcoming events, wristband stock requirement, operational workload, likely on-site replacements) and recommendation cards ("Pre-generate QR credentials for 4,200 attendees"; "Investigate RFID Encoder Group 3"; "Send wallet-add reminders for tomorrow's event") each with its reason and a person's Apply (VO-R11). A fixed "AI may / AI must not" panel from the pack. *(source: screens/P08-venue-back-office.yaml#BO-363)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Apply recommendation**: Opens the screen that does it (BO-356 for pre-generation, BO-360 for an encoder group, the notification tool for reminders); nothing runs from here. *(source: screens/P08-venue-back-office.yaml#BO-363)*

**Data it reads**: `listTicketMedia` (onLoad, Ticket Media Analytics & AI Operations Intelligence)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket media analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket media analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket media analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ticket media analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Not enough history for predictions**: Prediction cards say "Not enough data yet (needs 30 days)"; never a zero. *(source: screens/P08-venue-back-office.yaml#BO-363)*
- **User without REPORT_VIEW_VENUE**: "Needs reporting rights" (VO-R08). *(source: contracts/spine/access.yaml#listTicketMedia)*

#### Consistency with other screens

- Match `BO-354`: Same KPI definitions as the operational hub where they overlap.
- Match `ANL-003`: Operational Performance in Venue Analytics should show the same credential KPIs from the same definitions; reporting is one permission-based module (cross-process, analytics).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  generated: 31260
  generationSuccess: 99.71%
  deliverySuccess: 98.2%
  activation: 91.4%
  walletAdoption: 34%
  rfidAdoption: 18%
  faceAdoption: 12%
  multiMedia: 33%
  replacementRate: 0.9%
  averageGenerationTime: 1.8 s
insight: RFID wristbands issued by Encoder Group B have a 3.8x higher replacement rate than other encoder groups.
```

#### Permissions

- `listTicketMedia` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-363` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-363`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 18: Works in Ticket Media Analytics & AI Operations Intelligence → Provide management and operations with analytics and AI intelligence across Virtual Tickets and credential media. This should be a serious operational intelligence layer—not simply a chatbot.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-363?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
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

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"deliverCredential": {"method":"POST","path":"/credentials/{credentialId}/deliveries","contract":"access","summary":"Send a credential over a channel","permission":"ORDER_REPRINT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialDeliveryInput","responds":"CredentialDeliveryDistributionOperationsView"},
"getCredentialIssuanceRetryPolicy": {"method":"GET","path":"/credential-issuance-retry-policy","contract":"access","summary":"Read the credential issuance retry policy","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CredentialIssuanceRetryPolicyView"},
"getEntitlement": {"method":"GET","path":"/entitlements/{entitlementId}","contract":"access","summary":"One entitlement, with what remains on it","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Entitlement"},
"getEntitlementCredential": {"method":"GET","path":"/entitlements/{entitlementId}/credential","contract":"access","summary":"The thing that gets scanned","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"rotate","in":"query","required":null}],"requestBody":null,"responds":null},
"getEntitlementHistory": {"method":"GET","path":"/entitlements/{entitlementId}/history","contract":"access","summary":"Every scan, freeze, share and reissue against it","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"listCredential": {"method":"GET","path":"/credential","contract":"access","summary":"Credential Operations Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"media","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customer","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"provider","in":"query","required":false},{"name":"exception","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialDeliveryDistribution": {"method":"GET","path":"/credential-delivery-distribution","contract":"access","summary":"Credential Delivery & Distribution Operations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialGenerationIssuance": {"method":"GET","path":"/credential-generation-issuance","contract":"access","summary":"Credential Generation & Issuance Monitor","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":false},{"name":"trigger","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialReplacementReissue": {"method":"GET","path":"/credential-replacement-reissue","contract":"access","summary":"Credential Replacement, Reissue, Revocation & Recovery","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialReplacementReissueRevocationRecoveryView"},
"listCredentialSecurityOperational": {"method":"GET","path":"/credential-security-operational","contract":"access","summary":"Credential Security, Audit & Operational Evidence","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"virtualTicket","in":"query","required":false},{"name":"action","in":"query","required":false},{"name":"actor","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialUsageCross": {"method":"GET","path":"/credential-usage-cross","contract":"access","summary":"Credential Usage & Cross-Media Traceability","permission":"TICKET_LOOKUP","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"virtualTicket","in":"query","required":false},{"name":"media","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFailedGenerationDelivery": {"method":"GET","path":"/failed-generation-delivery","contract":"access","summary":"Failed Generation, Delivery & Credential Exception Management","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":false},{"name":"failureType","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTicketMedia": {"method":"GET","path":"/ticket-media","contract":"access","summary":"Ticket Media Analytics & AI Operations Intelligence","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"media","in":"query","required":false},{"name":"provider","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"timePeriod","in":"query","required":false}],"requestBody":null,"responds":"TicketMediaAnalyticsAiOperationsIntelligenceView"},
"lookupTicket": {"method":"GET","path":"/access/lookup","contract":"access","summary":"Read-only validity check without admitting","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaCode","in":"query","required":null},{"name":"ticketId","in":"query","required":null}],"requestBody":null,"responds":"TicketStatus"},
"replaceCredential": {"method":"POST","path":"/credentials/{credentialId}/replace","contract":"access","summary":"Replace a credential's media","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialReplacementInput","responds":"CredentialOperationsCommandCenterView"},
"resolveCredentialException": {"method":"POST","path":"/credential-exceptions/{exceptionId}/resolve","contract":"access","summary":"Act on a credential exception","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialExceptionActionInput","responds":"FailedGenerationDeliveryCredentialExceptionManagemenView"},
"retryCredentialGeneration": {"method":"POST","path":"/credential-generation-issuance/retry","contract":"access","summary":"Retry failed credential generation","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialGenerationRetryInput","responds":"CredentialGenerationRetryResult"},
"setCredentialIssuanceRetryPolicy": {"method":"PUT","path":"/credential-issuance-retry-policy","contract":"access","summary":"Set the credential issuance retry policy","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialIssuanceRetryPolicyInput","responds":"CredentialIssuanceRetryPolicyView"},
"setMediaBindingActivation": {"method":"PUT","path":"/media-binding-activation","contract":"access","summary":"Media Binding, Activation & Assignment Operations","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaBindingActivationAssignmentOperationsInput","responds":"MediaBindingActivationAssignmentOperationsView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CredentialDeliveryDistributionOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Delivery & Distribution Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicket":{"type":"string","description":"Virtual Ticket"},"media":{"type":"string","description":"Media"},"recipient":{"type":"string","description":"Recipient"},"channel":{"type":"string","enum":["email","smsLink","whatsapp","b2cAccount","mobileApp","download","appleWallet","googleWallet","pos","boxOffice","kiosk","groupPortal","api","physicalCollection"],"description":"Delivery channel"},"destination":{"type":"string","description":"Destination, masked"},"sentAt":{"type":"string","format":"date-time","description":"Sent At"},"deliveredAt":{"type":"string","format":"date-time","description":"Delivered At"},"openedDownloaded":{"type":"string","format":"date-time","description":"When opened or downloaded"},"attempt":{"type":"integer","description":"Attempt"},"status":{"type":"string","enum":["notRequired","pending","sent","delivered","openedDownloaded","completed","failed","bounced","expired","cancelled"],"description":"Delivery status"},"recipientRole":{"type":"string","enum":["purchaser","ticketHolder","participant","guardian","groupLeader","authorizedRecipient"],"description":"Who the credential was delivered to"}}},
"CredentialDeliveryInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Send, or send again, one credential over one channel (decided 29 September, VM close-out).","required":["id","channel"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated delivery attempt id"},"channel":{"type":"string","enum":["email","smsLink","whatsapp","download","appleWallet","googleWallet","pos","api","physicalCollection"]},"recipient":{"type":"string","maxLength":320,"description":"Email address, phone number or collection point; empty sends to the recipient already on the credential"},"recipientRole":{"type":"string","enum":["purchaser","ticketHolder","participant","guardian","groupLeader","authorizedRecipient"],"default":"ticketHolder"},"note":{"type":"string","maxLength":300}}},
"CredentialExceptionActionInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"One action on a credential exception in the failure queue (decided 29 September, VM close-out).","required":["action"],"properties":{"action":{"type":"string","enum":["retry","regenerate","useFallback","escalate","assignOwner","openTechnicalCase"]},"ownerId":{"type":"string","description":"Required for assignOwner and escalate"},"fallbackMediaKind":{"type":"string","enum":["qr","pdf","printedTicket","rfidCard","wristband"],"description":"Required for useFallback"},"note":{"type":"string","maxLength":500}}},
"CredentialGenerationIssuanceMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Generation & Issuance Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"trigger":{"type":"string","enum":["orderConfirmation","ticketIssuance","membershipActivation","customerRequest","staffAction","rfidCollection","walletRequest","faceEnrollment","api","bulkOperation","scheduledProcess"],"description":"What triggered generation"},"requestId":{"type":"string","description":"Request ID"},"virtualTicket":{"type":"string","description":"Virtual Ticket"},"media":{"type":"string","description":"Media"},"template":{"type":"string","description":"Template"},"templateVersion":{"type":"string","description":"Template Version"},"product":{"type":"string","description":"Product"},"customer":{"type":"string","description":"Customer"},"provider":{"type":"string","description":"Provider"},"requestedAt":{"type":"string","format":"date-time","description":"Requested At"},"generatedAt":{"type":"string","format":"date-time","description":"Generated At"},"status":{"type":"string","enum":["requested","queued","templateResolved","dataMapped","credentialGenerated","bound","ready","delivered","failed"],"description":"Generation stage"},"error":{"type":"string","description":"Error"},"brand":{"type":"string","description":"Brand"},"venue":{"type":"string","description":"Venue"},"event":{"type":"string","description":"Event"},"channel":{"type":"string","description":"Channel"},"language":{"type":"string","description":"Language"},"customerContext":{"type":"string","description":"Customer context"},"failureReason":{"type":"string","enum":["templateMissing","requiredDataMissing","providerUnavailable","invalidPayload","tokenGenerationFailure","walletGenerationFailure","encoderUnavailable"],"description":"Failure category when status is failed"}}},
"CredentialGenerationRetryInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Retry failed credential generation, for selected requests or every eligible one (decided 29 September, VM close-out).","required":["scope"],"properties":{"scope":{"type":"string","enum":["selected","allEligible"]},"requestIds":{"type":"array","items":{"type":"string"},"maxItems":500,"description":"The failed generation requests (`CredentialGenerationIssuanceMonitorView.requestId`); required for selected"}}},
"CredentialGenerationRetryResult": {"type":"object","x-ticvai-persistence":"none — computed (decided 29 September, VM close-out)","description":"What a retry queued and what it skipped (decided 29 September, VM close-out).","required":["queued","skipped"],"properties":{"queued":{"type":"integer"},"skipped":{"type":"array","items":{"type":"object","properties":{"requestId":{"type":"string"},"reason":{"type":"string","enum":["notFailed","alreadyQueued","notRetryable"]}}}}}},
"CredentialIssuanceRetryPolicyInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"The tenant's automatic retry policy for failed credential generation (decided 29 September, VM close-out). Proposed defaults are ours (our build plan).","required":["automaticRetry"],"properties":{"automaticRetry":{"type":"boolean","default":true},"maxAttempts":{"type":"integer","minimum":1,"maximum":10,"default":3},"backoffMinutes":{"type":"integer","minimum":1,"maximum":240,"default":5,"description":"Wait before the first retry; doubles on each attempt"},"escalateAfterAttempts":{"type":"integer","minimum":1,"maximum":10,"default":3,"description":"After this many failures the request becomes a credential exception with an owner; not more than maxAttempts"}}},
"CredentialIssuanceRetryPolicyView": {"type":"object","x-ticvai-persistence":"access.credential_issuance_retry_policy","description":"The automatic retry policy in force, one per venue (decided 29 September, VM close-out).","required":["venueId","automaticRetry","maxAttempts","backoffMinutes","escalateAfterAttempts"],"properties":{"venueId":{"type":"string"},"automaticRetry":{"type":"boolean","default":true},"maxAttempts":{"type":"integer","minimum":1,"maximum":10,"default":3},"backoffMinutes":{"type":"integer","minimum":1,"maximum":240,"default":5},"escalateAfterAttempts":{"type":"integer","minimum":1,"maximum":10,"default":3},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","description":"The partition key (ADR-0005). Written at venue scope"}}},
"CredentialOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicketId":{"type":"string","description":"Virtual Ticket ID"},"credentialId":{"type":"string","description":"Credential ID"},"mediaType":{"type":"string","description":"Media Type"},"customerParticipant":{"type":"string","description":"Customer / Participant"},"product":{"type":"string","description":"Product"},"event":{"type":"string","description":"Event"},"credentialStatus":{"type":"string","enum":["pendingGeneration","generated","pendingActivation","active","suspended","revoked","expired","failed"],"description":"Credential status"},"deliveryStatus":{"type":"string","enum":["notRequired","pending","sent","delivered","openedDownloaded","completed","failed","bounced","expired","cancelled"],"description":"Delivery status (15.3.4)"},"activationStatus":{"type":"string","enum":["pending","scheduled","active","notRequired"],"description":"Activation status"},"bindingStatus":{"type":"string","enum":["pending","bound","unbound","failed"],"description":"Binding status"},"provider":{"type":"string","description":"Provider"},"lastActivity":{"type":"string","format":"date-time","description":"Last Activity"},"exception":{"type":"string","description":"Exception"},"owner":{"type":"string","description":"Owner"}}},
"CredentialOperationsCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"virtualTicketsIssued":{"type":"integer","description":"Virtual Tickets Issued"},"credentialsGenerated":{"type":"integer","description":"Credentials Generated"},"activeCredentials":{"type":"integer","description":"Active Credentials"},"pendingGeneration":{"type":"integer","description":"Pending Generation"},"pendingDelivery":{"type":"integer","description":"Pending Delivery"},"pendingBinding":{"type":"integer","description":"Pending Binding"},"pendingActivation":{"type":"integer","description":"Pending Activation"},"suspended":{"type":"integer","description":"Suspended"},"revoked":{"type":"integer","description":"Revoked"},"expired":{"type":"integer","description":"Expired"},"failedGeneration":{"type":"integer","description":"Failed Generation"},"failedDelivery":{"type":"integer","description":"Failed Delivery"},"synchronizationExceptions":{"type":"integer","description":"Synchronization Exceptions"},"multiMediaVirtualTickets":{"type":"integer","description":"Multi-Media Virtual Tickets"},"virtualTicketsWithoutActiveMedia":{"type":"integer","description":"Virtual Tickets Without Active Media"},"dynamicQr":{"type":"integer","description":"Credentials of this media type"},"barcode":{"type":"integer","description":"Credentials of this media type"},"pdf":{"type":"integer","description":"Credentials of this media type"},"appleWallet":{"type":"integer","description":"Credentials of this media type"},"googleWallet":{"type":"integer","description":"Credentials of this media type"},"rfid":{"type":"integer","description":"Credentials of this media type"},"nfc":{"type":"integer","description":"Credentials of this media type"},"faceRecognitionReference":{"type":"integer","description":"Credentials of this media type"},"card":{"type":"integer","description":"Credentials of this media type"},"wristband":{"type":"integer","description":"Credentials of this media type"}}},
"CredentialReplacementInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Replace the media of a credential while the Virtual Ticket stays the same (decided 29 September, VM close-out).","required":["reason"],"properties":{"reason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"]},"newMediaKind":{"type":"string","description":"Media type of the replacement (`MediaTypeTechnologyLibraryView.mediaType`); empty keeps the current kind"},"newMediaCode":{"type":"string","description":"Code of the new physical media where one is encoded at the counter"},"approvalRequestId":{"type":"string","format":"uuid","description":"The granted approval, where the replacement rule requires one"},"note":{"type":"string","maxLength":500}}},
"CredentialReplacementReissueRevocationRecoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Replacement, Reissue, Revocation & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"],"description":"Replacement reason this policy covers"},"immediateOldMediaRevocation":{"type":"boolean","description":"Immediate old-media revocation"},"gracePeriod":{"type":"string","description":"ISO 8601 duration, e.g. PT30M"},"maximumReplacements":{"type":"integer","description":"Maximum replacements"},"identityVerification":{"type":"boolean","description":"Identity verification"},"supervisorApproval":{"type":"boolean","description":"Supervisor approval"},"reasonCodes":{"type":"array","items":{"type":"string"},"description":"Reason codes"},"recoveryAllowed":{"type":"boolean","description":"A suspended credential may be restored under this policy"}},"required":["reason"]},
"CredentialSecurityAuditOperationalEvidenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Security, Audit & Operational Evidence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicket":{"type":"string","description":"Virtual Ticket"},"credential":{"type":"string","description":"Credential"},"media":{"type":"string","description":"Media"},"action":{"type":"string","enum":["credentialRequested","generated","bound","delivered","activated","updated","presented","suspended","reactivated","replaced","revoked","expired","rebound","regenerated","deleted"],"description":"Lifecycle action recorded"},"before":{"type":"string","description":"Before"},"after":{"type":"string","description":"After"},"actor":{"type":"string","description":"Actor"},"source":{"type":"string","description":"Source"},"device":{"type":"string","description":"Device"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"reason":{"type":"string","description":"Reason"},"approval":{"type":"string","description":"Approval"},"providerReference":{"type":"string","description":"Provider reference"},"relatedTransaction":{"type":"string","description":"Related transaction"},"anomalyFlags":{"type":"array","items":{"type":"string","enum":["excessiveRegeneration","repeatedReplacement","suspiciousRebinding","multipleCredentialAssignments","unexpectedProviderTokenChanges","unauthorizedAdministrativeActions"]},"description":"Suspicious patterns flagged on this entry"}}},
"CredentialUsageCrossMediaTraceabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Usage & Cross-Media Traceability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicket":{"type":"string","description":"Virtual Ticket"},"credential":{"type":"string","description":"Credential"},"media":{"type":"string","description":"Media"},"presentationTimestamp":{"type":"string","format":"date-time","description":"Presentation timestamp"},"location":{"type":"string","description":"Location"},"device":{"type":"string","description":"Device"},"externalSystem":{"type":"string","description":"External system"},"transactionType":{"type":"string","description":"Transaction type"},"result":{"type":"string","description":"Result"},"entitlementImpact":{"type":"string","description":"Entitlement impact"},"synchronizationStatus":{"type":"string","description":"Synchronization status"}}},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Entitlement": {"type":"object","x-ticvai-persistence":"access.entitlement","description":"**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n","required":["id","templateId","productId","orderId","subjectId","status","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","description":"A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"},"templateId":{"type":"string","format":"uuid","description":"The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"},"productId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."},"orderLineId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"mediaCode":{"type":"string","description":"What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"},"status":{"$ref":"../spine/orders.yaml#/components/schemas/EntitlementStatus"},"statusNote":{"type":"string","nullable":true,"description":"**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","description":"**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"},"entriesUsed":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"},"entriesAllowed":{"type":"integer","nullable":true},"lastEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"},"firstEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the first admission, written by the same writes as `lastEntryAt`; it starts a time-bound entitlement's window (DEC-232; CHG-CSP-030). A replayed earlier scan moves it back."},"timeBoundUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Where the template is time-bound, when its window closes**: `firstEntryAt` plus the validity rule's `minutesAfterFirstScan` (decided 2 October 2026, Chinmay, BO-159; DEC-232; CHG-CSP-030). Null until the first scan and on an entitlement with no time bound. A scan after it is denied (`timeBoundWindowElapsed`); it never extends `validTo`, and the earlier of the two wins."},"lifecycleLabel":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"**The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model** (decided 2 October 2026, Chinmay, critical set 2, BO-336: \"Map the pack's 13 names onto the model; add any missing states\", and BO-336/DI-670: \"Reserved maps to Pending fulfilment\"; DEC-266; CHG-CSP-033). Computed on read from `status` (orders `EntitlementStatus`), `suspendedReason`, `cancellationKind`, `issuedVia` and an active identity lock; the mapping is in `states/entitlement-status.yaml`. It is what BO-334, BO-336 and the ticket status transition matrix (`AccessTicketStatusTransition`) show; logic still reads `status`."},"cancellationKind":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","enum":["voided","refunded","performanceCancelled","superseded"],"description":"**Which act cancelled the entitlement**, so the pack's Voided, Refunded and Reissued / superseded are told apart while `status` keeps the one r1 value `cancelled` (DEC-266; CHG-CSP-033). Written with the cancelling transition: `voidEntitlement`, `createRefund`, `cancelPerformance`, or a reissue that supersedes it (`supersedesEntitlementId` on the new one). Null unless `cancelled`."},"frozenDays":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"},"suspendedReason":{"type":"string","nullable":true},"freezeReason":{"type":"string","nullable":true,"enum":["travelling","injury","personal","seasonal","other"],"description":"The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."},"freezeNote":{"type":"string","nullable":true,"maxLength":500,"description":"The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."},"isNameBound":{"type":"boolean","default":false},"holderName":{"type":"string","nullable":true},"sharedWithSubjectIds":{"type":"array","description":"`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n","items":{"type":"string","format":"uuid"}},"issuedVia":{"type":"string","enum":["sale","invitation","reissue","transfer","resale","membership","groupBooking"],"description":"**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"},"supersedesEntitlementId":{"type":"string","format":"uuid","nullable":true,"description":"For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"},"walletValueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"},"facePassEnrolmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"}}},
"FailedGenerationDeliveryCredentialExceptionManagemenView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Failed Generation, Delivery & Credential Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"exceptionId":{"type":"string","format":"uuid","description":"The key `resolveCredentialException` acts on (decided 29 September, VM close-out)"},"lastAction":{"type":"string","enum":["retry","regenerate","useFallback","escalate","assignOwner","openTechnicalCase"],"description":"The last action taken through `resolveCredentialException`"},"failureType":{"type":"string","enum":["generationFailed","bindingFailed","activationFailed","deliveryFailed","walletFailure","rfidEncodingFailure","duplicateCredential","invalidToken","providerFailure","synchronizationFailure","missingTemplate","missingRequiredData","expiredCredential","mappingFailure","unknownCredential"],"description":"Failure category"},"severity":{"type":"string","enum":["low","medium","high","critical"],"description":"Severity, weighted by event proximity, arrival time, affected tickets, fallback availability, VIP and access impact"},"virtualTicket":{"type":"string","description":"Virtual Ticket"},"credential":{"type":"string","description":"Credential"},"media":{"type":"string","description":"Media"},"customer":{"type":"string","description":"Customer"},"event":{"type":"string","description":"Event"},"failure":{"type":"string","description":"Failure"},"time":{"type":"string","format":"date-time","description":"Time"},"operationalImpact":{"type":"string","description":"Operational Impact"},"owner":{"type":"string","description":"Owner"},"retryStatus":{"type":"string","description":"Retry status"}}},
"MediaBindingActivationAssignmentOperationsInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Media Binding, Activation & Assignment Operations submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"credentialIdUid":{"type":"string","description":"Credential ID or UID read from the medium; for face, the biometric provider reference"},"virtualTicketId":{"type":"string","description":"Virtual Ticket the medium is bound to"},"mediaKind":{"type":"string","enum":["rfid","nfc","wristband","physicalCard","faceRecognition","temporaryCredential"],"description":"Medium being bound"},"captureMethod":{"type":"string","enum":["scan","tap","manualLookup","batchAssignment","encoderAssignment"],"description":"How the medium was read or assigned"},"activationMode":{"type":"string","enum":["activateNow","schedule","activateOnFirstUse","activateOnCollection","temporaryActivation"],"description":"When the bound medium becomes active"},"provider":{"type":"string","description":"Provider"},"scheduledAt":{"type":"string","format":"date-time","description":"Activation time when scheduled"}},"required":["virtualTicketId","mediaKind","credentialIdUid"]},
"MediaBindingActivationAssignmentOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Binding, Activation & Assignment Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicketId":{"type":"string","description":"Virtual Ticket the medium is bound to"},"mediaKind":{"type":"string","enum":["rfid","nfc","wristband","physicalCard","faceRecognition","temporaryCredential"],"description":"Medium being bound"},"virtualTicket":{"type":"string","description":"Virtual Ticket"},"customer":{"type":"string","description":"Customer"},"product":{"type":"string","description":"Product"},"existingMedia":{"type":"string","description":"Existing Media"},"credentialIdUid":{"type":"string","description":"Credential ID / UID"},"provider":{"type":"string","description":"Provider"},"activationMode":{"type":"string","enum":["activateNow","schedule","activateOnFirstUse","activateOnCollection","temporaryActivation"],"description":"When the bound medium becomes active"},"validity":{"type":"string","description":"Validity"},"bindingRule":{"type":"string","description":"Binding Rule"},"captureMethod":{"type":"string","enum":["scan","tap","manualLookup","batchAssignment","encoderAssignment"],"description":"How the medium was read or assigned"},"scheduledAt":{"type":"string","format":"date-time","description":"Activation time when scheduled"}},"required":["virtualTicketId","mediaKind","credentialIdUid"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"TicketMediaAnalyticsAiOperationsIntelligenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Ticket Media Analytics & AI Operations Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialsGenerated":{"type":"integer","description":"Credentials Generated"},"generationSuccess":{"type":"number","description":"Generation Success %"},"deliverySuccess":{"type":"number","description":"Delivery Success %"},"activation":{"type":"number","description":"Activation %"},"walletAdoption":{"type":"number","description":"Percent"},"rfidAdoption":{"type":"number","description":"Percent"},"faceCredentialAdoption":{"type":"number","description":"Percent"},"multiMediaAdoption":{"type":"number","description":"Percent"},"replacementRate":{"type":"number","description":"Replacement Rate"},"revocationRate":{"type":"number","description":"Revocation Rate"},"generationFailure":{"type":"number","description":"Generation Failure %"},"deliveryFailure":{"type":"number","description":"Delivery Failure %"},"averageGenerationTime":{"type":"number","description":"Seconds"},"averageResolutionTime":{"type":"number","description":"Seconds"},"mediaUsageDistribution":{"type":"array","items":{"type":"string"},"description":"Share of eligible customers per media type; may exceed 100% in total"},"providerUptime":{"type":"number","description":"Percent"},"generationFailures":{"type":"integer","description":"Generation failures"},"encodingFailures":{"type":"integer","description":"Encoding failures"},"deliveryFailures":{"type":"integer","description":"Delivery failures"},"synchronizationDelay":{"type":"number","description":"Seconds"},"replacementFrequency":{"type":"number","description":"Replacement frequency"},"credentialFailureRisk":{"type":"string","description":"Predicted; advisory"},"deliveryFailureProbability":{"type":"number","description":"Predicted, 0 to 1; advisory"},"mediaDemandForUpcomingEvents":{"type":"string","description":"Media demand for upcoming events"},"rfidWristbandStockRequirements":{"type":"string","description":"RFID/wristband stock requirements"},"operationalWorkload":{"type":"string","description":"Operational workload"},"likelyOnSiteReplacementVolumes":{"type":"integer","description":"Predicted; advisory"}}},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}}
}
```
