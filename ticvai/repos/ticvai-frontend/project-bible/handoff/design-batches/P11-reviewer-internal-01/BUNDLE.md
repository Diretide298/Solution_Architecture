# P11-reviewer-internal-01 — P11 · Reviewer (Internal)

**3 screens · 7 operations · 5 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ACCREDITATION_APPROVE, ACCREDITATION_VIEW`. A control nobody can use must say so,
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
| `ACC-006` | Reviewer Queue | B–D | 8 | 4 | 6 | 8 | 0 | 6 | — | notStarted (generated) |
| `ACC-007` | Reviewer Application Detail | B–D | 0 | 0 | 6 | 10 | 1 | 0 | — | notStarted (generated) |
| `ACC-008` | Credential Register | B–D | 2 | 12 | 6 | 3 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ACC-006` Reviewer Queue

**Work the queue of applications waiting on a decision, oldest-due first, and approve the straightforward ones without opening them.**

| | |
|---|---|
| App · platform | TICVAI Control · P11 Accreditation Web (web) |
| Module | Reviewer (Internal) · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public staff holding `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. · LTR and RTL · light theme |
| Pattern | approvalInbox (compact density):  |
| Offline | online only |
| Opens with | `programmeId` (session), `applicationId` (navigation) · cold entry: Opens on the reviewer's own programmes, due-first. |
| Route | `/reviewer-internal/reviewer-queue` |

**What the spec says about it.** **One queue component, shared with P08 BO-635** (decided 2 October 2026, Chinmay, workbook Q368; DEC-368, CHG-SOT-018). This screen and BO-635 render the shared `accreditationReview` queue (`screens/_components.yaml`, patterns) against the same operations; build it once and keep the two screens the same.

**Known gaps.** **Removed 9 September.** The screen declared `getWaitTimes`, which is the guest app's ride-queue read. A reviewer queue and a virtual queue share a word and nothing else — the fourth instance of a …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The reviewer's queue in the accreditation portal: applications waiting on a decision for the reviewer's programmes, due-first, with enough on the selected row to approve a clean one. Staff-facing and TICVAI-branded (per VO-R15). The one thing to get right: Approve from the queue is offered only when nothing is left to check, because the client agreed that staff open the application to review the photo and documents.

**Known correction pending (do not draw the wrong version)**

- **Columns bind ApprovalRequest.summary, requestedAt, slaDueAt, status** Why: The bound read returns AccreditationApplication; use subject, submittedAt, decisionDueAt and status. *(source: contracts/satellite/accreditation.yaml#listAccreditationApplications; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The edge to ACC-007 carries documentId** Why: ACC-007 needs applicationId. *(source: screens/P11-accreditation-portal.yaml#ACC-007; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Entered from ACC-001, the public landing** Why: Staff surface; reached from the reviewer's sign-in. *(source: DI-296 / DI-297; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Row signals "no press card, no commission" and the Performance filter** Why: Press and theatre wording; the signals are generic requirement and document states. *(source: screens/P08-venue-back-office.yaml#BO-636; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Approve carries permission APPROVAL_DECIDE (CHG-WIR-001); Approve is drawn but no decision operation is bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which reviewer surface survives, the P11 reviewer screens (ACC-006, ACC-007) or the P08 board (BO-635, BO-636)?** → One queue and one workspace component, used in both P11 (ACC-006, ACC-007) and P08 (BO-635, BO-636). *(decided by Chinmay, 2026-10-02; DEC-368 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Applicant or outlet | search field | — | — | — | — | Searches holder name and organisation. **Not "find a record".** | — |
| Performance | select field | — | — | — | — | All performances, or one. A reviewer usually works one night at a time. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationApplications` ?programmeId |
| Status | text field | — | — | `listAccreditationApplications` ?status |
| Applicant type | text field | — | — | `listAccreditationApplications` ?applicantType |

**Form: Approve** (modal, opened by *Approve*; *Approve* calls `decideAccreditationApplication`, *Cancel* sends nothing)

