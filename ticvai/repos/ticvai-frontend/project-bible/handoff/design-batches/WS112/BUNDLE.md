# WS112 — ACCREDITATION board 5

**10 screens · 6 operations · 4 schemas · 3 permissions**

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
  `ACCREDITATION_CONFIGURE, ACCREDITATION_MANAGE, ACCREDITATION_VIEW`. A control nobody can use must say so,
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
| `BO-654` | Accreditation Access Command Center | D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-655` | Access Profile Management | D | 9 | 0 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `BO-656` | Venue & Zone Access Matrix | D | 0 | 16 | 6 | 6 | 1 | 0 | — | notStarted (—) |
| `BO-657` | Operational Area Permission Management | D | 0 | 16 | 6 | 6 | 1 | 5 | — | notStarted (—) |
| `BO-658` | Date & Time Access Rules | D | 0 | 16 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `BO-659` | Access Schedule Management | D | 0 | 0 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `BO-660` | Holder Access Assignment | D | 0 | 50 | 6 | 7 | 0 | 0 | — | notStarted (—) |
| `BO-661` | Temporary Access & Exception Management | D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-662` | Access Revocation & Suspension | D | 0 | 0 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `BO-663` | Access Rights Preview, Impact & Synchronization | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-656, BO-657, BO-658, BO-659, BO-661, BO-662, BO-663 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-654` Accreditation Access Command Center

**Central operational dashboard for accreditation access permissions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-654 |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Dashboard KPIs shall include) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-access-command-center-bo-654` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The landing page of the access-rights board: how many accredited people can go where, what is about to lapse, and what needs action (unassigned approved credentials, exceptions, suspended access). Used by the accreditation manager before and during an event. Per VO-R02 it is one dashboard pattern with KPI tiles, an alert list and quick actions into the board's screens. The one thing to get right: it governs who may enter which zone; it does not monitor people on site, which per DI-672 is a filter inside entitlement monitoring.

**Known correction pending (do not draw the wrong version)**

