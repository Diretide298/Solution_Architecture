# WS108 — ACCREDITATION board 1

**10 screens · 17 operations · 10 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ACCREDITATION_APPLY, ACCREDITATION_CONFIGURE, ACCREDITATION_MANAGE, ACCREDITATION_VIEW, GUEST_VIEW, MARKETING_MANAGE, MARKETING_VIEW`. A control nobody can use must say so,
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

### Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers)

Customer & marketing is how a venue knows its guests and talks to them. There is ONE guest profile per person across ticketing, F&B and retail, so a guest who books online and later dines is the same profile (DI-339). A profile needs at least an email or a mobile, never neither (DI-372). Profiles are created by registration, by guest checkout, or by staff at a till or desk. Repeat guest checkouts with the same verified email or phone attach to the same profile automatically (DI-941, R120 default). Two records that might be the same person are NEVER merged automatically: the guest is asked to confirm, and an admin review queue runs alongside (DI-377). Each candidate shows why it matched; the record that loses is superseded, not deleted; consent takes the narrower of the two positions (DI-808). Around the profile sit three things that must never be confused. CONSENT is what the law allows: per purpose and per channel, append-only, with the notice version and the source (recordConsent). It is Given, Withdrawn or Not asked. A SUBSCRIPTION is what the guest asked to receive, e.g. a newsletter list (MarketingSubscription). A PREFERENCE is what they like: table, dietary, accessibility (updateGuestPreferences). An anonymous visitor's cookie decision is recorded against a device key (recordDeviceConsent) and attaches to the guest when they sign in (claimDeviceConsent). Marketing consent at GUEST CHECKOUT is an open client question, and the design follows its default: an unticked opt-in beside the terms, one per channel and purpose. It is recorded with source "checkout" against the order and the verified contact, and nothing is sent without it. Whether that is sufficient consent under PDPL is the client DPO's call (M18-15 (audit R-M18-15), DI-954, DI-940). Marketing reads profiles through SEGMENTS (rules, evaluated when used) and static LISTS (imported). It reaches guests by CAMPAIGNS (one send to an audience) and JOURNEYS (automations started by an event, with waits and branches). Journeys may offer only pre-configured offers, never a free-typed discount (MoM 2026-08-20 4.6). Everything goes through ONE communications module that every other module uses (MoM 2026-08-31 4.6). Consent and suppression are applied at send time, and the number excluded, with the reasons, is reported before anything goes out (launchCampaign). Transactional messages (tickets, receipts, queue calls, case replies) do not need marketing consent and must never carry marketing. LOYALTY pays for spend: points, tiers, rewards and expiry. GAMIFICATION pays for behaviour: challenges, badges, streaks, referrals and leaderboards (createChallenge). A guest reads their own loyalty position (getLoyaltyPosition). A till, the back office or support reads a named guest's (getGuestLoyalty, or identifyGuest at a till). SERVICE: one Case object covers lost property, complaints, questions, accessibility and refund requests (CaseKind). A guest raises one with raiseMyCase, which needs the connection …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Guest | The person the venue serves, signed in or not. In body copy on every surface. | Customer, User, Subject, Contact, Patron | contracts/satellite/marketing-crm.yaml#/components/schemas/GuestProfile |
| Guest profile | The CRM record of one person (details, consent, preferences, history). Distinct from the Account, which is how a guest signs in. | Customer record, Contact, Subject | contracts/satellite/marketing-crm.yaml#getGuestProfile |
| Consent - Given / Withdrawn / Not asked | What the law allows, per purpose (marketing, personalisation, profiling, third-party sharing, AI processing, transactional) and per channel. "Not asked" is not "Withdrawn" and must look different. | Opted in/out as a status, Accepted, Declined, Revoked, Unsubscribed (that is a subscription) | contracts/satellite/marketing-crm.yaml#/components/schemas/ConsentDecision |
| Subscription | A list the guest asked to receive (a newsletter, event news), per channel. Unsubscribing from a list is not withdrawing consent. | Consent, Opt-in | contracts/satellite/marketing-crm.yaml#/components/schemas/MarketingSubscription |
| Preferences | What the guest likes or needs (seating, drinks, dietary, accessibility, contact channel). Never grants permission. | Consents, Settings | contracts/satellite/marketing-crm.yaml#updateGuestPreferences |
| Send me offers and news | The marketing opt-in label beside the terms at checkout, unticked, one per channel and purpose. | I agree to marketing, Pre-ticked boxes, Keep me updated ticked by default | DI-954 |
| Points / Tier / Points to next tier / Expiring points | The loyalty position. Points are a liability earned per programme; tiers are ranked (Bronze, Silver, Gold, Platinum in the meetings). | Credits, Coins, Balance alone (wallet money is "credit"), Level | DI-382 |
| Pending points | Points earned on a purchase still inside its refund window; shown apart from spendable points. | Available points for pending ones | contracts/satellite/marketing-crm.yaml#getLoyaltyPosition |
| Reward | What points can be turned into (rewards catalogue). | Prize (games redemption uses prize), Voucher unless it is one | contracts/satellite/marketing-crm.yaml#listRewards |
| Challenge / Badge / Streak / Referral | Gamification - rewards for behaviour, not spend. Status badges such as Explorer, Adventurer, Legend. | Mission and Quest used interchangeably on one screen, Loyalty tier for a badge | DI-392 |
| Case | One service record - lost property, complaint, question, accessibility, refund request or other - with a number (venue prefix plus sequence), a status and an SLA. | Ticket (a ticket is an admission product), Issue, Incident (that is maintenance and safety) | contracts/satellite/marketing-crm.yaml#/components/schemas/CaseKind |
| Reply to guest / Internal note | The two kinds of case message. The agent always chooses one explicitly; there is no default. | Comment, Message (ambiguous) | F05 step 2 |
| Conversation | A live chat session (web chat, in-app, WhatsApp, SMS, email, kiosk, voice). With the assistant, then queued, then with an agent. It is not a case. | Ticket, Case (until one is raised from it) | contracts/satellite/marketing-crm.yaml#/components/schemas/ConversationState |
| Segment / List / Audience | A segment is rules evaluated when used. A list is static, imported or hand-picked. The audience is what a campaign or journey targets. | Group, Cohort, Target list for a segment | DI-381 |
| Campaign / Journey | A campaign is one send (one-off, scheduled, triggered or recurring) to an audience. A journey is an automation started by an event, with steps, waits and branches. | Flow (booking flows use it), Automation for a one-off send, Blast | R146 |
| Offer | A pre-configured, system-validated discount or benefit that a campaign or journey references. It is never typed into the builder. | Discount field, Coupon (unless the offer is a coupon code) | MoM 2026-08-20 4.6 |
| Reachable | How many guests in an audience can actually be sent to on a channel after consent and suppression. Always shown beside the matching count. | Audience size alone | contracts/satellite/marketing-crm.yaml#previewSegment |
| Possible duplicate / Merge | Two profiles that may be one person. Never called "Duplicate" as a verdict. Merging needs confirmation and stays reversible for 30 days. | Duplicate (as a status), Combine, Auto-merge | DI-808 |
| Data request | A guest's privacy request - a copy of my data, a correction, erasure, a restriction - with a legal clock. Statuses submitted, in progress, completed. | DSAR on guest screens, Subject data, Ticket | DI-379 |
| Waiver / Consent question | A waiver is a signed, versioned form. A consent question ("Are you able to swim?", "I accept the risk") is a single question asked per person or per booking and recorded as consent. | Contract, Disclaimer, Form for a waiver in guest copy | DI-1062 |
| Lost item / Found item / Possible match | The two directions of lost property and the suggested pairing between them. | Lost case, Claim before it is claimed | contracts/satellite/marketing-crm.yaml#/components/schemas/LostItem |
| Wishlist | Products and dates a guest saved to buy later, including F&B and retail to buy on site. | Favourites (used for transport routes), Saved for later on one surface and Wishlist on another | DI-202 |
| Notification / Message | A notification is an item in the guest's in-app feed. A message is one send on a channel (email, SMS, WhatsApp, push, in-app). | Alert for marketing content, Inbox for the guest feed | contracts/satellite/marketing-crm.yaml#/components/schemas/GuestNotification |
| Template | A reusable message body per channel and language with merge fields. Transactional and marketing templates are separate kinds. | Layout, Design | contracts/satellite/marketing-crm.yaml#createMessageTemplate |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-615` | Accreditation Command Center | D | 0 | 38 | 6 | 6 | 1 | 6 | — | notStarted (—) |
| `BO-616` | Accreditation Application Directory | D | 0 | 24 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-617` | New Accreditation Application | D | 0 | 0 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-618` | Accreditation Form Builder | A | 1 | 46 | 6 | 75 | 1 | 6 | — | notStarted (—) |
| `BO-619` | Accreditation Category Management | D | 25 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-620` | Accreditation Program Setup | D | 0 | 0 | 6 | 4 | 1 | 6 | — | notStarted (—) |
| `BO-621` | Applicant Type Configuration | D | 0 | 0 | 6 | 7 | 1 | 0 | — | notStarted (—) |
| `BO-622` | Application Requirements Matrix | D | 0 | 0 | 6 | 7 | 1 | 0 | — | notStarted (—) |
| `BO-623` | Accreditation Intake Monitor | D | 0 | 29 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-624` | Registration Rules & Publication | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-616, BO-617, BO-619, BO-620, BO-621, BO-622, BO-623, BO-624 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-615` Accreditation Command Center

**Executive and operational landing screen for the accreditation module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-615 |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-command-center-bo-615` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The accreditation team's landing: how many applications are in each state, how many credentials are live, what is about to expire, and the exceptions that need someone today, with quick routes into the boards. It is a command centre (per VO-R02): KPI tiles with deltas, an alerts list, two visual summaries and quick actions, drawn once as a configurable dashboard. The one thing to get right: every tile and alert opens the filtered list behind it, so the number is never a dead end.

**Known correction pending (do not draw the wrong version)**

