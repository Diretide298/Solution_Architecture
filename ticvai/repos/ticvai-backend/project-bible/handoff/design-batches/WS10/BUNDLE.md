# WS10 — Access Control board 10

**10 screens · 17 operations · 26 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, ACCREDITATION_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-234` | Dynamic Access Policy Command Center | C | 0 | 182 | 6 | 2 | 1 | 0 | — | notStarted (generated) |
| `BO-235` | Access Attribute Catalog | C | 6 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-236` | Visual Dynamic Policy Builder | B–D | 0 | 20 | 6 | 2 | 0 | 0 | — | notStarted (generated) |
| `BO-237` | Context, Time, Event & Capacity Policy Builder | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-238` | Identity, Membership & Accreditation Policies | B–D | 0 | 0 | 6 | 7 | 0 | 6 | — | notStarted (generated) |
| `BO-239` | Policy Scope, Hierarchy & Inheritance | B–D | 11 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-240` | Authorization Governance & Temporary Access | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-241` | Policy Evaluation Architecture & Offline Distribution | B–D | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-242` | Policy Simulation, Conflict & Impact Analysis | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-243` | Policy Approval, Audit, Analytics & AI Optimization | C | 2 | 7 | 6 | 13 | 0 | 3 | — | notStarted (generated) |

## Thin screens in this batch

**BO-235, BO-236, BO-237, BO-238, BO-240, BO-241, BO-242 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-234` Dynamic Access Policy Command Center

**Provide central governance and visibility over all dynamic access policies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task APP-SETUP-BO-234 |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/dynamic-access-policy-command-center-bo-234` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): A policy write on the command centre; writes belong to BO-236 and BO-237 (VO-R02, ADR-0041; design-notes correction venue-operations BO-234).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Command centre of the dynamic access policy board (attribute-based access): tiles for active, draft, pending approval, triggered today, allow, deny and review decisions, conflicts, expiring and AI recommendations; the policy directory (Policy, Scope, Type, Priority, Status) with health (Healthy, Conflict, Unused, High denial rate, Expiring, Requires review); AI insights such as a conflict between two policies at 18:00-19:00. The one thing to get right: conflicts and high-denial policies are surfaced first.

**Known correction pending (do not draw the wrong version)**

- **Directory table has one column, "Review Decisions"** Why: Review decisions is a KPI tile; the directory columns are Policy, Scope, Type, Priority, Status. *(source: screens/P08-venue-back-office.yaml#BO-234; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): A policy write (setVisualDynamicPolicy) on the command centre (CHG-WIR-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Policies** (metric tile, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**Draft Policies** (metric tile, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**Policies Pending Approval** (metric tile, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**Policies Triggered Today** (metric tile, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**Allow Decisions** (metric tile, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**Deny Decisions** (metric tile, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**Policy Conflicts** (metric tile, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**Expiring Policies** (metric tile, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**AI Recommendations** (metric tile, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**Every dynamic access policy** (data table, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Review decisions | text | not in the schema: `Review Decisions` |

**The selected dynamic access policy** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Review decisions | text | not in the schema: `Review Decisions` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: The ten pack tiles (including Review decisions, missing from the screen) per VO-R02; Policy conflicts red when non-zero. *(source: screens/P08-venue-back-office.yaml#BO-234)*
- **Policy directory**: Columns Policy, Scope, Type (Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership, Time/event), Priority (higher wins), Status, Health badge; sorted by health problems then priority. *(source: screens/P08-venue-back-office.yaml#BO-234 / contracts/spine/access.yaml#listDynamicPolicyEffectiveness)*
- **AI insights**: Plain sentences naming both policies and the time window of a conflict, each with Open both; advisory only (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-235)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open policy**: Opens the builder (BO-236) or effectiveness detail (BO-243). *(source: DI-653)*

**Data it reads**: `listDynamicAccessPolicy` (onLoad, Dynamic Access Policy Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-235` Access Attribute Catalog: *Works in Access Attribute Catalog*; calls `listDynamicAccessPolicy`
- → `BO-236` Visual Dynamic Policy Builder: *Works in Visual Dynamic Policy Builder*; calls `listDynamicAccessPolicy`
- → `BO-237` Context, Time, Event & Capacity Policy Builder: *Works in Context, Time, Event & Capacity Policy Builder*; calls `listDynamicAccessPolicy`
- → `BO-238` Identity, Membership & Accreditation Policies: *Works in Identity, Membership & Accreditation Policies*; calls `listDynamicAccessPolicy`
- → `BO-239` Policy Scope, Hierarchy & Inheritance: *Works in Policy Scope, Hierarchy & Inheritance*; calls `listDynamicAccessPolicy`
- → `BO-240` Authorization Governance & Temporary Access: *Works in Authorization Governance & Temporary Access*; calls `listDynamicAccessPolicy`
- → `BO-241` Policy Evaluation Architecture & Offline Distribution: *Works in Policy Evaluation Architecture & Offline Distribution*; calls `listDynamicAccessPolicy`
- → `BO-242` Policy Simulation, Conflict & Impact Analysis: *Works in Policy Simulation, Conflict & Impact Analysis*; calls `listDynamicAccessPolicy`
- → `BO-243` Policy Approval, Audit, Analytics & AI Optimization: *Works in Policy Approval, Audit, Analytics & AI Optimization*; carries `policyId`; calls `listDynamicAccessPolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic access policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic access policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic access policy yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic access policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `to` is before `from`, or the range is longer than 366 days |

#### Consistency with other screens

- Match `BO-243`: Same status words (Draft, Pending approval, Active, Expired) and health badges.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policies:
- policy: Ladies Night Access
  scope: Water Park
  type: Guest attribute
  priority: 100
  status: Active
  health: Healthy
- policy: VIP Backstage
  scope: Event Arena
  type: Accreditation
  priority: 90
  status: Active
  health: Conflict
- policy: Peak Capacity Control
  scope: Adventure Park
  type: Occupancy
  priority: 80
  status: Active
  health: High denial rate
- policy: Staff Restricted Zone
  scope: Resort
  type: Employee
  priority: 95
  status: Active
  health: Healthy
```

#### Permissions

