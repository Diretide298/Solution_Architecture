# WS03 — Access Control board 3

**10 screens · 17 operations · 23 schemas · 4 permissions**

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
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, GUEST_MANAGE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-164` | Digital Credential Security Command Center | C | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-165` | Dynamic QR Security Profile Builder | C | 13 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-166` | Credential Activation & Display Rules | A | 6 | 4 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-167` | Device Binding & Session Security | A | 5 | 18 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-168` | BLE Beacon & Geofence Configuration | A | 21 | 21 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-169` | Credential Transfer & Rebinding | C | 9 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-170` | Credential Revocation & Lifecycle Events | C | 7 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-171` | Offline Cryptographic Validation Profile | C | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-172` | Embedded Entitlement Payload Designer | C | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-173` | Credential Security Simulation, Audit & Publication | C | 0 | 13 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-166, BO-170, BO-171, BO-172, BO-173 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-164` Digital Credential Security Command Center

**Central configuration and monitoring page for all secure digital credentials.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-164 |
| Who uses it | venue staff holding `AUDIT_VIEW`, `SCOPE_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/digital-credential-security-command-center-bo-164` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The command centre monitors; the device-binding and dynamic-profile writes belong to BO-167 and BO-165, which declare them (ADR-0041, DI-653; design-notes … Removed 2 October 2026 (CHG-WIR-001): The command centre monitors; the device-binding and dynamic-profile writes belong to BO-167 and BO-165, which declare them (ADR-0041, DI-653; design-notes …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The command centre of the digital credential security board: KPI tiles (active digital credentials, dynamic QR enabled, device-bound, location-protected, offline-ready, revoked today, transfers, security alerts, suspicious sessions) and the credential portfolio (dynamic QR tickets, memberships, annual passes) by security profile, with tiles into the nine detail screens. The one thing to get right: show posture at a glance and where it is weak, not a settings form.

**Known correction pending (do not draw the wrong version)**

- **Table labelled "Every digital credential security" bound to one column (credentialType)** Why: Generated placeholder; the pack lists the per-profile columns. *(source: screens/P08-venue-back-office.yaml#BO-164; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Primary action "Save device binding policy" (and a dynamic profile write) on the command centre (CHG-WIR-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Digital Credentials** (metric tile)

**Dynamic QR Enabled** (metric tile)

**Device-Bound Credentials** (metric tile)

**Location-Protected Credentials** (metric tile)

**Offline-Ready Credentials** (metric tile)

**Credentials Revoked Today** (metric tile)

**Transfer Events** (metric tile)

**Security Alerts** (metric tile)

**Suspicious Sessions** (metric tile)

**Every digital credential security** (data table, from `listDigitalCredentialSecurity`)

| Shows | Format | Notes |
|---|---|---|
| Credential type | chip: Dynamic QR ticket, Membership, Annual pass, Mobile wallet, Loyalty, Digital pass… | — |

**The selected digital credential security** (detail panel): The pack groups this record's detail under its own headings: “For each credential profile”.

| Shows | Format | Notes |
|---|---|---|
| Credential type | chip: Dynamic QR ticket, Membership, Annual pass, Mobile wallet, Loyalty, Digital pass… | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: The nine tiles from the pack with today's delta; Security alerts and Suspicious sessions turn red above zero and open the list behind them (per VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-164)*
- **Portfolio table**: One row per credential profile: credential type, QR mode (Static, Dynamic, Dynamic + device, Dynamic + location, Dynamic + device + location), refresh interval, device binding policy, offline-ready, active count. *(source: screens/P08-venue-back-office.yaml#BO-164 / contracts/spine/access.yaml#setDynamicSecurityProfile)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open a detail screen**: Tiles to BO-165 to BO-173 and back (VO-R13). *(source: DI-653)*

**Data it reads**: `listDigitalCredentialSecurity` (onLoad, Digital Credential Security Command Center); `listCredentialSecurity` (onLoad, Credential Security Simulation, Audit & Publication)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-165` Dynamic QR Security Profile Builder: *Works in Dynamic QR Security Profile Builder*; calls `listDigitalCredentialSecurity`
- → `BO-166` Credential Activation & Display Rules: *Works in Credential Activation & Display Rules*; calls `listDigitalCredentialSecurity`
- → `BO-167` Device Binding & Session Security: *Works in Device Binding & Session Security*; calls `listDigitalCredentialSecurity`
- → `BO-168` BLE Beacon & Geofence Configuration: *Works in BLE Beacon & Geofence Configuration*; calls `listDigitalCredentialSecurity`
- → `BO-169` Credential Transfer & Rebinding: *Works in Credential Transfer & Rebinding*; calls `listDigitalCredentialSecurity`
- → `BO-170` Credential Revocation & Lifecycle Events: *Works in Credential Revocation & Lifecycle Events*; calls `listDigitalCredentialSecurity`
- → `BO-171` Offline Cryptographic Validation Profile: *Works in Offline Cryptographic Validation Profile*; calls `listDigitalCredentialSecurity`
- → `BO-172` Embedded Entitlement Payload Designer: *Works in Embedded Entitlement Payload Designer*; calls `listDigitalCredentialSecurity`
- → `BO-173` Credential Security Simulation, Audit & Publication: *Works in Credential Security Simulation, Audit & Publication*; calls `listDigitalCredentialSecurity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital credential security list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital credential security untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital credential security yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital credential security are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No dynamic QR profile yet**: Empty state "All tickets use standard QR" with "Create a dynamic QR profile" leading to BO-165. *(source: designer default)*

#### Consistency with other screens

- Match `BO-165`: QR mode names identical to the profile builder.
- Match `GST-055`: Refresh interval shown here is what the guest's countdown shows.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  activeDigital: 18240
  dynamicQr: 12900
  deviceBound: 11760
  locationProtected: 6400
  offlineReady: 18240
  revokedToday: 37
  transfers: 112
  securityAlerts: 3
  suspiciousSessions: 5
profiles:
- type: Dynamic QR tickets
  mode: Dynamic + device
  refresh: 30 s
  binding: 1 device, OTP to change
- type: Annual passes
  mode: Dynamic + device + location
  refresh: 30 s
  binding: 1 device, supervisor approval
```

#### Permissions

- `listDigitalCredentialSecurity` → `SCOPE_VIEW` (read) · staff
- `listCredentialSecurity` → `AUDIT_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-164` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-164`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 1: Opens Digital Credential Security Command Center → Central configuration and monitoring page for all secure digital credentials.
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F113 branch at step 1 (expected): when Nothing has been set up on Digital Credential Security Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F113 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …
- ADR-0041 *A command centre is a saved dashboard, not a screen* (`docs/adr/0041-a-command-centre-is-a-saved-dashboard.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-164?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-165`, `BO-166`, `BO-167`, `BO-168`, `BO-169`, `BO-170`, `BO-171`, `BO-172`, `BO-173`.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-165` Dynamic QR Security Profile Builder

