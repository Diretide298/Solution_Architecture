# P06-operations-05 — P06 · Operations (5 of 5)

**6 screens · 11 operations · 25 schemas · 7 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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
  `ACCESS_VALIDATE, INCIDENT_MANAGE, INCIDENT_VIEW, INSPECTION_SUBMIT, INSPECTION_VIEW, REPORT_VIEW_VENUE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **5 of these operations work offline**: acknowledgeAnnouncement, listAnnouncements, listInspectionTemplates, logout, submitInspection
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `EMP-048` | Opening checklist | D | 12 | 13 | 6 | 2 | 0 | 0 | — | notStarted (generated) |
| `EMP-047` | Emergency mode | D | 1 | 9 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `EMP-050` | Post-incident restore | D | 15 | 14 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `EMP-045` | Arabic / RTL | D | 0 | 0 | 4 | 0 | 0 | 0 | — | notStarted (generated) |
| `EMP-046` | Sign out | B | 0 | 0 | 4 | 0 | 0 | 0 | — | notStarted (generated) |
| `EMP-049` | Hand over the journal | C | 20 | 7 | 6 | 8 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**EMP-045, EMP-046 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-048` Opening checklist

**Confirm a gate is fit to open before the first guest reaches it.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | Block D · task APP-SETUP-EMP-048 |
| Who uses it | venue staff holding `INSPECTION_SUBMIT`, `INSPECTION_VIEW` (1 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listInspectionTemplates` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Works from the cached template. Completions queue |
| Opens with | nothing: it opens on its own |
| Route | `/operations/opening-checklist` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Template authoring (createInspectionTemplate, INSPECTION_MANAGE) is tenant-level management in the back office; the opening checklist only works today's checks …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** On the Staff App, before the first guest arrives, a steward or technician works the opening checklist for their gate, ride or area: pick today's checks, answer each item (pass/fail, yes/no, a number, a photo, a signature), sign, submit - offline if needed. The one thing to get right: a failed safety-critical item is unmistakable, cannot be "passed" by completing the rest, and takes the asset out of service by itself.

**Fixed on main** (the package already carries these; draw what it says): "Create inspection template" on the phone screen and a table of every template (CHG-WIR-001); Navigation exits to Sign in and Select venue (inferred) (CHG-WIR-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Template | picker: choose a template | — | — | `listInspections` ?templateId |
| Asset | upload, or pick from the media library | — | — | `listInspections` ?assetId |
| Outcome | segmented control | — | Passed · Passed with observations · Failed | `listInspections` ?outcome |
| Performed from | date picker | — | — | `listInspections` ?performedFrom |
| Performed to | date picker | — | — | `listInspections` ?performedTo |

**Form: Submit inspection** (modal, opened by *Submit inspection*; *Submit inspection* calls `submitInspection`, *Cancel* sends nothing)

**Collects what `submitInspection` sends before it is called.** Required: `id`, `templateId`, `venueId`, `responses`, `recordedAt`. Optional: `assetId`, `signatureRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `submitInspection` body |
| Template `templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `submitInspection` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `submitInspection` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `submitInspection` body |
| Responses `responses` | repeatable rows | required | — | at least 1 | — | — | `submitInspection` body |
| Key `responses[].key` | text field | required | — | — | — | — | `submitInspection` body |
| Value `responses[].value` | field | required | — | — | — | — | `submitInspection` body |
| Passed `responses[].passed` | toggle | optional | — | — | — | — | `submitInspection` body |
| Note `responses[].note` | text area | optional | — | max length 1000 | — | — | `submitInspection` body |
| Attachment refs `responses[].attachmentRefs` | list of values (chips) | optional | — | — | — | — | `submitInspection` body |
| Signature ref `signatureRef` | text field | optional | — | — | — | — | `submitInspection` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `submitInspection` body |

Errors to draw in the form: 400 A required item was not answered

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Checklist choice**: Show only today's pre-opening templates for the venue and the person's area (frequency Pre-opening first, then Daily); not a table of all templates. *(source: contracts/satellite/maintenance.yaml#listInspectionTemplates)*
- **Item responses**: One item per card, large touch targets: Pass/Fail and Yes/No as two big buttons, numeric with unit and expected range, text, photo (camera opens directly), signature pad at the end. Safety-critical items carry a red "Safety" tag; the template's instructions are one tap away on each item. *(source: contracts/satellite/maintenance.yaml#createInspectionTemplate / MATRIX 17.5.1 / DI-232)*
- **Asset**: Scan the asset's tag to attach it (lookup works offline); typed search as fallback. *(source: contracts/satellite/maintenance.yaml#lookupAsset)*

#### Outputs: what the screen shows and produces

**Shown**

**Every inspection template** (data table, from `listInspectionTemplates`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Frequency | chip: Pre opening, Post closing, Daily, Weekly, Monthly, Annual… | — |
| Retention years | 1,234 | Compliance inspections are retained alongside the financial trail. |

**Every inspection** (data table, from `listInspections`)

| Shows | Format | Notes |
|---|---|---|
| Template name | text | — |
| Outcome | chip: Passed, Passed with observations, Failed | — |
| Failed item count | 1,234 | — |
| Failed safety critical count | 1,234 | — |

**The selected inspection template** (detail panel, from `listInspectionTemplates`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Frequency | chip: Pre opening, Post closing, Daily, Weekly, Monthly, Annual… | — |
| Items | list or chips (count when long) | — |
| Retention years | 1,234 | Compliance inspections are retained alongside the financial trail. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit inspection (primary button) | `submitInspection` POST `/inspections` | SubmitInspectionRequest | InspectionResult | 400 A required item was not answered | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Progress**: "7 of 12 checked, 1 failed (safety)" with failed items listed first at the end. *(source: contracts/satellite/maintenance.yaml#submitInspection)*
- **Result**: Passed (green) / Failed - asset taken out of service, work order raised (red), with the work order number. *(source: contracts/satellite/maintenance.yaml#submitInspection)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Submit**: Requires the signature; queued when offline with "Will send when you are back online" and a count in the header. *(source: contracts/satellite/maintenance.yaml#submitInspection)*

**Data it reads**: `listInspectionTemplates` (onLoad, List inspection templates); `listInspections` (onLoad, List completed inspections)

**Where the user goes next**

- → `EMP-003` Home — on duty: *Sees the home screen on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The opening checklist list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the opening checklist untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No opening checklist yet. Offers Submit inspection (`submitInspection`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listInspectionTemplates` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `INSPECTION_VIEW`, which `listInspectionTemplates` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INSPECTION_SUBMIT` for `submitInspection`. |
| Offline (`?state=offline`) | Works from the cached template. Completions queue |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required item was not answered |

#### Edge cases to draw

- **Offline at the start of the shift**: Works from the cached template; the submission queues; the asset is marked out of service locally and the server confirms on sync. *(source: screens/P06-staff-app.yaml#EMP-048 / contracts/satellite/maintenance.yaml#submitInspection)*
- **Template changed since cached**: Banner "A newer checklist exists - refresh when online"; completing the cached one is still valid. *(source: designer default)*

#### Consistency with other screens

- Match `EMP-004`: A failed item's work order appears in the technician's task list.
- Match `BO-069`: The asset's status changes there (Out of service) with the inspection as the reason.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
checklist:
  name: Falcon Coaster - pre-opening
  items:
  - Restraint bars lock (safety) - Pass
  - Track walk complete - Yes
  - Hydraulic pressure 180-220 bar - 205
  - Queue line barriers in place - Yes
  - Photo of station platform
  by: Rahul Menon
  at: 07:42
```

#### Permissions

- `listInspectionTemplates` → `INSPECTION_VIEW` (read) · staff
- `submitInspection` → `INSPECTION_SUBMIT` (operate) · staff
- `listInspections` → `INSPECTION_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `INSPECTION_VIEW`, which `listInspectionTemplates` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INSPECTION_SUBMIT` for `submitInspection`.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.5.7 | Safety Audits - System shall support safety audits. | Maintenance & Safety Management | CONTRACTED | `submitInspection` |
| 17.5.9 | Safety Compliance Tracking - System shall support safety compliance tracking. | Maintenance & Safety Management | CONTRACTED | `listInspections` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-048` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 3: Works the opening checklist → What must be true before the venue opens
- Flow F64 *A steward signs in and takes a venue and a role*, step 3: The opening checklist is worked. → **Tasks, not a paper list.** A checklist nobody records is a checklist nobody did.
- Flow F08 branch at step 3 (recoverable): when A gate needs covering mid-shift, EMP-010 through EMP-015 — the app scans too. Lower throughput than a handheld, and enough for a relief.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Submit inspection.
- [ ] Every transition is wired: `EMP-003`.
- [ ] Every gated control is gated: `INSPECTION_SUBMIT`, `INSPECTION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-047` Emergency mode

**Evacuate, and stop pretending to be a ticketing app.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | Block D · task APP-STAFF-EMP-047 |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act |
| Offline | Fully offline by design |
| Opens with | `announcementId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/emergency-mode` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Emergency mode is a full-screen takeover with one action (acknowledge); the generic announcements set put publish and the reach roll call on it. Declaring goes … Removed 2 October 2026 (CHG-WIR-001): Emergency mode is a full-screen takeover with one action (acknowledge); the generic announcements set put publish and the reach roll call on it. Declaring goes … Contract gap recorded 2 October 2026 (CHG-WIR-004): No staff all-clear (announcement kind or operation) ends emergency mode.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Emergency mode: when an emergency announcement arrives, the Staff App stops being a ticketing app and becomes one screen - what is happening, what to do, where to go, and a single "I have received this" button - until the duty manager stands it down. The one thing to get right: it is a full-screen takeover that cannot be dismissed into normal work, the acknowledgement works with no signal, and a duty manager on the same screen sees the roll call of who has not confirmed.

**Known correction pending (do not draw the wrong version)**

- **The screen is the generic announcements list-detail (toggle, "Every announcement" table, detail panel)** Why: Emergency mode is a full-screen takeover with one action; a table of all announcements is the opposite of what the flow asks. *(source: F08 step 2 / screens/P06-staff-app.yaml#EMP-047; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Nothing in the staff contract ends an emergency (no all-clear kind, no stand-down)** Why: The guest broadcast has allClear; the staff AnnouncementKind does not, so phones have no defined way out of emergency mode except expiresAt. *(source: contracts/satellite/workforce.yaml#/components/schemas/AnnouncementKind / contracts/satellite/workforce.yaml#broadcastToGuests; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Offline state "Fully offline by design" while publishAnnouncement and getAnnouncementReach are online only (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should staff emergency announcements carry assembly points like the guest broadcast does?** → Drawn default accepted: Name the assembly point in the instructions text; draw a "Show on map" link greyed until a field exists. *(decided by Chinmay, 2026-10-02; DEC-536 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Does declaring a staff emergency also need a second person, as the guest evacuation does?** → Drawn default stands (answer: "Single declarer with a typed confirmation; second person only on the guest broadcast"): Single declarer with typed confirmation; second-person approval drawn only on the guest broadcast. *(decided by Chinmay, 2026-10-02; DEC-537 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Unacknowledged only | toggle | optional | — | — | — | Sends `?unacknowledgedOnly=` to `listAnnouncements`. | `listAnnouncements` ?unacknowledgedOnly |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Acknowledge**: One large button "I have received this" (Arabic "تم الاستلام"), at least 56 px high, reachable one-handed at the bottom. Optional status after acknowledging, as chips: "Safe at assembly point", "Helping guests", "Need help". *(source: contracts/satellite/workforce.yaml#acknowledgeAnnouncement / F69 step 4 / designer default)*
- **Declare emergency (duty manager only)**: Title (max 140), instructions (max 4,000), audience (whole venue by default), and a typed confirmation ("EVACUATE") before sending. Kind is fixed to Emergency; acknowledgement and push are forced on and shown locked. *(source: contracts/satellite/workforce.yaml#publishAnnouncement)*

#### Outputs: what the screen shows and produces

**Shown**

**Every announcement** (data table, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| Title | text | — |
| Body | text | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published at | 1 Oct 2026, 14:30 | — |

**The selected announcement** (detail panel, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Acknowledge announcement (primary button) | `acknowledgeAnnouncement` POST `/announcements/{announcementId}/acknowledge` | — | — | — | works offline |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Takeover screen**: Red full-screen header "EMERGENCY" with the title, the instructions in large type, time declared and by whom, and the assembly point or exit named in the text. Bypasses quiet hours, plays the alert sound and vibrates even on silent where the OS allows. Normal navigation is hidden except a "Call duty manager" button. *(source: contracts/satellite/workforce.yaml#publishAnnouncement / F08 step 2)*
- **Roll call (duty manager)**: Targeted, delivered, acknowledged counts as tiles, then the outstanding list with on-shift people first, each with name, role and last known post, and a Call button. Refreshes every 15 seconds while online; shows its age offline. *(source: contracts/satellite/workforce.yaml#getAnnouncementReach / F69 step 4)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **I have received this**: Acknowledged instantly on the device ("Received 14:31, sending..." until sync); the screen stays in emergency mode with the instructions still visible. *(source: contracts/satellite/workforce.yaml#acknowledgeAnnouncement)*
- **Declare emergency**: Confirmation names the reach ("This will take over 212 staff phones at Aqua Park"); on success the declarer's own phone shows the roll call. A 403 shows "Needs emergency announcement rights". *(source: contracts/satellite/workforce.yaml#publishAnnouncement)*
- **Stand down (all clear)**: Duty manager ends emergency mode for the audience; phones return to EMP-050 post-incident restore, then home. *(source: F08 step 2 / screens/P06-staff-app.yaml#EMP-047)*

**Data it reads**: `listAnnouncements` (onLoad, What staff have been told)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-050` Post-incident restore: *Post-incident restore*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The emergency mode list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the emergency mode untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No emergency mode yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on unacknowledgedOnly and the emergency mode are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Fully offline by design |

#### Edge cases to draw

- **No signal when the emergency is received or acknowledged**: The takeover works from the cached announcement; the acknowledgement is journalled and sent on the first signal. The roll call is greyed with "Needs a connection" for the manager. *(source: contracts/satellite/workforce.yaml#acknowledgeAnnouncement)*
- **Person signed in mid-emergency or was on a break**: Emergency mode opens straight after sign-in, before role selection completes. *(source: F08 step 2)*
- **Two emergencies at once (e.g. evacuation of one zone and lightning hold elsewhere)**: Stacked, newest on top, each with its own acknowledge; the count "2 active" in the header. *(source: designer default)*
- **Publisher without ANNOUNCEMENT_EMERGENCY**: Declare emergency shown disabled with "Needs emergency announcement rights", never hidden. *(source: contracts/satellite/workforce.yaml#publishAnnouncement)*

#### Consistency with other screens

- Match `BO-066`: Emergency published from the back office triggers this screen; same title and instructions, same roll call wording.
- Match `EMP-050`: Stand down leads to post-incident restore.
- Match `BO-201`: Gate emergency controls (Drop arm) are a separate act on the gates; this screen tells staff. Guest evacuation notices (broadcastToGuests) are a third, two-person act. Show "Guests notified 14:32" here when known, and use the same zone and exit names.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
emergency:
  title: Evacuate Adventure Zone via North Exit
  instructions: Stop all rides in Adventure Zone. Guide guests to Assembly Point B (North Car Park). Do not use
    Gate 3.
  declared: 14:30 by Ahmed Al Mansoori, Operations manager
  reach:
    targeted: 212
    delivered: 205
    acknowledged: 188
    outstanding: 24
  outstanding:
  - name: Omar Haddad
    role: Ride operator
    post: Falcon Coaster
    onShift: true
  - name: Maria Santos
    role: Cashier
    post: North Entry ticket office
    onShift: true
```

#### Permissions

- `listAnnouncements` → `WORKFORCE_VIEW` (read) · staff
- `acknowledgeAnnouncement` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-047` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-047?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Acknowledge announcement, What publishing changes.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-050`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-050` Post-incident restore

**Put the venue back to how it was.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `maintenance` module |
| Block | Block D · task APP-STAFF-EMP-050 |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `INCIDENT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listIncidents` reads the population and `getIncident` reads one of them — list, select, act |
| Offline | **Works offline by design.** Post-incident restore is exactly when the network is worst |
| Opens with | `incidentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/post-incident-restore` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: reportIncident. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Recording the authority notification is a step of following up the incident (EMP-027), not of restoring the venue; the screen's own note says notification …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** After an incident is controlled - an evacuation, a fire alarm, a ride stop, a cordoned area - the duty supervisor puts the venue back the way it was: checks each thing the incident changed, returns rides and gates to service (with an inspection where required), sends the all-clear, and records that it was done. It must cope with poor or no network, because that is when it is used. The one thing to get right: a checklist of what is still out because of this incident, each item visibly restored or deliberately kept closed, so nothing reopens by accident and nothing stays closed by oversight.

**Known correction pending (do not draw the wrong version)**

- **The screen binds only incident list, update and authority notification; nothing it binds restores anything** Why: "Put the venue back to how it was" needs asset return to service (setAssetStatus with inspection), gate modes (setTurnstileMode), an all-clear (publishAnnouncement, getAnnouncementReach) and a read of what the incident changed. None is bound. *(source: screens/P06-staff-app.yaml#EMP-050 / contracts/satellite/maintenance.yaml#setAssetStatus / F69 step 4; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Nothing records what an incident took out of service** Why: AssetStatusChange carries workOrderId and inspectionId but no incidentId, so "what is still out because of this incident" cannot be read. *(source: contracts/satellite/maintenance.yaml#/components/schemas/AssetStatusChange; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **State "Works offline by design" but listIncidents and getIncident are online only** Why: The read the screen opens with cannot be served offline; cache the incident when EMP-027 opens it, or make getIncident offline-capable. *(source: contracts/satellite/maintenance.yaml#getIncident / screens/P06-staff-app.yaml#EMP-050; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Record authority notification bound here, and F69 step 3 makes this the notification screen (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the restore checklist a configurable ad-hoc inspection template per venue (as the rental pack's incident-based inspection suggests), or a fixed list?** → Drawn default accepted: Draw the incident-derived rows plus a configurable "Restore checks" section from an ad-hoc template. *(decided by Chinmay, 2026-10-02; DEC-538 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Severity | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | Sends `?severity=` to `listIncidents`. | `listIncidents` ?severity |
| Status | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | Sends `?status=` to `listIncidents`. | `listIncidents` ?status |
| Is reportable | toggle | optional | — | — | — | Sends `?isReportable=` to `listIncidents`. | `listIncidents` ?isReportable |

**Form: Save incident** (modal, opened by *Save incident*; *Save incident* calls `updateIncident`, *Cancel* sends nothing)

**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | — | `updateIncident` body |
| Severity `severity` | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | — | `updateIncident` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Investigation note `investigationNote` | text area | optional | — | max length 10000 | — | Appended as a new entry of `IncidentDetail.investigationNotes`, never overwriting the last (audit R106 (5)). | `updateIncident` body |
| Root cause `rootCause` | text area | optional | — | max length 2000 | — | — | `updateIncident` body |
| Corrective actions `correctiveActions` | text area | optional | — | max length 5000 | — | — | `updateIncident` body |
| Corrective work order `correctiveWorkOrderId` | picker: choose a corrective work order | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `updateIncident` body |
| Escalate `escalate` | group | optional | — | — | — | Escalate an incident under investigation (the optional Escalated step; CHG-RUL-011). | `updateIncident` body |
| To principal `escalate.toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `updateIncident` body |
| Reason `escalate.reason` | text area | required | — | min length 3; max length 1000 | — | — | `updateIncident` body |
| Reason `reason` | text area | optional | — | min length 3; max length 1000 | — | Why the status changes. Required to reopen a closed incident (back to `underInvestigation`) and to close a `reported` one straight away (CHG-RUL-011). | `updateIncident` body |

Errors to draw in the form: 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move outside the incident flow (`incident-transition-not-allowed`; CHG-RUL-011): to `actionRequired`, from `closed` to anything but `underInvestigation`, a …

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Restore checklist**: One row per thing taken out - assets out of service, gates in Drop arm or Closed, rides closed, areas restricted, products stopped - each with Restore or Keep closed; Keep closed requires a reason. Generic checks follow (area clear of hazards, barriers removed, first-aid stock replaced) from an ad-hoc inspection template. *(source: screens/P06-staff-app.yaml#EMP-050 / contracts/satellite/maintenance.yaml#/components/schemas/InspectionTemplate)*
- **Return asset to service**: For an asset that requires an inspection to return, Restore opens the inspection first; the return is refused without it. A reason is always recorded ("Restored after INC-2026-0217 - false alarm, ride inspected"). *(source: contracts/satellite/maintenance.yaml#setAssetStatus / F12 step 5)*
- **Gate mode**: Gates changed during the incident are listed with their current mode and a "Back to Normal" control, using the access gate-mode component (Drop arm green, Closed red). *(source: contracts/spine/access.yaml#setTurnstileMode)*
- **All-clear announcement**: Prefilled message ("All clear at the food court - normal operation resumed 12:40"), audience (staff in zone or whole venue), acknowledgement required for venue-wide events. *(source: contracts/satellite/workforce.yaml#publishAnnouncement / F69 step 4)*

#### Outputs: what the screen shows and produces

**Shown**

**Every incident** (data table, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The selected incident** (detail panel, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The incident** (detail panel, from `getIncident`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save incident (secondary button) | `updateIncident` PATCH `/incidents/{incidentId}` | inline | Incident | 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Incident header**: Incident number, kind, severity, time since it occurred, and progress "4 of 6 restored"; reportable incidents show notification status read-only. *(source: contracts/satellite/maintenance.yaml#getIncident)*
- **Restored log**: Each restored item with who and when, appended to the incident as an investigation note so the incident's timeline shows the restore. *(source: contracts/satellite/maintenance.yaml#updateIncident)*
- **Announcement reach**: "Read by 38 of 45 staff" with the names of those who have not acknowledged, for venue-wide events. *(source: contracts/satellite/workforce.yaml#getAnnouncementReach / F69 step 4)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Restore (per row)**: Performs that row's act (asset status, gate mode, ride reopen) and ticks it; a failure is shown on the row ("Needs the post-maintenance inspection"). *(source: contracts/satellite/maintenance.yaml#setAssetStatus / contracts/spine/access.yaml#setTurnstileMode)*
- **Send all clear**: Publishes the announcement and opens Emergency mode (EMP-047) to follow acknowledgements. *(source: contracts/satellite/workforce.yaml#publishAnnouncement / F69 step 4)*
- **Finish restore**: Allowed when every row is Restored or Keep closed with a reason; appends a "Venue restored" note and returns home carrying the incident id. *(source: contracts/satellite/maintenance.yaml#updateIncident / designer default)*

**Data it reads**: `listIncidents` (onLoad, List incidents)

**Where the user goes next**

- → `EMP-047` Emergency mode: *If it is a venue-wide event, an announcement goes out*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*; carries `incidentId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The post-incident restore list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the post-incident restore untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No post-incident restore yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on severity, status, isReportable and the post-incident restore are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `updateIncident`. |
| Offline (`?state=offline`) | **Works offline by design.** Post-incident restore is exactly when the network is worst |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Closure attempted without findings or a corrective action; 422 A move outside the incident flow (`incident-transition-not-allowed`; CHG-RUL-011): to `actionRequired`, from `closed` to anything but `underInvestigation`, a … |

#### Edge cases to draw

- **No network**: Asset return to service and inspections are offline-capable and queue; gate modes and announcements need the network and are greyed with "Needs connection - use the radio" (per VO-R07). *(source: contracts/satellite/maintenance.yaml#setAssetStatus / contracts/satellite/maintenance.yaml#submitInspection)*
- **Something stays closed**: Kept-closed items stay on the home screen as "Still closed after INC-2026-0217" until restored. *(source: designer default)*
- **Ride back in service but its queue did not reopen**: The row shows "Ride back in service - queue still closed" and offers to reopen the queue (the F12 cascade failure). *(source: F12 step 5)*

#### Consistency with other screens

- Match `EMP-047`: Emergency mode starts what this screen ends; the same list of what was changed (gates, rides, areas) is shown in both.
- Match `BO-069`: Return to service uses the same reason and inspection rules as the asset register.
- Match `EMP-027`: Restore entries appear in the incident's timeline.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
incident: INC-2026-0217 Fire alarm, Summit Peaks food court, Major, occurred 12:05
items:
- item: Food court zone
  change: Evacuated
  action: Restore
  done: 12:38 Ahmed Al Mansoori
- item: North Entry gates 1-2
  change: Drop arm
  action: Back to Normal
  done: '12:39'
- item: Laser Arena
  change: Out of service
  action: Restore after inspection
  done: pending
- item: Falcon Coaster
  change: Stopped
  action: Keep closed
  reason: Unrelated restraint fault WO-2026-01482
announcement: All clear at Summit Peaks food court - normal operation resumed 12:40 (read by 38 of 45)
```

#### Permissions

- `listIncidents` → `INCIDENT_VIEW` (read) · staff
- `getIncident` → `INCIDENT_VIEW` (read) · staff
- `updateIncident` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `updateIncident`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.5 | System shall provide real-time visibility of incidents, hazards, complaints, emergencies, and operational disruptions. | Unified Operations Dashboard | CONTRACTED | `listIncidents` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-050` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-050?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save incident.
- [ ] Every transition is wired: `EMP-047`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `INCIDENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-045` Arabic / RTL

**Render the staff app right to left.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | Block D · task APP-STAFF-EMP-045 |
| Who uses it | venue |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **the screen's operations choose no pattern** — no list, no get, no write that groups. It falls to the default, and the fallback is recorded rather than passed off as a decision |
| Offline | **Fully offline.** Direction is a device setting, not a server one |
| Opens with | nothing: it opens on its own |
| Route | `/operations/arabic-rtl` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** **This screen declares no operation the contracts recognise.** Nothing fills it, nothing it does is committed anywhere, and its shape below is a default rather than a reading.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Language and direction for the Staff App: choose English or Arabic, and the whole app mirrors right to left. Reached from Device settings; works with no network. The one thing to get right: Arabic is a mirror, not a translation - layout, navigation and icons with a direction flip, while numbers, times, money, ticket and media codes stay left to right inside the Arabic line.

**Known correction pending (do not draw the wrong version)**

- **Screen named "Arabic / RTL" with pattern listDetail and no operations** Why: It is the Language setting (English, Arabic) whose consequence is direction; draw it as a two-option settings screen with preview. *(source: screens/P06-staff-app.yaml#EMP-045; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Staff announcements carry a single locale with no Arabic variant, so the language chosen here cannot be honoured for them** Why: DI-019 includes notifications in full Arabic support. *(source: DI-019 / contracts/satellite/workforce.yaml#/components/schemas/Announcement; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are Arabic-Indic digits ever wanted on staff devices, or always Western digits?** → Drawn default accepted: Western digits in both languages; no digits toggle drawn until confirmed. *(decided by Chinmay, 2026-10-02; DEC-535 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Language**: Two large options, each written in its own language: "English" and "العربية". Choosing one switches text and direction immediately, with no restart. Follows the device language on first run. *(source: DI-019)*
- **Digits**: Western digits (0-9) by default in both languages; a toggle for Arabic-Indic digits only if the client confirms. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Preview**: A sample shift card ("السبت 10 أكتوبر، 07:00 - 15:00، بوابة الساحة الرئيسية 2") and a sample price "AED 1,855.00" rendered in the chosen direction, showing the time range and amount kept left to right. *(source: DI-019)*
- **What changes**: One line under the choice, "Menus, lists and calendars run right to left. Times, prices and codes do not change." *(source: ADR-0011 / DI-019)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Choose language**: Applies at once to every screen, including the rota calendar (days run right to left), the scanner result and notifications text. *(source: DI-019)*

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | — |
| Error (`?state=error`) | — |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Offline (`?state=offline`) | **Fully offline.** Direction is a device setting, not a server one |

#### Edge cases to draw

- **Content that exists only in English (an announcement written in English, a guest name in Latin script)**: Shown as written inside the mirrored layout, aligned to its own script; tagged "English only" on announcements. *(source: DI-019 / contracts/satellite/workforce.yaml#/components/schemas/Announcement)*
- **Offline**: Fully usable; language is a device setting. *(source: screens/P06-staff-app.yaml#EMP-045)*
- **Time range in Arabic**: "07:00 - 15:00" keeps start on the left; the dash never reverses the operands. *(source: ADR-0011 / DI-019)*

#### Consistency with other screens

- Match `EMP-044`: Same settings layout; the accessibility preview follows the language chosen here.
- Match `EMP-022`: The rota calendar must be checked in both directions (week runs right to left in Arabic).
- Match `EMP-039`: Announcements show the Arabic version when the device is in Arabic and one exists.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
options:
- English
- العربية
preview:
  shift: السبت 10 أكتوبر 2026، 07:00 - 15:00
  post: بوابة الساحة الرئيسية 2
  amount: AED 1,855.00
  ticket: VT0010
```

#### Permissions

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-045` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-045?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-046` Sign out

**Leave the shared device safe for the next person.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | Block B · task APP-STAFF-EMP-046 |
| Who uses it | venue |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`logout`) and no read of a population — it is settings, not a list |
| Offline | Signs out locally and the journal stays on the device for the next steward |
| Opens with | nothing: it opens on its own |
| Route | `/operations/sign-out` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** **`logout` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Leave the shared handheld safe for the next person: sign out, with what stays on the device said plainly. A steward with queued offline scans is told they will sync after sign-out, not lost.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Logout (primary button) | `logout` POST `/auth/logout` | — | — | — | works offline |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Sign out**: Ends this session only; pending offline actions remain queued under the person who made them and sync when online; returns to EMP-001. *(source: contracts/spine/identity.yaml#logout; ADR-0013)*

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Closing the session |
| Error (`?state=error`) | **Sign-out with a pending journal warns rather than blocks.** A steward handing over a device must not be trapped by a failed sync |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Offline (`?state=offline`) | Signs out locally and the journal stays on the device for the next steward |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pendingSync: 14 scans waiting to sync
signedIn: Yusuf Rahman · Steward · since 07:58
```

#### Permissions

- `logout` → no permission · staff

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-046` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-046?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Logout, Cancel.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-049` Hand over the journal

**Move an unsynced journal off a device that is going flat.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `access` module |
| Block | Block C · task APP-STAFF-EMP-049 |
| Who uses it | venue staff holding `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The point of the screen.** It exists because the journal outlives the shift |
| Opens with | nothing: it opens on its own |
| Route | `/operations/hand-over-the-journal` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No operation hands an unsynced scan journal from one device to another or to the edge node.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Hand over an unsynced journal from a device that is going flat or changing hands, so the next shift does not carry somebody else's scans: show what is unsynced, and transfer it (to another device or the venue edge) before the device is passed on. The one thing to get right: the device cannot be handed over silently with an unsynced journal.

**Known correction pending (do not draw the wrong version)**

- **The screen declares no operation at all** Why: Handing over a journal (device to device, or to the edge node) has no contract; it cannot be built. *(source: screens/P06-staff-app.yaml#EMP-049 / F71 step 3; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |

**Form: Sync scans** (modal, opened by *Sync scans*; *Sync scans* calls `syncScans`, *Cancel* sends nothing)

**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | Sequence numbers are monotonic per device, not globally. | `syncScans` body |
| Scans `scans` | repeatable rows | required | — | at least 1; at most 500 | — | — | `syncScans` body |
| ID `scans[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `syncScans` body |
| Media code `scans[].mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `syncScans` body |
| Media kind `scans[].mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `syncScans` body |
| Direction `scans[].direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `syncScans` body |
| Group size `scans[].groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `syncScans` body |
| Proximity token `scans[].proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `syncScans` body |
| Recorded at `scans[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `syncScans` body |
| Sequence `scans[].sequence` | number field | required | — | min 1 | — | Monotonic per device. The server processes in this order. | `syncScans` body |
| Local outcome `scans[].localOutcome` | segmented control | required | — | Admitted · Denied · Overridden | — | What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded. | `syncScans` body |
| Local deny reason `scans[].localDenyReason` | select | optional | — | Not found · Not yet valid · Expired · Already used · Reentry limit reached · Exit required before reentry · Wrong access point · Wrong performance · Outside admission window · Entitlement suspended · Blacklisted · Capacity reached … | — | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean. | `syncScans` body |
| Overridden by principal `scans[].overriddenByPrincipalId` | picker: choose an overridden by principal | optional | — | — | shows names, sends the id | — | `syncScans` body |
| Override reason `scans[].overrideReason` | text field | optional | — | — | — | — | `syncScans` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |

**The selected scan event** (detail panel, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | Null while pending. Differs from recordedAt for offline scans. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sync scans (primary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Unsynced journal**: Count, oldest item, owner (the steward whose scans they are). *(source: F71 step 3)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Hand over**: Not bound to any operation yet; draw the action with the transfer target and flag it. *(source: screens/P06-staff-app.yaml#EMP-049)*

**Data it reads**: `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hand over the list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hand over the untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hand over the yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the hand over the are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_VALIDATE` for `syncScans`. |
| Offline (`?state=offline`) | **The point of the screen.** It exists because the journal outlives the shift |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `EMP-017`: A successful sync makes the handover unnecessary.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
journal:
  owner: Rahul Menon
  unsynced: 86
  oldest: '11:05'
  battery: 6%
```

#### Permissions

- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_VALIDATE` for `syncScans`.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| 18.1.4 | Synchronization - System shall synchronize data when connectivity is restored. | Employee Mobile App & AI Assistant | CONTRACTED | `syncScans` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-049` · status **notStarted** · provenance generated
- Flow F71 *A device is prepared, used and handed over*, step 3: At the end of the session the journal is handed over. → **Handed over, not just synced.** A device passed to the next shift with an unsynced journal carries somebody else’s scans.
- Flow F71 branch at step 3 (medium): when The journal will not sync., **A technician job, not a supervisor one.** Connectivity is IT; deciding whether a scan stands is not — CF-159 settled that split.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync scans.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P06 reference designs** (from `handoff/design-batches/apps/4-staff-app/README.md`)

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the client's employee app reference: dark theme, Home, Tasks, Scan, AI, More.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P06 as a whole** (3: 0 open, 3 closed). Open first; a closed row says where it went on 30 September.

- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A49** Confirm scope: deliver a lightweight standalone ticket-validation app for dedicated scanner devices, in addition to the scan/validate function embedded in the full Staff Operations App *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A71** Design an offline-first, native ticket-scanning/access-control capability (local scan storage with sync-on-reconnect) for both the dedicated scanner app and the scanning function embedded in the Employee App *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 10 Aug 2026 · workshop tracker)*

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

### Across P06 Venue Staff App

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### In P06 · Operations

- Employee app navigation: Work Orders, Task & Assets, Inventory/Safety/Inspections, Attendance, Approvals/Requests, Incidents, Communications, Venue Map; plus employee ID/profile and preferences. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-228)*

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acknowledgeAnnouncement": {"method":"POST","path":"/announcements/{announcementId}/acknowledge","contract":"workforce","summary":"Confirm you have read it","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getIncident": {"method":"GET","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Read an incident","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"IncidentDetail"},
"listAnnouncements": {"method":"GET","path":"/announcements","contract":"workforce","summary":"What staff have been told","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"unacknowledgedOnly","in":"query","required":null}],"requestBody":null,"responds":"Announcement"},
"listIncidents": {"method":"GET","path":"/incidents","contract":"maintenance","summary":"List incidents","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"isReportable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInspectionTemplates": {"method":"GET","path":"/inspection-templates","contract":"maintenance","summary":"List inspection templates","permission":"INSPECTION_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"InspectionTemplate"},
"listInspections": {"method":"GET","path":"/inspections","contract":"maintenance","summary":"List completed inspections","permission":"INSPECTION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"templateId","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"performedFrom","in":"query","required":null},{"name":"performedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"logout": {"method":"POST","path":"/auth/logout","contract":"identity","summary":"Close the current session","permission":null,"offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"submitInspection": {"method":"POST","path":"/inspections","contract":"maintenance","summary":"Submit a completed inspection","permission":"INSPECTION_SUBMIT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SubmitInspectionRequest","responds":"InspectionResult"},
"syncScans": {"method":"POST","path":"/access/scans","contract":"access","summary":"Replay scans recorded offline","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ScanSyncResult"},
"updateIncident": {"method":"PATCH","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Investigate, escalate, close or reopen an incident","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Announcement": {"type":"object","x-ticvai-persistence":"workforce.announcement","required":["title","body","kind","publishedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"type":"string","maxLength":140},"body":{"type":"string","maxLength":4000},"kind":{"$ref":"#/components/schemas/AnnouncementKind"},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresAcknowledgement":{"type":"boolean"},"deliveryChannels":{"type":"array","description":"How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n","items":{"type":"string","enum":["inApp","push"]},"default":["inApp","push"]},"expiresAt":{"type":"string","format":"date-time","nullable":true},"publishedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"publishedAt":{"type":"string","format":"date-time"},"locale":{"type":"string","nullable":true}}},
"AnnouncementKind": {"type":"string","description":"`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n","enum":["operational","safety","emergency","hr","celebration"]},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"Incident": {"x-ticvai-persistence":"maintenance.incident","type":"object","required":["id","incidentNumber","kind","severity","status","venueId","occurredAt","reportedByPrincipalId"],"properties":{"id":{"type":"string","format":"uuid"},"incidentNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"status":{"$ref":"#/components/schemas/IncidentStatus"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"locationDescription":{"type":"string","nullable":true},"isReportable":{"type":"boolean","description":"Requires notification to an external authority within a statutory window."},"notificationDueAt":{"type":"string","format":"date-time","nullable":true},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"reportedByPrincipalId":{"type":"string","format":"uuid"},"correctiveWorkOrderId":{"type":"string","format":"uuid","nullable":true},"escalation":{"type":"object","nullable":true,"readOnly":true,"description":"**Set while the incident is escalated** (the optional Escalated step of the 3 October flow; CHG-RUL-011). Screens show \"Escalated\" when `status` is `underInvestigation` and this is set. Cleared when the incident closes.\n","properties":{"toPrincipalId":{"type":"string","format":"uuid"},"byPrincipalId":{"type":"string","format":"uuid"},"reason":{"type":"string"},"escalatedAt":{"type":"string","format":"date-time"}}},"reopenCount":{"type":"integer","minimum":0,"readOnly":true,"description":"How many times the incident was reopened (CHG-RUL-011). Each reopen is a logged row."},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"IncidentAuthorityNotification": {"x-ticvai-persistence":"maintenance.incident_authority_notification","type":"object","description":"**One notification to an external authority, appended by `recordAuthorityNotification`.** An incident may be reported to more than one authority, or to the same one twice, and each is the evidence that an obligation was met — so each is a row, not an overwrite of `maintenance.incident.notified_at`.\n","required":["id","incidentId","authority","notifiedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"authority":{"type":"string","maxLength":200},"reference":{"type":"string","maxLength":128,"nullable":true},"notifiedAt":{"type":"string","format":"date-time"},"notifiedByPrincipalId":{"type":"string","format":"uuid"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentDetail": {"x-ticvai-persistence":"maintenance.incident","allOf":[{"$ref":"#/components/schemas/Incident"},{"type":"object","properties":{"description":{"type":"string","description":"The original report. Never edited — investigation adds to the record."},"investigationNote":{"type":"string","nullable":true,"readOnly":true,"description":"The latest entry of `investigationNotes`, kept for readers that show one line."},"investigationNotes":{"type":"array","readOnly":true,"description":"**Every investigation note, oldest first** (decided 28 September, audit R106 (5)). Read from `maintenance.incident_investigation_note`; appended by `updateIncident`.\n","items":{"$ref":"#/components/schemas/IncidentInvestigationNote"}},"rootCause":{"type":"string","nullable":true},"correctiveActions":{"type":"string","nullable":true},"firstAidGiven":{"type":"boolean"},"emergencyServicesCalled":{"type":"boolean"},"witnessCount":{"type":"integer"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"involvedParties":{"type":"array","description":"Who was involved, as given in `ReportIncidentRequest.involvedSubjectIds` and `involvedStaffPrincipalIds`. Read from `maintenance.incident_involved_party`.\n","items":{"$ref":"#/components/schemas/IncidentInvolvedParty"}},"authorityNotifications":{"type":"array","description":"Read from `maintenance.incident_authority_notification`, oldest first.","items":{"$ref":"#/components/schemas/IncidentAuthorityNotification"}}}}]},
"IncidentInvestigationNote": {"x-ticvai-persistence":"maintenance.incident_investigation_note","type":"object","description":"**One investigation note, appended by `updateIncident`** (decided 28 September, audit R106 (5)). A history rather than a field, so what an investigator thought on Tuesday survives what they found on Thursday.\n","required":["id","incidentId","note","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"note":{"type":"string","maxLength":10000},"kind":{"type":"string","enum":["note","statusChange","escalation","reopen"],"default":"note","description":"**Every change is logged here** (CHG-RUL-011): an investigator's note, or a row the server writes for a status change, an escalation or a reopen, with `note` as its reason.\n"},"fromStatus":{"allOf":[{"$ref":"#/components/schemas/IncidentStatus"}],"nullable":true},"toStatus":{"allOf":[{"$ref":"#/components/schemas/IncidentStatus"}],"nullable":true},"writtenByPrincipalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentInvolvedParty": {"x-ticvai-persistence":"maintenance.incident_involved_party","type":"object","description":"**One person involved in an incident, by opaque reference.** A guest or member of the public is a `pii.subject` id — personal details live there, the erasable store of ADR-0023, so the incident record survives an erasure request intact. A member of staff is a principal id. Exactly one of the two is set, as `kind` says.\n","required":["id","incidentId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["subject","staff"]},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"A `pii.subject` id where `kind` is `subject`."},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"The staff principal where `kind` is `staff`."},"role":{"type":"string","nullable":true,"enum":["injured","involved","witness","reporter",null],"description":"The person's part in the incident, from `addIncidentPerson` (CHG-RUL-013)."},"contactStored":{"type":"boolean","readOnly":true,"description":"Whether a contact is held for the person: only with their consent to be contacted (`AddIncidentPersonRequest.contactConsent`; CHG-RUL-013).\n"}}},
"IncidentKind": {"type":"string","enum":["guestInjury","staffInjury","nearMiss","propertyDamage","equipmentFailure","securityIncident","fireOrEvacuation","foodSafety","environmental","other"]},
"IncidentSeverity": {"type":"string","enum":["nearMiss","minor","moderate","major","critical"]},
"IncidentStatus": {"type":"string","enum":["reported","underInvestigation","actionRequired","closed"]},
"Inspection": {"x-ticvai-persistence":"maintenance.inspection","type":"object","required":["id","templateId","venueId","outcome","performedByPrincipalId","performedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"templateName":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"outcome":{"$ref":"#/components/schemas/InspectionOutcome"},"failedItemCount":{"type":"integer"},"failedSafetyCriticalCount":{"type":"integer"},"performedByPrincipalId":{"type":"string","format":"uuid","description":"An inspection nobody signed is not an inspection."},"performedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true},"retainUntil":{"type":"string","format":"date","nullable":true}}},
"InspectionItem": {"x-ticvai-persistence":"maintenance.inspection_item","type":"object","description":"**One answer to one question, which the API has always accepted and never stored.** `SubmitInspectionRequest.responses[]` takes a key, a value, a pass flag, a note and attachments; the only persistence ever claimed for them was `maintenance.inspection_response`, a table that does not exist.\nSo `maintenance.inspection_template_item` held the questions, `maintenance.inspection` held `failedItemCount` and `failedSafetyCriticalCount`, and **which check failed was accepted over the wire and dropped** — on a record that takes an asset out of service.\nReturned on `InspectionResult`, not on `Inspection`: `listInspections` returns the latter in a list, and twenty item rows per inspection on a list screen is the wrong trade. The counts stay for exactly that reason.\n","required":["id","inspectionId","itemKey"],"properties":{"id":{"type":"string","format":"uuid"},"inspectionId":{"type":"string","format":"uuid"},"templateItemId":{"type":"string","format":"uuid","nullable":true,"description":"**Nullable because a template changes and an inspection does not.** An answer recorded against an item that was later removed still has to be readable, so the key below is the durable record and this is the live link.\n"},"itemKey":{"type":"string","maxLength":120,"description":"The template item's `key`, copied at submission and never updated."},"label":{"type":"string","nullable":true,"description":"The question as it was asked, copied at submission. **A template reworded next season must not silently reword last season's inspection.**\n"},"value":{"nullable":true,"description":"Whatever the item's `kind` calls for — a boolean, a number, a string."},"passed":{"type":"boolean","nullable":true,"description":"Null where the item is informational rather than pass or fail."},"isSafetyCritical":{"type":"boolean","default":false,"description":"Copied from the template item at submission, for the same reason as `label`: it is what makes `failedSafetyCriticalCount` reproducible, and the template can change.\n"},"note":{"type":"string","maxLength":1000,"nullable":true},"attachmentAssetIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**A deliberate array, and the same exception as `workforce.sync_conflict.affectedAssignmentIds`**: evidence attached to this answer at the moment it was recorded. It is never queried from the other end — nobody asks which inspection items reference a photograph — and it must not change when an asset library is reorganised.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"InspectionItemKind": {"type":"string","enum":["passFail","yesNo","numeric","text","photo","signature"]},
"InspectionOutcome": {"type":"string","enum":["passed","passedWithObservations","failed"]},
"InspectionResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["inspection","consequences"],"properties":{"inspection":{"$ref":"#/components/schemas/Inspection"},"items":{"type":"array","description":"**The answers, which had nowhere to live until 20 September.** A failed safety-critical item takes an asset out of service and `consequences` below says it happened; this says which check caused it.\n","items":{"$ref":"#/components/schemas/InspectionItem"}},"consequences":{"type":"object","description":"What the submission triggered. A failed safety-critical item takes the asset out of service without waiting for anyone to decide.\n","properties":{"assetTakenOutOfService":{"type":"boolean"},"workOrdersRaised":{"type":"array","items":{"type":"string","format":"uuid"}},"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"escalatedToPrincipalId":{"type":"string","format":"uuid","nullable":true}}}}},
"InspectionTemplate": {"x-ticvai-persistence":"maintenance.inspection_template + maintenance.inspection_template_item","type":"object","required":["id","code","name","items"],"properties":{"instructions":{"type":"string","description":"**The procedure itself.** A technician asking how to isolate a chiller is asking a safety question, and the answer has to come from the template rather than from its title.\n"},"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid","nullable":true},"appliesToAssetCategoryId":{"type":"string","format":"uuid","nullable":true},"frequency":{"type":"string","enum":["preOpening","postClosing","daily","weekly","monthly","annual","adHoc"]},"items":{"type":"array","minItems":1,"items":{"type":"object","required":["key","label","kind","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"kind":{"$ref":"#/components/schemas/InspectionItemKind"},"isRequired":{"type":"boolean"},"isSafetyCritical":{"type":"boolean","default":false,"description":"A failed safety-critical item **blocks the inspection from passing** and cannot be overridden by completing the rest.\n"},"requiresPhotoOnFail":{"type":"boolean","default":true},"minValue":{"type":"number","nullable":true},"maxValue":{"type":"number","nullable":true},"guidance":{"type":"string","nullable":true}}}},"retentionYears":{"type":"integer","default":7,"description":"Compliance inspections are retained alongside the financial trail."},"isActive":{"type":"boolean"}}},
"OfflineScan": {"x-ticvai-persistence":"none — client-side journal","allOf":[{"$ref":"#/components/schemas/ValidateRequest"},{"type":"object","required":["sequence","localOutcome"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. The server processes in this order."},"localOutcome":{"allOf":[{"$ref":"#/components/schemas/ScanOutcome"}],"description":"What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"},"localDenyReason":{"$ref":"#/components/schemas/DenyReason"},"overriddenByPrincipalId":{"type":"string","format":"uuid","nullable":true},"overrideReason":{"type":"string","nullable":true}}}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"ScanSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer","description":"Entries processed before any stop."},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string"},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","reconciled","rejected"]},"serverOutcome":{"$ref":"#/components/schemas/ScanOutcome"},"divergence":{"type":"string","nullable":true,"description":"Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"SubmitInspectionRequest": {"x-ticvai-persistence":"maintenance.inspection + maintenance.inspection_item","type":"object","required":["id","templateId","venueId","responses","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"responses":{"type":"array","minItems":1,"items":{"type":"object","required":["key","value"],"properties":{"key":{"type":"string"},"value":{},"passed":{"type":"boolean","nullable":true},"note":{"type":"string","maxLength":1000},"attachmentRefs":{"type":"array","items":{"type":"string"}}}}},"signatureRef":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"ValidateRequest": {"type":"object","required":["id","mediaCode","mediaKind","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key and dedupe key."},"mediaCode":{"type":"string","maxLength":256,"description":"What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"},"mediaKind":{"$ref":"#/components/schemas/MediaKind"},"direction":{"$ref":"#/components/schemas/Direction"},"groupSize":{"type":"integer","minimum":1,"description":"For group media admitting several holders on one read."},"proximityToken":{"type":"string","description":"BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"},"recordedAt":{"type":"string","format":"date-time","description":"Device time of the read. Authoritative for ordering, not for validity."}}}
}
```
