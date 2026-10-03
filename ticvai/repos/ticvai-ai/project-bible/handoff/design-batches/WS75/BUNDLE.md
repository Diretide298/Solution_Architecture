# WS75 — Digital Asset Management DAM board 2

**10 screens · 11 operations · 12 schemas · 2 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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
  `ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW`. A control nobody can use must say so,
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

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `CMS-071` | AI Asset Intelligence Command Center | B | 0 | 171 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `CMS-072` | AI Auto-Tagging & Content Understanding | B | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-073` | Semantic & Natural-Language Asset Search | B | 0 | 14 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `CMS-074` | Visual Similarity & Related Asset Discovery | B | 2 | 11 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-075` | Duplicate & Near-Duplicate Management | B | 19 | 0 | 6 | 0 | 1 | 2 | — | notStarted (—) |
| `CMS-076` | Asset Version Control & Revision History | B | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-077` | Version Comparison & Replacement Impact | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-078` | Transformation & Rendition Management | B | 1 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-079` | Rendition Processing & Delivery Readiness | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-080` | AI Quality, Intelligence Review & Recommendations | B | 0 | 18 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**CMS-073, CMS-076, CMS-077 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-071` AI Asset Intelligence Command Center

**Provide DAM administrators and content teams with an overview of AI processing, version activity, duplicate detection, rendition generation, and asset-quality issues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-071 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/ai-asset-intelligence-command-center-cms-071` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Review AI Results, Duplicate Review, Version Activity, Rendition Queue, Processing Failures. Each needs an … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): The screen is about media files in the DAM (assets.yaml); maintenance listAssets returns rides, turnstiles and pumps from the physical asset register …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Digital Asset Management board's AI command centre - media files (images, videos, documents), not physical assets: how many files AI has processed, what is pending, tags generated, duplicate candidates, version updates, renditions, processing failures and items needing review, with processing health and AI confidence distribution. It belongs to the media library (P13), not to maintenance and safety; it is in this chunk only because of the word "asset". The one thing to get right: draw it as the DAM command centre (KPI tiles, health and confidence charts, intelligence alerts, tiles into CMS-072 to CMS-080), and drop the maintenance binding.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No operation returns AI processing counts, confidence bands or duplicate candidate counts (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): Classified under process-module Maintenance & Safety and bound to maintenance listAssets (CHG-WIR-001); KPIs drawn as seventeen columns of one data table with a detail panel (CHG-SGU-023).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which process owner takes CMS-071 (DAM / media library) now that it leaves venue operations?** → Drawn default accepted: Leave the screen's design to the DAM chunk; keep only this note here. *(decided by Chinmay, 2026-10-02; DEC-520 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getMediaUsageAnalytics` ?from |
| To | date and time picker | — | — | `getMediaUsageAnalytics` ?to |
| Group by | radio group | — | Asset type · Category · Venue · Owner · Channel | `getMediaUsageAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**AI-Processed Assets** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Pending AI Processing** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**AI Tags Generated** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Duplicate Candidates** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Version Updates** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Renditions Generated** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Processing Failures** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Assets Requiring Review** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Processed** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Queued** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Processing** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Review Required** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Failed** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**95–100%** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**80–94%** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**60–79%** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Below Threshold** (metric tile, from `getMediaUsageAnalytics`)

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**AI processing over time** (chart, from `getMediaUsageAnalytics`): Per VO-R02: processing volume by day.

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Confidence bands** (chart, from `getMediaUsageAnalytics`): Per VO-R02: high, medium and low confidence counts; drawn pending the fields (CHG-SGU-024).

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Label | text | — |
| Asset count | 1,234 | — |
| Storage bytes | 1,234 | — |
| Downloads | 1,234 | — |
| Views | 1,234 | — |
| Shares | 1,234 | — |
| Never used count | 1,234 | — |
| Unclassified count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Review AI Results (primary button) | navigation or local | — | — | — | — |
| Duplicate Review (secondary button) | navigation or local | — | — | — | — |
| Version Activity (secondary button) | navigation or local | — | — | — | — |
| Rendition Queue (secondary button) | navigation or local | — | — | — | — |
| Processing Failures (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: AI-processed assets, Pending AI processing, AI tags generated, Duplicate candidates, Version updates, Renditions generated, Processing failures (red when above 0), Assets requiring review. *(source: screens/P13-white-label-cms.yaml#CMS-071)*
- **Processing health**: A stacked bar Processed / Queued / Processing / Review required / Failed. *(source: screens/P13-white-label-cms.yaml#CMS-071)*
- **AI confidence distribution**: Four bands 95-100%, 80-94%, 60-79%, below threshold, as a bar chart; the threshold is the tenant's configured value. *(source: screens/P13-white-label-cms.yaml#CMS-071)*
- **Intelligence alerts**: "126 potential duplicates detected", "48 assets below the confidence threshold", "18 video jobs failed", "342 renditions generated today" - each opening its board screen. *(source: screens/P13-white-label-cms.yaml#CMS-071)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Review AI results / Duplicate review / Version activity / Rendition queue / Processing failures**: Tiles opening CMS-072/CMS-080, CMS-075, CMS-076, CMS-078 and CMS-079; each returns here. *(source: screens/P13-white-label-cms.yaml#CMS-071 / F184 step 1)*

**Data it reads**: `getMediaUsageAnalytics` (onLoad, What the library looks like to AI)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Back to Tenant Workspace*
- → `CMS-072` AI Auto-Tagging & Content Understanding: *AI Auto-Tagging & Content Understanding*
- → `CMS-073` Semantic & Natural-Language Asset Search: *Semantic & Natural-Language Asset Search*
- → `CMS-074` Visual Similarity & Related Asset Discovery: *Visual Similarity & Related Asset Discovery*
- → `CMS-075` Duplicate & Near-Duplicate Management: *Duplicate & Near-Duplicate Management*
- → `CMS-076` Asset Version Control & Revision History: *Asset Version Control & Revision History*
- → `CMS-077` Version Comparison & Replacement Impact: *Version Comparison & Replacement Impact*
- → `CMS-078` Transformation & Rendition Management: *Transformation & Rendition Management*
- → `CMS-079` Rendition Processing & Delivery Readiness: *Rendition Processing & Delivery Readiness*
- → `CMS-080` AI Quality, Intelligence Review & Recommendations: *AI Quality, Intelligence Review & Recommendations*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset intelligence yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Tenant without AI enabled**: AI tiles show "AI processing not enabled for this tenant"; version and rendition tiles still show. *(source: designer default)*

#### Consistency with other screens

- Match `CMS-001`: Reached from and returns to the Tenant Workspace of the media library.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  aiProcessed: 46,284
  pending: 842
  tags: 184,620
  duplicateCandidates: 126
  versionUpdates: 428
  renditions: 128,420
  failed: 18
  reviewRequired: 214
```

#### Permissions

- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-071` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-071`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 1: Opens AI Asset Intelligence Command Center → Provide DAM administrators and content teams with an overview of AI processing, version activity, duplicate detection, rendition generation, and asset-quality issues.
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F184 branch at step 1 (expected): when Nothing has been set up on AI Asset Intelligence Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F184 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (171 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-071?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Review AI Results, Duplicate Review, Version Activity, Rendition Queue, Processing Failures.
- [ ] Every transition is wired: `CMS-001`, `CMS-072`, `CMS-073`, `CMS-074`, `CMS-075`, `CMS-076`, `CMS-077`, `CMS-078`, `CMS-079`, `CMS-080`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-072` AI Auto-Tagging & Content Understanding

**Automatically analyze uploaded assets and generate useful descriptive metadata.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-072 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/ai-auto-tagging-content-understanding-cms-072` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Accept, Reject, Edit, Accept All Above Threshold. Each needs an operation, or needs removing from the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI-generated tags and descriptions for uploaded assets, accepted or rejected by a person; accept-all only above a confidence threshold.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept (primary button) | navigation or local | — | — | — | — |
| Reject (destructive button) | navigation or local | — | — | — | — |
| Edit (secondary button) | navigation or local | — | — | — | — |
| Accept All Above Threshold (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

**What opens over it**

- confirmDialog *Reject*: **Reject on a auto-tagging content understanding is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The auto-tagging content understanding list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the auto-tagging content understanding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No auto-tagging content understanding yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the auto-tagging content understanding are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A tag names a closed vocabulary (`MediaTaxonomy.keywordVocabularies[].closed`) and its value is not one of that vocabulary's terms. |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asset: lazy-river-sunset.jpg
suggestedTags:
- water
- family
- sunset
confidence:
- 96%
- 88%
- 71%
```

#### Permissions

- `analyseMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `setMediaAssetTags` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.7 | AI shall automatically generate tags, keywords, and classifications for uploaded assets. | Digital Asset Management | CONTRACTED | `analyseMediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI auto-tagging proposes tags with a confidence score shown per tag (e.g. "family" 96%, "children" 94%, "waterpark" 90%). *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-848)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-072` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-072`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 2: Works in AI Auto-Tagging & Content Understanding → Automatically analyze uploaded assets and generate useful descriptive metadata.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-072?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept, Reject, Edit, Accept All Above Threshold.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-073` Semantic & Natural-Language Asset Search

**Allow users to search based on meaning rather than exact filenames or tags. Board 1 provided structured search.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-073 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each result should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/semantic-natural-language-asset-search-cms-073` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Search by meaning ("family on the lazy river at sunset"), with relevance and the reason it matched.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 7 labels bound). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Image · Video · Audio · Document · Vector · Font · Archive | `searchMedia` ?kind |
| Tag | text field | — | — | `searchMedia` ?tag |
| Collection | picker: choose a collection | — | — | `searchMedia` ?collectionId |
| Search | text field | — | — | `searchMedia` ?search |
| Unused only | toggle | off | — | `searchMedia` ?unusedOnly |
| Rights expiring within days | number field (days) | — | — | `searchMedia` ?rightsExpiringWithinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every semantic natural-language asset** (data table)

| Shows | Format | Notes |
|---|---|---|
| Thumbnail | text | not in the schema: `Thumbnail` |
| Asset | text | not in the schema: `asset` |
| Relevance score | text | not in the schema: `relevance score` |
| AI tags | text | not in the schema: `AI tags` |
| Matching reason | text | not in the schema: `matching reason` |
| Format | text | not in the schema: `format` |
| Dimensions | text | not in the schema: `dimensions` |

**The selected semantic natural-language asset** (detail panel): The pack groups this record's detail under its own headings: “Digital Asset Management”, “Security”.

| Shows | Format | Notes |
|---|---|---|
| Thumbnail | text | not in the schema: `Thumbnail` |
| Asset | text | not in the schema: `asset` |
| Relevance score | text | not in the schema: `relevance score` |
| AI tags | text | not in the schema: `AI tags` |
| Matching reason | text | not in the schema: `matching reason` |
| Format | text | not in the schema: `format` |
| Dimensions | text | not in the schema: `dimensions` |

**Data it reads**: `searchMedia` (onLoad, Semantic search)

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The semantic natural-language asset list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the semantic natural-language asset untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Semantic & Natural-Language Asset Search. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the semantic natural-language asset are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every semantic natural-language asset:
- Thumbnail: 46
  relevance score: 92%
  AI tags: 11
  matching reason: 11
- Thumbnail: 312
  relevance score: 78%
  AI tags: 128
  matching reason: 128
- Thumbnail: 74
  relevance score: 64%
  AI tags: 46
  matching reason: 46
```

#### Permissions

- `searchMedia` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.9 | Campaign Asset Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 22.10.25 | Media Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 23.1.1 | System shall provide a centralized repository for storing and managing digital assets including images, videos, documents, PDFs, marketing materials, brand assets, audio files, templates, and … | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.5 | System shall support searching assets using keywords, metadata, tags, categories, and filters. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.15 | System shall expose DAM functionality through APIs and support integration with CMS, CRM, marketing platforms, mobile applications, and third-party systems. | Digital Asset Management | CONTRACTED | `searchMedia` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Semantic/natural-language search finds images by visual content (e.g. "children playing in the pool"), not only filename or tags. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-847)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-073` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-073`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 4: Works in Semantic & Natural-Language Asset Search → Allow users to search based on meaning rather than exact filenames or tags. Board 1 provided structured search.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-073?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-074` Visual Similarity & Related Asset Discovery

**Allow users to find visually related or similar media.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-074 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/visual-similarity-related-asset-discovery-cms-074` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Assets visually similar to the selected one.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Source asset | search field | — | — | — | — | Sends `?assetId=` (required). | `findSimilarMediaAssets` |
| Minimum similarity | number field | — | — | — | — | Sends `?minSimilarity=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Asset | upload, or pick from the media library | — | — | `findSimilarMediaAssets` ?assetId |
| Min similarity | number field | 0.8 | — | `findSimilarMediaAssets` ?minSimilarity |

#### Outputs: what the screen shows and produces

**Shown**

**Similar assets** (data table, from `findSimilarMediaAssets`): `relation` keeps similar, duplicate candidate and variant apart, as the pack requires; the pack's Version and Rendition are not among its values.

| Shows | Format | Notes |
|---|---|---|
| Asset | the image or video | — |
| Similarity | 1,234.5 | — |
| Relation | chip: Exact duplicate, Near duplicate, Variant, Related | — |
| Differing fields | list or chips (count when long) | — |
| Thumbnail | text | not in the schema: `Thumbnail` |

**The selected match** (detail panel, from `findSimilarMediaAssets`): The pack's Explain Match ("94% - Family, Water Attraction, Outdoor, Daytime").

| Shows | Format | Notes |
|---|---|---|
| Asset | the image or video | — |
| Similarity | 1,234.5 | — |
| Relation | chip: Exact duplicate, Near duplicate, Variant, Related | — |
| Differing fields | list or chips (count when long) | — |
| Similarity factors | text | not in the schema: `Similarity factors` |
| Matched because | text | not in the schema: `Matched because` |

**Data it reads**: `findSimilarMediaAssets` (onLoad, Visually similar and related)

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visual similarity related list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visual similarity related untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Visual Similarity & Related Asset Discovery. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visual similarity related are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
selected: wave-pool-hero.jpg
similar:
- asset: wave-pool-hero-v2.jpg
  similarity: 97%
- asset: wave-pool-crowd.jpg
  similarity: 81%
```

#### Permissions

- `findSimilarMediaAssets` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Visual similarity search finds similar stored images; near-duplicate detection flags near-identical uploads (e.g. 99% similarity) for a keep / replace / discard decision. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-850)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-074` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-074`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 6: Works in Visual Similarity & Related Asset Discovery → Allow users to find visually related or similar media.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-074?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-075` Duplicate & Near-Duplicate Management

**Prevent the DAM from becoming filled with unnecessary copies of identical or nearly identical content.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-075 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `mediaId` (navigation) |
| Route | `/media-library/duplicate-near-duplicate-management-cms-075` |

**What the spec says about it.** **Archive and quarantine are reversible; deletion is the only end of an asset's life (decided 28 September, audit STATE-MEDIA).** Archive Duplicate archives the copy (`updateMediaAsset`, `status: archived`) and can be undone with Restore Archived Copy; Delete Duplicate (`deleteMediaAsset`) removes it for good.

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 0 operations.** Unserved: Exact Duplicate, Near Duplicate, Keep Both, Mark Related, Create Version Relationship, Replace Duplicate … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Exact and near duplicates with what to do: keep both, relate, version, replace, archive or delete. Deleting a duplicate in use is refused or warned with its usages.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Asset | upload, or pick from the media library | — | — | `findSimilarMediaAssets` ?assetId |
| Min similarity | number field | 0.8 | — | `findSimilarMediaAssets` ?minSimilarity |

**Form: Archive Duplicate** (confirmDialog, opened by *Archive Duplicate*; *Archive* calls `updateMediaAsset`, *Cancel* sends nothing)

**Archive Duplicate is reversible** (decided 28 September, audit STATE-MEDIA): the copy leaves use and can be restored to `ready`; it is refused while the copy is referenced. Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Accessibility text. Required before an asset may be used in a guest-facing surface — WCAG 2.2 AA is a stated target. | `updateMediaAsset` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateMediaAsset` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Replaces the asset's collection memberships. Stored as `MediaCollectionMember` rows, one per collection. | `updateMediaAsset` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `updateMediaAsset` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `updateMediaAsset` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `updateMediaAsset` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `updateMediaAsset` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `updateMediaAsset` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `updateMediaAsset` body |
| Status `status` | segmented control | optional | — | Ready · Archived; Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | — | A lifecycle move from `states/media.yaml`. Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | `updateMediaAsset` body |

Errors to draw in the form: 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem)

**Form: Delete Duplicate** (confirmDialog, opened by *Delete Duplicate*; *Delete* calls `deleteMediaAsset`, *Cancel* sends nothing)

**Deletes the copy for good** — deletion is the only end of an asset's life (decided 28 September, audit STATE-MEDIA). Names the copy and the asset it duplicates, lists every reference when refused as in use, and offers Archive instead where the copy may be wanted again.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 409 Asset is in use. (MediaInUseProblem)

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Exact Duplicate (primary button) | navigation or local | — | — | — | — |
| Near Duplicate (secondary button) | navigation or local | — | — | — | — |
| Keep Both (secondary button) | navigation or local | — | — | — | — |
| Mark Related (secondary button) | navigation or local | — | — | — | — |
| Create Version Relationship (secondary button) | navigation or local | — | — | — | — |
| Replace Duplicate (secondary button) | navigation or local | — | — | — | — |
| Archive Duplicate (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |
| Restore Archived Copy (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |
| Delete Duplicate (destructive button) | `deleteMediaAsset` DELETE `/media/{mediaId}` | — | — | 409 Asset is in use. (MediaInUseProblem) | opens confirmDialog first |

**Data it reads**: `findSimilarMediaAssets` (onLoad, Duplicates above the threshold)

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The duplicate near-duplicate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the duplicate near-duplicate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Duplicate & Near-Duplicate Management. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the duplicate near-duplicate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Asset is in use. (MediaInUseProblem); 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds ASSET_LIBRARY_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ASSET_LIBRARY_MANAGE for Delete Duplicate, Archive Duplicate. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/assets.yaml#deleteMediaAsset)*
- **deleteMediaAsset answers 409**: Show it as something the person can act on, not a failure: Asset is in use. Every reference is listed *(source: contracts/satellite/assets.yaml#deleteMediaAsset)*
- **updateMediaAsset answers 409**: Show it as something the person can act on, not a failure: Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow from the asset's current status (`transitionNotAllowed`) *(source: contracts/satellite/assets.yaml#updateMediaAsset)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pair:
- logo-aquacove.png
- logo-aquacove (1).png
kind: exact duplicate
usages:
- 12
- 0
suggestion: Delete the unused copy
```

#### Permissions

- `findSimilarMediaAssets` → `ASSET_LIBRARY_VIEW` (read) · staff
- `deleteMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `updateMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Visual similarity search finds similar stored images; near-duplicate detection flags near-identical uploads (e.g. 99% similarity) for a keep / replace / discard decision. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-850)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-075` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-075`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 8: Works in Duplicate & Near-Duplicate Management → Prevent the DAM from becoming filled with unnecessary copies of identical or nearly identical content.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-075?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Exact Duplicate, Near Duplicate, Keep Both, Mark Related, Create Version Relationship, Replace Duplicate, Archive Duplicate, Restore Archived Copy, Delete Duplicate.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-076` Asset Version Control & Revision History

**Maintain controlled versions of the same logical digital asset without creating unrelated master records.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-076 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation), `mediaId` (navigation) |
| Route | `/media-library/asset-version-control-revision-history-cms-076` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Versions of one logical asset; making a version current updates every usage.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset version revision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset version revision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Asset Version Control & Revision History. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset version revision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds ASSET_LIBRARY_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ASSET_LIBRARY_MANAGE for replaceMediaAsset. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/assets.yaml#replaceMediaAsset)*
- **replaceMediaAsset answers 409**: Show it as something the person can act on, not a failure: The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed (`sizeExceeded`) *(source: contracts/satellite/assets.yaml#replaceMediaAsset)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listMediaAssetVersions (MediaAssetVersion):
- version: 12
  sizeBytes: 12
  createdAt: 01/10/2026 09:14
  note: Guest charged twice at Main Gate Till 3
  isCurrent: true
- version: 3
  sizeBytes: 3
  createdAt: 30/09/2026 18:02
  note: Group of 40 from Desert Gate Tours
  isCurrent: false
```

#### Permissions

- `listMediaAssetVersions` → `ASSET_LIBRARY_VIEW` (read) · staff
- `replaceMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.8 | System shall maintain historical versions of assets and allow comparison, rollback, and restoration. | Digital Asset Management | CONTRACTED | `replaceMediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Asset ID persists across versions (e.g. 1.0 -> 1.1); before confirming a replacement the user sees a replacement-impact analysis listing the live channels (kiosk, mobile app, etc.) that use the asset. *(agreed · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-851)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-076` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-076`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 10: Works in Asset Version Control & Revision History → Maintain controlled versions of the same logical digital asset without creating unrelated master records.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-076?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-077` Version Comparison & Replacement Impact

**Allow users to compare versions and understand the consequences of making a new version current.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-077 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/version-comparison-replacement-impact-cms-077` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Compare two versions and see what replacing the current one would change.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The version comparison replacement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the version comparison replacement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Version Comparison & Replacement Impact. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the version comparison replacement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listMediaAssetVersions (MediaAssetVersion):
- version: 12
  sizeBytes: 12
  createdAt: 01/10/2026 09:14
  note: Guest charged twice at Main Gate Till 3
  isCurrent: true
- version: 3
  sizeBytes: 3
  createdAt: 30/09/2026 18:02
  note: Group of 40 from Desert Gate Tours
  isCurrent: false
```

#### Permissions

- `listMediaAssetVersions` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Asset ID persists across versions (e.g. 1.0 -> 1.1); before confirming a replacement the user sees a replacement-impact analysis listing the live channels (kiosk, mobile app, etc.) that use the asset. *(agreed · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-851)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-077` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-077`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 12: Works in Version Comparison & Replacement Impact → Allow users to compare versions and understand the consequences of making a new version current.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-077?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-078` Transformation & Rendition Management

**Generate channel-appropriate media from a master asset without forcing users to manually upload many independent copies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-078 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators should configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/transformation-rendition-management-cms-078` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Channel renditions generated from a master asset (sizes, formats) by preset.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rendition Presets | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The transformation rendition configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the transformation rendition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Transformation & Rendition Management. Offers `requestMediaRendition`, the action this screen has; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds ASSET_LIBRARY_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ASSET_LIBRARY_MANAGE for requestMediaRendition. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/assets.yaml#requestMediaRendition)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listMediaRenditions (MediaRendition):
- width: 12
  height: 12
  sizeBytes: 12
  status: active
- width: 3
  height: 3
  sizeBytes: 3
  status: pending
```

#### Permissions

- `listMediaRenditions` → `ASSET_LIBRARY_VIEW` (read) · staff
- `requestMediaRendition` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- One uploaded image is auto-optimised into channel renditions (mobile app, B2C website, kiosk, etc.); rendition status shows per channel whether each version is ready or missing. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-849)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-078` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-078`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 14: Works in Transformation & Rendition Management → Generate channel-appropriate media from a master asset without forcing users to manually upload many independent copies.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-078?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-079` Rendition Processing & Delivery Readiness

**Monitor media-processing jobs and ensure required formats are ready before content is distributed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-079 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/rendition-processing-delivery-readiness-cms-079` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Retry, Cancel, View Error, Regenerate. Each needs an operation, or needs removing from the screen; this is … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Rendition jobs and whether required formats are ready before distribution; retry failures.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Retry (primary button) | navigation or local | — | — | — | — |
| Cancel (destructive button) | navigation or local | — | — | — | — |
| View Error (secondary button) | navigation or local | — | — | — | — |
| Regenerate (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

**What opens over it**

- confirmDialog *Cancel*: **Cancel on a rendition processing delivery is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rendition processing delivery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rendition processing delivery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Rendition Processing & Delivery Readiness. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rendition processing delivery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listMediaRenditions (MediaRendition):
- width: 12
  height: 12
  sizeBytes: 12
  status: active
- width: 3
  height: 3
  sizeBytes: 3
  status: pending
```

#### Permissions

- `listMediaRenditions` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- One uploaded image is auto-optimised into channel renditions (mobile app, B2C website, kiosk, etc.); rendition status shows per channel whether each version is ready or missing. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-849)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-079` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-079`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 16: Works in Rendition Processing & Delivery Readiness → Monitor media-processing jobs and ensure required formats are ready before content is distributed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-079?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Retry, Cancel, View Error, Regenerate.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-080` AI Quality, Intelligence Review & Recommendations

**Provide a governed review workspace for AI results and identify content-quality issues before assets are reused or distributed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-080 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/ai-quality-intelligence-review-recommendations-cms-080` |

**Known gaps.** **The pack names 12 actions on this screen and the screen declares 0 operations.** Unserved: Accept Recommendation, Reject, Review Asset, Generate Rendition, Resolve Issue, Board 2 — Shared … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Review AI results and content-quality issues with AI consumption and cost.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 9 labels bound). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getMediaUsageAnalytics` ?from |
| To | date and time picker | — | — | `getMediaUsageAnalytics` ?to |
| Group by | radio group | — | Asset type · Category · Venue · Owner · Channel | `getMediaUsageAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every quality intelligence review** (data table)

| Shows | Format | Notes |
|---|---|---|
| Assets processed | text | not in the schema: `Assets processed` |
| Images analyzed | text | not in the schema: `images analyzed` |
| Video minutes analyzed | text | not in the schema: `video minutes analyzed` |
| Audio minutes transcribed | text | not in the schema: `audio minutes transcribed` |
| OCR pages | text | not in the schema: `OCR pages` |
| Embedding generation | text | not in the schema: `embedding generation` |
| Semantic searches | text | not in the schema: `semantic searches` |
| AI requests | text | not in the schema: `AI requests` |
| Estimated/actual AI consumption cost | text | not in the schema: `estimated/actual AI consumption cost` |

**The selected quality intelligence review** (detail panel): The pack groups this record's detail under its own headings: “Digital Asset Management”, “Quality Score”, “Issues”, “Review Queue”, “DAM-IMG-008421”, “Versions”.

| Shows | Format | Notes |
|---|---|---|
| Assets processed | text | not in the schema: `Assets processed` |
| Images analyzed | text | not in the schema: `images analyzed` |
| Video minutes analyzed | text | not in the schema: `video minutes analyzed` |
| Audio minutes transcribed | text | not in the schema: `audio minutes transcribed` |
| OCR pages | text | not in the schema: `OCR pages` |
| Embedding generation | text | not in the schema: `embedding generation` |
| Semantic searches | text | not in the schema: `semantic searches` |
| AI requests | text | not in the schema: `AI requests` |
| Estimated/actual AI consumption cost | text | not in the schema: `estimated/actual AI consumption cost` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept Recommendation (primary button) | navigation or local | — | — | — | — |
| Reject (destructive button) | navigation or local | — | — | — | — |
| Review Asset (secondary button) | navigation or local | — | — | — | — |
| Generate Rendition (secondary button) | navigation or local | — | — | — | — |
| Resolve Issue (secondary button) | navigation or local | — | — | — | — |
| Board 2 — Shared Configuration Requirements (secondary button) | navigation or local | — | — | — | — |
| AI processing enabled/disabled (secondary button) | navigation or local | — | — | — | — |
| supported AI capabilities (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (estimated/actual AI consumption cost)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `getMediaUsageAnalytics` (onLoad, Quality and coverage)

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

**What opens over it**

- confirmDialog *Reject*: **Reject on a quality intelligence review is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The quality intelligence review list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the quality intelligence review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for AI Quality, Intelligence Review & Recommendations. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the quality intelligence review are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every quality intelligence review:
- Assets processed: 128
  images analyzed: 3 h 20 min
  video minutes analyzed: 57
  audio minutes transcribed: 46
  OCR pages: 3 h 20 min
  embedding generation: 19
  semantic searches: 46
  AI requests: 128
- Assets processed: 46
  images analyzed: 42 min
  video minutes analyzed: 11
  audio minutes transcribed: 312
  OCR pages: 42 min
  embedding generation: 233
  semantic searches: 312
  AI requests: 42
- Assets processed: 312
  images analyzed: 1.8 s
  video minutes analyzed: 128
  audio minutes transcribed: 74
  OCR pages: 1.8 s
  embedding generation: 57
  semantic searches: 74
  AI requests: 7
```

#### Permissions

- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI quality review flags low resolution, missing information, unsupported renditions or inconsistent formatting, with recommended fixes. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-852)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-080` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-080`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 18: Works in AI Quality, Intelligence Review & Recommendations → Provide a governed review workspace for AI results and identify content-quality issues before assets are reused or distributed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-080?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept Recommendation, Reject, Review Asset, Generate Rendition, Resolve Issue, Board 2 — Shared Configuration …, AI processing enabled/disabled, supported AI capabilities.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P13 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html`: the look of the controls: every configuration control, laid out and explained.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the configuration side panel, for the controls, and the guest booking the live preview shows.
- `sources/designs/TICVAI_White_Label_Guest_App_UI_Reference_1.pdf`: the client's White Label Builder boards.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P13 as a whole** (5: 0 open, 5 closed). Open first; a closed row says where it went on 30 September.

- **A47** Advise Qossai/Allam on the Apple/Google Developer account ownership model and a simplified, low-effort app-publishing workflow for white-labelled tenant apps (incl. how to reflect "Powered by TICVAI" branding) *(Pradnya Yeram · Low · Done → 30 Sep: Closed, Done (as recorded earlier) · 24 Sep 2026 · workshop tracker)*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker)*
- **A338** Build the real white-label CMS builder (client builds a site in ~30 min) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Sep 2026 · workshop tracker)*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker)*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker)*

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

### Across P13 Venue CMS

- The config side panel is a reference tool only, not the CMS. The CMS will be step-based and include header/footer, logos and banners. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W12 Config side panel · DI-1014)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Qossai: build AI-assisted site design/generation into the website builder, keeping site design (header, footer, color, font, layout) separate from content (tickets), with tickets flowing into the site's structure once published. To be explored. *(client request · MoM 3 Aug 2026, 7. AI-Assisted Website Generation · DI-115)*
- Qossai: give clients as much design flexibility as possible within the configurable structure. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-114)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"analyseMediaAsset": {"method":"POST","path":"/media-assets/{assetId}/analyse","contract":"assets","summary":"Auto-tag, describe and classify an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteMediaAsset": {"method":"DELETE","path":"/media/{mediaId}","contract":"assets","summary":"Delete an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"findSimilarMediaAssets": {"method":"GET","path":"/media-assets/similar","contract":"assets","summary":"Visually similar, near-duplicate and related assets","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"assetId","in":"query","required":true},{"name":"minSimilarity","in":"query","required":null}],"requestBody":null,"responds":"MediaSimilarity"},
"getMediaUsageAnalytics": {"method":"GET","path":"/media-usage","contract":"assets","summary":"Downloads, views, shares and library health","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"MediaUsageRow"},
"listMediaAssetVersions": {"method":"GET","path":"/media-assets/{assetId}/versions","contract":"assets","summary":"Every revision, and what replacing it would affect","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetVersion"},
"listMediaRenditions": {"method":"GET","path":"/media-assets/{assetId}/renditions","contract":"assets","summary":"The derived sizes and formats, and whether they are ready","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaRendition"},
"replaceMediaAsset": {"method":"POST","path":"/media/{mediaId}/replace","contract":"assets","summary":"Replace the file behind an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaReplaceResult"},
"requestMediaRendition": {"method":"POST","path":"/media-assets/{assetId}/renditions","contract":"assets","summary":"Generate a size or format","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaRendition","responds":null},
"searchMedia": {"method":"GET","path":"/media","contract":"assets","summary":"Search the asset library","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"tag","in":"query","required":null},{"name":"collectionId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":"unusedOnly","in":"query","required":null},{"name":"rightsExpiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setMediaAssetTags": {"method":"PUT","path":"/media-assets/{assetId}/tags","contract":"assets","summary":"Tags and keywords, whoever or whatever supplied them","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaTag"},
"updateMediaAsset": {"method":"PATCH","path":"/media/{mediaId}","contract":"assets","summary":"Amend metadata, tags or rights","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetVersion": {"type":"object","x-ticvai-persistence":"assets.asset_version","description":"Boards 2.6 and 2.7. **Usage impact belongs to the version read**, because replacing a logo is routine or an incident depending on where it appears.\n","properties":{"assetId":{"type":"string","format":"uuid"},"version":{"type":"integer"},"fileName":{"type":"string"},"sizeBytes":{"type":"integer"},"checksum":{"type":"string","nullable":true},"createdBy":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"note":{"type":"string","nullable":true},"isCurrent":{"type":"boolean"},"usageImpact":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"surface":{"type":"string","enum":["campaign","journey","ticketTemplate","screen","publishedPage","product","signage"]},"referenceId":{"type":"string","format":"uuid"},"label":{"type":"string"},"live":{"type":"boolean"}}}},"scopePath":{"type":"string"}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MediaRendition": {"type":"object","x-ticvai-persistence":"assets.rendition","description":"Boards 2.8 and 2.9. **Readiness is the fact that matters**, not existence.","required":["preset"],"properties":{"id":{"type":"string","format":"uuid"},"preset":{"type":"string","description":"e.g. `thumbnail`, `web1600`, `printCmyk`, `hls720`."},"format":{"type":"string","nullable":true},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"sizeBytes":{"type":"integer","nullable":true},"status":{"type":"string","enum":["queued","processing","ready","failed"]},"failureReason":{"type":"string","nullable":true},"url":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"MediaReplaceResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","affectedSurfaces"],"properties":{"asset":{"$ref":"#/components/schemas/MediaAsset"},"affectedSurfaces":{"type":"integer","description":"How many surfaces now show the new file."},"liveSurfaces":{"type":"integer","description":"Of those, how many are published to guests right now."},"derivativesRegenerating":{"type":"boolean"}}},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaSimilarity": {"type":"object","description":"Boards 2.4 and 2.5. **Duplicate and related are one score at two thresholds.**","properties":{"assetId":{"type":"string","format":"uuid"},"similarity":{"type":"number"},"relation":{"type":"string","enum":["exactDuplicate","nearDuplicate","variant","related"]},"differingFields":{"type":"array","items":{"type":"string"}}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"MediaTag": {"type":"object","x-ticvai-persistence":"assets.tag","description":"Board 2.2. **A tag carries its origin and confidence**, so machine labels can be filtered without being deleted.\n","required":["value"],"properties":{"value":{"type":"string"},"vocabulary":{"type":"string","nullable":true},"source":{"type":"string","enum":["human","autoTag","import","inherited"],"default":"human"},"confidence":{"type":"number","nullable":true},"accepted":{"type":"boolean","default":true,"description":"A proposed auto-tag below the promotion threshold sits here as false."},"addedBy":{"type":"string","format":"uuid","nullable":true},"addedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"MediaUsageRow": {"type":"object","description":"Boards 1.10 and 4.9. **Assets never used is the number that justifies the library.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"assetCount":{"type":"integer"},"storageBytes":{"type":"integer"},"downloads":{"type":"integer"},"views":{"type":"integer"},"shares":{"type":"integer"},"neverUsedCount":{"type":"integer"},"unclassifiedCount":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
