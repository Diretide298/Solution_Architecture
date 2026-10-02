# P11-applicant-journey-01 — P11 · Applicant Journey

**5 screens · 10 operations · 5 schemas · 1 permissions**

Platform P11 Accreditation Web · ships as **ticvai-control** ·
public audience · web ·
online only

## Who this is for

**public on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `ACCREDITATION_APPLY`. A control nobody can use must say so,
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
| `ACC-001` | Landing / Programme Overview | B–D | 0 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `ACC-002` | Registration Form | B–D | 6 | 0 | 5 | 1 | 6 | 0 | — | notStarted (generated) |
| `ACC-003` | Application Review & Submit | B–D | 0 | 0 | 6 | 1 | 2 | 0 | — | notStarted (generated) |
| `ACC-004` | Application Status Tracking | B–D | 0 | 0 | 6 | 9 | 2 | 0 | — | notStarted (generated) |
| `ACC-005` | Accreditation Badge | B–D | 0 | 0 | 5 | 2 | 2 | 6 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ACC-001` Landing / Programme Overview

**Explain what accreditation at this venue is, what an application needs, and how long it takes — then offer the two ways in. **The explanation is the screen**, not a preamble to it.**

| | |
|---|---|
| App · platform | TICVAI Control · P11 Accreditation Web (web) |
| Module | Applicant Journey · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public |
| Device and orientation | This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. · LTR and RTL · light theme |
| Pattern | publicPortalLanding (compact density):  |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/applicant-journey/landing-programme-overview` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The public front door of accreditation for one tenant: an applicant (a contractor, a journalist, a sponsor's guest, a government liaison) or an organisation's coordinator learns what accreditation is, which category to apply under, what they must have ready, and how long it takes, then starts or tracks an application. It carries the tenant's brand with "Powered by TICVAI" (per VO-R15) and works in Arabic right-to-left (per VO-R10). The one thing to get right: the three turnaround numbers (time to apply, time to a decision, the closing date before the event) are stated as real values, not prose.

**Known correction pending (do not draw the wrong version)**

- **The landing links to ACC-006 Reviewer Queue** Why: The reviewer side is staff-facing and TICVAI-branded with a staff sign-in; offering it on the tenant-branded public landing mixes the two audiences. Reviewers reach ACC-006 from their own sign-in, not from this page. *(source: screens/P11-accreditation-portal.yaml#ACC-001; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"What you will need" lists a press card, the performances to cover and a commission letter** Why: That is a press-only, theatre-shaped list. The client's programme serves staff, contractors, vendors, media, VIPs, guests and government representatives, each with its own requirements; the list must come from the category's requirement rows. *(source: screens/P08-venue-back-office.yaml#BO-615 / DI-656 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **apisNote says zero operations is correct because the page is CMS content** Why: Two of the three numbers (closing date, decision time) and the "opens on" date are programme and SLA data that change per programme; as static content they will drift. listAccreditationProgrammes is staff-only, so a guest-callable read of open programmes is needed, or the CMS must be fed from the programme on publish. *(source: contracts/satellite/accreditation.yaml#listAccreditationProgrammes / DI-695; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"The cut-off before the performance"** Why: Theatre wording; the client's programmes are events, venues and seasons. Use "Applications close" with the event date. *(source: screens/P08-venue-back-office.yaml#BO-620 / DI-695; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where does "time to apply" come from, a CMS sentence per programme or a computed estimate from the form length?** → Drawn default accepted: A CMS sentence per programme, edited on BO-624. *(decided by Chinmay, 2026-10-02; DEC-362 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **programme choice**: When more than one programme is open (for example "Summit Peaks Winter Festival 2026" and "Aqua Park Contractor Scheme 2026-27"), the landing opens on a short list of programme cards, each with its event or venue, its closing date and its categories; choosing one sets the programme every later step uses. With one open programme, skip the list. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme / DI-656)*

#### Outputs: what the screen shows and produces

**Shown**

**What accreditation is, and is not** (detail panel): Programme, guidelines, and **what accreditation is not** — the section that prevents most refused applications, because the common failure is applying for the wrong thing.

**What you will need** (detail panel): Press card number if held, the performances they intend to cover, and a commission letter. **Listed before the form opens**, because an applicant who discovers on step three that they need a document from an editor abandons the application.

**How long it takes** (detail panel): Time to apply, time to a decision, and the cut-off before the performance. **Three numbers, stated** — CF and MoM both record that the absence of a stated turnaround is what generates the phone calls this screen exists to prevent.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Start an application (primary button) | navigation or local | — | — | — | — |
| Track an existing one (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **How long it takes**: Three figures in a row of equal tiles, each with a one-line label: "About 15 minutes to apply", "Decision within 5 working days", "Applications close Thu 10 Dec 2026, 18:00". The closing figure is the programme's applicationsCloseAt in venue time (per VO-R10); the decision figure is the category's approval SLA. Where categories differ (government slower than media), show a small per-category table under the tile instead of one number. *(source: DI-695 / DI-661 / MoM 2026-09-07 4.5 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **What you will need**: Per category, the requirements that apply (photograph, Emirates ID or passport, employment letter, contractor authorisation, media identification, sponsor letter), split into "Needed to submit" and "Can follow, needed before approval". State the accepted formats (PDF, JPEG, PNG) and the size limit here, and say that uploading an Emirates ID or passport fills in the identity details automatically. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements / DI-657 / DI-658)*
- **What accreditation is, and is not**: One short paragraph and the category list (Staff, Contractor, Vendor, Media, VIP, Guest, Government or authority) with one line each on who it is for; then "not a ticket: guests buying entry use the ticket shop" with a link to the tenant's web shop. Applying under the wrong category is the common refusal, so the category descriptions carry the weight. *(source: screens/P08-venue-back-office.yaml#BO-615 / screens/P08-venue-back-office.yaml#BO-619 / DI-654)*
- **Applying for a team**: A third, smaller entry beside the two buttons: "Applying for people in your organisation?" explaining that a coordinator can submit on behalf of members and that large groups use the venue's bulk template. *(source: DI-655 / DI-664 / MoM 2026-09-07 4.7)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start an application**: Signs the applicant in (email or mobile one-time code) if not already, then opens ACC-002 on the chosen programme. The application is created as a draft on the first Continue, not on this click. *(source: contracts/satellite/accreditation.yaml#createAccreditationApplication / screens/P11-accreditation-portal.yaml#ACC-002)*
- **Track an existing one**: Opens ACC-004 for the signed-in applicant, listing every application they made or that was made for them. *(source: contracts/satellite/accreditation.yaml#listMyAccreditationApplications)*

**Where the user goes next**

- → `ACC-002` Registration Form: *Registration Form*
- → `ACC-004` Application Status Tracking: *Application Status Tracking*
- → `ACC-006` Reviewer Queue: *Reviewer Queue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The programme text, from the CMS bundle. Nothing is fetched per applicant. |
| Error (`?state=error`) | **Content failed and the two actions still work.** An applicant who knows what they came to do should not be blocked by a paragraph that did not load. |
| Empty, no results (`?state=emptyNoResults`) | No programme is open. Says when the next one opens rather than showing an empty page — *"accreditation for the winter season opens 4 November"* is an answer; a blank screen is not. |
| Empty, first run (`?state=emptyFirstRun`) | No programme is open yet. Says when the next one opens rather than showing an empty page — a date is an answer, a blank screen is not. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No programme open**: Says when the next one opens ("Accreditation for the Winter Festival opens 4 Nov 2026") and keeps Track an existing one available; never a blank page. *(source: screens/P11-accreditation-portal.yaml#ACC-001)*
- **Programme closes within 48 hours**: An amber strip above the tiles, "Applications close in 1 day 4 hours", so a late applicant knows before starting a long form. *(source: designer default)*
- **A category is full (quota reached)**: The category card shows "Full - no new applications" and Start is disabled for it with that reason. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Content failed to load**: Both actions still work; the tiles show "Not available right now" rather than zero. *(source: screens/P11-accreditation-portal.yaml#ACC-001)*

#### Consistency with other screens

- Match `ACC-003`: The "What happens next" panel repeats the decision figure from this page with the same words and the same number.
- Match `BO-624`: BO-624's Preview Applicant Journey renders this page with the programme's real values before publishing; both must read the same programme fields.
- Match `P02 guest app`: The guest app is a secondary route for individual applicants (DI-693); if it offers accreditation it shows the same three numbers.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tenant: Yas Leisure Group
programme: Summit Peaks Winter Festival 2026 accreditation
turnaround:
  apply: About 15 minutes
  decision: Within 5 working days (Government or authority, 10 working days)
  closes: Thu 10 Dec 2026, 18:00
categories:
- Staff
- Contractor
- Vendor
- Media
- VIP
- Guest
- Government or authority
footer: Yas Leisure Group - Powered by TICVAI
```

#### Permissions

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The landing shows three stated turnaround numbers: time to apply, time to a decision, and the cut-off before the performance (CF and MoM record that an unstated turnaround is what generates phone calls). *(agreed · screen note 7 Sep 2026, ACC-001 · DI-695)*
- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

Also apply: 8 for all of P11, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P11 Accreditation Web.dc.html#acc-001` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ACC-001?state=<state>`: loading, error, emptyNoResults, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Start an application, Track an existing one.
- [ ] Every transition is wired: `ACC-002`, `ACC-004`, `ACC-006`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ACC-002` Registration Form

**Collect who the applicant works for, what they intend to cover, and the documents that support it — in steps, with a draft that survives leaving.**

| | |
|---|---|
| App · platform | TICVAI Control · P11 Accreditation Web (web) |
| Module | Applicant Journey · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public staff holding `ACCREDITATION_APPLY` (1 operate); in the flows as contractor |
| Device and orientation | This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. · LTR and RTL · light theme |
| Pattern | multiStepForm (compact density):  |
| Offline | online only |
| Opens with | `applicationRef` (deepLink), `applicationId` (navigation) · cold entry: **Reached from the landing page, or resumed from a link in an acknowledgement email weeks later.** A reference that no longer resolves says the programme … |
| Route | `/applicant-journey/registration-form` |

**Known gaps.** The pattern requires a draft that autosaves. **A four-step form that loses everything to a dropped connection is a form people do not come back to**, and the drawn frame offers *"Save and finish …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The application form itself, for an individual applying for themselves or a coordinator applying for a member of their organisation. Its fields are not fixed: they come from the programme's form and the requirement rows for the chosen category and applicant type. Identity comes first: the applicant uploads an Emirates ID or passport, OCR fills the identity fields, and a number already accredited is stopped there. The one thing to get right: a draft that is never lost and a form that is the category's form, not a press form.

**Known correction pending (do not draw the wrong version)**

- **Fixed press fields (Role photographer/writer/broadcast/technical, Press card number, Commissioning editor, "Coverage" step)** Why: The form must be the programme's configurable form per category (formId and requirement rows); media questions belong only to the Media category's form. A contractor or a government liaison cannot apply on this screen as drawn. *(source: screens/P08-venue-back-office.yaml#BO-617 / MATRIX 12.1.2 / DI-656 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No identity document step and no OCR** Why: Agreed on 7 September; extracted values must be stored as fields for expiry tracking and renewal prompts. *(source: DI-658 / DI-691 / TRACKER Actions row 240; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The contract has no identity document fields** Why: The identity number, issuing country and expiry live only inside the free-form subject object; there is no structured, encrypted field or blind index to check uniqueness against, which DI-691 and ADR-0063 both require. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication / ADR-0063 / DI-691; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Duplicate identity is accepted and queued as a pending conflict** Why: createAccreditationApplication accepts the application "either way" and raises a pending identity conflict; the client decided that a duplicate passport or Emirates ID submission is blocked. *(source: contracts/satellite/accreditation.yaml#createAccreditationApplication / DI-692 / TRACKER Actions row 241; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gap saveAccreditationDraft still listed** Why: Stale; drafts are served by createAccreditationApplication with status draft and updateAccreditationApplication (29 September). *(source: contracts/satellite/accreditation.yaml#updateAccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Exit edge to ACC-007 Reviewer Application Detail carrying documentId (CHG-WIR-002).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does the applicant sign in, or work only by reference?** → Drawn default accepted: Sign in with an email or mobile one-time code before step one (the contract's guest operations need it); the reference is shown for support calls. *(decided by Chinmay, 2026-10-02; DEC-363 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Can an organisation's coordinator upload the bulk Excel template in the portal, or only send it to the venue?** → Drawn default accepted: Draw only the hint text on this screen; the import itself stays on the staff side. *(decided by Chinmay, 2026-10-02; DEC-364 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Organisation | text field | — | — | — | — | Who you work for. Free text — an outlet that is not on a list is still an outlet. | — |
| Role | select field | — | — | — | — | Photographer, writer, broadcast, technical. **Drives what coverage may be requested.** | — |
| Press card number | text field | — | — | — | — | Optional, and marked so. Its absence is a reviewer's signal, not a blocker. | — |
| Commissioning editor | text field | — | — | — | — | Who commissioned the coverage, where there is one. | — |
| Supporting documents | file upload | — | — | — | — | Commission letter and badge photo. Accepted formats stated before the picker opens. | — |
| Consent | consent block | — | — | — | — | **Stated once, unticked, and collected before documents rather than after.** The 2 September session recorded consent language as a live question for face data; the same principle applies to a press … | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Category and applicant type (first step)**: Category as cards from the programme's categories (closed set, never free text), then applicant type from the programme's applicantTypes. Changing category after documents are uploaded warns "Your document list will change" and keeps uploads that still match a requirement. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme / DI-656)*
- **Applying for**: "Myself" or "A member of my organisation" (DI-655). In the second case the coordinator's organisation is fixed from their account and the identity step collects the member's details, not the coordinator's. submittedByPrincipalId is the server's, never a field (per VO-R03). *(source: DI-655 / contracts/satellite/accreditation.yaml#createAccreditationApplication)*
- **Identity document (upload, then OCR)**: Upload Emirates ID (front and back) or passport photo page as image or PDF from phone or laptop. Accepted formats and size limit are stated before the picker opens and enforced at upload. OCR fills full name, document number, nationality, date of birth and expiry; each filled field carries a small "Read from your document - please check" tag until the applicant edits or confirms it. Low-confidence fields are left empty and highlighted rather than guessed. *(source: DI-658 / DI-691 / DI-657 / MoM 2026-09-07 4.3 / TRACKER Actions row 240)*
- **Emirates ID / passport number**: Emirates ID is 15 digits shown as 784-YYYY-NNNNNNN-C with the check digit validated; passport is 6-9 letters and digits. After the step is saved the number is shown masked ("Emirates ID ending 5671") and never echoed back in full, because it is stored encrypted. *(source: ADR-0063 / DI-692)*
- **Document expiry date**: Must be in the future. If it falls before the programme's event end date, show an amber note "Your Emirates ID expires before the event; you will be asked to renew it", but allow saving. *(source: DI-663 / MoM 2026-09-07 4.6)*
- **Form fields from the programme's form**: Each requirement row of kind field renders as its fieldType (text, email, phone, date, country, number, yes/no, single choice as radio or select, multiple choice as chips). visibility mandatory shows no marker, optional shows "(optional)", conditional appears only when its condition answer is given, hidden is not drawn. Validation (pattern, length, min/max, allowed values) runs on blur with the row's label in the message. Role, press card number and similar media questions exist only where the Media category's form defines them. *(source: screens/P08-venue-back-office.yaml#BO-619 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*
- **Photograph**: A head-and-shoulders photo with an on-screen guide (plain light background, face uncovered, recent), cropped to the badge aspect; the venue's photo rules (format, minimum resolution, size) are checked at upload. *(source: screens/P08-venue-back-office.yaml#BO-628 / DI-657)*
- **Supporting documents**: One upload slot per document requirement, labelled with the requirement (Contractor authorisation, Employment letter, Sponsor letter), never a generic multi-file picker. A document with its own expiry (insurance certificate) asks for the expiry date beside the file. *(source: contracts/satellite/accreditation.yaml#submitAccreditationDocument)*
- **Consent**: Unticked, stated once, before documents: consent to process identity documents (including OCR) and the photograph, with the retention period stated. Programme declarations (kind declaration) are separate ticks on the last step. *(source: screens/P11-accreditation-portal.yaml#ACC-002 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*

#### Outputs: what the screen shows and produces

**Shown**

**Step 1 of 4 — Organisation** (progress indicator): Organisation · Coverage · Documents · Check and submit.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Continue (primary button) | navigation or local | — | — | — | — |
| Save and finish later (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **What this application needs**: A side checklist of every requirement for the category with its state: Done, Missing - needed to submit (red), Missing - can follow, needed before approval (grey). It updates as uploads land, so the applicant never discovers a blocker on the last step. *(source: contracts/satellite/accreditation.yaml#submitAccreditationApplication / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*
- **Draft reference and save state**: After the first Continue the reference appears in the header ("Draft ACR-2026-004417") with "Saved 14:02"; every Continue saves. Steps are category-driven: About you, Organisation and role, Documents, Check and submit. *(source: contracts/satellite/accreditation.yaml#updateAccreditationApplication)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Continue**: First press creates the application with status draft; later presses update it (whole application, per VO-R04) and move on. Errors stay against their fields and never clear entered values. A 409 means the application is no longer a draft (opened in another tab and submitted) and says so. *(source: contracts/satellite/accreditation.yaml#createAccreditationApplication / contracts/satellite/accreditation.yaml#updateAccreditationApplication)*
- **Save and finish later**: Saves, then a dialog "Your draft is saved. Return with reference ACR-2026-004417; we have emailed you a link." *(source: screens/P11-accreditation-portal.yaml#ACC-002)*
- **Upload a document**: Sends the file against its requirementCode (with expiresAt where asked); the slot shows Uploaded with the file name and a Replace link. A file over the size limit or in another format is refused before upload with the limit named. *(source: contracts/satellite/accreditation.yaml#submitAccreditationDocument / DI-657)*

**Where the user goes next**

- → `ACC-003` Application Review & Submit: *Application Review & Submit*; carries `applicationId`, `applicationRef`
- → `ACC-007` Reviewer Application Detail: *A reviewer checks and approves*; carries `applicationId`, `documentId`

**What opens over it**

- confirmDialog *Save and finish later*: **Says what is kept and how to get back.** *"Your draft is saved. Return with reference ACC-4417"* — a dialog that says only *"saved"* leaves the applicant with nothing to return with.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The draft, where one exists. |
| Empty, first run (`?state=emptyFirstRun`) | A new application. Step one, nothing prefilled except what the account knows. |
| Error (`?state=error`) | **The draft is safe and the step is not lost.** Errors on a long form must never clear entered fields. |
| Denied (`?state=denied`) | The programme is closed. Says when it reopens. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The application is not draft or informationRequested; 422 A subject field fails its requirement row's fieldType or validation; 422 Submitted with a requirement that blocks submission unsatisfied |

#### Edge cases to draw

- **Emirates ID or passport already accredited**: Blocked on the identity step: "An accreditation with this Emirates ID already exists. Sign in with the account that holds it, or contact the accreditation team." It does not say whose record it is. *(source: DI-692 / DI-659 / MoM 2026-09-07 4.4)*
- **OCR cannot read the document**: "We could not read this clearly" with the reason (blurred, cut off, too small) and the option to retake or type the details by hand. *(source: DI-657 / DI-658)*
- **Programme closes while the draft is open**: The draft stays readable; Continue and Submit are disabled with "Applications closed on 10 Dec 2026, 18:00". *(source: screens/P11-accreditation-portal.yaml#ACC-002 / contracts/satellite/accreditation.yaml#submitAccreditationApplication)*
- **Category quota fills while drafting**: Says so at the next Continue and offers another open category where the programme allows it. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Coordinator with many members**: After the second application from the same coordinator, a hint "Applying for 10 or more people? Ask for the bulk template." *(source: DI-664)*

#### Consistency with other screens

- Match `BO-617`: The staff "New Accreditation Application" renders the same form from the same programme form and requirement rows; one form renderer, two shells.
- Match `BO-627`: Identity field names, the masked number format and the OCR "please check" tag are the same on the staff identity tab.
- Match `BO-622`: Requirement labels and the submit/approval split shown here come from BO-622's matrix rows, word for word.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programme: Summit Peaks Winter Festival 2026 accreditation
category: Contractor
applicantType: Rigging crew
organisation: Falcon Stage Rigging LLC
applicant:
  name: Rahul Menon
  nationality: India
  dateOfBirth: 14 Mar 1991
  document: Emirates ID ending 5671
  documentExpiry: 02 Feb 2027
requirements:
- label: Photograph
  state: Done
- label: Emirates ID or passport
  state: Done
- label: Contractor authorisation
  state: Missing - needed to submit
- label: Safety induction certificate
  state: Missing - needed before approval
reference: ACR-2026-004417
```

#### Permissions

- `createAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `submitAccreditationDocument` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `updateAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest

**A refused user sees:** The programme is closed. Says when it reopens.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.2 | Accreditation Registration System shall support accreditation applications through configurable forms. | Accreditation & Credential Management | CONTRACTED | `updateAccreditationApplication` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Uniqueness is enforced on passport and Emirates ID; a duplicate submission is blocked. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-692)*
- Identity documents are OCR'd to auto-populate the accreditation form, and extracted data is kept as fields (for expiry tracking and renewal prompts). *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-691)*
- Allam asked, Chinmay confirmed: uploading an ID (e.g. Emirates ID image or PDF from phone or laptop) auto-fills form fields (ID number, expiry) via OCR; data is stored as structured fields to track expiry and prompt renewal. *(agreed · MoM 7 Sep 2026, 4.3 OCR Auto-Fill / 5. Key Decisions · DI-658)*
- Submission tracking shows submitted, pending and missing-document applications. Upload accepts PDF, JPEG, PNG and enforces file-size/quality limits at upload time. *(client request · MoM 7 Sep 2026, 4.3 Application Requirements, Document Validation & OCR Auto-Fill · DI-657)*
- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*
- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

Also apply: 8 for all of P11, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P11 Accreditation Web.dc.html#acc-002` · status **notStarted** · provenance generated
- Flow F23 *A contractor gets a badge and uses it*, step 1: Applies with documents and a photo → Identity, company, what access is needed
- Flow F23 branch at step 1 (requiresStaff): when The sponsor company is not registered, Blocks. A contractor with no sponsor is a person with no accountable employer, and that is the point of accreditation.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ACC-002?state=<state>`: loading, emptyFirstRun, error, denied, offline.
- [ ] Every action is wired with its success and its failure: Continue, Save and finish later.
- [ ] Every transition is wired: `ACC-003`, `ACC-007`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ACC-003` Application Review & Submit

**Show everything the applicant entered, let them change any of it, say what happens next, and submit.**

| | |
|---|---|
| App · platform | TICVAI Control · P11 Accreditation Web (web) |
| Module | Applicant Journey · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public staff holding `ACCREDITATION_APPLY` (1 operate) |
| Device and orientation | This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. · LTR and RTL · light theme |
| Pattern | multiStepForm (compact density):  |
| Offline | online only |
| Opens with | `applicationRef` (ACC-002), `applicationId` (navigation) · cold entry: **Cannot be reached cold and should not be.** Opened directly, it loads the draft behind the reference or says the reference is unknown. |
| Route | `/applicant-journey/application-review-and-submit` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): By step four a draft already exists; Submit calls submitAccreditationApplication only, and creating again would make a second application (design-notes …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The last step: the applicant sees every answer and document, fixes any one through a Change link, learns what happens next and when, and submits. Submission is where requirements that block submission are enforced, so this screen must show those blockers before the button is pressed, not after.

**Known correction pending (do not draw the wrong version)**

- **"Coverage requested: named performances and named areas, stalls, pit"** Why: Theatre and press wording, and the application has no requested-areas field; access is granted by the reviewer as an access profile. Show requested access only where the category's form asks for it. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication / contracts/satellite/accreditation.yaml#decideAccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): createAccreditationApplication is bound to "Submit the reviewed application" alongside submitAccreditationApplication (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does the applicant choose the zones they need, or does the reviewer decide them from the category alone?** → Drawn default accepted: The applicant does not choose; the badge shows what was granted. *(decided by Chinmay, 2026-10-02; DEC-365 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Declarations**: Each programme declaration (kind declaration, for example "The information I have given is true") is an unticked checkbox above Submit; Submit is disabled until all mandatory ones are ticked. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*

#### Outputs: what the screen shows and produces

**Shown**

**Step 4 of 4 — Check and submit** (progress indicator)

**Organisation** (detail panel): **Every answer, each with its own Change link back to the step that owns it.** *Change*, not *Back* — an applicant on step four wants to fix one field, not walk backwards through three.

**Coverage requested** (detail panel): Named performances and named areas — *"stalls, pit"*. **Coverage is specific, and that is the point**: a badge that says *press* and nothing else is a badge a steward cannot act on, which is the same decision `ACC-005` renders.

**Documents** (detail panel): Each file with its accepted-or-not state, so a rejected upload is visible before submit.

**What happens next** (detail panel): An acknowledgement immediately, a decision within a stated number of working days. **Set before submit, not after** — this is where the expectation is formed.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit application (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Answers by step**: Grouped as the steps were (About you, Organisation and role, Documents), each answer with its own Change link; an answer left empty reads "Not given", never blank. Identity numbers stay masked. *(source: screens/P11-accreditation-portal.yaml#ACC-003 / ADR-0063)*
- **Requirements summary**: At the top: unmet requirements that block submission in red with Fix links ("Contractor authorisation - needed to submit"); unmet requirements that only block approval in grey ("Safety induction - you can submit; the reviewer will need it before approving"). *(source: contracts/satellite/accreditation.yaml#submitAccreditationApplication)*
- **What happens next**: "We will email you now to confirm. A decision is due by Sun 18 Oct 2026. We will tell you by email and SMS at each change: approved, not approved, or more information needed." *(source: DI-663 / DI-695 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Submit application**: Confirmation names the programme and category and says the application can no longer be edited, only withdrawn. On success opens ACC-004 with the reference. A 422 lists the unmet requirement labels with Fix links; a 409 says the programme closed. *(source: contracts/satellite/accreditation.yaml#submitAccreditationApplication)*
- **Change**: Opens the owning step of ACC-002 with the field focused; saving returns here. *(source: contracts/satellite/accreditation.yaml#updateAccreditationApplication)*

**Where the user goes next**

- → `ACC-002` Registration Form: *Registration Form*; carries `applicationId`, `applicationRef`
- → `ACC-004` Application Status Tracking: *Application Status Tracking*; carries `applicationId`, `applicationRef`

**What opens over it**

- confirmDialog *Submit application*: Names what is being submitted and that it cannot be edited afterwards, only withdrawn.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The completed draft. |
| Error (`?state=error`) | **Submission failed and nothing was lost.** The application stays a draft and the button stays available. |
| Denied (`?state=denied`) | The programme closed while the application was open. Says so plainly. |
| Empty, no results (`?state=emptyNoResults`) | No draft to review. Sends the applicant to `ACC-002` rather than showing an empty summary. |
| Empty, first run (`?state=emptyFirstRun`) | No draft to review. Sends the applicant to ACC-002 rather than showing an empty summary. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not a draft, or the programme's application window is closed; 409 The application is not draft or informationRequested; 422 A requirement that blocks submission is not satisfied; 422 A subject field fails its requirement row's fieldType or validation |

#### Edge cases to draw

- **Double press on Submit**: The second press does nothing visible (idempotent); one application, one acknowledgement. *(source: contracts/satellite/accreditation.yaml#submitAccreditationApplication)*
- **Duplicate identity found only at submit**: Same block message as on ACC-002, with a link back to the identity step. *(source: DI-692)*
- **Programme closed while open**: The page says so plainly; the draft remains readable from ACC-004. *(source: screens/P11-accreditation-portal.yaml#ACC-003)*

#### Consistency with other screens

- Match `ACC-001`: The decision date wording and value match the landing's decision tile.
- Match `ACC-004`: The first timeline entry on ACC-004 is "Submitted" with this moment's time.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reference: ACR-2026-004417
decisionDue: Sun 18 Oct 2026
unmetBlockingSubmission: []
unmetBlockingApproval:
- Safety induction certificate
```

#### Permissions

- `submitAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `updateAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest

**A refused user sees:** The programme closed while the application was open. Says so plainly.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.2 | Accreditation Registration System shall support accreditation applications through configurable forms. | Accreditation & Credential Management | CONTRACTED | `updateAccreditationApplication` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Uniqueness is enforced on passport and Emirates ID; a duplicate submission is blocked. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-692)*
- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*

Also apply: 8 for all of P11, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P11 Accreditation Web.dc.html#acc-003` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ACC-003?state=<state>`: loading, error, denied, emptyNoResults, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Submit application.
- [ ] Every transition is wired: `ACC-002`, `ACC-004`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ACC-004` Application Status Tracking

**Tell an applicant where their application is and when they will hear — **with a date, not a queue position.****

| | |
|---|---|
| App · platform | TICVAI Control · P11 Accreditation Web (web) |
| Module | Applicant Journey · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public staff holding `ACCREDITATION_APPLY` (1 operate) |
| Device and orientation | This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. · LTR and RTL · light theme |
| Pattern | statusTracker (compact density):  |
| Offline | online only |
| Opens with | `applicationRef` (deepLink), `applicationId` (navigation) · cold entry: **This screen is always reached cold** — from an acknowledgement email, usually weeks later and often on a different device. That is the design, and it is why … |
| Route | `/applicant-journey/application-status-tracking` |

**Known gaps.** **A status screen with no status read.** The screen declared no operation. It also cannot use the reviewer's `listApprovalRequests`: an applicant is not authenticated as a principal with approval … The screen offers *Add a document* — the common reviewer request — and nothing performs it.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where an application stands and when a decision is due, read by the applicant (or the coordinator who applied for them) often weeks later on another device. It is also where an applicant answers a request for more information, resubmits after a refusal, or withdraws. The one thing to get right: a date ("Decision expected by 18 Oct"), never a queue position, and a clear next action when the venue is waiting on the applicant.

**Known correction pending (do not draw the wrong version)**

- **Components bind to ApprovalRequest.status, ApprovalRequest.decisions, ApprovalRequest.summary and slaDueAt** Why: An applicant cannot read approvals; the screen reads AccreditationApplication (status, decisionDueAt, missingRequirements, decisionReason) from listMyAccreditationApplications. *(source: contracts/satellite/accreditation.yaml#listMyAccreditationApplications; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gaps getAccreditationApplicationByReference and addAccreditationDocument still listed** Why: Stale since 29 September; listMyAccreditationApplications and submitAccreditationDocument serve them. *(source: contracts/satellite/accreditation.yaml#listMyAccreditationApplications / contracts/satellite/accreditation.yaml#submitAccreditationDocument; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"The reference is the credential" and "always reached cold, it takes only the reference"** Why: The only applicant read is guest-authenticated and scoped to the caller; there is no read by reference. Either the screen requires sign-in (the reference only identifies which application) or a reference read is added. *(source: contracts/satellite/accreditation.yaml#listMyAccreditationApplications / screens/P11-accreditation-portal.yaml#ACC-004; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only Add a document and Withdraw are drawn** Why: Resubmit after a return or refusal and amending answers are bound operations with no control on the screen. *(source: contracts/satellite/accreditation.yaml#resubmitAccreditationApplication / contracts/satellite/accreditation.yaml#updateAccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does a company's main account see applications submitted by its sub-accounts?** → Drawn default accepted: Draw "Applications by my organisation" as a filter that is present but greyed with "Coming with organisation accounts". *(decided by Chinmay, 2026-10-02; DEC-366 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listMyAccreditationApplications` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Note to the reviewer (when sending back)**: Required, up to 1,000 characters, "What did you change?"; it is what the reviewer reads first on the returned application. *(source: contracts/satellite/accreditation.yaml#resubmitAccreditationApplication)*
- **Withdrawal reason**: Optional, up to 500 characters, with suggestions (Assignment cancelled, Applied under the wrong category, Duplicate). *(source: contracts/satellite/accreditation.yaml#withdrawAccreditationApplication)*

#### Outputs: what the screen shows and produces

**Shown**

**With a reviewer** (banner): Where it is now, and **the date a decision is due** — `ApprovalRequest.slaDueAt`. *"Fourth in the queue"* was considered and rejected on the frame: a position moves backwards and a date does not.

**Where it has been** (timeline): Received, documents checked, decision — each with its date.

**Application** (detail panel): The reference, the performances, and what was requested.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add a document (secondary button) | navigation or local | — | — | — | — |
| Withdraw this application (destructive button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Status banner**: Plain words per status: Draft "Not sent yet", submitted "Received", underReview "With a reviewer", informationRequested "We need something from you" (amber, lists missingRequirements by label), approved "Approved" (green, link to the badge), rejected "Not approved" with decisionReason and the route back, withdrawn, expired. Under it the decision date from decisionDueAt; past that date, "Taking longer than expected" and the accreditation desk contact. *(source: contracts/satellite/accreditation.yaml#listMyAccreditationApplications / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication)*
- **My applications**: When the person has several (a coordinator who applied for twelve members), a list first: name, category, status chip, decision due, sorted by those needing action first; tapping opens the detail. Cursor paging. *(source: contracts/satellite/accreditation.yaml#listMyAccreditationApplications / DI-660)*
- **Where it has been**: Received, decision (and resubmitted, where it happened), each with date and time in venue time. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add a document**: Shown only for informationRequested; opens an upload pre-set to the requirement asked for; the requirement turns Done. *(source: contracts/satellite/accreditation.yaml#submitAccreditationDocument)*
- **Change my answers**: Shown only for informationRequested; opens the relevant ACC-002 step; any other status returns 409 and the button is not offered. *(source: contracts/satellite/accreditation.yaml#updateAccreditationApplication)*
- **Send back to the reviewer**: From informationRequested, the same application returns to submitted with the note; from rejected, a new application linked to the refused one is created and opened (the refusal stays in the record). *(source: contracts/satellite/accreditation.yaml#resubmitAccreditationApplication / MATRIX 12.1.33)*
- **Withdraw this application**: Allowed from draft, submitted, underReview or informationRequested; confirmation says it is final. A decided application shows no Withdraw. *(source: contracts/satellite/accreditation.yaml#withdrawAccreditationApplication)*
- **View my badge**: Shown when approved and a credential exists; opens ACC-005. *(source: screens/P11-accreditation-portal.yaml#ACC-005)*

**Data it reads**: `listMyAccreditationApplications` (onLoad, The applicant's own applications, status, what is missing …)

**Where the user goes next**

- → `ACC-005` Accreditation Badge: *Accreditation Badge*; carries `applicationRef`, `holderId`

**What opens over it**

- confirmDialog *Withdraw this application*: **States that withdrawal is final and the programme may close before a new application can be made.** A withdrawal that can be made by accident is one the venue hears about by telephone.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The application behind the reference. |
| Empty, no results (`?state=emptyNoResults`) | **The reference is not recognised.** Says so without hinting whether it once existed — a status endpoint that distinguishes *never existed* from *withdrawn* is an enumeration oracle. |
| Error (`?state=error`) | Could not load. The reference is unaffected and can be retried. |
| Denied (`?state=denied`) | The reference has expired. Applications are readable for a stated period after the season. |
| Empty, first run (`?state=emptyFirstRun`) | No application behind this reference yet — a reference issued but not submitted. Points back at the draft. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not informationRequested or rejected, or the programme's window is closed; 409 The application is already decided, withdrawn or expired; 409 The application is not draft or informationRequested; 422 A requirement that blocks submission is still not satisfied |

#### Edge cases to draw

- **Identity document expires before the event**: An amber notice "Your Emirates ID expires on 02 Feb 2027, before the event ends. Upload the renewed one by 01 Feb or your credential will be blocked." *(source: DI-663 / MoM 2026-09-07 4.6)*
- **Reviewer decides while the applicant is uploading**: The upload is kept; the banner refreshes to the decision and the upload is listed as "Received after the decision". *(source: designer default)*
- **Unknown or foreign reference**: "We could not find this application" without saying whether it ever existed. *(source: screens/P11-accreditation-portal.yaml#ACC-004)*

#### Consistency with other screens

- Match `BO-640`: The decision reason the applicant reads here is the applicant-visible explanation written on BO-640/BO-636; internal comments never appear here.
- Match `ACC-003`: Decision date wording is the same.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
applications:
- reference: ACR-2026-004417
  holder: Rahul Menon
  category: Contractor
  status: We need something from you
  missing:
  - Safety induction certificate
  decisionDue: 18 Oct 2026
- reference: ACR-2026-004421
  holder: Maria Santos
  category: Contractor
  status: With a reviewer
  decisionDue: 19 Oct 2026
- reference: ACR-2026-004388
  holder: Omar Haddad
  category: Contractor
  status: Approved
  decided: 09 Oct 2026
```

#### Permissions

- `listMyAccreditationApplications` → `ACCREDITATION_APPLY` (operate) · guest
- `withdrawAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `submitAccreditationDocument` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `updateAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `resubmitAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest

**A refused user sees:** The reference has expired. Applications are readable for a stated period after the season.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.2 | Accreditation Registration System shall support accreditation applications through configurable forms. | Accreditation & Credential Management | CONTRACTED | `updateAccreditationApplication` |
| 12.1.33 | Accreditation Rejection Management - System shall support rejection and resubmission workflows. | Accreditation & Credential Management | CONTRACTED | `resubmitAccreditationApplication` |
| 11.1.10 | Out-of-Office Routing - System shall automatically reroute approvals when approvers are unavailable. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.28 | Mobile Approvals - System shall support approval actions through mobile applications. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.29 | Email-Based Approvals - System shall support approval actions through email links. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.54 | Approval Reopening - System shall support reopening previously completed approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.73 | AI Risk Assessment - System shall provide AI-generated risk assessments for approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.75 | AI Escalation Recommendations - System shall recommend escalation actions based on approval patterns. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.78 | Shared Service Approval Centers - System shall support centralized approval processing teams. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Lifecycle: activation, expiry, renewal, suspension; if a document (e.g. Emirates ID) expires before the event, a resubmission request is raised and the credential is blocked if unresolved. Applicants are notified at each status change (approved, rejected, needs validation). *(client request · MoM 7 Sep 2026, 4.6 / 4.7 Lifecycle & Notifications · DI-663)*
- Submission tracking shows submitted, pending and missing-document applications. Upload accepts PDF, JPEG, PNG and enforces file-size/quality limits at upload time. *(client request · MoM 7 Sep 2026, 4.3 Application Requirements, Document Validation & OCR Auto-Fill · DI-657)*

Also apply: 8 for all of P11, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P11 Accreditation Web.dc.html#acc-004` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ACC-004?state=<state>`: loading, emptyNoResults, error, denied, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Add a document, Withdraw this application.
- [ ] Every transition is wired: `ACC-005`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ACC-005` Accreditation Badge

**Present the issued badge so it can be scanned, and say exactly where it is valid.**

| | |
|---|---|
| App · platform | TICVAI Control · P11 Accreditation Web (web) |
| Module | Applicant Journey · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public staff holding `ACCREDITATION_APPLY` (1 operate); in the flows as contractor |
| Device and orientation | This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. · LTR and RTL · light theme |
| Pattern | credentialView (touchLarge density):  |
| Offline | **Serves the cached badge and says so.** A badge that will not render without a network is a badge that fails at the door it was issued for. |
| Opens with | `applicationRef` (ACC-004), `credentialId` (navigation), `holderId` (navigation) · cold entry: Opened from a bookmark or a wallet pass. Loads the badge behind the reference, or explains that badges are issued only after approval. |
| Route | `/applicant-journey/accreditation-badge` |

**Known gaps.** The screen shows one badge and the only read is a list. **A holder opening their own badge should not fetch every badge issued** — and `listAccreditationBadges` carries a reviewer's permission, which …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The holder's own credential, presented at a gate or a service door and read by a steward. It shows the scannable code large, the photo and name a steward compares, the category colour that matches the printed badge, the zones it opens and, as plainly, that every other area is refused. The one thing to get right: a revoked, suspended, replaced or expired credential never shows a scannable code and never looks like it is loading.

**Known correction pending (do not draw the wrong version)**

- **Components bind to AccreditationBadge, AccreditationBadge.zones, expiresAt, state and revokedReason** Why: There is no AccreditationBadge; the schema is AccreditationCredential (status, no zones, no revoked reason). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gap getAccreditationBadge still listed** Why: Stale; listMyAccreditationCredentials serves the holder's own credentials. *(source: contracts/satellite/accreditation.yaml#listMyAccreditationCredentials; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listMyAccreditationCredentials promises category, validity and effective zones** Why: Its items are AccreditationCredential, which carries none of them; the "Where it works" and "Valid until" panels have nothing to bind. *(source: contracts/satellite/accreditation.yaml#listMyAccreditationCredentials / contracts/satellite/accreditation.yaml#/components/schemas/HolderAccess; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Offline is required" on a platform declared offlineCapable false** Why: A web page cannot promise an offline badge; the wallet pass is the offline answer and should be the primary action. *(source: screens/P11-accreditation-portal.yaml#ACC-005; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Sample "Photographer - The Northern Review" and "stage door, stalls and pit, named performances"** Why: Theatre and press world; use the venue world of VO-R17 and a non-press category so designers do not build a press-only badge. *(source: screens/P08-venue-back-office.yaml#BO-644; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **May a holder print their own QR credential, or does the venue require a printed badge from the desk?** → Drawn default accepted: Print shown for QR credentials only. *(decided by Chinmay, 2026-10-02; DEC-367 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listMyAccreditationCredentials` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Your badge** (credential display): The scannable credential, rendered large and bright. **Offline is required** — a stage door is the worst signal in the building, and the 2 September decision that a dynamic-QR ticket is redirected into the app exists for exactly this reason.

**Holder** (detail panel): Name, role and outlet, as printed. Photographer · The Northern Review.

**Where it works** (detail panel): **Stage door, stalls and pit, named performances — and *any other door, refused*.** The negative case is stated on the badge because the steward reads this, not a policy.

**Valid until** (banner): **`expired` and `revoked` must be unmistakable and must not resemble `loading`.** `AccreditationBadge.state` carries both, and `revokedReason` says why.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add to phone (secondary button) | navigation or local | — | — | — | — |
| Print (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **The code**: Rendered from encodedIdentifier in its symbology (QR by default), at least 60 percent of the screen width with a quiet zone, on white even in dark mode, with "Turn your screen brightness up" once. *(source: contracts/satellite/accreditation.yaml#listMyAccreditationCredentials / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential)*
- **Holder strip**: Photo, full name in English and Arabic, organisation, category with the same colour stripe as the printed badge, accreditation number, valid from and to. *(source: screens/P08-venue-back-office.yaml#BO-649 / contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate)*
- **Where it works**: The granted zones by name, with time windows where the access profile has them ("Backstage, 08:00-23:00 build and show days"), then one line "All other areas: not permitted". *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccessProfile / DI-662)*
- **Status panel**: For revoked, suspended, replaced, lost or expired: no code; a full-width panel in the status colour with the word, the date and what to do ("Replaced on 12 Oct; use your new badge", "Suspended - contact the accreditation desk"). *(source: contracts/satellite/accreditation.yaml#listMyAccreditationCredentials / screens/P11-accreditation-portal.yaml#ACC-005)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add to Apple Wallet / Add to Google Wallet**: Shows the button for the device's platform (both on desktop); the pass updates itself when the accreditation is suspended, revoked, renewed or replaced. Only for issued or active mobile or QR credentials. *(source: contracts/satellite/accreditation.yaml#issueMyAccreditationWalletPass)*
- **Print**: Only for a QR credential; prints the code with name and validity on one page. A printed badge holder sees "Collect your badge at the accreditation desk" instead. *(source: DI-662 / MoM 2026-09-07 4.6)*
- **Renew**: Shown only inside the renewal window; opens a prefilled renewal application, or renews at once where the programme does not require re-checking, and says which happened. *(source: contracts/satellite/accreditation.yaml#renewAccreditation / MATRIX 12.1.37)*

**Data it reads**: `listMyAccreditationCredentials` (onLoad, The holder's own credentials with encodedIdentifier …)

**Where the user goes next**

- → `ACC-004` Application Status Tracking: *Application Status Tracking*; carries `applicationRef`
- → `SCN-003` Ready to scan: *A steward scans it at a service gate*; calls `listMyAccreditationCredentials`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The badge. |
| Empty, no results (`?state=emptyNoResults`) | No badge yet — the application has not been approved. Points at `ACC-004`. |
| Error (`?state=error`) | Could not refresh. **The cached badge still displays and says when it was last checked.** |
| Offline (`?state=offline`) | **Serves the cached badge and says so.** A badge that will not render without a network is a badge that fails at the door it was issued for. |
| Empty, first run (`?state=emptyFirstRun`) | No badge issued yet. The application has not been approved; points at ACC-004. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Outside the renewal window, the holder is revoked, suspended or archived, or a renewal is already open; 409 The credential is not a mobile or QR credential, or is not issued or active |

#### Edge cases to draw

- **No network at the door**: The portal is a website and is not offline-capable; the reliable offline route is the wallet pass, so the page pushes "Add to Wallet" after first view. A page already open shows the last code with "Last checked 14:05". *(source: screens/P11-accreditation-portal.yaml#ACC-005 / contracts/satellite/accreditation.yaml#issueMyAccreditationWalletPass)*
- **Holder has a printed badge and a mobile credential**: Two tabs, Mobile and Printed; the printed one shows its serial number only, not a code. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationCredential)*
- **Not approved yet**: Points to ACC-004 with the decision date. *(source: screens/P11-accreditation-portal.yaml#ACC-005)*

#### Consistency with other screens

- Match `SCN-003`: The steward's verification (verifyAccreditationCredential) shows the same photo, name, organisation, category and zones; the words "not permitted" match.
- Match `BO-647`: Category colour and the fields shown mirror the badge template so a printed and a mobile badge look like the same credential.
- Match `BO-649`: BO-649's "configurable information" list is what this screen shows.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holder:
  name: Rahul Menon
  nameAr: راهول مينون
  organisation: Falcon Stage Rigging LLC
  category: Contractor
  stripe: Orange
  accreditationNumber: SP26-CON-00318
credential:
  kind: mobileCredential
  symbology: qr
  status: active
  validFrom: 01 Dec 2026
  validTo: 14 Dec 2026
zones:
- Main stage build area, 06:00-22:00
- Loading dock
- Crew catering
```

#### Permissions

- `listMyAccreditationCredentials` → `ACCREDITATION_APPLY` (operate) · guest
- `issueMyAccreditationWalletPass` → `ACCREDITATION_APPLY` (operate) · guest
- `renewAccreditation` → `ACCREDITATION_APPLY` (operate) · staff, guest

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.21 | Digital Credentials - System shall support mobile accreditation credentials. | Accreditation & Credential Management | CONTRACTED | `listMyAccreditationCredentials` |
| 12.1.37 | Accreditation Renewal - System shall support accreditation renewal workflows. | Accreditation & Credential Management | CONTRACTED | `renewAccreditation` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*
- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

Also apply: 8 for all of P11, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P11 Accreditation Web.dc.html#acc-005` · status **notStarted** · provenance generated
- Flow F23 *A contractor gets a badge and uses it*, step 3: The badge is issued → QR, NFC or printed — `MediaKind` already covers all four
- Flow F23 branch at step 3 (requiresStaff): when The badge is lost, Reissued, and the old one blacklisted. **Both must happen** — reissuing without revoking leaves two valid badges.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ACC-005?state=<state>`: loading, emptyNoResults, error, offline, emptyFirstRun.
- [ ] Every action is wired with its success and its failure: Add to phone, Print.
- [ ] Every transition is wired: `ACC-004`, `SCN-003`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P11 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for forms and finish.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for the reviewer screens' density.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P11 as a whole** (6: 0 open, 6 closed). Open first; a closed row says where it went on 30 September.

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker)*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker)*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker)*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker)*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker)*
- **C45** Share accreditation, entitlements and virtual queue documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 7 Sep 2026 · workshop tracker)*

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

### Across P11 Accreditation Web

- The web portal is the primary channel for accreditation; the mobile app is a secondary route for individual applicants. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-693)*
- Accreditation is primarily completed in the web portal (document upload and photo checks suit a larger screen); the same submission is also available in the guest mobile app as a secondary option for individuals. *(agreed · MoM 7 Sep 2026, 4.8 Accreditation Channel Placement & API Access · DI-666)*
- Bulk: a company with many members (e.g. 1,000) gets an Excel template to submit all details and documents at once; each imported record still goes through profile, documents and approval. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-664)*
- A main account holder (company/agent) sees the status of every application under their organisation (approved, rejected, requires resubmission), whether the credential is collected physically or sent as a soft copy by email. *(client request · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-660)*
- The venue creates a partner/company account (main or sub-accounts) whose users log in and submit accreditation for their members; entry can be done by the end user or by the admin team on their behalf. *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-655)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**14 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAccreditationApplication": {"method":"POST","path":"/accreditation-applications","contract":"accreditation","summary":"Apply, or apply on behalf of somebody","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationApplication","responds":"AccreditationApplication"},
"issueMyAccreditationWalletPass": {"method":"POST","path":"/my/accreditation-credentials/{credentialId}/wallet-pass","contract":"accreditation","summary":"Put my accreditation credential in Apple or Google Wallet","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationCredentialDelivery"},
"listMyAccreditationApplications": {"method":"GET","path":"/my/accreditation-applications","contract":"accreditation","summary":"The applications this person made, or that were made for them","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyAccreditationCredentials": {"method":"GET","path":"/my/accreditation-credentials","contract":"accreditation","summary":"The credentials this person holds, with where each is valid","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"renewAccreditation": {"method":"POST","path":"/accreditation-holders/{holderId}/renew","contract":"accreditation","summary":"Renew a holder's accreditation for another period","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"resubmitAccreditationApplication": {"method":"POST","path":"/accreditation-applications/{applicationId}/resubmit","contract":"accreditation","summary":"Send an application back after a return for information or a rejection","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"submitAccreditationApplication": {"method":"POST","path":"/accreditation-applications/{applicationId}/submit","contract":"accreditation","summary":"Send a draft for review","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"submitAccreditationDocument": {"method":"POST","path":"/accreditation-documents","contract":"accreditation","summary":"Supply a document against a requirement","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationDocument","responds":"AccreditationDocument"},
"updateAccreditationApplication": {"method":"PUT","path":"/accreditation-applications/{applicationId}","contract":"accreditation","summary":"Save a draft, or amend an application returned for information","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationApplication","responds":"AccreditationApplication"},
"withdrawAccreditationApplication": {"method":"POST","path":"/accreditation-applications/{applicationId}/withdraw","contract":"accreditation","summary":"Withdraw an application before it is decided","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationApplication": {"type":"object","x-ticvai-persistence":"accreditation.application","description":"Board 1.3. **Usually submitted by an organisation on behalf of its people.**","required":["programmeId"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"applicantType":{"type":"string"},"submittedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"subject":{"type":"object","additionalProperties":true,"description":"Name, date of birth, nationality, contact — shaped by the requirements matrix."},"requirementStatus":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"requirementCode":{"type":"string"},"satisfied":{"type":"boolean"},"documentId":{"type":"string","format":"uuid","nullable":true}}}},"status":{"type":"string","enum":["draft","submitted","underReview","informationRequested","approved","rejected","withdrawn","expired"]},"decisionReason":{"type":"string","nullable":true},"missingRequirements":{"type":"array","readOnly":true,"description":"The requirement codes a reviewer returned the application for, or rejected it over — what the applicant must change before resubmitting","items":{"type":"string"}},"decisionDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a decision is due — the approvals request's SLA. **A date, not a queue position**"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"holderId":{"type":"string","format":"uuid","nullable":true},"renewsHolderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.37. Set by `renewAccreditation`; approval extends this holder rather than creating one"},"resubmissionOfApplicationId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.33. The rejected application this one resubmits, so the rejection stays in the record"},"resubmissionNote":{"type":"string","maxLength":1000,"nullable":true,"readOnly":true,"description":"What the applicant changed, from `resubmitAccreditationApplication`"},"submittedAt":{"type":"string","format":"date-time","nullable":true},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"AccreditationCredential": {"type":"object","x-ticvai-persistence":"accreditation.credential","description":"Board 4. **Not the accreditation** — reissuing one re-vets nobody.","required":["holderId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["printedBadge","mobileCredential","qr","nfcCard","rfidCard","wristband"]},"symbology":{"type":"string","nullable":true,"description":"12.1.22. **How `encodedIdentifier` is carried**, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a `mobileCredential`, a barcode where a printed badge carries one, `nfcNdef` or `rfidEpc` for an encoded card, `none` where nothing is encoded.\n","enum":["qr","dataMatrix","pdf417","aztec","code128","nfcNdef","rfidEpc","none"]},"serialNumber":{"type":"string","nullable":true},"encodedIdentifier":{"type":"string","nullable":true},"badgeTemplateId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"issuedBy":{"type":"string","format":"uuid"},"activatedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["pendingPrint","issued","active","lost","replaced","revoked","expired"]},"replacesCredentialId":{"type":"string","format":"uuid","nullable":true},"replacementCount":{"type":"integer","default":0},"scopePath":{"type":"string"}}},
"AccreditationCredentialDelivery": {"type":"object","x-ticvai-persistence":"accreditation.mobile_credential_delivery","description":"12.1.21. **Issuing a mobile credential and getting it onto a phone are two acts**, and the second is recorded so *\"I never got it\"* has an answer. Written by `deliverAccreditationCredential` (the accreditation team sends it) and `issueMyAccreditationWalletPass` (the holder adds it to a wallet).\n","required":["credentialId","channel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"credentialId":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid","readOnly":true},"channel":{"type":"string","enum":["email","sms","holderApp","appleWallet","googleWallet"]},"destinationMasked":{"type":"string","nullable":true,"readOnly":true,"description":"The address or number used, masked (`j***@agency.com`). Always the holder's own"},"walletPassSerial":{"type":"string","nullable":true,"readOnly":true},"walletPassUrl":{"type":"string","nullable":true,"readOnly":true,"description":"Signed and expiring; adds the pass to the wallet"},"status":{"type":"string","readOnly":true,"enum":["queued","sent","delivered","opened","failed","superseded"]},"failureReason":{"type":"string","nullable":true,"readOnly":true},"requestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time","readOnly":true},"deliveredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationDocument": {"type":"object","x-ticvai-persistence":"accreditation.document","description":"Board 2.5. **Submitted against a named requirement, not into a folder.**","required":["requirementCode","assetId"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid","nullable":true},"applicationId":{"type":"string","format":"uuid","nullable":true},"requirementCode":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"submittedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["submitted","verified","rejected","expired"]},"verifiedBy":{"type":"string","format":"uuid","nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**An insurance certificate valid until March accredits somebody until March**, whatever the programme says.\n"},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