**Collects what `decideAccreditationApplication` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Approve · Reject · Return for information · Escalate | — | — | `decideAccreditationApplication` body |
| Reason `reason` | text area | optional | — | — | — | — | `decideAccreditationApplication` body |
| Missing requirements `missingRequirements` | list of values (chips) | optional | — | — | — | — | `decideAccreditationApplication` body |
| Access profile `accessProfileId` | picker: choose an access profile | optional | — | — | shows names, sends the id | — | `decideAccreditationApplication` body |
| Valid from `validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `decideAccreditationApplication` body |
| Valid to `validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `decideAccreditationApplication` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search**: Applicant name, organisation, reference or email; at least 2 characters. *(source: screens/P11-accreditation-portal.yaml#ACC-006)*
- **Filters**: Programme (from session), Event, Category, Organisation, Status (Received, With a reviewer, Waiting on applicant). "Performance" becomes Event. *(source: screens/P08-venue-back-office.yaml#BO-636)*

#### Outputs: what the screen shows and produces

**Shown**

**Queue** (data table): **Due first, and how long it has waited.** `slaDueAt` is the sort, not `requestedAt` — an application for tonight outranks one submitted earlier for next month. Rows carry the signals a reviewer decides on: *no press card, no commission*, *commission letter attached*, *accredited last season*.

| Shows | Format | Notes |
|---|---|---|
| Summary | text | — |
| Requested at | 1 Oct 2026, 14:30 | — |
| Sla due at | 1 Oct 2026, 14:30 | — |
| Status | chip: Draft, Pending, Escalated, Returned, Information requested, Approved… | — |

**Selected application** (detail panel): Enough to approve without opening `ACC-007`.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |
| Approve (secondary button) | `decideAccreditationApplication` POST `/accreditation-applications/{applicationId}/decide` | inline | AccreditationApplication | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Queue table "Applications to review"**: Columns: Applicant (photo thumbnail, name, organisation), Category, Event, Submitted ("3 days ago"), Decision due (chip: "Due in 2 days" grey, "Due today" amber, "Overdue 1 day" red), Checks (requirements met "5 of 6", documents verified "2 of 3", flags for possible duplicate and document expiring before the event), Status. Sorted by decisionDueAt ascending; an application for tonight's event outranks an older one for next month. Cursor paging. *(source: contracts/satellite/accreditation.yaml#listAccreditationApplications / DI-661)*
- **Selected application panel**: Photo beside ID document thumbnail, category, organisation, requirement checklist with states, approval stage ("Stage 1 of 2 - Media manager"). *(source: screens/P08-venue-back-office.yaml#BO-637 / DI-659)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Approve**: Enabled only when every requirement that blocks approval is met, every document is verified and no identity conflict is pending; otherwise disabled with the reason ("2 documents not verified"). Opens the approve drawer (access profile, validity) with the category's defaults. In a multi-level path the label says "Approve stage 1 of 2". *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication / DI-659 / DI-661)*
- **Open**: Opens ACC-007 with the applicationId. *(source: screens/P11-accreditation-portal.yaml#ACC-007)*

**Data it reads**: `listAccreditationApplications` (onLoad, Applications awaiting review, oldest first)

**Where the user goes next**

- → `ACC-007` Reviewer Application Detail: *Reviewer Application Detail*; carries `applicationId`, `documentId`
- → `ACC-008` Credential Register: *Credential Register*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue. |
| Empty, first run (`?state=emptyFirstRun`) | **An empty queue is success, not a broken screen.** Nothing is waiting — says so as reassurance, and says when the next applications are expected. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this filter. The queue itself is not empty. |
| Permission denied (`?state=emptyNoAccess`) | You do not review for this programme. |
| Error (`?state=error`) | Could not load the queue. **No decision is lost** — nothing was in flight. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Another reviewer decided it**: The row updates to the decision with the reviewer's name; Approve is withdrawn. *(source: screens/P11-accreditation-portal.yaml#ACC-007)*
- **Empty queue**: "Nothing waiting" as reassurance, with the next programme closing date. *(source: screens/P11-accreditation-portal.yaml#ACC-006)*
- **Reviewer not assigned to this programme**: "You do not review for this programme" (per VO-R08), never an empty table. *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-635`: Same queue, same columns, same sort and same SLA chips as the back-office review queue (per VO-R14); draw one queue component.
- Match `BO-623`: SLA chip thresholds match the intake monitor's SLA ageing buckets.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- applicant: Sara Al Nuaimi
  organisation: Gulf Lens Media
  category: Media
  event: Winter Festival opening night
  due: Due today
  checks: 6 of 6, documents 3 of 3
- applicant: James Carter
  organisation: Northbridge Events
  category: VIP
  event: Winter Festival
  due: Due in 2 days
  checks: 4 of 5, possible duplicate
- applicant: Khalid Al Zaabi
  organisation: Abu Dhabi Civil Defence liaison
  category: Government or authority
  due: Overdue 1 day
  checks: 5 of 5, documents 1 of 2
```

#### Permissions

- `listAccreditationApplications` → `ACCREDITATION_VIEW` (read) · staff
- `decideAccreditationApplication` → `ACCREDITATION_APPROVE` (operate) · staff

**A refused user sees:** You do not review for this programme.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.3 | Approval Workflow System shall support accreditation review and approval. | Accreditation & Credential Management | CONTRACTED | `decideAccreditationApplication` |
| 11.1.10 | Out-of-Office Routing - System shall automatically reroute approvals when approvers are unavailable. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.28 | Mobile Approvals - System shall support approval actions through mobile applications. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.29 | Email-Based Approvals - System shall support approval actions through email links. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.54 | Approval Reopening - System shall support reopening previously completed approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.73 | AI Risk Assessment - System shall provide AI-generated risk assessments for approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.75 | AI Escalation Recommendations - System shall recommend escalation actions based on approval patterns. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.78 | Shared Service Approval Centers - System shall support centralized approval processing teams. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P11, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P11 Accreditation Web.dc.html#acc-006` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ACC-006?state=<state>`: loading, emptyFirstRun, emptyNoResults, emptyNoAccess, error, offline.
- [ ] Every action is wired with its success and its failure: Approve, Approve.
- [ ] Every transition is wired: `ACC-007`, `ACC-008`.
- [ ] Every gated control is gated: `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ACC-007` Reviewer Application Detail

**Everything the decision needs about one application, in one place, so the reviewer does not open another screen to decide.**

| | |
|---|---|
| App · platform | TICVAI Control · P11 Accreditation Web (web) |
| Module | Reviewer (Internal) · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public staff holding `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as contractor |
| Device and orientation | This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. · LTR and RTL · light theme |
| Pattern | approvalInbox (compact density):  |
| Offline | online only |
| Opens with | `applicationId` (ACC-006), `documentId` (navigation) · cold entry: Reached from the queue, or from a link in a reviewer's email. Opened cold it loads the application, or says it has already been decided and by whom. |
| Route | `/reviewer-internal/reviewer-application-detail` |

**What the spec says about it.** **One workspace component, shared with P08 BO-636** (decided 2 October 2026, Chinmay, workbook Q368; DEC-368, CHG-SOT-018). This screen and BO-636 render the shared `accreditationReview` workspace (`screens/_components.yaml`, patterns) against the same operations; build it once and keep the two screens the same.

**Known gaps.** The screen shows one application and the only read is a list. **A detail screen that fetches a collection to find one row is a detail screen that gets slower as the queue grows.**

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** One application with everything the decision needs: who the person is (photo against their ID document), what they applied for, each document and its verification, what this venue knows about them already, and when the decision is due. The reviewer verifies documents and then approves, refuses, returns for information or escalates. The one thing to get right: approval is impossible while anything that blocks approval is unresolved, and every refusal carries a reason the applicant will read.

**Known correction pending (do not draw the wrong version)**

- **Only Approve and Refuse are drawn** Why: The contract and the pack also require Return for information and Escalate; the pack adds Put on hold. *(source: screens/P08-venue-back-office.yaml#BO-637 / contracts/satellite/accreditation.yaml#decideAccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Approve and Refuse carry APPROVAL_DECIDE** Why: The call checks ACCREDITATION_APPROVE (and verifying documents needs it too). *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication / contracts/satellite/accreditation.yaml#verifyAccreditationDocument; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Panels bind ApprovalRequest, ApprovalRequest.slaDueAt and ApprovalDecision.reason; gap getApprovalRequest** Why: Stale; getAccreditationApplication and decideAccreditationApplication serve them. *(source: contracts/satellite/accreditation.yaml#getAccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Approve drawer note "coverage granted may be narrower, stalls not pit"** Why: Theatre wording; what is narrowed is the access profile and validity. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"History with this venue" has no binding** Why: Needs listAccreditationAudit by holder and applications by holder; listAccreditationApplications has no holderId filter. *(source: contracts/satellite/accreditation.yaml#listAccreditationApplications / contracts/satellite/accreditation.yaml#listAccreditationAudit; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Exit to ACC-005 "The badge is issued" carrying holderId (CHG-WIR-002).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Must a refusal carry separate internal and applicant-visible text?** → Drawn default accepted: Draw two fields; the internal one greyed until the contract holds it. *(decided by Chinmay, 2026-10-02; DEC-369 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Application | picker: choose an application | — | — | `listAccreditationDocuments` ?applicationId |
| Holder | picker: choose a holder | — | — | `listAccreditationDocuments` ?holderId |
| Requirement code | text field | — | — | `listAccreditationDocuments` ?requirementCode |
| Status | radio group | — | Submitted · Verified · Rejected · Expired | `listAccreditationDocuments` ?status |
| Expiring within days | number field (days) | — | min 0 | `listAccreditationDocuments` ?expiringWithinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Document verification outcome**: Per document: Verified, or a refusal reason from a closed set (Illegible, Wrong document, Expired, Other). Every outcome but Verified requires a note. Verifying an identity document confirms or corrects its expiry date. *(source: contracts/satellite/accreditation.yaml#verifyAccreditationDocument)*
- **Approve drawer (access profile, valid from, valid to)**: Access profile defaults to the category's default and may be narrowed, never widened beyond the category without escalation; validity defaults to the programme's period; valid to may not pass the earliest expiry of a mandatory document. A preview lists the zones the person will open. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication / DI-662 / DI-663)*
- **Refuse**: Reason code (from the programme's rejection reasons) and an explanation the applicant will read; optionally the requirements to fix (missingRequirements) so the applicant knows what to change. *(source: screens/P08-venue-back-office.yaml#BO-640 / contracts/satellite/accreditation.yaml#decideAccreditationApplication)*
- **Return for information**: Tick the requirements that are missing or wrong and write what is needed; the applicant sees the list on ACC-004. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication)*

#### Outputs: what the screen shows and produces

**Shown**

**The application** (detail panel): Role, outlet, press card, commission — **including the ones that are absent**, stated as *Not stated* and *None attached* rather than left blank. A blank field and a declared absence look identical and only one is information.

**History with this venue** (detail panel): **Accredited before, and conditions breached.** This is the field the decision usually turns on and the one a reviewer would otherwise go looking for.

**Decision due** (banner)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |
| Refuse (destructive button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **The application**: Every answer, with absent ones stated as "Not given" or "None attached". Photo and ID document image side by side for comparison. Identity numbers masked, with Reveal for permitted reviewers (logged). *(source: DI-659 / ADR-0063)*
- **History with this venue**: Previous applications and their outcomes, earlier holder record and status changes (suspended, revoked), resubmission chain ("Refused 02 Oct - missing documentation; resubmitted 05 Oct"). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication / contracts/satellite/accreditation.yaml#listAccreditationAudit)*
- **Decision due**: Banner with decisionDueAt and stage of the approval path; red once overdue. *(source: contracts/satellite/accreditation.yaml#getAccreditationApplication / DI-661)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Approve**: Disabled with the list of what is outstanding while any approval-blocking requirement is unmet, a document is unverified or an identity conflict is pending. On success the application shows Approved and offers "Issue credential" (to BO-645). *(source: screens/P08-venue-back-office.yaml#BO-637 / contracts/satellite/accreditation.yaml#decideAccreditationApplication)*
- **Refuse**: Confirmation states the applicant will read the explanation; the application becomes Not approved and the route back is open to the applicant. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication / MATRIX 12.1.33)*
- **Return for information**: Application goes to informationRequested; the decision timer handling follows the SLA policy. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication)*
- **Escalate**: Sends to the next approval level with a reason; the stage indicator advances. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication / DI-661)*

**Data it reads**: `getAccreditationApplication` (onLoad, The application under review); `listAccreditationDocuments` (onLoad, The application's documents (applicationId), each with its …)

**Where the user goes next**

- → `ACC-006` Reviewer Queue: *Reviewer Queue*
- → `ACC-008` Credential Register: *Credential Register*
- → `ACC-005` Accreditation Badge: *The badge is issued*; carries `holderId`

**What opens over it**

- confirmDialog *Refuse*: **Captures the reason, and says the applicant will read it.** `ApprovalDecision.reason` is part of the record; a refusal with no reason produces an appeal by telephone.
- drawer *Approve*: Coverage granted may be narrower than coverage requested — *stalls, not pit*. **The badge renders what is granted**, so the two screens must agree.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The application. |
| Error (`?state=error`) | **A failed decision is not a made decision.** Says the decision was not recorded and leaves the buttons live. |
| Permission denied (`?state=emptyNoAccess`) | You do not review for this programme. |
| Empty, no results (`?state=emptyNoResults`) | This application was decided by somebody else while it was open. Shows the decision. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing selected. The queue is where a reviewer starts. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Pending identity conflict on this person**: Red banner "Possible duplicate of SP26-CON-00211 - resolve before approving" linking to BO-631. *(source: contracts/satellite/accreditation.yaml#resolveIdentityConflict / DI-659)*
- **Decided by somebody else while open**: The decision, its author and time replace the actions. *(source: screens/P11-accreditation-portal.yaml#ACC-007)*
- **Decision call fails**: "The decision was not recorded" with the buttons still live. *(source: screens/P11-accreditation-portal.yaml#ACC-007)*

#### Consistency with other screens

- Match `BO-636`: Same workspace as the back-office review workspace (per VO-R14); same outcome labels and the same approve drawer.
- Match `BO-630`: Document refusal reasons are the same closed set as in the verification queue.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
application:
  reference: ACR-2026-004402
  applicant: James Carter
  category: VIP
  organisation: Northbridge Events
  documents:
  - Passport - verified
  - Sponsor letter - submitted
  due: 20 Oct 2026
history:
- Accredited Winter Festival 2025, VIP, no incidents
approve:
  accessProfile: VIP hospitality
  validFrom: 10 Dec 2026
  validTo: 14 Dec 2026
```

#### Permissions

- `decideAccreditationApplication` → `ACCREDITATION_APPROVE` (operate) · staff
- `getAccreditationApplication` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationDocuments` → `ACCREDITATION_VIEW` (read) · staff
- `verifyAccreditationDocument` → `ACCREDITATION_APPROVE` (operate) · staff

**A refused user sees:** You do not review for this programme.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.3 | Approval Workflow System shall support accreditation review and approval. | Accreditation & Credential Management | CONTRACTED | `decideAccreditationApplication` |
| 12.1.18 | Document Management - System shall support storage of accreditation-related documents. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |
| 12.1.19 | Identity Verification - System shall support identity verification before accreditation approval. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |
| 11.1.10 | Out-of-Office Routing - System shall automatically reroute approvals when approvers are unavailable. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.28 | Mobile Approvals - System shall support approval actions through mobile applications. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.29 | Email-Based Approvals - System shall support approval actions through email links. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.54 | Approval Reopening - System shall support reopening previously completed approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.73 | AI Risk Assessment - System shall provide AI-generated risk assessments for approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.75 | AI Escalation Recommendations - System shall recommend escalation actions based on approval patterns. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.78 | Shared Service Approval Centers - System shall support centralized approval processing teams. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*

Also apply: 8 for all of P11, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P11 Accreditation Web.dc.html#acc-007` · status **notStarted** · provenance generated
- Flow F23 *A contractor gets a badge and uses it*, step 2: A reviewer checks and approves → **Through `approvals`** — one mechanism, not a fifth
- Flow F23 branch at step 2 (requiresStaff): when Background check required and not complete, Blocks issue. **12.1.x implies verification and names no provider** — CF-21, and the workshop question.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ACC-007?state=<state>`: loading, error, emptyNoAccess, emptyNoResults, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Approve, Refuse.
- [ ] Every transition is wired: `ACC-006`, `ACC-008`, `ACC-005`.
- [ ] Every gated control is gated: `ACCREDITATION_APPROVE`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ACC-008` Credential Register

**Every credential issued this season, who holds it, where it is valid, and whether it has been used — and revoke one when it has to be revoked.**

| | |
|---|---|
| App · platform | TICVAI Control · P11 Accreditation Web (web) |
| Module | Reviewer (Internal) · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public staff holding `ACCREDITATION_VIEW` (1 read) |
| Device and orientation | This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. · LTR and RTL · light theme |
| Pattern | listDetail (compact density):  |
| Offline | online only |
| Opens with | `programmeId` (session) · cold entry: Opens on the current season. |
| Route | `/reviewer-internal/credential-register` |

**Known gaps.** The register offers **Revoke** and nothing performs it. `AccreditationBadge.state` and `revokedReason` exist to record the outcome, so the schema is ready and the operation is not. The register shows a **last used** column and the schema has no such field. *Not yet* is the value that matters — a credential issued and never presented is the one to ask about.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The register of every credential issued this season: who holds it, what it opens, when it was issued, whether it has ever been used, and its status, handed to a security team before an event. Revoked and replaced rows stay visible. The one thing to get right: stopping a credential and stopping a person's accreditation are different acts with different consequences, and the screen must say which one is happening.

**Known correction pending (do not draw the wrong version)**

- **"Revoke" with gap revokeAccreditationBadge and permission APPROVAL_DECIDE** Why: Stale and ambiguous: a single credential is ended by replaceAccreditationCredential (ACCREDITATION_ISSUE) and the accreditation by setAccreditationStatus revoked (ACCREDITATION_MANAGE). Draw both, named. *(source: contracts/satellite/accreditation.yaml#replaceAccreditationCredential / contracts/satellite/accreditation.yaml#setAccreditationStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Export has no operation bound** Why: exportAccreditationData exists and should be bound. *(source: contracts/satellite/accreditation.yaml#exportAccreditationData; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Gap lastUsedAt and table bound to AccreditationBadge (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "Last used" a scan at any gate, or only an admitted scan?** → Drawn default accepted: Admitted scans only; denied attempts appear in the detail panel. *(decided by Chinmay, 2026-10-02; DEC-370 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Holder or reference | search field | — | — | — | — | — | — |
| Season | select field | — | — | — | — | Defaults to the current season. **A register scoped to all time is a register nobody reads.** | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationCredentials` ?holderId |
| Status | text field | — | — | `listAccreditationCredentials` ?status |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Season**: Programme select, defaulting to the current one; "All time" is not offered. *(source: screens/P11-accreditation-portal.yaml#ACC-008)*
- **Revoke reason**: Required; for a credential a closed set (Lost, Stolen, Damaged, Name change, Photo change, Access change), for an accreditation free text. *(source: contracts/satellite/accreditation.yaml#replaceAccreditationCredential / contracts/satellite/accreditation.yaml#setAccreditationStatus)*

#### Outputs: what the screen shows and produces

**Shown**

**Last used** (data table, from `listAccreditationAccessActivity`)

| Shows | Format | Notes |
|---|---|---|
| At | 1 Oct 2026, 14:30 | — |
| Holder | the name it points at, never the id | — |
| Holder name | text | — |
| Zone | the name it points at, never the id | — |
| Zone name | text | — |
| Credential | the name it points at, never the id | — |
| Outcome | chip: Admitted, Denied, Escorted | — |
| Denied reason | text | — |

**Credential register** (data table): Holder, valid for, issued, last used. **Revoked rows stay visible and read as revoked** — removing them from the register is how a revoked badge gets re-issued by mistake.

| Shows | Format | Notes |
|---|---|---|
| Holder name | text | — |
| Zones | list or chips (count when long) | Where this badge admits, which is the whole point of it. |
| Issued at | 1 Oct 2026, 14:30 | — |
| State | chip: Issued, Collected, Suspended, Revoked, Expired | — |

**Credential** (detail panel)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Revoke (destructive button) | navigation or local | — | — | — | — |
| Export (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Credential register table**: Columns: Holder (photo, name, organisation), Credential (kind and serial, e.g. "Printed badge SP26-B-00318"), Valid for (zones), Issued, Last used ("Not yet" in amber when issued more than 2 days ago), Status. Revoked, replaced and lost rows stay, struck through, with a link to the replacement. Cursor paging. *(source: contracts/satellite/accreditation.yaml#listAccreditationCredentials / contracts/satellite/accreditation.yaml#listAccreditationAccessActivity)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Replace credential**: Issues a new credential and invalidates this one in the same act; the confirm names the new kind and says the old one stops working at once. *(source: contracts/satellite/accreditation.yaml#replaceAccreditationCredential)*
- **Revoke accreditation**: Confirmation per VO-R16: "Khalid Al Zaabi loses access to 4 zones now; 2 credentials stop working at every gate." Every credential is invalidated and pushed to the gates. *(source: contracts/satellite/accreditation.yaml#setAccreditationStatus)*
- **Export**: Starts an export of the filtered register; the file arrives in the export list when ready. *(source: contracts/satellite/accreditation.yaml#exportAccreditationData)*

**Data it reads**: `listAccreditationCredentials` (onLoad, Every credential issued, with its validity)

**Where the user goes next**

- → `ACC-006` Reviewer Queue: *Reviewer Queue*
- → `ACC-007` Reviewer Application Detail: *Reviewer Application Detail*

**What opens over it**

- confirmDialog *Revoke*: **Names the holder and what stops working, and captures the reason.** A revocation takes somebody's access to a building they may already be standing outside.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The register. |
| Empty, first run (`?state=emptyFirstRun`) | No credentials issued yet this season. Points at the queue. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches. The register is not empty. |
| Permission denied (`?state=emptyNoAccess`) | You do not administer credentials for this programme. |
| Error (`?state=error`) | Could not load. **No credential is affected** by a failed read. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Revoking while the holder is inside**: The confirm warns that the person may already be on site; gates refuse at the next scan, including offline gates after their package refresh. *(source: contracts/satellite/accreditation.yaml#verifyAccreditationCredential)*
- **Viewer without credential rights**: "You do not administer credentials for this programme", Revoke disabled with the permission named (per VO-R08). *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-645`: Same credential list and statuses as the back-office credential screens.
- Match `SCN-003`: Status words (Replaced, Lost, Revoked, Expired) are the ones the steward sees.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- holder: Rahul Menon
  credential: Mobile QR SP26-M-00318
  validFor: Main stage build area, Loading dock
  issued: 09 Oct 2026
  lastUsed: Not yet
  status: Active
- holder: Maria Santos
  credential: Printed badge SP26-B-00322
  validFor: Crew catering
  issued: 08 Oct 2026
  lastUsed: 11 Oct 2026, 07:42
  status: Active
- holder: Omar Haddad
  credential: Printed badge SP26-B-00290
  validFor: Loading dock
  issued: 01 Oct 2026
  lastUsed: 05 Oct 2026, 06:58
  status: Replaced
```

#### Permissions

- `listAccreditationCredentials` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationAccessActivity` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** You do not administer credentials for this programme.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.31 | Access Audit Trail - System shall maintain audit logs of accreditation access activities. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAccessActivity` |
| 12.1.48 | Accreditation Utilization Reporting - System shall provide accreditation utilization reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAccessActivity` |
| 12.1.49 | Accreditation Access Reporting - System shall provide reports on accreditation access activity. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAccessActivity` |

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P11, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P11 Accreditation Web.dc.html#acc-008` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ACC-008?state=<state>`: loading, emptyFirstRun, emptyNoResults, emptyNoAccess, error, offline.
- [ ] Every action is wired with its success and its failure: Revoke, Export.
- [ ] Every transition is wired: `ACC-006`, `ACC-007`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"decideAccreditationApplication": {"method":"POST","path":"/accreditation-applications/{applicationId}/decide","contract":"accreditation","summary":"Approve, reject, return for more, or escalate","permission":"ACCREDITATION_APPROVE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"getAccreditationApplication": {"method":"GET","path":"/accreditation-applications/{applicationId}","contract":"accreditation","summary":"One application, with where each requirement stands","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccreditationApplication"},
"listAccreditationAccessActivity": {"method":"GET","path":"/accreditation-access-activity","contract":"accreditation","summary":"Where accredited people actually went","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"holderId","in":"query","required":null},{"name":"zoneId","in":"query","required":null},{"name":"deniedOnly","in":"query","required":null}],"requestBody":null,"responds":"AccreditationAccessEvent"},
"listAccreditationApplications": {"method":"GET","path":"/accreditation-applications","contract":"accreditation","summary":"Applications, by state and programme","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"applicantType","in":"query","required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"listAccreditationCredentials": {"method":"GET","path":"/accreditation-credentials","contract":"accreditation","summary":"Badges and digital credentials issued","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"holderId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"AccreditationCredential"},
"listAccreditationDocuments": {"method":"GET","path":"/accreditation-documents","contract":"accreditation","summary":"Documents supplied, by holder, application, requirement or state","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"applicationId","in":"query","required":null},{"name":"holderId","in":"query","required":null},{"name":"requirementCode","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"verifyAccreditationDocument": {"method":"POST","path":"/accreditation-documents/{documentId}/verify","contract":"accreditation","summary":"Accept or refuse a submitted document","permission":"ACCREDITATION_APPROVE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationDocument"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationAccessEvent": {"type":"object","description":"Board 8.4. **Granted access against used access is the whole of the annual review.**\n","properties":{"at":{"type":"string","format":"date-time"},"holderId":{"type":"string","format":"uuid"},"holderName":{"type":"string"},"zoneId":{"type":"string","format":"uuid"},"zoneName":{"type":"string"},"credentialId":{"type":"string","format":"uuid","nullable":true},"outcome":{"type":"string","enum":["admitted","denied","escorted"]},"deniedReason":{"type":"string","nullable":true}}},
"AccreditationApplication": {"type":"object","x-ticvai-persistence":"accreditation.application","description":"Board 1.3. **Usually submitted by an organisation on behalf of its people.**","required":["programmeId"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"applicantType":{"type":"string"},"submittedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"subject":{"type":"object","additionalProperties":true,"description":"Name, date of birth, nationality, contact — shaped by the requirements matrix."},"requirementStatus":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"requirementCode":{"type":"string"},"satisfied":{"type":"boolean"},"documentId":{"type":"string","format":"uuid","nullable":true}}}},"status":{"type":"string","enum":["draft","submitted","underReview","informationRequested","approved","rejected","withdrawn","expired"]},"decisionReason":{"type":"string","nullable":true},"missingRequirements":{"type":"array","readOnly":true,"description":"The requirement codes a reviewer returned the application for, or rejected it over — what the applicant must change before resubmitting","items":{"type":"string"}},"decisionDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a decision is due — the approvals request's SLA. **A date, not a queue position**"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"holderId":{"type":"string","format":"uuid","nullable":true},"renewsHolderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.37. Set by `renewAccreditation`; approval extends this holder rather than creating one"},"resubmissionOfApplicationId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.33. The rejected application this one resubmits, so the rejection stays in the record"},"resubmissionNote":{"type":"string","maxLength":1000,"nullable":true,"readOnly":true,"description":"What the applicant changed, from `resubmitAccreditationApplication`"},"submittedAt":{"type":"string","format":"date-time","nullable":true},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"AccreditationCredential": {"type":"object","x-ticvai-persistence":"accreditation.credential","description":"Board 4. **Not the accreditation** — reissuing one re-vets nobody.","required":["holderId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["printedBadge","mobileCredential","qr","nfcCard","rfidCard","wristband"]},"symbology":{"type":"string","nullable":true,"description":"12.1.22. **How `encodedIdentifier` is carried**, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a `mobileCredential`, a barcode where a printed badge carries one, `nfcNdef` or `rfidEpc` for an encoded card, `none` where nothing is encoded.\n","enum":["qr","dataMatrix","pdf417","aztec","code128","nfcNdef","rfidEpc","none"]},"serialNumber":{"type":"string","nullable":true},"encodedIdentifier":{"type":"string","nullable":true},"badgeTemplateId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"issuedBy":{"type":"string","format":"uuid"},"activatedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["pendingPrint","issued","active","lost","replaced","revoked","expired"]},"replacesCredentialId":{"type":"string","format":"uuid","nullable":true},"replacementCount":{"type":"integer","default":0},"scopePath":{"type":"string"}}},
"AccreditationDocument": {"type":"object","x-ticvai-persistence":"accreditation.document","description":"Board 2.5. **Submitted against a named requirement, not into a folder.**","required":["requirementCode","assetId"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid","nullable":true},"applicationId":{"type":"string","format":"uuid","nullable":true},"requirementCode":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"submittedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["submitted","verified","rejected","expired"]},"verifiedBy":{"type":"string","format":"uuid","nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**An insurance certificate valid until March accredits somebody until March**, whatever the programme says.\n"},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
