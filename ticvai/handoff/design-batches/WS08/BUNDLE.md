# WS08 — Access Control board 8

**10 screens · 19 operations · 28 schemas · 4 permissions**

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
  `ACCESS_POINT_CONFIGURE, QUEUE_MANAGE, QUEUE_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-214` | Guest Journey Command Center | B–D | 8 | 220 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-215` | Group & B2B Admission Profile Builder | B–D | 7 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-216` | Group Leader & Fast B2B Validation | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-217` | Group Attendance & Partial Entry Manager | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-218` | Family, Child, POD & Companion Journey | B–D | 13 | 0 | 5 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-219` | Re-entry & Temporary Exit Journey | B–D | 4 | 0 | 5 | 9 | 0 | 6 | — | notStarted (generated) |
| `BO-220` | Multi-Park & Crossover Journey Orchestrator | B–D | 47 | 0 | 6 | 9 | 0 | 6 | — | notStarted (generated) |
| `BO-221` | Fast Pass & Attraction Access Journey | B–D | 27 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-222` | Special Event, Free View & Alternative Admission | A | 15 | 0 | 5 | 1 | 0 | 0 | — | notStarted (generated) |
| `BO-223` | Journey Simulation, Audit & Publication | B–D | 8 | 26 | 6 | 9 | 0 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**BO-216, BO-217, BO-220, BO-222 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-214` Guest Journey Command Center

**Central configuration and monitoring screen for all special and multi-person admission journeys.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/guest-journey-command-center-bo-214` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Admission profiles are created on BO-032; a second create path on the command centre duplicates it (VO-R14) and a command centre carries no create forms (VO-R02) …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Board 8 command centre for admission journeys that are not "scan one ticket, admit one guest": school and B2B groups, families with children, POD companions and nannies, re-entry, multi-park crossover, Fast Pass, special events and VIP. Ten KPI tiles for today, the journey portfolio (journey, type, venue, credential, status), live journey health (delayed groups, high manual intervention, incomplete group entry, companion violations, crossover exceptions, Fast Pass anomalies) and AI lane advice. The one thing to get right: exceptions and live health come before the portfolio, and each journey type opens its board screen.

**Known correction pending (do not draw the wrong version)**

- **journeyType and credentialType are free strings** Why: The pack's portfolio uses a closed set (B2B group, family, multi-park, Fast Pass, VIP; group QR, mixed, QR/RFID, RFID, Face/QR); free text cannot drive filters or tiles. *(source: screens/P08-venue-back-office.yaml#BO-214 / contracts/spine/access.yaml#setJourneyProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Live journey health and AI alerts are not in the read** Why: The pack makes them the monitoring half of the screen. *(source: screens/P08-venue-back-office.yaml#BO-214 / contracts/spine/access.yaml#listGuestJourney; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every guest journey" and "The selected guest journey"; Save button in the action bar** Why: Generated placeholders ("Journey portfolio"); the save belongs in the journey editor drawer. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): createAdmissionRules ("start a new guest journey from an admission profile") is bound on the command centre (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Form: Save journey profile** (modal, opened by *Save journey profile*; *Save journey profile* calls `setJourneyProfile`, *Cancel* sends nothing)