- `listDynamicAccessPolicy` → `SCOPE_VIEW` (read) · staff
- `listDynamicPolicyEffectiveness` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.47 | Access Analytics Dashboard - System shall provide dashboards for access policy analytics. | Admission and Access | CONTRACTED | `listDynamicAccessPolicy` |
| 3.3.48 | Policy Effectiveness Reporting - System shall provide reporting on policy effectiveness. | Admission and Access | CONTRACTED | `listDynamicPolicyEffectiveness` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-234` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-234`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 1: Opens Dynamic Access Policy Command Center → Provide central governance and visibility over all dynamic access policies.
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F120 branch at step 1 (expected): when Nothing has been set up on Dynamic Access Policy Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F120 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …
- ADR-0041 *A command centre is a saved dashboard, not a screen* (`docs/adr/0041-a-command-centre-is-a-saved-dashboard.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (182 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-234?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-235`, `BO-236`, `BO-237`, `BO-238`, `BO-239`, `BO-240`, `BO-241`, `BO-242`, `BO-243`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-235` Access Attribute Catalog

**Define the attributes available to the TICVAI policy engine. This becomes the reusable data dictionary for dynamic access decisions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task APP-SETUP-BO-235 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-attribute-catalog-bo-235` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The data dictionary the policy engine may test: attributes grouped by category (Guest, Credential, Employee, Location, Time, Operational, Device, Risk), each with a stable key (guest.tier), label, data type and allowed values. Policy builders pick only from here. The one thing to get right: attributes used by a published policy are locked against type changes and disabling, and the screen says which policies use them.

**Known correction pending (do not draw the wrong version)**

- **Content region is an empty unbound table (pack "gives nothing that can be drawn")** Why: The pack lists categories and attributes and the read returns them; bind listAccessAttributeCatalog. *(source: screens/P08-venue-back-office.yaml#BO-235 / contracts/spine/access.yaml#listAccessAttributeCatalog; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Used by N policies" is not returned** Why: Needed to explain the 409 lock before the user hits it. *(source: contracts/spine/access.yaml#setAccessAttributeCatalog; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Sent by *Save attribute*** (`setAccessAttributeCatalog`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Attribute key `attributeKey` | text field | required | — | max length 100; pattern `^[a-z][a-zA-Z0-9]*(\.[a-z][a-zA-Z0-9]*)*$` | — | Stable key a policy condition names, e.g. guest.tier. | `setAccessAttributeCatalog` body |
| Category `category` | select | required | — | Guest · Credential · Employee · Location · Time · Operational · Device · Risk | — | — | `setAccessAttributeCatalog` body |
| Label `label` | text field | required | — | max length 200 | — | — | `setAccessAttributeCatalog` body |
| Data type `dataType` | select | required | — | String · Integer · Number · Boolean · Date · Date time · Enum | — | — | `setAccessAttributeCatalog` body |
| Allowed values `allowedValues` | list of values (chips) | optional | — | — | — | Required when dataType is enum | `setAccessAttributeCatalog` body |
| Enabled `enabled` | toggle | optional | on | — | — | — | `setAccessAttributeCatalog` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **attributeKey**: Lower camel segments separated by dots (guest.tier, credential.mediaType), max 100, unique in the tenant, immutable once saved. *(source: contracts/spine/access.yaml#setAccessAttributeCatalog)*
- **category**: One of the eight categories; the catalogue is displayed grouped by it. *(source: screens/P08-venue-back-office.yaml#BO-235 / contracts/spine/access.yaml#setAccessAttributeCatalog)*
- **dataType / allowedValues**: Text, Whole number, Number, Yes/No, Date, Date and time, List; List requires values (chip editor). *(source: contracts/spine/access.yaml#setAccessAttributeCatalog)*
- **Sensitive attributes**: Gender and country/residency carry the pack's "where legally/business permitted" note; show a caution label when enabling them. *(source: screens/P08-venue-back-office.yaml#BO-235)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save attribute (primary button) | `setAccessAttributeCatalog` PUT `/access-attribute-catalog` | AccessAttributeCatalogInput | AccessAttributeCatalogView | 409 Changing the data type of, or disabling, an attribute a published policy tests; 422 dataType enum with no allowedValues | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Catalogue**: Grouped list Category > attributes with label, key, type, values, enabled, and "Used by N policies". *(source: contracts/spine/access.yaml#listAccessAttributeCatalog)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save attribute**: Upsert by key; refused (409) to change type or disable an attribute a published policy tests - message names the policies. *(source: contracts/spine/access.yaml#setAccessAttributeCatalog)*

**Data it reads**: `listAccessAttributeCatalog` (onLoad, Access Attribute Catalog)

**Where the user goes next**

- → `BO-234` Dynamic Access Policy Command Center: *Returns to the board's landing screen*; calls `listAccessAttributeCatalog`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access attribute catalog list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access attribute catalog untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access attribute catalog yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access attribute catalog are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Changing the data type of, or disabling, an attribute a published policy tests; 422 dataType enum with no allowedValues |

#### Consistency with other screens

- Match `BO-155`: The rule builder's condition pickers list exactly these attributes.
- Match `BO-236`: Same for the dynamic policy builder.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
attributes:
- category: Guest
  key: guest.category
  label: Guest category
  type: List
  values: Adult, Child, Senior, POD
- category: Credential
  key: credential.mediaType
  label: Media type
  type: List
  values: QR, RFID, NFC, Face
- category: Credential
  key: membership.tier
  label: Membership tier
  type: List
  values: Silver, Gold, Platinum
- category: Operational
  key: venue.occupancyPercent
  label: Venue occupancy (%)
  type: Whole number
```

#### Permissions

- `listAccessAttributeCatalog` → `SCOPE_VIEW` (read) · staff
- `setAccessAttributeCatalog` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-235` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-235`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 2: Works in Access Attribute Catalog → Define the attributes available to the TICVAI policy engine. This becomes the reusable data dictionary for dynamic access decisions.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-235?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save attribute.
- [ ] Every transition is wired: `BO-234`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-236` Visual Dynamic Policy Builder

**Provide a no-code interface for constructing contextual access policies.**

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
| Route | `/access-venue/visual-dynamic-policy-builder-bo-236` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The no-code builder for guest admission policies: IF conditions (Accreditation = VIP AND Event = Concert A AND Zone = Backstage AND Time BETWEEN 17:00 AND 23:59 AND Credential status = Active) THEN a result (Allow, Deny, Review, Require ID, Require biometric, Require companion, Require supervisor), with priority and validity, saved in the closed rule format that the cloud and the offline gate evaluate identically. The one thing to get right: the builder can only produce what the rule format allows - conditions from the attribute catalogue, fixed comparators, at most one level of nested groups - so what the administrator sees is exactly what the gate runs.

**Known correction pending (do not draw the wrong version)**

- **policyId is a required input** Why: A new policy has no id; the server assigns it (VO-R03). *(source: contracts/spine/access.yaml#setVisualDynamicPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The input has no policy type or allowed zones, which the stored policy carries** Why: The command centre's Type column and zone scoping cannot be set from the builder. *(source: contracts/spine/access.yaml#/components/schemas/AccessDynamicPolicy / contracts/spine/access.yaml#setVisualDynamicPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Save changes has no operation and no read of policies is bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The pack's policies have an ELSE (THEN Allow ELSE Deny); the contract has one result when the condition holds. Does "else" mean deny, or "this policy has no say"?** → Drawn default accepted: Draw "Otherwise - no decision from this policy (other policies decide)" with the ELSE result greyed. *(decided by Chinmay, 2026-10-02; DEC-257 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name**: Required, max 200 (e.g. VIP Backstage Access), Arabic variant for any guest-facing use. *(source: contracts/spine/access.yaml#setVisualDynamicPolicy)*
- **conditionRule**: A block canvas: the top block is "All of" (AND) or "Any of" (OR); each condition is subject > attribute (picked from the attribute catalogue, BO-235) > comparator (equals, not equals, in, not in, between, less than, at most, greater than, at least, exists, not exists) > value(s) typed to the attribute (date picker, time, list chips); NOT is a toggle on a condition or group. One level of groups only ("Gold AND (Occupancy < 90% OR VIP override)"); a deeper nest is not offered. At most 50 conditions. *(source: screens/P08-venue-back-office.yaml#BO-237 / contracts/spine/access.yaml#/components/schemas/AdmissionRule / contracts/spine/access.yaml#/components/schemas/AdmissionCondition / ADR-0068)*
- **result**: The seven results as coloured chips (Allow green, Deny red, the five Require/Review amber), required. *(source: screens/P08-venue-back-office.yaml#BO-237 / contracts/spine/access.yaml#setVisualDynamicPolicy)*
- **priority**: Whole number, higher wins among policies of the same scope (as on BO-234); shown with the neighbouring policies' priorities. *(source: screens/P08-venue-back-office.yaml#BO-234 / contracts/spine/access.yaml#setVisualDynamicPolicy)*
- **validFrom / validTo**: Optional date-times in venue time; empty from = at once; after validTo the policy becomes Expired automatically. *(source: contracts/spine/access.yaml#setVisualDynamicPolicy)*
- **status**: Active / Inactive switch; switching to Active sends the policy for approval (shows "Pending approval"), Inactive takes effect at once. *(source: contracts/spine/access.yaml#setVisualDynamicPolicy)*
- **policyId**: Not an input; a new policy gets its id from the server (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Policies** (data table, from `listDynamicAccessPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy | text | — |
| Policy name | text | e.g. |
| Scope | text | Where the policy applies, e.g. |
| Policy type | chip: Guest attribute, Accreditation, Occupancy, Employee, Risk, Membership… | — |
| Priority | 1,234 | — |
| Status | chip: Draft, Pending approval, Active, Inactive, Expired | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active policies | 1,234 | Active Policies |
| Draft policies | 1,234 | Draft Policies |
| Policies pending approval | 1,234 | Policies Pending Approval |
| Policies triggered today | 1,234 | Policies Triggered Today |
| Allow decisions | 1,234 | Allow Decisions |
| Deny decisions | 1,234 | Deny Decisions |
| Review decisions | 1,234 | Review decisions today |
| Policy conflicts | 1,234 | Policy Conflicts |
| Expiring policies | 1,234 | Expiring Policies |
| AI recommendations | 1,234 | AI Recommendations |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Plain-language reading**: Under the canvas, the rule read back as a sentence ("Allow when accreditation is VIP and event is Concert A and zone is Backstage between 17:00 and 23:59 and the credential is active"). *(source: screens/P08-venue-back-office.yaml#BO-236 / designer default)*
- **Policy list (left)**: Policies with type, result chip, priority, status and version. *(source: contracts/spine/access.yaml#listDynamicAccessPolicy)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save policy**: Saves a new version (whole policy, VO-R04); Active submits it for approval. 400 for a rule the format refuses (wrong operand count, too deep) shown on the block. *(source: contracts/spine/access.yaml#setVisualDynamicPolicy / contracts/spine/access.yaml#/components/schemas/AdmissionCondition)*
- **Test**: Opens the simulation (BO-242) for this draft version. *(source: DI-629)*
- **Cancel**: Discards edits and returns to BO-234. *(source: screens/P08-venue-back-office.yaml#BO-236)*

**Data it reads**: `listDynamicAccessPolicy` (onLoad, The policies to open and edit)

**Where the user goes next**

- → `BO-234` Dynamic Access Policy Command Center: *Returns to the board's landing screen*; calls `setVisualDynamicPolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visual dynamic policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visual dynamic policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visual dynamic policy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visual dynamic policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Attribute disabled in the catalogue after the policy was written**: The block shows the attribute struck through with "No longer available"; the policy cannot be re-saved until changed. *(source: contracts/spine/access.yaml#setAccessAttributeCatalog)*
- **Policy depends on a live value (occupancy, risk) at an offline gate**: A badge "Needs central data - offline behaviour set on BO-241". *(source: screens/P08-venue-back-office.yaml#BO-242)*

#### Consistency with other screens

- Match `BO-155`: The visual access rule builder (board 2) should use the same block design and comparator words.
- Match `BO-235`: Condition pickers list exactly the catalogue's attributes.
- Match `BO-237`: Context, time, event and capacity policies are the same builder with the time/occupancy subjects preselected (VO-R14).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  name: VIP Backstage Access
  result: Allow
  priority: 90
  valid: 1 Oct 2026 17:00 - 1 Oct 2026 23:59
  status: Pending approval
conditions:
- Accreditation level = VIP
- Event = Concert A
- Zone = Backstage
- Time between 17:00 and 23:59
- Credential status = Active
```

#### Permissions

- `setVisualDynamicPolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listDynamicAccessPolicy` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.22 | Policy Builder - System shall provide a visual policy configuration interface. | Admission and Access | CONTRACTED | `setVisualDynamicPolicy` |
| 3.3.47 | Access Analytics Dashboard - System shall provide dashboards for access policy analytics. | Admission and Access | CONTRACTED | `listDynamicAccessPolicy` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-236` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-236`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 4: Works in Visual Dynamic Policy Builder → Provide a no-code interface for constructing contextual access policies.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-236?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-234`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-237` Context, Time, Event & Capacity Policy Builder

**Configure policies driven by changing venue conditions rather than only guest attributes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§MONITOR) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/context-time-event-capacity-policy-builder-bo-237` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of context, time, event and capacity policies (setContextTimeEvent has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Policies that react to venue conditions rather than guest attributes: date, day, time, season, event, performance, special event, holiday, operating calendar, occupancy and attraction status - "Ladies Night, Friday 18:00-23:59", "Zone occupancy at least 90% - stop standard admission but allow exit and emergency roles", "Attraction closed - deny attraction entry", "Private corporate event - only corporate accreditation". Includes the occupancy bands Normal / Monitor / Restrict / Stop admission. The one thing to get right: capacity bands are shown as one coloured scale with the live occupancy on it, and stop rules always say who is still let through.

**Known correction pending (do not draw the wrong version)**

- **Drawn as a command centre with a metric tile labelled "90-94%" and buttons "Event" and "Special Event"** Why: Sample values used as labels; the screen is a builder (a band scale and context choices), not a dashboard. *(source: screens/P08-venue-back-office.yaml#BO-238 / screens/P08-venue-back-office.yaml#BO-237; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only two thresholds (monitor, restrict) against the pack's four bands** Why: The Stop admission band (95%+) has no field, and it is the one that denies. *(source: screens/P08-venue-back-office.yaml#BO-238 / contracts/spine/access.yaml#setContextTimeEvent; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write-only (no read of context policies); policyId a required input (CHG-WIR-004)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **contextType**: The eleven context types as a first choice; it decides which condition blocks appear (a time window for time, an event picker for event, a percentage for occupancy, an attraction for attraction status). *(source: screens/P08-venue-back-office.yaml#BO-237 / contracts/spine/access.yaml#setContextTimeEvent)*
- **conditionRule / result**: The same builder as BO-236 with the timeEvent or occupancy subject preselected; result from the seven results. *(source: contracts/spine/access.yaml#setContextTimeEvent / contracts/spine/access.yaml#/components/schemas/AdmissionRule)*
- **monitorThresholdPercent / restrictThresholdPercent**: A single 0-100% scale with draggable band edges, Normal (green) to Monitor (amber, default 80) to Restrict (orange, default 90) to Stop admission (red, 95 in the pack); Restrict must be above Monitor. *(source: screens/P08-venue-back-office.yaml#BO-238 / contracts/spine/access.yaml#setContextTimeEvent)*
- **Exempt flows**: For stop rules, "Still allowed" chips (Exit, Emergency and security roles, Members) so the gate never traps people inside or keeps responders out. *(source: screens/P08-venue-back-office.yaml#BO-237)*
- **validFrom / validTo / status**: As BO-236; recurring windows such as every Friday 18:00-23:59 come from the operating calendar (VO-R01), not typed dates. *(source: contracts/spine/access.yaml#setContextTimeEvent)*

#### Outputs: what the screen shows and produces

**Shown**

**90–94%** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Event (primary button) | navigation or local | — | — | — | — |
| Special Event (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Live band**: Current occupancy per zone on the band scale ("Aqua Park 86% - Monitor"), so the effect of a threshold is visible while editing. *(source: contracts/spine/access.yaml#listLiveVenueOccupancy / DI-650)*
- **Policy list**: Context policies with type icon, window or threshold, result, status. *(source: contracts/spine/access.yaml#listDynamicAccessPolicy)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save context policy**: Saves a new version; Active goes for approval (as BO-236). *(source: contracts/spine/access.yaml#setContextTimeEvent)*

**Where the user goes next**

- → `BO-234` Dynamic Access Policy Command Center: *Returns to the board's landing screen*; calls `setContextTimeEvent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The context time event list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the context time event untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No context time event yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the context time event are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Venue reaches Stop admission**: Scanners deny "Venue full" with live occupancy shown, until guests exit; exits and exempt roles still pass. *(source: DI-650)*
- **Policy tests a sensitive attribute (Ladies Night uses gender)**: Caution label "Use only where legally and business permitted", as on the attribute catalogue. *(source: screens/P08-venue-back-office.yaml#BO-235)*

#### Consistency with other screens

- Match `BO-222`: Special days come from the operating calendar; this screen ties policies to them.
- Match `BO-255`: Occupancy bands and colours match the live occupancy screen.
- Match `BO-236`: Same builder and results.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policies:
- name: Ladies Night Access
  context: Operating calendar
  window: Fridays 18:00-23:59
  result: Allow
  scope: Aqua Park
- name: Peak Capacity Control
  context: Occupancy
  bands: Monitor 80%, Restrict 90%, Stop 95%
  result: Deny
  stillAllowed: Exit, Security, Emergency services
- name: Falcon Coaster closed
  context: Attraction status
  result: Deny
live:
  zone: Aqua Park
  occupancy: 86%
  band: Monitor
```

#### Permissions

- `setContextTimeEvent` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access decisions consider who, ticket type, where, when and context; e.g. an otherwise valid unused ticket is denied once the venue's maximum live occupancy is reached, until guests exit. Scanners need a venue-full denial state. *(agreed · MoM 2 Sep 2026, 4.16 Attribute-Based Access Control · DI-650)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-237` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-237`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 6: Works in Context, Time, Event & Capacity Policy Builder → Configure policies driven by changing venue conditions rather than only guest attributes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-237?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Event, Special Event.
- [ ] Every transition is wired: `BO-234`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-238` Identity, Membership & Accreditation Policies

**Configure policies based on who the requesting person is.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `ACCREDITATION_CONFIGURE`, `SCOPE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/identity-membership-accreditation-policies-bo-238` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Policies about who the person is: twelve identity types (guest, member, annual pass holder, employee, contractor, vendor, performer, media, VIP, security, emergency services, event staff), each with zones allowed and denied and a validity - Gold member to priority entrance, member lounge and selected attractions during membership validity; Event crew level 3 to production zone, backstage and staff entrance but not VIP hospitality or the finance office; employees only when active, on shift and their role allows the zone; temporary accreditation that expires by itself. The one thing to get right: allowed and denied zones side by side on the venue map, and automatic expiry visible.

**Known correction pending (do not draw the wrong version)**

- **The read returns identityType, allowedZones and deniedZones; the write (setVisualDynamicPolicy) has none of them** Why: The screen can show identity policies but cannot create or edit them as shown. *(source: contracts/spine/access.yaml#listIdentityMembershipAccreditation / contracts/spine/access.yaml#setVisualDynamicPolicy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **setAccessProfile (accreditation zones, dates, times) is bound here as a second write** Why: Accreditation zone rights already live in the accreditation module's access profiles; two editors of one right (VO-R14). This screen should reference them. *(source: contracts/satellite/accreditation.yaml#setAccessProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Buttons "Guest" and "Security"** Why: Two identity type values drawn as actions; they are filter chips of the identity type list. *(source: screens/P08-venue-back-office.yaml#BO-238; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **identityType**: One of the twelve types as the first choice; drives which attributes the condition offers (membership tier, accreditation level, employee status). *(source: screens/P08-venue-back-office.yaml#BO-238 / contracts/spine/access.yaml#listIdentityMembershipAccreditation)*
- **allowedZones / deniedZones**: The zone tree with three states per zone (Allowed, Denied, Not set); denied always wins and is drawn red. *(source: screens/P08-venue-back-office.yaml#BO-239 / contracts/spine/access.yaml#listIdentityMembershipAccreditation)*
- **conditionRule**: The BO-236 builder; for employees a preset "Employee status = Active AND Current shift = Active AND Role allows zone". *(source: screens/P08-venue-back-office.yaml#BO-239 / contracts/spine/access.yaml#setVisualDynamicPolicy)*
- **validFrom / validTo**: Date-times in venue time; temporary accreditation shows "Valid 01 Oct 14:00 until 01 Oct 23:30 - expires automatically". *(source: screens/P08-venue-back-office.yaml#BO-239 / contracts/spine/access.yaml#listIdentityMembershipAccreditation)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Guest (primary button) | navigation or local | — | — | — | — |
| Security (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Policies by identity type**: Grouped list - identity type > policy name, allowed zones count, denied zones count, validity, status. *(source: contracts/spine/access.yaml#listIdentityMembershipAccreditation)*
- **Zone map**: The selected policy's allowed (green) and denied (red) zones on the venue map. *(source: screens/P08-venue-back-office.yaml#BO-239 / designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save identity policy**: Saves through the dynamic policy write; Active goes for approval. *(source: contracts/spine/access.yaml#setVisualDynamicPolicy)*

**Data it reads**: `listIdentityMembershipAccreditation` (onLoad, Identity, Membership & Accreditation Policies)

**Where the user goes next**

- → `BO-234` Dynamic Access Policy Command Center: *Returns to the board's landing screen*; calls `listIdentityMembershipAccreditation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The identity membership accreditation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the identity membership accreditation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No identity membership accreditation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the identity membership accreditation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Employee scans a staff door off shift**: Denied with "Not on shift" wording; the policy shows it depends on the rota (cross-process, workforce). *(source: screens/P08-venue-back-office.yaml#BO-239)*
- **Membership lapsed during the visit**: Member-only zones deny from the moment validity ends; the guest's ticket admission is unaffected. *(source: screens/P08-venue-back-office.yaml#BO-239 / designer default)*

#### Consistency with other screens

- Match `BO-659`: Accreditation access schedules (zones by date and time) are set in the accreditation module; this screen must not be a second place to grant accreditation zones.
- Match `BO-055`: The "current shift active" condition reads the workforce rota (cross-process).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policies:
- identity: Member
  name: Gold member access
  allowed: Priority entrance, Member lounge, Falcon Coaster, Wave Rider
  denied: '-'
  valid: During membership
- identity: Event staff
  name: Event crew - level 3
  allowed: Production zone, Backstage, Staff entrance
  denied: VIP hospitality, Finance office
- identity: Contractor
  name: Temporary accreditation
  valid: 01 Oct 2026 14:00 - 01 Oct 2026 23:30
  note: Expires automatically
```

#### Permissions

- `listIdentityMembershipAccreditation` → `SCOPE_VIEW` (read) · staff
- `setVisualDynamicPolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `setAccessProfile` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.22 | Policy Builder - System shall provide a visual policy configuration interface. | Admission and Access | CONTRACTED | `setVisualDynamicPolicy` |
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-238` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-238`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 8: Works in Identity, Membership & Accreditation Policies → Configure policies based on who the requesting person is.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-238?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Guest, Security.
- [ ] Every transition is wired: `BO-234`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `ACCREDITATION_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-239` Policy Scope, Hierarchy & Inheritance

**Govern how policies apply across TICVAI's multi-tenant and multi-venue architecture.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrator defines) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/policy-scope-hierarchy-inheritance-bo-239` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where each policy sits in the hierarchy (tenant, venue, park, zone, attraction, access point) and how conflicts resolve: inherited, local, overridden or mandatory policies; category ranks (Emergency, Security/fraud, Regulatory/safety, Venue restriction, Accreditation, Membership, Standard access); and the conflict rule (highest priority wins, deny overrides allow, most specific wins, mandatory parent wins, explicit resolution). The one thing to get right: at any node, show which policies apply and why - "Inherited from tenant, mandatory" - so a local admin understands what they cannot override.

**Known correction pending (do not draw the wrong version)**

- **The five conflict rules drawn as four selectFields named after the options (Explicit resolution missing)** Why: They are the values of one choice. *(source: screens/P08-venue-back-office.yaml#BO-240 / screens/P08-venue-back-office.yaml#BO-239; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **categoryRank and conflictResolution are stored on every placement row** Why: The pack makes the priority order and the conflict rule one configurable setting ("the actual hierarchy should be configurable"); per-row values can contradict each other. *(source: screens/P08-venue-back-office.yaml#BO-240 / contracts/spine/access.yaml#setPolicyScopeHierarchy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The hierarchy stops at access point; the pack and the vocabulary go down to gate/lane** Why: Lane-level policies (a VIP lane) cannot be placed. *(source: screens/P08-venue-back-office.yaml#BO-239 / contracts/spine/access.yaml#setPolicyScopeHierarchy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the conflict-resolution rule chosen once per tenant, per venue, or per policy placement?** → Drawn default accepted: Draw it once at the top of the screen for the tenant, with a venue override greyed. *(decided by Chinmay, 2026-10-02; DEC-258 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Highest Priority Wins | select field | — | — | — | — | — | — |
| Deny Overrides Allow | select field | — | — | — | — | — | — |
| Most Specific Wins | select field | — | — | — | — | — | — |
| Mandatory Parent Wins | select field | — | — | — | — | — | — |

**Sent by *Save scope placement*** (`setPolicyScopeHierarchy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policy `policyId` | text field | required | — | — | — | The dynamic access policy placed in the hierarchy | `setPolicyScopeHierarchy` body |
| Scope level `scopeLevel` | select | required | — | Tenant · Venue · Park · Zone · Attraction · Access point | — | — | `setPolicyScopeHierarchy` body |
| Scope `scopeId` | text field | required | — | — | — | — | `setPolicyScopeHierarchy` body |
| Policy category `policyCategory` | select | required | — | Emergency · Security fraud · Regulatory safety · Venue restriction · Accreditation · Membership · Standard access | — | — | `setPolicyScopeHierarchy` body |
| Category rank `categoryRank` | number field | optional | — | min 1 | — | Lower wins; emergency is 1 | `setPolicyScopeHierarchy` body |
| Conflict resolution `conflictResolution` | radio group | required | Deny overrides allow | Highest priority wins · Deny overrides allow · Most specific wins · Mandatory parent wins · Explicit resolution | — | — | `setPolicyScopeHierarchy` body |
| Mandatory `mandatory` | toggle | optional | off | — | — | A child scope cannot override a mandatory policy | `setPolicyScopeHierarchy` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **scopeLevel / scopeId**: Pick the node on the hierarchy tree (Tenant > Venue > Park > Zone > Attraction > Access point); tenant level only for tenant administrators. *(source: contracts/spine/access.yaml#setPolicyScopeHierarchy / ADR-0018)*
- **policyCategory / categoryRank**: Category from the seven; the rank order is drawn as one draggable list (Emergency first) - see corrections. *(source: screens/P08-venue-back-office.yaml#BO-239 / contracts/spine/access.yaml#setPolicyScopeHierarchy)*
- **conflictResolution**: One single choice of five with a one-line example each; default Deny overrides allow ("a gate that must choose between two answers refuses"). *(source: screens/P08-venue-back-office.yaml#BO-240 / contracts/spine/access.yaml#setPolicyScopeHierarchy)*
- **mandatory**: "Mandatory - lower levels cannot override" toggle; mandatory placements show a lock at every child node. *(source: contracts/spine/access.yaml#setPolicyScopeHierarchy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save scope placement (primary button) | `setPolicyScopeHierarchy` PUT `/policy-scope-hierarchy` | PolicyScopeHierarchyInheritanceInput | PolicyScopeHierarchyInheritanceView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Hierarchy tree**: Each node with its policies tagged Inherited / Local / Overridden / Mandatory; selecting a node lists the effective policies in evaluation order. *(source: screens/P08-venue-back-office.yaml#BO-239 / contracts/spine/access.yaml#listPolicyScopeHierarchy)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save placement**: Upsert keyed by policy + level + node; confirmation names the nodes below that inherit it. *(source: contracts/spine/access.yaml#setPolicyScopeHierarchy)*

**Data it reads**: `listPolicyScopeHierarchy` (onLoad, Policy Scope, Hierarchy & Inheritance)

**Where the user goes next**

- → `BO-234` Dynamic Access Policy Command Center: *Returns to the board's landing screen*; calls `listPolicyScopeHierarchy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy scope hierarchy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy scope hierarchy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy scope hierarchy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Venue admin tries to override a mandatory tenant policy (Global fraud lock)**: Not offered; the node shows "Mandatory from tenant - cannot override". *(source: screens/P08-venue-back-office.yaml#BO-239 / contracts/spine/access.yaml#setPolicyScopeHierarchy)*
- **Placement at a node in another venue**: Not reachable from this venue's session; tenant-level users work from the tenant node (VO-R09). *(source: ADR-0030)*

#### Consistency with other screens

- Match `BO-234`: Priority and status words are the same as the command centre.
- Match `BO-242`: The simulation trace shows the hierarchy level and rank of each policy.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
placements:
- policy: Credential must be active
  level: Tenant
  node: Yas Leisure Group
  category: Standard access
  mandatory: true
- policy: Global fraud lock
  level: Tenant
  node: Yas Leisure Group
  category: Security/fraud
  rank: 2
  mandatory: true
- policy: Aqua Park operating hours
  level: Venue
  node: Aqua Park
  category: Venue restriction
- policy: VIP lounge restriction
  level: Zone
  node: Summit Peaks VIP Lounge
  category: Venue restriction
```

#### Permissions

- `listPolicyScopeHierarchy` → `SCOPE_VIEW` (read) · staff
- `setPolicyScopeHierarchy` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-239` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-239`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 10: Works in Policy Scope, Hierarchy & Inheritance → Govern how policies apply across TICVAI's multi-tenant and multi-venue architecture.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-239?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save scope placement.
- [ ] Every transition is wired: `BO-234`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-240` Authorization Governance & Temporary Access

**Apply enterprise governance principles to privileged and temporary access.**

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
| Route | `/access-venue/authorization-governance-temporary-access-bo-240` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No operation creates, approves or revokes a temporary or emergency access grant.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Governance of privileged and temporary physical access: temporary grants (a contractor to Technical Room A, 01 Oct 10:00-14:00, reason reader maintenance, approved by the venue security manager, expiring by itself), emergency access grants with scope, duration, reason, approver and full audit, and expiring grants. The one thing to get right: every grant shows its expiry counting down and its approver, and nobody approves their own request.

**Known correction pending (do not draw the wrong version)**

- **Read-only screen with buttons "Temporary Access" and "Expiring Grants" and no operation** Why: The pack's temporary and emergency grants must be created, approved and revoked; no write exists. The two buttons are list filters. *(source: contracts/spine/access.yaml#listAuthorizationGovernanceTemporary / screens/P08-venue-back-office.yaml#BO-240; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Segregation of duties and delegated administration are on this guest-admission board** Why: Who may change which policies is staff authorisation, which lives in Identity's authorisation policy (ADR-0068); show it here read-only and link to it. *(source: screens/P08-venue-back-office.yaml#BO-241 / ADR-0068; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The read shows granteeUserId and approver as ids** Why: People are recognised by name. *(source: contracts/spine/access.yaml#listAuthorizationGovernanceTemporary; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Grant**: Grantee (person search), type (Temporary, Emergency, Delegated administration), scope (zones or access points from the tree), from-to in venue time, reason (required), approver - drawn greyed until a write exists. *(source: screens/P08-venue-back-office.yaml#BO-240 / screens/P08-venue-back-office.yaml#BO-241 / contracts/spine/access.yaml#listAuthorizationGovernanceTemporary)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Temporary Access (primary button) | navigation or local | — | — | — | — |
| Expiring Grants (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Grants list**: Grantee name, type, scope, from-to, reason, approver, status (Pending approval, Active, Expired, Revoked); Active sorted by soonest expiry with "expires in 45 min". *(source: contracts/spine/access.yaml#listAuthorizationGovernanceTemporary)*
- **Governance controls**: Least privilege, segregation of duties, temporary access, expiring grants, delegated administration, approval requirements - each with its current setting and where it is configured. *(source: screens/P08-venue-back-office.yaml#BO-240)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Request grant**: Raises an approval request; the approver is never the requester. Greyed until bound. *(source: screens/P08-venue-back-office.yaml#BO-241 / contracts/spine/approvals.yaml#createApprovalRequest)*
- **Revoke grant**: Confirmation with reason; the grant stops at the next decision online and with the next urgent distribution offline. *(source: screens/P08-venue-back-office.yaml#BO-209)*

**Data it reads**: `listAuthorizationGovernanceTemporary` (onLoad, Authorization Governance & Temporary Access)

**Where the user goes next**

- → `BO-234` Dynamic Access Policy Command Center: *Returns to the board's landing screen*; calls `listAuthorizationGovernanceTemporary`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The authorization governance temporary list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the authorization governance temporary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No authorization governance temporary yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the authorization governance temporary are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Emergency grant needed at night with no approver available**: Issued by an authorised user and marked "Approval after the fact" with a deadline; full audit. *(source: screens/P08-venue-back-office.yaml#BO-241 / designer default)*

#### Consistency with other screens

- Match `BO-243`: Approval wording and segregation of duties match the policy approval screen.
- Match `BO-367`: Approvals go through the platform approval inbox (cross-process).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
grants:
- grantee: Omar Haddad (contractor)
  type: Temporary
  scope: Technical Room A
  window: 01 Oct 2026 10:00-14:00
  reason: Reader maintenance
  approver: Ahmed Al Mansoori
  status: Active
  expires: in 45 min
- grantee: Civil Defence team
  type: Emergency
  scope: All zones, Aqua Park
  window: 01 Oct 2026 15:20-17:20
  reason: Fire alarm response
  approver: Fatima Al Hashimi
  status: Active
```

#### Permissions

- `listAuthorizationGovernanceTemporary` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-240` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-240`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 12: Works in Authorization Governance & Temporary Access → Apply enterprise governance principles to privileged and temporary access.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-240?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Temporary Access, Expiring Grants.
- [ ] Every transition is wired: `BO-234`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-241` Policy Evaluation Architecture & Offline Distribution

**Define where and how policies are evaluated. This screen connects Board 10 with the offline/edge architecture already configured in Board 7.**

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
| Route | `/access-venue/policy-evaluation-architecture-offline-distribution-bo-241` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): Edge nodes are configured on BO-205 and the tenancy till policy governs POS; this screen writes setPolicyEvaluationSetting only (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where each policy category is evaluated - Central, Edge, Device or Hybrid (central when available, cached at edge or device when not) - which locations support it, what happens offline (available, conditional, unavailable), how old cached data may be (live risk score falls back to a cached score at most 15 minutes old, else operator review), and how the active policy set is distributed from the central engine to venue edge and device groups. The one thing to get right: the compatibility matrix makes it obvious which policies stop working offline and what the gate does instead.

**Known correction pending (do not draw the wrong version)**

- **policyCategory is a free string (max 100)** Why: It must match the policy categories used by the policies; free text cannot join to them. *(source: contracts/spine/access.yaml#setPolicyEvaluationSetting; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No field for the fallback result when cached data is unavailable** Why: The pack's "If unavailable - require operator review" is the decision the gate needs. *(source: screens/P08-venue-back-office.yaml#BO-242; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Content is an empty unbound table** Why: Bind listPolicyEvaluationArchitecture as the matrix. *(source: contracts/spine/access.yaml#listPolicyEvaluationArchitecture; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): setEdgeNodeLocal and the tenancy till policy setOfflinePolicy are bound here, with a button "Save edge node local" (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Form: Save policy evaluation setting** (modal, opened by *Save policy evaluation setting*; *Save policy evaluation setting* calls `setPolicyEvaluationSetting`, *Cancel* sends nothing)

**Collects what `setPolicyEvaluationSetting` sends before it is called.** Required: `id`, `scopePath`, `policyCategory`, `evaluationMode`. Optional: `supportedLocations`, `offlineBehaviour`, `maxDataAgeMinutes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setPolicyEvaluationSetting` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setPolicyEvaluationSetting` body |
| Policy category `policyCategory` | text field | required | — | max length 100 | — | e.g. Ticket Status, Time Rule, Membership Tier, Live Occupancy, Live Fraud AI. | `setPolicyEvaluationSetting` body |
| Evaluation mode `evaluationMode` | radio group | required | — | Central · Edge · Device · Hybrid | — | — | `setPolicyEvaluationSetting` body |
| Supported locations `supportedLocations` | multi-select chips | optional | — | Central · Edge · Device | — | — | `setPolicyEvaluationSetting` body |
| Offline behaviour `offlineBehaviour` | segmented control | optional | — | Available · Conditional · Unavailable | — | — | `setPolicyEvaluationSetting` body |
| Max data age minutes `maxDataAgeMinutes` | number field (minutes) | optional | — | min 0 | — | — | `setPolicyEvaluationSetting` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 `maxDataAgeMinutes` missing for conditional offline behaviour.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **policyCategory**: Chosen from the policy categories (ticket status, time rule, membership tier, live occupancy, live fraud AI ...), not typed; one setting per category. *(source: screens/P08-venue-back-office.yaml#BO-242 / contracts/spine/access.yaml#setPolicyEvaluationSetting)*
- **evaluationMode / supportedLocations**: Four cards (Central, Edge, Device, Hybrid) with the pack's one-line meaning; supported locations as ticks, the chosen mode's location ticked and locked. *(source: screens/P08-venue-back-office.yaml#BO-241 / contracts/spine/access.yaml#setPolicyEvaluationSetting)*
- **offlineBehaviour / maxDataAgeMinutes**: Available / Conditional / Unavailable; Conditional reveals "Use cached data up to [15] min old", minutes, at least 1. *(source: screens/P08-venue-back-office.yaml#BO-242 / contracts/spine/access.yaml#setPolicyEvaluationSetting)*
- **Fallback result**: "If cached data is unavailable" - Require operator review / Deny / Allow; drawn greyed (no field). *(source: screens/P08-venue-back-office.yaml#BO-242)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save policy evaluation setting (primary button) | `setPolicyEvaluationSetting` PUT `/policy-evaluation-settings` | AccessPolicyEvaluationSetting | AccessPolicyEvaluationSetting | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 `maxDataAgeMinutes` missing for conditional offline behaviour. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Compatibility matrix**: Policy categories as rows, Central / Edge / Device / Offline as columns with ticks, dashes and "Conditional". *(source: screens/P08-venue-back-office.yaml#BO-242 / contracts/spine/access.yaml#listPolicyEvaluationArchitecture)*
- **Distribution**: Central policy engine > Venue edge > Authorised device groups, each with the policy set version it holds and when it was received. *(source: screens/P08-venue-back-office.yaml#BO-242 / ADR-0068 / contracts/spine/access.yaml#/components/schemas/OfflinePackage)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save evaluation setting**: Whole-row upsert keyed on the category (VO-R04). *(source: contracts/spine/access.yaml#setPolicyEvaluationSetting)*

**Data it reads**: `listPolicyEvaluationArchitecture` (onLoad, Policy Evaluation Architecture & Offline Distribution)

**Where the user goes next**

- → `BO-234` Dynamic Access Policy Command Center: *Returns to the board's landing screen*; calls `listPolicyEvaluationArchitecture`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy evaluation architecture list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy evaluation architecture untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy evaluation architecture yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the policy evaluation architecture are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 `maxDataAgeMinutes` missing for conditional offline behaviour. |

#### Edge cases to draw

- **A device group holds an older policy set version**: Amber with "v3.4 - 3.5 published 10:20, awaiting refresh"; its scans record the version they were decided under. *(source: ADR-0068)*

#### Consistency with other screens

- Match `BO-206`: Offline Validation Policy Builder (board 7) classifies board 2 rules as offline compatible, online required or conditional; same three words as offline behaviour here.
- Match `BO-207`: The edge package carries the policy set version shown here.
- Match `BO-205`: Edge nodes are configured there, not here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
- category: Ticket status
  central: true
  edge: true
  device: true
  offline: Available
- category: Membership tier
  central: true
  edge: true
  device: true
  offline: Available
- category: Live occupancy
  central: true
  edge: true
  device: '-'
  offline: Conditional (cached, max 15 min)
- category: Live fraud AI
  central: true
  edge: '-'
  device: '-'
  offline: Unavailable - require operator review
distribution:
  central: Policy set 3.5
  edge: AP-EDGE-01 3.5 (10:21)
  devices: Main Plaza handhelds 3.4 (awaiting refresh)
```

#### Permissions

- `listPolicyEvaluationArchitecture` → `SCOPE_VIEW` (read) · staff
- `setPolicyEvaluationSetting` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-241` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-241`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 14: Works in Policy Evaluation Architecture & Offline Distribution → Define where and how policies are evaluated. This screen connects Board 10 with the offline/edge architecture already configured in Board 7.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-241?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save policy evaluation setting.
- [ ] Every transition is wired: `BO-234`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-242` Policy Simulation, Conflict & Impact Analysis

**Test policies before they affect live guest admission.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/policy-simulation-conflict-impact-analysis-bo-242` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Tests a policy version before it reaches live gates: a simulated person and moment (Gold member, Adventure Park ticket, VIP lounge, Friday 19:15, occupancy 82%, low risk) produce an evaluation trace (each policy PASS / FAIL) and a final result; conflicts are detected (Gold members Allow vs private event Deny non-event credentials) with policies, hierarchy, priority, resulting decision, affected products, venues and guests; impact ("affects 12,480 active credentials across 3 venues") and regression against saved scenarios ("148: 145 passed, 3 changed outcome"). The one thing to get right: results are results - the trace, conflicts and counts are outputs of the run, and changed outcomes are listed one by one.

**Known correction pending (do not draw the wrong version)**

- **The request carries the results (scenarioCount, passedCount, changedOutcomeCount, affectedCredentials) and the table binds result columns to the run operation** Why: These are what the run returns; the response needs the trace, conflicts and counts. *(source: contracts/spine/access.yaml#simulatePolicyConflictImpact; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The simulated person has only a credential id and a time** Why: The pack simulates by attributes (membership, location, occupancy, risk) without a real ticket. *(source: screens/P08-venue-back-office.yaml#BO-242; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Run simulation button has no operation; simulation is a PUT** Why: Bind it; a run is a new result, not an upsert. *(source: screens/P08-venue-back-office.yaml#BO-242 / contracts/spine/access.yaml#simulatePolicyConflictImpact; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation stores saved regression scenarios** Why: Regression testing needs a scenario library. *(source: screens/P08-venue-back-office.yaml#BO-243; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **policyId / policyVersion**: Policy and version picker (draft versions included), preset when opened from BO-236. *(source: contracts/spine/access.yaml#simulatePolicyConflictImpact)*
- **Simulated person and context**: Either a real ticket (credential search) or a made-up guest - identity type, membership tier, accreditation, ticket product - plus location (tree), date and time (scenarioTime), occupancy % and risk band. Only ticket and time exist in the contract (see corrections). *(source: screens/P08-venue-back-office.yaml#BO-242 / contracts/spine/access.yaml#simulatePolicyConflictImpact)*
- **runSavedScenarios**: "Also run saved scenarios (regression)" toggle, on by default before approval. *(source: screens/P08-venue-back-office.yaml#BO-243 / contracts/spine/access.yaml#simulatePolicyConflictImpact)*

#### Outputs: what the screen shows and produces

**Shown**

**Every policy simulation conflict** (data table, from `simulatePolicyConflictImpact`)

| Shows | Format | Notes |
|---|---|---|
| Policies involved | list or chips (count when long) | policies involved |
| Hierarchy | text | hierarchy |
| Priority | 1,234 | priority |
| Resulting decision | chip: Allow, Deny, Review, Require ID, Require biometric, Require companion… | resulting decision |
| Affected products | 1,234 | affected products |
| Affected venues | 1,234 | affected venues |

**The selected policy simulation conflict** (detail panel): The pack groups this record's detail under its own headings: “Time”, “Occupancy”, “Credential Active”, “Gold Membership”, “VIP Lounge Access”, “Capacity Restriction”.

| Shows | Format | Notes |
|---|---|---|
| Policies involved | list or chips (count when long) | policies involved |
| Hierarchy | text | hierarchy |
| Priority | 1,234 | priority |
| Resulting decision | chip: Allow, Deny, Review, Require ID, Require biometric, Require companion… | resulting decision |
| Affected products | 1,234 | affected products |
| Affected venues | 1,234 | affected venues |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run simulation (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Evaluation trace**: Each policy in evaluation order with its level, priority and PASS / FAIL, then FINAL RESULT in the result colour. *(source: screens/P08-venue-back-office.yaml#BO-242)*
- **Conflicts**: Policies involved, hierarchy, priority, resulting decision, affected products, affected venues, estimated guests impacted; red POLICY CONFLICT header. *(source: screens/P08-venue-back-office.yaml#BO-242 / screens/P08-venue-back-office.yaml#BO-243)*
- **Impact and regression**: "This version affects 12,480 active credentials across 3 venues"; "148 scenarios - 145 passed, 3 changed outcome" with the three listed (scenario, old result, new result). *(source: screens/P08-venue-back-office.yaml#BO-243 / contracts/spine/access.yaml#simulatePolicyConflictImpact)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Run simulation**: Evaluates without a real transaction, attendance or entitlement change; the run is attached to the version for approval (BO-243). *(source: DI-629 / contracts/spine/access.yaml#simulatePolicyConflictImpact)*
- **Save as scenario**: Keeps the inputs and expected result for future regression runs; greyed until bound. *(source: screens/P08-venue-back-office.yaml#BO-243)*

**Where the user goes next**

- → `BO-234` Dynamic Access Policy Command Center: *Returns to the board's landing screen*; calls `simulatePolicyConflictImpact`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy simulation conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy simulation conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy simulation conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the policy simulation conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-163`: Rule simulation (board 2) uses the same virtual scan inputs and trace layout.
- Match `BO-243`: Impact and regression figures here are those shown at approval.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
input:
  guest: Gold member
  ticket: Summit Peaks Day Pass
  location: Summit Peaks VIP Lounge
  time: Fri 2 Oct 2026 19:15
  occupancy: 82%
  risk: Low
trace:
- Credential active - PASS
- Gold membership - PASS
- VIP Lounge access - PASS
- Capacity restriction - PASS
- FINAL RESULT - ACCESS ALLOWED
conflict:
  a: Gold members - Allow (Membership, priority 60)
  b: Private corporate event - Deny non-event credentials (Venue restriction, priority 80)
  decision: Deny
  guests: 1240
regression:
  scenarios: 148
  passed: 145
  changed: 3
```

#### Permissions

- `simulatePolicyConflictImpact` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-242` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-242`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 16: Works in Policy Simulation, Conflict & Impact Analysis → Test policies before they affect live guest admission.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-242?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run simulation.
- [ ] Every transition is wired: `BO-234`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-243` Policy Approval, Audit, Analytics & AI Optimization

**Govern the complete policy lifecycle and continuously measure policy effectiveness.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task APP-SETUP-BO-243 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `SCOPE_VIEW` (1 configure, 2 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor; Measure) and no metric row |
| Offline | online only |
| Opens with | `policyId` (navigation), `requestId` (navigation) |
| Route | `/access-venue/policy-approval-audit-analytics-ai-optimization-bo-243` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): listPolicies reads the white-label legal policies (privacy, terms, refund, cookie), the wrong domain; access policies come from listDynamicAccessPolicy and …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Governs the access policy lifecycle (Draft > Test > Impact analysis > Approval > Schedule > Publish > Monitor > Optimise > Retire) and measures each policy's effect: denial rate, override rate, false-positive indicators, operator review rate, guest impact, security incidents. Business, security and technical approval stages; versions with rollback. The one thing to get right: impact before publish ("affects 12,480 active credentials across 3 venues"; regression "148 scenarios, 145 passed, 3 changed outcome").

**Known correction pending (do not draw the wrong version)**

- **Buttons labelled "Policy Owner", "Business Approval", "Security Approval", "Technical Approval" and "ROLLBACK TO V3.4"; a column labelled "→"** Why: Approval stages and a sample version were turned into buttons and a column; draw stages as the approval chain and Rollback with a version picker. *(source: screens/P08-venue-back-office.yaml#BO-243; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation exit to BO-234 has no transitions defined** Why: Board return should be explicit like the other board screens (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-243; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): listPolicies (white-label legal policies - privacy, terms, refund, cookie) is bound as the screen's main read (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listDynamicPolicyEffectiveness` ?from |
| To | date and time picker | — | — | `listDynamicPolicyEffectiveness` ?to |
| Policy | picker: choose a policy | — | — | `listDynamicPolicyEffectiveness` ?policyId |
| Policy type | select | — | Guest attribute · Accreditation · Occupancy · Employee · Risk · Membership · Time event | `listDynamicPolicyEffectiveness` ?policyType |

**Sent by *ROLLBACK TO V3.4*** (`rollbackAccessPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target version `targetVersion` | number field | required | — | min 1 | — | The version whose content is restored | `rollbackAccessPolicy` body |
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | — | `rollbackAccessPolicy` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Approval decision**: Approve, Reject (reason required), Return, Request information; the requester cannot approve their own; MFA step-up where the rule demands it. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **Rollback**: Pick a previous version from the history and a reason (max 300); restoring creates a new version that goes through the same approval route. *(source: contracts/spine/access.yaml#rollbackAccessPolicy)*
- **Effectiveness period**: From-to dates (required by the read), default last 30 days. *(source: contracts/spine/access.yaml#listDynamicPolicyEffectiveness)*

#### Outputs: what the screen shows and produces

**Shown**

**The selected policy approval audit** (detail panel): The pack groups this record's detail under its own headings: “Draft”, “Test”, “Impact Analysis”, “Approval”, “Schedule”, “Publish”.

| Shows | Format | Notes |
|---|---|---|
| → | text | not in the schema: `→` |
| Denial rate | text | not in the schema: `Denial Rate` |
| Override rate | text | not in the schema: `Override Rate` |
| False positive indicators | text | not in the schema: `False-Positive Indicators` |
| Operator review rate | text | not in the schema: `Operator Review Rate` |
| Guest impact | text | not in the schema: `Guest Impact` |
| Security incidents | text | not in the schema: `Security Incidents` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Policy Owner (primary button) | navigation or local | — | — | — | — |
| Business Approval (secondary button) | navigation or local | — | — | — | — |
| Security Approval (secondary button) | navigation or local | — | — | — | — |
| Technical Approval (secondary button) | navigation or local | — | — | — | — |
| ROLLBACK TO V3.4 (destructive button) | `rollbackAccessPolicy` POST `/dynamic-access-policy/{policyId}/rollback` | inline | DynamicAccessPolicyCommandCenterView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 targetVersion is the current version, or does not exist for this policy | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lifecycle rail**: The nine stages as a horizontal rail with the policy's current stage highlighted. *(source: screens/P08-venue-back-office.yaml#BO-243)*
- **Effectiveness table**: Per policy - triggers, allow/deny/review counts, denial rate, override rate (overrides of its denials), trend sparkline. *(source: contracts/spine/access.yaml#listDynamicPolicyEffectiveness)*
- **Impact and regression**: Before approval, show credentials, products and venues affected and the saved-scenario regression result. *(source: screens/P08-venue-back-office.yaml#BO-243)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Send for approval**: Raises an approval request referencing the policy version (configuration change kind). *(source: contracts/spine/approvals.yaml#createApprovalRequest)*
- **Roll back to version N**: Confirmation names the version and that a new version will be created and approved. *(source: contracts/spine/access.yaml#rollbackAccessPolicy)*

**Data it reads**: `listDynamicAccessPolicy` (onLoad, The access policies awaiting approval, with their versions); `listDynamicPolicyEffectiveness` (onLoad, Per-policy triggers, denials, overrides and trend over a …)

**What opens over it**

- confirmDialog *ROLLBACK TO V3.4*: **ROLLBACK TO V3.4 on a policy approval audit is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy approval audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy approval audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy approval audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the policy approval audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem); 409 The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and … (ApprovalStateProblem); 409 targetVersion is the current version, or does not exist for this … |

#### Edge cases to draw

- **A decision made under an old version is questioned**: History keeps every version; each scan records the version that decided it. *(source: ADR-0068 / contracts/spine/access.yaml#rollbackAccessPolicy)*

#### Consistency with other screens

- Match `BO-234`: Same statuses and health badges.
- Match `BO-367`: Approval actions use the platform approval inbox wording (cross-process, platform).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  name: Peak Capacity Control
  version: 3.5
  stage: Approval
  impact: 12,480 active credentials across 3 venues
  regression: '148 scenarios: 145 passed, 3 changed outcome'
  denialRate: 4.2%
  overrideRate: 0.6%
```

#### Permissions

- `listDynamicAccessPolicy` → `SCOPE_VIEW` (read) · staff
- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `decideApprovalRequest` → `APPROVAL_DECIDE` (operate) · staff, public
- `rollbackAccessPolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listDynamicPolicyEffectiveness` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.47 | Access Analytics Dashboard - System shall provide dashboards for access policy analytics. | Admission and Access | CONTRACTED | `listDynamicAccessPolicy` |
| 1.1.59 | Complimentary entitlement redemption | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.64 | Employees shall submit requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.65 | Managers shall approve requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 11.1.51 | Draft Approval Requests - System shall support saving approval requests in draft status. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.63 | API-Based Approval Processing - System shall expose approval workflows through APIs. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.20 | Approval Comments - System shall allow approvers to add comments to approval decisions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.21 | Approval Rejection Reasons - System shall require rejection reasons when approvals are denied. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.57 | Digital Signature Support - System shall support digital signatures for sensitive approvals. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.59 | Approval Authentication - System shall require authentication before approval actions are executed. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.60 | MFA-Protected Approvals - System shall support MFA requirements for sensitive approval actions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.61 | Sensitive Action Confirmation - System shall require confirmation before execution of sensitive approvals. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-243` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS27 Access Control Board 10.dc.html#bo-243`
- Workshop pack: Access Control Module_Reference.pdf board 10
- Flow F120 *Access Control board 10: Dynamic Access Policy Command Center*, step 18: Works in Policy Approval, Audit, Analytics & AI Optimization → Govern the complete policy lifecycle and continuously measure policy effectiveness.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-243?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Policy Owner, Business Approval, Security Approval, Technical Approval, ROLLBACK TO V3.4.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"decideApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/decide","contract":"approvals","summary":"Approve, reject, return or ask for information","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"listAccessAttributeCatalog": {"method":"GET","path":"/access-attribute-catalog","contract":"access","summary":"Access Attribute Catalog","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessAttributeCatalogView"},
"listAuthorizationGovernanceTemporary": {"method":"GET","path":"/authorization-governance-temporary","contract":"access","summary":"Authorization Governance & Temporary Access","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicAccessPolicy": {"method":"GET","path":"/dynamic-access-policy","contract":"access","summary":"Dynamic Access Policy Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicPolicyEffectiveness": {"method":"GET","path":"/dynamic-policy-effectiveness","contract":"access","summary":"How each gate admission policy has behaved over a period","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"policyId","in":"query","required":null},{"name":"policyType","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listIdentityMembershipAccreditation": {"method":"GET","path":"/identity-membership-accreditation","contract":"access","summary":"Identity, Membership & Accreditation Policies","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"IdentityMembershipAccreditationPoliciesView"},
"listPolicyEvaluationArchitecture": {"method":"GET","path":"/policy-evaluation-architecture","contract":"access","summary":"Policy Evaluation Architecture & Offline Distribution","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PolicyEvaluationArchitectureOfflineDistributionView"},
"listPolicyScopeHierarchy": {"method":"GET","path":"/policy-scope-hierarchy","contract":"access","summary":"Policy Scope, Hierarchy & Inheritance","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PolicyScopeHierarchyInheritanceView"},
"rollbackAccessPolicy": {"method":"POST","path":"/dynamic-access-policy/{policyId}/rollback","contract":"access","summary":"Put a previous policy version back","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DynamicAccessPolicyCommandCenterView"},
"setAccessAttributeCatalog": {"method":"PUT","path":"/access-attribute-catalog","contract":"access","summary":"Add or amend an access attribute","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessAttributeCatalogInput","responds":"AccessAttributeCatalogView"},
"setAccessProfile": {"method":"PUT","path":"/accreditation-access-profiles","contract":"accreditation","summary":"Define which zones, on which dates, at which times","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessProfile","responds":"AccessProfile"},
"setContextTimeEvent": {"method":"PUT","path":"/context-time-event","contract":"access","summary":"Context, Time, Event & Capacity Policy Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ContextTimeEventCapacityPolicyBuilderInput","responds":"ContextTimeEventCapacityPolicyBuilderView"},
"setPolicyEvaluationSetting": {"method":"PUT","path":"/policy-evaluation-settings","contract":"access","summary":"Set where and how a policy category is evaluated","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessPolicyEvaluationSetting","responds":"AccessPolicyEvaluationSetting"},
"setPolicyScopeHierarchy": {"method":"PUT","path":"/policy-scope-hierarchy","contract":"access","summary":"Place a policy in the scope hierarchy","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PolicyScopeHierarchyInheritanceInput","responds":"PolicyScopeHierarchyInheritanceView"},
"setVisualDynamicPolicy": {"method":"PUT","path":"/visual-dynamic-policy","contract":"access","summary":"Visual Dynamic Policy Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualDynamicPolicyBuilderInput","responds":"VisualDynamicPolicyBuilderView"},
"simulatePolicyConflictImpact": {"method":"PUT","path":"/policy-conflict-impact","contract":"access","summary":"Policy Simulation, Conflict & Impact Analysis","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PolicySimulationConflictImpactAnalysisInput","responds":"PolicySimulationConflictImpactAnalysisView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAttributeCatalogInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Access Attribute Catalog submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["attributeKey","category","label","dataType"],"properties":{"attributeKey":{"type":"string","pattern":"^[a-z][a-zA-Z0-9]*(\\.[a-z][a-zA-Z0-9]*)*$","maxLength":100,"description":"Stable key a policy condition names, e.g. guest.tier. Unique within the tenant"},"category":{"type":"string","enum":["guest","credential","employee","location","time","operational","device","risk"]},"label":{"type":"string","maxLength":200},"dataType":{"type":"string","enum":["string","integer","number","boolean","date","dateTime","enum"]},"allowedValues":{"type":"array","items":{"type":"string"},"description":"Required when dataType is enum"},"enabled":{"type":"boolean","default":true}}},
"AccessAttributeCatalogView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Attribute Catalog displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"category":{"type":"string","enum":["guest","credential","employee","location","time","operational","device","risk"]},"attributeKey":{"type":"string","description":"Dotted governed key, e.g. membership.tier"},"label":{"type":"string"},"dataType":{"type":"string","enum":["string","integer","number","boolean","date","dateTime","enum"]},"allowedValues":{"type":"array","items":{"type":"string"},"description":"For enum attributes, e.g. Standard, Silver, Gold, Platinum"},"enabled":{"type":"boolean","description":"Whether the venue may use this attribute in policies (e.g. gender or residency only where legally and business permitted)"}},"required":["attributeKey","category"]},
"AccessDynamicPolicyEffectiveness": {"type":"object","x-ticvai-persistence":"none — computed from access.scan_event (dynamicPolicyId, dynamicPolicyResult and override rows) over the requested period, joined to access.dynamic_policy","description":"One gate admission policy over a period (3.3.48; decided 29 September, build pass).","required":["policyId","triggers"],"properties":{"policyId":{"type":"string","format":"uuid"},"policyName":{"type":"string"},"policyType":{"type":"string","enum":["guestAttribute","accreditation","occupancy","employee","risk","membership","timeEvent"]},"status":{"type":"string","enum":["draft","pendingApproval","active","inactive","expired"]},"versionsInPeriod":{"type":"array","items":{"type":"integer"},"description":"The versions that decided a scan in the period."},"triggers":{"type":"integer","minimum":0,"description":"Scans this policy decided."},"allowed":{"type":"integer","minimum":0},"denied":{"type":"integer","minimum":0},"sentToReview":{"type":"integer","minimum":0},"steppedUp":{"type":"integer","minimum":0,"description":"Scans the policy sent to requireId, requireBiometric, requireCompanion or requireSupervisor."},"overridden":{"type":"integer","minimum":0,"description":"Denials a supervisor then admitted against (an override row naming the denied scan)."},"overrideRatePercent":{"type":"number","minimum":0,"maximum":100,"nullable":true,"description":"overridden over denied; null when nothing was denied."},"lastTriggeredAt":{"type":"string","format":"date-time","nullable":true},"neverTriggered":{"type":"boolean","description":"Active through the period and decided nothing."},"trend":{"type":"array","description":"One point per day in the period, in the venue's time zone.","items":{"type":"object","properties":{"date":{"type":"string","format":"date"},"triggers":{"type":"integer"},"denied":{"type":"integer"},"overridden":{"type":"integer"}}}}}},
"AccessPolicyEvaluationSetting": {"type":"object","x-ticvai-persistence":"access.policy_evaluation_setting","description":"Where and how one policy category is evaluated - evaluation mode, supported locations, offline behaviour and the oldest cached data an offline evaluation may use (declared 29 September, data-model close-out DM1).","required":["id","scopePath","policyCategory","evaluationMode"],"properties":{"id":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"policyCategory":{"type":"string","maxLength":100,"description":"e.g. Ticket Status, Time Rule, Membership Tier, Live Occupancy, Live Fraud AI. Unique per scope"},"evaluationMode":{"type":"string","enum":["central","edge","device","hybrid"]},"supportedLocations":{"type":"array","items":{"type":"string","enum":["central","edge","device"]}},"offlineBehaviour":{"type":"string","enum":["available","conditional","unavailable"],"nullable":true},"maxDataAgeMinutes":{"type":"integer","minimum":0,"nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessProfile": {"type":"object","x-ticvai-persistence":"accreditation.access_profile","description":"Board 5.2. **How an estate stays governable.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"zoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"operationalAreas":{"type":"array","items":{"type":"string"}},"schedule":{"type":"array","description":"**Zone, date and time are three dimensions and all three are needed.**","items":{"type":"object","properties":{"zoneId":{"type":"string","format":"uuid","nullable":true},"daysOfWeek":{"type":"array","items":{"type":"string"}},"dateFrom":{"type":"string","format":"date","nullable":true},"dateTo":{"type":"string","format":"date","nullable":true},"from":{"type":"string","nullable":true},"to":{"type":"string","nullable":true},"eventPhase":{"type":"string","nullable":true,"enum":["build","rehearsal","doorsOpen","liveShow","breakdown"]}}}},"escortRequired":{"type":"boolean","default":false},"holderCount":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"AdmissionRule": {"type":"object","x-ticvai-persistence":"none — embedded as the jsonb column condition_rule of access.dynamic_policy, and in each access.dynamic_policy_version definition","description":"**One rule format that runs on both sides** (ADR-0068, accepted 1 October). A guest-admission condition was free text (`conditionExpression`, \"AND, OR, NOT, IN and BETWEEN\"), which a .NET server and a TypeScript gate cannot be relied on to read the same way. This is a closed JSON format instead: every condition is drawn from the `policyType` and `contextType` enums already on `AccessDynamicPolicy`, with a fixed set of comparators, so `validateAccess` online and the gate offline evaluate the same active version to the same answer. **One evaluator in .NET and one in TypeScript, proven equal by a shared set of test vectors in CI** (ACC-RULE-EVAL, B1 with the scanner).\n\n`match` combines `conditions` and `groups` (`all` is AND, `any` is OR); each group is its own `all` or `any` over its conditions and counts as one condition of the rule; `negate` is NOT. **Two levels and no more**: every rule the Access Control pack shows fits in them, and a deeper tree is refused `400` rather than approximated. A rule that needs more than the closed set extends the set; free text does not come back (ADR-0068, Revisit).","required":["match","conditions"],"properties":{"formatVersion":{"type":"integer","enum":[1],"default":1,"description":"The rule format's version. An evaluator refuses a version it does not know rather than guess."},"match":{"type":"string","enum":["all","any"]},"conditions":{"type":"array","minItems":1,"maxItems":50,"items":{"$ref":"#/components/schemas/AdmissionCondition"}},"groups":{"type":"array","maxItems":10,"items":{"type":"object","required":["match","conditions"],"properties":{"match":{"type":"string","enum":["all","any"]},"negate":{"type":"boolean","default":false},"conditions":{"type":"array","minItems":1,"maxItems":50,"items":{"$ref":"#/components/schemas/AdmissionCondition"}}}}}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"AuthorizationGovernanceTemporaryAccessView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Authorization Governance & Temporary Access displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"validFrom":{"type":"string","format":"date-time"},"grantType":{"type":"string","enum":["temporary","emergency","delegatedAdministration"]},"grantId":{"type":"string"},"scope":{"type":"string","description":"scope"},"validTo":{"type":"string","format":"date-time","description":"duration"},"reason":{"type":"string","description":"reason"},"approver":{"type":"string","description":"approver"},"granteeUserId":{"type":"string"},"status":{"type":"string","enum":["pendingApproval","active","expired","revoked"]}},"required":["grantId","grantType","scope","validFrom","validTo","reason"]},
"ContextTimeEventCapacityPolicyBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Context, Time, Event & Capacity Policy Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`). For example: Zone Occupancy >= 90% AND Day = Friday AND Time BETWEEN 18:00 AND 23:59."},"name":{"type":"string"},"policyId":{"type":"string"},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"description":"Kind of venue condition the policy reacts to"},"monitorThresholdPercent":{"type":"integer","description":"Occupancy percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","description":"Occupancy percent at which the band becomes Restrict"},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"`inactive` switches the policy off at once; `active` on a new or inactive policy submits it for approval (`pendingApproval`) (decided 29 September, writers pass)"},"validFrom":{"type":"string","format":"date-time","nullable":true,"description":"Start of validity; null for at once (decided 29 September, writers pass)"},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"End of validity: after it a timer moves the policy to `expired` (decided 29 September, writers pass)"}},"required":["policyId","name","contextType","conditionRule","result"]},
"ContextTimeEventCapacityPolicyBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Context, Time, Event & Capacity Policy Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`). For example: Zone Occupancy >= 90% AND Day = Friday AND Time BETWEEN 18:00 AND 23:59."},"name":{"type":"string"},"policyId":{"type":"string"},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"description":"Kind of venue condition the policy reacts to"},"monitorThresholdPercent":{"type":"integer","description":"Occupancy percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","description":"Occupancy percent at which the band becomes Restrict"}},"required":["policyId","name","contextType","conditionRule","result"]},
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"DynamicAccessPolicyCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Dynamic Access Policy Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"version":{"type":"integer","minimum":1,"description":"Current version. `rollbackAccessPolicy` restores an earlier one as a new version (decided 29 September, VM close-out)"},"policyId":{"type":"string"},"policyName":{"type":"string","description":"e.g. VIP Backstage Event"},"scope":{"type":"string","description":"Where the policy applies, e.g. a venue, park or all venues"},"policyType":{"type":"string","enum":["guestAttribute","accreditation","occupancy","employee","risk","membership","timeEvent"]},"priority":{"type":"integer"},"status":{"type":"string","enum":["draft","pendingApproval","active","inactive","expired"]}},"required":["policyId"]},
"DynamicAccessPolicyCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activePolicies":{"type":"integer","description":"Active Policies"},"draftPolicies":{"type":"integer","description":"Draft Policies"},"policiesPendingApproval":{"type":"integer","description":"Policies Pending Approval"},"policiesTriggeredToday":{"type":"integer","description":"Policies Triggered Today"},"allowDecisions":{"type":"integer","description":"Allow Decisions"},"denyDecisions":{"type":"integer","description":"Deny Decisions"},"reviewDecisions":{"type":"integer","description":"Review decisions today"},"policyConflicts":{"type":"integer","description":"Policy Conflicts"},"expiringPolicies":{"type":"integer","description":"Expiring Policies"},"aiRecommendations":{"type":"integer","description":"AI Recommendations"}}},
"IdentityMembershipAccreditationPoliciesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Identity, Membership & Accreditation Policies displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"policyId":{"type":"string"},"identityType":{"type":"string","enum":["guest","member","annualPassHolder","employee","contractor","vendor","performer","media","vip","security","emergencyServices","eventStaff"],"description":"Who the requesting person is"},"validTo":{"type":"string","format":"date-time","description":"until"},"name":{"type":"string","description":"e.g. Event Crew, Level 3"},"allowedZones":{"type":"array","items":{"type":"string"}},"deniedZones":{"type":"array","items":{"type":"string"}},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`). For example: Employee Status = Active AND Current Shift = Active."},"validFrom":{"type":"string","format":"date-time"}},"required":["policyId","identityType"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PolicyEvaluationArchitectureOfflineDistributionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Policy Evaluation Architecture & Offline Distribution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"evaluationMode":{"type":"string","enum":["central","edge","device","hybrid"]},"policyCategory":{"type":"string","description":"e.g. Ticket Status, Time Rule, Membership Tier, Live Occupancy, Live Fraud AI"},"supportedLocations":{"type":"array","items":{"type":"string"},"description":"Any of central, edge, device"},"offlineBehaviour":{"type":"string","enum":["available","conditional","unavailable"]},"maxDataAgeMinutes":{"type":"integer","description":"Oldest cached data an offline evaluation may use"}},"required":["policyCategory","evaluationMode"]},
"PolicyScopeHierarchyInheritanceInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Policy Scope, Hierarchy & Inheritance submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["policyId","scopeLevel","scopeId","policyCategory","conflictResolution"],"properties":{"policyId":{"type":"string","description":"The dynamic access policy placed in the hierarchy"},"scopeLevel":{"type":"string","enum":["tenant","venue","park","zone","attraction","accessPoint"]},"scopeId":{"type":"string"},"policyCategory":{"type":"string","enum":["emergency","securityFraud","regulatorySafety","venueRestriction","accreditation","membership","standardAccess"]},"categoryRank":{"type":"integer","minimum":1,"description":"Lower wins; emergency is 1"},"conflictResolution":{"type":"string","enum":["highestPriorityWins","denyOverridesAllow","mostSpecificWins","mandatoryParentWins","explicitResolution"],"default":"denyOverridesAllow"},"mandatory":{"type":"boolean","default":false,"description":"A child scope cannot override a mandatory policy"}}},
"PolicyScopeHierarchyInheritanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Policy Scope, Hierarchy & Inheritance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"scopeId":{"type":"string"},"scopeLevel":{"type":"string","enum":["tenant","venue","park","zone","attraction","accessPoint"]},"policyId":{"type":"string"},"conflictResolution":{"type":"string","enum":["highestPriorityWins","denyOverridesAllow","mostSpecificWins","mandatoryParentWins","explicitResolution"],"description":"How a conflict with another policy is resolved"},"policyCategory":{"type":"string","enum":["emergency","securityFraud","regulatorySafety","venueRestriction","accreditation","membership","standardAccess"]},"categoryRank":{"type":"integer","description":"Configurable precedence of the category; 1 wins"},"mandatory":{"type":"boolean","description":"Parent policy that overrides local permissions below it"}},"required":["policyId","scopeLevel","scopeId"]},
"PolicySimulationConflictImpactAnalysisInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Policy Simulation, Conflict & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"policyId":{"type":"string"},"policyVersion":{"type":"string"},"scenarioTime":{"type":"string","format":"date-time","description":"Simulated moment of the scan"},"credentialId":{"type":"string","description":"Optional credential to simulate"},"runSavedScenarios":{"type":"boolean","description":"Regression: run saved scenarios against this policy version"},"scenarioCount":{"type":"integer"},"passedCount":{"type":"integer"},"changedOutcomeCount":{"type":"integer"},"affectedCredentials":{"type":"integer"}},"required":["policyId"]},
"PolicySimulationConflictImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Policy Simulation, Conflict & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"policyId":{"type":"string"},"occupancy":{"type":"integer","description":"Occupancy (the pack shows 82%)"},"policiesInvolved":{"type":"array","items":{"type":"string"},"description":"policies involved"},"hierarchy":{"type":"string","description":"hierarchy"},"priority":{"type":"integer","description":"priority"},"resultingDecision":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"description":"resulting decision"},"affectedProducts":{"type":"integer","description":"affected products"},"affectedVenues":{"type":"integer","description":"affected venues"},"estimatedGuestsImpacted":{"type":"integer","description":"estimated guests impacted"},"policyVersion":{"type":"string"},"scenarioTime":{"type":"string","format":"date-time","description":"Simulated moment of the scan"},"credentialId":{"type":"string","description":"Optional credential to simulate"},"runSavedScenarios":{"type":"boolean","description":"Regression: run saved scenarios against this policy version"},"scenarioCount":{"type":"integer"},"passedCount":{"type":"integer"},"changedOutcomeCount":{"type":"integer"},"affectedCredentials":{"type":"integer"}},"required":["policyId"]},
"VisualDynamicPolicyBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Visual Dynamic Policy Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`). For example: Accreditation = VIP AND Zone = Backstage."},"name":{"type":"string","description":"e.g. VIP Backstage Access"},"policyId":{"type":"string"},"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"description":"Decision the policy returns when its condition holds"},"priority":{"type":"integer"},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"`inactive` switches the policy off at once; `active` on a new or inactive policy submits it for approval (`pendingApproval`) (decided 29 September, writers pass)"},"validFrom":{"type":"string","format":"date-time","nullable":true,"description":"Start of validity; null for at once (decided 29 September, writers pass)"},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"End of validity: after it a timer moves the policy to `expired` (decided 29 September, writers pass)"}},"required":["policyId","name","conditionRule","result"]},
"VisualDynamicPolicyBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Visual Dynamic Policy Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`). For example: Accreditation = VIP AND Zone = Backstage."},"name":{"type":"string","description":"e.g. VIP Backstage Access"},"policyId":{"type":"string"},"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"description":"Decision the policy returns when its condition holds"},"priority":{"type":"integer"}},"required":["policyId","name","conditionRule","result"]}
}
```
