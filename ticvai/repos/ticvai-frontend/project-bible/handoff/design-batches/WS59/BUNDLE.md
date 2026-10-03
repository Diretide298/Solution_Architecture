# WS59 — Ticket Media   Credential Management board 1

**10 screens · 16 operations · 18 schemas · 3 permissions**

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
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-334` | Virtual Ticket Command Center | B–D | 2 | 26 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-335` | Virtual Ticket Identity & Master Record Configuration | A | 9 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-336` | Virtual Ticket Status & Lifecycle Model | B–D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-337` | Media Type & Credential Technology Registry | B–D | 18 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-338` | Multi-Media Binding & Association Rules | B–D | 36 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-339` | Credential Identity, Token & Reference Mapping | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-340` | Entitlement & Cross-Media Synchronization Rules | B–D | 7 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-341` | Media Activation, Priority & Fallback Rules | B–D | 6 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-342` | Media Replacement, Revocation & Rebinding Rules | B–D | 22 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-343` | Virtual Ticket Architecture Testing, Governance & Audit | B–D | 9 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-336, BO-339, BO-340 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-334` Virtual Ticket Command Center

**Provide administrators and operations teams with a centralized view of all Virtual Tickets and their associated media across TICVAI. This is the primary administrative entry point into the Virtual Ticket architecture.**

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
| Route | `/access-venue/virtual-ticket-command-center-bo-334` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): listVirtualTicketStatus and listVirtualTicketArchitecture are the reads of BO-336 and BO-343; the hub needs neither, and the second needs AUDIT_VIEW, which … Removed 2 October 2026 (CHG-WIR-001): listVirtualTicketStatus and listVirtualTicketArchitecture are the reads of BO-336 and BO-343; the hub needs neither, and the second needs AUDIT_VIEW, which …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The hub of the Virtual Ticket architecture board (15.1): one place where an administrator or an operations lead finds any Virtual Ticket and sees, in one row, its status, how much of it is used and every medium that carries it. It opens the nine configuration screens of the board and returns from them. The one thing to get right: a ticket is one row with its media listed under it ("VT-2026-009821, 4 media: Dynamic QR active, RFID active, Apple Wallet active, Face active"), never one row per medium, and a media code typed in the search finds the ticket it belongs to.

**Known correction pending (do not draw the wrong version)**

- **KPI "Pending Activation" and "Revoked" have no matching ticket status** Why: The row's ticketStatus enum has pendingFulfillment (not pending activation) and no revoked value; revoked is a media status. Either the tiles count tickets whose media are pending or revoked (and say so: "Tickets with revoked media"), or the enum is wrong. *(source: contracts/spine/access.yaml#/components/schemas/VirtualTicketCommandCenterView / contracts/spine/access.yaml#/components/schemas/VirtualTicketCommandCenterViewSummary; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Row carries only a media count and the primary medium** Why: The pack example and DI-652 need each linked medium with its own status in the row or detail; add a media summary (type, code masked, status) to the view or bind getEntitlementCredential on selection. *(source: screens/P08-venue-back-office.yaml#BO-334 / DI-652; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation lists exits to BO-340 to BO-343 but declares transitions only to BO-335 to BO-339** Why: All nine board screens must be reachable from the hub (DI-653). *(source: screens/P08-venue-back-office.yaml#BO-334 / DI-653; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Ticket status vocabulary (13 values) differs from the entitlement state model of record** Why: orders.EntitlementStatus has issued, partiallyConsumed, fullyConsumed, expired, cancelled, surrendered (suspended is a flag). The hub, BO-336 and the guest screens must show one vocabulary; see BO-336. *(source: contracts/spine/orders.yaml#/components/schemas/EntitlementStatus / contracts/spine/access.yaml#setTicketStatusTransition; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every virtual ticket", "The selected virtual ticket" and the permissions banner** Why: Generated placeholders (VO-R12); the banner is a build note, not UI - the permissions become per-action enablement. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039 / ADR-0002 / DI-387; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): listVirtualTicketStatus and listVirtualTicketArchitecture are bound on load of the hub (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do "Pending Activation" and "Revoked" count tickets or media?** → Drawn default accepted: Draw them as "Tickets awaiting media activation" and "Tickets with revoked media". *(decided by Chinmay, 2026-10-02; DEC-265 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search virtual ticket | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by brand, venue, event, product, performance, ticket type and 7 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | text field | — | — | `listVirtualTicket` ?brand |
| Venue | text field | — | — | `listVirtualTicket` ?venue |
| Event | text field | — | — | `listVirtualTicket` ?event |
| Performance | text field | — | — | `listVirtualTicket` ?performance |
| Channel | text field | — | — | `listVirtualTicket` ?channel |
| Customer | text field | — | — | `listVirtualTicket` ?customer |
| Virtual ticket status | text field | — | — | `listVirtualTicket` ?virtualTicketStatus |
| Media type | text field | — | — | `listVirtualTicket` ?mediaType |
| Product | text field | — | — | `listVirtualTicket` ?product |
| Ticket type | text field | — | — | `listVirtualTicket` ?ticketType |
| Number of media | text field | — | — | `listVirtualTicket` ?numberOfMedia |
| Validity | text field | — | — | `listVirtualTicket` ?validity |
| Usage status | text field | — | — | `listVirtualTicket` ?usageStatus |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search virtual ticket**: One search box that accepts a Virtual Ticket ID (VT-2026-009821), an order reference, a holder name or any media code (QR-7F3K-92LD, RF-10452, a wallet serial). A media code resolves to its ticket and the result row highlights which medium matched. listVirtualTicket has no free-text or media-code parameter, so bind the media-code case to the resolver lookup (lookupTicket by mediaCode) and flag the gap. *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#listVirtualTicket / contracts/spine/access.yaml#lookupTicket / DI-180)*
- **Filter by**: Thirteen filters, so draw the five most used as visible chips (Venue from the top-bar switcher per VO-R09, Event, Product, Virtual Ticket status, Media type) and the rest (Brand, Performance, Ticket type, Channel, Customer, Number of media, Validity, Usage status) under "More filters". Number of media is a choice 0 / 1 / 2 / 3+ (0 is the "no active media" problem set); Validity is a date range in venue time; status and usage are multi-select chips with the status words of BO-336. *(source: screens/P08-venue-back-office.yaml#BO-334 / contracts/spine/access.yaml#listVirtualTicket)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Virtual Tickets** (metric tile)

**Active** (metric tile)

**Pending Activation** (metric tile)

**Suspended** (metric tile)

**Used / Consumed** (metric tile)

**Partially Consumed** (metric tile)

**Expired** (metric tile)

**Cancelled** (metric tile)

**Revoked** (metric tile)

**Virtual Tickets with Multiple Media** (metric tile)

**Virtual Tickets with No Active Media** (metric tile)

**Media Binding Exceptions** (metric tile)

**Credential Synchronization Issues** (metric tile)

**Every virtual ticket** (data table, from `listVirtualTicket`)

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket ID |
| Product | text | Product |
| Event performance | text | Event / Performance |
| Ticket holder | text | Ticket Holder |
| Order reference | text | Order Reference |
| Ticket type | text | Ticket Type |
| Seat resource where applicable | text | Seat / Resource where applicable |
| Ticket status | chip: Created, Pending fulfillment, Active, Partially used, Used, Expired… | Virtual Ticket status (lifecycle 15.1.3) |
| Usage status | chip: Unused, Partially used, Used | How much of the entitlement is consumed |
| Number of linked media | 1,234 | Number of Linked Media |
| Primary media | text | Primary Media |
| Last credential activity | 1 Oct 2026, 14:30 | Last Credential Activity |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |

**The selected virtual ticket** (detail panel): The pack groups this record's detail under its own headings: “VT-2026-009821”.

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket ID |
| Product | text | Product |
| Event performance | text | Event / Performance |
| Ticket holder | text | Ticket Holder |
| Order reference | text | Order Reference |
| Ticket type | text | Ticket Type |
| Seat resource where applicable | text | Seat / Resource where applicable |
| Ticket status | chip: Created, Pending fulfillment, Active, Partially used, Used, Expired… | Virtual Ticket status (lifecycle 15.1.3) |
| Usage status | chip: Unused, Partially used, Used | How much of the entitlement is consumed |
| Number of linked media | 1,234 | Number of Linked Media |
| Primary media | text | Primary Media |
| Last credential activity | 1 Oct 2026, 14:30 | Last Credential Activity |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** View Virtual Ticket, View Media, Bind Media, Replace Media, Suspend, Reactivate, Revoke Media, View Usage, View Audit, Diagnose Credential. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Thirteen tiles per VO-R02, computed over the whole filtered set, not the page. Group them in two rows: lifecycle (Total, Active, Pending activation, Suspended, Used, Partially used, Expired, Cancelled, Revoked) and health (With multiple media, With no active media, Media binding exceptions, Credential synchronisation issues). The health row is amber/red when non-zero and each tile filters the directory to its set; "With no active media" also names how many are for events in the next 24 hours. *(source: screens/P08-venue-back-office.yaml#BO-334 / contracts/spine/access.yaml#/components/schemas/VirtualTicketCommandCenterViewSummary)*
- **Virtual Ticket directory**: Title "Virtual Tickets" (VO-R12). Columns: Virtual Ticket ID (monospace, copyable), Product, Event / performance, Holder, Order reference, Ticket type, Seat or resource, Valid from-to, Ticket status, Usage (Unused / Partly used / Used), Media (count plus media icons, primary first), Last credential activity (relative, "12 min ago", full time on hover), Last modified. Sort by last credential activity, newest first. Cursor paging (VO-R12), the list grows with every sale. *(source: screens/P08-venue-back-office.yaml#BO-334 / contracts/spine/access.yaml#/components/schemas/VirtualTicketCommandCenterView)*
- **Ticket detail panel**: Shows the pack's worked example as a card: the ticket header (ID, product, holder, seat, status), then each linked medium on its own line with its own status ("RFID - Lost / Revoked" while the ticket stays Active), so ticket status and media status are visibly separate. "Open 360 view" goes to BO-355 with the ticket id. *(source: screens/P08-venue-back-office.yaml#BO-334 / screens/P08-venue-back-office.yaml#BO-336 / DI-652)*
- **AI condition flags**: A short list above the directory in the pack's wording ("128 Virtual Tickets for tomorrow's event have no active customer-presentable media"; "17 Virtual Tickets have multiple credentials with inconsistent activation states"), each with "Show these" that applies the filter. Labelled advisory; it never changes ticket validity (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-334 / screens/P08-venue-back-office.yaml#BO-335)*
- **Board tiles**: Nine tiles opening BO-335 to BO-343 in the pack order (Identity, Lifecycle, Media registry, Binding rules, Credential resolver, Synchronisation, Activation and fallback, Replacement rules, Test and govern), drawn as the board configuration flow; each returns here (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-343 / DI-653)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Row quick actions**: View ticket and View media open BO-355; View usage and View audit open BO-361 and BO-362 filtered to the ticket; Bind media opens BO-358, Replace media opens BO-359, Suspend opens the lock manager (BO-247, lock scope "this medium only"). Reactivate, Revoke media and Diagnose credential have no operation: draw them disabled with "Not available yet". Each enabled action is greyed with the missing permission named when the user lacks it (VO-R08). *(source: contracts/spine/access.yaml#listVirtualTicket / contracts/spine/access.yaml#lockIdentity / contracts/spine/access.yaml#replaceCredential)*
- **Export**: designer default - not drawn; no export operation is bound and the pack does not ask for one. *(source: designer default)*

**Data it reads**: `listVirtualTicket` (onLoad, Virtual Ticket Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-335` Virtual Ticket Identity & Master Record Configuration: *Works in Virtual Ticket Identity & Master Record Configuration*; calls `listVirtualTicket`
- → `BO-336` Virtual Ticket Status & Lifecycle Model: *Works in Virtual Ticket Status & Lifecycle Model*; calls `listVirtualTicket`
- → `BO-337` Media Type & Credential Technology Registry: *Works in Media Type & Credential Technology Registry*; calls `listVirtualTicket`
- → `BO-338` Multi-Media Binding & Association Rules: *Works in Multi-Media Binding & Association Rules*; calls `listVirtualTicket`
- → `BO-339` Credential Identity, Token & Reference Mapping: *Works in Credential Identity, Token & Reference Mapping*; calls `listVirtualTicket`
- → `BO-340` Entitlement & Cross-Media Synchronization Rules: *Works in Entitlement & Cross-Media Synchronization Rules*; calls `listVirtualTicket`
- → `BO-341` Media Activation, Priority & Fallback Rules: *Works in Media Activation, Priority & Fallback Rules*; calls `listVirtualTicket`
- → `BO-342` Media Replacement, Revocation & Rebinding Rules: *Works in Media Replacement, Revocation & Rebinding Rules*; calls `listVirtualTicket`
- → `BO-343` Virtual Ticket Architecture Testing, Governance & Audit: *Works in Virtual Ticket Architecture Testing, Governance & Audit*; calls `listVirtualTicket`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the virtual ticket are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Media code belongs to a ticket in another venue**: The lookup says "VT-2026-004410 belongs to Summit Peaks" and does not switch venue (VO-R09). *(source: ADR-0030)*
- **User has SCOPE_VIEW but not AUDIT_VIEW**: The hub must still load. Today listVirtualTicketArchitecture (AUDIT_VIEW) is bound on load and would refuse; load it only inside BO-343. *(source: contracts/spine/access.yaml#listVirtualTicketArchitecture)*
- **Ticket with zero media**: Row shows "No media" in amber with "Generate" leading to BO-356; never an empty cell. *(source: screens/P08-venue-back-office.yaml#BO-334)*

#### Consistency with other screens

- Match `BO-354`: BO-354 is the same estate seen per credential instance; BO-334 is per ticket. Same status chips, same media icons, and the row of either opens BO-355. BO-174 (Media & Credential Command Center, access board) is a third hub over the same data and should collapse into one of these (VO-R14, DI-671).
- Match `BO-335`: Ticket IDs display in the format configured there (VT-{yyyy}-{000000000}).
- Match `WEB-018`: The ticket status words here map one-to-one to the guest words on WEB-018 and GST-012 (Ready to use, Partly used, Used, Expired, Cancelled, Transferred away).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  total: 184220
  active: 61340
  pendingActivation: 2210
  suspended: 38
  used: 109870
  partiallyUsed: 7412
  expired: 3120
  cancelled: 212
  revoked: 18
  multipleMedia: 9420
  noActiveMedia: 128
  bindingExceptions: 7
  syncIssues: 17
rows:
- id: VT-2026-009821
  product: Aqua Park Day Pass - Adult
  event: Sat 10 Oct 2026
  holder: Sara Al Nuaimi
  order: ORD-2026-55120
  status: Active
  usage: Unused
  media: 3 - Dynamic QR (primary), RFID wristband, Apple Wallet
  lastActivity: 10 Oct 09:14 Main Plaza Gate 2
- id: VT-2026-004410
  product: Summit Peaks Annual Pass
  holder: Khalid Al Zaabi
  status: Active
  usage: Partly used
  media: 4 - Face (primary), RFID card, Mobile QR, Google Wallet
- id: VT-2026-011902
  product: Falcon Coaster Fast Pass
  holder: Priya Nair
  status: Pending activation
  usage: Unused
  media: 0 - No media
```

#### Permissions

- `listVirtualTicket` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-334` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-334`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 1: Opens Virtual Ticket Command Center → Provide administrators and operations teams with a centralized view of all Virtual Tickets and their associated media across TICVAI. This is the primary administrative entry point into the Virtual …
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F168 branch at step 1 (expected): when Nothing has been set up on Virtual Ticket Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F168 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-334?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-335`, `BO-336`, `BO-337`, `BO-338`, `BO-339`, `BO-340`, `BO-341`, `BO-342`, `BO-343`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-335` Virtual Ticket Identity & Master Record Configuration

**Define the authoritative Virtual Ticket object used throughout TICVAI. This screen is extremely important because the Virtual Ticket—not the QR/RFID/card— is the master ticket record.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · task APP-SETUP-BO-335 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/virtual-ticket-identity-master-record-configuration-bo-335` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Defines the Virtual Ticket - the master ticket record that every QR, wristband, card, wallet pass or face attaches to - for a venue: the ticket number format (prefix, suffix, length, e.g. VT-2026-000009821), classification, ownership and holder rules, transferability, validity, consumption and entitlement models, and which media a ticket must carry. The one thing to get right: show that the number never changes when media are replaced, regenerated, reprinted or moved to another device.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Every model field is a free string in the write and a selectField with no options on the screen (CHG-SBO-005)
- Write-only; no read of the current configuration (CHG-SBO-005)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What are the allowed values of ticket classification, ownership model, holder assignment, consumption model and entitlement model?** → Drawn default accepted: Draw the selects greyed with "Options to be agreed"; validity and transferability use the existing vocabularies. *(decided by Chinmay, 2026-10-02; DEC-129 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ID generation pattern | select field | — | — | — | — | — | — |
| Ticket classification | select field | — | — | — | — | — | — |
| Ticket ownership model | select field | — | — | — | — | — | — |
| Holder assignment requirements | select field | — | — | — | — | — | — |
| Transferability reference | select field | — | — | — | — | — | — |
| Validity model | select field | — | — | — | — | — | — |
| Consumption model | select field | — | — | — | — | — | — |
| Entitlement model | select field | — | — | — | — | — | — |
| Media requirements | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **idGenerationPattern**: Builder of prefix (e.g. VT-), year token, separator, sequence length (e.g. 9), suffix; live preview "VT-2026-000009821"; sequence randomised per MATRIX 3.2.5. *(source: screens/P08-venue-back-office.yaml#BO-335 / DI-608 / MATRIX 3.2.5)*
- **Models (classification, ownership, holder assignment, transferability, validity, consumption, entitlement)**: The pack names the nine models but gives no option lists. Draw each as a select, filled where the package already has a vocabulary (validity model = Fixed dates / N days after sale / after activation / after first use, as the admission profile; transferability = the product template's transferable setting) and greyed with "Options to be agreed" for the rest; never free text. *(source: screens/P08-venue-back-office.yaml#BO-335 / contracts/spine/access.yaml#/components/schemas/AdmissionRules / MATRIX 1.1.27)*
- **mediaRequirements**: Multi-select of QR, Dynamic QR, RFID wristband, NFC, Wallet pass, Face; order sets the fallback order shown on the ticket. *(source: contracts/spine/access.yaml#setVirtualTicketIdentity / DI-608 / DI-652)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Persistence statement**: A fixed panel listing what does not change the number (media replacement, QR regeneration, RFID replacement, wallet update, device change, face enrolment change, reprint). *(source: screens/P08-venue-back-office.yaml#BO-335)*
- **Master record references**: Read-only list of what a Virtual Ticket references (order, line, reservation, product and version, event, performance, venue, holder, participant, customer, membership, seat). *(source: screens/P08-venue-back-office.yaml#BO-335)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save configuration**: Applies to tickets issued after saving; existing numbers never change (say so in the confirmation). *(source: screens/P08-venue-back-office.yaml#BO-335 / TRACKER Actions row 194)*

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `setVirtualTicketIdentity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket identity configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket identity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket identity configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-334`: The Virtual Ticket command centre and workspace display numbers in this format.
- Match `WEB-018`: Guests see the same ticket number under their code.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
config:
  pattern: VT-{yyyy}-{000000000}
  preview: VT-2026-000009821
  media: Dynamic QR, RFID wristband (fallback), Face (members only)
mediaIndependence: RFID-77812 lost and revoked; RFID-99142 issued; ticket stays VT-009821
```

#### Permissions

- `setVirtualTicketIdentity` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-335` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-335`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 2: Works in Virtual Ticket Identity & Master Record Configuration → Define the authoritative Virtual Ticket object used throughout TICVAI. This screen is extremely important because the Virtual Ticket—not the QR/RFID/card— is the master ticket record.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-335?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-336` Virtual Ticket Status & Lifecycle Model

**Configure the standardized lifecycle of a Virtual Ticket independently from the lifecycle of individual media.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/virtual-ticket-status-lifecycle-model-bo-336` |

**What the spec says about it.** **The pack's 13 Virtual Ticket status names map onto the entitlement model (decided 2 October 2026 by Chinmay, DEC-266; CHG-CSP-033); no state is missing.** Reserved is Pending fulfilment (DEC-267).

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Configures the Virtual Ticket lifecycle - which status moves are allowed, which need an authorised exception, and which systems may cause them - separately from the status of any medium. A ticket stays Active when its RFID is lost and revoked. The one thing to get right: the venue can only narrow the platform lifecycle, never add moves to it, so draw the seeded matrix with switches, not a blank table.

**Known correction pending (do not draw the wrong version)**

- **Two status vocabularies for one ticket** Why: The transition rows use 13 statuses (created, pendingFulfillment, active, partiallyUsed, used, expired, suspended, cancelled, voided, reissuedSuperseded, refunded, transferred, blocked); the write says rows are seeded from the entitlement state model, whose enum is issued, partiallyConsumed, fullyConsumed, expired, cancelled, surrendered with suspended as a flag. They cannot both be the ticket's … *(source: contracts/spine/access.yaml#setTicketStatusTransition / contracts/spine/orders.yaml#/components/schemas/EntitlementStatus / DI-670; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Content region is an empty unbound table and the gap says the pack gives nothing to draw** Why: The pack gives the states, the example transitions, the trigger sources and the propagation example; bind listVirtualTicketStatus to the matrix. *(source: screens/P08-venue-back-office.yaml#BO-336 / contracts/spine/access.yaml#listVirtualTicketStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The write's overlay lists id and scopePath as required** Why: Server-owned (VO-R03); the key is the from/to pair. *(source: contracts/spine/access.yaml#/components/schemas/AccessTicketStatusTransition; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Button "Save ticket status transition"** Why: Generated label; "Save" inside the cell editor. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which status list is authoritative for the Virtual Ticket - the pack's 13 or the entitlement model's 6 plus the suspended flag?** → Map the pack's 13 Virtual Ticket status names onto the entitlement model; add any missing states. *(decided by Chinmay, 2026-10-02; DEC-266 / CHG-NOTE-008)*
- **DI-670 lists entitlement statuses active, reserved, consumed, transferred, expired, refunded/cancelled; the ticket lifecycle has no Reserved. Is Reserved the same as Pending fulfilment?** → Drawn default stands (answer: "As BO-336: Reserved maps to Pending fulfilment"): Show Pending fulfilment with the subtitle "Reserved, not yet issued". *(decided by Chinmay, 2026-10-02; DEC-267 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Form: Save ticket status transition** (modal, opened by *Save ticket status transition*; *Save ticket status transition* calls `setTicketStatusTransition`, *Cancel* sends nothing)

**Collects what `setTicketStatusTransition` sends before it is called.** Required: `id`, `fromStatus`, `toStatus`, `allowed`, `requiresAuthorizedException`, `scopePath`. Optional: `originatingSources`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setTicketStatusTransition` body |
| From status `fromStatus` | select | required | — | Created · Pending fulfillment · Active · Partially used · Used · Expired · Suspended · Cancelled · Voided · Reissued superseded · Refunded · Transferred … | — | — | `setTicketStatusTransition` body |
| To status `toStatus` | select | required | — | Created · Pending fulfillment · Active · Partially used · Used · Expired · Suspended · Cancelled · Voided · Reissued superseded · Refunded · Transferred … | — | Unique with fromStatus per scope | `setTicketStatusTransition` body |
| Allowed `allowed` | toggle | required | — | — | — | — | `setTicketStatusTransition` body |
| Requires authorized exception `requiresAuthorizedException` | toggle | required | off | — | — | Allowed only with an authorised exception, e.g. | `setTicketStatusTransition` body |
| Originating sources `originatingSources` | multi-select chips | optional | — | Order management · Cancellation · Refund · Upgrade conversion · Ticket transfer · Membership · Expiry · Access usage · Authorized operator · API · Scheduled process | — | — | `setTicketStatusTransition` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setTicketStatusTransition` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 The transition is not in the entitlement state model.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Transition (fromStatus, toStatus)**: Draw a from-by-to matrix of the ticket statuses (rows = from, columns = to). Each cell is one rule: Allowed (green tick), Needs authorised exception (amber key), Not allowed (grey). Cells the platform model does not have are locked with "Not in the platform lifecycle" - turning one on is refused (422). Clicking a cell opens a small editor; there are no id or scopePath inputs (VO-R03). *(source: contracts/spine/access.yaml#setTicketStatusTransition)*
- **requiresAuthorizedException**: Toggle "Needs an authorised exception" (default off); the pack's example is Used to Active. When on, the editor says which permission grants the exception (supervisor override) and that every use is logged. *(source: screens/P08-venue-back-office.yaml#BO-336 / contracts/spine/access.yaml#setTicketStatusTransition)*
- **originatingSources**: Chips, multi-select, from the closed list Order management, Cancellation, Refund, Upgrade / conversion, Ticket transfer, Membership, Expiry, Access usage, Authorised operator, API, Scheduled process. Empty means any source; say so ("Any source"). *(source: screens/P08-venue-back-office.yaml#BO-337 / contracts/spine/access.yaml#/components/schemas/AccessTicketStatusTransition)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save ticket status transition (primary button) | `setTicketStatusTransition` PUT `/ticket-status-transitions` | AccessTicketStatusTransition | AccessTicketStatusTransition | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 The transition is not in the entitlement state model. | gated `ACCESS_POINT_CONFIGURE`; opens modal first; produces a document or message: Set a Virtual Ticket status transition rule |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Status legend**: The six main statuses as a horizontal flow (Created > Pending fulfilment > Active > Partially used > Used > Expired) with the governed alternatives (Suspended, Cancelled, Voided, Reissued / superseded, Refunded, Transferred, Blocked) below it, as the pack lays them out. The pack's 13 names map onto the entitlement model, and states the model lacks are added (Reserved is Pending fulfilment). *(source: screens/P08-venue-back-office.yaml#BO-336 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **Ticket vs media separation panel**: A fixed explanatory panel using the pack example: Virtual Ticket ACTIVE; QR Active, RFID Lost / Revoked, Apple Wallet Active, Face Active - "The ticket itself remains valid." *(source: screens/P08-venue-back-office.yaml#BO-336 / DI-652)*
- **Cross-media propagation**: Read-only summary of what each ticket status does to every bound medium (Cancelled - QR unusable, RFID unusable, Wallet updated or revoked, Face association inactive), with "Edit in Synchronisation rules" linking to BO-340, which owns that write. *(source: screens/P08-venue-back-office.yaml#BO-337 / contracts/spine/access.yaml#setCredentialEventPropagationRule)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save transition**: One PUT per cell (the row key is the from/to pair, so per-cell save is correct here, unlike VO-R04 forms). Confirmation names the effect ("Active to Suspended will need an authorised exception from now on; 61,340 active tickets affected"). 422 on a move the platform does not have, shown on the cell. *(source: contracts/spine/access.yaml#setTicketStatusTransition)*

**Data it reads**: `listVirtualTicketStatus` (onLoad, Virtual Ticket Status & Lifecycle Model)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listVirtualTicketStatus`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket status list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket status yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the virtual ticket status are still there. The pack's own statuses are Order Management — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The transition is not in the entitlement state model. |

#### Edge cases to draw

- **Turning off a move a live process depends on (for example Active to Cancelled used by refunds)**: Warn which sources use it ("Refund and Cancellation originate this move; refunds will fail to cancel the ticket") before saving. *(source: contracts/spine/access.yaml#/components/schemas/AccessTicketStatusTransition / designer default)*
- **Viewer without access configuration rights**: Matrix read-only, cells not clickable, "Needs access configuration rights" (VO-R08). *(source: contracts/spine/access.yaml#setTicketStatusTransition)*

#### Consistency with other screens

- Match `BO-334`: Same status names and colours in the hub's chips and KPI tiles.
- Match `BO-340`: Propagation of a status change to media is configured there; this screen only shows it.
- Match `WEB-018`: Guest-facing words for the same states (Ready to use, Partly used, Used, Expired, Cancelled, Transferred away) per DI-670.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
- from: Active
  to: Suspended
  rule: Allowed
  sources: Authorised operator, Membership
- from: Suspended
  to: Active
  rule: Allowed
  sources: Authorised operator
- from: Active
  to: Cancelled
  rule: Allowed
  sources: Cancellation, Refund
- from: Used
  to: Active
  rule: Needs authorised exception
  sources: Authorised operator
- from: Expired
  to: Active
  rule: Not in the platform lifecycle
```

#### Permissions

- `listVirtualTicketStatus` → `SCOPE_VIEW` (read) · staff
- `setTicketStatusTransition` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-336` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-336`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 4: Works in Virtual Ticket Status & Lifecycle Model → Configure the standardized lifecycle of a Virtual Ticket independently from the lifecycle of individual media.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-336?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save ticket status transition.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-337` Media Type & Credential Technology Registry

**Maintain the centralized catalogue of credential technologies supported by TICVAI. This makes the credential architecture extensible rather than hard-coded.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For each technology configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-type-credential-technology-registry-bo-337` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The catalogue of credential technologies - QR, dynamic QR, barcode, PDF, Apple and Google Wallet, RFID and NFC cards and wristbands, printed and thermal tickets, membership cards, wearables, face reference and future tenant-defined media - each with its capabilities, providers and integration adapter. New media are new rows, never a redesign. The one thing to get right: media type and vendor are separate (RFID is one type, implemented by several providers), and a type in use can only be retired, never deleted.

**Known correction pending (do not draw the wrong version)**

- **Screen binds two reads (listMediaTypeTechnology and listMediaTypeCredential) and no write** Why: A configuration editor with no save; the registry write exists only for BO-175. Merge the two catalogue shapes into one record and one write. *(source: contracts/spine/access.yaml#listMediaTypeTechnology / contracts/spine/access.yaml#listMediaTypeCredential / contracts/spine/access.yaml#setMediaTypeTechnology; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **All eighteen controls are selectFields, including Name, ID and eight Yes/No capabilities** Why: Text inputs, toggles and multi-selects as above; selects with no options cannot be filled. *(source: contracts/spine/access.yaml#/components/schemas/MediaTypeCredentialTechnologyRegistryView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Supports encryption/signing" is one control over two contract flags** Why: supportsEncryption and supportsSigning are separate capabilities. *(source: contracts/spine/access.yaml#/components/schemas/MediaTypeCredentialTechnologyRegistryView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Two media vocabularies across the board** Why: The registry view uses category (digital, physical, biometric, future) with free technology text; the library write uses a mediaType enum (qr, rfidIso15693, facePass, faceTag, partnerQr, thirdPartyCredential and more); binding rules, activation rules and the delivery and exception enums each use yet another list. Every media picker in Boards 1 to 3 should read one list. *(source: contracts/spine/access.yaml#/components/schemas/MediaTypeCredentialTechnologyRegistryView / contracts/spine/access.yaml#setMediaTypeTechnology / contracts/spine/access.yaml#resolveCredentialException; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which face recognition and RFID vendors are integrated (provider list)?** → Drawn default accepted: Show providers as "To be named" chips; HID and Suprema are candidates. *(decided by Chinmay, 2026-10-02; DEC-268 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Media Type ID | select field | — | — | — | — | — | — |
| Name | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Technology | select field | — | — | — | — | — | — |
| Token format | select field | — | — | — | — | — | — |
| Generation method | select field | — | — | — | — | — | — |
| Validation mechanism | select field | — | — | — | — | — | — |
| Supports visual design | select field | — | — | — | — | — | — |
| Supports dynamic update | select field | — | — | — | — | — | — |
| Supports revocation | select field | — | — | — | — | — | — |
| Supports expiration | select field | — | — | — | — | — | — |
| Supports offline reference | select field | — | — | — | — | — | — |
| Supports replacement | select field | — | — | — | — | — | — |
| Supports encryption/signing | select field | — | — | — | — | — | — |
| Supported channels | select field | — | — | — | — | — | — |
| Supported devices | select field | — | — | — | — | — | — |
| Integration adapter | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Media Type ID / Name**: ID is a short upper-case key (QR-DYN, RFID-WB) shown read-only after the first save; Name has an Arabic variant (VO-R10). The generated selectFields for ID and Name are text inputs. *(source: contracts/spine/access.yaml#/components/schemas/MediaTypeCredentialTechnologyRegistryView)*
- **Category**: Four cards - Digital, Physical, Biometric, Future (tenant-defined / integration-based). *(source: screens/P08-venue-back-office.yaml#BO-337 / contracts/spine/access.yaml#listMediaTypeCredential)*
- **Provider**: Multi-select of integrated providers (several RFID vendors per type); shown as chips with each provider's adapter. *(source: screens/P08-venue-back-office.yaml#BO-337)*
- **Supports visual design / dynamic update / revocation / expiration / offline reference / replacement / encryption / …**: Eight Yes/No toggles in a "Capabilities" group, not selects. They drive the rest of the board: a type without "Supports revocation" cannot be chosen as a medium that must stop scanning on cancellation (BO-340), one without "Supports offline reference" is flagged on gates working offline. Encryption and signing are two toggles (the contract has two flags; the screen merged them into one). *(source: screens/P08-venue-back-office.yaml#BO-337 / contracts/spine/access.yaml#/components/schemas/MediaTypeCredentialTechnologyRegistryView)*
- **Token format / Generation method / Validation mechanism / Integration adapter**: Selects where a closed set exists (validation mechanism: online lookup, offline signed payload, offline seed rotation, biometric match) and text otherwise; integration adapter is a pick from the registered adapters, never free text. *(source: contracts/spine/access.yaml#listMediaTypeCredential / designer default)*
- **Supported channels / Supported devices**: Multi-select chips (channels - web, app, POS, kiosk, box office, API; devices - turnstile, handheld, kiosk reader, printer, encoder). *(source: contracts/spine/access.yaml#listMediaTypeCredential / designer default)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Registry list**: Grouped by category; columns Name, Technology, Providers, capability icons (eight small icons, lit when supported), Channels, Active. The pack's minimum list is seeded rows, shown with "Platform seed". *(source: screens/P08-venue-back-office.yaml#BO-337 / contracts/spine/access.yaml#listMediaTypeCredential)*
- **Usage**: In the detail, "Used by 3 binding rules, 2 media templates, 41,280 active credentials" so a retire is an informed decision. *(source: contracts/spine/access.yaml#setMediaTypeTechnology / designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save media type**: Whole-record upsert keyed by media type id (VO-R04). Today the only write is setMediaTypeTechnology, which serves BO-175's library shape; bind it here too once the two shapes are merged. *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*
- **Retire**: Sets Active off, never deletes (issued credentials still validate); refused 409 when an active encoding profile names the type, with the profiles listed. *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*

**Data it reads**: `listMediaTypeTechnology` (onLoad, Media Type & Technology Library); `listMediaTypeCredential` (onLoad, Media Type & Credential Technology Registry)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listMediaTypeCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media type credential configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media type credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media type credential configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Future / tenant-defined media type (hotel room key, city transit card)**: Category Future requires an integration adapter before it can be activated. *(source: screens/P08-venue-back-office.yaml#BO-337 / DI-652)*

#### Consistency with other screens

- Match `BO-175`: BO-175 Media Type & Technology Library (access board) edits the same catalogue with a different shape (listMediaTypeTechnology + setMediaTypeTechnology). One screen survives with both shapes merged (VO-R14); the BO-337 name and the pack 15.1.4 fields are the richer set.
- Match `BO-338`: Binding rules pick media types from this registry only.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
types:
- id: QR-DYN
  name: Dynamic QR
  category: Digital
  providers: TICVAI
  capabilities: dynamic update, revocation, expiration, offline reference, signing
  channels: App
- id: RFID-WB
  name: RFID Wristband
  category: Physical
  providers: HID, Suprema
  capabilities: revocation, replacement, offline reference
  devices: Turnstile, Handheld, Encoder
- id: AW-PASS
  name: Apple Wallet pass
  category: Digital
  providers: Apple
  capabilities: visual design, dynamic update, revocation, expiration
- id: FACE-REF
  name: Face recognition reference
  category: Biometric
  providers: Face vendor (to be named)
  capabilities: revocation, replacement
```

#### Permissions

- `listMediaTypeTechnology` → `SCOPE_VIEW` (read) · staff
- `listMediaTypeCredential` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-337` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-337`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 6: Works in Media Type & Credential Technology Registry → Maintain the centralized catalogue of credential technologies supported by TICVAI. This makes the credential architecture extensible rather than hard-coded.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-337?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-338` Multi-Media Binding & Association Rules

**Configure how one Virtual Ticket can be associated with multiple media simultaneously. This is one of the most important screens in Area 15.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/access-venue/multi-media-binding-association-rules-bo-338` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The rules for how many and which media one Virtual Ticket may carry at once - allowed, mandatory and optional media, their roles (primary, secondary, backup, temporary), the combinations allowed and which activation revokes which - scoped by product, ticket type, event, customer type, membership, channel, age, country and access environment. The pack calls it one of the most important screens of the area. The one thing to get right: a rule reads as a sentence per product ("Annual pass: Face required; Mobile QR and RFID card optional"), and nothing here can create a second entitlement.

**Known correction pending (do not draw the wrong version)**

- **Twelve selectFields with no options, including the counts** Why: Media lists need the grid above, counts need steppers, and combinations need rule rows; the screen also has no list of rules although it opens with a ruleId. *(source: screens/P08-venue-back-office.yaml#BO-338 / contracts/spine/access.yaml#listMultiMediaBinding; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Scope conditions (product, ticket type, event, customer type, membership, channel, age, country, access environment) are not on the screen** Why: The pack's Binding Scope and the write both carry them; without them every rule applies to every ticket. *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#setMediaBindingRule; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Read and write name the same fields differently (allowedMedia vs allowedMediaTypeIds, product vs productId, age vs ageCategory) and the overlay lists id and scopePath as required** Why: The edit form cannot round-trip; align names, and id/scopePath are server-owned (VO-R03). *(source: contracts/spine/access.yaml#/components/schemas/AccessMediaBindingRule; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **exclusiveActivation is a flat list of strings** Why: The pack's rule is directional ("Physical RFID activated, temporary paper credential automatically revoked"); a flat list cannot say which medium revokes which. *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#setMediaBindingRule; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **When more than one binding rule matches a ticket, which wins (most specific scope, or an explicit priority)?** → Drawn default accepted: Draw "Most specific rule wins" as a fixed note and show overlaps on save. *(decided by Chinmay, 2026-10-02; DEC-269 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Allowed media | select field | — | — | — | — | — | — |
| Mandatory media | select field | — | — | — | — | — | — |
| Optional media | select field | — | — | — | — | — | — |
| Maximum active media | select field | — | — | — | — | — | — |
| Minimum media required | select field | — | — | — | — | — | — |
| Primary media | select field | — | — | — | — | — | — |
| Secondary media | select field | — | — | — | — | — | — |
| Backup media | select field | — | — | — | — | — | — |
| Temporary media | select field | — | — | — | — | — | — |
| Media combination | select field | — | — | — | — | — | — |
| Simultaneous activation | select field | — | — | — | — | — | — |
| Exclusive activation | select field | — | — | — | — | — | — |

**Form: Save media binding rule** (modal, opened by *Save media binding rule*; *Save media binding rule* calls `setMediaBindingRule`, *Cancel* sends nothing)

**Collects what `setMediaBindingRule` sends before it is called.** Required: `id`, `scopePath`. Optional: `allowedMediaTypeIds`, `mandatoryMediaTypeIds`, `optionalMediaTypeIds`, `primaryMediaTypeId`, `secondaryMediaTypeIds`, `backupMediaTypeIds`, `temporaryMediaTypeIds`, `minimumMediaRequired`, `maximumActiveMedia`, `mediaCombinations`, `simultaneousActivation`, `exclusiveActivation` and 10 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setMediaBindingRule` body |
| Allowed media types `allowedMediaTypeIds` | multi-picker: choose allowed media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Mandatory media types `mandatoryMediaTypeIds` | multi-picker: choose mandatory media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Optional media types `optionalMediaTypeIds` | multi-picker: choose optional media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Primary media type `primaryMediaTypeId` | picker: choose a primary media type | optional | — | — | shows names, sends the id | — | `setMediaBindingRule` body |
| Secondary media types `secondaryMediaTypeIds` | multi-picker: choose secondary media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Backup media types `backupMediaTypeIds` | multi-picker: choose backup media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Temporary media types `temporaryMediaTypeIds` | multi-picker: choose temporary media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Minimum media required `minimumMediaRequired` | number field | optional | 0 | min 0 | — | — | `setMediaBindingRule` body |
| Maximum active media `maximumActiveMedia` | number field | optional | — | min 1 | — | — | `setMediaBindingRule` body |
| Media combinations `mediaCombinations` | list of values (chips) | optional | — | — | — | Permitted media combinations | `setMediaBindingRule` body |
| Simultaneous activation `simultaneousActivation` | list of values (chips) | optional | — | — | — | Media that may be active at the same time, e.g. | `setMediaBindingRule` body |
| Exclusive activation `exclusiveActivation` | list of values (chips) | optional | — | — | — | Media whose activation revokes another, e.g. | `setMediaBindingRule` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setMediaBindingRule` body |
| Ticket type `ticketType` | text field | optional | — | max length 100 | — | — | `setMediaBindingRule` body |
| Event `eventId` | text field | optional | — | — | — | — | `setMediaBindingRule` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setMediaBindingRule` body |
| Customer type `customerType` | text field | optional | — | max length 100 | — | — | `setMediaBindingRule` body |
| Membership `membership` | text field | optional | — | max length 100 | — | — | `setMediaBindingRule` body |
| Channel `channel` | text field | optional | — | max length 50 | — | — | `setMediaBindingRule` body |
| Age category `ageCategory` | text field | optional | — | max length 50 | — | — | `setMediaBindingRule` body |
| Country `country` | text field | optional | — | max length 2 | — | ISO 3166-1 alpha-2 | `setMediaBindingRule` body |
| Access environment `accessEnvironment` | text field | optional | — | max length 100 | — | — | `setMediaBindingRule` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setMediaBindingRule` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Minimum above maximum, or an unknown media type.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scope (product, ticketType, event, customerType, membership, channel, ageCategory, country, accessEnvironment)**: "Applies to" builder at the top: each condition is a picker from its own list (product from the catalogue, country ISO-2 with flag, age category from the venue's categories); empty = any. Venue comes from the switcher (VO-R09), not a field. Show the most specific rule wins and preview which rule a sample product would match. *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#/components/schemas/AccessMediaBindingRule)*
- **Allowed / mandatory / optional media**: One media grid instead of three selects: a row per media type from BO-337 with a three-way choice Required / Optional / Not allowed. Allowed = Required + Optional, derived, so the three lists can never contradict. *(source: screens/P08-venue-back-office.yaml#BO-338 / contracts/spine/access.yaml#/components/schemas/AccessMediaBindingRule)*
- **Roles (primary, secondary, backup, temporary)**: A role column in the same grid: exactly one Primary (required when any medium is required), then Secondary, Backup, Temporary. Only allowed media can take a role. *(source: contracts/spine/access.yaml#/components/schemas/AccessMediaBindingRule)*
- **minimumMediaRequired / maximumActiveMedia**: Two steppers "At least [1] and at most [3] active media". Minimum 0 allowed (default 0), maximum at least 1; minimum above maximum is refused (422) and shown on the field. *(source: contracts/spine/access.yaml#setMediaBindingRule)*
- **mediaCombinations / simultaneousActivation / exclusiveActivation**: Two small rule lists in the pack's own sentence form: "[Face] and [RFID] may stay active together" and "Activating [RFID wristband] revokes [Temporary paper ticket]". The contract holds them as strings; the UI builds them from media pickers, never free text. *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#/components/schemas/AccessMediaBindingRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save media binding rule (primary button) | `setMediaBindingRule` PUT `/media-binding-rules` | AccessMediaBindingRule | AccessMediaBindingRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Delete media binding rule (destructive button) | `deleteMediaBindingRule` DELETE `/media-binding-rules/{ruleId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rule list**: One line per rule as a sentence ("Waterpark day ticket - RFID wristband required; Mobile QR optional before wristband collection; max 2 active"), with scope chips and the count of tickets currently bound under it. *(source: screens/P08-venue-back-office.yaml#BO-338 / screens/P08-venue-back-office.yaml#BO-339)*
- **Relationship diagram**: "1 Virtual Ticket - 0..N media" drawn once at the top with the VT-009821 example (Dynamic QR, RFID wristband, Apple Wallet, Face). *(source: screens/P08-venue-back-office.yaml#BO-338)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save binding rule**: Whole-rule upsert (VO-R04); a new rule sends no id and the server assigns it (VO-R03). 422 when a named media type does not exist or minimum exceeds maximum. Takes effect at the next binding; media already bound are not re-evaluated, which the confirmation says. *(source: contracts/spine/access.yaml#setMediaBindingRule)*
- **Delete binding rule**: Confirmation (VO-R16): "Media already bound under this rule stay bound; new bindings will use the remaining rules." Names the products the rule covered. *(source: contracts/spine/access.yaml#deleteMediaBindingRule)*

**Data it reads**: `listMultiMediaBinding` (onLoad, Multi-Media Binding & Association Rules)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listMultiMediaBinding`

**What opens over it**

- confirmDialog *Delete media binding rule*: **Names what `deleteMediaBindingRule` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-media binding association configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-media binding association untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-media binding association configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 Minimum above maximum, or an unknown media type. |

#### Edge cases to draw

- **Two rules match the same product with different scopes**: Show which wins (more conditions wins) in the preview; warn on exact duplicates before save. *(source: designer default)*
- **Required medium that the registry marks inactive**: Rule shows a red "Face recognition reference is retired" badge; binding would fail. *(source: contracts/spine/access.yaml#setMediaTypeTechnology)*

#### Consistency with other screens

- Match `BO-341`: Primary / secondary / fallback order configured there must match the roles here; draw both as one editor (VO-R14).
- Match `BO-358`: Binding at the counter reads the matching rule and refuses a medium the rule does not allow or that would exceed the maximum.
- Match `BO-176`: Virtual Credential & Media Association (access board) shows the same association per ticket.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- appliesTo: Product Summit Peaks Annual Pass
  required: Face (primary)
  optional: Mobile QR, RFID card
  min: 1
  max: 3
  together: Face + RFID
- appliesTo: Aqua Park Day Pass
  required: RFID wristband (primary)
  optional: Mobile QR (temporary until collection)
  max: 2
  exclusive: RFID wristband revokes Mobile QR
- appliesTo: Event Summer Concert
  default: Dynamic QR (primary)
  optional: Apple Wallet, Google Wallet
  max: 3
```

#### Permissions

- `listMultiMediaBinding` → `SCOPE_VIEW` (read) · staff
- `setMediaBindingRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `deleteMediaBindingRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*
- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-338` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-338`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 8: Works in Multi-Media Binding & Association Rules → Configure how one Virtual Ticket can be associated with multiple media simultaneously. This is one of the most important screens in Area 15.

#### Acceptance for the design

- [ ] Every input above is drawn (36), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-338?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save media binding rule, Delete media binding rule.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-339` Credential Identity, Token & Reference Mapping

**Define how individual media identifiers resolve securely back to the authoritative Virtual Ticket.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-identity-token-reference-mapping-bo-339` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Shows how every media identifier resolves back to its one authoritative Virtual Ticket - the credential resolver - with the mapping record for each binding (binding id, ticket, media type, reference, token masked, provider reference, dates, status, version, security profile, protection). It is a read and test screen for technical and support staff, not a configuration form. The one thing to get right: sensitive values are never shown in full, and a face binding shows a reference to the biometric service, never biometric data.

**Known correction pending (do not draw the wrong version)**

- **Content region is an empty unbound table, and the gap says the pack gives nothing to draw** Why: The pack lists the mapping record fields and the read returns them; bind listCredentialIdentityToken. *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#listCredentialIdentityToken; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Key references" drawn as the primary button** Why: It is one of the protection methods in the pack's Security list, not an action. *(source: screens/P08-venue-back-office.yaml#BO-339; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Pattern listDetail named a configuration screen ("Define how ... resolve") but nothing configurable exists** Why: The resolver is behaviour; the screen is a read and test view. Say so in the title area ("How media resolve to tickets"). *(source: contracts/spine/access.yaml#listCredentialIdentityToken; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The credential binding list, including token references, needs only SCOPE_VIEW** Why: The pack says sensitive credential values should not be exposed unnecessarily; the resolver mapping should need audit or access-configuration rights, not the scope-view right every back-office user has. *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#listCredentialIdentityToken; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Virtual ticket | text field | — | — | `listCredentialIdentityToken` ?virtualTicketId |
| Media type | text field | — | — | `listCredentialIdentityToken` ?mediaType |
| Credential reference | text field | — | — | `listCredentialIdentityToken` ?credentialReference |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters (virtualTicketId, mediaType, credentialReference)**: Three filters across the top; the list is paged and only loads after one is set or for the last 24 hours, since bindings grow with every ticket. *(source: contracts/spine/access.yaml#listCredentialIdentityToken)*
- **Resolve a credential (test)**: A small "Resolve" box in the pack's form: Media type [RFID] + Credential [04:A2:...] -> "Virtual Ticket VT-009821". Bind it to lookupTicket by mediaCode (read-only, admits nobody); show the ticket, the binding that matched and its status. *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#lookupTicket)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Key references (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Mapping table**: Title "Credential bindings". Columns Binding ID, Virtual Ticket (link to BO-355), Media type, Credential reference, Token (masked, last 4 shown: "****92LD"), Provider reference, Issued, Activated, Expiry, Status (Pending, Active, Suspended, Revoked, Expired), Version, Security profile, Protection (Tokenised / Hashed / Encrypted / Signed / Key reference / Masked as small tags). *(source: screens/P08-venue-back-office.yaml#BO-339 / contracts/spine/access.yaml#/components/schemas/CredentialIdentityTokenReferenceMappingView)*
- **Resolver diagram**: Inputs (QR token, RFID UID, Wallet object, NFC token, Face reference) feeding one resolver that returns the Virtual Ticket ID; static, at the top. *(source: screens/P08-venue-back-office.yaml#BO-339)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Key references**: Not a button: key references are one of the protection methods. Show the key reference id in the detail panel; there is no key-management operation here. *(source: contracts/spine/access.yaml#/components/schemas/CredentialIdentityTokenReferenceMappingView)*
- **Reveal token**: designer default - not offered; the pack says sensitive values should not be exposed in administrative UI or logs. *(source: screens/P08-venue-back-office.yaml#BO-339)*

**Data it reads**: `listCredentialIdentityToken` (onLoad, Credential Identity, Token & Reference Mapping)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listCredentialIdentityToken`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential identity token list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential identity token untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential identity token yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential identity token are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Face binding row**: Token column reads "Biometric service reference" with the provider; no image, no template. *(source: screens/P08-venue-back-office.yaml#BO-339 / ADR-0063)*
- **Credential resolves to nothing**: "No ticket uses this credential" with the media type; never a 404 page. *(source: contracts/spine/access.yaml#lookupTicket)*
- **Credential resolves to a revoked binding**: Show the ticket and "This medium was revoked on 12 Oct 2026 (Lost)"; the resolver still names the ticket for support. *(source: contracts/spine/access.yaml#replaceCredential)*

#### Consistency with other screens

- Match `BO-355`: The 360 workspace's credential wallet shows the same binding id, status and masked reference.
- Match `SCN-009`: The scanner's ticket lookup uses the same lookupTicket resolution.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
bindings:
- binding: CB-55128
  ticket: VT-2026-009821
  media: Dynamic QR
  token: '****92LD'
  provider: TICVAI
  issued: 3 Oct 2026 10:12
  status: Active
  version: 3
  protection: Signed, Masked
- binding: CB-55130
  ticket: VT-2026-009821
  media: RFID wristband
  reference: RF-10452
  token: 04:A2:**:**:7E
  provider: HID
  status: Active
  protection: Hashed, Masked
- binding: CB-55131
  ticket: VT-2026-009821
  media: Face
  token: Biometric service reference
  status: Active
```

#### Permissions

- `listCredentialIdentityToken` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-339` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-339`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 10: Works in Credential Identity, Token & Reference Mapping → Define how individual media identifiers resolve securely back to the authoritative Virtual Ticket.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-339?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Key references.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-340` Entitlement & Cross-Media Synchronization Rules

**Ensure all media attached to a Virtual Ticket share the same authoritative ticket and entitlement state.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/entitlement-cross-media-synchronization-rules-bo-340` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Makes every medium on a ticket share one entitlement and usage state. For each ticket event (entry, exit, redemption, partial consumption, cancellation, refund, suspension, reactivation, transfer, upgrade, expiry, replacement) it sets what happens to the credential and where the change must reach (platform, app, gate network, offline revocation package, wallet service), and which synchronisation failures are watched. The one thing to get right: the pack's principle in words on the screen - a face entry uses the ticket, so QR and RFID then see it used; media never hold their own entitlement.

**Known correction pending (do not draw the wrong version)**

- **The read returns only event, monitored conditions and a note; revocation action and targets are missing** Why: The editor cannot open pre-filled for a whole-row PUT (VO-R04); add revocationAction and propagationTargets to the view. *(source: contracts/spine/access.yaml#/components/schemas/EntitlementCrossMediaSynchronizationRulesView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Event vocabularies differ - the read has 12 events, the write 17 (adds exchange, reissue, manualInvalidation, fraudLock, accountSuspension)** Why: Rules saved for the extra five events would never show in the list. *(source: contracts/spine/access.yaml#listEntitlementCrossMedia / contracts/spine/access.yaml#setCredentialEventPropagationRule; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table bound to one column (monitoredConditions), labels "Every entitlement cross-media synchronization" and "Save credential event propagation rule"** Why: Generated; title "Synchronisation rules", action "Save rule" (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Overlay lists id and scopePath as required** Why: Server-owned; the key is the event (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Form: Save credential event propagation rule** (modal, opened by *Save credential event propagation rule*; *Save credential event propagation rule* calls `setCredentialEventPropagationRule`, *Cancel* sends nothing)

**Collects what `setCredentialEventPropagationRule` sends before it is called.** Required: `id`, `triggerEvent`, `scopePath`. Optional: `revocationAction`, `propagationTargets`, `monitoredConditions`, `propagation`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setCredentialEventPropagationRule` body |
| Trigger event `triggerEvent` | select | required | — | Entry · Exit · Redemption · Partial consumption · Cancellation · Refund · Suspension · Reactivation · Transfer · Exchange · Upgrade · Reissue … | — | Unique per scope; one vocabulary for both screens that read it (decided 29 September, writers pass) | `setCredentialEventPropagationRule` body |
| Revocation action `revocationAction` | segmented control | optional | — | Invalidate · Suspend · Replace | — | What happens to the credential; refund, exchange and reissue always revoke | `setCredentialEventPropagationRule` body |
| Propagation targets `propagationTargets` | multi-select chips | optional | — | Central platform · Mobile app · Gate network · Offline revocation package · Wallet credential service | — | — | `setCredentialEventPropagationRule` body |
| Monitored conditions `monitoredConditions` | multi-select chips | optional | — | Delayed updates · Conflicting states · Offline transactions pending synchronization · Provider update failures · Stale wallet credentials | — | — | `setCredentialEventPropagationRule` body |
| Propagation `propagation` | text area | optional | — | max length 500 | — | How the Virtual Ticket state change reaches every bound medium | `setCredentialEventPropagationRule` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setCredentialEventPropagationRule` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **triggerEvent**: The rows of the screen, one per event, not a free select: Entry, Exit, Redemption, Partial consumption, Cancellation, Refund, Suspension, Reactivation, Transfer, Exchange, Upgrade, Reissue, Expiry, Replacement, Manual invalidation, Fraud lock, Account suspension. *(source: screens/P08-venue-back-office.yaml#BO-340 / contracts/spine/access.yaml#/components/schemas/AccessCredentialEventPropagationRule)*
- **revocationAction**: Invalidate / Suspend / Replace / None (usage events such as Entry change state but revoke nothing). Refund, Exchange and Reissue are locked to a revoking action with "always revokes" beside them. *(source: contracts/spine/access.yaml#setCredentialEventPropagationRule)*
- **propagationTargets**: Five checkboxes in a fixed order - Central platform, Mobile app, Gate network, Offline revocation package, Wallet credential service; Central platform always on and locked. *(source: contracts/spine/access.yaml#/components/schemas/AccessCredentialEventPropagationRule)*
- **monitoredConditions**: Chips - Delayed updates, Conflicting states, Offline transactions pending sync, Provider update failures, Stale wallet credentials. *(source: screens/P08-venue-back-office.yaml#BO-341 / contracts/spine/access.yaml#/components/schemas/AccessCredentialEventPropagationRule)*
- **propagation**: Optional note (max 500) describing how the change reaches each medium; not the place for rules. *(source: contracts/spine/access.yaml#setCredentialEventPropagationRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Every entitlement cross-media synchronization** (data table, from `listEntitlementCrossMedia`)

| Shows | Format | Notes |
|---|---|---|
| Monitored conditions | list or chips (count when long) | Synchronisation problems detected and alerted |

**The selected entitlement cross-media synchronization** (detail panel): The pack groups this record's detail under its own headings: “Critical Principle”, “For example, TICVAI must prevent”, “Instead”, “Face Credential”, “Virtual Ticket resolved”, “Access transaction recorded”.

| Shows | Format | Notes |
|---|---|---|
| Monitored conditions | list or chips (count when long) | Synchronisation problems detected and alerted |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save credential event propagation rule (primary button) | `setCredentialEventPropagationRule` PUT `/credential-event-propagation-rules` | AccessCredentialEventPropagationRule | AccessCredentialEventPropagationRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `ACCESS_POINT_CONFIGURE`; opens modal first; produces a document or message: Set how a ticket lifecycle event propagates to the credential |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Event table**: Title "Synchronisation rules". Columns Event, What happens to media, Reaches (five target icons), Watched for. Events with no rule saved show the platform default greyed with "Default". *(source: contracts/spine/access.yaml#listEntitlementCrossMedia)*
- **Principle and worked example**: A panel "Media do not own entitlement" with the pack's two examples: QR = Used, RFID = Unused, Face = Unused is never three entitlements; and the face-entry sequence (Face credential > Virtual Ticket resolved > access recorded > usage updated > QR/RFID/Wallet see the new state). Below, the partial entitlement example (Annual pass - Main admission, 2 guest admissions, 5 parking uses, 10% F&B) showing remaining rights shared by all media. *(source: screens/P08-venue-back-office.yaml#BO-340 / screens/P08-venue-back-office.yaml#BO-341)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rule**: Whole-row upsert keyed on the event (VO-R04); the edit drawer must open with the stored action and targets, which the read does not return today (see corrections). Confirmation names the media affected ("Applies to 61,340 active tickets' media on their next change"). *(source: contracts/spine/access.yaml#setCredentialEventPropagationRule)*

**Data it reads**: `listEntitlementCrossMedia` (onLoad, Entitlement & Cross-Media Synchronization Rules)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listEntitlementCrossMedia`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entitlement cross-media synchronization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entitlement cross-media synchronization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entitlement cross-media synchronization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entitlement cross-media synchronization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Gate offline when a cancellation happens**: Show that the change reaches that gate with its next offline revocation package, with the package age (VO-R07). *(source: contracts/spine/access.yaml#/components/schemas/AccessCredentialEventPropagationRule)*
- **Wallet provider does not support revocation**: "Wallet updated where supported" note, with the registry capability from BO-337. *(source: screens/P08-venue-back-office.yaml#BO-337 / contracts/spine/access.yaml#listMediaTypeCredential)*

#### Consistency with other screens

- Match `BO-170`: Credential Revocation & Lifecycle Events (access board) writes the same rows with the same write; the two must be one screen (VO-R14), keeping this event list.
- Match `BO-336`: The propagation summary shown on the lifecycle screen comes from here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- event: Entry
  media: Usage updated, no revocation
  reaches: Platform, Gate network, App
- event: Cancellation
  media: Invalidate
  reaches: Platform, App, Gate network, Offline package, Wallet service
  watched: Delayed updates, Stale wallet credentials
- event: Refund
  media: Invalidate (always)
  reaches: All five
- event: Replacement
  media: Replace (old medium revoked)
  reaches: Platform, Gate network, Offline package
```

#### Permissions

- `listEntitlementCrossMedia` → `SCOPE_VIEW` (read) · staff
- `setCredentialEventPropagationRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-340` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-340`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 12: Works in Entitlement & Cross-Media Synchronization Rules → Ensure all media attached to a Virtual Ticket share the same authoritative ticket and entitlement state.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-340?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save credential event propagation rule.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-341` Media Activation, Priority & Fallback Rules

**Configure when each credential becomes active and how alternative media behave if the preferred credential cannot be used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-activation-priority-fallback-rules-bo-341` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Sets, per media type, when each medium becomes active (on issuance, ticket activation, download, wallet installation, RFID assignment, face enrolment, first use, event date, manually or on a schedule), the priority order at the gate (for example Face, then RFID, then Dynamic QR) and how temporary credentials behave when the preferred medium cannot be used. The one thing to get right: a fallback is the same ticket presented another way - the screen must never suggest that a backup medium carries extra entries.

**Known correction pending (do not draw the wrong version)**

- **Read-only screen with no write** Why: The pack says "Configure"; listMediaActivationPriority has no matching set operation, so nothing can be saved. *(source: screens/P08-venue-back-office.yaml#BO-341 / contracts/spine/access.yaml#listMediaActivationPriority; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Activation moments drawn as four action buttons and temporary-credential settings as six empty selects** Why: Values of activationTrigger and typed fields (duration, two booleans, two closed sets). *(source: contracts/spine/access.yaml#/components/schemas/MediaActivationPriorityFallbackRulesView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **replacementBehavior, originalMediaImpact and validityDuration are free strings** Why: They decide what a gate does; they need closed sets (and a duration type) to be enforced. *(source: contracts/spine/access.yaml#/components/schemas/MediaActivationPriorityFallbackRulesView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Temporary media | select field | — | — | — | — | — | — |
| Validity duration | select field | — | — | — | — | — | — |
| One-time use | select field | — | — | — | — | — | — |
| Automatic expiration | select field | — | — | — | — | — | — |
| Replacement behavior | select field | — | — | — | — | — | — |
| Original-media impact | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **activationTrigger**: One choice per media type from the ten activation moments, drawn as a table row per medium (Medium / Becomes active / Fallback to). Scheduled activation reveals a date-time; On event date shows "at gate opening time of the performance" (from the admission profile). The four generated action buttons ("On ticket activation", "On download", "On wallet installation", "On event date") are values of this choice, not actions. *(source: screens/P08-venue-back-office.yaml#BO-341 / contracts/spine/access.yaml#/components/schemas/MediaActivationPriorityFallbackRulesView)*
- **Priority and fallbackMediaTypes**: A drag-ordered list Primary > Secondary > Fallback (pack example Face recognition > RFID > Dynamic QR), from the media allowed by the binding rule; under it the pack's fallback scenarios as plain sentences generated from the order ("Face recognition unavailable - use RFID"; "RFID lost - use Mobile QR"; "Customer phone unavailable - issue temporary physical credential"). *(source: screens/P08-venue-back-office.yaml#BO-341 / screens/P08-venue-back-office.yaml#BO-342 / DI-608)*
- **Temporary credential (temporaryMedia, validityDuration, oneTimeUse, automaticExpiration, replacementBehavior …**: A "Temporary credential" group shown only for media marked temporary: validity as a number + unit (minutes, hours, until end of day), One-time use toggle, Expires automatically toggle (default on), Replacement behaviour select (Revoked when the permanent medium is bound / Kept until it expires), Original medium select (Stays active / Suspended while temporary is active / Revoked). Not free text. *(source: screens/P08-venue-back-office.yaml#BO-342 / contracts/spine/access.yaml#/components/schemas/MediaActivationPriorityFallbackRulesView)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| On ticket activation (primary button) | navigation or local | — | — | — | — |
| On download (secondary button) | navigation or local | — | — | — | — |
| On wallet installation (secondary button) | navigation or local | — | — | — | — |
| On event date (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Activation table**: One row per media type with its trigger, priority position, fallback chain and a temporary badge; a timeline strip under it shows a sample ticket's media lighting up (QR at issuance, Wallet on installation, RFID at collection). *(source: contracts/spine/access.yaml#listMediaActivationPriority / designer default)*
- **Same-ticket statement**: "These media do not represent different tickets - they all resolve to the same Virtual Ticket." printed under the priority list. *(source: screens/P08-venue-back-office.yaml#BO-342)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save activation rules**: No write exists; draw Save disabled with "Not available yet" and raise it. When added, a whole-row upsert per media type (VO-R04). *(source: contracts/spine/access.yaml#listMediaActivationPriority)*

**Data it reads**: `listMediaActivationPriority` (onLoad, Media Activation, Priority & Fallback Rules)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listMediaActivationPriority`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media activation priority configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media activation priority untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media activation priority configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Activation trigger needs a medium the binding rule does not allow**: Row shows a warning linking to BO-338. *(source: contracts/spine/access.yaml#setMediaBindingRule)*
- **Dynamic QR on a dynamic-QR event bought on the web**: Trigger is fixed to activation in the app (the web redirects), shown locked with the reason. *(source: DI-635)*

#### Consistency with other screens

- Match `BO-338`: Roles there and priority here are the same idea; one editor with two sections (VO-R14).
- Match `BO-166`: Credential activation and display rules (beacon/geofence, time before admission) govern when the guest sees the code; activation here governs when it is valid.
- Match `GST-055`: The guest's "Your code appears when you reach the gates" state follows these rules.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- medium: Face recognition
  active: On face enrolment
  priority: Primary
  fallback: RFID wristband
- medium: RFID wristband
  active: On RFID assignment
  priority: Secondary
  fallback: Dynamic QR
- medium: Dynamic QR
  active: Immediate on issuance
  priority: Fallback
- medium: Paper day pass (temporary)
  active: Immediate on issuance
  temporary: Valid 4 hours, one-time use, expires automatically, revoked when RFID is bound
```

#### Permissions

- `listMediaActivationPriority` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-341` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-341`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 14: Works in Media Activation, Priority & Fallback Rules → Configure when each credential becomes active and how alternative media behave if the preferred credential cannot be used.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-341?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: On ticket activation, On download, On wallet installation, On event date.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-342` Media Replacement, Revocation & Rebinding Rules

**Configure controlled handling of lost, stolen, damaged, compromised or replaced credential media.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-replacement-revocation-rebinding-rules-bo-342` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The policy for lost, stolen, damaged, compromised or replaced media: for each replacement reason, whether reissue is allowed, how many times, the fee, whether approval, identity check or a supervisor is needed, whether the old medium is revoked at once or after a grace period, and whether both may work during it. The counter workflow (BO-359) reads these rules. The one thing to get right: one policy row per reason, and replacing a medium never replaces the ticket (VT-009821 stays; RFID-88721 revoked, RFID-99211 active).

**Known correction pending (do not draw the wrong version)**

- **Suspend Media, Revoke Media and Replace Media buttons (with confirm dialogs) on a policy screen** Why: They act on a guest's credential, not on the policy, and have no operation here. Replace is replaceCredential on BO-359; suspension follows an identity lock (lockIdentity on BO-247, lock scope "medium only"); revoke-without-replace has no operation. *(source: contracts/spine/access.yaml#listMediaReplacementRevocation / contracts/spine/access.yaml#lockIdentity / contracts/spine/access.yaml#replaceCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Wallet credential replacement" and "Printed ticket replacement" drawn as buttons** Why: They are pack scenarios (reasons). "New mobile device" maps to customerChangedPhone, but "Printed ticket replacement" has no reason value in the enum. *(source: screens/P08-venue-back-office.yaml#BO-342 / contracts/spine/access.yaml#setMediaReplacementRevocation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Old media automatically revoked" is a textField and the other booleans are selects** Why: Toggles; grace period is a duration control. *(source: contracts/spine/access.yaml#/components/schemas/MediaReplacementRevocationRebindingRulesInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Save replacement rule has no permission on the screen** Why: The write needs ACCESS_POINT_CONFIGURE; show it disabled for others (VO-R08). *(source: contracts/spine/access.yaml#setMediaReplacementRevocation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's "Printed ticket replacement" scenario has no replacementReason value** Why: The reason enum has eleven values and none for a printed ticket; either add it or route printed tickets to the reprint flow (ORDER_REPRINT) and say so on the screen. *(source: screens/P08-venue-back-office.yaml#BO-342 / contracts/spine/access.yaml#setMediaReplacementRevocation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "Printed ticket replacement" a reason of its own (reprint) or the Damaged / Lost reason applied to paper?** → Drawn default accepted: Treat a reprint as Damaged with media type Printed ticket; flag the missing reason. *(decided by Chinmay, 2026-10-02; DEC-270 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Reissue allowed | select field | — | — | — | — | — | — |
| Number of replacements | select field | — | — | — | — | — | — |
| Replacement fee reference | select field | — | — | — | — | — | — |
| Approval required | select field | — | — | — | — | — | — |
| Identity verification | select field | — | — | — | — | — | — |
| Old media automatically revoked | text field | — | — | — | — | — | — |
| Grace period | select field | — | — | — | — | — | — |
| Simultaneous media policy | select field | — | — | — | — | — | — |
| Reason mandatory | select field | — | — | — | — | — | — |
| Supervisor approval | select field | — | — | — | — | — | — |

**Sent by *Save replacement rule*** (`setMediaReplacementRevocation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Replacement reason `replacementReason` | select | required | — | Lost · Stolen · Damaged · Compromised · Customer changed phone · RFID failure · Wristband replacement · QR compromise · Wallet replacement · Face re enrollment · Incorrect assignment | — | The reason this rule is for, in the vocabulary of `replaceCredential`, so the rule a replacement reads is keyed the way the replacement names it (decided 29 September, writers … | `setMediaReplacementRevocation` body |
| Outcome `outcome` | radio group | required | — | Replace · Rebind · Suspend media · Revoke media | — | What happens to the media | `setMediaReplacementRevocation` body |
| Number of replacements `numberOfReplacements` | number field | optional | — | min 0 | — | Maximum replacements per credential | `setMediaReplacementRevocation` body |
| Replacement fee reference `replacementFeeReference` | text field | optional | — | — | — | Catalogue product charged for the replacement; empty is free | `setMediaReplacementRevocation` body |
| Approval required `approvalRequired` | toggle | optional | off | — | — | — | `setMediaReplacementRevocation` body |
| Supervisor approval `supervisorApproval` | toggle | optional | off | — | — | — | `setMediaReplacementRevocation` body |
| Identity verification `identityVerification` | toggle | optional | on | — | — | — | `setMediaReplacementRevocation` body |
| Old media automatically revoked `oldMediaAutomaticallyRevoked` | toggle | optional | on | — | — | — | `setMediaReplacementRevocation` body |
| Grace period `gracePeriod` | text field | optional | — | — | — | ISO 8601 duration the old media stays valid; empty is none | `setMediaReplacementRevocation` body |
| Simultaneous media policy `simultaneousMediaPolicy` | segmented control | optional | One active | One active · Allow both during grace | — | — | `setMediaReplacementRevocation` body |
| Reason mandatory `reasonMandatory` | toggle | optional | on | — | — | — | `setMediaReplacementRevocation` body |
| Reissue allowed `reissueAllowed` | toggle | optional | on | — | — | — | `setMediaReplacementRevocation` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **replacementReason**: The rows of the screen (one policy per reason): Lost, Stolen, Damaged, Compromised, Customer changed phone, RFID failure, Wristband replacement, QR compromise, Wallet replacement, Face re-enrolment, Incorrect assignment. Picked from a list, keyed, not typed. *(source: screens/P08-venue-back-office.yaml#BO-342 / contracts/spine/access.yaml#setMediaReplacementRevocation)*
- **outcome**: Four cards - Replace, Rebind, Suspend medium, Revoke medium - with one line each on what the guest experiences. *(source: contracts/spine/access.yaml#/components/schemas/MediaReplacementRevocationRebindingRulesInput)*
- **numberOfReplacements / replacementFeeReference**: "Up to [2] replacements per credential" (0 = not allowed, empty = no limit); fee is a pick of a catalogue product with its price shown ("Wristband replacement fee - AED 25.00"), empty = free. Never an amount typed here. *(source: screens/P08-venue-back-office.yaml#BO-360 / contracts/spine/access.yaml#/components/schemas/MediaReplacementRevocationRebindingRulesInput)*
- **approvalRequired / supervisorApproval / identityVerification / reasonMandatory / reissueAllowed**: Five toggles with the contract defaults (approval off, supervisor off, identity check on, reason on, reissue on). *(source: contracts/spine/access.yaml#/components/schemas/MediaReplacementRevocationRebindingRulesInput)*
- **oldMediaAutomaticallyRevoked / gracePeriod / simultaneousMediaPolicy**: "Old medium" group: Revoke at once (default) or Keep working for [n] minutes/hours (grace period, stored as ISO 8601, typed as number + unit); "During the grace period" One active only / Both work. "Both work" is only offered with a grace period. For Lost and Stolen, warn when a grace period is set (the pack's own AI example: old RFID left active 30 minutes conflicts with the lost-credential policy). *(source: screens/P08-venue-back-office.yaml#BO-343 / contracts/spine/access.yaml#/components/schemas/MediaReplacementRevocationRebindingRulesInput)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Wallet credential replacement (primary button) | navigation or local | — | — | — | — |
| Printed ticket replacement (secondary button) | navigation or local | — | — | — | — |
| Suspend Media (destructive button) | navigation or local | — | — | — | — |
| Revoke Media (destructive button) | navigation or local | — | — | — | — |
| Replace Media (secondary button) | navigation or local | — | — | — | — |
| Save replacement rule (primary button) | `setMediaReplacementRevocation` PUT `/media-replacement-revocation` | MediaReplacementRevocationRebindingRulesInput | MediaReplacementRevocationRebindingRulesView | 422 replacementFeeReference names no catalogue product | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Policy table**: Title "Replacement rules". One row per reason - Outcome, Limit, Fee, Checks (icons for identity, approval, supervisor), Old medium ("Revoked at once" / "Works 30 min"). Reasons with no saved rule show defaults greyed. *(source: contracts/spine/access.yaml#listMediaReplacementRevocation)*
- **Continuity example**: The pack's before/after panel - VT-009821 ACTIVE; RFID-88721 REVOKED; RFID-99211 ACTIVE - so the policy is read in terms of one ticket. *(source: screens/P08-venue-back-office.yaml#BO-342 / screens/P08-venue-back-office.yaml#BO-343)*
- **What every change records**: Static note listing the audit fields (old binding, new binding, user, date-time, reason, approval, related transaction), with "See evidence" linking to BO-362. *(source: screens/P08-venue-back-office.yaml#BO-343)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save replacement rule**: Whole-row upsert keyed by reason (VO-R04); 422 on contradictions (both-work without grace period) shown on the field. Applies to replacements started after saving. *(source: contracts/spine/access.yaml#setMediaReplacementRevocation)*

**Data it reads**: `listMediaReplacementRevocation` (onLoad, Media Replacement, Revocation & Rebinding Rules)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listMediaReplacementRevocation`

**What opens over it**

- confirmDialog *Suspend Media*: **Suspend Media on a media replacement revocation is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Revoke Media*: **Revoke Media on a media replacement revocation is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media replacement revocation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media replacement revocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media replacement revocation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 replacementFeeReference names no catalogue product |

#### Edge cases to draw

- **Limit lowered below what some credentials already used**: Confirmation says "14 credentials have already reached 2 replacements; their next replacement will be refused." *(source: contracts/spine/access.yaml#replaceCredential)*
- **Viewer without access configuration rights**: Read-only table, Save disabled with the reason (VO-R08). *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-359`: The counter workflow shows the same rule (limit, fee, checks, grace period) read-only before it replaces.
- Match `BO-179`: Media Swap & Replacement (access board) is the zero-value swap of DI-637; same continuity wording.
- Match `BO-027`: Reissue & Media Replacement (orders board) reads the same policy rows; one source of truth.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- reason: Lost
  outcome: Replace
  limit: 2
  fee: Wristband replacement - AED 25.00
  identity: true
  approval: false
  oldMedium: Revoked at once
- reason: Stolen
  outcome: Revoke medium
  limit: 2
  fee: Free
  identity: true
  supervisor: true
  oldMedium: Revoked at once
- reason: Customer changed phone
  outcome: Rebind
  limit: 3
  fee: Free
  identity: true
  oldMedium: Works 15 min, one active only
- reason: Damaged
  outcome: Replace
  limit: 2
  fee: Free
  identity: false
  oldMedium: Revoked at once
```

#### Permissions

- `listMediaReplacementRevocation` → `SCOPE_VIEW` (read) · staff
- `setMediaReplacementRevocation` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-342` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-342`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 16: Works in Media Replacement, Revocation & Rebinding Rules → Configure controlled handling of lost, stolen, damaged, compromised or replaced credential media.

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-342?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Wallet credential replacement, Printed ticket replacement, Suspend Media, Revoke Media, Replace Media, Save replacement rule.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-343` Virtual Ticket Architecture Testing, Governance & Audit

**Provide the final testing and governance environment for Virtual Ticket and multi-media configurations. Board 1 established what the Virtual Ticket is and how multiple credentials can point to the same authoritative ticket. Board 2 defines how each media type is created, designed, configured, branded, populated with data, previewed, tested and published.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration Simulator; Configuration Owner; AI Configuration Review) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/virtual-ticket-architecture-testing-governance-audit-bo-343` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The test-and-govern gate of the Virtual Ticket board: simulate scenarios (VIP ticket with QR + Apple Wallet; annual pass with Face + RFID + Mobile QR; waterpark with Mobile QR before arrival and RFID after check-in), run a ticket lifecycle across media, inject failures, run automatic architecture checks, send the configuration through review and approval, and read the complete audit trail of configuration and binding changes. The one thing to get right: simulation lives inside this screen and never touches live tickets, and every check result names the screen that fixes it.

**Known correction pending (do not draw the wrong version)**

- **Pack approval stages became selectFields ("Technical Review", "Operations Review", "Approval", "Publication") and pack sentences became textFields (for example "configured lost-credential security policy." and "Preview → Validate → Approve & Publish")** Why: Approval stages are a route, and the text fields are fragments of the pack's prose (one is the Board 2 introduction); none are inputs. *(source: screens/P08-venue-back-office.yaml#BO-343; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Simulation and automatic checks have no operation; only the audit list is bound** Why: The pack's core of this screen is test and validate; without operations it is an audit viewer. *(source: contracts/spine/access.yaml#listVirtualTicketArchitecture; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation has no transition back to BO-334** Why: Board screens return to their hub (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-343; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Purpose carries Board 2's objective text** Why: Pack prose from the following pages ("Board 2 defines how each media type is created ...") leaked into the screen's purpose. *(source: screens/P08-venue-back-office.yaml#BO-344 / screens/P08-venue-back-office.yaml#BO-343; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| → Technical Review | select field | — | — | — | — | — | — |
| → Security Review where applicable | text field | — | — | — | — | — | — |
| → Operations Review | select field | — | — | — | — | — | — |
| → Approval | select field | — | — | — | — | — | — |
| → Publication | select field | — | — | — | — | — | — |
| configured lost-credential security policy.” | text field | — | — | — | — | — | — |
| Replacement/Rebinding → Test & Govern | text field | — | — | — | — | — | — |
| Multi-Format Ticket Media Design Studio—including dedicated design/configuration | text field | — | — | — | — | — | — |
| Preview → Validate → Approve & Publish | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Change type | text field | — | — | `listVirtualTicketArchitecture` ?changeType |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scenario**: Pick a product (or one of the three saved pack scenarios) and the media it would carry; then a step player for the lifecycle (Ticket created > QR generated > RFID bound > Face enrolled > Entry via face > Ticket state updated > RFID presented > same entitlement evaluated) where each step shows the ticket state and every medium's state side by side. *(source: screens/P08-venue-back-office.yaml#BO-343)*
- **Failure to inject**: Chips - Lost RFID, Revoked QR, Expired wallet token, Face unavailable, Offline device, Duplicate credential presentation, Synchronisation failure, Provider outage, Credential binding conflict; the result shows which fallback took over (from BO-341) or the denial in VO-R06 words. *(source: screens/P08-venue-back-office.yaml#BO-343)*
- **Audit filter (changeType)**: Chips - Configuration change, Media binding, Rebinding, Activation, Suspension, Revocation, Replacement, Resolver change, Rule change, Approval; plus a date range. *(source: contracts/spine/access.yaml#/components/schemas/VirtualTicketArchitectureTestingGovernanceAuditView)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Architecture validation**: A checklist with pass / warning / fail and a count, each linking to the screen that fixes it - Media without resolver configuration (BO-339), Invalid media combinations (BO-338), Missing security profile (BO-337), Missing fallback (BO-341), Conflicting activation rules (BO-341), Excessive active credentials (BO-338), Broken provider integration (BO-337), Invalid lifecycle dependencies (BO-336). *(source: screens/P08-venue-back-office.yaml#BO-343)*
- **Approval route**: A rail Configuration owner > Technical review > Security review (where applicable) > Operations review > Approval > Publication, with the current stage and who holds it. *(source: screens/P08-venue-back-office.yaml#BO-343 / contracts/spine/approvals.yaml#createApprovalRequest)*
- **Audit trail**: Title "Configuration and binding history". Columns Change type, Actor (name, never a principal id), When (venue time), Before, After (shown as a two-column diff on selection). Newest first, cursor paging (VO-R12). *(source: contracts/spine/access.yaml#listVirtualTicketArchitecture)*
- **AI configuration review**: Advisory findings in the pack's style ("RFID replacement leaves the old RFID active for 30 minutes; this conflicts with the lost-credential policy") with Open the rule; never auto-fixed (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-343)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Run simulation / Run checks**: No operation exists; draw both and mark "Not available yet", per the contract's own note. *(source: contracts/spine/access.yaml#listVirtualTicketArchitecture)*
- **Submit for approval**: Raises an approval request naming the configuration changes since the last publication; the requester cannot approve their own. *(source: contracts/spine/approvals.yaml#createApprovalRequest / contracts/spine/approvals.yaml#decideApprovalRequest)*

**Data it reads**: `listVirtualTicketArchitecture` (onLoad, Virtual Ticket Architecture Testing, Governance & Audit)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket architecture configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket architecture untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket architecture configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **User without AUDIT_VIEW**: The audit tab says "Needs audit rights" (VO-R08); simulation and checks stay usable. *(source: contracts/spine/access.yaml#listVirtualTicketArchitecture)*
- **A check fails while an approval is in flight**: The approval rail shows a red marker "Configuration changed after submission" on the stage. *(source: designer default)*

#### Consistency with other screens

- Match `BO-163`: The access rule simulation tool (virtual scan, DI-629) and this simulator should share the step-player component and result wording.
- Match `BO-353`: Board 2's preview/approval gate uses the same approval rail.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
checks:
  passed: 6
  warnings: 1
  failed: 1
  failedItem: Missing fallback - Summit Peaks Annual Pass has Face only
  warning: Lost RFID grace period 30 min
audit:
- type: Rule change
  actor: Fatima Al Hashimi
  when: 29 Sep 2026 16:40
  before: Lost - grace 30 min
  after: Lost - revoked at once
- type: Rebinding
  actor: Rahul Menon
  when: 30 Sep 2026 11:02
  before: RF-88721 on VT-2026-009821
  after: RF-99211 on VT-2026-009821
```

#### Permissions

- `listVirtualTicketArchitecture` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-343` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-343`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 18: Works in Virtual Ticket Architecture Testing, Governance & Audit → Provide the final testing and governance environment for Virtual Ticket and multi-media configurations. Board 1 established what the Virtual Ticket is and how multiple credentials can point to the …

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-343?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AUDIT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"deleteMediaBindingRule": {"method":"DELETE","path":"/media-binding-rules/{ruleId}","contract":"access","summary":"Delete a multi-media binding rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listCredentialIdentityToken": {"method":"GET","path":"/credential-identity-token","contract":"access","summary":"Credential Identity, Token & Reference Mapping","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"virtualTicketId","in":"query","required":false},{"name":"mediaType","in":"query","required":false},{"name":"credentialReference","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEntitlementCrossMedia": {"method":"GET","path":"/entitlement-cross-media","contract":"access","summary":"Entitlement & Cross-Media Synchronization Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EntitlementCrossMediaSynchronizationRulesView"},
"listMediaActivationPriority": {"method":"GET","path":"/media-activation-priority","contract":"access","summary":"Media Activation, Priority & Fallback Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaActivationPriorityFallbackRulesView"},
"listMediaReplacementRevocation": {"method":"GET","path":"/media-replacement-revocation","contract":"access","summary":"Media Replacement, Revocation & Rebinding Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaReplacementRevocationRebindingRulesView"},
"listMediaTypeCredential": {"method":"GET","path":"/media-type-credential","contract":"access","summary":"Media Type & Credential Technology Registry","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaTypeCredentialTechnologyRegistryView"},
"listMediaTypeTechnology": {"method":"GET","path":"/media-type-technology","contract":"access","summary":"Media Type & Technology Library","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaTypeTechnologyLibraryView"},
"listMultiMediaBinding": {"method":"GET","path":"/multi-media-binding","contract":"access","summary":"Multi-Media Binding & Association Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MultiMediaBindingAssociationRulesView"},
"listVirtualTicket": {"method":"GET","path":"/virtual-ticket","contract":"access","summary":"Virtual Ticket Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customer","in":"query","required":false},{"name":"virtualTicketStatus","in":"query","required":false},{"name":"mediaType","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"numberOfMedia","in":"query","required":false},{"name":"validity","in":"query","required":false},{"name":"usageStatus","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVirtualTicketArchitecture": {"method":"GET","path":"/virtual-ticket-architecture","contract":"access","summary":"Virtual Ticket Architecture Testing, Governance & Audit","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"changeType","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVirtualTicketStatus": {"method":"GET","path":"/virtual-ticket-statu","contract":"access","summary":"Virtual Ticket Status & Lifecycle Model","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VirtualTicketStatusLifecycleModelView"},
"setCredentialEventPropagationRule": {"method":"PUT","path":"/credential-event-propagation-rules","contract":"access","summary":"Set how a ticket lifecycle event propagates to the credential","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessCredentialEventPropagationRule","responds":"AccessCredentialEventPropagationRule"},
"setMediaBindingRule": {"method":"PUT","path":"/media-binding-rules","contract":"access","summary":"Create or replace a multi-media binding rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessMediaBindingRule","responds":"AccessMediaBindingRule"},
"setMediaReplacementRevocation": {"method":"PUT","path":"/media-replacement-revocation","contract":"access","summary":"Save a media replacement rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaReplacementRevocationRebindingRulesInput","responds":"MediaReplacementRevocationRebindingRulesView"},
"setTicketStatusTransition": {"method":"PUT","path":"/ticket-status-transitions","contract":"access","summary":"Set a Virtual Ticket status transition rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessTicketStatusTransition","responds":"AccessTicketStatusTransition"},
"setVirtualTicketIdentity": {"method":"PUT","path":"/virtual-ticket-identity","contract":"access","summary":"Virtual Ticket Identity & Master Record Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VirtualTicketIdentityMasterRecordConfigurationInput","responds":"VirtualTicketIdentityMasterRecordConfigurationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCredentialEventPropagationRule": {"type":"object","x-ticvai-persistence":"access.credential_event_propagation_rule","description":"For one ticket lifecycle event, the revocation action on the credential and how the change propagates to every bound medium, with the conditions monitored (declared 29 September, data-model close-out DM1).","required":["id","triggerEvent","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"triggerEvent":{"type":"string","enum":["entry","exit","redemption","partialConsumption","cancellation","refund","suspension","reactivation","transfer","exchange","upgrade","reissue","expiry","replacement","manualInvalidation","fraudLock","accountSuspension"],"description":"Unique per scope; one vocabulary for both screens that read it (decided 29 September, writers pass)"},"revocationAction":{"type":"string","nullable":true,"enum":["invalidate","suspend","replace"],"description":"What happens to the credential; refund, exchange and reissue always revoke"},"propagationTargets":{"type":"array","items":{"type":"string","enum":["centralPlatform","mobileApp","gateNetwork","offlineRevocationPackage","walletCredentialService"]}},"monitoredConditions":{"type":"array","items":{"type":"string","enum":["delayedUpdates","conflictingStates","offlineTransactionsPendingSynchronization","providerUpdateFailures","staleWalletCredentials"]}},"propagation":{"type":"string","maxLength":500,"nullable":true,"description":"How the Virtual Ticket state change reaches every bound medium"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessMediaBindingRule": {"type":"object","x-ticvai-persistence":"access.media_binding_rule","description":"One multi-media binding rule - which media a Virtual Ticket may, must or may optionally carry, in which roles and combinations - for the scope named by its conditions (declared 29 September, data-model close-out DM1).","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"allowedMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"mandatoryMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"optionalMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"primaryMediaTypeId":{"type":"string","format":"uuid","nullable":true},"secondaryMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"backupMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"temporaryMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minimumMediaRequired":{"type":"integer","minimum":0,"default":0},"maximumActiveMedia":{"type":"integer","minimum":1,"nullable":true},"mediaCombinations":{"type":"array","items":{"type":"string"},"description":"Permitted media combinations"},"simultaneousActivation":{"type":"array","items":{"type":"string"},"description":"Media that may be active at the same time, e.g. face with RFID"},"exclusiveActivation":{"type":"array","items":{"type":"string"},"description":"Media whose activation revokes another, e.g. RFID activated revokes temporary paper"},"productId":{"type":"string","format":"uuid","nullable":true},"ticketType":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"customerType":{"type":"string","maxLength":100,"nullable":true},"membership":{"type":"string","maxLength":100,"nullable":true},"channel":{"type":"string","maxLength":50,"nullable":true},"ageCategory":{"type":"string","maxLength":50,"nullable":true},"country":{"type":"string","maxLength":2,"nullable":true,"description":"ISO 3166-1 alpha-2"},"accessEnvironment":{"type":"string","maxLength":100,"nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessTicketStatusTransition": {"type":"object","x-ticvai-persistence":"access.ticket_status_transition","description":"One Virtual Ticket lifecycle transition rule - from status, to status, whether allowed, whether it needs an authorised exception and where it may originate (declared 29 September, data-model close-out DM1). Seeded from states/entitlement-status.yaml when a venue is created; setTicketStatusTransition may narrow a move, never add one (decided 29 September, writers pass).\n\n**The 13 names are the client's, mapped onto the entitlement model** (decided 2 October 2026, Chinmay, critical set 2, BO-336; DEC-266; CHG-CSP-033): created and pendingFulfillment (Reserved, DI-670) are the order before an entitlement is issued; active is `issued`; partiallyUsed and used are `partiallyConsumed` and `fullyConsumed`; expired is `expired`; suspended is `issued` with the suspended flag; blocked is `issued` under an active identity lock; cancelled, voided, refunded and reissuedSuperseded are `cancelled` told apart by `Entitlement.cancellationKind`; transferred is `surrendered`. Every name maps, so no state was added to the model; a cell with no model transition behind it is locked \"Not in the platform lifecycle\". `Entitlement.lifecycleLabel` carries the name.\n","required":["id","fromStatus","toStatus","allowed","requiresAuthorizedException","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"fromStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"]},"toStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"Unique with fromStatus per scope"},"allowed":{"type":"boolean"},"requiresAuthorizedException":{"type":"boolean","default":false,"description":"Allowed only with an authorised exception, e.g. used to active"},"originatingSources":{"type":"array","items":{"type":"string","enum":["orderManagement","cancellation","refund","upgradeConversion","ticketTransfer","membership","expiry","accessUsage","authorizedOperator","api","scheduledProcess"]}},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CredentialIdentityTokenReferenceMappingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Identity, Token & Reference Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialBindingId":{"type":"string","description":"Credential Binding ID"},"virtualTicketId":{"type":"string","description":"Virtual Ticket ID"},"mediaType":{"type":"string","description":"Media Type"},"credentialReference":{"type":"string","description":"Credential Reference"},"tokenIdentifier":{"type":"string","description":"Token or identifier, masked in administrative views"},"providerReference":{"type":"string","description":"Provider Reference"},"issuedDate":{"type":"string","format":"date-time","description":"Issued Date"},"activationDate":{"type":"string","format":"date-time","description":"Activation Date"},"expiry":{"type":"string","format":"date-time","description":"Expiry"},"status":{"type":"string","enum":["pending","active","suspended","revoked","expired"],"description":"Credential binding status"},"version":{"type":"string","description":"Version"},"securityProfile":{"type":"string","description":"Security profile"},"protectionMethods":{"type":"array","items":{"type":"string","enum":["tokenization","hashing","encryption","signedPayloads","keyReferences","masking"]},"description":"How the credential value is protected"}},"required":["credentialBindingId","virtualTicketId","mediaType"]},
"EntitlementCrossMediaSynchronizationRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Entitlement & Cross-Media Synchronization Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"triggerEvent":{"type":"string","enum":["entry","exit","redemption","partialConsumption","cancellation","refund","suspension","reactivation","transfer","upgrade","expiry","replacement"],"description":"Ticket event this synchronisation rule handles"},"monitoredConditions":{"type":"array","items":{"type":"string","enum":["delayedUpdates","conflictingStates","offlineTransactionsPendingSynchronization","providerUpdateFailures","staleWalletCredentials"]},"description":"Synchronisation problems detected and alerted"},"propagation":{"type":"string","description":"How the Virtual Ticket state change reaches every bound medium"}},"required":["triggerEvent"]},
"MediaActivationPriorityFallbackRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Activation, Priority & Fallback Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"mediaTypeId":{"type":"string","description":"Media type this rule applies to"},"activationTrigger":{"type":"string","enum":["immediateOnIssuance","onTicketActivation","onDownload","onWalletInstallation","onRfidAssignment","onFaceEnrollment","onFirstUse","onEventDate","manualActivation","scheduledActivation"],"description":"When this medium becomes active"},"temporaryMedia":{"type":"boolean","description":"Temporary media"},"validityDuration":{"type":"string","description":"ISO 8601 duration, e.g. PT30M"},"oneTimeUse":{"type":"boolean","description":"One-time use"},"automaticExpiration":{"type":"boolean","description":"Automatic expiration"},"replacementBehavior":{"type":"string","description":"Replacement behavior"},"originalMediaImpact":{"type":"string","description":"Original-media impact"},"fallbackMediaTypes":{"type":"array","items":{"type":"string"},"description":"Ordered media to use if this one cannot be used, e.g. face unavailable then RFID"}},"required":["mediaTypeId","activationTrigger"]},
"MediaReplacementRevocationRebindingRulesInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Media Replacement, Revocation & Rebinding Rules submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["replacementReason","outcome"],"properties":{"replacementReason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"],"description":"The reason this rule is for, in the vocabulary of `replaceCredential`, so the rule a replacement reads is keyed the way the replacement names it (decided 29 September, writers pass). The old keys map: lostRfidCard to lost or rfidFailure, damagedWristband to wristbandReplacement, compromisedQr to qrCompromise, newMobileDevice to customerChangedPhone, walletCredentialReplacement to walletReplacement, faceReEnrollment unchanged, printedTicketReplacement to damaged, incorrectCredentialAssignment to incorrectAssignment."},"outcome":{"type":"string","enum":["replace","rebind","suspendMedia","revokeMedia"],"description":"What happens to the media"},"numberOfReplacements":{"type":"integer","minimum":0,"description":"Maximum replacements per credential"},"replacementFeeReference":{"type":"string","description":"Catalogue product charged for the replacement; empty is free"},"approvalRequired":{"type":"boolean","default":false},"supervisorApproval":{"type":"boolean","default":false},"identityVerification":{"type":"boolean","default":true},"oldMediaAutomaticallyRevoked":{"type":"boolean","default":true},"gracePeriod":{"type":"string","description":"ISO 8601 duration the old media stays valid; empty is none"},"simultaneousMediaPolicy":{"type":"string","enum":["oneActive","allowBothDuringGrace"],"default":"oneActive"},"reasonMandatory":{"type":"boolean","default":true},"reissueAllowed":{"type":"boolean","default":true}}},
"MediaReplacementRevocationRebindingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Replacement, Revocation & Rebinding Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"outcome":{"type":"string","enum":["replace","rebind","suspendMedia","revokeMedia"],"description":"What happens to the media (decided 29 September, VM close-out)"},"replacementReason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"],"description":"The reason this rule is for, in the vocabulary of `replaceCredential`, so the rule a replacement reads is keyed the way the replacement names it (decided 29 September, writers pass). The old keys map: lostRfidCard to lost or rfidFailure, damagedWristband to wristbandReplacement, compromisedQr to qrCompromise, newMobileDevice to customerChangedPhone, walletCredentialReplacement to walletReplacement, faceReEnrollment unchanged, printedTicketReplacement to damaged, incorrectCredentialAssignment to incorrectAssignment."},"numberOfReplacements":{"type":"integer","description":"Number of replacements"},"replacementFeeReference":{"type":"string","description":"Reference to a fee in pricing configuration; no amount is held here"},"approvalRequired":{"type":"boolean","description":"Approval required"},"identityVerification":{"type":"boolean","description":"Identity verification"},"oldMediaAutomaticallyRevoked":{"type":"boolean","description":"Old media automatically revoked"},"gracePeriod":{"type":"string","description":"ISO 8601 duration, e.g. PT30M"},"simultaneousMediaPolicy":{"type":"string","description":"Simultaneous media policy"},"reasonMandatory":{"type":"boolean","description":"Reason mandatory"},"supervisorApproval":{"type":"boolean","description":"Supervisor approval"},"reissueAllowed":{"type":"boolean","description":"Reissue allowed"}},"required":["replacementReason"]},
"MediaTypeCredentialTechnologyRegistryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Type & Credential Technology Registry displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"mediaTypeId":{"type":"string","description":"Media Type ID"},"name":{"type":"string","description":"Name"},"category":{"type":"string","enum":["digital","physical","biometric","future"],"description":"Media category"},"provider":{"type":"array","items":{"type":"string"},"description":"Provider integrations that implement this media type (media type is not the vendor)"},"technology":{"type":"string","description":"Technology"},"tokenFormat":{"type":"string","description":"Token format"},"generationMethod":{"type":"string","description":"Generation method"},"validationMechanism":{"type":"string","description":"Validation mechanism"},"supportsVisualDesign":{"type":"boolean","description":"Supports visual design"},"supportsDynamicUpdate":{"type":"boolean","description":"Supports dynamic update"},"supportsRevocation":{"type":"boolean","description":"Supports revocation"},"supportsExpiration":{"type":"boolean","description":"Supports expiration"},"supportsOfflineReference":{"type":"boolean","description":"Supports offline reference"},"supportsReplacement":{"type":"boolean","description":"Supports replacement"},"supportsEncryption":{"type":"boolean","description":"Supports encryption"},"supportsSigning":{"type":"boolean","description":"Supports signing"},"supportedChannels":{"type":"array","items":{"type":"string"},"description":"Supported channels"},"supportedDevices":{"type":"array","items":{"type":"string"},"description":"Supported devices"},"integrationAdapter":{"type":"string","description":"Integration adapter"}},"required":["mediaTypeId","name","category"]},
"MediaTypeTechnologyLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Type & Technology Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"active":{"type":"boolean","description":"False once retired through `setMediaTypeTechnology`; issued credentials stay valid (decided 29 September, VM close-out)"},"mediaType":{"type":"string","enum":["linearBarcode","twoDimensionalBarcode","qr","rfidContact","rfidProximity","rfidIso15693","rfidOtherStandard","appCredential","mobileWallet","paperTicket","wristband","plasticCard","hotelCard","facePass","faceTag","partnerQr","externalBarcode","thirdPartyCredential"],"description":"The kind of medium this profile defines"},"technology":{"type":"string","enum":["barcode","rfid","nfc","magneticStripe","mobile","physical","biometric","external"],"description":"Technology family"},"encodingFormat":{"type":"string","description":"encoding format"},"supportedReaderTypes":{"type":"array","items":{"type":"string"},"description":"supported reader types"},"onlineOfflineCapability":{"type":"string","enum":["onlineOnly","offlineOnly","onlineAndOffline"],"description":"online/offline capability"},"writableReadOnly":{"type":"string","enum":["writable","readOnly"],"description":"writable/read-only"},"securityClassification":{"type":"string","description":"security classification"},"applicableVenues":{"type":"array","items":{"type":"string"},"description":"Venue ids"},"applicableProducts":{"type":"array","items":{"type":"string"},"description":"Product ids"},"mediaTypeId":{"type":"string","description":"Media type profile identifier"},"name":{"type":"string","description":"Profile name"}}},
"MultiMediaBindingAssociationRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Multi-Media Binding & Association Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Binding rule ID"},"allowedMedia":{"type":"array","items":{"type":"string"},"description":"Media type IDs allowed"},"mandatoryMedia":{"type":"array","items":{"type":"string"},"description":"Media type IDs required"},"optionalMedia":{"type":"array","items":{"type":"string"},"description":"Media type IDs optional"},"maximumActiveMedia":{"type":"integer","description":"Maximum active media"},"minimumMediaRequired":{"type":"integer","description":"Minimum media required"},"primaryMedia":{"type":"string","description":"Primary media"},"secondaryMedia":{"type":"array","items":{"type":"string"},"description":"Secondary media"},"backupMedia":{"type":"array","items":{"type":"string"},"description":"Backup media"},"temporaryMedia":{"type":"array","items":{"type":"string"},"description":"Temporary media"},"mediaCombination":{"type":"array","items":{"type":"string"},"description":"Permitted media combinations"},"simultaneousActivation":{"type":"array","items":{"type":"string"},"description":"Media that may be active at the same time, e.g. face with RFID"},"exclusiveActivation":{"type":"array","items":{"type":"string"},"description":"Media whose activation revokes another, e.g. RFID activated revokes temporary paper"},"product":{"type":"string","description":"Product"},"ticketType":{"type":"string","description":"Ticket Type"},"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"customerType":{"type":"string","description":"Customer Type"},"membership":{"type":"string","description":"Membership"},"channel":{"type":"string","description":"Channel"},"age":{"type":"string","description":"Age"},"country":{"type":"string","description":"Country"},"accessEnvironment":{"type":"string","description":"Access environment"}},"required":["ruleId"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"VirtualTicketArchitectureTestingGovernanceAuditView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Ticket Architecture Testing, Governance & Audit displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"changeType":{"type":"string","enum":["configurationChange","mediaBinding","rebinding","activation","suspension","revocation","replacement","resolverChange","ruleChange","approval"],"description":"What kind of change was recorded"},"actor":{"type":"string","description":"Actor"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"before":{"type":"string","description":"State before the change"},"after":{"type":"string","description":"State after the change"}}},
"VirtualTicketCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Ticket Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicketId":{"type":"string","description":"Virtual Ticket ID"},"product":{"type":"string","description":"Product"},"eventPerformance":{"type":"string","description":"Event / Performance"},"ticketHolder":{"type":"string","description":"Ticket Holder"},"orderReference":{"type":"string","description":"Order Reference"},"ticketType":{"type":"string","description":"Ticket Type"},"seatResourceWhereApplicable":{"type":"string","description":"Seat / Resource where applicable"},"ticketStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"Virtual Ticket status (lifecycle 15.1.3)"},"usageStatus":{"type":"string","enum":["unused","partiallyUsed","used"],"description":"How much of the entitlement is consumed"},"numberOfLinkedMedia":{"type":"integer","description":"Number of Linked Media"},"primaryMedia":{"type":"string","description":"Primary Media"},"lastCredentialActivity":{"type":"string","format":"date-time","description":"Last Credential Activity"},"lastModified":{"type":"string","format":"date-time","description":"Last Modified"},"validFrom":{"type":"string","format":"date-time","description":"Valid from"},"validTo":{"type":"string","format":"date-time","description":"Valid to"}}},
"VirtualTicketCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"totalVirtualTickets":{"type":"integer","description":"Total Virtual Tickets"},"active":{"type":"integer","description":"Active"},"pendingActivation":{"type":"integer","description":"Pending Activation"},"suspended":{"type":"integer","description":"Suspended"},"usedConsumed":{"type":"integer","description":"Used / Consumed"},"partiallyConsumed":{"type":"integer","description":"Partially Consumed"},"expired":{"type":"integer","description":"Expired"},"cancelled":{"type":"integer","description":"Cancelled"},"revoked":{"type":"integer","description":"Revoked"},"virtualTicketsWithMultipleMedia":{"type":"integer","description":"Virtual Tickets with Multiple Media"},"virtualTicketsWithNoActiveMedia":{"type":"integer","description":"Virtual Tickets with No Active Media"},"mediaBindingExceptions":{"type":"integer","description":"Media Binding Exceptions"},"credentialSynchronizationIssues":{"type":"integer","description":"Credential Synchronization Issues"}}},
"VirtualTicketIdentityMasterRecordConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Virtual Ticket Identity & Master Record Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"venueId":{"type":"string","description":"Venue this configuration applies to"},"idGenerationPattern":{"type":"string","description":"Virtual Ticket ID format: prefix, suffix and length"},"ticketClassification":{"type":"string","description":"Ticket classification"},"ticketOwnershipModel":{"type":"string","description":"Ticket ownership model"},"holderAssignmentRequirements":{"type":"string","description":"Holder assignment requirements"},"transferabilityReference":{"type":"string","description":"Transferability reference"},"validityModel":{"type":"string","description":"Validity model"},"consumptionModel":{"type":"string","description":"Consumption model"},"entitlementModel":{"type":"string","description":"Entitlement model"},"mediaRequirements":{"type":"array","items":{"type":"string"},"description":"Media types a ticket of this configuration must carry"}},"required":["venueId"]},
"VirtualTicketIdentityMasterRecordConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Ticket Identity & Master Record Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue this configuration applies to"},"idGenerationPattern":{"type":"string","description":"Virtual Ticket ID format: prefix, suffix and length"},"ticketClassification":{"type":"string","description":"Ticket classification"},"ticketOwnershipModel":{"type":"string","description":"Ticket ownership model"},"holderAssignmentRequirements":{"type":"string","description":"Holder assignment requirements"},"transferabilityReference":{"type":"string","description":"Transferability reference"},"validityModel":{"type":"string","description":"Validity model"},"consumptionModel":{"type":"string","description":"Consumption model"},"entitlementModel":{"type":"string","description":"Entitlement model"},"mediaRequirements":{"type":"array","items":{"type":"string"},"description":"Media types a ticket of this configuration must carry"}},"required":["venueId"]},
"VirtualTicketStatusLifecycleModelView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Ticket Status & Lifecycle Model displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"fromStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"Status the transition starts from"},"toStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"Status the transition leads to"},"originatingSources":{"type":"array","items":{"type":"string","enum":["orderManagement","cancellation","refund","upgradeConversion","ticketTransfer","membership","expiry","accessUsage","authorizedOperator","api","scheduledProcess"]},"description":"Where this transition may originate"},"allowed":{"type":"boolean","description":"Whether the transition is allowed"},"requiresAuthorizedException":{"type":"boolean","description":"Allowed only with an authorised exception, e.g. Used to Active"}},"required":["fromStatus","toStatus"]}
}
```