- **The screen is a dataTable with no columns, and the gap note says the pack gives nothing that can be drawn** Why: Pack pages 3 and 4 list ten KPI cards, the filters, two visual summaries, five quick actions and an alerts area; draw it as a command centre (per VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-615 / screens/P08-venue-back-office.yaml#BO-616; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Tiles must be computed by fetching whole lists** Why: The list reads return unpaged arrays with no counts; a 1,000-member programme makes the landing fetch every record. A counts read is needed. *(source: MATRIX 12.1.47 / contracts/satellite/accreditation.yaml#listAccreditationApplications; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation exits only to board 1 screens** Why: The pack's quick actions Review applications, Issue credentials and Manage access lead to boards 3, 4 and 5; those edges are missing. *(source: screens/P08-venue-back-office.yaml#BO-616; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Active credentials, Expired documents and the duplicate alert have no read bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What window defines "Expiring soon"?** → Drawn default accepted: 30 days, shown in the tile caption. *(decided by Chinmay, 2026-10-02; DEC-446 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationApplications` ?programmeId |
| Status | text field | — | — | `listAccreditationApplications` ?status |
| Applicant type | text field | — | — | `listAccreditationApplications` ?applicantType |
| Programme | picker: choose a programme | — | — | `listAccreditationHolders` ?programmeId |
| Organisation | picker: choose an organisation | — | — | `listAccreditationHolders` ?organisationId |
| Status | text field | — | — | `listAccreditationHolders` ?status |
| Expiring within days | number field (days) | — | — | `listAccreditationHolders` ?expiringWithinDays |
| Holder | picker: choose a holder | — | — | `listAccreditationCredentials` ?holderId |
| Status | text field | — | — | `listAccreditationCredentials` ?status |
| Application | picker: choose an application | — | — | `listAccreditationDocuments` ?applicationId |
| Holder | picker: choose a holder | — | — | `listAccreditationDocuments` ?holderId |
| Requirement code | text field | — | — | `listAccreditationDocuments` ?requirementCode |
| Status | radio group | — | Submitted · Verified · Rejected · Expired | `listAccreditationDocuments` ?status |
| Expiring within days | number field (days) | — | min 0 | `listAccreditationDocuments` ?expiringWithinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Programme, Event, Category, Organisation and a date range (default: this programme's application window). The venue comes from the top-bar switcher (per VO-R09); a tenant filter appears only for users whose scope is the tenant. *(source: screens/P08-venue-back-office.yaml#BO-616)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Active credentials** (data table, from `listAccreditationCredentials`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Holder | the name it points at, never the id | — |
| Kind | chip: Printed badge, Mobile credential, QR, NFC card, RFID card, Wristband | — |
| Symbology | chip: QR, Data matrix, Pdf417, Aztec, Code128, NFC ndef… | 12.1.22. How `encodedIdentifier` is carried, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a … |
| Serial number | text | — |
| Encoded identifier | text | — |
| Badge template | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Issued by | the name it points at, never the id | — |
| Activated at | 1 Oct 2026, 14:30 | — |
| Status | chip: Pending print, Issued, Active, Lost, Replaced, Revoked… | — |
| Replaces credential | the name it points at, never the id | — |
| Replacement count | 1,234 | — |

**Expired documents** (data table, from `listAccreditationDocuments`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Holder | the name it points at, never the id | — |
| Application | the name it points at, never the id | — |
| Requirement code | text | — |
| Asset | the image or video | — |
| Submitted at | 1 Oct 2026, 14:30 | — |
| Status | chip: Submitted, Verified, Rejected, Expired | — |
| Verified by | the name it points at, never the id | — |
| Verified at | 1 Oct 2026, 14:30 | — |
| Rejection reason | text | — |
| Expires at | 1 Oct 2026 | An insurance certificate valid until March accredits somebody until March, whatever the programme says. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Duplicate alerts** (data table, from `listAccreditationIdentityConflicts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Holders | list or chips (count when long) | — |
| Score | 1,234.5 | — |
| Matched on | list or chips (count when long) | — |
| Differing access | yes / no (icon or chip) | — |
| Status | chip: Pending, Merged, Rejected | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Surviving holder | the name it points at, never the id | The holder kept when the conflict was merged |
| Resolution reason | text | — |
| Resolved by principal | the name it points at, never the id | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Ten tiles in the pack's order: Total applications, Pending (submitted), Under review, Approved, Rejected, Active credentials, Expiring soon, Suspended, Revoked, Expired; plus Expired documents from the 7 September meeting. Each tile shows the count and the change against the previous period ("+42 this week"). Pending and Under review come from application status; Suspended, Revoked and Expired from holder status; Expiring soon from holders with validTo inside 30 days. *(source: screens/P08-venue-back-office.yaml#BO-615 / screens/P08-venue-back-office.yaml#BO-616 / DI-654 / contracts/satellite/accreditation.yaml#listAccreditationHolders)*
- **Visual summaries**: Applications by category as a stacked bar by status; credentials by type as a small bar; both filter the page on click. *(source: screens/P08-venue-back-office.yaml#BO-616)*
- **Alerts needing action**: Ordered by urgency, each with a count and an Open link: applications past their decision date, possible duplicates waiting, holders whose identity document expires before their event, categories above 90 percent of quota, badge print jobs that partly failed. *(source: screens/P08-venue-back-office.yaml#BO-616 / DI-661 / DI-663 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Freshness stamp**: "As of 14:05" beside the tiles, because the reads come from a replica. *(source: contracts/satellite/accreditation.yaml#listAccreditationApplications)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Quick actions**: New application (BO-617), Create programme (BO-620), Review applications (BO-635), Issue credentials (BO-644), Manage access (the access-rights board). Each is disabled with the permission named where the user lacks it (per VO-R08). *(source: screens/P08-venue-back-office.yaml#BO-616)*
- **Open a tile**: Opens BO-616 filtered to that state (holders tiles open BO-625 filtered); Back returns here with filters kept. *(source: ADR-0041 / DI-653)*

**Data it reads**: `listAccreditationApplications` (onLoad, Applications in flight); `listAccreditationHolders` (onLoad, Holders by status); `listAccreditationCredentials` (onLoad, Active credentials); `listAccreditationDocuments` (onLoad, Documents expired or expiring); `listAccreditationIdentityConflicts` (onLoad, Possible duplicate identities)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-616` Accreditation Application Directory: *Accreditation Application Directory*; carries `applicationId`
- → `BO-617` New Accreditation Application: *New Accreditation Application*; carries `applicationId`
- → `BO-618` Accreditation Form Builder: *Accreditation Form Builder*; carries `programmeId`
- → `BO-619` Accreditation Category Management: *Accreditation Category Management*; carries `programmeId`
- → `BO-620` Accreditation Program Setup: *Accreditation Program Setup*; carries `programmeId`
- → `BO-621` Applicant Type Configuration: *Applicant Type Configuration*
- → `BO-622` Application Requirements Matrix: *Application Requirements Matrix*
- → `BO-623` Accreditation Intake Monitor: *Accreditation Intake Monitor*
- → `BO-624` Registration Rules & Publication: *Registration Rules & Publication*; carries `programmeId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **First run, no programme yet**: Tiles are replaced by "Create your first accreditation programme" leading to BO-620, not a row of zeros. *(source: screens/P08-venue-back-office.yaml#BO-615)*
- **Viewer without accreditation rights**: Names the missing permission; never empty tiles (per VO-R08). *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-684`: The Accreditation Executive Dashboard reads the same two lists (MATRIX 12.1.47); draw one dashboard with seeded tiles, not two hand-built pages (per VO-R02).
- Match `BO-623`: The intake monitor's tiles are a second tab of this dashboard pattern; tile names and SLA buckets match.
- Match `BO-644`: The credential issuance command centre uses the same tile and alert components.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programme: Summit Peaks Winter Festival 2026 accreditation
tiles:
  totalApplications: 1284
  pending: 96
  underReview: 141
  approved: 902
  rejected: 61
  activeCredentials: 877
  expiringSoon: 23
  suspended: 4
  revoked: 7
  expired: 12
  expiredDocuments: 18
alerts:
- 14 applications past their decision date
- 6 possible duplicates waiting
- 9 Emirates IDs expire before the event
- Media category at 94% of quota (470 of 500)
```

#### Permissions

- `listAccreditationApplications` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationCredentials` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationDocuments` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationIdentityConflicts` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.18 | Document Management - System shall support storage of accreditation-related documents. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |
| 12.1.19 | Identity Verification - System shall support identity verification before accreditation approval. | Accreditation & Credential Management | CONTRACTED | `listAccreditationDocuments` |
| 12.1.22 | QR Credential Support - System shall support QR-based accreditation credentials. | Accreditation & Credential Management | CONTRACTED | data `AccreditationCredential` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-615` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-615`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 1: Opens Accreditation Command Center → Executive and operational landing screen for the accreditation module.
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F217 branch at step 1 (expected): when Nothing has been set up on Accreditation Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F217 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-615?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-616`, `BO-617`, `BO-618`, `BO-619`, `BO-620`, `BO-621`, `BO-622`, `BO-623`, `BO-624`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-616` Accreditation Application Directory

**Central repository of all accreditation applications.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-616 |
| Who uses it | venue staff holding `ACCREDITATION_APPLY`, `ACCREDITATION_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each application record shall display) and no metric row |
| Offline | online only |
| Opens with | `applicationId` (navigation) |
| Route | `/access-venue/accreditation-application-directory-bo-616` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Every accreditation application, searchable and filterable, for the accreditation team and supervisors who answer "where is this person's application". Each row joins the application with its holder, its credential and its reviewer so the answer needs no second screen. The one thing to get right: the status chip distinguishes the application's state from the holder's (an approved application whose holder is now suspended), using the pack's nine status words.

**Known correction pending (do not draw the wrong version)**

- **Photograph, Event, Venue, Assigned reviewer, Credential status and Expiry date are not on AccreditationApplication** Why: They come from the holder, the programme, the approvals request and the credential; the directory needs a joined read or these columns cannot be filled. *(source: screens/P08-venue-back-office.yaml#BO-616 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No search or paging on the list read** Why: listAccreditationApplications filters only by programme, status and applicant type and returns an unpaged array; the pack's six search keys and a large programme need search and cursor paging. *(source: contracts/satellite/accreditation.yaml#listAccreditationApplications; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Pack statuses Suspended and Revoked are not application statuses** Why: They belong to the holder; draw them as a second chip, not as values of the application status filter. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationHolder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every accreditation application" and "The selected accreditation application"** Why: Generated placeholders; use "Applications" and the applicant's name. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which bulk actions does the client expect beyond export, assign and withdraw?** → Drawn default accepted: Draw those three; leave a greyed "More actions". *(decided by Chinmay, 2026-10-02; DEC-447 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationApplications` ?programmeId |
| Status | text field | — | — | `listAccreditationApplications` ?status |
| Applicant type | text field | — | — | `listAccreditationApplications` ?applicantType |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search**: One box for applicant name, email, mobile, organisation, accreditation number or credential ID; the type is detected (an email by "@", a credential ID by its prefix) and shown as a chip "Searching credential ID". *(source: screens/P08-venue-back-office.yaml#BO-616)*
- **Filters**: Programme, Event, Category, Applicant type, Organisation, Status (multi), Reviewer, Submitted between. *(source: screens/P08-venue-back-office.yaml#BO-616 / contracts/satellite/accreditation.yaml#listAccreditationApplications)*

#### Outputs: what the screen shows and produces

**Shown**

**Every accreditation application** (data table)

| Shows | Format | Notes |
|---|---|---|
| Application ID | text | not in the schema: `Application ID` |
| Applicant name | text | not in the schema: `Applicant name` |
| Photograph | text | not in the schema: `Photograph` |
| Accreditation category | text | not in the schema: `Accreditation category` |
| Organization/company | text | not in the schema: `Organization/company` |
| Event | text | not in the schema: `Event` |
| Venue | text | not in the schema: `Venue` |
| Submission date | text | not in the schema: `Submission date` |
| Current status | text | not in the schema: `Current status` |
| Assigned reviewer | text | not in the schema: `Assigned reviewer` |
| Credential status | text | not in the schema: `Credential status` |
| Expiry date | text | not in the schema: `Expiry date` |

**The selected accreditation application** (detail panel): The pack groups this record's detail under its own headings: “Scope of Work”.

| Shows | Format | Notes |
|---|---|---|
| Application ID | text | not in the schema: `Application ID` |
| Applicant name | text | not in the schema: `Applicant name` |
| Photograph | text | not in the schema: `Photograph` |
| Accreditation category | text | not in the schema: `Accreditation category` |
| Organization/company | text | not in the schema: `Organization/company` |
| Event | text | not in the schema: `Event` |
| Venue | text | not in the schema: `Venue` |
| Submission date | text | not in the schema: `Submission date` |
| Current status | text | not in the schema: `Current status` |
| Assigned reviewer | text | not in the schema: `Assigned reviewer` |
| Credential status | text | not in the schema: `Credential status` |
| Expiry date | text | not in the schema: `Expiry date` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Applications table**: Columns in the pack's order: Application ID (reference), Applicant (photo thumbnail and name), Category, Organisation, Event, Venue, Submitted, Status, Assigned reviewer, Credential status, Expiry. Status words map as Draft, Submitted, Under review, Additional information required (informationRequested), Approved, Rejected, Withdrawn, Expired; holder states Suspended and Revoked appear as a second chip beside an Approved status. Sort by Submitted, newest first. Title "Applications". *(source: screens/P08-venue-back-office.yaml#BO-616 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication)*
- **Detail panel**: Requirement checklist, decision reason where decided, decision due where open, credential and its status, and links to the holder record (BO-626) and the review workspace (BO-636). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Withdraw on the applicant's behalf**: Only for draft, submitted, under review or information required; asks for a reason (the applicant's words, e.g. "Assignment cancelled by employer"); a decided application shows no Withdraw. *(source: contracts/satellite/accreditation.yaml#withdrawAccreditationApplication)*
- **Bulk actions**: With rows selected: Export, Assign reviewer, Withdraw (where every selected row allows it); each shown only to users with the permission and confirming with the count ("Withdraw 3 applications"). *(source: screens/P08-venue-back-office.yaml#BO-616)*

**Data it reads**: `listAccreditationApplications` (onLoad, The directory)

**Where the user goes next**

- → `BO-615` Accreditation Command Center: *Back to Accreditation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation application list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation application untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation application yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation application are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The application is already decided, withdrawn or expired |

#### Edge cases to draw

- **Organisation submitted 200 applications at once**: Filtering by organisation shows the batch with a count; cursor paging keeps the list usable. *(source: DI-664)*
- **Search by Emirates ID or passport number**: Not offered in the free box; an exact-match identity search sits behind its own permission and is logged, because the number is stored encrypted. *(source: ADR-0063)*

#### Consistency with other screens

- Match `BO-625`: Holder directory uses the same status chips and the same search box behaviour.
- Match `BO-635`: The review queue is this directory pre-filtered to Submitted and Under review, sorted by decision due.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- id: ACR-2026-004417
  applicant: Rahul Menon
  category: Contractor
  organisation: Falcon Stage Rigging LLC
  event: Winter Festival 2026
  venue: Summit Peaks
  submitted: 07 Oct 2026
  status: Additional information required
  reviewer: Fatima Al Hashimi
  credential: None
  expiry: '-'
- id: ACR-2026-004388
  applicant: Omar Haddad
  category: Contractor
  organisation: Falcon Stage Rigging LLC
  event: Winter Festival 2026
  venue: Summit Peaks
  submitted: 02 Oct 2026
  status: Approved + Suspended
  reviewer: Ahmed Al Mansoori
  credential: Printed badge - issued
  expiry: 14 Dec 2026
```

#### Permissions

- `listAccreditationApplications` → `ACCREDITATION_VIEW` (read) · staff
- `withdrawAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-616` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-616`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 2: Works in Accreditation Application Directory → Central repository of all accreditation applications.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-616?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-615`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-617` New Accreditation Application

**Allow authorized backend personnel to manually create accreditation applications.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-617 |
| Who uses it | venue staff holding `ACCREDITATION_APPLY` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `applicationId` (navigation) |
| Route | `/access-venue/new-accreditation-application-bo-617` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Accreditation staff create an application on someone's behalf: a walk-in at the accreditation desk, a government liaison who sent details by letter, or a member of a partner company whose coordinator phoned. The operator picks the programme, category and applicant type first, and the same form the applicant would see renders below. The one thing to get right: the operator gets the same OCR, duplicate block and submit checks as the portal, with no shortcut around them.

**Known correction pending (do not draw the wrong version)**

- **Only Create and Cancel buttons, and the gap note says the pack gives nothing that can be drawn** Why: Pack page 5 lists seven selections and nine applicant fields; and the screen needs Save draft and Submit, both bound. *(source: screens/P08-venue-back-office.yaml#BO-617 / contracts/satellite/accreditation.yaml#submitAccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The application has no event, venue or requested-validity field** Why: The pack asks the operator to select event, venue and validity period; AccreditationApplication carries only programme and category, so a multi-event programme cannot record which event was requested. *(source: screens/P08-venue-back-office.yaml#BO-617 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Duplicate identity is accepted and queued** Why: Same conflict as ACC-002; the client agreed duplicates are blocked. *(source: contracts/satellite/accreditation.yaml#createAccreditationApplication / DI-692; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should staff be able to submit despite a requirement that blocks submission (for example a VIP whose letter will follow)?** → Drawn default accepted: No override; the operator records the application as a draft. *(decided by Chinmay, 2026-10-02; DEC-448 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Programme, category, applicant type**: In that order, each filtering the next; category shows its quota left ("Media - 30 of 500 left"). Event and venue are chosen from the programme's events and venues (a single value is pre-selected). *(source: screens/P08-venue-back-office.yaml#BO-617 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Organisation**: A search-select of existing organisations; required where the category's requirements include organisation confirmation. *(source: screens/P08-venue-back-office.yaml#BO-617 / DI-655)*
- **Applicant information**: Rendered from the programme's form and requirement rows (full name, identification, contact, job title, nationality where permitted, emergency contact where configured), with the identity document upload and OCR at the top, exactly as on ACC-002. *(source: screens/P08-venue-back-office.yaml#BO-617 / DI-658 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*
- **Photograph**: Upload or capture from a desk camera, with the crop guide and photo rules of BO-628. *(source: screens/P08-venue-back-office.yaml#BO-617 / screens/P08-venue-back-office.yaml#BO-628)*
- **Supporting documents**: One slot per document requirement, labelled by requirement, with expiry where the document has one. *(source: contracts/satellite/accreditation.yaml#submitAccreditationDocument)*
- **Validity period**: Shown read-only from the programme ("Valid 01-14 Dec 2026"); the reviewer sets the granted validity at approval. *(source: contracts/satellite/accreditation.yaml#decideAccreditationApplication)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Requirement checklist**: Same checklist as ACC-002, split into needed to submit and needed before approval. *(source: contracts/satellite/accreditation.yaml#submitAccreditationApplication)*
- **Entered by**: "Entered by Fatima Al Hashimi on behalf of the applicant" on the application, so the reviewer knows it did not come from the portal. *(source: DI-655 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationApplication)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save draft**: Creates the application as a draft; the operator can come back to it from BO-616. *(source: contracts/satellite/accreditation.yaml#createAccreditationApplication / contracts/satellite/accreditation.yaml#updateAccreditationApplication)*
- **Submit application**: Submits; a 422 lists unmet requirements that block submission against their slots. On success opens the application in BO-616 with "Submitted - decision due 18 Oct". *(source: contracts/satellite/accreditation.yaml#submitAccreditationApplication)*
- **Import a roster instead**: A link for many people at once to the bulk import (BO-680), where each row still passes the same checks. *(source: DI-664 / contracts/satellite/accreditation.yaml#importAccreditationHolders)*

**Where the user goes next**

- → `BO-615` Accreditation Command Center: *Back to Accreditation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The new accreditation application list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the new accreditation application untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No new accreditation application yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the new accreditation application are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not a draft, or the programme's application window is closed; 409 The application is not draft or informationRequested; 422 A requirement that blocks submission is not satisfied; 422 A subject field fails its requirement row's fieldType or validation |

#### Edge cases to draw

- **Identity number already accredited**: Blocked at the identity section with a link to the existing holder record (staff may see whose it is). *(source: DI-692 / DI-659)*
- **Programme window closed**: Submit disabled with the closing date; staff with configuration rights see a link to BO-624 to reopen. *(source: contracts/satellite/accreditation.yaml#submitAccreditationApplication)*

#### Consistency with other screens

- Match `ACC-002`: Same form renderer, same OCR behaviour, same duplicate message (staff variant links to the holder).
- Match `BO-616`: Saved drafts appear in the directory with status Draft and "Entered by staff".

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programme: Summit Peaks Winter Festival 2026 accreditation
category: Government or authority
applicantType: Civil defence liaison
organisation: Abu Dhabi Civil Defence
applicant:
  name: Khalid Al Zaabi
  document: Emirates ID ending 0942
  jobTitle: Fire safety officer
enteredBy: Fatima Al Hashimi
```

#### Permissions

- `createAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `updateAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest
- `submitAccreditationApplication` → `ACCREDITATION_APPLY` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.2 | Accreditation Registration System shall support accreditation applications through configurable forms. | Accreditation & Credential Management | CONTRACTED | `updateAccreditationApplication` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The venue creates a partner/company account (main or sub-accounts) whose users log in and submit accreditation for their members; entry can be done by the end user or by the admin team on their behalf. *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-655)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-617` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-617`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 4: Works in New Accreditation Application → Allow authorized backend personnel to manually create accreditation applications.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-617?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create, Cancel.
- [ ] Every transition is wired: `BO-615`.
- [ ] Every gated control is gated: `ACCREDITATION_APPLY`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-618` Accreditation Form Builder

**Configure applicant-facing registration forms without software development.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `accreditation` module |
| Block | Block A · ticket #28875 (APP-SETUP-BO-618) |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`, `GUEST_VIEW`, `MARKETING_MANAGE`, `MARKETING_VIEW` (2 configure, 3 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Fields may be configured as) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `programmeId` (navigation), `formId` (navigation) |
| Route | `/access-venue/accreditation-form-builder-bo-618` |

**Known gaps.** **Accreditation Form Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The back office builds the registration form an accreditation applicant fills in (media, corporate, individual), without development. The form is a marketing-crm form of kind registration, linked to the programme. The customer-marketing rule that matters: a published form version is immutable once anyone has submitted against it. A change makes a new version, and the old one stays readable forever.

**Fixed on main** (the package already carries these; draw what it says): The screen has createForm but no listForms or getForm, so existing forms cannot be opened or versioned. (CHG-WIR-005); Components are a text field labelled "Mandatory / Optional / Conditional / Hidden" and a select labelled "Key requirement - 12.1.2". (CHG-SBO-013).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Field requirement | select field | — | — | — | — | Per field: mandatory, optional, conditional or hidden. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Waiver · Survey · Data capture · Consent form · Incident report · Registration | `listForms` ?kind |
| Is template | toggle | — | — | `listAccreditationProgrammes` ?isTemplate |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Field visibility**: Each field is Mandatory, Optional, Conditional (shown when another answer matches) or Hidden. This is a segmented control per field, not a text box. *(source: screens/P08-venue-back-office.yaml#BO-618; contracts/satellite/marketing-crm.yaml#createForm)*
- **Category**: Each applicant category (media, corporate, individual guest) has its own form; the programme links a category to an event, venue or season. *(source: DI-656)*
- **Signature**: Requiring a signature turns the form into a waiver-like declaration; say so beside the toggle. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/FormDefinition)*

#### Outputs: what the screen shows and produces

**Shown**

**Show the programmes, the one being changed among them** (card list, from `listAccreditationProgrammes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Applications open at | 1 Oct 2026, 14:30 | — |
| Applications close at | 1 Oct 2026, 14:30 | — |
| Is template | yes / no (icon or chip) | 12.1.56. A reusable programme template: never opened for applications, and what `cloneAccreditationProgramme` copies its categories … |
| Status | chip: Draft, Open, Closed, Archived | — |

**Forms** (data table, from `listForms`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Name | text | — |
| Kind | chip: Waiver, Survey, Data capture, Consent form, Incident report, Registration | — |
| Consent purposes | list or chips (count when long) | What a `consentForm` consents to (Chinmay, 2 October, batch 4; follows BO-188: biometric capture needs consent on the venue's own form … |
| Fields | list or chips (count when long) | — |
| Key | text | — |
| Label | text | — |
| Label localised | grouped details | — |
| Type | chip: Text, Long text, Number, Date, Select, Multi select… | — |
| Options | list or chips (count when long) | — |
| Is required | yes / no (icon or chip) | — |
| Is personal data | yes / no (icon or chip) | Marked at the field, because retention is decided at the field. A survey answer and a medical condition on the same form have different … |
| Consent purpose | the name it points at, never the id | — |
| Show when | grouped details | — |
| Requires signature | yes / no (icon or chip) | What makes it a waiver. And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it. |
| Signature kind | chip: Drawn, Typed, Checkbox, None | — |
| Score scale | chip: Nps, Csat, Ces, Likert5, Likert7, Stars | What makes it a survey. Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's. |
| Applies to products | list or chips (count when long) | — |
| Valid for months | 1,234 | How long an acceptance lasts. A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to … |

**The form** (detail panel, from `getForm`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Kind | chip: Waiver, Survey, Data capture, Consent form, Incident report, Registration | — |
| Consent purposes | list or chips (count when long) | What a `consentForm` consents to (Chinmay, 2 October, batch 4; follows BO-188: biometric capture needs consent on the venue's own form … |
| Fields | list or chips (count when long) | — |
| Key | text | — |
| Label | text | — |
| Label localised | grouped details | — |
| Type | chip: Text, Long text, Number, Date, Select, Multi select… | — |
| Options | list or chips (count when long) | — |
| Is required | yes / no (icon or chip) | — |
| Is personal data | yes / no (icon or chip) | Marked at the field, because retention is decided at the field. A survey answer and a medical condition on the same form have different … |
| Consent purpose | the name it points at, never the id | — |
| Show when | grouped details | — |
| Field | text | — |
| Equals | text | — |
| Requires signature | yes / no (icon or chip) | What makes it a waiver. And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it. |
| Signature kind | chip: Drawn, Typed, Checkbox, None | — |
| Score scale | chip: Nps, Csat, Ces, Likert5, Likert7, Stars | What makes it a survey. Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's. |
| Applies to products | list or chips (count when long) | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Version badge**: "Version 3 - published 12 Oct 2026 - 41 submissions" with "Editing creates version 4". *(source: contracts/satellite/marketing-crm.yaml#createForm)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Link to programme**: Sets the programme's form; the programme's requirements matrix (not the form) decides what blocks submission and approval. *(source: contracts/satellite/accreditation.yaml#updateAccreditationProgramme)*

**Data it reads**: `listForms` (onLoad, The builder's list of forms); `listAccreditationProgrammes` (onLoad, Show the programmes, the one being changed among them)

**Where the user goes next**

- → `BO-615` Accreditation Command Center: *Back to Accreditation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation form configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation form untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation form configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A template cannot be opened for applications |

#### Consistency with other screens

- Match `CMS-043`: The waiver and form builder uses the same field palette and the same version behaviour.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form: Media accreditation - Coastal Aqua Summer Festival 2026
fields:
- Full name (mandatory)
- Outlet (mandatory)
- Press card photo (mandatory)
- Camera equipment (conditional - if Photographer)
- Emirates ID (optional)
```

#### Permissions

- `createForm` → `MARKETING_MANAGE` (configure) · staff
- `updateAccreditationProgramme` → `ACCREDITATION_CONFIGURE` (configure) · staff
- `listForms` → `MARKETING_VIEW` (read) · staff
- `getForm` → `GUEST_VIEW` (read) · staff, guest
- `listAccreditationProgrammes` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

75 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.13 | The system should provide the ability to capture configurable survey data. e.g. nationality, residency, guest type (individual, group, ...) in the POS and self-service kiosks. The survey should be … | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.5.3 | The system should collect demographic data about guests and transfer to Guest 360 (CRM) through API integration. The data to be collected should be configurable. | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.7.22 | It is expected to have the Reseller collecting the Guest information to be filled in online in order for FE to retrieve them. | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.7.28 | The Guest information collected by the Market place are available for FE who can use it for future marketing campaigns. | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.8.6 | The system should be able to prompt call center agents for entry of market sampling questions, several customizable data points and demographic data collection capabilities, e.g. country code, first … | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.12.6 | The system should be able to capture guest information for marketing purposes. This will include: Name, country/region of origin, email address, and phone / Mobile number. Data validation rules … | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.12.7 | The system should allow configuration of optional/mandatory parameters for the guest data to be collected. The mandatory parameters should be allowed to configured based on certain parameter. Example … | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.12.8 | The system should allow configuration of data validation rules on the guest data being collected to ensure the correctness of the information. | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.12.9 | The system should allow the selection of the data entry personnel for the required parameters. I.e. which field should be entered by the venue (client) user and which fields should be completed by … | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.12.10 | The system should provide the ability to capture configurable survey data from the guests. The survey can be configured to appear in the different points of the purchase journey. | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.12.20 | Annual Pass Products 1) Customers must first fill in personal information via the annual pass registration page or can go to the ticket counter onsite to purchase Annual Pass Ticket 2) At the … | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.12.31 | On the order, it must be possible to register: • The customer • the PLU, • the visit date, • the number of guests, • guest information (name, email, phone, address) which is configurable by the … | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| … 63 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-618` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-618`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 6: Works in Accreditation Form Builder → Configure applicant-facing registration forms without software development.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-618?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-615`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`, `GUEST_VIEW`, `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-619` Accreditation Category Management

**Configure reusable accreditation categories.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-619 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `programmeId` (navigation) |
| Route | `/access-venue/accreditation-category-management-bo-619` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where an accreditation administrator defines the categories people are accredited under (Staff, Contractor, Vendor, Media, VIP, Guest, Government or authority, Security, Medical, Operations, Sponsor, Production crew) and each category's defaults. In the contract a category lives inside a programme, so this screen edits the categories of the programme in hand. The one thing to get right: quota is shown as used against limit, because a category without a counted quota is the overrun the client worries about.

**Known correction pending (do not draw the wrong version)**

- **The pack asks for reusable categories with defaults for form, workflow, credential design, access profile, validity, required documents, identity verification and notification rules, plus active/inactive, effective dates and versioning** Why: The contract holds categories per programme with only access profile, quota and badge template; form, workflow, validity, documents, verification and notifications are per programme or per requirement row, and there is no status, effective date or version. Grey the missing defaults (per VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-619 / screens/P08-venue-back-office.yaml#BO-620 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The dataTable has no columns and the gap says nothing can be drawn** Why: The pack lists twelve categories and eight defaults; the contract gives five columns. *(source: screens/P08-venue-back-office.yaml#BO-619; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Only listAccreditationProgrammes is bound; the screen has no write (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are categories reusable across programmes (a tenant library) or defined per programme?** → Drawn default accepted: Per programme, with "Copy categories from another programme" (the clone operation's categories option). *(decided by Chinmay, 2026-10-02; DEC-449 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Is template | toggle | — | — | `listAccreditationProgrammes` ?isTemplate |

**Form: Save categories** (modal, opened by *Save categories*; *Save categories* calls `updateAccreditationProgramme`, *Cancel* sends nothing)

**Collects what `updateAccreditationProgramme` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `updateAccreditationProgramme` body |
| Code `code` | text field | required | — | — | — | — | `updateAccreditationProgramme` body |
| Name `name` | text field | required | — | — | — | — | `updateAccreditationProgramme` body |
| Venues `venueIds` | multi-picker: choose venues | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Events `eventIds` | multi-picker: choose events | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Categories `categories` | repeatable rows | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Code `categories[].code` | text field | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Name `categories[].name` | text field | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Default access profile `categories[].defaultAccessProfileId` | picker: choose a default access profile | optional | — | — | shows names, sends the id | — | `updateAccreditationProgramme` body |
| Quota `categories[].quota` | number field | optional | — | — | — | A cap on how many may be accredited in this category. Without one, a category is a promise nobody counted. | `updateAccreditationProgramme` body |
| Badge template `categories[].badgeTemplateId` | picker: choose a badge template | optional | — | — | shows names, sends the id | The badge printed for this category; travels with the category when a programme is cloned | `updateAccreditationProgramme` body |
| Applicant types `applicantTypes` | list of values (chips) | optional | — | — | — | — | `updateAccreditationProgramme` body |
| Applications open at `applicationsOpenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccreditationProgramme` body |
| Applications close at `applicationsCloseAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccreditationProgramme` body |
| Approval workflow `approvalWorkflowId` | picker: choose an approval workflow | optional | — | — | shows names, sends the id | — | `updateAccreditationProgramme` body |
| Form `formId` | picker: choose a form | optional | — | — | shows names, sends the id | 12.1.2. The `marketing-crm` form definition (`createForm`, BO-618) the applicant fills in. | `updateAccreditationProgramme` body |
| Is template `isTemplate` | toggle | optional | off | — | — | 12.1.56. A reusable programme template: never opened for applications, and what `cloneAccreditationProgramme` copies its categories, requirements, validity, notification rules and … | `updateAccreditationProgramme` body |
| Status `status` | radio group | optional | — | Draft · Open · Closed · Archived | — | — | `updateAccreditationProgramme` body |
| Face matching `faceMatching` | group | optional | — | Face matching for duplicate applicants: only where the venue enables it, with each applicant's consent and the venue's legal sign-off; off by default (Chinmay, 2 October, workbook Q461; ADR-0063 …; Enabling needs `legalSignOffRef` (the venue's legal sign-off … | — | Face matching for duplicate applicants: only where the venue enables it, with each applicant's consent and the venue's legal sign-off; off by default (Chinmay, 2 October, workbook … | `updateAccreditationProgramme` body |
| Enabled `faceMatching.enabled` | toggle | optional | off | — | — | — | `updateAccreditationProgramme` body |
| Legal sign off ref `faceMatching.legalSignOffRef` | text field | optional | — | — | — | The venue's legal sign-off document (a stored file reference). | `updateAccreditationProgramme` body |
| Identity verification `identityVerification` | group | optional | — | — | — | UAE Pass and ICP verification, in release 1 (Chinmay, 2 October, workbook Q457; CHG-CSA-031). | `updateAccreditationProgramme` body |
| Methods `identityVerification.methods` | multi-select chips | optional | — | Uae pass · Icp · Manual review | — | — | `updateAccreditationProgramme` body |
| Required `identityVerification.required` | toggle | optional | off | — | — | Whether an application is blocked from approval until a listed check passes. | `updateAccreditationProgramme` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `updateAccreditationProgramme` body |

Errors to draw in the form: 409 A template cannot be opened for applications

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Programme**: Programme selector at the top; categories below belong to it. Opening from BO-620 carries the programmeId. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Category name and code**: Name in English and Arabic (per VO-R10); code short, upper-case, unique in the programme (MEDIA, CONTR, GOV). "Add category" offers the pack's twelve as suggestions, then a custom name. *(source: screens/P08-venue-back-office.yaml#BO-619)*
- **Default access profile**: Select from the venue's access profiles; shows the zones it opens in a tooltip. Empty means the reviewer must choose one at approval. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme / contracts/satellite/accreditation.yaml#listAccessProfiles)*
- **Quota**: Whole number of people, empty for no cap (shown as "No limit", with a nudge that uncapped categories are not counted). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Badge template**: Select from badge templates with a thumbnail; the colour stripe of the chosen template becomes the category colour across the module. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme / contracts/satellite/accreditation.yaml#/components/schemas/BadgeTemplate)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save categories (secondary button) | `updateAccreditationProgramme` PUT `/accreditation-programmes/{programmeId}` | AccreditationProgramme | AccreditationProgramme | 409 A template cannot be opened for applications | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Categories table**: Columns Category (colour swatch, name), Code, Default access profile, Quota ("38 of 50 used"), Badge template, Holders. Title "Categories". *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save categories**: Writes the whole programme with its category list (per VO-R04), so the editor opens pre-filled with the programme's other fields untouched. Confirmation names changes ("2 added, 1 quota changed"). *(source: contracts/satellite/accreditation.yaml#updateAccreditationProgramme)*
- **Remove category**: Blocked while applications or holders use it ("41 holders are in Media"); allowed only for an unused category, with confirmation. *(source: screens/P08-venue-back-office.yaml#BO-033)*

**Data it reads**: `listAccreditationProgrammes` (onLoad, Categories within a programme)

**Where the user goes next**

- → `BO-615` Accreditation Command Center: *Back to Accreditation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation category list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation category untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation category yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation category are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A template cannot be opened for applications |

#### Edge cases to draw

- **Quota lowered below the number already accredited**: Warn "48 already accredited; the new limit 40 stops new approvals but removes nobody". *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Programme is open**: Edits allowed; a banner says changes apply to applications from now on. *(source: designer default)*

#### Consistency with other screens

- Match `BO-620`: Programme setup's "Allowed categories" is this list; one editor, two entry points (per VO-R14).
- Match `BO-647`: Category colour equals the badge template's colour stripe.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programme: Summit Peaks Winter Festival 2026 accreditation
categories:
- name: Media
  code: MEDIA
  accessProfile: Media - all public zones and press centre
  quota: 470 of 500
  template: Media orange
- name: Contractor
  code: CONTR
  accessProfile: Build crew - back of house
  quota: 212 of 300
  template: Crew grey
- name: Government or authority
  code: GOV
  accessProfile: All zones - escorted none
  quota: No limit
  template: Authority red
```

#### Permissions

- `listAccreditationProgrammes` → `ACCREDITATION_VIEW` (read) · staff
- `updateAccreditationProgramme` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-619` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-619`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 8: Works in Accreditation Category Management → Configure reusable accreditation categories.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-619?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save categories.
- [ ] Every transition is wired: `BO-615`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-620` Accreditation Program Setup

**Create the accreditation program governing a particular event, venue, season or organization.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-620 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `programmeId` (navigation) |
| Route | `/access-venue/accreditation-program-setup-bo-620` |

**Known gaps.** **Accreditation Program Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The administrator creates the programme that governs accreditation for an event, a venue, a season or a standing scheme: its name and code, the events and venues it covers, when applications open and close, the categories and applicant types allowed, the registration form, and the approval workflow. Most programmes start as a copy of last season's or of a template. The one thing to get right: the dates (application window, accreditation period, event dates) are shown together on one timeline so a window that closes after the event starts is obvious.

**Known correction pending (do not draw the wrong version)**

- **Gap says the screen declares no write operation** Why: Stale; createAccreditationProgramme, updateAccreditationProgramme and cloneAccreditationProgramme are bound. *(source: contracts/satellite/accreditation.yaml#createAccreditationProgramme / contracts/satellite/accreditation.yaml#updateAccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Pack fields Accreditation period, Registration channel, Maximum application volume, Credential template and Default access profile have no programme field** Why: Period is AccreditationValidity (another write), template and access profile are per category, and channel and a programme-level maximum do not exist; grey the last two (per VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-620 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Buttons labelled Create and Cancel only** Why: The screen also saves, copies and saves as template. *(source: contracts/satellite/accreditation.yaml#cloneAccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "Temporary" accreditation a programme kind or a short validity within any programme?** → Drawn default accepted: A short validity; not a separate kind. *(decided by Chinmay, 2026-10-02; DEC-450 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Is template | toggle | — | — | `listAccreditationProgrammes` ?isTemplate |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start from**: "Blank", "A template" (listAccreditationProgrammes with isTemplate) or "Last season's programme"; copying shows ticks for what comes across: Categories, Requirements, Validity, Notification rules, Form (all ticked by default). *(source: contracts/satellite/accreditation.yaml#cloneAccreditationProgramme / MATRIX 12.1.56)*
- **Name and code**: Name in English and Arabic; code upper-case and unique in the tenant (SP-WF-2026). Required. *(source: contracts/satellite/accreditation.yaml#createAccreditationProgramme)*
- **Events and venues**: Multi-select of the venue's events and of venues (the switcher's venue pre-selected). A read-only "Programme kind" chip is derived: Event-specific (one event), Venue-specific (no event, one venue), Multi-venue, Seasonal. *(source: screens/P08-venue-back-office.yaml#BO-620 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme / MATRIX 12.1.38 / MATRIX 12.1.39)*
- **Application window**: Opens and closes as date and time in venue time; close must be after open; a close later than the first event day warns. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Applicant types**: Chips (Rigging crew, Caterer, Photographer, Broadcaster, Government liaison); each one used by a requirement row cannot be removed. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*
- **Registration form and approval workflow**: Select from the forms built on BO-618 and the published approval workflows, each with an Open link; both may be left empty while the programme is a draft. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme / MATRIX 12.1.2)*
- **Tenant, status, template origin**: Never inputs; tenant and venue from the session (per VO-R03), status changes only on BO-624, "Copied from Winter Festival 2025" shown read-only. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Programme timeline**: A month strip with the application window, the accreditation validity period and the event days as three bands (per VO-R01 a calendar offers Day, Week and Month; Month is the default here). *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Programmes list**: Columns Name, Code, Kind, Window, Status (Draft, Open, Closed, Archived, Template), Applications. Templates are listed in their own tab. *(source: contracts/satellite/accreditation.yaml#listAccreditationProgrammes)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Create programme**: Creates it as a draft; next steps panel lists what BO-624 will check. *(source: contracts/satellite/accreditation.yaml#createAccreditationProgramme)*
- **Save changes**: Writes the whole programme (per VO-R04); categories edited on BO-619 are kept because the form loaded them. *(source: contracts/satellite/accreditation.yaml#updateAccreditationProgramme)*
- **Copy programme**: Creates a new draft from the source with the chosen parts; never copies applications, holders or credentials, and says so. *(source: contracts/satellite/accreditation.yaml#cloneAccreditationProgramme)*
- **Save as template**: Marks it a template; a template can never be opened for applications. *(source: contracts/satellite/accreditation.yaml#updateAccreditationProgramme)*

**Data it reads**: `listAccreditationProgrammes` (onLoad, Templates to start from (isTemplate=true))

**Where the user goes next**

- → `BO-615` Accreditation Command Center: *Back to Accreditation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation program list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation program untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation program yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation program are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A programme with this code already exists at this scope; 409 A template cannot be opened for applications |

#### Edge cases to draw

- **Window closes after the event starts**: Amber warning on the timeline; saving allowed. *(source: designer default)*
- **Programme is open**: Event and venue lists can grow but not lose an entry that has applications; the reason is shown on the locked chip. *(source: designer default)*

#### Consistency with other screens

- Match `BO-619`: Allowed categories edits the same list as BO-619.
- Match `BO-624`: Opening, suspending and closing the programme happen on BO-624, never here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programmes:
- name: Summit Peaks Winter Festival 2026 accreditation
  code: SP-WF-2026
  kind: Event-specific
  window: 01 Oct - 10 Dec 2026
  status: Open
  applications: 1284
- name: Aqua Park Contractor Scheme 2026-27
  code: AP-CS-2627
  kind: Venue-specific
  window: 15 Sep 2026 - 31 Aug 2027
  status: Open
  applications: 233
- name: Festival template
  code: TPL-FEST
  kind: Template
  window: '-'
  status: Template
  applications: 0
```

#### Permissions

- `createAccreditationProgramme` → `ACCREDITATION_CONFIGURE` (configure) · staff
- `listAccreditationProgrammes` → `ACCREDITATION_VIEW` (read) · staff
- `cloneAccreditationProgramme` → `ACCREDITATION_CONFIGURE` (configure) · staff
- `updateAccreditationProgramme` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.8 | Accreditation Categories - System shall support configurable accreditation categories. | Accreditation & Credential Management | CONTRACTED | `createAccreditationProgramme` |
| 12.1.38 | Event-Specific Accreditation - System shall support accreditations linked to specific events. | Accreditation & Credential Management | CONTRACTED | `createAccreditationProgramme` |
| 12.1.39 | Venue-Specific Accreditation - System shall support venue-specific accreditations. | Accreditation & Credential Management | CONTRACTED | `createAccreditationProgramme` |
| 12.1.56 | Accreditation Templates - System shall support reusable accreditation templates. | Accreditation & Credential Management | CONTRACTED | `cloneAccreditationProgramme` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-620` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-620`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 10: Works in Accreditation Program Setup → Create the accreditation program governing a particular event, venue, season or organization.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-620?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create, Cancel.
- [ ] Every transition is wired: `BO-615`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-621` Applicant Type Configuration

**Configure operational rules according to the type of person being accredited. Rather than building completely separate systems for staff, contractors, media, VIPs, etc., TICVAI should provide one accreditation engine with configurable applicant types. For each type, administrators shall define: Mandatory information Required documents Identity verification requirement Sponsor requirement Organization requirement Approval path Default validity Credential type Default access rules Renewal eligibility This architecture significantly reduces duplicated configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-621 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/applicant-type-configuration-bo-621` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of accreditation requirements (only PUT /accreditation-requirements exists); affects BO-621 and BO-622.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where the administrator says, for each type of person (a rigger, a caterer, a broadcaster, a government liaison), what they must supply and how they are vetted, so one engine serves every population. In the contract an applicant type is a name on the programme and its rules are rows in the requirements matrix, so this screen is the requirements matrix seen one applicant type at a time. The one thing to get right: saving one type's rules must not wipe the other types' rows, because the save replaces the whole matrix.

**Known correction pending (do not draw the wrong version)**

- **setAccreditationRequirements is bound with no read** Why: There is no GET for the requirements matrix, so the editor cannot open pre-filled and a PUT would wipe rows it never loaded. *(source: contracts/satellite/accreditation.yaml#setAccreditationRequirements; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Approval path, default validity, credential type, default access rules and renewal eligibility per type** Why: The contract has applicant types only as strings and requirement rows; these five rules have no per-type field. *(source: screens/P08-venue-back-office.yaml#BO-622 / MATRIX 12.1.9 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Save and Cancel only, no list or editor drawn** Why: The gap note says nothing can be drawn; the pack lists ten rules per type. *(source: screens/P08-venue-back-office.yaml#BO-620; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are applicant types and categories two axes (a Contractor category with Rigging crew and Caterer types) or the same thing?** → Drawn default accepted: Two axes, as the matrix is keyed Programme by Category by Applicant type. *(decided by Chinmay, 2026-10-02; DEC-451 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Applicant type**: List of the programme's applicant types on the left; selecting one shows its rules. Add type adds to the programme's list. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*
- **Mandatory information, required documents, identity verification, sponsor and organisation requirement**: Each is a requirement row for this type with kind field, document, photo, declaration or backgroundCheck, a visibility (Mandatory, Optional, Conditional, Hidden) and two switches "Needed to submit" and "Needed before approval" (defaults off and on). Sponsor confirmation and organisation confirmation are document rows. *(source: screens/P08-venue-back-office.yaml#BO-620 / screens/P08-venue-back-office.yaml#BO-622 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*
- **Approval path, default validity, credential type, default access rules, renewal eligibility**: Shown greyed with "Set per programme or category today" (per VO-R13) until the contract holds them per type. *(source: screens/P08-venue-back-office.yaml#BO-622)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Type summary**: One sentence per type, e.g. "Rigging crew - 3 documents, identity verified, safety induction before approval". *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rules**: Sends the programme's entire matrix (all types, all categories) with this type's rows changed (per VO-R04); confirmation names the change ("Rigging crew - 1 requirement added"). Applications already submitted are re-checked against approval blockers, and the confirm says how many are affected. *(source: contracts/satellite/accreditation.yaml#setAccreditationRequirements)*

**Where the user goes next**

- → `BO-615` Accreditation Command Center: *Back to Accreditation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The applicant type list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the applicant type untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No applicant type yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the applicant type are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Type removed while applications use it**: Blocked with the count of applications of that type. *(source: designer default)*
- **New approval blocker added mid-programme**: The confirm says "38 submitted applications of this type will need it before approval". *(source: contracts/satellite/accreditation.yaml#setAccreditationRequirements)*

#### Consistency with other screens

- Match `BO-622`: Same rows and the same switches; this screen is BO-622 filtered to one applicant type (per VO-R14). Draw it as a view of BO-622, not a second editor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
types:
- type: Rigging crew
  rows:
  - Photograph - needed to submit
  - Emirates ID or passport - needed to submit
  - Contractor authorisation - needed before approval
  - Safety induction certificate - needed before approval, expires 12 months
- type: Broadcaster
  rows:
  - Photograph
  - Media identification
  - Employment letter
- type: Government liaison
  rows:
  - Government identification
  - Sponsor confirmation
```

#### Permissions

- `setAccreditationRequirements` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.9 | Staff Accreditation - System shall support staff accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.10 | Contractor Accreditation - System shall support contractor accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.11 | Vendor Accreditation - System shall support vendor accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.12 | Media Accreditation - System shall support media accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.13 | VIP Accreditation - System shall support VIP accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.14 | Guest Accreditation - System shall support guest accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.15 | Government Accreditation - System shall support government and authority accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-621` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-621`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 12: Works in Applicant Type Configuration → Configure operational rules according to the type of person being accredited. Rather than building completely separate systems for staff, contractors, media, VIPs, etc., TICVAI should provide one …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-621?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-615`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-622` Application Requirements Matrix

**Configure what an applicant must provide before an application can progress. The system shall allow administrators to configure requirements by: Program × Category × Applicant Type**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-622 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/application-requirements-matrix-bo-622` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The requirements matrix: for each programme, category and applicant type, what an applicant must provide and whether its absence stops submission, stops approval, or neither. It decides what the applicant's checklist says, what the submit check refuses and what keeps Approve disabled. The one thing to get right: the difference between "needed to submit" and "needed before approval" is visible in every cell, because a missing photo should not stop a midnight application but a missing background check must stop an approval.

**Known correction pending (do not draw the wrong version)**

- **No read for the matrix** Why: Only PUT /accreditation-requirements exists; the grid cannot open with current values and a save replaces rows it never saw. *(source: contracts/satellite/accreditation.yaml#setAccreditationRequirements; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Pack state "Not applicable" against contract visibility "hidden"** Why: Hidden means a form field that exists but is not shown; Not applicable means no row. Do not map one to the other. *(source: screens/P08-venue-back-office.yaml#BO-622 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only Save and Cancel are drawn** Why: The gap says nothing can be drawn; the pack gives the axes, nine requirements and four states. *(source: screens/P08-venue-back-office.yaml#BO-622; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does "expiry in months" mean the document must stay valid that long, or that a verified document must be re-supplied after that long?** → Drawn default accepted: Re-supply after that long; label "Valid for N months once verified". *(decided by Chinmay, 2026-10-02; DEC-452 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Grid axes**: Rows are requirements (Photograph, Passport or ID, Employment confirmation, Contractor authorisation, Media identification, Government identification, Sponsor confirmation, Vehicle information, Additional documents, plus custom); columns are category, with an applicant-type selector above (All types, or one). *(source: screens/P08-venue-back-office.yaml#BO-622 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*
- **Cell state**: Required, Optional, Conditional or Not applicable (the pack's words). Required and Conditional cells carry two small toggles "Submit" and "Approval" for blocksSubmission and blocksApproval. Not applicable means no row is written. *(source: screens/P08-venue-back-office.yaml#BO-622 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*
- **Requirement detail (side panel)**: Label (English and Arabic), kind (document, field, photo, background check, training, declaration, payment), expiry in months for documents that lapse, the condition for Conditional ("when Vehicle access = Yes"), and for field rows the form field it checks, its answer type and validation. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements / MATRIX 12.1.2)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Legend and counts**: "Media: 4 required (2 stop submission), 1 conditional"; a legend explains the two toggles in one line each. *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save matrix**: Sends the whole matrix for the programme (per VO-R04); confirmation counts added, removed and changed rows and the applications affected. *(source: contracts/satellite/accreditation.yaml#setAccreditationRequirements)*
- **Copy from another programme**: Uses the clone operation's requirements option into a draft programme; not offered on an open programme. *(source: contracts/satellite/accreditation.yaml#cloneAccreditationProgramme)*

**Where the user goes next**

- → `BO-615` Accreditation Command Center: *Back to Accreditation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The application requirements list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the application requirements untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No application requirements yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the application requirements are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A field row points at a form field that no longer exists on the form**: The row shows "Form field missing" in red and the save warns. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationRequirements)*
- **Condition refers to a requirement that is Not applicable for that category**: Refused on save with the row named. *(source: designer default)*

#### Consistency with other screens

- Match `BO-621`: BO-621 is this grid filtered to one applicant type (per VO-R14).
- Match `ACC-002`: Labels here are the labels applicants read in their checklist.
- Match `BO-624`: The publication checklist item "Required documents configured" reads this matrix.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programme: Summit Peaks Winter Festival 2026 accreditation
rows:
- requirement: Photograph
  Media: Required - submit
  Contractor: Required - submit
  VIP: Required - approval
  Government: Required - approval
- requirement: Passport or Emirates ID
  Media: Required - submit
  Contractor: Required - submit
  VIP: Required - submit
  Government: Required - submit
- requirement: Contractor authorisation
  Media: Not applicable
  Contractor: Required - approval
  VIP: Not applicable
  Government: Not applicable
- requirement: Vehicle information
  Media: Conditional - when vehicle access = Yes
  Contractor: Conditional - when vehicle access = Yes
  VIP: Optional
  Government: Optional
```

#### Permissions

- `setAccreditationRequirements` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.9 | Staff Accreditation - System shall support staff accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.10 | Contractor Accreditation - System shall support contractor accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.11 | Vendor Accreditation - System shall support vendor accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.12 | Media Accreditation - System shall support media accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.13 | VIP Accreditation - System shall support VIP accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.14 | Guest Accreditation - System shall support guest accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |
| 12.1.15 | Government Accreditation - System shall support government and authority accreditation management. | Accreditation & Credential Management | CONTRACTED | `setAccreditationRequirements` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-622` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-622`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 14: Works in Application Requirements Matrix → Configure what an applicant must provide before an application can progress. The system shall allow administrators to configure requirements by: Program × Category × Applicant Type

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-622?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-615`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-623` Accreditation Intake Monitor

**Give operations teams visibility into incoming accreditation demand.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-623 |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The screen shall show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-intake-monitor-bo-623` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Operations' view of incoming demand: how many applications arrived today and this week, by category and organisation, how many are stuck (incomplete, waiting for documents, possible duplicates), and how the queue is ageing against its SLA. The one thing to get right: these are KPI tiles and charts with alerts, not columns of a table, and each opens the filtered applications.

**Known correction pending (do not draw the wrong version)**

- **The nine metrics are drawn as columns of a dataTable "Every accreditation intake" with a detail panel** Why: They are KPIs; draw tiles and charts (per VO-R02). The generated label is a placeholder. *(source: ADR-0041 / DI-653 / screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Counts by day, category and organisation must be computed from the full list** Why: The list read has no date filter, aggregation or paging. *(source: contracts/satellite/accreditation.yaml#listAccreditationApplications; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Duplicate candidates has no read bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should Intake Monitor stay a separate screen or become a tab of the Command Center?** → Drawn default accepted: A tab of BO-615. *(decided by Chinmay, 2026-10-02; DEC-453 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationApplications` ?programmeId |
| Status | text field | — | — | `listAccreditationApplications` ?status |
| Applicant type | text field | — | — | `listAccreditationApplications` ?applicantType |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Programme, Event, Category, Organisation; period Today, This week, Custom. *(source: screens/P08-venue-back-office.yaml#BO-622)*

#### Outputs: what the screen shows and produces

**Shown**

**Every accreditation intake** (data table)

| Shows | Format | Notes |
|---|---|---|
| Applications today | text | not in the schema: `Applications today` |
| Applications this week | text | not in the schema: `Applications this week` |
| Application volumes by category | text | not in the schema: `Application volumes by category` |
| Application volumes by organization | text | not in the schema: `Application volumes by organization` |
| Incomplete applications | text | not in the schema: `Incomplete applications` |
| Applications awaiting documents | text | not in the schema: `Applications awaiting documents` |
| Duplicate candidates | text | not in the schema: `Duplicate candidates` |
| Applications requiring review | text | not in the schema: `Applications requiring review` |
| SLA ageing | text | not in the schema: `SLA ageing` |

**Duplicate candidates** (data table, from `listAccreditationIdentityConflicts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Holders | list or chips (count when long) | — |
| Score | 1,234.5 | — |
| Matched on | list or chips (count when long) | — |
| Differing access | yes / no (icon or chip) | — |
| Status | chip: Pending, Merged, Rejected | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Surviving holder | the name it points at, never the id | The holder kept when the conflict was merged |
| Resolution reason | text | — |
| Resolved by principal | the name it points at, never the id | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**The selected accreditation intake** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Applications today | text | not in the schema: `Applications today` |
| Applications this week | text | not in the schema: `Applications this week` |
| Application volumes by category | text | not in the schema: `Application volumes by category` |
| Application volumes by organization | text | not in the schema: `Application volumes by organization` |
| Incomplete applications | text | not in the schema: `Incomplete applications` |
| Applications awaiting documents | text | not in the schema: `Applications awaiting documents` |
| Duplicate candidates | text | not in the schema: `Duplicate candidates` |
| Applications requiring review | text | not in the schema: `Applications requiring review` |
| SLA ageing | text | not in the schema: `SLA ageing` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Applications today, Applications this week (each with the change against the same day or week before), Incomplete (drafts and returned for information), Awaiting documents (a document requirement unmet), Duplicate candidates (pending identity conflicts), Requiring review (submitted and under review). *(source: screens/P08-venue-back-office.yaml#BO-622 / screens/P08-venue-back-office.yaml#BO-624)*
- **Volume charts**: Applications per day for the window as a line; by category and by organisation as horizontal bars (top 10 organisations, rest grouped). *(source: screens/P08-venue-back-office.yaml#BO-622)*
- **SLA ageing**: Four buckets by decision due date, Due later, Due within 24 h, Due today, Overdue, as a segmented bar with counts. *(source: screens/P08-venue-back-office.yaml#BO-624 / DI-661)*
- **Alerts**: "Applications today are 3 times the daily average" or "Media backlog: 62 waiting, 18 overdue", each as a suggestion with its reason (per VO-R11), never acting on its own. *(source: screens/P08-venue-back-office.yaml#BO-624 / DI-661)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Drill into a tile, bar or bucket**: Opens BO-616 (or BO-635 for review buckets, BO-631 for duplicates) filtered accordingly. *(source: screens/P08-venue-back-office.yaml#BO-624)*

**Data it reads**: `listAccreditationApplications` (onLoad, Intake monitor); `listAccreditationIdentityConflicts` (onLoad, Duplicate candidates among incoming applications)

**Where the user goes next**

- → `BO-615` Accreditation Command Center: *Back to Accreditation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation intake list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation intake untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation intake yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation intake are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A bulk import lands 1,000 applications from one organisation**: The day's volume spikes; the alert names the import ("Falcon Stage Rigging LLC import, 1,000 rows") rather than flagging abnormal demand. *(source: DI-664)*

#### Consistency with other screens

- Match `BO-615`: Same dashboard pattern; Intake can be a tab of the command centre (per VO-R02 and VO-R14).
- Match `BO-635`: SLA bucket thresholds match the review queue chips.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  today: 38
  thisWeek: 214
  incomplete: 57
  awaitingDocuments: 44
  duplicateCandidates: 6
  requiringReview: 237
slaAgeing:
  dueLater: 160
  within24h: 41
  dueToday: 22
  overdue: 14
topOrganisations:
- Falcon Stage Rigging LLC 212
- Gulf Lens Media 88
- Northbridge Events 41
```

#### Permissions

- `listAccreditationApplications` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationIdentityConflicts` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Submission tracking shows submitted, pending and missing-document applications. Upload accepts PDF, JPEG, PNG and enforces file-size/quality limits at upload time. *(client request · MoM 7 Sep 2026, 4.3 Application Requirements, Document Validation & OCR Auto-Fill · DI-657)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-623` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-623`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 16: Works in Accreditation Intake Monitor → Give operations teams visibility into incoming accreditation demand.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-623?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-615`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-624` Registration Rules & Publication

**Final governance screen before opening an accreditation program for applications. The system shall provide a validation checklist covering: Registration form configured Categories configured Required documents configured Approval workflow assigned Credential template assigned Validity rules configured Access profile assigned Notification templates configured Application period configured Provide a complete operational workspace to create, review, verify, maintain and audit accreditation holder profiles before any credential is approved or issued. This board shall manage the individual’s identity, organization relationship, photographs, documents, verification status, duplicate detection, profile history and compliance readiness. The accreditation holder profile shall act as the single source of truth for the person across accreditation programs, events and venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | Block D · task VM-BO-624 |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `programmeId` (navigation) |
| Route | `/access-venue/registration-rules-publication-bo-624` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): createAccreditationProgramme was bound as "Publish the rules"; publishing an existing programme is updateAccreditationProgramme with status open (already …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The last gate before a programme opens to applicants: a checklist that shows whether every part is configured, a preview of what applicants will see, and the controls that publish, suspend or close registration. The one thing to get right: Publish is impossible while a checklist item is missing, and every item names the screen that fixes it.

**Known correction pending (do not draw the wrong version)**

- **Suspend registration has no status** Why: Programme status is draft, open, closed or archived; there is no suspended state to pause and resume. *(source: screens/P08-venue-back-office.yaml#BO-624 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation reads the checklist items** Why: There is no validate operation, no read for requirements, validity or notification rules here; the checklist cannot be computed from what is bound. *(source: screens/P08-venue-back-office.yaml#BO-624 / contracts/satellite/accreditation.yaml#setAccreditationRequirements; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The screen's generated purpose runs into Board 2's objective text** Why: The purpose ends with "Provide a complete operational workspace to create, review, verify, maintain and audit accreditation holder p..." which is the next board's objective. *(source: screens/P08-venue-back-office.yaml#BO-625 / screens/P08-venue-back-office.yaml#BO-624; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): createAccreditationProgramme is bound as "Publish the rules", with Create and Cancel buttons (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should suspension be a programme state, or is closing and reopening enough?** → Drawn default accepted: Draw Suspend greyed with the reason "Not yet supported"; Close available. *(decided by Chinmay, 2026-10-02; DEC-454 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Programme**: Carried from BO-620 (programmeId); otherwise a selector. *(source: screens/P08-venue-back-office.yaml#BO-624)*
- **Reason (suspend or close)**: Required free text when suspending or closing an open programme; the applicant-facing message is a separate field shown on ACC-001. *(source: screens/P08-venue-back-office.yaml#BO-624)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validation checklist**: Nine rows in the pack's order, each Configured (green tick), Missing (red) or Not required (grey) with a Fix link: Registration form (BO-618), Categories (BO-619), Required documents (BO-622), Approval workflow (BO-637), Credential template (BO-647), Validity rules, Access profile per category, Notification templates, Application period (BO-620). *(source: screens/P08-venue-back-office.yaml#BO-624)*
- **Status and audit**: Current status (Draft, Open, Suspended, Closed) with "Last changed by Fatima Al Hashimi, 30 Sep 2026 16:10" (per VO-R05). *(source: screens/P08-venue-back-office.yaml#BO-624)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validate configuration**: Re-runs the checklist and shows the time of the check. *(source: screens/P08-venue-back-office.yaml#BO-624)*
- **Preview applicant journey**: Opens ACC-001 to ACC-003 in a preview frame with the tenant's branding and this programme's values; nothing can be submitted from the preview. *(source: screens/P08-venue-back-office.yaml#BO-624)*
- **Publish**: Disabled until every required item is Configured. Sets the programme open; confirmation names the window and the public link ("Applications open 01 Oct 2026, 09:00 to 10 Dec 2026, 18:00"). *(source: screens/P08-venue-back-office.yaml#BO-624 / contracts/satellite/accreditation.yaml#updateAccreditationProgramme)*
- **Suspend registration / Close registration**: Stops new submissions (drafts kept); confirmation names the number of open drafts that will not be able to submit. *(source: screens/P08-venue-back-office.yaml#BO-624)*

**Where the user goes next**

- → `BO-615` Accreditation Command Center: *Back to Accreditation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The registration rules publication list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the registration rules publication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No registration rules publication yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the registration rules publication are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A template cannot be opened for applications |

#### Edge cases to draw

- **Programme is a template**: Publish disabled with "Templates never open for applications; copy it into a programme first". *(source: contracts/satellite/accreditation.yaml#updateAccreditationProgramme)*
- **A required item breaks after publishing (form deleted, workflow deactivated)**: The checklist row turns red on the open programme and an alert appears on BO-615. *(source: designer default)*

#### Consistency with other screens

- Match `BO-643`: Board 3's publication screen uses the same checklist component and the same Save draft, Validate, Publish row.
- Match `ACC-001`: The closed and suspended messages applicants read come from here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programme: Summit Peaks Winter Festival 2026 accreditation
checklist:
  form: Configured
  categories: Configured
  documents: Configured
  workflow: Configured
  template: Configured
  validity: Missing
  accessProfile: Configured (7 of 7 categories)
  notifications: Missing
  period: Configured
```

#### Permissions

- `updateAccreditationProgramme` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-624` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-624`
- Workshop pack: ACCREDITATION.pdf board 1
- Flow F217 *ACCREDITATION board 1: Accreditation Command Center*, step 18: Works in Registration Rules & Publication → Final governance screen before opening an accreditation program for applications. The system shall provide a validation checklist covering: Registration form configured Categories configured Required …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-624?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-615`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
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
"cloneAccreditationProgramme": {"method":"POST","path":"/accreditation-programmes/{programmeId}/clone","contract":"accreditation","summary":"Start a programme from a template or last season's programme","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationProgramme"},
"createAccreditationApplication": {"method":"POST","path":"/accreditation-applications","contract":"accreditation","summary":"Apply, or apply on behalf of somebody","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationApplication","responds":"AccreditationApplication"},
"createAccreditationProgramme": {"method":"POST","path":"/accreditation-programmes","contract":"accreditation","summary":"Define a programme, its categories and its window","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationProgramme","responds":"AccreditationProgramme"},
"createForm": {"method":"POST","path":"/forms","contract":"marketing-crm","summary":"Define a waiver, survey or capture form","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FormDefinition","responds":"FormDefinition"},
"getForm": {"method":"GET","path":"/forms/{formId}","contract":"marketing-crm","summary":"One form, to fill in or to edit","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"FormDefinition"},
"listAccreditationApplications": {"method":"GET","path":"/accreditation-applications","contract":"accreditation","summary":"Applications, by state and programme","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"applicantType","in":"query","required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"listAccreditationCredentials": {"method":"GET","path":"/accreditation-credentials","contract":"accreditation","summary":"Badges and digital credentials issued","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"holderId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"AccreditationCredential"},
"listAccreditationDocuments": {"method":"GET","path":"/accreditation-documents","contract":"accreditation","summary":"Documents supplied, by holder, application, requirement or state","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"applicationId","in":"query","required":null},{"name":"holderId","in":"query","required":null},{"name":"requirementCode","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccreditationHolders": {"method":"GET","path":"/accreditation-holders","contract":"accreditation","summary":"Everybody accredited, and what state they are in","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"organisationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"listAccreditationIdentityConflicts": {"method":"GET","path":"/accreditation-identity-conflicts","contract":"accreditation","summary":"People who may already be accredited under another record","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccreditationIdentityConflict"},
"listAccreditationProgrammes": {"method":"GET","path":"/accreditation-programmes","contract":"accreditation","summary":"Programmes, their categories and their applicant types","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"isTemplate","in":"query","required":null}],"requestBody":null,"responds":"AccreditationProgramme"},
"listForms": {"method":"GET","path":"/forms","contract":"marketing-crm","summary":"Waivers, surveys and capture forms","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setAccreditationRequirements": {"method":"PUT","path":"/accreditation-requirements","contract":"accreditation","summary":"What each applicant type must supply and pass","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationRequirements","responds":"AccreditationRequirements"},
"submitAccreditationApplication": {"method":"POST","path":"/accreditation-applications/{applicationId}/submit","contract":"accreditation","summary":"Send a draft for review","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"},
"updateAccreditationApplication": {"method":"PUT","path":"/accreditation-applications/{applicationId}","contract":"accreditation","summary":"Save a draft, or amend an application returned for information","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationApplication","responds":"AccreditationApplication"},
"updateAccreditationProgramme": {"method":"PUT","path":"/accreditation-programmes/{programmeId}","contract":"accreditation","summary":"Amend a programme, link its registration form, or mark it a template","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationProgramme","responds":"AccreditationProgramme"},
"withdrawAccreditationApplication": {"method":"POST","path":"/accreditation-applications/{applicationId}/withdraw","contract":"accreditation","summary":"Withdraw an application before it is decided","permission":"ACCREDITATION_APPLY","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationApplication"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationApplication": {"type":"object","x-ticvai-persistence":"accreditation.application","description":"Board 1.3. **Usually submitted by an organisation on behalf of its people.**","required":["programmeId"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"applicantType":{"type":"string"},"submittedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"subject":{"type":"object","additionalProperties":true,"description":"Name, date of birth, nationality, contact — shaped by the requirements matrix."},"requirementStatus":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"requirementCode":{"type":"string"},"satisfied":{"type":"boolean"},"documentId":{"type":"string","format":"uuid","nullable":true}}}},"status":{"type":"string","enum":["draft","submitted","underReview","informationRequested","approved","rejected","withdrawn","expired"]},"decisionReason":{"type":"string","nullable":true},"missingRequirements":{"type":"array","readOnly":true,"description":"The requirement codes a reviewer returned the application for, or rejected it over — what the applicant must change before resubmitting","items":{"type":"string"}},"decisionDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a decision is due — the approvals request's SLA. **A date, not a queue position**"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"holderId":{"type":"string","format":"uuid","nullable":true},"renewsHolderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.37. Set by `renewAccreditation`; approval extends this holder rather than creating one"},"resubmissionOfApplicationId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"12.1.33. The rejected application this one resubmits, so the rejection stays in the record"},"resubmissionNote":{"type":"string","maxLength":1000,"nullable":true,"readOnly":true,"description":"What the applicant changed, from `resubmitAccreditationApplication`"},"submittedAt":{"type":"string","format":"date-time","nullable":true},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"AccreditationCredential": {"type":"object","x-ticvai-persistence":"accreditation.credential","description":"Board 4. **Not the accreditation** — reissuing one re-vets nobody.","required":["holderId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["printedBadge","mobileCredential","qr","nfcCard","rfidCard","wristband"]},"symbology":{"type":"string","nullable":true,"description":"12.1.22. **How `encodedIdentifier` is carried**, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a `mobileCredential`, a barcode where a printed badge carries one, `nfcNdef` or `rfidEpc` for an encoded card, `none` where nothing is encoded.\n","enum":["qr","dataMatrix","pdf417","aztec","code128","nfcNdef","rfidEpc","none"]},"serialNumber":{"type":"string","nullable":true},"encodedIdentifier":{"type":"string","nullable":true},"badgeTemplateId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"issuedBy":{"type":"string","format":"uuid"},"activatedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["pendingPrint","issued","active","lost","replaced","revoked","expired"]},"replacesCredentialId":{"type":"string","format":"uuid","nullable":true},"replacementCount":{"type":"integer","default":0},"scopePath":{"type":"string"}}},
"AccreditationDocument": {"type":"object","x-ticvai-persistence":"accreditation.document","description":"Board 2.5. **Submitted against a named requirement, not into a folder.**","required":["requirementCode","assetId"],"properties":{"id":{"type":"string","format":"uuid"},"holderId":{"type":"string","format":"uuid","nullable":true},"applicationId":{"type":"string","format":"uuid","nullable":true},"requirementCode":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"submittedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["submitted","verified","rejected","expired"]},"verifiedBy":{"type":"string","format":"uuid","nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**An insurance certificate valid until March accredits somebody until March**, whatever the programme says.\n"},"scopePath":{"type":"string"}}},
"AccreditationHolder": {"type":"object","x-ticvai-persistence":"accreditation.holder","description":"**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n","required":["id","fullName"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true},"nationality":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true,"description":"12.1.16. The holder's own address — where a mobile credential and renewal notices go"},"phone":{"type":"string","nullable":true,"description":"12.1.16. E.164"},"identityDocumentVerified":{"type":"boolean","default":false},"organisationId":{"type":"string","format":"uuid","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","suspended","revoked","expired","archived"]},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"completenessPercent":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationIdentityConflict": {"type":"object","x-ticvai-persistence":"accreditation.identity_conflict","description":"Board 2.7. **One badge revoked and the other still opening doors.**\n\n**`matchedOn` names `face` only where the programme's `faceMatching` is enabled** and both applicants consented (workbook Q461; CHG-CSA-031).\n\n**Stored, not recomputed on each read** (data model for the agreed operations, 29 September): a suspected pair is raised by `createAccreditationApplication` and `importAccreditationHolders` using `marketing-crm`'s identity resolution, and keeps its id and status while somebody decides it, so a pair rejected as two different people is not raised again on the next import. Resolved by `resolveIdentityConflict` (`pending` to `merged` or `rejected`, decided 29 September, writers pass); lifecycle in `states/accreditation-identity-conflict.yaml`.","required":["id","holderIds","status"],"properties":{"id":{"type":"string","format":"uuid"},"holderIds":{"type":"array","items":{"type":"string","format":"uuid"}},"score":{"type":"number"},"matchedOn":{"type":"array","items":{"type":"string"}},"differingAccess":{"type":"boolean"},"status":{"type":"string","enum":["pending","merged","rejected"]},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"survivingHolderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The holder kept when the conflict was merged"},"resolutionReason":{"type":"string","maxLength":500,"nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationProgramme": {"type":"object","x-ticvai-persistence":"accreditation.programme","description":"Boards 1.5 and 1.6. **The thing an application is made against.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"eventIds":{"type":"array","items":{"type":"string","format":"uuid"}},"categories":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"defaultAccessProfileId":{"type":"string","format":"uuid","nullable":true},"quota":{"type":"integer","nullable":true,"description":"**A cap on how many may be accredited in this category.** Without one, a category is a promise nobody counted.\n"},"badgeTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"The badge printed for this category; travels with the category when a programme is cloned"}}}},"applicantTypes":{"type":"array","items":{"type":"string"}},"applicationsOpenAt":{"type":"string","format":"date-time","nullable":true},"applicationsCloseAt":{"type":"string","format":"date-time","nullable":true},"approvalWorkflowId":{"type":"string","format":"uuid","nullable":true},"formId":{"type":"string","format":"uuid","nullable":true,"description":"12.1.2. The `marketing-crm` form definition (`createForm`, BO-618) the applicant fills in. The requirements matrix's `field` rows name the form fields they check, so the form is configured without software development and what blocks approval stays in one place.\n"},"isTemplate":{"type":"boolean","default":false,"description":"12.1.56. **A reusable programme template**: never opened for applications, and what `cloneAccreditationProgramme` copies its categories, requirements, validity, notification rules and form link from.\n"},"templateProgrammeId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The programme or template this one was cloned from"},"status":{"type":"string","enum":["draft","open","closed","archived"]},"faceMatching":{"type":"object","description":"**Face matching for duplicate applicants: only where the venue enables it, with each applicant's consent and the venue's legal sign-off; off by default** (Chinmay, 2 October, workbook Q461; ADR-0063; CHG-CSA-031). With `enabled` false, identity conflicts are raised on names, dates of birth and documents only and never on a face, and BO-631 shows no Face chip. Enabling needs `legalSignOffRef` (the venue's legal sign-off, recorded with who gave it and when), and a face is compared only for an applicant whose application carries a face-matching consent (the programme's consent form, CHG-CSA-026).","properties":{"enabled":{"type":"boolean","default":false},"legalSignOffRef":{"type":"string","nullable":true,"description":"The venue's legal sign-off document (a stored file reference)."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},"identityVerification":{"type":"object","description":"**UAE Pass and ICP verification, in release 1** (Chinmay, 2 October, workbook Q457; CHG-CSA-031). Which government identity checks an applicant passes through: UAE Pass sign-in (identity `guestUaePassLogin`) and the ICP identity check (access's verification adaptor). **Both need the client's access to the government services** (an external dependency); until it is granted, `methods` may name them but the check answers `manualReview`.","properties":{"methods":{"type":"array","items":{"type":"string","enum":["uaePass","icp","manualReview"]}},"required":{"type":"boolean","default":false,"description":"Whether an application is blocked from approval until a listed check passes."}}},"scopePath":{"type":"string"}}},
"AccreditationRequirements": {"type":"object","x-ticvai-persistence":"accreditation.requirements","description":"Board 1.8. **Blocking submission and blocking approval are not the same.**","properties":{"programmeId":{"type":"string","format":"uuid"},"rows":{"type":"array","items":{"type":"object","properties":{"applicantType":{"type":"string"},"categoryCode":{"type":"string","nullable":true},"requirementCode":{"type":"string"},"label":{"type":"string"},"kind":{"type":"string","enum":["document","field","photo","backgroundCheck","training","declaration","payment"]},"blocksSubmission":{"type":"boolean","default":false},"blocksApproval":{"type":"boolean","default":true},"expiryMonths":{"type":"integer","nullable":true},"formFieldKey":{"type":"string","nullable":true,"description":"For a `field` row, the key of the field on the programme's form that it checks"},"fieldType":{"type":"string","nullable":true,"description":"12.1.2. For a `field` row, what kind of answer it takes","enum":["text","email","phone","date","country","number","boolean","singleChoice","multipleChoice"]},"visibility":{"type":"string","default":"mandatory","description":"Pack page 5 (BO-618) — mandatory, optional, conditional on another answer, or hidden","enum":["mandatory","optional","conditional","hidden"]},"condition":{"type":"object","nullable":true,"description":"For `conditional`, the answer that makes this row apply","properties":{"requirementCode":{"type":"string"},"equals":{"type":"string"}}},"validation":{"type":"object","nullable":true,"description":"Checked on save and on submit; a failing answer is refused with the row's label","properties":{"pattern":{"type":"string","nullable":true},"minLength":{"type":"integer","nullable":true},"maxLength":{"type":"integer","nullable":true},"minValue":{"type":"number","nullable":true},"maxValue":{"type":"number","nullable":true},"allowedValues":{"type":"array","items":{"type":"string"}}}}}}},"scopePath":{"type":"string"}}},
"FormDefinition": {"type":"object","x-ticvai-persistence":"marketing.form_definition + marketing.form_definition_field","description":"CF-129, CL-04. **A waiver, a survey and a data-capture form are one mechanism.**\nA waiver is this form with a signature. A survey is this form with a scale. A demographic capture is this form at the point of sale. They were raised as three separate gaps and share every part: field configuration, conditional display, versioning, an acceptance record and a stored artefact.\n**Three implementations would drift on the version rule first.** A waiver signed against version 3 must stay bound to version 3, and that is the same requirement a survey has when question wording changes mid-campaign — **an NPS score means nothing if you cannot say which question produced it.**\n","required":["id","name","kind","version","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["waiver","survey","dataCapture","consentForm","incidentReport","registration"]},"consentPurposes":{"type":"array","description":"**What a `consentForm` consents to** (Chinmay, 2 October, batch 4; follows BO-188: biometric capture needs consent on the venue's own form; CHG-CSA-026). A guardian-signed form for a minor carries the guardian fields of the waiver builder (workbook Q237: guardian consent, configurable per country). Empty for any other kind.","items":{"type":"string","enum":["facePass","faceTag","marketing","photography","waiver"]}},"version":{"readOnly":true,"type":"integer","description":"**Set by the server** — 1 on `createForm`, the next number on every change. **Immutable once anything is submitted against it.** A change creates a new version, and the old one stays readable forever — 2.15.13 requires the exact accepted version retained, which is legal evidence rather than a nicety.\n"},"fields":{"type":"array","items":{"$ref":"#/components/schemas/FormField"}},"requiresSignature":{"type":"boolean","default":false,"description":"**What makes it a waiver.** And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it.\n"},"signatureKind":{"type":"string","enum":["drawn","typed","checkbox","none"],"default":"none"},"scoreScale":{"type":"string","nullable":true,"enum":["nps","csat","ces","likert5","likert7","stars"],"description":"**What makes it a survey.** Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's.\n"},"appliesToProductIds":{"type":"array","items":{"type":"string","format":"uuid"}},"validForMonths":{"type":"integer","nullable":true,"description":"**How long an acceptance lasts.** A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to sign again — which only works if the expiry is stated.\n"},"minimumAge":{"type":"integer","nullable":true},"requiresGuardianForMinors":{"type":"boolean","default":true,"description":"**A minor cannot waive their own rights.** A guardian signs, and the record has to name them — an unsigned or self-signed minor waiver is worth nothing at the moment it matters.\n"},"status":{"readOnly":true,"type":"string","enum":["draft","published","superseded","retired"]},"legalReviewedBy":{"type":"string","nullable":true},"legalReviewedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"FormField": {"type":"object","description":"One field. **Conditional display is the shared requirement** — a survey branching on an answer and a waiver revealing a medical question on a yes are the same mechanism.\n","required":["key","label","type"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"labelLocalised":{"type":"object","additionalProperties":{"type":"string"}},"type":{"type":"string","enum":["text","longText","number","date","select","multiSelect","boolean","scale","signature","file","phone","email"]},"options":{"type":"array","items":{"type":"string"}},"isRequired":{"type":"boolean","default":false},"isPersonalData":{"type":"boolean","default":false,"description":"**Marked at the field, because retention is decided at the field.** A survey answer and a medical condition on the same form have different lifetimes, and a form-level flag makes the whole thing as sensitive as its most sensitive field.\n"},"consentPurposeId":{"type":"string","format":"uuid","nullable":true},"showWhen":{"type":"object","nullable":true,"properties":{"field":{"type":"string"},"equals":{"type":"string"}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