**Collects what `setJourneyProfile` sends before it is called.** Required: `id`, `scopePath`, `name`, `status`. Optional: `venueId`, `journeyType`, `credentialType`, `steps`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | The journeyProfileId | `setJourneyProfile` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Null is every park of the tenant | `setJourneyProfile` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setJourneyProfile` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setJourneyProfile` body |
| Journey type `journeyType` | text field | optional | — | max length 60 | — | e.g. | `setJourneyProfile` body |
| Credential type `credentialType` | text field | optional | — | max length 100 | — | e.g. | `setJourneyProfile` body |
| Status `status` | segmented control | required | Active | Active · Inactive | — | — | `setJourneyProfile` body |
| Steps `steps` | repeatable rows | optional | — | — | — | Ordered journey steps, each an accessPointId with a direction (entry or exit) and an optional local time HH:MM, as GuestJourneySimulationInput.steps | `setJourneyProfile` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Active Journey Profiles** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Group Arrivals Today** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Guests via Group Admission** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Family Journeys** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Re-entry Guests** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Crossovers Today** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Fast Pass Validations** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Special Event Admissions** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**VIP Admissions** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Journey Exceptions** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Every guest journey** (data table, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**The selected guest journey** (detail panel): The pack groups this record's detail under its own headings: “Journey Type Venue Credential Status”.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save journey profile (primary button) | `setJourneyProfile` PUT `/journey-profiles` | AccessJourneyProfile | AccessJourneyProfile | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: The ten pack tiles per VO-R02 (Active journey profiles, Group arrivals today, Guests via group admission, Family journeys, Re-entry guests, Crossovers today, Fast Pass validations, Special event admissions, VIP admissions, Journey exceptions), today in venue time; Journey exceptions red when above zero. Guests via group admission counts people admitted, not group scans. *(source: screens/P08-venue-back-office.yaml#BO-214 / contracts/spine/access.yaml#listGuestJourney)*
- **Journey portfolio**: Columns Journey, Type, Venue ("All parks" when the profile has no venue), Credential, Status; type and credential drawn as chips from closed lists. Inactive journeys shown greyed at the end, never deleted. *(source: screens/P08-venue-back-office.yaml#BO-214 / contracts/spine/access.yaml#setJourneyProfile)*
- **Live journey health**: A list of the six health signals, each naming the group, gate or journey and how long ("Abu Dhabi International School group: 72 of 120 entered, 40 min after arrival slot") with Open. *(source: screens/P08-venue-back-office.yaml#BO-214)*
- **AI journey assistant**: A suggestion with its reason and an action a person takes ("School groups 09:00-10:00 average an 11-minute queue at Group Gate 2; open another group-validation lane" > Open BO-230). *(source: screens/P08-venue-back-office.yaml#BO-214)*
- **Entry statistics by category**: Admissions today split into general admission, group, re-entry and crossover, with schools and other groups broken down. *(source: DI-647)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New journey / Edit journey**: Opens a journey editor drawer (name, type, venue or all parks, credential, ordered steps of access point, direction and optional time); Save is a whole-row upsert (VO-R04). There is no delete: Deactivate sets the status so past simulations still name it. *(source: contracts/spine/access.yaml#setJourneyProfile)*
- **Open a board screen**: Tiles and health items open BO-215 to BO-223 and return here. *(source: DI-653 / F118 step 1)*

**Data it reads**: `listGuestJourney` (onLoad, Guest Journey Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-215` Group & B2B Admission Profile Builder: *Works in Group & B2B Admission Profile Builder*; calls `listGuestJourney`
- → `BO-216` Group Leader & Fast B2B Validation: *Works in Group Leader & Fast B2B Validation*; calls `listGuestJourney`
- → `BO-217` Group Attendance & Partial Entry Manager: *Works in Group Attendance & Partial Entry Manager*; calls `listGuestJourney`
- → `BO-218` Family, Child, POD & Companion Journey: *Works in Family, Child, POD & Companion Journey*; calls `listGuestJourney`
- → `BO-219` Re-entry & Temporary Exit Journey: *Works in Re-entry & Temporary Exit Journey*; calls `listGuestJourney`
- → `BO-220` Multi-Park & Crossover Journey Orchestrator: *Works in Multi-Park & Crossover Journey Orchestrator*; calls `listGuestJourney`
- → `BO-221` Fast Pass & Attraction Access Journey: *Works in Fast Pass & Attraction Access Journey*; calls `listGuestJourney`
- → `BO-222` Special Event, Free View & Alternative Admission: *Works in Special Event, Free View & Alternative Admission*; calls `listGuestJourney`
- → `BO-223` Journey Simulation, Audit & Publication: *Works in Journey Simulation, Audit & Publication*; calls `listGuestJourney`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest journey yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest journey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Journey profile used by a simulation and then deactivated**: It stays listed as Inactive with its last simulation result. *(source: contracts/spine/access.yaml#setJourneyProfile)*

#### Consistency with other screens

- Match `BO-223`: Journey simulation walks the steps defined here; same journey names.
- Match `BO-254`: Re-entry and crossover counts match the monitoring board's entry, exit, re-entry and crossover analytics.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  activeProfiles: 9
  groupArrivalsToday: 14
  guestsViaGroup: 1186
  familyJourneys: 412
  reEntryGuests: 238
  crossoversToday: 517
  fastPassValidations: 2904
  specialEventAdmissions: 85
  vipAdmissions: 64
  journeyExceptions: 7
portfolio:
- journey: School Group Entry
  type: B2B group
  venue: Aqua Park
  credential: Group QR
  status: Active
- journey: Family Admission
  type: Family
  venue: All parks
  credential: Mixed
  status: Active
- journey: 2-Park Hopper
  type: Multi-park
  venue: All parks
  credential: QR / RFID
  status: Active
- journey: Silver Fast Pass
  type: Fast Pass
  venue: Summit Peaks
  credential: RFID
  status: Active
- journey: VIP Experience
  type: VIP
  venue: All parks
  credential: Face Pass / QR
  status: Active
```

#### Permissions

- `listGuestJourney` → `SCOPE_VIEW` (read) · staff
- `setJourneyProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-214` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-214`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 1: Opens Guest Journey Command Center → Central configuration and monitoring screen for all special and multi-person admission journeys.
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F118 branch at step 1 (expected): when Nothing has been set up on Guest Journey Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F118 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (220 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-214?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save journey profile.
- [ ] Every transition is wired: `BO-100`, `BO-215`, `BO-216`, `BO-217`, `BO-218`, `BO-219`, `BO-220`, `BO-221`, `BO-222`, `BO-223`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-215` Group & B2B Admission Profile Builder

**Configure how a group or B2B booking is admitted: whole group, partial, in waves, by leader quantity or by manifest.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure admission for) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/group-b2b-admission-profile-builder-bo-215` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of group admission profiles (setGroupAdmissionProfile has no list or get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Defines how a group is admitted, separately from individual tickets: which segments it serves (schools, tour operators, corporate groups, resellers, travel groups, camps, families, events), how the group presents (single group QR, group barcode, group RFID, leader credential, individual credentials, hybrid) and how it is admitted (entire group, partial group, multiple waves, individual scan, leader + quantity, manifest-based). The one thing to get right: the gate behaviour sentence it produces - "one group scan authorises N guests, adds N to attendance and opens the group gate".

**Known correction pending (do not draw the wrong version)**

- **Seven selectFields labelled with segment names (Schools, Tour Operators ... Families); Events missing; credential mode and admission method not drawn** Why: Sample values used as labels; the segments are one multi-select of eight and the two enums are the heart of the screen. *(source: contracts/spine/access.yaml#setGroupAdmissionProfile / screens/P08-venue-back-office.yaml#BO-215; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **profileId is marked required yet "absent creates one"** Why: Contradiction; a create must not need an id (VO-R03). *(source: contracts/spine/access.yaml#setGroupAdmissionProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gate behaviour (authorise N, increment attendance N, open group gate) and the link to group products have no fields** Why: The pack's gate behaviour block and the matrix's "one scan unlocks N" need them. *(source: screens/P08-venue-back-office.yaml#BO-215 / screens/P08-venue-back-office.yaml#BO-216; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Save button has no operation** Why: Bind it to setGroupAdmissionProfile. *(source: screens/P08-venue-back-office.yaml#BO-215; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Write-only; no read of existing group profiles (CHG-WIR-004)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a group profile attached to a product (like an admission profile) or chosen per booking?** → Drawn default accepted: Per product, shown as "Group products using it". *(decided by Chinmay, 2026-10-02; DEC-251 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Schools | select field | — | — | — | — | — | — |
| Tour Operators | select field | — | — | — | — | — | — |
| Corporate Groups | select field | — | — | — | — | — | — |
| Resellers | select field | — | — | — | — | — | — |
| Travel Groups | select field | — | — | — | — | — | — |
| Camps | select field | — | — | — | — | — | — |
| Families | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name**: Required, max 200, Arabic variant; e.g. "School Group Admission". *(source: contracts/spine/access.yaml#setGroupAdmissionProfile)*
- **groupSegments**: One multi-select of the eight segments as chips (Events included); at least one. *(source: screens/P08-venue-back-office.yaml#BO-215 / contracts/spine/access.yaml#setGroupAdmissionProfile)*
- **credentialMode**: Six cards, single choice, each saying what the steward scans (one group QR for all, a leader credential, each guest's own credential, or a hybrid of leader plus individual). *(source: screens/P08-venue-back-office.yaml#BO-215 / contracts/spine/access.yaml#setGroupAdmissionProfile / DI-137)*
- **admissionMethod**: Six cards, single choice. Partial group and Multiple waves reveal the wave policy (BO-217); Leader + quantity reveals the fast validation options (BO-216); Manifest-based asks for the manifest to be on the booking. *(source: screens/P08-venue-back-office.yaml#BO-215 / contracts/spine/access.yaml#setGroupAdmissionProfile)*
- **venueId / profileId**: Not inputs; venue from the top bar, the profile id from the server on create (VO-R03). *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Gate behaviour preview**: "One scan of the group QR authorises up to 50 guests, adds the number admitted to attendance and opens the group gate" built from the choices; the quantity comes from the booking, shown as "N = guests on the booking". *(source: screens/P08-venue-back-office.yaml#BO-215 / screens/P08-venue-back-office.yaml#BO-216)*
- **Profile list**: Name, segments, credential mode, admission method, group products using it. *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save group profile**: Whole-row upsert (VO-R04); confirmation names the group products that use it and that gates apply it at the next package refresh. *(source: contracts/spine/access.yaml#setGroupAdmissionProfile)*

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `setGroupAdmissionProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group b2b admission configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group b2b admission untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group b2b admission configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Individual credentials with Entire group admission**: Warn that every guest still scans; suggest Leader + quantity for speed (a hint, not a block). *(source: screens/P08-venue-back-office.yaml#BO-216 / designer default)*

#### Consistency with other screens

- Match `BO-162`: Group Admission & Quantity Validation (board 2) holds group modes and max group size on another read; both describe the same group rule and should be one editor (VO-R14).
- Match `SCN-007`: The scanner's group admission screen behaves as the chosen admission method says.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- name: School Group Admission
  segments: Schools, Camps
  credential: Single group QR
  method: Leader + quantity
  products: School Day Pass (group), Summer Camp Day
- name: Tour Operator Arrivals
  segments: Tour operators, Travel groups, Resellers
  credential: Hybrid
  method: Multiple waves
```

#### Permissions

- `setGroupAdmissionProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group/B2B admission profile view shows entry statistics by category (general admission, group, re-entry, crossover) and attendance breakdowns for schools and other groups from scanned tickets. *(client request · MoM 2 Sep 2026, 4.15 Guest Journey, Group/B2B Profiles & Live Operations Dashboard · DI-647)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-215` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-215`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 2: Works in Group & B2B Admission Profile Builder → Group & B2B Admission Profile Builder

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-215?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-216` Group Leader & Fast B2B Validation

**Solve the specific matrix requirement for faster entrance flow when large B2B groups have multiple tickets stored on one device.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/group-leader-fast-b2b-validation-bo-216` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Today's B2B group bookings and whether each is ready for fast entry: payment, booking, visit date, group product, access rules and manifest checks, booked guests, attendance so far and remaining. At the gate the steward scans the leader's QR, sees "GROUP - 120 GUESTS" and admits all or enters the actual number. The one thing to get right: a booking shows READY FOR FAST ENTRY only when every pre-arrival check passes, and the failed check is named.

**Known correction pending (do not draw the wrong version)**

- **Check columns drawn as raw booleans (payment, booking, groupProduct, accessRules, manifest); visit date check missing** Why: The pack's pre-arrival status is six ticks and a readiness verdict; visitDateValid is in the read. *(source: screens/P08-venue-back-office.yaml#BO-217 / contracts/spine/access.yaml#listGroupLeaderFast; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Leader configuration (who is the authorised leader, which credential is the leader's) has no write** Why: The pack's "Configure Leader / Authorised / Credential" block cannot be stored. *(source: screens/P08-venue-back-office.yaml#BO-216; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Labels "Every group leader fast" and "The selected group leader fast"** Why: Generated placeholders; "Group arrivals" (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Visit date (default today), group segment, ready / not ready, search by group or leader name. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Every group leader fast** (data table, from `listGroupLeaderFast`)

| Shows | Format | Notes |
|---|---|---|
| Payment | yes / no (icon or chip) | Payment check passed |
| Booking | yes / no (icon or chip) | Booking check passed |
| Group product | yes / no (icon or chip) | Group product check passed |
| Access rules | yes / no (icon or chip) | Access rules check passed |
| Manifest | yes / no (icon or chip) | Manifest check passed |

**The selected group leader fast** (detail panel): The pack groups this record's detail under its own headings: “Booked”, “SCAN LEADER QR”, “Admit All 120”, “Enter Actual Attendance”, “CONFIRM”, “Attendance”.

| Shows | Format | Notes |
|---|---|---|
| Payment | yes / no (icon or chip) | Payment check passed |
| Booking | yes / no (icon or chip) | Booking check passed |
| Group product | yes / no (icon or chip) | Group product check passed |
| Access rules | yes / no (icon or chip) | Access rules check passed |
| Manifest | yes / no (icon or chip) | Manifest check passed |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Group arrivals list**: Group name, leader, booked guests, attendance, remaining, six check chips (Payment, Booking, Visit date, Group product, Access rules, Manifest) and a Ready for fast entry badge (green) or the first failing check (red). Not ready first. *(source: screens/P08-venue-back-office.yaml#BO-217 / contracts/spine/access.yaml#listGroupLeaderFast)*
- **Group detail**: The fast validation journey as the steward will see it (Scan leader QR > Group: 120 guests > Admit all 120 or Enter actual attendance [112] > Confirm > Attendance +112, Remaining 8), the associated tickets when they are individual tickets on the leader's device, and the waves admitted so far. *(source: screens/P08-venue-back-office.yaml#BO-216 / screens/P08-venue-back-office.yaml#BO-217)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open group attendance**: Opens the group's waves on BO-217. *(source: designer default)*
- **Open booking**: Opens the B2B booking (cross-process) to fix a failed payment or manifest check. *(source: designer default)*

**Data it reads**: `listGroupLeaderFast` (onLoad, Group Leader & Fast B2B Validation)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listGroupLeaderFast`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group leader fast list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group leader fast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group leader fast yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group leader fast are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Leader arrives with a failed check (unpaid)**: Not ready; at the gate the group scan is denied Unpaid with the next action "Send leader to Guest Services". *(source: contracts/spine/access.yaml#/components/schemas/DenyReason)*
- **Bulk credential mode**: Where the leader's phone holds 120 individual tickets, the gate loads the booking and validates eligible tickets together; ineligible ones are listed by name. *(source: screens/P08-venue-back-office.yaml#BO-216 / screens/P08-venue-back-office.yaml#BO-217)*

#### Consistency with other screens

- Match `SCN-007`: The scanner's group admission screen shows the same "Admit all / Enter actual attendance" choice and remaining count.
- Match `EMP-015`: Group scan on the Staff App behaves the same.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
groups:
- group: Abu Dhabi International School
  leader: Fatima Al Hashimi
  booked: 120
  attendance: 112
  remaining: 8
  checks: all passed
  status: Ready for fast entry
- group: Gulf Star Tours (coach 2)
  leader: James Carter
  booked: 46
  attendance: 0
  remaining: 46
  checks: Manifest missing
  status: Not ready
```

#### Permissions

- `listGroupLeaderFast` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-216` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-216`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 4: Works in Group Leader & Fast B2B Validation → Solve the specific matrix requirement for faster entrance flow when large B2B groups have multiple tickets stored on one device.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-216?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-217` Group Attendance & Partial Entry Manager

**Manage actual attendance when fewer guests arrive than the quantity purchased. The matrix explicitly requires the scanner to show the exact group size and allow the operator to enter actual attendants so daily attendance is updated correctly.**

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
| Route | `/access-venue/group-attendance-partial-entry-manager-bo-217` |

**Known gaps.** **Group Attendance & Partial Entry Manager declares no operation that writes anything** — its only declared call is `listGroupAttendancePartial`, a read. The name promises authoring and the contract … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Actual group attendance when fewer guests arrive than were bought: each admission wave (group, leader, gate, operator, quantity, time, device) and the running purchased / entered / remaining figures, plus the partial-entry policy (allow partial admission, allow multiple waves, maximum waves, unused admission expiry). The one thing to get right: attendance counts the people actually admitted (43, then 48), and the remaining places (7, then 2) stay usable until they expire.

**Known correction pending (do not draw the wrong version)**

- **Content is an empty unbound table (pack "gives nothing that can be drawn")** Why: The pack gives a worked example and an audit list, and listGroupAttendancePartial returns them; bind it. *(source: screens/P08-venue-back-office.yaml#BO-218 / contracts/spine/access.yaml#listGroupAttendancePartial; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The wave policy (partial admission, multiple waves, maximum waves, unused expiry) has no write** Why: The screen name and pack promise configuration; nothing stores it. *(source: screens/P08-venue-back-office.yaml#BO-218 / screens/P08-venue-back-office.yaml#BO-217; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Wave policy**: Allow partial admission (yes/no), Allow multiple waves (yes/no), Maximum waves (Unlimited or N), Unused admission expiry (End of visit day by default). Drawn greyed: no write exists. *(source: screens/P08-venue-back-office.yaml#BO-218)*
- **Filters**: Visit date (default today), group, gate. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Group card**: "Purchased 50 - Entered 48 - Remaining 2" as a segmented bar, with the expiry of the remaining places ("Remaining 2 expire at park close 22:00"). *(source: screens/P08-venue-back-office.yaml#BO-217 / screens/P08-venue-back-office.yaml#BO-218 / contracts/spine/access.yaml#listGroupAttendancePartial)*
- **Wave timeline**: One row per wave - time, gate, quantity (+43, +5), operator, device, leader - oldest first, so the story reads top to bottom. *(source: screens/P08-venue-back-office.yaml#BO-218 / contracts/spine/access.yaml#listGroupAttendancePartial)*
- **Group attendance breakdown**: Today's groups by segment (schools, tour operators, corporate) with purchased vs entered totals. *(source: DI-647)*

**Data it reads**: `listGroupAttendancePartial` (onLoad, Group Attendance & Partial Entry Manager)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listGroupAttendancePartial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group attendance partial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group attendance partial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group attendance partial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group attendance partial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Steward enters more than remaining**: Refused at the scanner ("Only 2 places remain"); never shown here as a negative remaining. *(source: contracts/spine/access.yaml#validateGroupAccess)*
- **Maximum waves reached with places remaining**: The card says "Wave limit reached - 2 places cannot be used" in amber. *(source: screens/P08-venue-back-office.yaml#BO-218)*

#### Consistency with other screens

- Match `BO-216`: Same group names, attendance and remaining figures.
- Match `BO-257`: Attendance analytics count admitted guests from these waves, not purchased quantity.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
group:
  group: Al Noor Summer Camp
  purchased: 50
  entered: 48
  remaining: 2
  expires: Remaining 2 expire at park close 22:00
waves:
- time: 09:12
  gate: Main Plaza Gate 2
  quantity: 43
  operator: Rahul Menon
  device: HH-02
  leader: Omar Haddad
- time: '11:40'
  gate: North Entry
  quantity: 5
  operator: Maria Santos
  device: NE-01
  leader: Omar Haddad
```

#### Permissions

- `listGroupAttendancePartial` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group/B2B admission profile view shows entry statistics by category (general admission, group, re-entry, crossover) and attendance breakdowns for schools and other groups from scanned tickets. *(client request · MoM 2 Sep 2026, 4.15 Guest Journey, Group/B2B Profiles & Live Operations Dashboard · DI-647)*
- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-217` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-217`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 6: Works in Group Attendance & Partial Entry Manager → Manage actual attendance when fewer guests arrive than the quantity purchased. The matrix explicitly requires the scanner to show the exact group size and allow the operator to enter actual …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-217?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-218` Family, Child, POD & Companion Journey

**Configure linked-person access journeys. The matrix requires child protection through adult-ticket pairing or biometric validation of the assigned adult. It also requires POD accompanying persons and nannies to be bound to a primary guest and only enter when accompanied by that guest.**

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
| Route | `/access-venue/family-child-pod-companion-journey-bo-218` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Who must enter (and leave) with whom: child needs an adult, minor needs a guardian, POD companion and nanny only with their primary guest, group member with the leader. For each rule, how the companion is verified (paired adult credential or the assigned adult's Face Pass) and where (admission, exit, attraction). The one thing to get right: a dependent's credential can never bypass the relationship - the nanny scanned alone is denied with "Primary guest required", and child exit can require the assigned adult.

**Known correction pending (do not draw the wrong version)**

- **Read and write disagree - the read returns relationshipType and verificationMethod (pairedAdultCredential, assignedAdultBiometric); the write takes guestCategory, requiredCompanionCategory, companionVerification (linkedTicket, companionBiometric) and verifyAt** Why: The form cannot open with what the list shows (VO-R04); one shape is needed. *(source: contracts/spine/access.yaml#listFamilyChildPod / contracts/spine/access.yaml#setGuestCompanionEligibility; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The five relationship types drawn as select and text fields** Why: They are values of one relationship choice, not five inputs. *(source: screens/P08-venue-back-office.yaml#BO-218; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The write cannot express Group leader > group member (or Primary guest > nanny as a pair), while the read can** Why: requiredCompanionCategory has adult, podCompanion, nanny, guardian only; the pack lists both relationships. *(source: screens/P08-venue-back-office.yaml#BO-219 / contracts/spine/access.yaml#setGuestCompanionEligibility; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where is a specific nanny or child linked to a specific primary guest (the pack's "John Smith - Child 1, Child 2, POD companion, Nanny")?** → Drawn default accepted: At sale or at Guest Services on the ticket; this screen shows the rule only and links to the ticket investigation console (BO-226) for a guest's links. *(decided by Chinmay, 2026-10-02; DEC-252 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Parent → Child | select field | — | — | — | — | — | — |
| Guardian → Minor | select field | — | — | — | — | — | — |
| POD → Companion | select field | — | — | — | — | — | — |
| Primary Guest → Nanny | text field | — | — | — | — | — | — |
| Group Leader → Group Member | text field | — | — | — | — | — | — |

**Sent by *Save companion rule*** (`setGuestCompanionEligibility`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rule `ruleId` | picker: choose a rule | optional | — | — | shows names, sends the id | Absent creates a rule | `setGuestCompanionEligibility` body |
| Venue `venueId` | text field | required | — | — | — | — | `setGuestCompanionEligibility` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setGuestCompanionEligibility` body |
| Guest category `guestCategory` | select | required | — | Adult · Child · Junior · Senior · Pod · Pod companion · Nanny · Vip · Member · Staff · Accreditation · Customer segment | — | — | `setGuestCompanionEligibility` body |
| Required companion category `requiredCompanionCategory` | radio group | required | — | Adult · Pod companion · Nanny · Guardian | — | Category of the companion who must be present | `setGuestCompanionEligibility` body |
| Companion verification `companionVerification` | segmented control | optional | Linked ticket | Linked ticket · Companion biometric | — | — | `setGuestCompanionEligibility` body |
| Verify at `verifyAt` | multi-select chips | required | — | Admission · Exit · Attraction; at least 1 | — | Where the companion is checked | `setGuestCompanionEligibility` body |
| Attractions `attractionIds` | list of values (chips) | optional | — | — | — | Where verifyAt includes attraction | `setGuestCompanionEligibility` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name**: Required, max 200 (e.g. "Child under 12 needs an adult"). *(source: contracts/spine/access.yaml#setGuestCompanionEligibility)*
- **guestCategory / requiredCompanionCategory**: Built as a sentence: "A [Child] must be accompanied by a [Adult]" from the closed lists; the five pack relationships (Parent > child, Guardian > minor, POD > companion, Primary guest > nanny, Group leader > group member) are offered as starting templates. *(source: screens/P08-venue-back-office.yaml#BO-219 / contracts/spine/access.yaml#setGuestCompanionEligibility)*
- **companionVerification**: Linked ticket (paired adult credential, default) or Companion biometric (the assigned adult's Face Pass), with the consent note for biometrics. *(source: contracts/spine/access.yaml#setGuestCompanionEligibility / ADR-0063)*
- **verifyAt / attractionIds**: Checkboxes Admission, Exit, Attraction (at least one); Exit carries the hint "child protection - the assigned adult must be present to leave"; Attraction reveals an attraction picker (required then). *(source: screens/P08-venue-back-office.yaml#BO-219 / contracts/spine/access.yaml#setGuestCompanionEligibility)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save companion rule (primary button) | `setGuestCompanionEligibility` PUT `/guest-companion-eligibility` | GuestCompanionEligibilityRulesInput | GuestCompanionEligibilityRulesView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rule list**: Rule name, dependent, required companion, verification, checked at; grouped by relationship. *(source: contracts/spine/access.yaml#listFamilyChildPod)*
- **Gate outcome preview**: "Nanny scanned alone: Denied - Primary guest required (amber)"; "Primary guest present: Admitted". Uses the accompaniment deny reason label. *(source: screens/P08-venue-back-office.yaml#BO-219 / contracts/spine/access.yaml#/components/schemas/DenyReason)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save companion rule**: Upsert by ruleId (no id creates); unknown id is 404. At the gate a failed rule denies with the rule's reason, never silently. *(source: contracts/spine/access.yaml#setGuestCompanionEligibility)*

**Data it reads**: `listFamilyChildPod` (onLoad, Family, Child, POD & Companion Journey)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listFamilyChildPod`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The family child pod configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the family child pod untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No family child pod configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Assigned adult has no Face Pass when biometric verification is chosen**: The gate falls back to the linked ticket check and the steward sees why. *(source: DI-641 / designer default)*
- **Child exits through a gate with no camera**: Exit check by linked ticket; the rule screen warns which exit gates cannot do biometric checks. *(source: screens/P08-venue-back-office.yaml#BO-203 / designer default)*

#### Consistency with other screens

- Match `BO-161`: Companion rules on the access rule board (BO-161) are the same rules; one editor (VO-R14).
- Match `BO-249`: Relationship and companion fraud monitoring reads violations of these rules.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- name: Child under 12 needs an adult
  dependent: Child
  companion: Adult
  verification: Linked ticket
  at: Admission, Exit
- name: Nanny only with primary guest
  dependent: Nanny
  companion: Guardian
  verification: Linked ticket
  at: Admission
- name: POD companion with POD guest
  dependent: POD companion
  companion: Adult
  verification: Linked ticket
  at: Admission, Attraction (Wave Rider)
relationship:
  primary: Khalid Al Zaabi
  linked: Child 1 Hamad, Child 2 Mariam, Nanny Maria Santos
```

#### Permissions

- `listFamilyChildPod` → `SCOPE_VIEW` (read) · staff
- `setGuestCompanionEligibility` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-218` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-218`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 8: Works in Family, Child, POD & Companion Journey → Configure linked-person access journeys. The matrix requires child protection through adult-ticket pairing or biometric validation of the assigned adult. It also requires POD accompanying persons and …

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-218?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save companion rule.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-219` Re-entry & Temporary Exit Journey

**Manage guests temporarily leaving and returning to the venue. The source matrix requires configurable re-entry and also describes a journey using a designated re-entry gate with both ticket verification and a UV stamp.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/re-entry-temporary-exit-journey-bo-219` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): listEntryTemporaryExit returns a separate re-entry rule (ruleId, maximum, name) beside the admission profile; re-entry is a block of the profile, read by …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The re-entry block of an admission profile seen as a journey: a guest scans out and is "Temporarily outside", then comes back through the designated re-entry gate with an extra check (UV stamp, face or operator). Re-entry allowed, maximum, same day, exit required first, designated gate, verification. The one thing to get right: temporary exit and re-entry are counted as their own journey events, never as new admissions, and the seven re-entry checks are shown in the order the gate runs them.

**Known correction pending (do not draw the wrong version)**

- **The verification options drawn as four separate fields (three selects and a text field) and no Save button** Why: They are one single choice; updateAdmissionRules is bound but nothing triggers it. *(source: screens/P08-venue-back-office.yaml#BO-219 / contracts/spine/access.yaml#updateAdmissionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): listEntryTemporaryExit returns a separate "re-entry rule" (ruleId, maximum, name) beside the admission profile (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Credential only | select field | — | — | — | — | — | — |
| Credential + UV stamp | text field | — | — | — | — | — | — |
| Credential + Face | select field | — | — | — | — | — | — |
| Credential + operator | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Admission profile**: Opens on the profile passed in (profileId); a profile picker at the top switches between profiles that allow re-entry. *(source: contracts/spine/access.yaml#listAdmissionRules / screens/P08-venue-back-office.yaml#BO-219)*
- **maxReentries / sameDayOnly / requiresExitBeforeReentry / designatedAccessPointIds**: As the pack's re-entry profile: Re-entry allowed (yes/no), Maximum [1], Same day (yes), Exit required first (yes), Designated gate (access point picker, e.g. Re-entry Gate 03; empty = any allowed point). Same fields and labels as the admission profile editor. *(source: screens/P08-venue-back-office.yaml#BO-219 / contracts/spine/access.yaml#updateAdmissionRules)*
- **reEntryVerification**: One single choice - Credential only (default), Credential + UV stamp, Credential + face, Credential + operator, Custom. *(source: screens/P08-venue-back-office.yaml#BO-219 / contracts/spine/access.yaml#updateAdmissionRules)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Journey strip**: Entry > Exit scan > TEMPORARILY OUTSIDE > Re-entry gate > checks > ALLOW RE-ENTRY, with the guest-facing words at each step. *(source: screens/P08-venue-back-office.yaml#BO-219)*
- **Re-entry checks**: Previous entry, Valid exit, Re-entry entitlement, Re-entry quantity, Correct gate, Anti-passback, Additional verification; each failure maps to its deny reason label. *(source: screens/P08-venue-back-office.yaml#BO-219)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save re-entry rules**: Saves the whole admission profile (updateAdmissionRules replaces it whole, VO-R04) - so the screen loads the full profile and resends every block; confirmation names the products using the profile. *(source: contracts/spine/access.yaml#updateAdmissionRules)*

**Data it reads**: `listAdmissionRules` (onLoad, The admission profiles that allow a temporary exit)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listAdmissionRules`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The re-entry temporary exit configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the re-entry temporary exit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No re-entry temporary exit configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Edge cases to draw

- **Guest re-enters at the wrong gate**: Denied "Wrong gate - use Re-entry Gate 03". *(source: contracts/spine/access.yaml#/components/schemas/DenyReason)*
- **Exit required first but the guest left through a free-rotation exit**: Denied "Exit scan required before re-entry"; next action "Supervisor may override after checking scan history". *(source: DI-626)*

#### Consistency with other screens

- Match `BO-032`: This is the Exit and re-entry section of the admission profile editor (VO-R14); same labels and one Save.
- Match `BO-156`: Entry, exit and re-entry rules on board 2 edit the same block.
- Match `BO-258`: Re-entries are reported separately from entries there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  name: Standard day ticket
  reEntry: true
  maximum: 1
  sameDay: true
  exitFirst: true
  gate: Re-entry Gate 03
  verification: Credential + UV stamp
```

#### Permissions

- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-219` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-219`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 10: Works in Re-entry & Temporary Exit Journey → Manage guests temporarily leaving and returning to the venue. The source matrix requires configurable re-entry and also describes a journey using a designated re-entry gate with both ticket …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-219?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-220` Multi-Park & Crossover Journey Orchestrator

**Operationalize the multi-park rules configured in Board 2. The matrix specifically distinguishes crossover from normal entry and re-entry and requires crossover to be tracked separately.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/multi-park-crossover-journey-orchestrator-bo-220` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Runs multi-park journeys configured on board 2: a guest enters Park A, leaves or transfers, and crosses over into Park B, tracked separately from normal entry, re-entry and exit. Shows the crossover rules (2-Park Hopper - first park any, second park Aqua Park, after first admission, earliest 14:00, maximum 1), the live crossover events, and a guest's journey status ("Summit Peaks - INSIDE; Aqua Park - CROSSOVER AVAILABLE"). The one thing to get right: the four movement types are never mixed in counts or colours.

**Known correction pending (do not draw the wrong version)**

- **Movement type enum is normalEntry, reEntry, crossover - exit is missing** Why: The pack keeps four movements separate, including Exit. *(source: screens/P08-venue-back-office.yaml#BO-221 / contracts/spine/access.yaml#listMultiParkCrossover2; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Content is an empty unbound table; button "Save admission rules"** Why: Bind the movement log (listMultiParkCrossover2); the save is "Save crossover rules" (generated label, VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-220; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Two reads of crossover rules (listMultiParkCrossover rule rows and the admission profile's crossover block)** Why: The rule rows carry their own ruleId; crossover is a block of the profile (29 September), so there should be one source. *(source: contracts/spine/access.yaml#listMultiParkCrossover / contracts/spine/access.yaml#updateAdmissionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation looks up one guest's journey status** Why: The pack's Journey Status block needs it. *(source: screens/P08-venue-back-office.yaml#BO-220; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Sent by *Save admission rules*** (`updateAdmissionRules`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `updateAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `updateAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `updateAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `updateAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `updateAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `updateAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `updateAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `updateAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `updateAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `updateAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `updateAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `updateAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `updateAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `updateAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `updateAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `updateAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `updateAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `updateAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `updateAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `updateAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `updateAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `updateAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `updateAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `updateAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `updateAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `updateAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `updateAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `updateAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `updateAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `updateAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `updateAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `updateAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `updateAdmissionRules` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Crossover rules (allowedParks, parkOrder, sameDayCrossover, differentDayAccess, dayPattern, numberOfParkEntries …**: Edited as the Crossover section of the admission profile (same fields and labels as BO-032): at least two parks; earliest crossover HH:MM in venue time; prerequisite park must be one of the allowed parks. *(source: screens/P08-venue-back-office.yaml#BO-220 / contracts/spine/access.yaml#updateAdmissionRules / contracts/spine/access.yaml#listMultiParkCrossover)*
- **Guest journey lookup**: Ticket number or media code to show one guest's current park and eligible next park. *(source: screens/P08-venue-back-office.yaml#BO-220)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save admission rules (primary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Visual journey**: Park A (first entry) > guest leaves/transfers > CROSSOVER > Park B, with the rule's conditions written on the arrow. *(source: screens/P08-venue-back-office.yaml#BO-220)*
- **Movement log**: Events with type chips Normal entry / Re-entry / Crossover / Exit in four distinct colours, from park, to park, ticket, time; cursor paging (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-220 / screens/P08-venue-back-office.yaml#BO-221 / contracts/spine/access.yaml#listMultiParkCrossover2)*
- **Journey status**: For a looked-up ticket - current park and INSIDE / OUTSIDE, eligible next park with CROSSOVER AVAILABLE or the reason it is not (before 14:00, maximum used). *(source: screens/P08-venue-back-office.yaml#BO-220)*
- **AI detection**: Flags such as "attempting crossover to Aqua Park without the first entry at Summit Peaks", advisory, linking to the scan. *(source: screens/P08-venue-back-office.yaml#BO-221)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save crossover rules**: Saves the whole admission profile (VO-R04), applied at the next package refresh. *(source: contracts/spine/access.yaml#updateAdmissionRules)*

**Data it reads**: `listMultiParkCrossover2` (onLoad, Multi-Park & Crossover Journey Orchestrator); `listMultiParkCrossover` (onLoad, Multi-Park & Crossover Rules); `listAdmissionRules` (onLoad, The admission profiles that carry crossover rules)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listMultiParkCrossover2`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-park crossover journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-park crossover journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-park crossover journey yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-park crossover journey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Edge cases to draw

- **Crossover attempted before the earliest time**: Denied with "Crossover from 14:00" (not-yet-valid wording with the time). *(source: screens/P08-venue-back-office.yaml#BO-220)*

#### Consistency with other screens

- Match `BO-160`: Multi-Park & Crossover Rules (board 2) and this screen edit the same crossover block; the rule editor lives there or in BO-032, this screen shows its operation (VO-R14).
- Match `BO-258`: Crossover analytics use the same four movement types.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: 2-Park Hopper
  firstPark: Any
  secondPark: Aqua Park
  crossover: After first park admission
  earliest: '14:00'
  maximum: 1
  days: Same day
events:
- time: '14:06'
  ticket: VT0733
  type: Crossover
  from: Summit Peaks
  to: Aqua Park
- time: '14:11'
  ticket: VT0734
  type: Re-entry
  from: '-'
  to: Summit Peaks
status:
  ticket: VT0733
  current: Aqua Park - INSIDE
  next: Summit Peaks - re-entry after crossover not allowed
```

#### Permissions

- `listMultiParkCrossover2` → `SCOPE_VIEW` (read) · staff
- `listMultiParkCrossover` → `SCOPE_VIEW` (read) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-220` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-220`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 12: Works in Multi-Park & Crossover Journey Orchestrator → Operationalize the multi-park rules configured in Board 2. The matrix specifically distinguishes crossover from normal entry and re-entry and requires crossover to be tracked separately.

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-220?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save admission rules.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-221` Fast Pass & Attraction Access Journey

**Configure the operational experience for limited and unlimited priority-access entitlements. The matrix requires Silver Fast Pass to support three accesses and Gold to support unlimited access with an optional one-access-per-ride restriction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `QUEUE_MANAGE`, `QUEUE_VIEW`, `SCOPE_VIEW` (2 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select eligible) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `queueId` (navigation) |
| Route | `/access-venue/fast-pass-attraction-access-journey-bo-221` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Fast Pass profiles and how they behave at the ride: Silver (3 uses, 1 per validation, "2 FAST PASSES REMAINING" at the scanner) and Gold (unlimited, maximum 1 per ride), which attraction categories accept them, and what the ride operator sees (profile, ride, previous use, eligible). The one thing to get right: the Fast Pass lane is distinct from the virtual queue and walk-in lines, and the remaining count the guest and operator see is the one the entitlement engine consumes.

**Known correction pending (do not draw the wrong version)**

- **Two saves - "Save Fast Pass settings" (updateQueue, a ride lane's Fast Pass block, QUEUE_MANAGE, entry param queueId) and "Save fast pass profile"** Why: Eligibility is mapped twice (by attraction category on the profile and by entitlement products on each lane); pick one mapping and keep the lane edit on the queue screen. *(source: contracts/satellite/queue.yaml#updateQueue / contracts/spine/access.yaml#setFastPassProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Roller Coaster, Drop Tower, Water Ride drawn as three selectFields; Adventure Ride missing** Why: Sample values used as labels; one multi-select of four categories. *(source: screens/P08-venue-back-office.yaml#BO-221; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **eligibleAttractionCategories is a free string list** Why: The pack names four categories; a closed set (or the attraction type list of the topology) is needed. *(source: contracts/spine/access.yaml#setFastPassProfile; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Roller Coaster | select field | — | — | — | — | — | — |
| Drop Tower | select field | — | — | — | — | — | — |
| Water Ride | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Open only | toggle | off | — | `listQueues` ?openOnly |

**Form: Save fast pass profile** (modal, opened by *Save fast pass profile*; *Save fast pass profile* calls `setFastPassProfile`, *Cancel* sends nothing)

**Collects what `setFastPassProfile` sends before it is called.** Required: `id`, `scopePath`, `name`, `unlimited`. Optional: `venueId`, `totalUses`, `consumptionPerValidation`, `onePerRide`, `eligibleAttractionCategories`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | The profileId the list shows | `setFastPassProfile` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setFastPassProfile` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setFastPassProfile` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setFastPassProfile` body |
| Unlimited `unlimited` | toggle | required | off | — | — | — | `setFastPassProfile` body |
| Total uses `totalUses` | number field | optional | — | min 1 | — | Null when unlimited | `setFastPassProfile` body |
| Consumption per validation `consumptionPerValidation` | number field | optional | 1 | min 1 | — | — | `setFastPassProfile` body |
| One per ride `onePerRide` | toggle | optional | off | — | — | — | `setFastPassProfile` body |
| Eligible attraction categories `eligibleAttractionCategories` | list of values (chips) | optional | — | — | — | The list's eligibleType, e.g. | `setFastPassProfile` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `totalUses` missing on a limited profile.

**Sent by *Save Fast Pass settings*** (`updateQueue`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The same locale-to-text map `createQueue` takes and `Queue` returns, so an edit form round-trips the name. | `updateQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | optional | — | min 0 | — | — | `updateQueue` body |
| Max party size `maxPartySize` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | — | min 1 | — | — | `updateQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `updateQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | — | min 0; max 100 | — | — | `updateQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Replaces the whole block; null removes it. | `updateQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `updateQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `updateQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `updateQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `updateQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `updateQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `updateQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `updateQueue` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name**: Required, max 200, Arabic variant (e.g. Silver, Gold). *(source: contracts/spine/access.yaml#setFastPassProfile)*
- **unlimited / totalUses**: A choice Limited [N] uses / Unlimited; N required and at least 1 when limited, hidden when unlimited. *(source: screens/P08-venue-back-office.yaml#BO-221 / contracts/spine/access.yaml#setFastPassProfile)*
- **consumptionPerValidation / onePerRide**: "Uses consumed per ride" (default 1); "Maximum 1 per ride" toggle, offered for unlimited profiles as in Gold. *(source: screens/P08-venue-back-office.yaml#BO-221 / contracts/spine/access.yaml#setFastPassProfile)*
- **eligibleAttractionCategories**: One multi-select of Roller coaster, Drop tower, Water ride, Adventure ride, with the rides in each category listed underneath. *(source: screens/P08-venue-back-office.yaml#BO-221 / contracts/spine/access.yaml#setFastPassProfile)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save Fast Pass settings (primary button) | `updateQueue` PATCH `/queues/{queueId}` | inline | Queue | — | — |
| Save fast pass profile (secondary button) | `setFastPassProfile` PUT `/fast-pass-profiles` | AccessFastPassProfile | AccessFastPassProfile | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Profile cards**: Silver / Gold cards with uses, consumption, restriction and eligible categories. *(source: screens/P08-venue-back-office.yaml#BO-221 / contracts/spine/access.yaml#listFastPassAttraction)*
- **Operator display preview**: "GOLD - Ride: Falcon Coaster - Previous use 10:32 - Eligible: YES", and the guest-facing "2 FAST PASSES REMAINING". *(source: screens/P08-venue-back-office.yaml#BO-221 / screens/P08-venue-back-office.yaml#BO-222)*
- **Validation sequence**: Credential > Fast Pass entitlement > Attraction eligibility > Usage restriction > Consume / record > FAST PASS ACCESS GRANTED. *(source: screens/P08-venue-back-office.yaml#BO-221 / screens/P08-venue-back-office.yaml#BO-222)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save Fast Pass profile**: Upsert by id (no id creates); whole row (VO-R04). Confirmation names the products that sell this profile. *(source: contracts/spine/access.yaml#setFastPassProfile)*

**Data it reads**: `listFastPassAttraction` (onLoad, Fast Pass & Attraction Access Journey); `listQueues` (onLoad, The attraction lanes a Fast Pass is configured on)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listFastPassAttraction`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fast pass attraction configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fast pass attraction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fast pass attraction configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 `totalUses` missing on a limited profile. |

#### Edge cases to draw

- **Silver used up**: Denied with "No Fast Passes left (3 of 3 used)"; next action "Join the standby or virtual queue". *(source: DI-628)*
- **Gold guest rides the same ride twice**: Denied "Already used on this ride at 10:32". *(source: screens/P08-venue-back-office.yaml#BO-222)*
- **Virtual-queue guest at the Fast Pass lane**: Not admitted to the Fast Pass lane; virtual queue guests have their own handling and are never merged into the paid lane. *(source: DI-678)*

#### Consistency with other screens

- Match `BO-159`: The entitlement consumption engine counts the uses; same units.
- Match `BO-001`: The ride's queue configuration (cross-process, virtual queue) holds the Fast Pass lane; the lane must accept exactly the profiles mapped here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- name: Silver
  uses: 3
  perValidation: 1
  onePerRide: false
  categories: Roller coaster, Water ride
  rides: Falcon Coaster, Wave Rider
- name: Gold
  uses: Unlimited
  onePerRide: true
  categories: Roller coaster, Drop tower, Water ride, Adventure ride
operator:
  profile: GOLD
  ride: Falcon Coaster
  previousUse: '10:32'
  eligible: 'YES'
```

#### Permissions

- `listFastPassAttraction` → `SCOPE_VIEW` (read) · staff
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `updateQueue` → `QUEUE_MANAGE` (configure) · staff
- `setFastPassProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: walk-in, virtual-queue and VIP guests must be distinguished at the ride; VQ guests are never merged into the VIP line (would erode paid value); VQ arrivals need their own handling, e.g. a separate line or a QR scan within the arrival window. *(agreed · MoM 7 Sep 2026, 4.15 Virtual Queue - Three-Tier Guest Model · DI-678)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-221` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-221`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 14: Works in Fast Pass & Attraction Access Journey → Configure the operational experience for limited and unlimited priority-access entitlements. The matrix requires Silver Fast Pass to support three accesses and Gold to support unlimited access with …

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-221?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save Fast Pass settings, Save fast pass profile.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `QUEUE_MANAGE`, `QUEUE_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-222` Special Event, Free View & Alternative Admission

**Configure temporary/special admission processes that differ from normal venue access. The matrix requires special-event products capable of capturing attendance without physical admission, N- person attendance entered through a turnstile/tablet/handheld, and Free View days where main gates are open while attraction gates continue validating tickets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20680 (APP-SETUP-BO-222) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/special-event-free-view-alternative-admission-bo-222` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): setContextTimeEvent is the context policy builder's write (BO-237, which declares it); a context policy is a different object from a special-event admission …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Configures special admission journeys that temporarily replace normal access: Free View days (main gates open in free spin and count passage while attractions keep validating), special, private, corporate and school events, and manual attendance (N people entered on a turnstile, tablet or handheld). The one thing to get right: each journey is drawn as a per-gate behaviour table (Main Entrance: validation off, free spin, count passage; Attractions: validation on) bounded by a date-time window.

**Known correction pending (do not draw the wrong version)**

- **Two selectFields labelled with sample values "15 Sep 2026" and "08:00-18:00"** Why: Sample values used as labels; they are the start/end window fields. *(source: screens/P08-venue-back-office.yaml#BO-222; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Body requires id and scopePath** Why: Server-owned (VO-R03). *(source: contracts/spine/access.yaml#setOperatingCalendarEntry; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): setContextTimeEvent (an occupancy/context policy builder, BO-237) is bound here (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 15 Sep 2026 | select field | — | — | — | — | — | — |
| 08:00–18:00 | select field | — | — | — | — | — | — |

**Form: Save operating calendar entry** (modal, opened by *Save operating calendar entry*; *Save operating calendar entry* calls `setOperatingCalendarEntry`, *Cancel* sends nothing)

**Collects what `setOperatingCalendarEntry` sends before it is called.** Required: `id`, `venueId`, `dayType`, `startsAt`, `endsAt`, `scopePath`. Optional: `name`, `ticketValidationRequired`, `admissionType`, `attractionValidation`, `manualAttendanceRequired`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setOperatingCalendarEntry` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setOperatingCalendarEntry` body |
| Day type `dayType` | select | required | — | Normal operating day · Weekend · Holiday · Seasonal schedule · Private event · Free entry day · Maintenance period · Special event · Ladies only session · School group session · After hours event | — | Kind of calendar entry | `setOperatingCalendarEntry` body |
| Name `name` | text field | optional | — | — | — | — | `setOperatingCalendarEntry` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setOperatingCalendarEntry` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setOperatingCalendarEntry` body |
| Ticket validation required `ticketValidationRequired` | toggle | optional | on | — | — | False on free-entry days | `setOperatingCalendarEntry` body |
| Admission type `admissionType` | segmented control | optional | — | Free view day · Special event | — | Set on special admission windows only | `setOperatingCalendarEntry` body |
| Attraction validation `attractionValidation` | toggle | optional | — | — | — | Special windows: attraction gates keep validating tickets | `setOperatingCalendarEntry` body |
| Manual attendance required `manualAttendanceRequired` | toggle | optional | — | — | — | Special windows: operator enters attendance count | `setOperatingCalendarEntry` body |
| Venue closed `venueClosed` | toggle | optional | off | — | — | A day the whole venue is closed (design-notes correction on BO-019, Block B: "No operation sets product blackout dates or a venue closure day"; CHG-CSP-051). | `setOperatingCalendarEntry` body |
| Priority `priority` | number field | optional | 0 | min 0; max 1000 | — | Which entry wins where two overlap: the higher priority (decided 2 October 2026, Chinmay, batch 6 set 10a, BO-152: "The venue sets a priority per entry"; DEC-229; CHG-CSP-027). | `setOperatingCalendarEntry` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setOperatingCalendarEntry` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `endsAt` is not after `startsAt`, or the entry overlaps another with the same `priority` (`overlapping-entry-same-priority`; CHG-CSP-027).

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Journey type / dayType**: Special event, Free View day, Private event, Corporate event, School event, Manual attendance - as cards; the contract's dayType enum also covers ladies-only, school group and after-hours sessions. *(source: screens/P08-venue-back-office.yaml#BO-222 / contracts/spine/access.yaml#setOperatingCalendarEntry)*
- **startsAt / endsAt**: Date-time range in venue time on a calendar (Day/Week/Month per VO-R01); end after start. *(source: contracts/spine/access.yaml#setOperatingCalendarEntry)*
- **ticketValidationRequired, attractionValidation, manualAttendanceRequired**: A small matrix "Main entrance: validate tickets yes/no" and "Attractions: keep validating yes/no", plus "Staff enter attendance count" - matching the pack's Free View example; free-entry days default main gate validation off. *(source: screens/P08-venue-back-office.yaml#BO-222 / contracts/spine/access.yaml#/components/schemas/AccessOperatingCalendarEntry)*
- **Special-event admission profile**: Where the event needs its own profile (capture attendance without physical admission), create it from here into the admission profile editor (BO-032), not with a second form. *(source: contracts/spine/access.yaml#createAdmissionRules / MATRIX 3.2.71)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save operating calendar entry (primary button) | `setOperatingCalendarEntry` PUT `/operating-calendar-entries` | AccessOperatingCalendarEntry | AccessOperatingCalendarEntry | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Upcoming special days**: Calendar with coloured entries by type and a list of the next 10 with gates affected and expected attendance. *(source: contracts/spine/access.yaml#listSpecialEventFree)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save special day**: Whole-entry upsert (VO-R04); gates change behaviour at the window start, which the confirmation states. *(source: contracts/spine/access.yaml#setOperatingCalendarEntry)*

**Data it reads**: `listSpecialEventFree` (onLoad, Special Event, Free View & Alternative Admission)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listSpecialEventFree`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The special event free configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the special event free untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No special event free configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 `endsAt` is not after `startsAt`, or the entry overlaps another with the same `priority` (`overlapping-entry-same-priority`; CHG-CSP-027). |

#### Edge cases to draw

- **Overlapping entries on the same gates**: Warn with both entries named (the pack's AI conflict warning) before saving. *(source: screens/P08-venue-back-office.yaml#BO-151)*

#### Consistency with other screens

- Match `BO-152`: The same write (operating calendar entry) serves the Operating Calendar; draw both as one calendar with a "Special admission" filter (VO-R14).
- Match `BO-201`: Free spin wording matches gate modes.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entries:
- type: Free View day
  window: Fri 13 Nov 2026 08:00-18:00
  mainEntrance: Validation off, free spin, count passage
  attractions: Validation on
- type: School event
  window: Tue 20 Oct 2026 09:00-13:00
  manualAttendance: true
  expected: 420
```

#### Permissions

- `listSpecialEventFree` → `SCOPE_VIEW` (read) · staff
- `createAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `setOperatingCalendarEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.51 | Admission entitlement management | Ticketing Catalogue | CONTRACTED | `createAdmissionRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-222` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-222`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 16: Works in Special Event, Free View & Alternative Admission → Configure temporary/special admission processes that differ from normal venue access. The matrix requires special-event products capable of capturing attendance without physical admission, N- person …

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-222?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save operating calendar entry.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-223` Journey Simulation, Audit & Publication

**Test an entire guest journey—not merely an individual scan—before deploying it.**

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
| Route | `/access-venue/journey-simulation-audit-publication-bo-223` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-005): "Journey" means two things here: this screen simulates access journeys (listGuestJourney, beside simulateGuestJourney), not marketing automation journeys …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Test a whole guest access journey (a sequence of scans with anti-passback rules) before deploying it. Nothing is admitted and no entitlement is consumed during a simulation.

**Fixed on main** (the package already carries these; draw what it says): The list is listJourneys (marketing automation journeys) beside simulateGuestJourney (access). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Sent by *Run journey simulation*** (`simulateGuestJourney`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Journey profile `journeyProfileId` | text field | required | — | — | — | The access journey (`GuestJourneyCommandCenterView.journeyProfileId`) | `simulateGuestJourney` body |
| Scenario `scenario` | radio group | required | — | Standard day · Free view day · Special event · Peak day | — | — | `simulateGuestJourney` body |
| Simulated date `simulatedDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Date the calendar rules are evaluated for; empty is today | `simulateGuestJourney` body |
| Entitlements `entitlementIds` | list of values (chips) | optional | — | — | — | Entitlements the simulated guest holds | `simulateGuestJourney` body |
| Steps `steps` | repeatable rows | optional | — | at least 1; at most 50 | — | The scans, in order | `simulateGuestJourney` body |
| Access point `steps[].accessPointId` | text field | required | — | — | — | — | `simulateGuestJourney` body |
| Direction `steps[].direction` | segmented control | optional | Entry | Entry · Exit | — | — | `simulateGuestJourney` body |
| At `steps[].at` | time picker | optional | — | — | HH:mm, 24-hour | Local time HH:MM | `simulateGuestJourney` body |

#### Outputs: what the screen shows and produces

**Shown**

**Access journeys** (data table, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**The selected journey simulation audit** (detail panel): The pack groups this record's detail under its own headings: “Purchased”, “Arrive”, “Simulation Trace”, “Attendance”, “Remaining”, “Journey Audit”.

| Shows | Format | Notes |
|---|---|---|
| Impossible journey sequences | text | not in the schema: `impossible journey sequences` |
| Missing gates | text | not in the schema: `missing gates` |
| Incompatible hardware | text | not in the schema: `incompatible hardware` |
| Missing companion relationship | text | not in the schema: `missing companion relationship` |
| Conflicting quantities | text | not in the schema: `conflicting quantities` |
| Duplicate attendance | text | not in the schema: `duplicate attendance` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Free View Day (primary button) | navigation or local | — | — | — | — |
| Run journey simulation (primary button) | `simulateGuestJourney` POST `/guest-journey/simulate` | GuestJourneySimulationInput | GuestJourneySimulationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listGuestJourney` (onLoad, The access journey profiles to simulate)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The journey simulation audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the journey simulation audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No journey simulation audit yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the journey simulation audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
simulation: Free View Day - main gate -> wave pool -> re-entry main gate - result admitted, admitted, denied (anti-passback
  30 min)
```

#### Permissions

- `simulateGuestJourney` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listGuestJourney` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.1 | Visual Journey Builder | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.6 | Abandoned Cart Recovery Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.7 | Membership Lifecycle Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.8 | Loyalty Lifecycle Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.9 | Wallet Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.10 | Birthday & Anniversary Campaigns | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.14 | Cross-Sell & Upsell Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.21 | Automation Analytics Dashboard | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.22 | Automation Audit Trail | Marketing & CRM | CONTRACTED | data `Journey` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-223` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-223`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 18: Works in Journey Simulation, Audit & Publication → Test an entire guest journey—not merely an individual scan—before deploying it.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-223?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Free View Day, Run journey simulation.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAdmissionRules": {"method":"POST","path":"/admission-rules","contract":"access","summary":"Create an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"listAdmissionRules": {"method":"GET","path":"/admission-rules","contract":"access","summary":"List admission profiles","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFamilyChildPod": {"method":"GET","path":"/family-child-pod","contract":"access","summary":"Family, Child, POD & Companion Journey","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FamilyChildPodCompanionJourneyView"},
"listFastPassAttraction": {"method":"GET","path":"/fast-pass-attraction","contract":"access","summary":"Fast Pass & Attraction Access Journey","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FastPassAttractionAccessJourneyView"},
"listGroupAttendancePartial": {"method":"GET","path":"/group-attendance-partial","contract":"access","summary":"Group Attendance & Partial Entry Manager","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGroupLeaderFast": {"method":"GET","path":"/group-leader-fast","contract":"access","summary":"Group Leader & Fast B2B Validation","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGuestJourney": {"method":"GET","path":"/guest-journey","contract":"access","summary":"Guest Journey Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMultiParkCrossover": {"method":"GET","path":"/multi-park-crossover","contract":"access","summary":"Multi-Park & Crossover Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MultiParkCrossoverRulesView"},
"listMultiParkCrossover2": {"method":"GET","path":"/multi-park-crossover-2","contract":"access","summary":"Multi-Park & Crossover Journey Orchestrator","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueues": {"method":"GET","path":"/queues","contract":"queue","summary":"List queues","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSpecialEventFree": {"method":"GET","path":"/special-event-free","contract":"access","summary":"Special Event, Free View & Alternative Admission","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SpecialEventFreeViewAlternativeAdmissionView"},
"setFastPassProfile": {"method":"PUT","path":"/fast-pass-profiles","contract":"access","summary":"Create or replace a Fast Pass profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessFastPassProfile","responds":"AccessFastPassProfile"},
"setGroupAdmissionProfile": {"method":"PUT","path":"/group-admission-profile","contract":"access","summary":"Group & B2B Admission Profile Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GroupB2bAdmissionProfileBuilderInput","responds":"GroupB2bAdmissionProfileBuilderView"},
"setGuestCompanionEligibility": {"method":"PUT","path":"/guest-companion-eligibility","contract":"access","summary":"Save a companion eligibility rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestCompanionEligibilityRulesInput","responds":"GuestCompanionEligibilityRulesView"},
"setJourneyProfile": {"method":"PUT","path":"/journey-profiles","contract":"access","summary":"Create or replace a guest journey profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessJourneyProfile","responds":"AccessJourneyProfile"},
"setOperatingCalendarEntry": {"method":"PUT","path":"/operating-calendar-entries","contract":"access","summary":"Create or replace an operating calendar entry","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessOperatingCalendarEntry","responds":"AccessOperatingCalendarEntry"},
"simulateGuestJourney": {"method":"POST","path":"/guest-journey/simulate","contract":"access","summary":"Simulate an access journey","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestJourneySimulationInput","responds":"GuestJourneySimulationView"},
"updateAdmissionRules": {"method":"PUT","path":"/admission-rules/{profileId}","contract":"access","summary":"Update an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"updateQueue": {"method":"PATCH","path":"/queues/{queueId}","contract":"queue","summary":"Amend queue configuration","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Queue"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessFastPassProfile": {"type":"object","x-ticvai-persistence":"access.fast_pass_profile","description":"One Fast Pass profile (e.g. Silver, Gold) - total uses or unlimited, uses consumed per validation, the one-access-per-ride restriction and the eligible attraction categories (declared 29 September, data-model close-out DM1).","required":["id","scopePath","name","unlimited"],"properties":{"id":{"type":"string","format":"uuid","description":"The profileId the list shows"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"name":{"type":"string","maxLength":200},"unlimited":{"type":"boolean","default":false},"totalUses":{"type":"integer","minimum":1,"nullable":true,"description":"Null when unlimited"},"consumptionPerValidation":{"type":"integer","minimum":1,"default":1},"onePerRide":{"type":"boolean","default":false},"eligibleAttractionCategories":{"type":"array","items":{"type":"string"},"description":"The list's eligibleType, e.g. rollerCoaster, dropTower, waterRide, adventureRide"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessJourneyProfile": {"type":"object","x-ticvai-persistence":"access.journey_profile","description":"One guest access journey profile (e.g. School Group Entry) - type, venue, credential used, status and the ordered steps a simulation walks (declared 29 September, data-model close-out DM1).","required":["id","scopePath","name","status"],"properties":{"id":{"type":"string","format":"uuid","description":"The journeyProfileId"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Null is every park of the tenant"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"name":{"type":"string","maxLength":200},"journeyType":{"type":"string","maxLength":60,"nullable":true,"description":"e.g. B2B group, family"},"credentialType":{"type":"string","maxLength":100,"nullable":true,"description":"e.g. group QR, mixed"},"status":{"type":"string","enum":["active","inactive"],"default":"active"},"steps":{"allOf":[{"$ref":"#/components/schemas/AccessJsonList"}],"description":"Ordered journey steps, each an accessPointId with a direction (entry or exit) and an optional local time HH:MM, as GuestJourneySimulationInput.steps"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessJsonList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the row that holds it.** A short list of structured entries read with its row and never queried on its own (thresholds, per-language messages, field mappings, steps), so a child table would add a join for nothing. The property that uses it says what an entry holds (declared 29 September, data-model close-out DM1).","items":{"type":"object"}},
"AccessOperatingCalendarEntry": {"type":"object","x-ticvai-persistence":"access.operating_calendar_entry","description":"One dated entry in a venue operating calendar (normal day, holiday, private event, free-entry day, special event and so on), with whether tickets must be validated. Merges access.special_admission_window, whose free-view and special-event windows are entries carrying an admission type (declared 29 September, data-model close-out DM1)","required":["id","venueId","dayType","startsAt","endsAt","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"dayType":{"type":"string","enum":["normalOperatingDay","weekend","holiday","seasonalSchedule","privateEvent","freeEntryDay","maintenancePeriod","specialEvent","ladiesOnlySession","schoolGroupSession","afterHoursEvent"],"description":"Kind of calendar entry"},"name":{"type":"string","nullable":true},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"ticketValidationRequired":{"type":"boolean","default":true,"description":"False on free-entry days"},"admissionType":{"type":"string","enum":["freeViewDay","specialEvent"],"nullable":true,"description":"Set on special admission windows only"},"attractionValidation":{"type":"boolean","nullable":true,"description":"Special windows: attraction gates keep validating tickets"},"manualAttendanceRequired":{"type":"boolean","nullable":true,"description":"Special windows: operator enters attendance count"},"venueClosed":{"type":"boolean","default":false,"description":"**A day the whole venue is closed** (design-notes correction on BO-019, Block B: \"No operation sets product blackout dates or a venue closure day\"; CHG-CSP-051). Every gate refuses admission for the entry's dates, as `temporaryClosure` does for one attraction, and the closures screen shows it beside the product blackouts (catalogue `setEntitlementTemplateBlackoutDates`). Stopping sales for those dates is the performances' own (`cancelPerformance`, catalogue)."},"priority":{"type":"integer","minimum":0,"maximum":1000,"default":0,"description":"**Which entry wins where two overlap: the higher priority** (decided 2 October 2026, Chinmay, batch 6 set 10a, BO-152: \"The venue sets a priority per entry\"; DEC-229; CHG-CSP-027). A holiday inside a season, a private event on a free-entry day: the venue says which applies by giving it the higher number. Two overlapping entries with the same priority are refused `422 overlapping-entry-same-priority`, so the calendar never has to guess."},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AdmissionRules": {"x-ticvai-persistence":"access.admission_rules","type":"object","required":["id","code","name","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Server-assigned.** Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names.\n"},"code":{"type":"string","maxLength":64},"perProductRules":{"allOf":[{"$ref":"#/components/schemas/PerProductRuleList"}],"description":"BL-059. **Transaction rules were per profile and a ticket type could not state its own.** An annual pass allowing one entry per day and a single ticket allowing one entry ever are different rules, and forcing a profile per product multiplies profiles instead.\n"},"name":{"type":"string","maxLength":200},"openMinutesBefore":{"type":"integer","description":"How long before a performance validation opens."},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean","default":false},"maxReentries":{"type":"integer","nullable":true},"entryLimit":{"type":"object","description":"**How many times the credential may enter** (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). Absent means `unlimited`.","required":["mode"],"properties":{"mode":{"type":"string","enum":["unlimited","once","nTimes","nPerDay","nPerPeriod"],"default":"unlimited"},"count":{"type":"integer","minimum":1,"description":"N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it)"},"periodDays":{"type":"integer","minimum":1,"description":"The period for nPerPeriod"}}},"exitScan":{"type":"string","enum":["required","optional","none"],"default":"optional","description":"(decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. `optional`: exits run in free rotation and headcount is inferred. `none`: the exit has no reader."},"maxExits":{"type":"integer","minimum":0,"nullable":true,"description":"Null is unlimited (decided 29 September, VM close-out)"},"reEntryWindowMinutes":{"type":"integer","minimum":1,"nullable":true,"description":"Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out)"},"sameDayOnly":{"type":"boolean","default":true,"description":"Re-entry only on the day of the exit (decided 29 September, VM close-out)"},"designatedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out)"},"validity":{"type":"object","description":"**When the credential is valid** (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). The admission window above still applies inside it.","required":["anchor"],"properties":{"anchor":{"type":"string","enum":["fixedRange","afterSale","afterActivation","afterFirstUse"],"description":"fixedRange uses from and to; the others count days from the event"},"days":{"type":"integer","minimum":1,"description":"N days after the anchor; required unless the anchor is fixedRange"},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date","description":"Inclusive. Must not be before from (`422`)"},"endOf":{"type":"string","enum":["day","week","month","year"],"nullable":true,"description":"Validity runs to the end of the day, week, month or year the relative period ends in"},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Empty is every day"},"dayTypes":{"type":"array","items":{"type":"string","enum":["peakDates","offPeakDates","holidays","seasons","eventDates"]},"description":"Calendar day types on which access is allowed; empty is every day type"},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Dates on which access is refused whatever else allows it"}}},"crossover":{"type":"object","nullable":true,"description":"**Crossover between parks** (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. Null means the profile admits to one park only.","required":["allowedParkOrgUnitIds"],"properties":{"allowedParkOrgUnitIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"parkOrder":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Required order of parks, if any; empty is any order"},"sameDayOnly":{"type":"boolean","default":true},"differentDayAccess":{"type":"boolean","default":false},"dayPattern":{"type":"string","enum":["consecutiveFromFirstScan","flexibleWithinValidity"],"default":"flexibleWithinValidity"},"maxParkEntries":{"type":"integer","minimum":1,"nullable":true,"description":"Null is unlimited"},"crossoverQuantity":{"type":"integer","minimum":1,"nullable":true,"description":"How many crossovers; null is unlimited"},"crossoverAfterTime":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Earliest venue-local time HH:MM a crossover is allowed"},"prerequisiteParkOrgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The park that must be entered first"},"reEntryAfterCrossover":{"type":"boolean","default":false}}},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Empty means any access point in the venue."},"reEntryVerification":{"type":"string","enum":["credentialOnly","credentialUvStamp","credentialFace","credentialOperator","custom"],"default":"credentialOnly","description":"What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1)."},"ruleConditions":{"type":"object","nullable":true,"description":"The visual rule builder body `setVisualAccessRule` writes: `appliesTo` (products or credential types), `conditions`, `logic` (AND / OR / NOT over the conditions), `decision` (allow, deny, referToOperator, overrideEligible) and `consequences`. **One `jsonb` column on the rule row**, read with the rule and never queried on its own; the locations stay in `access.entry_rule_point` (added 29 September, data-model close-out DM1)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"CreateQueueRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","capacityPerCycle","cycleMinutes"],"properties":{"code":{"type":"string","maxLength":64},"name":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid"},"attractionProductId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["standby","singleRider","fastPass","virtual","accessible","groupOnly","staffOnly"],"default":"standby","description":"5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"},"operatingWindows":{"type":"array","description":"**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n","items":{"type":"object","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue starts running."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue stops running."},"lastEntryMinutesBefore":{"type":"integer","default":0,"description":"**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"}}}},"parentQueueId":{"type":"string","format":"uuid","nullable":true,"description":"Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"},"loadBalanceWithQueueIds":{"type":"array","description":"BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n","items":{"type":"string","format":"uuid"}},"inQueueOfferEnabled":{"type":"boolean","default":false,"description":"**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"},"notifyBeforeCallMinutes":{"type":"integer","default":5,"description":"BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"},"capacityPerCycle":{"type":"integer","minimum":1},"cycleMinutes":{"type":"number","minimum":0},"maxPartySize":{"type":"integer","default":6},"returnWindowMinutes":{"type":"integer","default":15,"description":"How long a called party has to arrive before the entry expires."},"heightRequirementCm":{"type":"integer","nullable":true},"fastPassAllocationPercent":{"type":"number","minimum":0,"maximum":100,"default":0,"description":"Share of each cycle reserved for Fast Pass holders."},"zone":{"type":"string","nullable":true},"fastPass":{"allOf":[{"$ref":"#/components/schemas/QueueFastPass"}],"nullable":true,"description":"The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"}}},
"FamilyChildPodCompanionJourneyView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Family, Child, POD & Companion Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Companion rule identifier"},"relationshipType":{"type":"string","enum":["parentChild","guardianMinor","podCompanion","primaryGuestNanny","groupLeaderGroupMember","other"],"description":"Linked-person relationship this rule governs"},"verificationMethod":{"type":"string","enum":["pairedAdultCredential","assignedAdultBiometric"],"description":"How the accompanying adult is verified"},"assignedAdultRequiredForExit":{"type":"boolean","description":"The assigned adult must be present for the dependent to exit"}},"required":["ruleId"]},
"FastPassAttractionAccessJourneyView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Fast Pass & Attraction Access Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"profileId":{"type":"string","description":"Fast Pass profile identifier"},"totalUses":{"type":"integer","description":"Total Uses (the pack shows 3)"},"eligibleType":{"type":"array","items":{"type":"string"},"description":"Eligible attraction categories: rollerCoaster, dropTower, waterRide, adventureRide"},"name":{"type":"string","description":"Profile name, e.g. Silver, Gold"},"unlimited":{"type":"boolean","description":"Unlimited uses"},"consumptionPerValidation":{"type":"integer","description":"Uses consumed per validation"},"onePerRide":{"type":"boolean","description":"Restrict to one access per ride"}},"required":["profileId"]},
"GroupAttendancePartialEntryManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Group Attendance & Partial Entry Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"waveId":{"type":"string","description":"Admission wave identifier"},"remaining":{"type":"integer","description":"Guests still to arrive after this wave"},"totalEntered":{"type":"integer","description":"Total Entered (the pack shows 48)"},"group":{"type":"string","description":"Group"},"leader":{"type":"string","description":"Leader"},"gate":{"type":"string","description":"Gate"},"operator":{"type":"string","description":"Operator"},"quantity":{"type":"integer","description":"Quantity"},"time":{"type":"string","format":"date-time","description":"Time"},"device":{"type":"string","description":"Device"},"purchased":{"type":"integer","description":"Guests purchased on the group booking"}},"required":["waveId"]},
"GroupB2bAdmissionProfileBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Group & B2B Admission Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"name":{"type":"string","description":"Profile name"},"venueId":{"type":"string","description":"Venue"},"profileId":{"type":"string","description":"The rule row's key (access.group_admission_rule.id); absent creates one (decided 29 September, writers pass)","format":"uuid"},"groupSegments":{"type":"array","items":{"type":"string","enum":["schools","tourOperators","corporateGroups","resellers","travelGroups","camps","families","events"]},"description":"Group segments this profile applies to"},"credentialMode":{"type":"string","enum":["singleGroupQr","groupBarcode","groupRfid","groupLeaderCredential","individualCredentials","hybrid"],"description":"How the group presents its credentials"},"admissionMethod":{"type":"string","enum":["entireGroup","partialGroup","multipleWaves","individualScan","leaderQuantity","manifestBased"],"description":"How the group is admitted at the gate"}},"required":["profileId","venueId","name"]},
"GroupB2bAdmissionProfileBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Group & B2B Admission Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Profile name"},"venueId":{"type":"string","description":"Venue"},"profileId":{"type":"string","description":"Group admission profile identifier"},"groupSegments":{"type":"array","items":{"type":"string","enum":["schools","tourOperators","corporateGroups","resellers","travelGroups","camps","families","events"]},"description":"Group segments this profile applies to"},"credentialMode":{"type":"string","enum":["singleGroupQr","groupBarcode","groupRfid","groupLeaderCredential","individualCredentials","hybrid"],"description":"How the group presents its credentials"},"admissionMethod":{"type":"string","enum":["entireGroup","partialGroup","multipleWaves","individualScan","leaderQuantity","manifestBased"],"description":"How the group is admitted at the gate"}},"required":["profileId","venueId","name"]},
"GroupLeaderFastB2bValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Group Leader & Fast B2B Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"groupBookingId":{"type":"string","description":"Group booking"},"attendance":{"type":"integer","description":"Attendance (the pack shows +112)"},"remaining":{"type":"integer","description":"Guests not yet admitted"},"payment":{"type":"boolean","description":"Payment check passed"},"booking":{"type":"boolean","description":"Booking check passed"},"groupProduct":{"type":"boolean","description":"Group product check passed"},"accessRules":{"type":"boolean","description":"Access rules check passed"},"manifest":{"type":"boolean","description":"Manifest check passed"},"bookedGuests":{"type":"integer","description":"Guests booked"},"visitDateValid":{"type":"boolean","description":"Visit date check passed"}},"required":["groupBookingId"]},
"GuestCompanionEligibilityRulesInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Guest, Companion & Eligibility Rules submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["venueId","name","guestCategory","requiredCompanionCategory","verifyAt"],"properties":{"ruleId":{"type":"string","format":"uuid","description":"Absent creates a rule"},"venueId":{"type":"string"},"name":{"type":"string","maxLength":200},"guestCategory":{"type":"string","enum":["adult","child","junior","senior","pod","podCompanion","nanny","vip","member","staff","accreditation","customerSegment"]},"requiredCompanionCategory":{"type":"string","enum":["adult","podCompanion","nanny","guardian"],"description":"Category of the companion who must be present"},"companionVerification":{"type":"string","enum":["linkedTicket","companionBiometric"],"default":"linkedTicket"},"verifyAt":{"type":"array","items":{"type":"string","enum":["admission","exit","attraction"]},"minItems":1,"description":"Where the companion is checked"},"attractionIds":{"type":"array","items":{"type":"string"},"description":"Where verifyAt includes attraction"}}},
"GuestCompanionEligibilityRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Guest, Companion & Eligibility Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"guestCategory":{"type":"string","enum":["adult","child","junior","senior","pod","podCompanion","nanny","vip","member","staff","accreditation","customerSegment"]},"name":{"type":"string"},"requiredCompanionCategory":{"type":"string","description":"Category of the qualifying companion, e.g. adult"},"companionVerification":{"type":"string","enum":["linkedTicket","companionBiometric"]},"verifyAt":{"type":"array","items":{"type":"string","enum":["admission","exit","attraction"]},"description":"Where the companion is checked (decided 29 September, VM close-out)"},"attractionIds":{"type":"array","items":{"type":"string"}}},"required":["ruleId","guestCategory"]},
"GuestJourneyCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Guest Journey Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"journeyProfileId":{"type":"string","description":"Journey profile identifier"},"journeyName":{"type":"string","description":"Journey, e.g. School Group Entry"},"journeyType":{"type":"string","description":"Journey type, e.g. B2B group, family"},"venueId":{"type":"string","description":"Venue or all parks"},"credentialType":{"type":"string","description":"Credential used, e.g. group QR, mixed"},"status":{"type":"string","enum":["active","inactive"],"description":"Status"}},"required":["journeyProfileId"]},
"GuestJourneyCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeJourneyProfiles":{"type":"integer","description":"Active Journey Profiles"},"groupArrivalsToday":{"type":"integer","description":"Group Arrivals Today"},"guestsViaGroupAdmission":{"type":"integer","description":"Guests via Group Admission"},"familyJourneys":{"type":"integer","description":"Family Journeys"},"reEntryGuests":{"type":"integer","description":"Re-entry Guests"},"crossoversToday":{"type":"integer","description":"Crossovers Today"},"fastPassValidations":{"type":"integer","description":"Fast Pass Validations"},"specialEventAdmissions":{"type":"integer","description":"Special Event Admissions"},"vipAdmissions":{"type":"integer","description":"VIP Admissions"},"journeyExceptions":{"type":"integer","description":"Journey Exceptions"}}},
"GuestJourneySimulationInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"A journey to simulate against the access rules, before it is published (decided 29 September, VM close-out).","required":["journeyProfileId","scenario"],"properties":{"journeyProfileId":{"type":"string","description":"The access journey (`GuestJourneyCommandCenterView.journeyProfileId`)"},"scenario":{"type":"string","enum":["standardDay","freeViewDay","specialEvent","peakDay"]},"simulatedDate":{"type":"string","format":"date","description":"Date the calendar rules are evaluated for; empty is today"},"entitlementIds":{"type":"array","items":{"type":"string"},"description":"Entitlements the simulated guest holds"},"steps":{"type":"array","items":{"type":"object","required":["accessPointId"],"properties":{"accessPointId":{"type":"string"},"direction":{"type":"string","enum":["entry","exit"],"default":"entry"},"at":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time HH:MM"}}},"minItems":1,"maxItems":50,"description":"The scans, in order"}}},
"GuestJourneySimulationView": {"type":"object","x-ticvai-persistence":"none — computed; nothing is admitted or consumed (decided 29 September, VM close-out)","description":"What each step of a simulated journey would decide (decided 29 September, VM close-out).","required":["journeyProfileId","scenario","steps"],"properties":{"journeyProfileId":{"type":"string"},"scenario":{"type":"string","enum":["standardDay","freeViewDay","specialEvent","peakDay"]},"passed":{"type":"boolean","description":"Every step produced the expected decision"},"steps":{"type":"array","items":{"type":"object","properties":{"accessPointId":{"type":"string"},"decision":{"type":"string","enum":["allowed","denied","review"]},"reasonCode":{"type":"string"},"entitlementConsumed":{"type":"string","nullable":true},"decisionTrace":{"type":"array","items":{"type":"string"}}}}}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MultiParkCrossoverJourneyOrchestratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Multi-Park & Crossover Journey Orchestrator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"eventId":{"type":"string","description":"Journey event identifier"},"eventType":{"type":"string","enum":["normalEntry","reEntry","crossover"],"description":"Kind of admission, tracked separately"},"credentialId":{"type":"string","description":"Credential"},"fromParkId":{"type":"string","description":"Park the guest left"},"toParkId":{"type":"string","description":"Park entered"},"occurredAt":{"type":"string","format":"date-time","description":"When it happened"}},"required":["eventId"]},
"MultiParkCrossoverRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Multi-Park & Crossover Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"allowedParks":{"type":"array","items":{"type":"string"},"description":"allowed parks"},"parkOrder":{"type":"array","items":{"type":"string"},"description":"Required park order, if any"},"sameDayCrossover":{"type":"boolean","description":"same-day crossover"},"differentDayAccess":{"type":"boolean","description":"different-day access"},"numberOfParkEntries":{"type":"integer","description":"number of park entries"},"crossoverQuantity":{"type":"integer","description":"crossover quantity"},"crossoverTime":{"type":"string","description":"Earliest local time HH:MM a crossover is allowed"},"prerequisitePark":{"type":"string","description":"prerequisite park"},"reEntryAfterCrossover":{"type":"boolean","description":"re-entry after crossover"},"name":{"type":"string"},"dayPattern":{"type":"string","enum":["consecutiveFromFirstScan","flexibleWithinValidity"]}},"required":["ruleId","allowedParks"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PerProductRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the profile row** (`access.admission_rules.per_product_rules`). The rules are read with the profile and a rule is never queried on its own, so a child table would add a join for nothing.\n","items":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"entriesPerDay":{"type":"integer","nullable":true},"minimumGapMinutes":{"type":"integer","nullable":true,"description":"**Anti-passback in minutes rather than a boolean.** A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back over a fence.\n"},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"biometricPolicy":{"allOf":[{"$ref":"#/components/schemas/BiometricPolicy"}],"description":"BL-105, 3.2.9. **The biometric check is a property of the product, not of the venue** — memberships checked, day tickets not. It sits here rather than on the profile because `perProductRules` is already where a ticket type states its own terms, and a profile per product would multiply profiles to carry one flag.\n**Absent means `disabled`**, and `disabled` is the answer for every product until somebody chooses otherwise. **Inert while `VenueSettings.biometrics.isEnabled` is false**, so a rules profile copied to another venue cannot begin capturing faces there.\n"},"maxPassesPerBiometricIdentity":{"type":"integer","nullable":true,"minimum":1,"description":"BL-096, 2.14.7. **The annual-pass quota, keyed to biometric identity.** `enrolFacePass` already answers 409 where a face is on another annual pass; the constant behind that refusal was one and was invisible. **Null means unlimited** and is the answer for every product that is not an annual pass — a quota applied where nobody asked for one turns a family sharing a day ticket into a fraud alert.\n"}}}},
"Queue": {"x-ticvai-persistence":"queue.queue + queue.queue_operating_window","allOf":[{"$ref":"#/components/schemas/CreateQueueRequest"},{"type":"object","required":["id","status","waitingPartyCount"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/QueueStatus"},"statusReason":{"type":"string","nullable":true},"waitingPartyCount":{"type":"integer"},"waitingGuestCount":{"type":"integer"},"currentWaitMinutes":{"type":"integer","nullable":true},"waitTimeSource":{"$ref":"#/components/schemas/WaitTimeSource"},"waitTimeAsOf":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"},"manualWaitExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"},"manualWaitNote":{"type":"string","maxLength":200,"nullable":true,"readOnly":true,"description":"The `note` given with the current manual figure. Cleared when it expires."},"expectedReopenAt":{"type":"string","format":"date-time","nullable":true}}}]},
"QueueFastPass": {"x-ticvai-persistence":"queue.queue","type":"object","description":"**Which Fast Pass entitlements this lane accepts, and how** (decided 29 September, VM close-out; pack 'Access Control Module' p.109, BO-221 Fast Pass & Attraction Access Journey). Fast Pass stays an entitlement owned by Product & Entitlement; this block is the lane's side of it: which products it honours, the return window, a per-guest daily cap and the access points that redeem it. Stored on the queue row. Only meaningful where `kind` is `fastPass` or `fastPassAllocationPercent` is above 0.\n**Four ways into priority, not one** (decided 29 September, build pass; 5.6.7 and 5.6.34). A guest joins this lane as priority when they hold an entitlement from `entitlementProductIds` (VIP, annual pass, premium package), are a member of a tier in `loyaltyTierIds`, qualify for a live promotion in `promotionIds`, or declare an accessibility need where `accessibilityPriority` is on. The first criterion met is recorded on the entry as `WaitingGuest.priorityBasis`. Every criterion is resolved by the server at join time; nothing the request asserts about a tier or a promotion is trusted. All four draw on the same reserved `fastPassAllocationPercent`, so widening who qualifies never widens the share of the ride they take.\n","required":["entitlementProductIds"],"properties":{"entitlementProductIds":{"type":"array","description":"Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need.\n","items":{"type":"string","format":"uuid"}},"loyaltyTierIds":{"type":"array","description":"5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. Read from the guest's own loyalty position at join time, never from the request, so a guest cannot claim a tier they do not hold. Empty: tier grants nothing on this lane.\n","items":{"type":"string","format":"uuid"}},"promotionIds":{"type":"array","description":"5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. A guest qualifies when the promotion's conditions hold for them at join (the evaluation `promotions` already makes for a price), or by presenting its code in `JoinQueueRequest.promotionCode`. A paused or expired promotion grants nothing.\n","items":{"type":"string","format":"uuid"}},"accessibilityPriority":{"type":"boolean","default":false,"description":"5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. **Taken on trust**, because asking for proof at a ride entrance is worse than the occasional abuse; the declaration is on the entry, so the operator at the front sees it (`listQueueEntries`). A venue that wants proof sells or issues an accessibility pass and lists it in `entitlementProductIds` instead. **Not the `accessible` lane**: that is where a guest who cannot stand in a switchback waits; this moves them ahead in the lane they chose.\n"},"returnWindowMinutes":{"type":"integer","minimum":1,"maximum":240,"default":60,"description":"How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan.\n"},"maxPerGuestPerDay":{"type":"integer","minimum":1,"nullable":true,"description":"Fast Pass redemptions one guest may make on this lane per day; null is no cap."},"allowedAccessPointIds":{"type":"array","description":"Access points that redeem Fast Pass for this lane; empty is the queue's own.","items":{"type":"string","format":"uuid"}}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"SpecialEventFreeViewAlternativeAdmissionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Special Event, Free View & Alternative Admission displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"configId":{"type":"string","description":"Special admission configuration identifier"},"attendance":{"type":"integer","description":"Attendance (the pack shows +85)"},"admissionType":{"type":"string","enum":["freeViewDay","specialEvent"],"description":"Kind of special admission"},"startsAt":{"type":"string","format":"date-time","description":"Start"},"endsAt":{"type":"string","format":"date-time","description":"End"},"attractionValidation":{"type":"boolean","description":"Attraction gates keep validating tickets"},"manualAttendanceRequired":{"type":"boolean","description":"Operator enters attendance count"}},"required":["configId"]},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]}
}
```