**Configure how a dynamic QR is generated and protected. The matrix requires a unique QR per issued ticket/pass and periodic QR refresh to reduce screenshot and duplication fraud.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-165 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Options; Configuration may include) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/dynamic-qr-security-profile-builder-bo-165` |

**What the spec says about it.** **QR refresh: 30 seconds by default; the venue may choose 15, 30, 45, 60 or a custom value of at least 5 seconds (decided 2 October 2026 by Chinmay, DEC-233, DEC-136; CHG-CSP-024, `refreshIntervalSeconds`).**

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of dynamic QR security profiles (setDynamicSecurityProfile has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Builds reusable dynamic QR security profiles: the QR mode (static, dynamic, dynamic + device bound, dynamic + location bound, dynamic + device + location bound), how often the code refreshes, and what the signed token carries. Profiles are then applied per event or product, with exceptions falling back to standard QR or RFID (VIP invitations, B2B/reseller tickets). The one thing to get right: the screen configures policy and never shows or asks for keys - the signature component is a reference to the platform's key store.

**Known correction pending (do not draw the wrong version)**

- **Each refresh option (15 sec, 30 sec, 45 sec, 60 sec, Custom) and each payload component is a separate selectField; a textField is labelled with the sample "Refresh Every 30 seconds"** Why: They are values of two fields (one segmented control, one checkbox list); sample used as a label. *(source: screens/P08-venue-back-office.yaml#BO-165; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No way to say which events or products use a profile, nor a per-product override** Why: The MoM decided dynamic QR per event with per-product exceptions; the profile has no assignment. *(source: DI-633 / contracts/spine/access.yaml#/components/schemas/DynamicQrSecurityProfileBuilderInput; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No maximum QR age the gate accepts** Why: The pack's security test denies a code 72 seconds old against "configured maximum 60 seconds"; nothing configures that maximum. *(source: screens/P08-venue-back-office.yaml#BO-173 / contracts/spine/access.yaml#setDynamicSecurityProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write-only (no read of existing profiles); Save has no operation bound (CHG-WIR-004)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the refresh interval in the 15-60 s range of the pack, or the 6-12 s the client mentioned for beacon-activated codes?** → QR refresh: 30 s default; offer 15/30/45/60 and custom (5 s minimum). *(decided by Chinmay, 2026-10-02; DEC-233 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Refresh Every: 30 seconds | text field | — | — | — | — | — | — |
| 15 sec | select field | — | — | — | — | — | — |
| 30 sec | select field | — | — | — | — | — | — |
| 45 sec | select field | — | — | — | — | — | — |
| 60 sec | select field | — | — | — | — | — | — |
| Custom | select field | — | — | — | — | — | — |
| Credential ID | select field | — | — | — | — | — | — |
| Ticket ID | select field | — | — | — | — | — | — |
| Timestamp | select field | — | — | — | — | — | — |
| Nonce / OTP | select field | — | — | — | — | — | — |
| Device binding reference | select field | — | — | — | — | — | — |
| Venue context | select field | — | — | — | — | — | — |
| Entitlement payload | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name / profileId**: Name (Arabic variant) and a profile code (max 64, upper-case, e.g. DQR-DEVICE-30) shown as "Profile code"; code read-only once a product uses it. *(source: contracts/spine/access.yaml#setDynamicSecurityProfile)*
- **qrMode**: Five cards in the pack's order with what each protects against (screenshots, sharing to another phone, use away from the venue); Static greys the refresh and token sections. *(source: screens/P08-venue-back-office.yaml#BO-165 / contracts/spine/access.yaml#setDynamicSecurityProfile)*
- **refreshIntervalSeconds**: Segmented control 15 s / 30 s (default) / 45 s / 60 s / Custom; Custom reveals a seconds field. The MoM's 6-12 s (beacon-triggered) is reachable only through Custom; 30 s is the default (as on GST-055), and Custom has a 5 s minimum. *(source: screens/P08-venue-back-office.yaml#BO-165 / contracts/spine/access.yaml#setDynamicSecurityProfile / DI-632 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **payloadComponents**: Checkbox list Credential ID, Ticket ID, Timestamp, Nonce / OTP, Device binding reference, Venue context, Entitlement payload, Signature key reference; Timestamp and Signature key reference are locked on for any dynamic mode; Device binding reference is forced on for device-bound modes. Entitlement payload links to BO-172 where its content is designed. *(source: screens/P08-venue-back-office.yaml#BO-165 / contracts/spine/access.yaml#setDynamicSecurityProfile / TRACKER Actions row 225)*
- **venueId**: From the session (VO-R09). *(source: ADR-0030)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **QR lifecycle strip**: Generate > Display > Refresh > Validate > Rotate > Expire, with the chosen interval written on the Refresh arrow. *(source: screens/P08-venue-back-office.yaml#BO-165)*
- **Phone preview**: A phone frame showing the code with its countdown ring at the chosen interval (the guest's GST-055 view). *(source: screens/P08-venue-back-office.yaml#BO-165 / DI-632)*
- **Where it is used**: Products and events using the profile, and the exceptions that fall back to standard QR or RFID. *(source: DI-633 / TRACKER Actions row 226)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save profile**: Whole-profile upsert (VO-R04); applies to codes generated after the save; codes already on phones roll over at their next refresh. *(source: contracts/spine/access.yaml#setDynamicSecurityProfile)*

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `setDynamicSecurityProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic security profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic security profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic security profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Device- or location-bound mode chosen but no device binding policy or no beacons/geofence exist**: Warn with a link to BO-167 or BO-168 ("Guests could not activate their code"). *(source: screens/P08-venue-back-office.yaml#BO-165 / screens/P08-venue-back-office.yaml#BO-168)*
- **Guest phone offline at the gate**: Note under the mode that the code must still render and refresh offline (time-based), as agreed. *(source: DI-631)*

#### Consistency with other screens

- Match `BO-164`: The QR mode names and refresh shown in the command centre's portfolio are these.
- Match `BO-173`: The maximum QR age the gate accepts is tested there; it must relate to this interval.
- Match `GST-055`: The guest countdown equals the refresh interval.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- name: Day tickets - device bound
  code: DQR-DEVICE-30
  mode: Dynamic + device bound
  refresh: 30 s
  components: Credential ID, Ticket ID, Timestamp, Nonce, Device binding reference, Signature key reference
- name: Annual passes - full
  code: DQR-FULL-15
  mode: Dynamic + device + location bound
  refresh: 15 s
- name: VIP invitations
  code: STATIC-VIP
  mode: Static
```

#### Permissions

- `setDynamicSecurityProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic QR is chosen per event (fully dynamic, normal, or mixed); a per-product override disables it for exceptions such as physically delivered VIP invitations and B2B/reseller tickets, which fall back to standard QR or RFID. *(agreed · MoM 2 Sep 2026, 4.7 Dynamic QR Code - Business Flexibility & Exceptions · DI-633)*
- **Open question.** Dynamic QR refreshes periodically to cut fraud/resale. Open: beacon-based (code hidden until the phone is near a gate beacon via Bluetooth, then refreshes ~every 2 minutes; Qossai: more secure) vs app-generated; GPS geofencing also raised. Chinmay to propose. *(open · MoM 2 Sep 2026, 4.6 Dynamic QR Code - Concept & Generation Approach · DI-630)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-165` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-165`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 2: Works in Dynamic QR Security Profile Builder → Configure how a dynamic QR is generated and protected. The matrix requires a unique QR per issued ticket/pass and periodic QR refresh to reduce screenshot and duplication fraud.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-165?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-166` Credential Activation & Display Rules

**Configure when the guest is permitted to see/use the credential. The matrix specifies that after registration, a ticket may appear as a blurred QR and only become clear and usable near the park entrance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · task APP-SETUP-BO-166 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-activation-display-rules-bo-166` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Rules for when a guest may see and use their digital credential: what the app shows before activation (hidden, blurred, countdown, "available at the venue", directions) and once active (dynamic QR, activation timer, status, remaining entitlements), and what activates it (visit date, geofence, beacon, ticket valid, registered device). The one thing to get right: activation conditions are composed with AND / AND-OR exactly as the pack shows, and the guest-side preview updates live.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- activationTriggers is an array of free strings (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Content region is an empty unbound table and the save button has no permission (CHG-SBO-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Beacon-first or app-generated dynamic QR (and GPS geofencing as well)?** → Drawn default accepted: Offer both triggers with AND/OR as the pack shows. *(decided by Chinmay, 2026-10-02; DEC-127 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Form: Save activation and display rule** (modal, opened by *Save activation and display rule*; *Save activation and display rule* calls `setCredentialActivationDisplay`, *Cancel* sends nothing)

**Collects what `setCredentialActivationDisplay` sends before it is called.** Required: `venueId`, `name`, `beforeActivationDisplay`, `activeDisplay`, `activationTriggers`. Optional: `ruleId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rule `ruleId` | picker: choose a rule | optional | — | — | shows names, sends the id | Absent creates a rule | `setCredentialActivationDisplay` body |
| Venue `venueId` | text field | required | — | — | — | Venue the rule applies to | `setCredentialActivationDisplay` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setCredentialActivationDisplay` body |
| Before activation display `beforeActivationDisplay` | multi-select chips | required | — | Hide QR · Blur QR · Show countdown · Show available at venue · Show venue directions | — | What the guest sees before the credential activates | `setCredentialActivationDisplay` body |
| Active display `activeDisplay` | multi-select chips | required | — | Dynamic QR · Activation timer · Credential status · Remaining entitlements | — | What the guest sees once it is active | `setCredentialActivationDisplay` body |
| Activation triggers `activationTriggers` | list of values (chips) | required | — | at least 1 | — | What activates the credential, e.g. | `setCredentialActivationDisplay` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 No activation trigger, or a display option that contradicts another (hideQr with blurQr)

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **beforeActivationDisplay**: Multi-select of Hide code, Blur code, Show countdown, Show "Available at the venue", Show directions to the venue; at least one. *(source: screens/P08-venue-back-office.yaml#BO-166 / contracts/spine/access.yaml#setCredentialActivationDisplay)*
- **activeDisplay**: Multi-select of Dynamic QR, Activation timer, Credential status, Remaining entitlements; Dynamic QR on by default. *(source: contracts/spine/access.yaml#setCredentialActivationDisplay)*
- **activationTriggers**: Condition rows from the pack - Visit date must equal ticket date AND (Inside geofence AND/OR Beacon detected) AND Ticket valid AND Registered device - with the AND/OR switch between geofence and beacon. Geofences and beacons are picked from BO-168, not typed. *(source: screens/P08-venue-back-office.yaml#BO-166 / contracts/spine/access.yaml#setCredentialActivationDisplay)*

#### Outputs: what the screen shows and produces

**Shown**

**Activation and display rules** (data table, from `listCredentialActivationDisplay`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Before activation display | list or chips (count when long) | — |
| Active display | list or chips (count when long) | — |
| Activation triggers | list or chips (count when long) | Conditions that make the credential eligible, e.g. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save activation and display rule (primary button) | `setCredentialActivationDisplay` PUT `/credential-activation-display` | CredentialActivationDisplayRulesInput | CredentialActivationDisplayRulesView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 No activation trigger, or a display option that contradicts another (hideQr with blurQr) | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Phone preview**: Two phone frames side by side, "Before activation" and "Active", rendering the guest screen (GST-055) with the chosen options. *(source: screens/P08-venue-back-office.yaml#BO-166 / DI-632)*
- **Credential states**: Show the state chain Registered > Hidden/Blurred > Eligible > Active > Validated > Expired/Consumed/Revoked as a legend. *(source: screens/P08-venue-back-office.yaml#BO-166)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rule**: Whole-rule upsert (VO-R04); new rule sends no ruleId. *(source: contracts/spine/access.yaml#setCredentialActivationDisplay)*

**Data it reads**: `listCredentialActivationDisplay` (onLoad, Credential Activation & Display Rules)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listCredentialActivationDisplay`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential activation display list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential activation display untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential activation display yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential activation display are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 No activation trigger, or a display option that contradicts another (hideQr with blurQr) |

#### Edge cases to draw

- **Rule requires a beacon but the venue has none registered**: Warn "No beacons registered - guests could never activate" and link to BO-168. *(source: designer default)*
- **Guest phone offline**: The preview notes the code still activates by time and geofence on the device; activation must not depend on the network. *(source: DI-631)*

#### Consistency with other screens

- Match `GST-055`: The before/active states drawn there must be exactly these options.
- Match `BO-168`: Beacons and geofences named here are the ones registered there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: Aqua Park - activate at the gates
  before: Blur code + Show countdown
  active: Dynamic QR + Remaining entitlements
  triggers: Visit date = ticket date AND (Main Entrance geofence 150 m OR Gate beacon) AND Ticket valid AND Registered
    device
```

#### Permissions

- `listCredentialActivationDisplay` → `SCOPE_VIEW` (read) · staff
- `setCredentialActivationDisplay` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic QR is chosen per event (fully dynamic, normal, or mixed); a per-product override disables it for exceptions such as physically delivered VIP invitations and B2B/reseller tickets, which fall back to standard QR or RFID. *(agreed · MoM 2 Sep 2026, 4.7 Dynamic QR Code - Business Flexibility & Exceptions · DI-633)*
- The dynamic QR stays blurred until beacon proximity is detected, then activates and refreshes on a short interval (e.g. every 6-12 seconds); screenshot capture of the active code is prevented. *(client request · MoM 2 Sep 2026, 4.6 Credential activation and display rules · DI-632)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-166` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-166`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 4: Works in Credential Activation & Display Rules → Configure when the guest is permitted to see/use the credential. The matrix specifies that after registration, a ticket may appear as a blurred QR and only become clear and usable near the park …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-166?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save activation and display rule.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-167` Device Binding & Session Security

**Prevent one credential from being shared across unauthorized devices. The source explicitly requires tickets to be linked to a specific device/user and suspicious patterns such as device sharing and multiple simultaneous sessions to be detected.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · task APP-SETUP-BO-167 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `GUEST_MANAGE`, `SCOPE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `bindingId` (navigation) |
| Route | `/access-venue/device-binding-session-security-bo-167` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Stops one credential being used on several phones: the venue's binding policy (maximum active devices, concurrent sessions, what a device change needs - not allowed, allowed before first use, OTP, operator approval, supervisor approval) and the list of current bindings (guest, credential, device, app installation, OS, registered, last activated, last venue, security status), from which a service agent can release a credential from a lost phone. The one thing to get right: suspicious bindings come first - "Active on device A, activation attempted on device B: blocked and alerted" - and a release is a deliberate, reasoned act.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The policy write is one per venue and has no "binding required" switch (CHG-SBO-005)
- The contract still says "Deactivate binding (no operation yet)" (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Table labelled "Every device binding session" and the detail panel headings taken from the pack's example sentences ("Credential active on … (CHG-SBO-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the binding policy per venue or per credential profile (day tickets vs annual passes)?** → Drawn default accepted: Draw the venue policy with a greyed "Per profile" option. *(decided by Chinmay, 2026-10-02; DEC-234 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Form: Save device binding policy** (modal, opened by *Save device binding policy*; *Save device binding policy* calls `setDeviceBindingPolicy`, *Cancel* sends nothing)

**Collects what `setDeviceBindingPolicy` sends before it is called.** Required: `venueId`. Optional: `maximumActiveDevices`, `concurrentSessions`, `deviceChangePolicy`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setDeviceBindingPolicy` body |
| Maximum active devices `maximumActiveDevices` | number field | optional | 1 | min 1 | — | Devices the credential may be active on at once | `setDeviceBindingPolicy` body |
| Concurrent sessions `concurrentSessions` | number field | optional | 1 | min 1 | — | — | `setDeviceBindingPolicy` body |
| Device change policy `deviceChangePolicy` | radio group | optional | OTP verification required | Not allowed · Allowed before first use · OTP verification required · Operator approval required · Supervisor approval required | — | — | `setDeviceBindingPolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Release credential device** (modal, opened by *Release credential device*; *Release credential device* calls `releaseCredentialDevice`, *Cancel* sends nothing)

**Collects what `releaseCredentialDevice` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `releaseCredentialDevice` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `binding-released`: the binding is already released.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **maximumActiveDevices / concurrentSessions**: Steppers min 1, default 1, as the pack shows. *(source: screens/P08-venue-back-office.yaml#BO-167 / contracts/spine/access.yaml#setDeviceBindingPolicy)*
- **deviceChangePolicy**: Single choice of the five options, default OTP verification required, each with who acts (guest, service agent, supervisor). *(source: screens/P08-venue-back-office.yaml#BO-167 / contracts/spine/access.yaml#setDeviceBindingPolicy / DI-636)*
- **Release reason**: Required, max 500, in the Release dialog (e.g. "Lost phone - verified by Emirates ID at Guest Services"). *(source: contracts/spine/access.yaml#releaseCredentialDevice)*
- **venueId**: From the session (VO-R03); one policy per venue. *(source: contracts/spine/access.yaml#setDeviceBindingPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Device bindings** (data table, from `listDeviceBindingSession`)

| Shows | Format | Notes |
|---|---|---|
| User | text | User |
| Credential | text | Credential |
| App installation | text | App installation |
| Os | text | OS |
| Registration date | 1 Oct 2026, 14:30 | Registration date |
| Last activation | 1 Oct 2026, 14:30 | Last activation |
| Last known venue | text | Last known venue |
| Device | text | Device ID |
| Device reference | text | Device reference |

**The selected binding** (detail panel, from `listDeviceBindingSession`): The pack groups this record's detail under its own headings: “Maximum Active Devices”, “Concurrent Sessions”, “Device Change”, “Credential active on Device A”, “Response”.

| Shows | Format | Notes |
|---|---|---|
| User | text | User |
| Credential | text | Credential |
| App installation | text | App installation |
| Os | text | OS |
| Registration date | 1 Oct 2026, 14:30 | Registration date |
| Last activation | 1 Oct 2026, 14:30 | Last activation |
| Last known venue | text | Last known venue |
| Device | text | Device ID |
| Device reference | text | Device reference |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save device binding policy (primary button) | `setDeviceBindingPolicy` PUT `/device-binding-policy` | DeviceBindingPolicyInput | AccessCredentialPolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Release credential device (secondary button) | `releaseCredentialDevice` POST `/device-bindings/{bindingId}/release` | inline | AccessDeviceBinding | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Policy card**: The policy in force from the read's summary ("1 device, 1 session, OTP to change"), with Edit. *(source: contracts/spine/access.yaml#/components/schemas/DeviceBindingSessionSecurityViewSummary)*
- **Bindings list**: Titled "Device bindings"; columns Guest, Credential (ticket number), Device (model and a masked reference), OS, Registered, Last activation, Last venue, Status. Status Normal / Suspicious (amber) / Blocked (red); default sort Blocked and Suspicious first. Cursor paging (VO-R12) - the list grows with guests. *(source: screens/P08-venue-back-office.yaml#BO-167 / contracts/spine/access.yaml#listDeviceBindingSession)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save binding policy**: Replaces the venue's policy whole (VO-R04); applies to new bindings and device changes from now. *(source: contracts/spine/access.yaml#setDeviceBindingPolicy)*
- **Release credential from device**: Confirmation "VT-2026-000009821 can be activated on a new phone; the old phone's code stops working"; already released gives 409 binding-released. Needs guest management rights (VO-R08). *(source: contracts/spine/access.yaml#releaseCredentialDevice)*

**Data it reads**: `listDeviceBindingSession` (onLoad, Device Binding & Session Security)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listDeviceBindingSession`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device binding session list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device binding session untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device binding session yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the device binding session are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `binding-released`: the binding is already released. |

#### Edge cases to draw

- **Second simultaneous device**: Activation blocked and a security alert raised; the row shows Blocked with both devices. *(source: screens/P08-venue-back-office.yaml#BO-168 / contracts/spine/access.yaml#listDeviceBindingSession)*
- **Guest changes phone before first use under "allowed before first use"**: Self-service rebinding; the row shows the device change in its history. *(source: screens/P08-venue-back-office.yaml#BO-167)*

#### Consistency with other screens

- Match `BO-164`: The command centre's device-bound counts and suspicious sessions tile open this list filtered.
- Match `BO-169`: A transfer removes the sender's binding; the list shows it as released by transfer.
- Match `GST-055`: The guest sees "This ticket is active on another phone" with the same change rule.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  maxDevices: 1
  sessions: 1
  change: OTP verification required
bindings:
- guest: Sara Al Nuaimi
  credential: VT-2026-000009821
  device: iPhone 15 - ...4F2A
  os: iOS 18.6
  registered: 28 Sep 2026
  lastActivation: 1 Oct 2026 10:14
  venue: Aqua Park
  status: Normal
- guest: Khalid Al Zaabi
  credential: VT-2026-000010377
  device: Galaxy S24 - ...91C0
  os: Android 15
  status: Blocked
  note: Activation attempted on a second device 1 Oct 2026 10:21
```

#### Permissions

- `listDeviceBindingSession` → `SCOPE_VIEW` (read) · staff
- `setDeviceBindingPolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `releaseCredentialDevice` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-167` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-167`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 6: Works in Device Binding & Session Security → Prevent one credential from being shared across unauthorized devices. The source explicitly requires tickets to be linked to a specific device/user and suspicious patterns such as device sharing and …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-167?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save device binding policy, Release credential device.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `GUEST_MANAGE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-168` BLE Beacon & Geofence Configuration

**Configure location-aware credential activation. This is a major requirement under 3.1.9. The matrix requires BLE beacon proximity and geofence boundaries to activate/deactivate credentials at venue, attraction, zone and gate level.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · task APP-SETUP-BO-168 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Map-Based Configuration; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/ble-beacon-geofence-configuration-bo-168` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists the registered BLE beacons and geofences (setBleBeaconGeofence has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Registers the venue's BLE beacons and draws geofences on the venue map, at venue, park, zone, attraction or gate level, so credentials can activate or deactivate by location. The one thing to get right: it is map-first - pick a place, draw the zone (e.g. Main Entrance activation zone, 150 m), and see beacons as pins with health.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write-only screen; no read of registered beacons or geofences (CHG-WIR-004)
- Placement fields are free strings (venue, zone, gate, park, attraction) and health/lastDetected are in the write (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Every input is a selectField (Beacon Name, Beacon ID, Proximity threshold, Health) and the action bar has buttons labelled Venue … (CHG-SBO-009).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Beacon name | text field | optional | — | — | — | Beacon Name | `BleBeaconGeofenceConfigurationInput.beaconName` |
| Beacon ID | text field | optional | — | — | — | Beacon ID | `BleBeaconGeofenceConfigurationInput.beaconId` |
| Venue | text field | optional | — | — | — | Venue | `BleBeaconGeofenceConfigurationInput.venue` |
| Zone | text field | optional | — | — | — | Zone | `BleBeaconGeofenceConfigurationInput.zone` |
| Gate | text field | optional | — | — | — | Gate | `BleBeaconGeofenceConfigurationInput.gate` |
| Proximity threshold (metres) | number field | optional | — | — | — | Metres | `BleBeaconGeofenceConfigurationInput.proximityThreshold` |
| Active | segmented control | optional | — | Active · Inactive | — | Active/Inactive | `BleBeaconGeofenceConfigurationInput.activeInactive` |
| Geofence level | select field | — | — | — | — | Venue, attraction, zone or gate: the level the geofence activates the credential at (the board drew these as buttons). | — |

**Form: Save beacon** (modal, opened by *Save beacon*; *Save beacon* calls `setBleBeaconGeofence`, *Cancel* sends nothing)

**Collects what `setBleBeaconGeofence` sends before it is called.** Required: `beaconId`, `venue`. Optional: `beaconName`, `zone`, `gate`, `proximityThreshold`, `activeInactive`, `health`, `lastDetected`, `park`, `attraction`, `geofenceRadiusMeters`, `geofenceBoundary`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Beacon name `beaconName` | text field | optional | — | — | — | Beacon Name | `setBleBeaconGeofence` body |
| Beacon `beaconId` | text field | required | — | — | — | Beacon ID | `setBleBeaconGeofence` body |
| Venue `venue` | text field | required | — | — | — | Venue | `setBleBeaconGeofence` body |
| Zone `zone` | text field | optional | — | — | — | Zone | `setBleBeaconGeofence` body |
| Gate `gate` | text field | optional | — | — | — | Gate | `setBleBeaconGeofence` body |
| Proximity threshold `proximityThreshold` | number field | optional | — | — | — | Metres | `setBleBeaconGeofence` body |
| Active inactive `activeInactive` | segmented control | optional | — | Active · Inactive | — | Active/Inactive | `setBleBeaconGeofence` body |
| Health `health` | segmented control | optional | — | Healthy · Degraded · Offline | — | Read-only, reported by the beacon | `setBleBeaconGeofence` body |
| Last detected `lastDetected` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Last detected | `setBleBeaconGeofence` body |
| Park `park` | text field | optional | — | — | — | Park | `setBleBeaconGeofence` body |
| Attraction `attraction` | text field | optional | — | — | — | Attraction | `setBleBeaconGeofence` body |
| Geofence radius meters `geofenceRadiusMeters` | number field | optional | — | — | — | Radius of a circular activation zone | `setBleBeaconGeofence` body |
| Geofence boundary `geofenceBoundary` | list of values (chips) | optional | — | — | — | Polygon points as lat,lng when the zone is drawn | `setBleBeaconGeofence` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Beacon registry**: Beacon name, beacon id (hardware UUID/major/minor as one string), placement (venue, park, zone, attraction, gate pickers that cascade), proximity threshold in metres, Active/Inactive. Health and last detected are read-only. *(source: screens/P08-venue-back-office.yaml#BO-168 / contracts/spine/access.yaml#setBleBeaconGeofence)*
- **Geofence**: Draw a circle (radius in metres) or polygon on the map; the radius field and the drawn shape stay in sync; one or the other, not both. *(source: contracts/spine/access.yaml#setBleBeaconGeofence)*

#### Outputs: what the screen shows and produces

**Shown**

**Load the configuration as saved** (detail panel, from `getBleBeaconGeofence`)

| Shows | Format | Notes |
|---|---|---|
| Beacon name | text | Beacon Name |
| Venue | text | Venue |
| Zone | text | Zone |
| Gate | text | Gate |
| Proximity threshold | 1,234 | Metres |
| Active inactive | chip: Active, Inactive | Active/Inactive |
| Health | chip: Healthy, Degraded, Offline | Read-only, reported by the beacon |
| Last detected | 1 Oct 2026, 14:30 | Last detected |

**Health** (detail panel, from `setBleBeaconGeofence`): Read-only: reported by the beacon, never typed (with last detected).

| Shows | Format | Notes |
|---|---|---|
| Beacon name | text | Beacon Name |
| Beacon | text | Beacon ID |
| Venue | text | Venue |
| Zone | text | Zone |
| Gate | text | Gate |
| Proximity threshold | 1,234 | Metres |
| Active inactive | chip: Active, Inactive | Active/Inactive |
| Health | chip: Healthy, Degraded, Offline | Read-only, reported by the beacon |
| Last detected | 1 Oct 2026, 14:30 | Last detected |
| Park | text | Park |
| Attraction | text | Attraction |
| Geofence radius meters | 1,234 | Radius of a circular activation zone |
| Geofence boundary | list or chips (count when long) | Polygon points as lat,lng when the zone is drawn |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save beacon (primary button) | `setBleBeaconGeofence` PUT `/ble-beacon-geofence` | BleBeaconGeofenceConfigurationInput | BleBeaconGeofenceConfigurationView | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Map**: Venue map from the topology, geofences as translucent shapes labelled with name and radius, beacons as pins coloured by health (Healthy, Degraded, Offline) with last detected time. *(source: screens/P08-venue-back-office.yaml#BO-168)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save beacon / Save zone**: Whole-record upsert (VO-R04). *(source: contracts/spine/access.yaml#setBleBeaconGeofence)*

**Data it reads**: `getBleBeaconGeofence` (onLoad, Load the configuration as saved)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `setBleBeaconGeofence`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ble beacon geofence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ble beacon geofence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ble beacon geofence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Beacon offline**: Pin red; any activation rule that depends only on it is flagged on BO-166. *(source: designer default)*

#### Consistency with other screens

- Match `BO-064`: Access-point geofences for handheld validation (setAccessPointGeofence) are a different thing - guest credential activation here vs staff scanner location there; label both clearly.
- Match `BO-166`: Activation rules pick these zones and beacons.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
beacons:
- name: Main Entrance Beacon 1
  id: E2C56DB5-...-0001
  gate: Main Plaza Gate 1
  threshold: 5 m
  health: Healthy
  lastDetected: 1 Oct 2026 14:02
geofences:
- name: Main Entrance Activation Zone
  radius: 150 m
  level: Park
```

#### Permissions

- `setBleBeaconGeofence` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `getBleBeaconGeofence` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Dynamic QR refreshes periodically to cut fraud/resale. Open: beacon-based (code hidden until the phone is near a gate beacon via Bluetooth, then refreshes ~every 2 minutes; Qossai: more secure) vs app-generated; GPS geofencing also raised. Chinmay to propose. *(open · MoM 2 Sep 2026, 4.6 Dynamic QR Code - Concept & Generation Approach · DI-630)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-168` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-168`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 8: Works in BLE Beacon & Geofence Configuration → Configure location-aware credential activation. This is a major requirement under 3.1.9. The matrix requires BLE beacon proximity and geofence boundaries to activate/deactivate credentials at venue …

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-168?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save beacon.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-169` Credential Transfer & Rebinding

**Securely manage digital-ticket transfers. The matrix requires tickets to be transferable through email/app, with the recipient required to authenticate before accessing and activating the transferred QR.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-169 |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-transfer-rebinding-bo-169` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Releasing a device binding belongs to BO-167 Device Binding; this screen edits transfer policies, not a binding (design-notes correction venue-operations BO-169). Contract gap recorded 2 October 2026 (CHG-WIR-004): No operation saves the credential transfer and rebinding policy.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Sets how a digital ticket may be transferred: whether allowed, how many times, the deadline, before first use only, recipient account, OTP and acceptance required, cancel and return to sender, and audit. The pack's critical behaviour is the point of the screen - the moment a transfer completes the sender's credential is invalid, the old device binding is removed and the recipient's credential becomes active - so a ticket can never be usable by both. The one thing to get right: draw the transfer journey with that hand-over moment, and keep the ticket number unchanged.

**Known correction pending (do not draw the wrong version)**

- **Toggles drawn as selectFields and "Before first validation only" as a textField** Why: The read returns booleans and integers. *(source: screens/P08-venue-back-office.yaml#BO-169; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No policy-to-product link** Why: The screen cannot show or set which products a transfer policy governs. *(source: contracts/spine/access.yaml#listCredentialTransferRebinding; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Read-only - listCredentialTransferRebinding has no write, and the primary button is Release credential device (CHG-WIR-001); Entry parameter bindingId (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Transfer allowed | select field | — | — | — | — | — | — |
| Number of transfers | select field | — | — | — | — | — | — |
| Transfer deadline | select field | — | — | — | — | — | — |
| Before first validation only | text field | — | — | — | — | — | — |
| Require recipient account | select field | — | — | — | — | — | — |
| Require OTP | select field | — | — | — | — | — | — |
| Require acceptance | select field | — | — | — | — | — | — |
| Cancel pending transfer | select field | — | — | — | — | — | — |
| Return to sender | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **transferAllowed**: Master switch; off hides everything else and shows "Tickets under this policy cannot be transferred". *(source: screens/P08-venue-back-office.yaml#BO-169 / contracts/spine/access.yaml#listCredentialTransferRebinding)*
- **numberOfTransfers / transferDeadlineHours**: Steppers - "Up to 1 transfer" (empty = unlimited) and "Until 24 hours before the visit" (hours before the visit date). *(source: contracts/spine/access.yaml#listCredentialTransferRebinding)*
- **Recipient checks**: Toggles Before first validation only (default on), Require recipient account, Require OTP, Require acceptance, Allow sender to cancel a pending transfer, Return to sender if not accepted, Transfer audit required (locked on). *(source: screens/P08-venue-back-office.yaml#BO-169 / contracts/spine/access.yaml#listCredentialTransferRebinding)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Transfer journey**: Sender credential > Transfer request > Original QR protected > Recipient invitation > Recipient login > Accept > New device binding > New credential activation; under it the after-state "Old credential INVALID, old binding REMOVED, recipient ACTIVE/ELIGIBLE, ticket number unchanged". *(source: screens/P08-venue-back-office.yaml#BO-169 / screens/P08-venue-back-office.yaml#BO-170 / DI-620)*
- **Policies list**: Policies by name with a one-line summary ("1 transfer, until 24 h before, OTP + acceptance"); which products use each. *(source: contracts/spine/access.yaml#listCredentialTransferRebinding)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save transfer policy**: Should be a whole-policy upsert (VO-R04); no write exists - draw Save disabled with the reason (see corrections). *(source: contracts/spine/access.yaml#listCredentialTransferRebinding)*
- **Cancel pending transfer**: From a pending transfer, returns the ticket to the sender and re-activates the sender's code; drawn as a row action, not yet available. *(source: screens/P08-venue-back-office.yaml#BO-169 / contracts/spine/access.yaml#listCredentialTransferRebinding)*

**Data it reads**: `listCredentialTransferRebinding` (onLoad, Credential Transfer & Rebinding)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listCredentialTransferRebinding`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential transfer rebinding configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential transfer rebinding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential transfer rebinding configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Recipient never accepts**: With Return to sender on, the transfer expires at the deadline and the sender's code comes back; the original stays protected (not scannable) while pending. *(source: screens/P08-venue-back-office.yaml#BO-169)*
- **Ticket already scanned once**: Transfer refused under "Before first validation only" with that reason. *(source: screens/P08-venue-back-office.yaml#BO-169)*

#### Consistency with other screens

- Match `BO-167`: The sender's binding removal shows in the bindings list.
- Match `GST-014`: The guest-side transfer and claim screens (transferOrderTickets, claimTicketTransfer) follow this policy's checks and wording.
- Match `BO-170`: Transfer is also a lifecycle event whose revocation propagation is set on BO-170.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policies:
- name: Day tickets
  allowed: true
  transfers: 1
  deadline: 24 h before visit
  beforeFirstUse: true
  account: true
  otp: true
  acceptance: true
  returnToSender: true
- name: Annual passes
  allowed: false
journey: Priya Nair sends VT-2026-000009821 to James Carter - pending 2 h - accepted 1 Oct 2026 16:40 - Priya's
  code invalid, James active
```

#### Permissions

- `listCredentialTransferRebinding` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-169` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-169`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 10: Works in Credential Transfer & Rebinding → Securely manage digital-ticket transfers. The matrix requires tickets to be transferable through email/app, with the recipient required to authenticate before accessing and activating the transferred …

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-169?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-170` Credential Revocation & Lifecycle Events

**Immediately invalidate credentials when the underlying ticket changes. Requirement 3.1.4 specifically requires dynamic QR invalidation after refunds, cancellations, transfers, exchanges, upgrades or reissues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-170 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-revocation-lifecycle-events-bo-170` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Makes every ticket lifecycle event invalidate the old credential everywhere it lives. For each event (refund, cancellation, transfer, exchange, upgrade, reissue, expiry, manual invalidation, fraud lock, account suspension) the manager sets the action on the credential (invalidate, suspend, replace) and where the change must reach (central platform, mobile app, gate network, offline revocation package, wallet service). The one thing to get right: a revoked credential can still pass at an offline gate until that gate's revocation package refreshes - show the propagation chain and that exposure window.

**Known correction pending (do not draw the wrong version)**

- **Table "Every credential revocation lifecycle" bound to one column (propagationTargets)** Why: Generated placeholder; the rows are events with action and targets (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-170; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The read lacks monitoredConditions and propagation that the write sets; the write requires id and scopePath** Why: The edit form cannot reopen what it saved (VO-R04); id and scope are server-owned (VO-R03). *(source: contracts/spine/access.yaml#listCredentialRevocationLifecycle / contracts/spine/access.yaml#setCredentialEventPropagationRule; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

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

- **triggerEvent**: One row per event, the pack's ten listed first; each event appears once per venue (the upsert key). The other values of the shared vocabulary (entry, exit, redemption...) belong to BO-340 and are hidden here. *(source: screens/P08-venue-back-office.yaml#BO-170 / contracts/spine/access.yaml#setCredentialEventPropagationRule)*
- **revocationAction**: Invalidate / Suspend / Replace; for Refund, Exchange and Reissue it is locked to the revoking action with "Always revokes". *(source: contracts/spine/access.yaml#setCredentialEventPropagationRule)*
- **propagationTargets**: Five checkboxes in the pack's order; Gate network and Offline revocation package locked on for any revoking action. *(source: screens/P08-venue-back-office.yaml#BO-170 / screens/P08-venue-back-office.yaml#BO-171 / contracts/spine/access.yaml#setCredentialEventPropagationRule)*
- **monitoredConditions**: Multi-select (delayed updates, conflicting states, offline transactions pending sync, provider update failures, stale wallet credentials) - what raises an alert if propagation lags. *(source: contracts/spine/access.yaml#setCredentialEventPropagationRule)*
- **id, scopePath, timestamps**: Not inputs (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Every credential revocation lifecycle** (data table, from `listCredentialRevocationLifecycle`)

| Shows | Format | Notes |
|---|---|---|
| Propagation targets | list or chips (count when long) | — |

**The selected credential revocation lifecycle** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Propagation targets | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save credential event propagation rule (primary button) | `setCredentialEventPropagationRule` PUT `/credential-event-propagation-rules` | AccessCredentialEventPropagationRule | AccessCredentialEventPropagationRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `ACCESS_POINT_CONFIGURE`; opens modal first; produces a document or message: Set how a ticket lifecycle event propagates to the credential |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Event matrix**: Rows = events, columns = action and the five targets as ticks; one glance shows a gap. *(source: contracts/spine/access.yaml#listCredentialRevocationLifecycle)*
- **Worked example**: The pack's upgrade case as a card - "Ticket upgraded - old credential REVOKED, old QR INVALID, new credential GENERATED, new entitlement SYNCHRONIZED". *(source: screens/P08-venue-back-office.yaml#BO-170)*
- **Offline exposure note**: "Offline gates learn of a revocation at their next package refresh - maximum cache age 30 min (set on BO-171)" beside the Offline revocation package target. *(source: screens/P08-venue-back-office.yaml#BO-171 / contracts/spine/access.yaml#setGateOfflinePolicy)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rule**: Upsert keyed by the event (whole row, VO-R04). *(source: contracts/spine/access.yaml#setCredentialEventPropagationRule)*

**Data it reads**: `listCredentialRevocationLifecycle` (onLoad, Credential Revocation & Lifecycle Events)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listCredentialRevocationLifecycle`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential revocation lifecycle list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential revocation lifecycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential revocation lifecycle yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential revocation lifecycle are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Wallet pass cannot be revoked at once (provider delay)**: The stale-wallet condition alerts; the gate still refuses the old credential because it validates against the virtual ticket. *(source: contracts/spine/access.yaml#setCredentialEventPropagationRule / DI-652)*
- **Event with no rule**: Row shown "No rule - credential stays valid" in amber. *(source: designer default)*

#### Consistency with other screens

- Match `BO-340`: Entitlement & Cross-Media Synchronization Rules writes the same table with the wider event list; one vocabulary, same labels.
- Match `BO-171`: The revocation cache age that bounds offline exposure is set there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- event: Refund
  action: Invalidate (always)
  targets: Central platform, Mobile app, Gate network, Offline revocation package, Wallet service
- event: Upgrade
  action: Replace
  targets: All five
  monitored: Stale wallet credentials
- event: Fraud lock
  action: Suspend
  targets: Central platform, Gate network, Offline revocation package
```

#### Permissions

- `listCredentialRevocationLifecycle` → `SCOPE_VIEW` (read) · staff
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-170` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-170`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 12: Works in Credential Revocation & Lifecycle Events → Immediately invalidate credentials when the underlying ticket changes. Requirement 3.1.4 specifically requires dynamic QR invalidation after refunds, cancellations, transfers, exchanges, upgrades or …

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-170?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save credential event propagation rule.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-171` Offline Cryptographic Validation Profile

**Allow access devices to validate secure credentials without continuous backend connectivity. The matrix explicitly requires offline cryptographic validation and embedded entitlement validation without real-time backend connectivity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-171 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/offline-cryptographic-validation-profile-bo-171` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): Save was bound to setOfflinePolicy (tenancy, TENANT_CONFIGURE), the POS workstation offline policy; the gate policy is setGateOfflinePolicy …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Sets what a gate may validate on its own when the network is gone (credential authenticity, signature, ticket, venue, park, zone, visit date, time window, status snapshot, ticket type, guest category, seat, timeslot, reservation, entitlements, re-entry permissions, validity period), for how long (the pack's 8 hours) and what happens after that (continue restricted, operator warning, supervisor mode, fail closed, fallback). The one thing to get right: it is one offline policy per venue shared with BO-208 and BO-210, so the form must carry every part of that policy even though this screen edits only the validation part.

**Known correction pending (do not draw the wrong version)**

- **Content region is an empty table ''** Why: listOfflineCryptographicValidation returns one policy object; draw it as a form, not a table. *(source: contracts/spine/access.yaml#listOfflineCryptographicValidation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The Save button is bound to setOfflinePolicy (tenancy, TENANT_CONFIGURE), the POS workstation offline policy (CHG-WIR-001); Body requires id and scopePath (CHG-WIR-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **offlineChecks**: Checkbox groups as the pack lists them - Authenticity (credential authenticity, digital signature), Identity (ticket ID, ticket type, guest category), Place (venue, park, zone), Time (visit date, time window, timeslot, validity period), State (credential status snapshot, entitlements, re-entry permissions, seat, reservation). Authenticity and signature locked on. *(source: screens/P08-venue-back-office.yaml#BO-171 / contracts/spine/access.yaml#setGateOfflinePolicy)*
- **maxOfflineDurationHours**: "Maximum offline duration [8] hours", whole hours, 0 = must be online. *(source: screens/P08-venue-back-office.yaml#BO-172 / contracts/spine/access.yaml#setGateOfflinePolicy)*
- **afterThresholdBehavior**: Radio list Continue restricted validation, Operator warning, Supervisor mode, Fail closed, Fallback; Fail closed carries a red note "Gate refuses everyone until it reconnects". *(source: screens/P08-venue-back-office.yaml#BO-172 / contracts/spine/access.yaml#setGateOfflinePolicy)*
- **Revocation cache and degraded-mode fields of the same policy**: Shown read-only in a collapsed "Also in this policy" panel with links to BO-208 and BO-210, and sent unchanged on save (VO-R04). *(source: contracts/spine/access.yaml#setGateOfflinePolicy)*
- **id, venueId, scopePath, createdAt, updatedAt**: Not inputs (VO-R03); the policy is keyed on the venue. *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save gate offline policy (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Local security package**: Read-only list of what devices receive - trusted verification material, rules, revocation information, entitlement definitions, validity parameters - with package version and build time; never key material (the pack's acceptance condition). *(source: screens/P08-venue-back-office.yaml#BO-171 / screens/P08-venue-back-office.yaml#BO-172)*
- **Reconnection strip**: Upload scans > Resolve state > Update consumption > Detect conflicts > Refresh local package, linking to sync and reconciliation. *(source: screens/P08-venue-back-office.yaml#BO-172 / F06 step 6)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save offline policy**: Upsert keyed on the venue, replacing the whole policy; the confirmation says "Applies at the next offline package build". *(source: contracts/spine/access.yaml#setGateOfflinePolicy)*

**Data it reads**: `listOfflineCryptographicValidation` (onLoad, Offline Cryptographic Validation Profile)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listOfflineCryptographicValidation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline cryptographic validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline cryptographic validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline cryptographic validation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline cryptographic validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The edge threshold is shorter than the central one. |

#### Edge cases to draw

- **A check is required offline but its data is not embedded in the credential nor in the package**: Warn "Zone cannot be checked offline - add Zone to the payload (BO-172)". *(source: screens/P08-venue-back-office.yaml#BO-172)*
- **Gate offline beyond the maximum**: The scanner shows the chosen behaviour; this screen's preview shows it on a P07 frame. *(source: DI-646)*

#### Consistency with other screens

- Match `BO-208`: Same policy row (revocation cache age and staleness action); one policy, three anchors (VO-R14).
- Match `BO-210`: Same policy row (degraded modes and switch-over timings).
- Match `SCN-015`: The package age and contents shown on the scanner's offline package screen are these.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  venue: Aqua Park
  maxOffline: 8 h
  afterThreshold: Supervisor mode
  checks: Authenticity, Signature, Ticket ID, Venue, Park, Zone, Visit date, Time window, Status snapshot, Entitlements,
    Re-entry permissions
package:
  version: P-2026-10-01-07
  built: 1 Oct 2026 06:00
  devices: 46
```

#### Permissions

- `setGateOfflinePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listOfflineCryptographicValidation` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: the dynamic QR must appear and work without internet, since crowded events (10,000+) suffer severe congestion; it must work offline via Bluetooth/beacon or an equivalent local mechanism. *(agreed · MoM 2 Sep 2026, 4.6 Hard requirement (offline) · DI-631)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-171` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-171`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 14: Works in Offline Cryptographic Validation Profile → Allow access devices to validate secure credentials without continuous backend connectivity. The matrix explicitly requires offline cryptographic validation and embedded entitlement validation …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-171?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save gate offline policy, Cancel.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-172` Embedded Entitlement Payload Designer

**Determine what operational information can be securely carried by the credential for offline decisions. The matrix permits embedded information including ticket type, seat assignment, event ID, venue access rights, timeslot, reservations, locker assignments, membership entitlements, guest category and validity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-172 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/embedded-entitlement-payload-designer-bo-172` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of the embedded entitlement payload and no payload size or optimisation estimate operation.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Designs what a credential carries for offline decisions - identity (credential ID, ticket type, guest category), access (venue, park, zone, attraction permissions), validity (date, time, timeslot, expiry) and entitlements (admission, Fast Pass, membership, reservation, locker, seat) - and shows a human-readable preview ("Venue: Aqua Park, Valid: 29 Aug 2026, Guest: Adult, Park entry 1, Fast Pass 3, Re-entry 1") with estimates of payload size, QR density, scan reliability and offline coverage. The one thing to get right: the trade-off is visible - every claim added makes the QR denser and harder to scan.

**Known correction pending (do not draw the wrong version)**

- **Write-only (no read of the current payload); content is only Save and Cancel** Why: The pack lists 18 claims in four groups, a preview and optimisation estimates; the designer needs the current payload and an estimate call. *(source: screens/P08-venue-back-office.yaml#BO-173 / contracts/spine/access.yaml#setEmbeddedEntitlementPayload; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation returns payload size, density, reliability or coverage** Why: The pack's payload optimisation panel has no source. *(source: screens/P08-venue-back-office.yaml#BO-173; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **profileId**: Picks the credential security profile (BO-165) this payload belongs to, by name and code; never typed. *(source: contracts/spine/access.yaml#setEmbeddedEntitlementPayload)*
- **embeddedClaims**: Four checkbox groups in the pack's headings Identity, Access, Validity, Entitlements; Credential ID locked on. No personal data such as name or photo is offered. *(source: screens/P08-venue-back-office.yaml#BO-172 / screens/P08-venue-back-office.yaml#BO-173 / contracts/spine/access.yaml#setEmbeddedEntitlementPayload)*
- **name**: Optional label, e.g. "Day ticket offline payload". *(source: contracts/spine/access.yaml#setEmbeddedEntitlementPayload)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Payload preview**: The claims as label-value lines for a sample ticket, never encoded data or secrets. *(source: screens/P08-venue-back-office.yaml#BO-173)*
- **Optimisation meters**: Payload size (bytes), QR density (version), Scan reliability (Good / Fair / Poor), Offline coverage (share of offline checks of BO-171 the payload supports); recalculated as claims change. *(source: screens/P08-venue-back-office.yaml#BO-173)*
- **AI recommendation**: Advisory notes such as the pack's "Locker assignment does not need to be embedded for this credential profile because all locker validation points are online", with Apply (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-173)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save payload**: Upsert for the profile (VO-R04); applies to credentials generated after the save. *(source: contracts/spine/access.yaml#setEmbeddedEntitlementPayload)*

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `setEmbeddedEntitlementPayload`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The embedded entitlement payload list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the embedded entitlement payload untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No embedded entitlement payload yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the embedded entitlement payload are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Payload too large for reliable scanning at the configured QR size**: Scan reliability Poor in red and Save asks for confirmation. *(source: screens/P08-venue-back-office.yaml#BO-173)*

#### Consistency with other screens

- Match `BO-165`: The "Entitlement payload" component of a dynamic QR profile is this design.
- Match `BO-171`: Offline coverage compares against the offline checks set there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
payload:
  profile: DQR-DEVICE-30
  claims: Credential ID, Ticket type, Guest category, Venue, Park, Zone, Date, Timeslot, Admission, Fast Pass
preview:
  venue: Aqua Park
  valid: 9 Oct 2026
  guest: Adult
  parkEntry: 1
  fastPass: 3
  reEntry: 1
meters:
  size: 182 bytes
  density: QR version 9
  reliability: Good
  coverage: 11 of 12 checks
```

#### Permissions

- `setEmbeddedEntitlementPayload` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-172` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-172`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 16: Works in Embedded Entitlement Payload Designer → Determine what operational information can be securely carried by the credential for offline decisions. The matrix permits embedded information including ticket type, seat assignment, event ID, venue …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-172?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-173` Credential Security Simulation, Audit & Publication

**Test the complete secure credential lifecycle before production deployment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block C · task VM-BO-173 |
| Who uses it | venue staff holding `AUDIT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-security-simulation-audit-publication-bo-173` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No operation runs a credential security simulation or publishes, versions or rolls back a credential security configuration.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Tests the whole credential security set-up before it goes live and keeps its audit trail: the administrator picks a scenario (valid credential, screenshot / stale QR, wrong device, outside geofence, no beacon, transferred, refunded, offline gate, expired QR, duplicate session), reads the result and security trace (the pack's Annual Pass AP-10452, QR age 72 s against a maximum of 60 s - DENIED, Dynamic QR expired), then takes the configuration through Draft > Security test > Validate > Approval > Publish with versions, scheduled activation, rollback and emergency disable. The one thing to get right: simulation results are never confused with real events in the audit list.

**Known correction pending (do not draw the wrong version)**

- **No operation runs a security simulation or publishes, versions or rolls back a credential security configuration** Why: The screen's purpose is test and publish; only two audit reads are bound. *(source: screens/P08-venue-back-office.yaml#BO-173 / contracts/spine/access.yaml#listCredentialSecurity; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table "Every credential security simulation" with no columns** Why: The read returns ten audit fields; title "Credential security audit" (VO-R12). *(source: contracts/spine/access.yaml#/components/schemas/CredentialSecuritySimulationAuditPublicationView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The audit row has no flag telling a simulated event from a real one** Why: BO-193's biometric audit carries isSimulation; credential security needs the same. *(source: contracts/spine/access.yaml#/components/schemas/BiometricSimulationAuditPublicationView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Virtual ticket | text field | — | — | `listCredentialSecurityOperational` ?virtualTicket |
| Action | text field | — | — | `listCredentialSecurityOperational` ?action |
| Actor | text field | — | — | `listCredentialSecurityOperational` ?actor |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scenario**: Cards for the ten pack scenarios; each pre-fills the test (device registered or not, location, QR age). *(source: screens/P08-venue-back-office.yaml#BO-173)*
- **Test values**: Credential (ticket number search), Device (Registered / Other), Location (gate picker), QR age in seconds. *(source: screens/P08-venue-back-office.yaml#BO-173)*
- **Audit filters**: Ticket (virtual ticket), action (Activation, Refresh, Validation, Transfer, Revocation), actor, date range. *(source: contracts/spine/access.yaml#listCredentialSecurityOperational / contracts/spine/access.yaml#/components/schemas/CredentialSecuritySimulationAuditPublicationView)*

#### Outputs: what the screen shows and produces

**Shown**

**Every credential security simulation** (data table, from `listCredentialSecurity`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Credential | text | Credential |
| Ticket | text | Ticket |
| Guest account reference | text | Guest/account reference |
| Device | text | Device |
| Gate | text | Gate |
| Location | text | Location |
| Timestamp | 1 Oct 2026, 14:30 | Timestamp |
| Operator | text | Operator |
| Event type | chip: Activation, Refresh, Validation, Transfer, Revocation | — |
| Result reason code | text | result/reason code |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The selected credential security simulation** (detail panel): The pack groups this record's detail under its own headings: “QR age”, “Every important event records”, “Center health”, “Board 3 workflow”, “There is a deliberate distinction”, “Media, Credential & Verification Methods”.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Result and security trace**: Result word in large type (Allowed / Denied with reason in words, VO-R06), then the trace lines with ticks and crosses - Signature valid, Device valid, Venue valid, Entitlement valid, QR freshness failed. *(source: screens/P08-venue-back-office.yaml#BO-173)*
- **Audit trail**: Columns Time, Event (Activation, Refresh, Validation, Transfer, Revocation), Credential, Ticket, Guest/account, Device, Gate, Location, Operator, Result/reason; simulated rows badged "Simulation"; cursor paging (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-173 / contracts/spine/access.yaml#/components/schemas/CredentialSecuritySimulationAuditPublicationView)*
- **Publication panel**: Stepper Draft > Security test > Validate > Approval > Publish, version list, scheduled activation, rollback, and a separate red Emergency disable. *(source: screens/P08-venue-back-office.yaml#BO-173)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Run security test**: Shows the result and trace without affecting any guest or gate. *(source: screens/P08-venue-back-office.yaml#BO-173)*
- **Emergency disable**: Typed confirmation naming the profiles and credential count affected and what replaces them (standard QR); reason required. *(source: screens/P08-venue-back-office.yaml#BO-173)*

**Data it reads**: `listCredentialSecurity` (onLoad, Credential Security Simulation, Audit & Publication); `listCredentialSecurityOperational` (onLoad, Credential Security, Audit & Operational Evidence)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential security simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential security simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential security simulation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential security simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Viewer has audit rights but not configuration rights**: Audit trail visible; tests, publish and emergency disable disabled with the missing permission named (VO-R08). *(source: contracts/spine/access.yaml#listCredentialSecurity)*

#### Consistency with other screens

- Match `BO-163`: Same trace layout (tick lines then final decision) as rule simulation.
- Match `BO-193`: Same pattern for biometric simulation and audit.
- Match `BO-226`: Audit rows for one ticket appear in the investigation console's history.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
test:
  credential: Annual pass AP-10452
  device: Registered
  location: Main Plaza Gate 1
  qrAge: 72 s
  maximum: 60 s
  result: Denied
  reason: Dynamic QR expired
audit:
- time: 1 Oct 2026 10:14:22
  event: Validation
  credential: VT0010
  guest: Sara Al Nuaimi
  gate: Main Plaza Gate 2
  result: Admitted
- time: 1 Oct 2026 10:15:03
  event: Validation
  credential: VT0010
  gate: North Entry
  result: Denied - Dynamic QR expired
```

#### Permissions

- `listCredentialSecurity` → `AUDIT_VIEW` (read) · staff
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-173` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-173`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 18: Works in Credential Security Simulation, Audit & Publication → Test the complete secure credential lifecycle before production deployment.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-173?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AUDIT_VIEW`.
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

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getBleBeaconGeofence": {"method":"GET","path":"/ble-beacon-geofence","contract":"access","summary":"The BLE beacon and geofence configuration as saved","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BleBeaconGeofenceConfigurationView"},
"listCredentialActivationDisplay": {"method":"GET","path":"/credential-activation-display","contract":"access","summary":"Credential Activation & Display Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialActivationDisplayRulesView"},
"listCredentialRevocationLifecycle": {"method":"GET","path":"/credential-revocation-lifecycle","contract":"access","summary":"Credential Revocation & Lifecycle Events","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialRevocationLifecycleEventsView"},
"listCredentialSecurity": {"method":"GET","path":"/credential-security","contract":"access","summary":"Credential Security Simulation, Audit & Publication","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialSecurityOperational": {"method":"GET","path":"/credential-security-operational","contract":"access","summary":"Credential Security, Audit & Operational Evidence","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"virtualTicket","in":"query","required":false},{"name":"action","in":"query","required":false},{"name":"actor","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialTransferRebinding": {"method":"GET","path":"/credential-transfer-rebinding","contract":"access","summary":"Credential Transfer & Rebinding","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialTransferRebindingView"},
"listDeviceBindingSession": {"method":"GET","path":"/device-binding-session","contract":"access","summary":"Device Binding & Session Security","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDigitalCredentialSecurity": {"method":"GET","path":"/digital-credential-security","contract":"access","summary":"Digital Credential Security Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOfflineCryptographicValidation": {"method":"GET","path":"/offline-cryptographic-validation","contract":"access","summary":"Offline Cryptographic Validation Profile","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OfflineCryptographicValidationProfileView"},
"releaseCredentialDevice": {"method":"POST","path":"/device-bindings/{bindingId}/release","contract":"access","summary":"Release a credential from a device","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessDeviceBinding"},
"setBleBeaconGeofence": {"method":"PUT","path":"/ble-beacon-geofence","contract":"access","summary":"BLE Beacon & Geofence Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BleBeaconGeofenceConfigurationInput","responds":"BleBeaconGeofenceConfigurationView"},
"setCredentialActivationDisplay": {"method":"PUT","path":"/credential-activation-display","contract":"access","summary":"Save a credential activation and display rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialActivationDisplayRulesInput","responds":"CredentialActivationDisplayRulesView"},
"setCredentialEventPropagationRule": {"method":"PUT","path":"/credential-event-propagation-rules","contract":"access","summary":"Set how a ticket lifecycle event propagates to the credential","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessCredentialEventPropagationRule","responds":"AccessCredentialEventPropagationRule"},
"setDeviceBindingPolicy": {"method":"PUT","path":"/device-binding-policy","contract":"access","summary":"Set the device binding policy of a venue","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceBindingPolicyInput","responds":"AccessCredentialPolicy"},
"setDynamicSecurityProfile": {"method":"PUT","path":"/dynamic-security-profile","contract":"access","summary":"Dynamic QR Security Profile Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DynamicQrSecurityProfileBuilderInput","responds":"DynamicQrSecurityProfileBuilderView"},
"setEmbeddedEntitlementPayload": {"method":"PUT","path":"/embedded-entitlement-payload","contract":"access","summary":"Embedded Entitlement Payload Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EmbeddedEntitlementPayloadDesignerInput","responds":"EmbeddedEntitlementPayloadDesignerView"},
"setGateOfflinePolicy": {"method":"PUT","path":"/offline-policies","contract":"access","summary":"Set the offline policy of a venue","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessOfflinePolicy","responds":"AccessOfflinePolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCredentialEventPropagationRule": {"type":"object","x-ticvai-persistence":"access.credential_event_propagation_rule","description":"For one ticket lifecycle event, the revocation action on the credential and how the change propagates to every bound medium, with the conditions monitored (declared 29 September, data-model close-out DM1).","required":["id","triggerEvent","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"triggerEvent":{"type":"string","enum":["entry","exit","redemption","partialConsumption","cancellation","refund","suspension","reactivation","transfer","exchange","upgrade","reissue","expiry","replacement","manualInvalidation","fraudLock","accountSuspension"],"description":"Unique per scope; one vocabulary for both screens that read it (decided 29 September, writers pass)"},"revocationAction":{"type":"string","nullable":true,"enum":["invalidate","suspend","replace"],"description":"What happens to the credential; refund, exchange and reissue always revoke"},"propagationTargets":{"type":"array","items":{"type":"string","enum":["centralPlatform","mobileApp","gateNetwork","offlineRevocationPackage","walletCredentialService"]}},"monitoredConditions":{"type":"array","items":{"type":"string","enum":["delayedUpdates","conflictingStates","offlineTransactionsPendingSynchronization","providerUpdateFailures","staleWalletCredentials"]}},"propagation":{"type":"string","maxLength":500,"nullable":true,"description":"How the Virtual Ticket state change reaches every bound medium"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessCredentialPolicy": {"type":"object","x-ticvai-persistence":"access.credential_policy","description":"One credential policy of one kind for a venue - activation and display rule, transfer policy, Virtual Ticket identity configuration or device binding policy; merges the proposed credential_display_rule, transfer_policy and virtual_ticket_config (declared 29 September, data-model close-out DM1). The deviceBinding row is written by setDeviceBindingPolicy (decided 29 September, writers pass).","required":["id","kind","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The ruleId (display rule) or policyId (transfer policy) of the operations"},"kind":{"type":"string","enum":["activationDisplay","transfer","virtualTicketIdentity","deviceBinding"],"description":"Which policy this row is; the columns of the other kinds stay null"},"name":{"type":"string","maxLength":200,"nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Required for activationDisplay and virtualTicketIdentity (one virtualTicketIdentity row per venue)"},"beforeActivationDisplay":{"type":"array","items":{"type":"string","enum":["hideQr","blurQr","showCountdown","showAvailableAtVenue","showVenueDirections"]},"description":"activationDisplay - what the guest sees before the credential activates"},"activeDisplay":{"type":"array","items":{"type":"string","enum":["dynamicQr","activationTimer","credentialStatus","remainingEntitlements"]},"description":"activationDisplay - what the guest sees once it is active"},"activationTriggers":{"type":"array","items":{"type":"string"},"description":"activationDisplay - what activates the credential, e.g. beacon proximity, geofence entry, time before admission"},"transferAllowed":{"type":"boolean","nullable":true,"description":"transfer"},"numberOfTransfers":{"type":"integer","minimum":0,"nullable":true,"description":"transfer"},"beforeFirstValidationOnly":{"type":"boolean","nullable":true,"description":"transfer"},"requireRecipientAccount":{"type":"boolean","nullable":true,"description":"transfer"},"requireOtp":{"type":"boolean","nullable":true,"description":"transfer"},"requireAcceptance":{"type":"boolean","nullable":true,"description":"transfer"},"returnToSender":{"type":"boolean","nullable":true,"description":"transfer"},"transferDeadlineHours":{"type":"integer","minimum":0,"nullable":true,"description":"transfer - hours before the visit after which transfer closes"},"cancelPendingAllowed":{"type":"boolean","nullable":true,"description":"transfer"},"transferAuditRequired":{"type":"boolean","nullable":true,"description":"transfer"},"idGenerationPattern":{"type":"string","nullable":true,"description":"virtualTicketIdentity - Virtual Ticket ID format: prefix, suffix and length"},"ticketClassification":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"ticketOwnershipModel":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"holderAssignmentRequirements":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"transferabilityReference":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"validityModel":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"consumptionModel":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"entitlementModel":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"mediaRequirements":{"type":"array","items":{"type":"string"},"description":"virtualTicketIdentity - media types a ticket of this configuration must carry"},"maximumActiveDevices":{"type":"integer","minimum":1,"nullable":true,"description":"deviceBinding"},"concurrentSessions":{"type":"integer","minimum":1,"nullable":true,"description":"deviceBinding"},"deviceChangePolicy":{"type":"string","nullable":true,"enum":["notAllowed","allowedBeforeFirstUse","otpVerificationRequired","operatorApprovalRequired","supervisorApprovalRequired"],"description":"deviceBinding"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessDeviceBinding": {"type":"object","x-ticvai-persistence":"access.device_binding","description":"One guest device bound to a credential, with its registration, last activation and security status; the binding policy in force is a deviceBinding row of access.credential_policy (declared 29 September, data-model close-out DM1). Written by bindCredentialDevice (the guest app) and releaseCredentialDevice; securityStatus is set by the sharing detection job (decided 29 September, writers pass).","required":["id","entitlementId","deviceId","registeredAt","securityStatus","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest (pii.subject)"},"entitlementId":{"type":"string","format":"uuid"},"credentialBindingId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","maxLength":200},"deviceReference":{"type":"string","maxLength":200,"nullable":true},"appInstallationId":{"type":"string","maxLength":200,"nullable":true},"os":{"type":"string","maxLength":50,"nullable":true},"registeredAt":{"type":"string","format":"date-time"},"lastActivatedAt":{"type":"string","format":"date-time","nullable":true},"lastKnownVenueId":{"type":"string","format":"uuid","nullable":true},"securityStatus":{"type":"string","enum":["normal","suspicious","blocked"],"default":"normal"},"deactivatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Set when the binding is removed (deactivation, or a transfer of the credential)"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessOfflinePolicy": {"type":"object","x-ticvai-persistence":"access.offline_policy","description":"The offline policy of one venue: what gates validate locally and for how long, how old the revocation cache may get, and how devices step down through degraded modes. Merges access.offline_validation_profile, access.revocation_cache_policy and access.degraded_mode_policy (declared 29 September, data-model close-out DM1)","required":["id","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"maxOfflineDurationHours":{"type":"integer","minimum":0,"nullable":true,"description":"**Hours a reader may validate offline; past it, readers refuse offline taps** (decided 2 October 2026, Chinmay, critical set 1, BO-471: \"Yes: the venue sets a maximum offline duration; readers then refuse offline taps\"; DEC-426; CHG-CSP-035). Counted from the reader's last successful sync. Past the limit an access gate, a handheld and a games reader refuse every tap they would have validated from their local package (`ValidationResult.denyCause` `offlineLimitExceeded`) until they reconnect; `afterThresholdBehavior` decides only what the operator is shown and whether a supervisor may admit by hand (`supervisorMode`), and none of its values lets a reader keep validating unattended. The limit travels in the offline package (ADR-0068), so a reader that has lost the platform still knows it. Null sets no limit beyond the package's own expiry."},"offlineChecks":{"type":"array","items":{"type":"string","enum":["credentialAuthenticity","digitalSignature","ticketId","venue","park","zone","visitDate","timeWindow","credentialStatusSnapshot","ticketType","guestCategory","seat","timeslot","reservation","entitlements","reEntryPermissions","validityPeriod"]},"description":"What a gate may validate locally"},"afterThresholdBehavior":{"type":"string","enum":["continueRestrictedValidation","operatorWarning","supervisorMode","failClosed","fallback"],"nullable":true},"revocationTriggerEvents":{"type":"array","items":{"type":"string","enum":["fraudLock","refund","cancellation","lostCredential","transfer","reissue","manualInvalidation"]},"description":"Events that push an invalidation into the offline cache"},"revocationMaxAllowedAgeMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"Maximum allowed revocation cache age"},"revocationStalenessAction":{"type":"string","enum":["continue","continueWithWarning","restrictedProductsOnly","supervisorMode","denySelectedCredentialClasses","failClosed"],"nullable":true,"description":"What devices do when the cache is older than the maximum allowed age"},"operatingModes":{"type":"array","items":{"type":"string","enum":["online","degraded","edgeMode","localOffline","unsafeExpired"]},"description":"Operating modes a device moves through as connectivity fails"},"centralUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without central services before switching to edge mode"},"edgeUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without the venue edge before switching to local offline"},"automaticSwitch":{"type":"boolean","default":true,"description":"Switch modes automatically without stopping guest flow"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BleBeaconGeofenceConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What BLE Beacon & Geofence Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"beaconName":{"type":"string","description":"Beacon Name"},"beaconId":{"type":"string","description":"Beacon ID"},"venue":{"type":"string","description":"Venue"},"zone":{"type":"string","description":"Zone"},"gate":{"type":"string","description":"Gate"},"proximityThreshold":{"type":"integer","description":"Metres"},"activeInactive":{"type":"string","enum":["active","inactive"],"description":"Active/Inactive"},"health":{"type":"string","enum":["healthy","degraded","offline"],"description":"Read-only, reported by the beacon"},"lastDetected":{"type":"string","format":"date-time","description":"Last detected"},"park":{"type":"string","description":"Park"},"attraction":{"type":"string","description":"Attraction"},"geofenceRadiusMeters":{"type":"integer","description":"Radius of a circular activation zone"},"geofenceBoundary":{"type":"array","items":{"type":"string"},"description":"Polygon points as lat,lng when the zone is drawn"}},"required":["beaconId","venue"]},
"BleBeaconGeofenceConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What BLE Beacon & Geofence Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"beaconName":{"type":"string","description":"Beacon Name"},"beaconId":{"type":"string","description":"Beacon ID"},"venue":{"type":"string","description":"Venue"},"zone":{"type":"string","description":"Zone"},"gate":{"type":"string","description":"Gate"},"proximityThreshold":{"type":"integer","description":"Metres"},"activeInactive":{"type":"string","enum":["active","inactive"],"description":"Active/Inactive"},"health":{"type":"string","enum":["healthy","degraded","offline"],"description":"Read-only, reported by the beacon"},"lastDetected":{"type":"string","format":"date-time","description":"Last detected"},"park":{"type":"string","description":"Park"},"attraction":{"type":"string","description":"Attraction"},"geofenceRadiusMeters":{"type":"integer","description":"Radius of a circular activation zone"},"geofenceBoundary":{"type":"array","items":{"type":"string"},"description":"Polygon points as lat,lng when the zone is drawn"}},"required":["beaconId","venue"]},
"CredentialActivationDisplayRulesInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Credential Activation & Display Rules submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["venueId","name","beforeActivationDisplay","activeDisplay","activationTriggers"],"properties":{"ruleId":{"type":"string","format":"uuid","description":"Absent creates a rule"},"venueId":{"type":"string","description":"Venue the rule applies to"},"name":{"type":"string","maxLength":200},"beforeActivationDisplay":{"type":"array","items":{"type":"string","enum":["hideQr","blurQr","showCountdown","showAvailableAtVenue","showVenueDirections"]},"description":"What the guest sees before the credential activates"},"activeDisplay":{"type":"array","items":{"type":"string","enum":["dynamicQr","activationTimer","credentialStatus","remainingEntitlements"]},"description":"What the guest sees once it is active"},"activationTriggers":{"type":"array","items":{"type":"string"},"minItems":1,"description":"What activates the credential, e.g. beacon proximity, geofence entry, time before admission"}}},
"CredentialActivationDisplayRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Activation & Display Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"beforeActivationDisplay":{"type":"array","items":{"type":"string","enum":["hideQr","blurQr","showCountdown","showAvailableAtVenue","showVenueDirections"]}},"activeDisplay":{"type":"array","items":{"type":"string","enum":["dynamicQr","activationTimer","credentialStatus","remainingEntitlements"]}},"name":{"type":"string"},"activationTriggers":{"type":"array","items":{"type":"string"},"description":"Conditions that make the credential eligible, e.g. beaconProximity, geofence, timeWindow"}},"required":["ruleId"]},
"CredentialRevocationLifecycleEventsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Revocation & Lifecycle Events displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"revocationAction":{"type":"string","enum":["invalidate","suspend","replace"],"description":"What happens to the credential on the event"},"triggerEvent":{"type":"string","enum":["refund","cancellation","transfer","exchange","upgrade","reissue","expiry","manualInvalidation","fraudLock","accountSuspension"],"description":"Ticket event, in the access.credential_event_propagation_rule vocabulary (ticketExpiration is expiry) (decided 29 September, writers pass)"},"propagationTargets":{"type":"array","items":{"type":"string","enum":["centralPlatform","mobileApp","gateNetwork","offlineRevocationPackage","walletCredentialService"]}}},"required":["triggerEvent","revocationAction"]},
"CredentialSecurityAuditOperationalEvidenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Security, Audit & Operational Evidence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicket":{"type":"string","description":"Virtual Ticket"},"credential":{"type":"string","description":"Credential"},"media":{"type":"string","description":"Media"},"action":{"type":"string","enum":["credentialRequested","generated","bound","delivered","activated","updated","presented","suspended","reactivated","replaced","revoked","expired","rebound","regenerated","deleted"],"description":"Lifecycle action recorded"},"before":{"type":"string","description":"Before"},"after":{"type":"string","description":"After"},"actor":{"type":"string","description":"Actor"},"source":{"type":"string","description":"Source"},"device":{"type":"string","description":"Device"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"reason":{"type":"string","description":"Reason"},"approval":{"type":"string","description":"Approval"},"providerReference":{"type":"string","description":"Provider reference"},"relatedTransaction":{"type":"string","description":"Related transaction"},"anomalyFlags":{"type":"array","items":{"type":"string","enum":["excessiveRegeneration","repeatedReplacement","suspiciousRebinding","multipleCredentialAssignments","unexpectedProviderTokenChanges","unauthorizedAdministrativeActions"]},"description":"Suspicious patterns flagged on this entry"}}},
"CredentialSecuritySimulationAuditPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Security Simulation, Audit & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credential":{"type":"string","description":"Credential"},"ticket":{"type":"string","description":"Ticket"},"guestAccountReference":{"type":"string","description":"Guest/account reference"},"device":{"type":"string","description":"Device"},"gate":{"type":"string","description":"Gate"},"location":{"type":"string","description":"Location"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"operator":{"type":"string","description":"Operator"},"eventType":{"type":"string","enum":["activation","refresh","validation","transfer","revocation"]},"resultReasonCode":{"type":"string","description":"result/reason code"}}},
"CredentialTransferRebindingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Transfer & Rebinding displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"transferAllowed":{"type":"boolean"},"policyId":{"type":"string"},"numberOfTransfers":{"type":"integer","description":"Number of transfers"},"beforeFirstValidationOnly":{"type":"boolean","description":"Before first validation only"},"requireRecipientAccount":{"type":"boolean","description":"Require recipient account"},"requireOtp":{"type":"boolean","description":"Require OTP"},"requireAcceptance":{"type":"boolean","description":"Require acceptance"},"returnToSender":{"type":"boolean","description":"Return to sender"},"name":{"type":"string"},"transferDeadlineHours":{"type":"integer","description":"Hours before the visit after which transfer closes"},"cancelPendingAllowed":{"type":"boolean"},"transferAuditRequired":{"type":"boolean"}},"required":["policyId","transferAllowed"]},
"DeviceBindingPolicyInput": {"type":"object","x-ticvai-persistence":"none — request only; written as the deviceBinding row of access.credential_policy (declared 29 September, writers pass)","required":["venueId"],"properties":{"venueId":{"type":"string","format":"uuid"},"maximumActiveDevices":{"type":"integer","minimum":1,"default":1,"description":"Devices the credential may be active on at once"},"concurrentSessions":{"type":"integer","minimum":1,"default":1},"deviceChangePolicy":{"type":"string","enum":["notAllowed","allowedBeforeFirstUse","otpVerificationRequired","operatorApprovalRequired","supervisorApprovalRequired"],"default":"otpVerificationRequired"}}},
"DeviceBindingSessionSecurityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Device Binding & Session Security displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"user":{"type":"string","description":"User"},"credential":{"type":"string","description":"Credential"},"deviceId":{"type":"string","description":"Device ID"},"deviceReference":{"type":"string","description":"Device reference"},"appInstallation":{"type":"string","description":"App installation"},"os":{"type":"string","description":"OS"},"registrationDate":{"type":"string","format":"date-time","description":"Registration date"},"lastActivation":{"type":"string","format":"date-time","description":"Last activation"},"lastKnownVenue":{"type":"string","description":"Last known venue"},"securityStatus":{"type":"string","enum":["normal","suspicious","blocked"],"description":"Security status"}}},
"DeviceBindingSessionSecurityViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"maximumActiveDevices":{"type":"integer","description":"Maximum Active Devices (the pack shows 1)"},"concurrentSessions":{"type":"integer","description":"Concurrent Sessions (the pack shows 1)"},"deviceChangePolicy":{"type":"string","enum":["notAllowed","allowedBeforeFirstUse","otpVerificationRequired","operatorApprovalRequired","supervisorApprovalRequired"]}}},
"DigitalCredentialSecurityCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Digital Credential Security Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialType":{"type":"string","enum":["dynamicQrTicket","membership","annualPass","mobileWallet","loyalty","digitalPass","event"]},"profileId":{"type":"string"},"profileName":{"type":"string","description":"Credential profile, e.g. Day Ticket"},"dynamic":{"type":"boolean"},"deviceBound":{"type":"string","enum":["required","optional","off"]},"locationScope":{"type":"string","description":"gate, venue, event or none"},"offlineReady":{"type":"boolean"},"securityLevel":{"type":"string","enum":["strong","standard"]}}},
"DigitalCredentialSecurityCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeDigitalCredentials":{"type":"integer","description":"Active Digital Credentials"},"dynamicQrEnabled":{"type":"integer","description":"Credentials with dynamic QR enabled"},"deviceBoundCredentials":{"type":"integer","description":"Device-Bound Credentials"},"locationProtectedCredentials":{"type":"integer","description":"Location-Protected Credentials"},"offlineReadyCredentials":{"type":"integer","description":"Offline-Ready Credentials"},"credentialsRevokedToday":{"type":"integer","description":"Credentials Revoked Today"},"transferEvents":{"type":"integer"},"securityAlerts":{"type":"integer","description":"Security Alerts"},"suspiciousSessions":{"type":"integer","description":"Suspicious Sessions"}}},
"DynamicQrSecurityProfileBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is access.scan_event at 7%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Dynamic QR Security Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"name":{"type":"string"},"profileId":{"type":"string","maxLength":64,"description":"The credential security profile's code (access.credential_security_profile.code) (decided 29 September, writers pass)"},"qrMode":{"type":"string","enum":["static","dynamic","dynamicDeviceBound","dynamicLocationBound","dynamicDeviceLocationBound"]},"payloadComponents":{"type":"array","items":{"type":"string","enum":["credentialId","ticketId","timestamp","nonceOtp","deviceBindingReference","venueContext","entitlementPayload","signatureKeyReference"]},"description":"What the QR payload carries"},"venueId":{"type":"string"},"refreshIntervalSeconds":{"type":"integer","default":30,"minimum":5,"description":"**QR rotation interval: 30 seconds by default; the screen offers 15, 30, 45 and 60 and a custom value no shorter than 5 seconds** (decided 2 October 2026, Chinmay, batch 1, GST-055: \"30 seconds\", and covered-by-earlier set, BO-165; DEC-136, DEC-233; CHG-CSP-024; DI-1083, DI-632, DI-630). The venue's setting; the guest app's countdown (GST-055) shows the same value. The 6 to 12 seconds the client mentioned for beacon-activated codes is reachable as a custom value."}},"required":["profileId","name","qrMode"]},
"DynamicQrSecurityProfileBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Dynamic QR Security Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string"},"profileId":{"type":"string"},"qrMode":{"type":"string","enum":["static","dynamic","dynamicDeviceBound","dynamicLocationBound","dynamicDeviceLocationBound"]},"payloadComponents":{"type":"array","items":{"type":"string","enum":["credentialId","ticketId","timestamp","nonceOtp","deviceBindingReference","venueContext","entitlementPayload","signatureKeyReference"]},"description":"What the QR payload carries"},"venueId":{"type":"string"},"refreshIntervalSeconds":{"type":"integer","default":30,"minimum":5,"description":"**QR rotation interval: 30 seconds by default; the screen offers 15, 30, 45 and 60 and a custom value no shorter than 5 seconds** (decided 2 October 2026, Chinmay, batch 1, GST-055: \"30 seconds\", and covered-by-earlier set, BO-165; DEC-136, DEC-233; CHG-CSP-024; DI-1083, DI-632, DI-630). The venue's setting; the guest app's countdown (GST-055) shows the same value. The 6 to 12 seconds the client mentioned for beacon-activated codes is reachable as a custom value."}},"required":["profileId","name","qrMode"]},
"EmbeddedEntitlementPayloadDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Embedded Entitlement Payload Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"profileId":{"type":"string","description":"The credential security profile's code (access.credential_security_profile.code) (decided 29 September, writers pass)","maxLength":64},"embeddedClaims":{"type":"array","items":{"type":"string","enum":["credentialId","ticketType","guestCategory","venue","park","zone","attractionPermissions","date","time","timeslot","expiry","admission","fastPass","membership","reservation","locker","seat","otherOperationalClaims"]},"description":"Claims carried in the credential for offline decisions"},"name":{"type":"string"}},"required":["profileId","embeddedClaims"]},
"EmbeddedEntitlementPayloadDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Embedded Entitlement Payload Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"profileId":{"type":"string","description":"Credential security profile the payload belongs to"},"embeddedClaims":{"type":"array","items":{"type":"string","enum":["credentialId","ticketType","guestCategory","venue","park","zone","attractionPermissions","date","time","timeslot","expiry","admission","fastPass","membership","reservation","locker","seat","otherOperationalClaims"]},"description":"Claims carried in the credential for offline decisions"},"name":{"type":"string"}},"required":["profileId","embeddedClaims"]},
"OfflineCryptographicValidationProfileView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline Cryptographic Validation Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maxOfflineDurationHours":{"type":"integer","description":"e.g. 8"},"offlineChecks":{"type":"array","items":{"type":"string","enum":["credentialAuthenticity","digitalSignature","ticketId","venue","park","zone","visitDate","timeWindow","credentialStatusSnapshot","ticketType","guestCategory","seat","timeslot","reservation","entitlements","reEntryPermissions","validityPeriod"]},"description":"What a gate may validate locally"},"afterThresholdBehavior":{"type":"string","enum":["continueRestrictedValidation","operatorWarning","supervisorMode","failClosed","fallback"]}},"required":["offlineChecks","maxOfflineDurationHours","afterThresholdBehavior"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