- **Event, Venue, Accreditation program, Category, Organization, Zone, Access profile and Credential status are drawn as metric tiles** Why: On the pack page they are the "Users shall be able to filter by" list; they are filters, not KPIs. *(source: screens/P08-venue-back-office.yaml#BO-655 / screens/P08-venue-back-office.yaml#BO-654; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The only bound read is listAccessProfiles** Why: It gives profile counts and holderCount; eight of the ten KPIs (temporary grants, expiring permissions, suspended, revoked, exceptions, unassigned approved credentials) need holder, credential and holder-access counts that no bound read returns. Needs getKpiValues with accreditation access codes or a summary read. *(source: screens/P08-venue-back-office.yaml#BO-654 / contracts/satellite/accreditation.yaml#listAccessProfiles; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's quick actions (Create Access Profile, Assign Access, Temporary Grant, Revoke Access, View Access Matrix) are not on the screen** Why: Only navigation tiles exist; the actions are what the board is for. *(source: screens/P08-venue-back-office.yaml#BO-655; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **filters (Event, Venue, Accreditation programme, Category, Organisation, Zone, Access profile, Credential status)**: A filter bar above the tiles, not tiles. Venue defaults to the top-bar venue (per VO-R09) and is shown as a removable chip only for users whose scope spans several venues. Category and Credential status are closed sets (chips); Event, Programme, Organisation, Zone and Access profile are searchable selects. Filters apply to every tile and the alert list. *(source: screens/P08-venue-back-office.yaml#BO-655)*

#### Outputs: what the screen shows and produces

**Shown**

**Active access profiles** (metric tile)

**Accredited holders with access** (metric tile)

**Credentials with assigned access** (metric tile)

**Restricted-access holders** (metric tile)

**Temporary access grants** (metric tile)

**Expiring permissions** (metric tile)

**Suspended access** (metric tile)

**Revoked access** (metric tile)

**Access exceptions** (metric tile)

**Unassigned approved credentials** (metric tile)

**Event** (metric tile)

**Venue** (metric tile)

**Accreditation program** (metric tile)

**Category** (metric tile)

**Organization** (metric tile)

**Zone** (metric tile)

**Access profile** (metric tile)

**Credential status** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Ten tiles, in the pack's order: Active access profiles, Accredited holders with access, Credentials with assigned access, Restricted-access holders, Temporary access grants, Expiring permissions (next 7 days), Suspended access, Revoked access, Access exceptions, Unassigned approved credentials. Each shows the count and its change since yesterday; tiles that need action (Unassigned approved credentials, Access exceptions, Expiring permissions) carry an amber state above zero. Each tile opens its detail screen filtered. *(source: screens/P08-venue-back-office.yaml#BO-654 / screens/P08-venue-back-office.yaml#BO-655)*
- **Alerts**: A short list of items needing action, each with a deep link: approved holders with no credential or no access profile, temporary grants ending in the next 2 hours, profiles changed but not yet published to Access, holders left with no access after a profile change. *(source: screens/P08-venue-back-office.yaml#BO-654 / contracts/satellite/accreditation.yaml#/components/schemas/AccessImpact)*
- **On-site accredited holders**: Not drawn here. A link "See accredited holders on site" opens the Visit, Admission & Entitlement Usage Monitor (BO-297) with the accreditation filter applied. *(source: DI-672 / DI-694)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Quick actions**: Create access profile (BO-655, empty), Assign access (BO-660, holder picker first), Temporary grant (BO-661), Revoke access (BO-662, holder picker first), View access matrix (BO-656). Each returns here. *(source: screens/P08-venue-back-office.yaml#BO-655 / F221 step 1)*

**Data it reads**: `listAccessProfiles` (onLoad, Access at a glance)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-655` Access Profile Management: *Access Profile Management*
- → `BO-656` Venue & Zone Access Matrix: *Venue & Zone Access Matrix*
- → `BO-657` Operational Area Permission Management: *Operational Area Permission Management*
- → `BO-658` Date & Time Access Rules: *Date & Time Access Rules*
- → `BO-659` Access Schedule Management: *Access Schedule Management*
- → `BO-660` Holder Access Assignment: *Holder Access Assignment*
- → `BO-661` Temporary Access & Exception Management: *Temporary Access & Exception Management*
- → `BO-662` Access Revocation & Suspension: *Access Revocation & Suspension*
- → `BO-663` Access Rights Preview, Impact & Synchronization: *Access Rights Preview, Impact & Synchronization*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation access list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Reporting replica behind**: Show "Figures as of 10:42" on the tile row; tiles never spin individually. *(source: contracts/satellite/accreditation.yaml#listAccessProfiles)*
- **Board opened by a user with view rights only**: Quick actions that write are disabled with the missing permission named (per VO-R08); tiles and alerts still show. *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-615`: Same command-centre pattern as the Accreditation Command Center; the tile style, delta format and filter bar must be identical.
- Match `BO-297`: Live monitoring of accredited people on site is a filtered view of the entitlement usage monitor (DI-672), not a tile set here.
- Match `BO-664`: Suspended and Revoked counts here must equal the Lifecycle Command Center's for the same filters (same holder status source).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  activeProfiles: 14
  holdersWithAccess: 1186
  credentialsWithAccess: 1142
  restricted: 96
  temporaryGrants: 7
  expiringPermissions: 23
  suspended: 4
  revoked: 2
  exceptions: 11
  unassignedApproved: 38
alerts:
- 38 approved holders have no access profile (Al Noor Contracting 21, Gulf Media Network 17)
- Temporary grant Control Room for Omar Haddad ends 16:00 today
- Profile Media - Field Access changed by Maria Santos, not yet published
```

#### Permissions

- `listAccessProfiles` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-654` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-654`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 1: Opens Accreditation Access Command Center → Central operational dashboard for accreditation access permissions.
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F221 branch at step 1 (expected): when Nothing has been set up on Accreditation Access Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F221 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-654?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-655`, `BO-656`, `BO-657`, `BO-658`, `BO-659`, `BO-660`, `BO-661`, `BO-662`, `BO-663`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-655` Access Profile Management

**Create reusable accreditation access profiles.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-655 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each profile shall define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-profile-management-bo-655` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The access profile editor: the reusable bundle (Staff - Full Venue, Media - Press Areas, Contractor - Operational Areas) that says which zones and operational areas a holder may enter and when. A profile changed once changes access for everyone on it, live. Per VO-R14, BO-656 (zones), BO-657 (operational areas), BO-658 (dates and times), BO-659 (schedule) and BO-668 (venues) all write this same record and are drawn as tabs of this one editor with one Save. The one thing to get right: every Save shows its impact first (holders gaining, losing, left with none) and then sends the whole profile.

**Known correction pending (do not draw the wrong version)**

- **The pack's profile fields Accreditation categories allowed, Applicable events and Default credential behaviour have no field in AccessProfile** Why: The editor cannot store them; categories point at profiles (defaultAccessProfileId) rather than profiles listing categories, and events live on the programme. *(source: screens/P08-venue-back-office.yaml#BO-655 / screens/P08-venue-back-office.yaml#BO-656 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Profile statuses Draft / Active / Suspended / Archived are missing from AccessProfile** Why: Every save is live, so a profile cannot be prepared before an event or retired without deleting it. *(source: screens/P08-venue-back-office.yaml#BO-656 / contracts/satellite/accreditation.yaml#setAccessProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Fields drawn as select fields Date validity, Time validity, Access schedule** Why: These are the schedule rows (dateFrom, dateTo, daysOfWeek, from, to, eventPhase), an editable table per zone, not single selects. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **escortRequired is in the contract but not on the screen** Why: It is a profile-level rule the badge and scanner must show. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should a profile be restricted to the accreditation categories that may use it (pack "categories allowed")?** → Drawn default accepted: Draw a greyed "Allowed categories" multi-select with "Not yet supported" until the contract carries it. *(decided by Chinmay, 2026-10-02; DEC-477 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue | select field | — | — | — | — | — | — |
| Permitted zones | select field | — | — | — | — | — | — |
| Permitted operational areas | select field | — | — | — | — | — | — |
| Date validity | select field | — | — | — | — | — | — |
| Time validity | select field | — | — | — | — | — | — |
| Access schedule | select field | — | — | — | — | — | — |
| Accreditation categories allowed | select field | — | — | — | — | — | — |
| Applicable events | select field | — | — | — | — | — | — |
| Default credential behavior | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name / code**: Name as the pack's "Audience - Scope" pattern ("Media - Field Access"), Arabic variant per VO-R10; code short and upper-case (MEDIA-FIELD), unique per venue, read-only once holders are on the profile. *(source: screens/P08-venue-back-office.yaml#BO-655 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*
- **venueIds**: Defaults to the top-bar venue. Adding further venues makes it a multi-venue profile (BO-668 tab); a user can add only venues in their own scope. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile / MATRIX 12.1.40)*
- **zoneIds**: A topology tree (venue > park > zone) with tick boxes, using the same zones as Access Control. Empty means no zone, never "all"; say "No zones - holders on this profile cannot enter anywhere" in red. *(source: screens/P08-venue-back-office.yaml#BO-663 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*
- **escortRequired**: A switch "Holders must be escorted"; shown as an "Escort" chip on every badge preview and on the scanner result for this profile. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*
- **id, holderCount, scopePath**: Never inputs (per VO-R03); holderCount is shown read-only in the header ("Used by 212 holders"). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Profile list**: Columns Name, Code, Venues, Zones (count, with "+ 3 areas"), Schedule summary ("Event days 16:00-23:00"), Escort, Holders. Sorted by name; status column once profile statuses exist (see corrections). *(source: contracts/satellite/accreditation.yaml#listAccessProfiles)*
- **Plain-language summary**: At the top of the editor, the profile as a sentence, matching the BO-663 preview format: "Media - Field Access: Summit Peaks, Media Centre and Press Room any time; Field of Play 16:00-23:00 on event days; escort not required." *(source: screens/P08-venue-back-office.yaml#BO-663)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New profile**: Opens the editor empty with the top-bar venue selected and no zones; no id field. *(source: contracts/satellite/accreditation.yaml#setAccessProfile)*
- **Save profile**: First calls the impact preview and shows "212 holders affected: 0 gain, 14 lose Field of Play, 0 left with no access"; on confirm sends the whole profile (per VO-R04). The confirm names the count; a change that leaves anyone with no access needs a second explicit tick. *(source: contracts/satellite/accreditation.yaml#previewAccessImpact / contracts/satellite/accreditation.yaml#setAccessProfile)*
- **Duplicate profile**: Opens a copy with "(copy)" in the name and a blank code; nothing is saved until Save. *(source: designer default)*

**Data it reads**: `listAccessProfiles` (onLoad, Profiles)

**Where the user goes next**

- → `BO-654` Accreditation Access Command Center: *Back to Accreditation Access Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Two managers edit the same profile**: The write is server-wins; on save, if the profile changed since it was opened, show "Changed by Maria Santos at 10:31 - reload to see their change" rather than overwriting silently. *(source: contracts/satellite/accreditation.yaml#setAccessProfile)*
- **Profile edited during a live event**: The impact step flags holders currently on site ("31 of the 14 losing access are inside now") using the entitlement monitor, and the confirm says changes reach gates immediately. *(source: contracts/satellite/accreditation.yaml#previewAccessImpact / DI-672)*

#### Consistency with other screens

- Match `BO-656`: The matrix is a cross-profile view of zoneIds; a cell edited there and a tick here are the same field.
- Match `BO-032`: Guest admission profiles (Access) and accreditation access profiles are different records; never mix them in one picker, and label this one "Accreditation access profile" in shared places.
- Match `BO-708`: Each programme category's default access profile is picked from this list.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- name: Staff - Full Venue
  code: STAFF-FULL
  venues: Summit Peaks
  zones: 12
  schedule: Daily 06:00-23:59
  escort: 'No'
  holders: 340
- name: Media - Field Access
  code: MEDIA-FIELD
  venues: Summit Peaks
  zones: 3
  schedule: Event days 16:00-23:00 (Field of Play)
  escort: 'No'
  holders: 212
- name: Contractor - Operational Areas
  code: CONTR-OPS
  venues: Summit Peaks, Aqua Park
  zones: 2
  schedule: Mon-Fri 08:00-18:00
  escort: 'Yes'
  holders: 97
- name: VIP - Hospitality
  code: VIP-HOSP
  venues: Summit Peaks
  zones: 2
  schedule: Event opening to close
  escort: 'No'
  holders: 64
```

#### Permissions

- `listAccessProfiles` → `ACCREDITATION_VIEW` (read) · staff
- `setAccessProfile` → `ACCREDITATION_CONFIGURE` (configure) · staff

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

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-655` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-655`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 2: Works in Access Profile Management → Create reusable accreditation access profiles.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-655?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-654`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-656` Venue & Zone Access Matrix

**Visually configure which accreditation profiles can access each venue zone.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-656 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/venue-zone-access-matrix-bo-656` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The access matrix: accreditation profiles down the side, venue zones across the top, each cell saying whether that profile may enter that zone. It is the fastest way for a security lead to spot that "Vendor - Service Areas" can reach the Control Room. The one thing to get right: cell values are derived from the profile (zone ticked, with or without a time window or escort), and editing a cell edits that profile, so every edit shows impact before it is published.

**Known correction pending (do not draw the wrong version)**

- **The pack's four cell states (Allowed / Restricted / Conditional / Not Allowed) cannot be stored; AccessProfile.zoneIds is a plain inclusion list** Why: Only Allowed and Not allowed are real; Conditional must be derived from schedule rows and escortRequired, and Restricted has no meaning in the contract. Either define them as derived (as drawn) or add a per-zone access level. *(source: screens/P08-venue-back-office.yaml#BO-656 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Filter by event is not possible** Why: AccessProfile has no eventIds; event scope is on the programme, so an event filter needs programme categories' default profiles. *(source: screens/P08-venue-back-office.yaml#BO-656 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **primaryButton "Save access profile"** Why: The matrix publishes several profiles; the button is "Review impact and publish". *(source: screens/P08-venue-back-office.yaml#BO-656; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Write bound with no read (listAccessProfiles not bound) (CHG-WIR-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **cell value**: Four states as the pack asks: Allowed (zone in the profile, no time limit), Conditional (zone in the profile with schedule rows or escort required; hover shows "16:00-23:00 event days"), Restricted (zone in the profile but limited to named holders through exceptions), Not allowed (zone not in the profile). Clicking cycles Allowed / Not allowed only; Conditional opens the profile's schedule tab. Use icons plus colour, never colour alone. *(source: screens/P08-venue-back-office.yaml#BO-656 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*
- **filters**: Event and Venue (pack); Venue defaults to the top-bar venue. Zone columns are grouped by park and can be collapsed. *(source: screens/P08-venue-back-office.yaml#BO-656)*

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

- **Matrix**: Sticky first column (profile name and holder count) and sticky header (zone names, rotated if needed); high-security zones (Control Room, Restricted Security Area) marked with a lock icon so an Allowed there stands out. RTL per VO-R10 flips column order. *(source: screens/P08-venue-back-office.yaml#BO-656)*
- **Pending changes tray**: Edited cells are outlined; a tray lists "3 profiles changed, 5 cells" until published. *(source: screens/P08-venue-back-office.yaml#BO-656)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Review impact and publish**: Runs the impact preview once per changed profile and shows the combined result (holders gaining, losing, left with none), then saves each changed profile in full (per VO-R04). *(source: contracts/satellite/accreditation.yaml#previewAccessImpact / contracts/satellite/accreditation.yaml#setAccessProfile)*
- **Discard changes**: Clears the tray, no confirmation needed when nothing was published. *(source: designer default)*

**Data it reads**: `listAccessProfiles` (onLoad, The access profiles and their zones)

**Where the user goes next**

- → `BO-654` Accreditation Access Command Center: *Back to Accreditation Access Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue zone access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue zone access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue zone access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue zone access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **One of several profile saves fails**: Saves are per profile, not atomic. Show which profiles were published and which failed ("2 of 3 published; Vendor - Service Areas failed - retry"), and keep the failed cells outlined. *(source: contracts/satellite/accreditation.yaml#setAccessProfile)*
- **A zone removed from the venue topology**: Its column shows struck through with "Zone retired"; cells read-only. *(source: ADR-0030)*

#### Consistency with other screens

- Match `BO-655`: Same record; a cell here and the zone tick in the editor are one field, and the summary sentence uses the same states.
- Match `BO-663`: The preview's "Allowed / 16:00-23:00 only / Not Allowed" lines use the same words as the cell states.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
zones:
- Public Area
- Media Centre
- Press Conference Room
- VIP Lounge
- Hospitality
- Backstage
- Field of Play
- Control Room
- Loading Area
rows:
- profile: Media - Field Access
  Media Centre: Allowed
  Press Conference Room: Allowed
  Field of Play: Conditional (16:00-23:00)
  VIP Lounge: Not allowed
  Control Room: Not allowed
- profile: Production - Backstage
  Backstage: Allowed
  Loading Area: Allowed
  Control Room: Conditional (escort)
  Field of Play: Not allowed
- profile: Security - Controlled Zones
  Control Room: Allowed
  Field of Play: Allowed
  Backstage: Allowed
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

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-656` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-656`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 4: Works in Venue & Zone Access Matrix → Visually configure which accreditation profiles can access each venue zone.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-656?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save access profile, Cancel.
- [ ] Every transition is wired: `BO-654`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-657` Operational Area Permission Management

**Configure access to operational areas below the broader zone level.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-657 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/operational-area-permission-management-bo-657` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Operational areas below zone level (Broadcast compound, Press room, Loading dock, Security command centre) and which profiles include them. It is a tab of the access profile editor (per VO-R14) plus a small register of the areas themselves. The one thing to get right: an area belongs to a parent zone, so granting an area must not silently grant the whole zone, and the designer must show that an area string typed differently is a different area.

**Known correction pending (do not draw the wrong version)**

- **AccessProfile.operationalAreas is an array of free strings with no area register, parent venue, parent zone, role or schedule** Why: The pack associates each area with a parent venue, parent zone, profile, category, role and schedule, with inclusion and exclusion rules; none can be stored or validated. *(source: screens/P08-venue-back-office.yaml#BO-657 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Write bound with no read (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are operational areas enforced by readers (they need access points in the topology) or only checked by staff at the door?** → Drawn default accepted: Draw an "Enforced by" column with Reader / Staff check, greyed until answered. *(decided by Chinmay, 2026-10-02; DEC-478 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **operationalAreas (on a profile)**: A multi-select of areas from the venue's area register, grouped by parent zone ("Field of Play > Broadcast compound"), never free text, because the contract stores plain strings and a typo is a new area no reader knows. *(source: screens/P08-venue-back-office.yaml#BO-657 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*
- **area register entry**: Name (Arabic variant), parent venue, parent zone, optional operational role and schedule; the pack's inclusion and exclusion rules shown as "Include" and "Exclude" lists per profile (Exclude wins). *(source: screens/P08-venue-back-office.yaml#BO-657)*

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

- **Areas by profile**: Area list with parent zone, profiles that include it, holder count, and a red "Excluded" chip where a profile excludes it. *(source: screens/P08-venue-back-office.yaml#BO-657)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save profile**: Same impact-then-save as BO-655 (per VO-R04); the impact lists area changes as well as zone changes. *(source: contracts/satellite/accreditation.yaml#setAccessProfile / contracts/satellite/accreditation.yaml#previewAccessImpact)*

**Data it reads**: `listAccessProfiles` (onLoad, The access profiles and their operational areas)

**Where the user goes next**

- → `BO-654` Accreditation Access Command Center: *Back to Accreditation Access Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational area permission list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational area permission untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational area permission yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational area permission are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Area granted but its parent zone not in the profile**: Warn "Broadcast compound is inside Field of Play, which this profile does not include; holders will be stopped at the zone gate" and offer to add the zone. *(source: screens/P08-venue-back-office.yaml#BO-657)*
- **Area has no reader**: Show "No access point - area access is checked by staff" so nobody assumes a gate enforces it. *(source: screens/P08-venue-back-office.yaml#BO-663)*

#### Consistency with other screens

- Match `BO-655`: This is the "Operational areas" tab of the same editor and Save.
- Match `BO-148`: Zones and access points come from the venue topology in Access; areas must sit under those zones.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
areas:
- area: Broadcast compound
  zone: Field of Play
  profiles: Media - Field Access, Production - Backstage
  holders: 248
- area: Loading dock
  zone: Loading Area
  profiles: Vendor - Service Areas, Contractor - Operational Areas
  holders: 131
- area: Security command centre
  zone: Control Room
  profiles: Security - Controlled Zones
  holders: 18
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

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rights can be set at site, operating area (department, e.g. B2B, B2C, OTA, on-site POS, finance), workstation, role or user level; site-level settings (password policy, UI rights, configuration rights) cascade to everything beneath. *(agreed · MoM 7 Aug 2026, 2. System Organization: Tenant & Site Setup · DI-148)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-657` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-657`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 6: Works in Operational Area Permission Management → Configure access to operational areas below the broader zone level.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-657?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save access profile, Cancel.
- [ ] Every transition is wired: `BO-654`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-658` Date & Time Access Rules

**Control when accreditation access is valid.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-658 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/date-time-access-rules-bo-658` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** When access is valid: dates, days, hours and event phases per zone within a profile ("Media - Field Access, Field of Play, 15 Sep 2026, 16:00-23:00"). Outside the window the credential does not open that zone. It is the "Dates and times" tab of the access profile editor (per VO-R14). The one thing to get right: zone, date and time are three dimensions, so each rule row names its zone, and the result is shown on a calendar with day, week and month views (VO-R01).

**Known correction pending (do not draw the wrong version)**

- **Grace period, overnight access and blackout periods (pack) have no field in the schedule rows** Why: The schedule item carries only zone, days, dates, from/to times and event phase. *(source: screens/P08-venue-back-office.yaml#BO-659 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A screen that places access in time has no calendar** Why: VO-R01 needs Day, Week and Month views for every calendar in the process. *(source: screens/P08-venue-back-office.yaml#BO-658; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Write bound with no read (CHG-WIR-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **schedule rows**: An editable table, one row per rule: Zone (or "All zones in this profile"), Valid from date, Valid until date (not before from), Days (weekday chips, empty = every day), Start time, End time (HH:MM venue time), Event phase (Build, Rehearsal, Doors open, Live show, Breakdown). The pack's "Setup-day access" and "Breakdown-day access" are the Build and Breakdown phases. *(source: screens/P08-venue-back-office.yaml#BO-657 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*
- **overnight access**: An end time earlier than the start time means "until the next morning" and is shown as "22:00-02:00 (+1 day)"; never reject it as invalid. *(source: screens/P08-venue-back-office.yaml#BO-659)*
- **grace period / blackout periods**: Drawn greyed with "Not yet supported" (see corrections) so the client sees the gap. *(source: screens/P08-venue-back-office.yaml#BO-659)*

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

- **Access calendar**: Day, Week and Month views (VO-R01), plus Agenda. Each zone a coloured lane; event phases shaded. The Day view starts at the venue's day start hour and shows the hours a zone is open to this profile. *(source: screens/_components.yaml#calendarView)*
- **Rule sentence**: Each row reads back as a sentence, "Field of Play, 15 Sep 2026, 16:00-23:00 only", the same words as the BO-663 preview. *(source: screens/P08-venue-back-office.yaml#BO-659 / screens/P08-venue-back-office.yaml#BO-663)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save profile**: Impact preview, then whole-profile save (per VO-R04, VO-R05). *(source: contracts/satellite/accreditation.yaml#setAccessProfile / contracts/satellite/accreditation.yaml#previewAccessImpact)*

**Data it reads**: `listAccessProfiles` (onLoad, The access profiles and their date and time rules)

**Where the user goes next**

- → `BO-654` Accreditation Access Command Center: *Back to Accreditation Access Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The date time access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the date time access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No date time access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the date time access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Two rows for the same zone overlap or contradict**: Highlight both rows "Overlaps with row 2"; the union applies, say so. *(source: screens/P08-venue-back-office.yaml#BO-663)*
- **A zone in the profile has no schedule row**: Show "Any time while the accreditation is valid" against it, so absence is a visible choice. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*
- **Rule dates outside the programme or accreditation validity**: Warn "Valid until 25 Dec is after the accreditation ends on 20 Dec; access stops on 20 Dec". *(source: screens/P08-venue-back-office.yaml#BO-666)*

#### Consistency with other screens

- Match `BO-659`: Reusable schedules and these rows are the same schedule array; draw them as one tab.
- Match `BO-152`: Same calendar component as the access Operating Calendar (day/week/month, venue day start hour).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- zone: Field of Play
  from: 15 Sep 2026
  to: 15 Sep 2026
  days: ''
  start: '16:00'
  end: '23:00'
  phase: Live show
- zone: Media Centre
  from: 12 Sep 2026
  to: 16 Sep 2026
  days: ''
  start: 08:00
  end: 02:00
  phase: ''
- zone: Loading Area
  from: 10 Sep 2026
  to: 11 Sep 2026
  days: ''
  start: 06:00
  end: '18:00'
  phase: Build
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

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-658` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-658`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 8: Works in Date & Time Access Rules → Control when accreditation access is valid.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-658?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save access profile, Cancel.
- [ ] Every transition is wired: `BO-654`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-659` Access Schedule Management

**Create reusable schedules for accreditation permissions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-659 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-schedule-management-bo-659` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Reusable time patterns (Event Day Staff 06:00-23:59; Media 3 hours before to 2 hours after the event; Contractor 08:00-18:00 Monday-Friday) that can be attached to many profiles or to one holder. The one thing to get right: the client asks for named, reusable, event-relative schedules, and the contract only has schedule rows embedded in each profile; the design must show both the pattern and where it is used, and must not pretend a change here updates other profiles.

**Known correction pending (do not draw the wrong version)**

- **There is no schedule entity; schedules exist only as rows inside each AccessProfile** Why: The pack asks for reusable named schedules attachable to profiles or individual records; a change cannot propagate, and individual records only take time-boxed exceptions. *(source: screens/P08-venue-back-office.yaml#BO-659 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Event-relative, recurring with exceptions, holiday exceptions and special-event overrides cannot be stored** Why: Schedule rows hold fixed dates, weekdays, times and one eventPhase only. *(source: screens/P08-venue-back-office.yaml#BO-659 / MATRIX 12.1.29; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Listed in the calendar inventory with no calendar component** Why: Schedules place access in time; per VO-R01 a Day/Week/Month calendar is required. *(source: DI-907 / DI-919; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **primaryButton "Save access profile" on a schedule screen** Why: The schedule's action is "Save schedule" and then "Apply to profiles". *(source: screens/P08-venue-back-office.yaml#BO-659; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Must schedules be reusable named records (and event-relative), or is per-profile schedule rows enough for the first release?** → Drawn default accepted: Draw the library and the event-relative fields; mark the event-relative and exception fields "Not yet supported". *(decided by Chinmay, 2026-10-02; DEC-479 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **schedule type**: A choice of Fixed (dates and times), Recurring (weekdays and times), Event-relative (offset before event start and after event end, in hours and minutes), with Date exceptions and Holiday exceptions as a list of dates that override the pattern, and a Special-event override. *(source: screens/P08-venue-back-office.yaml#BO-659)*
- **event-relative offsets**: "Starts [3] h before the event, ends [2] h after the event" with a live example under it ("For the 15 Sep 19:00 match: 16:00-21:00 + 2 h = 16:00 to 23:00"). Only Event phase can be stored today (see corrections). *(source: screens/P08-venue-back-office.yaml#BO-659 / contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save access profile (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Schedule library**: Name, pattern sentence, used by (profiles count, holders count). A schedule used by nothing can be deleted. *(source: screens/P08-venue-back-office.yaml#BO-659)*
- **Calendar preview**: Day, Week and Month views (VO-R01) of the selected schedule over the event dates, with exceptions marked. *(source: DI-907 / DI-919)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Apply to profiles**: Copies the pattern into the chosen profiles' schedule rows, then the usual impact preview and one save per profile. *(source: contracts/satellite/accreditation.yaml#setAccessProfile / contracts/satellite/accreditation.yaml#previewAccessImpact)*

**Where the user goes next**

- → `BO-654` Accreditation Access Command Center: *Back to Accreditation Access Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access schedule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access schedule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access schedule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access schedule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Event time changes after an event-relative schedule was applied**: Until the contract can hold offsets, stored times do not move; show "Event time changed - 4 profiles use times derived from the old start" as an alert on BO-654. *(source: screens/P08-venue-back-office.yaml#BO-659)*
- **Holiday exception falls on an event day**: The special-event override wins; the calendar marks the day with both. *(source: screens/P08-venue-back-office.yaml#BO-659)*

#### Consistency with other screens

- Match `BO-658`: The resulting rows are the same schedule rows; one tab in the profile editor.
- Match `BO-055`: Staff rota shift times and the Event Day Staff schedule should agree for staff accreditations; same time format.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
schedules:
- name: Event Day Staff
  pattern: Event days 06:00-23:59
  usedBy: 3 profiles, 340 holders
- name: Media
  pattern: 3 h before event to 2 h after event
  usedBy: 2 profiles, 212 holders
- name: Contractor
  pattern: Mon-Fri 08:00-18:00
  usedBy: 1 profile, 97 holders
- name: Production Crew
  pattern: 24 h, 10 Sep 2026 - 18 Sep 2026
  usedBy: 1 profile, 45 holders
```

#### Permissions

- `setAccessProfile` → `ACCREDITATION_CONFIGURE` (configure) · staff

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

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-659` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-659`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 10: Works in Access Schedule Management → Create reusable schedules for accreditation permissions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-659?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save access profile, Cancel.
- [ ] Every transition is wired: `BO-654`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-660` Holder Access Assignment

**Assign access permissions to an individual accreditation holder.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-660 |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The screen shall display) and no metric row |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/holder-access-assignment-bo-660` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of HolderAccess (per holder or across holders); affects BO-660, BO-661, BO-668.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** One holder's access: their photo and accreditation, the profiles they inherit from their category, and any individual overrides on top. An accreditation officer uses it for "the Gulf Media Network cameraman also needs the tunnel". The one thing to get right: inherited access and individual overrides are visibly different, the resulting effective zones are shown, and the save replaces the holder's whole access record.

**Known correction pending (do not draw the wrong version)**

- **Exceptions carry a zone only** Why: The pack's Add operational area, Apply schedule and Apply date/time restriction cannot be expressed per holder. *(source: screens/P08-venue-back-office.yaml#BO-660 / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): No read is bound; the table "Every holder access" and panel "The selected holder access" have nothing to show (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which overrides count as high-risk and need an approver (by zone flag, by category, by duration)?** → Drawn default accepted: Draw zones with a lock icon as high-risk and require Approved by for them only. *(decided by Chinmay, 2026-10-02; DEC-480 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

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

- **accessProfileIds**: The category's default profile is shown first, labelled "Inherited from Media category", removable only with a reason; further profiles can be added from the profile list. *(source: screens/P08-venue-back-office.yaml#BO-660 / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess / MATRIX 12.1.5)*
- **exceptions (individual overrides)**: Each override: Zone, Grant or Remove, From and To (date-time, both required), Reason (required), Approved by (required where the zone is high-risk). "Add permitted zone" = Grant; "Remove zone" = Remove; "Add temporary permission" opens BO-661. The pack's "Add operational area" cannot be stored (see corrections). *(source: screens/P08-venue-back-office.yaml#BO-660 / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess)*
- **holderId, effectiveZones, scopePath**: Never inputs (per VO-R03); holderId comes from the navigation, effectiveZones is computed by the server. *(source: contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess)*

#### Outputs: what the screen shows and produces

**Shown**

**Every holder access** (data table)

| Shows | Format | Notes |
|---|---|---|
| Holder | text | not in the schema: `Holder` |
| Photograph | text | not in the schema: `Photograph` |
| Accreditation | text | not in the schema: `Accreditation` |
| Category | text | not in the schema: `Category` |
| Credential | text | not in the schema: `Credential` |
| Event | text | not in the schema: `Event` |
| Venue | text | not in the schema: `Venue` |
| Current access profile | text | not in the schema: `Current access profile` |

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

**The selected holder access** (detail panel): The pack groups this record's detail under its own headings: “Administrators shall be able to”, “Inherited Access”, “Individual Override”.

| Shows | Format | Notes |
|---|---|---|
| Holder | text | not in the schema: `Holder` |
| Photograph | text | not in the schema: `Photograph` |
| Accreditation | text | not in the schema: `Accreditation` |
| Category | text | not in the schema: `Category` |
| Credential | text | not in the schema: `Credential` |
| Event | text | not in the schema: `Event` |
| Venue | text | not in the schema: `Venue` |
| Current access profile | text | not in the schema: `Current access profile` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Holder header**: Photo, name, accreditation number, category, credential(s) with status, event, venue, current access profile, as the pack lists. *(source: screens/P08-venue-back-office.yaml#BO-660)*
- **Effective access**: A zone list with a source tag per zone: "Inherited" (grey, from profile name), "Override - granted until 18 Dec 16:00" (blue) or "Override - removed" (struck through, red). The pack's "clearly distinguish" is met by the tag and a legend, not by colour alone. *(source: screens/P08-venue-back-office.yaml#BO-660 / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save holder access**: Sends profiles and all exceptions together (per VO-R04) and shows the new effective zones. A high-risk override without an approver is refused with the reason; the approver picker lists users with approval rights. *(source: screens/P08-venue-back-office.yaml#BO-660 / contracts/satellite/accreditation.yaml#setHolderAccess)*

**Data it reads**: `listAccreditationHolders` (onLoad, Holders to assign access to); `listAccessProfiles` (onLoad, Profiles that can be assigned)

**Where the user goes next**

- → `BO-654` Accreditation Access Command Center: *Back to Accreditation Access Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The holder access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the holder access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No holder access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the holder access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Holder suspended or revoked**: Editor read-only with "Access is disabled while the accreditation is suspended" and a link to BO-670. *(source: screens/P08-venue-back-office.yaml#BO-673)*
- **Override with no end date**: Not allowed; "To" is required. "An override without an end is a profile change - edit the profile instead". *(source: contracts/satellite/accreditation.yaml#setHolderAccess)*
- **Override zone outside the holder's accreditation venues**: Refuse with "Arena B is not in this accreditation's venues". *(source: screens/P08-venue-back-office.yaml#BO-667)*

#### Consistency with other screens

- Match `BO-661`: Temporary grants are exceptions on this same record; one editor, one Save (VO-R14).
- Match `BO-626`: The holder profile's Access tab opens this screen; same header.
- Match `BO-663`: Effective access uses the preview's wording (Allowed / time-limited / Not allowed).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holder:
  name: Khalid Al Zaabi
  accreditationNumber: ACC-2026-002291
  category: Media
  organisation: Gulf Media Network
  credential: Printed badge BDG-002291-1, Active
  event: Summit Peaks Winter Festival 2026
  venue: Summit Peaks
inherited:
  profile: Media - Press Areas
  zones:
  - Media Centre
  - Press Conference Room
overrides:
- zone: Field of Play
  type: Grant
  from: 15 Dec 2026 16:00
  to: 15 Dec 2026 23:00
  reason: Pitch-side interview
  approvedBy: Fatima Al Hashimi
```

#### Permissions

- `setHolderAccess` → `ACCREDITATION_MANAGE` (configure) · staff
- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `listAccessProfiles` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.1 | Allows management of credentials and access rights for staff, contractors, VIPs, media personnel and special guests. | Accreditation & Credential Management | CONTRACTED | `setHolderAccess` |
| 12.1.5 | Access Assignment System shall assign venue access rights based on accreditation type. | Accreditation & Credential Management | CONTRACTED | `setHolderAccess` |
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.16 | Profile Management - System shall maintain detailed accreditation holder profiles. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |
| 12.1.17 | Photo Management - System shall support accreditation holder photographs. | Accreditation & Credential Management | CONTRACTED | data `AccreditationHolder` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-660` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-660`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 12: Works in Holder Access Assignment → Assign access permissions to an individual accreditation holder.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (50 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-660?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-654`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-661` Temporary Access & Exception Management

**Provide controlled short-term access outside normal accreditation permissions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-661 |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/temporary-access-exception-management-bo-661` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Short-term access outside the holder's normal profile, for example a contractor in the Control Room from 14:00 to 16:00 for maintenance. Each grant is time-boxed, reasoned, attributed and expires on its own. Per VO-R14 it is the "Temporary access" section of the holder access record (BO-660), plus a venue-wide list of grants active now and ending soon. The one thing to get right: a grant can never be open-ended, and the list makes it obvious who is inside a zone on a temporary basis right now.

**Known correction pending (do not draw the wrong version)**

- **Temporary grants can only name a zone; there is no requestedBy on the exception** Why: The pack asks for specific zone, operational area, date, time window or event, and records Requested by; the exception schema has zoneId, grant, from, to, reason, approvedBy only. *(source: screens/P08-venue-back-office.yaml#BO-660 / screens/P08-venue-back-office.yaml#BO-662 / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Write bound with no read; the venue-wide list of active grants has no operation** Why: There is no read of HolderAccess (per holder or across holders); the active-grants list and the BO-654 tile cannot be filled. *(source: contracts/satellite/accreditation.yaml#setHolderAccess; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **from and to are optional in the exception schema** Why: The contract's own rule says an exception with no end is a profile change nobody reviewed, and the pack says temporary access expires automatically; to should be required. *(source: screens/P08-venue-back-office.yaml#BO-662 / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **holder**: Picker by name or accreditation number; shows category and current profile so the officer sees what is already allowed. *(source: screens/P08-venue-back-office.yaml#BO-662)*
- **requested access**: Zone (topology picker); Specific event as a shortcut that fills From and To with the event's times. Operational area and per-event scoping are greyed (see corrections). *(source: screens/P08-venue-back-office.yaml#BO-660 / screens/P08-venue-back-office.yaml#BO-662)*
- **from / to**: Both required, date and time in venue time; default From now, To end of today; To must be after From. Show the duration ("2 h"). *(source: screens/P08-venue-back-office.yaml#BO-662 / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess)*
- **reason / requested by / approved by**: Reason required (text). Requested by defaults to the signed-in user and is shown, not typed. Approved by is required for high-risk zones and picks a user with approval rights; it is not the requester. *(source: screens/P08-venue-back-office.yaml#BO-662 / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save holder access (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Active and upcoming grants**: Columns Holder, Zone, From, To, Time left (live countdown for active ones), Reason, Requested by, Approved by. Ending in under an hour in amber. Cursor paging (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-662)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Grant temporary access**: Adds the exception to the holder's record and saves the whole record (per VO-R04); gates honour it from From. *(source: contracts/satellite/accreditation.yaml#setHolderAccess)*
- **End now**: Confirmation "Omar Haddad loses Control Room access immediately" with a reason; sets To to now. *(source: contracts/satellite/accreditation.yaml#setHolderAccess)*

**Where the user goes next**

- → `BO-654` Accreditation Access Command Center: *Back to Accreditation Access Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The temporary access exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the temporary access exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No temporary access exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the temporary access exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Grant reaches its end time**: It expires automatically without any action and moves to history; the pack requires no manual step. *(source: screens/P08-venue-back-office.yaml#BO-662)*
- **Holder's accreditation ends before the grant's To**: Warn and cap at the accreditation's validTo. *(source: screens/P08-venue-back-office.yaml#BO-666)*

#### Consistency with other screens

- Match `BO-660`: Same HolderAccess exceptions; one Save.
- Match `BO-654`: The "Temporary access grants" tile counts the active rows here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
grants:
- holder: Omar Haddad
  organisation: Al Noor Contracting
  zone: Control Room
  from: 15 Dec 2026 14:00
  to: 15 Dec 2026 16:00
  reason: HVAC maintenance
  requestedBy: Rahul Menon
  approvedBy: Ahmed Al Mansoori
- holder: Priya Nair
  organisation: Yas Hospitality Partners
  zone: VIP Lounge
  from: 15 Dec 2026 18:00
  to: 15 Dec 2026 23:30
  reason: Sponsor reception service
  requestedBy: Maria Santos
  approvedBy: ''
```

#### Permissions

- `setHolderAccess` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.1 | Allows management of credentials and access rights for staff, contractors, VIPs, media personnel and special guests. | Accreditation & Credential Management | CONTRACTED | `setHolderAccess` |
| 12.1.5 | Access Assignment System shall assign venue access rights based on accreditation type. | Accreditation & Credential Management | CONTRACTED | `setHolderAccess` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-661` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-661`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 14: Works in Temporary Access & Exception Management → Provide controlled short-term access outside normal accreditation permissions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-661?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save holder access, Cancel.
- [ ] Every transition is wired: `BO-654`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-662` Access Revocation & Suspension

**Immediately remove or temporarily disable accreditation access.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-662 |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `holderId` (navigation) |
| Route | `/access-venue/access-revocation-suspension-bo-662` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Taking access away from one holder, at once: suspend (they come back) or revoke (they do not), for all their access or only part of it (a venue, a zone, an area, one credential). Used by security in the middle of an event. The one thing to get right: the screen states the consequence before confirm, and after confirm says the gates have it now and offline devices will have it at their next refresh.

**Known correction pending (do not draw the wrong version)**

- **Partial revocation (Venue, Zone, Area, Specific entitlement, Credential) has no operation** Why: setAccreditationStatus acts on the whole holder; zone removal needs time-boxed HolderAccess exceptions, and there is no call to revoke one credential without replacing it. *(source: screens/P08-venue-back-office.yaml#BO-662 / contracts/satellite/accreditation.yaml#setAccreditationStatus / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **primaryButton "Save accreditation status"** Why: The actions are "Suspend access" and "Revoke access"; a destructive act is never a "Save". *(source: screens/P08-venue-back-office.yaml#BO-662; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Screen duplicates BO-670 and BO-671 (same operation, same holder)** Why: Per VO-R14 one suspend/revoke dialog serves Boards 5 and 6; keep the board entries as anchors. *(source: DI-671; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Must partial revocation (one zone, one venue, one credential) be permanent, or is a time-boxed removal enough?** → Drawn default accepted: Draw the scope selector with only All access enabled and the partial scopes greyed "Not yet supported". *(decided by Chinmay, 2026-10-02; DEC-481 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **action**: Two large choices, Suspend access (amber, "can be reactivated") and Revoke access (red, "permanent"), never a dropdown. *(source: screens/P08-venue-back-office.yaml#BO-662)*
- **scope**: All access (default), Venue, Zone, Area, Specific entitlement, Credential. All access uses the holder status change; a partial scope removes only that part (see corrections for what is storable). *(source: screens/P08-venue-back-office.yaml#BO-662)*
- **reason / effective time / notes**: Reason required, from the closed lists of BO-670 (suspend) and BO-671 (revoke); Effective time defaults to Now (a future time allowed for suspension only); Operator is the signed-in user, shown not typed; Notes optional. *(source: screens/P08-venue-back-office.yaml#BO-662 / contracts/satellite/accreditation.yaml#setAccreditationStatus)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save accreditation status (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Impact panel**: Before confirm: "Accreditation suspended, 2 credentials suspended, access to 5 zones disabled" with the credential list. *(source: screens/P08-venue-back-office.yaml#BO-672 / screens/P08-venue-back-office.yaml#BO-673)*
- **Propagation status**: After confirm: "Online gates updated 10:42"; "Offline devices pick this up at their next package refresh" with the oldest device package age, per VO-R07. *(source: screens/P08-venue-back-office.yaml#BO-662)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Confirm suspend / revoke**: Confirmation per VO-R16 naming holder and counts; revoke needs the reason re-read and a typed confirmation. Revocation invalidates every credential immediately and pushes to the gates. *(source: contracts/satellite/accreditation.yaml#setAccreditationStatus)*

**Where the user goes next**

- → `BO-654` Accreditation Access Command Center: *Back to Accreditation Access Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access revocation suspension list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access revocation suspension untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access revocation suspension yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access revocation suspension are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Holder is inside a restricted zone at the moment of revocation**: Show "Last admitted to Backstage 10:31" from access activity so security can act on site. *(source: contracts/satellite/accreditation.yaml#listAccreditationAccessActivity)*
- **Revoking an already revoked holder**: Revoke disabled with "Already revoked on 12 Dec by Ahmed Al Mansoori". *(source: screens/P08-venue-back-office.yaml#BO-665)*

#### Consistency with other screens

- Match `BO-670`: Suspension here and on BO-670 is the same call and the same reason list; draw one dialog used from both boards.
- Match `BO-671`: Revocation here and on BO-671 is the same call; same dialog and wording (VO-R14).
- Match `SCN-003`: The scanner shows a revoked accreditation with the same deny label (Media deactivated / Accreditation revoked) per VO-R06.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holder:
  name: James Carter
  accreditationNumber: ACC-2026-001877
  category: Contractor
  organisation: Al Noor Contracting
impact:
  credentials: 2
  zones: 5
  lastSeen: Loading Area 10:31
reason: Security investigation
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-662` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-662`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 16: Works in Access Revocation & Suspension → Immediately remove or temporarily disable accreditation access.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-662?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save accreditation status, Cancel.
- [ ] Every transition is wired: `BO-654`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-663` Access Rights Preview, Impact & Synchronization

**Validate accreditation access before publishing it to Access Control.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-663 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-rights-preview-impact-synchronization-bo-663` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The check before access goes live: a plain-language preview of who can enter what, a validation list, and the impact of a pending profile change, then Publish. Per VO-R05 simulation lives inside the screen it tests, so this is the final step of the access profile editor (and of the matrix), and also a per-holder "what can this person do" lookup. The one thing to get right: the preview reads like the pack's example, line per zone, and shows holders who would be left with no access before anything is published.

**Known correction pending (do not draw the wrong version)**

- **Save Draft and Synchronize have no contract support** Why: setAccessProfile is live on save and nothing reports synchronisation status with Access Control; the pack asks for both. *(source: screens/P08-venue-back-office.yaml#BO-663 / contracts/satellite/accreditation.yaml#setAccessProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **previewAccessImpact returns counts and a no-access list, not the per-holder, per-zone preview the pack shows** Why: The "Ahmed - Media Centre Allowed" view needs a holder effective-access read with schedule resolution, which does not exist. *(source: screens/P08-venue-back-office.yaml#BO-663 / contracts/satellite/accreditation.yaml#/components/schemas/AccessImpact; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Primary button has an empty label** Why: Generated placeholder; the actions are Validate and Publish access. *(source: screens/P08-venue-back-office.yaml#BO-663; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **subject**: Either a pending profile change (arrives from BO-655/656 with the unsaved profile) or one holder picked by name (per-holder preview). *(source: screens/P08-venue-back-office.yaml#BO-663 / contracts/satellite/accreditation.yaml#previewAccessImpact)*
- **preview at**: An optional date and time ("as of 15 Dec 2026 18:00") so time-limited zones resolve to Allowed or Not allowed at that moment. *(source: screens/P08-venue-back-office.yaml#BO-663 / DI-629)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Holder preview**: The pack's format exactly: name, category, venue, then one line per zone "Media Centre - Allowed", "Field of Play - 16:00-23:00 only", "VIP Lounge - Not Allowed", with Allowed green, time-limited amber, Not Allowed grey. *(source: screens/P08-venue-back-office.yaml#BO-663)*
- **Validation checklist**: Ten checks with pass/warn/fail and a fix link: Credential active, Accreditation active, Venue assigned, Zones configured, Areas configured, Date validity, Time validity, Schedule conflicts, Expired permissions, Conflicting access rules. *(source: screens/P08-venue-back-office.yaml#BO-663)*
- **Change impact**: Holders affected, gaining, losing; zones added and removed; and a named list of holders left with no access, which blocks Publish until acknowledged. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccessImpact)*
- **Sync with Access Control**: A status line "Synchronised with Access Control 10:42" or "Pending" or "Failed - retry", per the pack. *(source: screens/P08-venue-back-office.yaml#BO-663)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validate / Preview**: Runs the impact preview and the checklist; nothing is saved. *(source: contracts/satellite/accreditation.yaml#previewAccessImpact)*
- **Publish access**: Saves the profile (whole record, per VO-R04) and shows the sync line; returns to the editor or BO-654. *(source: contracts/satellite/accreditation.yaml#setAccessProfile)*
- **Save draft**: Greyed "Not yet supported" (profiles have no draft state). *(source: screens/P08-venue-back-office.yaml#BO-663)*

**Where the user goes next**

- → `BO-654` Accreditation Access Command Center: *Back to Accreditation Access Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access rights preview list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access rights preview untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access rights preview yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access rights preview are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Change leaves holders with no access during a live event**: Red banner naming the count and first names, and Publish needs a reason. *(source: contracts/satellite/accreditation.yaml#previewAccessImpact)*
- **Validation fails on Credential active**: The holder preview still renders but every line is prefixed "Would be denied - credential not active". *(source: screens/P08-venue-back-office.yaml#BO-663)*

#### Consistency with other screens

- Match `BO-655`: Same summary sentence and state words; this is the editor's final step.
- Match `BO-163`: Same idea as the access rule simulator (virtual scan); keep the result layout consistent (outcome plus reason).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
preview:
  holder: Ahmed Al Mansoori
  category: Media Accreditation
  venue: Summit Peaks
  lines:
  - Media Centre - Allowed
  - Press Room - Allowed
  - Field of Play - 16:00-23:00 only
  - VIP Lounge - Not Allowed
  - Control Room - Not Allowed
impact:
  holdersAffected: 212
  gaining: 0
  losing: 14
  leftWithNoAccess: 0
  zonesRemoved:
  - Field of Play
```

#### Permissions

- `previewAccessImpact` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-663` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-663`
- Workshop pack: ACCREDITATION.pdf board 5
- Flow F221 *ACCREDITATION board 5: Accreditation Access Command Center*, step 18: Works in Access Rights Preview, Impact & Synchronization → Validate accreditation access before publishing it to Access Control.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-663?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-654`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
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

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listAccessProfiles": {"method":"GET","path":"/accreditation-access-profiles","contract":"accreditation","summary":"Named bundles of zones, dates and times","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccessProfile"},
"listAccreditationHolders": {"method":"GET","path":"/accreditation-holders","contract":"accreditation","summary":"Everybody accredited, and what state they are in","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"organisationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"previewAccessImpact": {"method":"POST","path":"/accreditation-access-profiles/preview","contract":"accreditation","summary":"Who this change would affect, and how","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessProfile","responds":"AccessImpact"},
"setAccessProfile": {"method":"PUT","path":"/accreditation-access-profiles","contract":"accreditation","summary":"Define which zones, on which dates, at which times","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessProfile","responds":"AccessProfile"},
"setAccreditationStatus": {"method":"POST","path":"/accreditation-holders/{holderId}/status","contract":"accreditation","summary":"Suspend, reactivate, revoke or expire an accreditation","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"setHolderAccess": {"method":"PUT","path":"/accreditation-holders/{holderId}/access","contract":"accreditation","summary":"Assign profiles, and any exception on top","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"HolderAccess","responds":"HolderAccess"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessImpact": {"type":"object","description":"Board 5.10. **There is no undo fast enough once a shift has started.**","properties":{"holdersAffected":{"type":"integer"},"gainingAccess":{"type":"integer"},"losingAccess":{"type":"integer"},"leftWithNoAccess":{"type":"array","items":{"type":"object","properties":{"holderId":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"zonesAdded":{"type":"array","items":{"type":"string"}},"zonesRemoved":{"type":"array","items":{"type":"string"}}}},
"AccessProfile": {"type":"object","x-ticvai-persistence":"accreditation.access_profile","description":"Board 5.2. **How an estate stays governable.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"zoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"operationalAreas":{"type":"array","items":{"type":"string"}},"schedule":{"type":"array","description":"**Zone, date and time are three dimensions and all three are needed.**","items":{"type":"object","properties":{"zoneId":{"type":"string","format":"uuid","nullable":true},"daysOfWeek":{"type":"array","items":{"type":"string"}},"dateFrom":{"type":"string","format":"date","nullable":true},"dateTo":{"type":"string","format":"date","nullable":true},"from":{"type":"string","nullable":true},"to":{"type":"string","nullable":true},"eventPhase":{"type":"string","nullable":true,"enum":["build","rehearsal","doorsOpen","liveShow","breakdown"]}}}},"escortRequired":{"type":"boolean","default":false},"holderCount":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationHolder": {"type":"object","x-ticvai-persistence":"accreditation.holder","description":"**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n","required":["id","fullName"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true},"nationality":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true,"description":"12.1.16. The holder's own address — where a mobile credential and renewal notices go"},"phone":{"type":"string","nullable":true,"description":"12.1.16. E.164"},"identityDocumentVerified":{"type":"boolean","default":false},"organisationId":{"type":"string","format":"uuid","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","suspended","revoked","expired","archived"]},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"completenessPercent":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"HolderAccess": {"type":"object","x-ticvai-persistence":"accreditation.holder_access","description":"Boards 5.7 and 5.8. **An exception with no end is a profile change nobody reviewed.**\n","properties":{"holderId":{"type":"string","format":"uuid"},"accessProfileIds":{"type":"array","items":{"type":"string","format":"uuid"}},"exceptions":{"type":"array","items":{"type":"object","properties":{"zoneId":{"type":"string","format":"uuid"},"grant":{"type":"boolean"},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string"},"approvedBy":{"type":"string","format":"uuid","nullable":true}}}},"effectiveZones":{"type":"array","readOnly":true,"items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"}}}
}
```
