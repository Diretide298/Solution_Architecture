# WS114 — ACCREDITATION board 7

**10 screens · 7 operations · 6 schemas · 3 permissions**

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
| `BO-674` | Accreditation Communications Command Center | B–D | 0 | 5 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-675` | Notification Rule Management | B–D | 9 | 0 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `BO-676` | Expiry & Renewal Notification Scheduler | B–D | 6 | 0 | 6 | 5 | 0 | 0 | — | notStarted (—) |
| `BO-677` | Communication Template Library | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-678` | Channel, Language & Branding Configuration | B–D | 9 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-679` | Manual & Bulk Communication Center | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-680` | Accreditation Bulk Import | B–D | 0 | 0 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-681` | Import Validation & Processing Monitor | B–D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-682` | Accreditation Export & Data Extract Center | B–D | 7 | 0 | 6 | 4 | 0 | 6 | — | notStarted (—) |
| `BO-683` | Delivery, Batch & Operational History | B–D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-674, BO-677, BO-679, BO-680, BO-681, BO-683 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-674` Accreditation Communications Command Center

**Central dashboard for accreditation notifications and operational communications.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Dashboard analytics shall show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-communications-command-center-bo-674` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): The only bound operation was the rule write, used "at a glance"; the rules are edited on BO-675. No read returns accreditation notification sends or delivery … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of accreditation notification sends and delivery outcomes (or an accreditation filter on listDeliveryQueueFailure).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The landing page of the communications and bulk-operations board: what was sent, what is scheduled, what failed, and quick routes to send, configure rules, templates, imports and exports. Per VO-R02 it is a command-centre dashboard. The one thing to get right: failures and exceptions lead (a rejection email that never arrived is a complaint tomorrow), and every figure is about accreditation messages only.

**Fixed on main** (the package already carries these; draw what it says): Analytics names (Delivery success rate, Notifications by type, by channel, Failure trends, Upcoming scheduled communications) are drawn as … (CHG-SBO-016); The only bound operation is a write (setAccreditationNotificationRules) used "at a glance" (CHG-WIR-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **filters (Tenant, Event, Venue, Programme, Category, Notification type, Channel, Delivery status, Date range)**: A filter bar; Tenant only for tenant-level users (VO-R09), Channel and Delivery status as chips, Date range defaults to the last 7 days. *(source: screens/P08-venue-back-office.yaml#BO-675)*

#### Outputs: what the screen shows and produces

**Shown**

**Communications** (chart): Delivery success rate, notifications by type and channel, failure trends and upcoming scheduled communications are charts and tiles on a dashboard (VO-R02), not table columns.

| Shows | Format | Notes |
|---|---|---|
| Delivery success rate | text | not in the schema: `Delivery success rate` |
| Notifications by type | text | not in the schema: `Notifications by type` |
| Notifications by channel | text | not in the schema: `Notifications by channel` |
| Failure trends | text | not in the schema: `Failure trends` |
| Upcoming scheduled communications | text | not in the schema: `Upcoming scheduled communications` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Notifications sent, Scheduled, Pending delivery, Delivered, Failed, Approval notifications, Expiry notifications, Renewal reminders, Manual communications, Communication exceptions; Failed and Exceptions red above zero. *(source: screens/P08-venue-back-office.yaml#BO-674 / screens/P08-venue-back-office.yaml#BO-675)*
- **Charts**: Delivery success rate (percentage with trend), Notifications by type (bar), by channel (bar), Failure trend (line, daily), Upcoming scheduled communications (agenda list for the next 7 days). *(source: screens/P08-venue-back-office.yaml#BO-675)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Quick actions**: Send communication (BO-679), Create rule (BO-675), Manage templates (BO-677), Import records (BO-680), Export data (BO-682). *(source: screens/P08-venue-back-office.yaml#BO-675)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-675` Notification Rule Management: *Notification Rule Management*
- → `BO-676` Expiry & Renewal Notification Scheduler: *Expiry & Renewal Notification Scheduler*
- → `BO-677` Communication Template Library: *Communication Template Library*
- → `BO-678` Channel, Language & Branding Configuration: *Channel, Language & Branding Configuration*
- → `BO-679` Manual & Bulk Communication Center: *Manual & Bulk Communication Center*
- → `BO-680` Accreditation Bulk Import: *Accreditation Bulk Import*
- → `BO-681` Import Validation & Processing Monitor: *Import Validation & Processing Monitor*
- → `BO-682` Accreditation Export & Data Extract Center: *Accreditation Export & Data Extract Center*
- → `BO-683` Delivery, Batch & Operational History: *Delivery, Batch & Operational History*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation communications list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation communications untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation communications yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation communications are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Messaging provider down**: Banner "Email provider not responding since 09:10; 42 messages queued" and the Pending tile in amber. *(source: designer default)*

#### Consistency with other screens

- Match `BO-791`: Delivery, retry and failover of messages belong to the communication platform; this dashboard is its accreditation-filtered view and must use the same delivery status names.
- Match `BO-683`: Every tile drills into the operational history filtered.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  sent: 4820
  scheduled: 312
  pending: 42
  delivered: 4701
  failed: 77
  approval: 1240
  expiry: 610
  renewal: 288
  manual: 6
  exceptions: 3
successRate: 97.6%
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-674` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-674`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 1: Opens Accreditation Communications Command Center → Central dashboard for accreditation notifications and operational communications.
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F223 branch at step 1 (expected): when Nothing has been set up on Accreditation Communications Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F223 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-674?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-675`, `BO-676`, `BO-677`, `BO-678`, `BO-679`, `BO-680`, `BO-681`, `BO-682`, `BO-683`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-675` Notification Rule Management

**Configure when accreditation notifications are automatically triggered.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each rule shall define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/notification-rule-management-bo-675` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of AccreditationNotificationRules; affects BO-675 and BO-676.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Automatic notification rules per programme: which lifecycle event triggers which message, to whom (holder, organisation, sponsor, accreditation team), on which channel and in which language. Per DI-663 applicants are told at every status change, so the approved, rejected and information-requested rules ship on by default. The one thing to get right: the rule set for a programme is saved as one list, and every trigger the pack names has a row, even where the contract cannot yet hold it.

**Known correction pending (do not draw the wrong version)**

- **Write bound with no read** Why: There is no get operation for AccreditationNotificationRules; a whole-list PUT cannot be edited safely (VO-R04). *(source: contracts/satellite/accreditation.yaml#setAccreditationNotificationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Rule items lack language, category scope, active/inactive and a timing after the event; channels are free strings** Why: The pack's rule definition lists Trigger, Recipient, Channel, Template, Timing, Event/programme scope, Category, Language, Active/inactive. *(source: screens/P08-venue-back-office.yaml#BO-676 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationNotificationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Triggers Resubmitted, Credential issued, Credential activated, Reactivated and Renewal approved are missing from the event enum** Why: Named by the pack; DI-663 asks for a notice at each status change. *(source: screens/P08-venue-back-office.yaml#BO-675 / screens/P08-venue-back-office.yaml#BO-676 / DI-663; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Trigger | select field | — | — | — | — | — | — |
| Recipient | select field | — | — | — | — | — | — |
| Communication channel | select field | — | — | — | — | — | — |
| Template | select field | — | — | — | — | — | — |
| Timing | select field | — | — | — | — | — | — |
| Event/program scope | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Active/inactive status | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **programme**: Picked first; the rule list belongs to a programme. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationNotificationRules)*
- **trigger**: Select of lifecycle events in plain words (Application received, Information requested, Approved, Rejected, Credential ready, Expiring soon, Renewal window open, Expired, Suspended, Revoked). The pack's others (Resubmitted, Credential issued, Credential activated, Reactivated, Renewal approved) listed greyed. *(source: screens/P08-venue-back-office.yaml#BO-675 / screens/P08-venue-back-office.yaml#BO-676 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationNotificationRules)*
- **recipients**: Chips Holder, Organisation, Sponsor, Accreditation team (several allowed). Expiring and expired default to Holder plus Organisation, as the contract insists. *(source: contracts/satellite/accreditation.yaml#setAccreditationNotificationRules)*
- **channels**: Chips from the channels enabled in BO-678 (Email, SMS, App notification, In-platform); never free text. *(source: screens/P08-venue-back-office.yaml#BO-678)*
- **template / timing / language / category / active**: Template picker from BO-677 filtered by trigger; Timing (Immediately, or N days before for expiry triggers); Language and Category scope and Active switch drawn greyed until stored (see corrections). Arabic and English variants per DI-019. *(source: screens/P08-venue-back-office.yaml#BO-676 / DI-019)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rules table**: Trigger, Recipients, Channels, Template, Timing, Active; grouped by lifecycle stage (Application, Credential, Lifecycle, Expiry and renewal). *(source: screens/P08-venue-back-office.yaml#BO-676)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rules**: Sends the programme's whole rule list (VO-R04); a removed row is a deleted rule, so the confirm lists removed triggers. *(source: contracts/satellite/accreditation.yaml#setAccreditationNotificationRules)*
- **Send test**: Sends the rule's template to the signed-in user with sample values. *(source: designer default)*

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The notification rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the notification rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No notification rule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Disabling the Approved or Rejected rule**: Warn "Applicants will not be told of this decision (DI-663)" and require a reason. *(source: DI-663)*
- **Holder without email and the rule is email only**: Rule saves; the history (BO-683) shows those sends as Failed "No email on file". *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*

#### Consistency with other screens

- Match `BO-676`: Expiry and renewal sequences are rules of the same list with days before; one record, one Save.
- Match `BO-677`: Templates are picked from the library by trigger.
- Match `ACC-004`: The applicant's status page on P11 shows the same status names the messages use.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- trigger: Approved
  recipients: Holder, Organisation
  channels: Email, App
  template: Approval - EN/AR
  timing: Immediately
- trigger: Information requested
  recipients: Holder
  channels: Email, SMS
  template: Additional information request
  timing: Immediately
- trigger: Expiring soon
  recipients: Holder, Organisation
  channels: Email
  template: Expiry reminder
  timing: 30 days before
```

#### Permissions

- `setAccreditationNotificationRules` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.36 | Accreditation Expiry Notifications - System shall notify users before accreditation expiration. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.43 | Accreditation Notifications - System shall send accreditation status notifications. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.44 | Approval Notifications - System shall notify applicants of approval decisions. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.45 | Renewal Notifications - System shall notify users of upcoming renewals. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.46 | Expiration Notifications - System shall notify users of upcoming expirations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Lifecycle: activation, expiry, renewal, suspension; if a document (e.g. Emirates ID) expires before the event, a resubmission request is raised and the credential is blocked if unresolved. Applicants are notified at each status change (approved, rejected, needs validation). *(client request · MoM 7 Sep 2026, 4.6 / 4.7 Lifecycle & Notifications · DI-663)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-675` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-675`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 2: Works in Notification Rule Management → Configure when accreditation notifications are automatically triggered.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-675?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-676` Expiry & Renewal Notification Scheduler

**Configure proactive reminders before accreditation expiry or renewal.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/expiry-renewal-notification-scheduler-bo-676` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Reminder sequences before and after expiry, and renewal invitations: 30, 14, 7 and 1 day before, then on expiry. The one thing to get right: a sequence is a list of rules on the same trigger with different day offsets, drawn as a timeline, with duplicate protection so a holder never gets two "final reminders"; and the upcoming sends are visible on a calendar with day, week and month views (VO-R01).

**Known correction pending (do not draw the wrong version)**

- **Label "Days before/after event" is wrong for the anchor** Why: The pack anchors the sequence on expiry (and on the renewal window), and the contract holds daysBefore only; there is no "after". *(source: screens/P08-venue-back-office.yaml#BO-676 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationNotificationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Escalation rule, retry policy and duplicate protection have no field** Why: Listed by the pack; rules carry event, daysBefore, recipients, channels and template only. *(source: screens/P08-venue-back-office.yaml#BO-677 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationNotificationRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Places sends in time with no calendar component** Why: Per VO-R01 a calendar with day, week and month views. *(source: DI-907 / DI-919; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Write bound with no read** Why: No get for the rule list (VO-R04). *(source: contracts/spine/access.yaml#setJourneySequenceRule; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Days before/after event | select field | — | — | — | — | — | — |
| Recipient | select field | — | — | — | — | — | — |
| Template | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Escalation rule | select field | — | — | — | — | — | — |
| Retry policy | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **sequence steps**: A vertical timeline of steps, each "N days before expiry" (or "On expiry"), Recipient, Template, Channel. Pre-filled with the pack's sequence: 30 Reminder 1, 14 Reminder 2, 7 Urgent, 1 Final, 0 Expiration notice. Days are whole numbers, 0-365, unique per sequence. *(source: screens/P08-venue-back-office.yaml#BO-676 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationNotificationRules)*
- **renewal sequence**: A separate tab with Eligibility notice, Invitation, Reminder, Final reminder, Confirmation, anchored to the renewal window opening. *(source: screens/P08-venue-back-office.yaml#BO-676)*
- **escalation rule / retry policy**: Escalation ("If not renewed 7 days before, also notify the organisation and accreditation team") and Retry (attempts, interval) drawn greyed until stored. *(source: screens/P08-venue-back-office.yaml#BO-677)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Upcoming sends calendar**: Day, Week and Month views (VO-R01) of scheduled reminders with counts per day; clicking a day lists the holders. *(source: screens/P08-venue-back-office.yaml#BO-675)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save sequence**: Writes the steps as rules in the programme's rule list (whole list, VO-R04). *(source: contracts/satellite/accreditation.yaml#setAccreditationNotificationRules)*

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The expiry renewal notification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the expiry renewal notification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No expiry renewal notification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Holder renews after Reminder 2**: Remaining steps are cancelled for that holder; the calendar count drops. *(source: screens/P08-venue-back-office.yaml#BO-677)*
- **Two steps on the same day offset**: Refused at the field ("Already a step at 7 days"). *(source: screens/P08-venue-back-office.yaml#BO-677)*
- **Holder expiry changed after reminders were scheduled**: Schedule recalculates; already-sent steps are not resent (duplicate protection). *(source: screens/P08-venue-back-office.yaml#BO-677)*

#### Consistency with other screens

- Match `BO-675`: Same rule list; the sequence editor is a view of the expiry triggers.
- Match `BO-672`: The expiry monitor shows the last reminder sent per holder.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
expirySequence:
- days: 30
  step: Reminder 1
  recipient: Holder
  channel: Email
- days: 14
  step: Reminder 2
  recipient: Holder, Organisation
  channel: Email
- days: 7
  step: Urgent reminder
  recipient: Holder, Organisation
  channel: Email, SMS
- days: 1
  step: Final reminder
  recipient: Holder, Organisation, Accreditation team
  channel: Email, SMS
- days: 0
  step: Expiration notice
  recipient: Holder, Organisation
  channel: Email
```

#### Permissions

- `setAccreditationNotificationRules` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.36 | Accreditation Expiry Notifications - System shall notify users before accreditation expiration. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.43 | Accreditation Notifications - System shall send accreditation status notifications. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.44 | Approval Notifications - System shall notify applicants of approval decisions. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.45 | Renewal Notifications - System shall notify users of upcoming renewals. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.46 | Expiration Notifications - System shall notify users of upcoming expirations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-676` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-676`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 4: Works in Expiry & Renewal Notification Scheduler → Configure proactive reminders before accreditation expiry or renewal.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-676?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-677` Communication Template Library

**Manage reusable accreditation communication templates (merged into BO-785 Template Library).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/communication-template-library-bo-677` |

**What the spec says about it.** **Merged into BO-785** (decided 2 October 2026, Chinmay: duplicate screens merged as proposed; CHG-SBO-021). Accreditation communication templates are message templates (listMessageTemplates) in the one library, filtered to the accreditation purpose (design-note correction customer-marketing BO-785). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-785, and nothing on it is built separately.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The accreditation team's message templates (application received, documents missing, approved, rejected, credential ready). They are transactional messages to applicants, so they need no marketing consent and must carry no promotion.

**Known correction pending (do not draw the wrong version)**

- **Only listMessageTemplates is declared; templates cannot be created or edited here, and there is no filter for accreditation templates.** Why: Either link to BO-785 for editing, or add the create and update operations and a purpose/module filter. *(source: contracts/satellite/marketing-crm.yaml#listMessageTemplates; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Template row**: Code, channel, kind (transactional), languages with missing ones flagged, status. *(source: contracts/satellite/marketing-crm.yaml#listMessageTemplates)*

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Routes to BO-785 while it opens. |
| Error (`?state=error`) | Could not open BO-785; says so and offers to retry. |
| Empty, first run (`?state=emptyFirstRun`) | Never shown: this id routes to BO-785, whose empty states apply. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: this id routes to BO-785. |
| Permission denied (`?state=emptyNoAccess`) | As BO-785: shown when the caller lacks the access BO-785 requires, named in words. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-785`: Same template component and rules; this is the accreditation-filtered view of the one library.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
templates:
- ACC-RECEIVED (email, EN AR)
- ACC-DOCS-MISSING (email, WhatsApp, EN)
- ACC-APPROVED (email, EN AR)
```

#### Permissions

**A refused user sees:** As BO-785: shown when the caller lacks the access BO-785 requires, named in words.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-677` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-677`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 6: Works in Communication Template Library → Manage reusable accreditation communication templates.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-677?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-678` Channel, Language & Branding Configuration

**Control how communications are delivered and branded.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/channel-language-branding-configuration-bo-678` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-005): setLocalizationBrandingCustomer sets a waiver version's languages, branding and channels; accreditation communication branding is not a waiver version … Contract gap recorded 2 October 2026 (CHG-WIR-007): No operation configures accreditation communication branding and sender identity.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** How accreditation communications are delivered and branded: sender identity, reply-to, default and alternative languages, tenant, event and venue branding, header and footer, contact information.

**Fixed on main** (the package already carries these; draw what it says): The only operation is setLocalizationBrandingCustomer, which sets a WAIVER version's languages, branding and channels. (CHG-WIR-005); A select labelled "Key requirement - 12.1.57". (CHG-SBO-019).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Sender identity | select field | — | — | — | — | — | — |
| Reply information | select field | — | — | — | — | — | — |
| Default language | select field | — | — | — | — | — | — |
| Alternative languages | select field | — | — | — | — | — | — |
| Tenant logo | select field | — | — | — | — | — | — |
| Event branding | select field | — | — | — | — | — | — |
| Venue branding | select field | — | — | — | — | — | — |
| Header/footer | select field | — | — | — | — | — | — |
| Contact information | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Sender identity and reply-to**: Chosen from the brand's verified sender identities (platform-level), not typed. *(source: contracts/satellite/marketing-crm.yaml#setSenderIdentityDomain; DI-560)*
- **Languages**: Default language and alternatives; English and Arabic as a pair by default. *(source: DI-019)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel language branding configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel language branding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel language branding configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sender: accreditation@coastalaqua.ae (reply-to media@coastalaqua.ae)
languages:
- English (default)
- Arabic
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-678` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-678`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 8: Works in Channel, Language & Branding Configuration → Control how communications are delivered and branded.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-678?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-679` Manual & Bulk Communication Center

**Allow authorized operators to communicate with selected accreditation populations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/manual-bulk-communication-center-bo-679` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): sendTransactionalMessage declares the service and partner audiences only, and is per message; a staff screen cannot call it (design-notes correction …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Authorised operators message a selected accreditation population (all approved media for an event, all applicants missing a document). These are operational messages about their accreditation; no marketing may ride on them.

**Fixed on main** (the package already carries these; draw what it says): sendTransactionalMessage is service and partner audience only, but is the staff screen's only action. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Population**: Chosen by programme, category and status, with the recipient count before sending. *(source: screens/P08-venue-back-office.yaml#BO-679)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Send result**: Queued, delivered and failed counts, with failures retried or sent on the fallback channel. *(source: DI-559)*

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The manual bulk communication list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the manual bulk communication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No manual bulk communication yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the manual bulk communication are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
population: Approved media - Coastal Aqua Summer Festival - 86 recipients
message: Your media credential is ready for collection at Gate 2 from 10:00 on 14 Oct 2026.
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-679` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-679`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 10: Works in Manual & Bulk Communication Center → Allow authorized operators to communicate with selected accreditation populations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-679?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-680` Accreditation Bulk Import

**Import accreditation records at scale.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-bulk-import-bo-680` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Bulk import of an organisation's roster from the Excel template (a broadcaster's 200 crew, a contractor's 1,000 workers). A guided wizard: download template, upload, map columns, validate, resolve, submit. The one thing to get right: nothing is written until validation is complete, duplicates (same passport or Emirates ID) are caught row by row, and per DI-664 each imported person still goes through profile, documents and approval rather than becoming an accredited holder straight from a spreadsheet.

**Known correction pending (do not draw the wrong version)**

- **Import outcome is created/updated holders, so an imported row becomes an accredited holder without review** Why: DI-664 says each imported record still goes through profile, documents and approval; the import should create applications (submitted) not holders. *(source: DI-664 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationImportResult; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No template download, no column mapping, and no way to submit documents with the roster** Why: The pack and DI-664 ask for an Excel template with details and documents at once and column mapping; the call takes one spreadsheet asset only. *(source: screens/P08-venue-back-office.yaml#BO-680 / DI-664 / contracts/satellite/accreditation.yaml#importAccreditationHolders; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Row outcome is a free string; the pack's Valid / Warning / Error / Duplicate is a closed set** Why: Row filters and colours need the enum. *(source: screens/P08-venue-back-office.yaml#BO-681 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationImportResult; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Bulk import is reached from the Communications Command Center** Why: Matches the pack's Board 7, but the import is also a quick action on the Accreditation Command Center (BO-615) where organisations' rosters are managed; add that entry. *(source: screens/P08-venue-back-office.yaml#BO-674 / screens/P08-venue-back-office.yaml#BO-680; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How are documents (ID scans, photos) supplied with a bulk roster - a zip matched by file name, or uploaded per person afterwards?** → Drawn default accepted: Draw an optional "Documents (zip)" upload in step 2 with "File names must match the ID number column", greyed. *(decided by Chinmay, 2026-10-02; DEC-486 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **programme / organisation**: Programme required; organisation optional (all rows belong to it when set, and its users see the result on P11). *(source: contracts/satellite/accreditation.yaml#importAccreditationHolders / DI-655)*
- **file**: The programme's template only (XLSX or CSV), downloaded from step 1 with the programme's form fields as columns and an instructions sheet in English and Arabic. Uploaded as an asset first. *(source: screens/P08-venue-back-office.yaml#BO-680 / DI-664 / DI-019)*
- **column mapping**: Auto-matched by header; unmatched columns shown for manual mapping; required form fields must be mapped before Validate. *(source: screens/P08-venue-back-office.yaml#BO-680)*
- **default access profile**: Optional; defaults to each category's default profile, and is applied only once a record is approved. *(source: contracts/satellite/accreditation.yaml#importAccreditationHolders / DI-664)*
- **mode**: Not a field. "Validate" sends validateOnly; "Submit import" sends commit, enabled only after a clean validation. *(source: screens/P08-venue-back-office.yaml#BO-681 / contracts/satellite/accreditation.yaml#importAccreditationHolders)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Import accreditation holders (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Wizard steps**: Download template > Upload > Map columns > Validate > Resolve > Submit, with the current step and row counts in the header. *(source: screens/P08-venue-back-office.yaml#BO-680)*
- **Row results**: Each row with the pack's four statuses, Valid (green), Warning (amber, can import), Error (red, cannot), Duplicate (purple, identity conflict with an existing holder or another row), and the detail ("Emirates ID 784-1990-... already accredited as ACC-2026-000912"). Filter by status; error report download. *(source: screens/P08-venue-back-office.yaml#BO-681 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationImportResult)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validate**: Runs the import in validate-only mode and shows rows read, would create, would update, rejected and identity conflicts. *(source: contracts/satellite/accreditation.yaml#importAccreditationHolders)*
- **Submit import**: Commits valid and warning rows; the confirm states the counts and that errors and duplicates are skipped. Result opens in the processing monitor (BO-681). *(source: contracts/satellite/accreditation.yaml#importAccreditationHolders / F223 step 12)*

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation bulk import list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation bulk import untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation bulk import yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation bulk import are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **The same person appears twice in the file**: Both rows marked Duplicate with each other's row number. *(source: contracts/satellite/accreditation.yaml#importAccreditationHolders / DI-692)*
- **File larger than the inline limit (e.g. 1,000 rows with documents)**: Validation runs in the background with progress; the user can leave and find it in BO-681. *(source: DI-664)*
- **Programme closed for applications**: Block at step 1 with "Applications closed on 1 Dec 2026". *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationProgramme)*

#### Consistency with other screens

- Match `BO-681`: Same row statuses and wording; the monitor is where a submitted import is followed.
- Match `BO-631`: Duplicates found here use the same identity-conflict wording and resolution as single applications.
- Match `P11`: The organisation portal's bulk upload (DI-664) uses the same template and row statuses.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
file: GulfMediaNetwork_WinterFestival_crew.xlsx
result:
  rowsRead: 214
  valid: 196
  warning: 9
  error: 6
  duplicate: 3
rows:
- row: 12
  name: Rahul Menon
  status: Warning
  detail: Photo below recommended resolution
- row: 47
  name: Omar Haddad
  status: Duplicate
  detail: Passport already accredited as ACC-2026-000912
- row: 88
  name: Maria Santos
  status: Error
  detail: Category 'Press' does not exist in this programme
```

#### Permissions

- `importAccreditationHolders` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.54 | Accreditation Import - System shall support bulk import of accreditation records. | Accreditation & Credential Management | CONTRACTED | `importAccreditationHolders` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Bulk: a company with many members (e.g. 1,000) gets an Excel template to submit all details and documents at once; each imported record still goes through profile, documents and approval. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-664)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-680` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-680`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 12: Works in Accreditation Bulk Import → Import accreditation records at scale.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-680?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Import accreditation holders, Cancel.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-681` Import Validation & Processing Monitor

**Govern and monitor bulk accreditation imports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The screen shall display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/import-validation-processing-monitor-bo-681` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): importAccreditationHolders (a POST that runs an import) was bound on load, so opening the monitor would start an import; the import is run from BO-680. A list of … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists accreditation import batches or loads one.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The list of import batches and their progress, with row-level errors and an error report. Used to follow a large import and to answer "which of my 200 crew went in". The one thing to get right: a batch is a lasting record with an id, status and counts, and every imported record keeps its batch reference.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- AccreditationImportResult has no batch id, file name, uploader, time or processing status (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): importAccreditationHolders (a POST that runs an import) is bound on load (CHG-WIR-001); Table and panel titled "Every import validation processing" / "The selected import validation processing" (CHG-SBO-016).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Import batches** (data table)

| Shows | Format | Notes |
|---|---|---|
| Import batch ID | text | not in the schema: `Import batch ID` |
| File name | text | not in the schema: `File name` |
| Uploaded by | text | not in the schema: `Uploaded by` |
| Upload date/time | text | not in the schema: `Upload date/time` |
| Total records | text | not in the schema: `Total records` |
| Valid records | text | not in the schema: `Valid records` |
| Warning records | text | not in the schema: `Warning records` |
| Failed records | text | not in the schema: `Failed records` |
| Duplicate records | text | not in the schema: `Duplicate records` |
| Processing status | text | not in the schema: `Processing status` |

**The selected batch** (detail panel): The pack groups this record's detail under its own headings: “Processing statuses shall include”.

| Shows | Format | Notes |
|---|---|---|
| Import batch ID | text | not in the schema: `Import batch ID` |
| File name | text | not in the schema: `File name` |
| Uploaded by | text | not in the schema: `Uploaded by` |
| Upload date/time | text | not in the schema: `Upload date/time` |
| Total records | text | not in the schema: `Total records` |
| Valid records | text | not in the schema: `Valid records` |
| Warning records | text | not in the schema: `Warning records` |
| Failed records | text | not in the schema: `Failed records` |
| Duplicate records | text | not in the schema: `Duplicate records` |
| Processing status | text | not in the schema: `Processing status` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Batch list**: Columns as the pack: Import batch ID (IMP-2026-0142), File name, Uploaded by, Upload date/time, Total, Valid, Warning, Failed, Duplicate, Processing status. Newest first, cursor paging (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-681)*
- **Processing status**: The pack's sequence as a chip, Uploaded > Validating > Ready > Processing > Completed / Partially completed / Failed; Partially completed in amber with the failed count. *(source: screens/P08-venue-back-office.yaml#BO-681)*
- **Batch detail**: Row table with status and detail (same as BO-680), and the created records linking to their applications. *(source: screens/P08-venue-back-office.yaml#BO-681 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationImportResult)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Download error report**: XLSX of the failed and duplicate rows with a reason column, in the template's layout so it can be fixed and re-uploaded. *(source: screens/P08-venue-back-office.yaml#BO-681)*
- **Continue import**: For a batch in Ready, opens BO-680 at the Submit step. *(source: screens/P08-venue-back-office.yaml#BO-681)*

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The import validation processing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the import validation processing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No import validation processing yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the import validation processing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Batch failed half-way through commit**: Status Partially completed with the counts committed; re-running commits only the rows not yet created. *(source: screens/P08-venue-back-office.yaml#BO-681)*
- **User not the uploader**: Sees batches of their venue; personal data in rows needs the same rights as the holder directory. *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-680`: Same statuses and row wording.
- Match `BO-683`: Each batch appears in the operational history.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
batches:
- id: IMP-2026-0142
  file: GulfMediaNetwork_WinterFestival_crew.xlsx
  by: Maria Santos
  at: 02 Dec 2026 14:05
  total: 214
  valid: 196
  warning: 9
  failed: 6
  duplicate: 3
  status: Partially completed
- id: IMP-2026-0141
  file: AlNoor_contractors_Dec.xlsx
  by: Rahul Menon
  at: 01 Dec 2026 09:40
  total: 1000
  valid: 1000
  warning: 0
  failed: 0
  duplicate: 0
  status: Completed
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-681` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-681`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 14: Works in Import Validation & Processing Monitor → Govern and monitor bulk accreditation imports.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-681?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-682` Accreditation Export & Data Extract Center

**Export authorized accreditation data for operational or reporting purposes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§The system shall capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `exportId` (navigation) |
| Route | `/access-venue/accreditation-export-data-extract-center-bo-682` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): runReport and exportReportResult were a second export path beside exportAccreditationData; the accreditation export is the one the pack describes, and reports … Removed 2 October 2026 (CHG-WIR-001): runReport and exportReportResult were a second export path beside exportAccreditationData; the accreditation export is the one the pack describes, and reports …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Exporting accreditation data (holders, applications, credentials, access assignments, documents) as CSV or XLSX, with a history of who exported what. The typical export is the register a security team is handed before an event. The one thing to get right: personal data is off by default, needs a separate permission and a stated purpose, and the download link expires.

**Known correction pending (do not draw the wrong version)**

- **Requested by, Export date/time, Number of records and Export status are drawn as select inputs** Why: They are the export history columns the system captures, not choices the user makes. *(source: screens/P08-venue-back-office.yaml#BO-683 / screens/P08-venue-back-office.yaml#BO-682; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Select field "Key requirement 12.1.55"** Why: Pack prose turned into a field; remove. *(source: screens/P08-venue-back-office.yaml#BO-682; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Filters Event, Venue, Credential type and Date range are not in the export request** Why: The pack lists them; the request has programme, status, organisation, category and validOn. *(source: screens/P08-venue-back-office.yaml#BO-681 / screens/P08-venue-back-office.yaml#BO-683 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationDataExport; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): runReport and exportReportResult are bound beside exportAccreditationData, with entry params executionId and reportId (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Requested by | select field | — | — | — | — | — | — |
| Export date/time | select field | — | — | — | — | — | — |
| Filters | select field | — | — | — | — | — | — |
| Fields exported | select field | — | — | — | — | — | — |
| Number of records | select field | — | — | — | — | — | — |
| Export status | select field | — | — | — | — | — | — |
| Key requirement: 12.1.55 | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationHolders` ?programmeId |
| Organisation | picker: choose an organisation | — | — | `listAccreditationHolders` ?organisationId |
| Status | text field | — | — | `listAccreditationHolders` ?status |
| Expiring within days | number field (days) | — | — | `listAccreditationHolders` ?expiringWithinDays |
| Status | text field | — | — | `listAccreditationExports` ?status |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **dataset**: One of Holders, Applications, Credentials, Access assignments, Documents (cards, one choice). *(source: contracts/satellite/accreditation.yaml#exportAccreditationData)*
- **filters**: Programme, Status, Organisation, Category, and "Valid on" (a date - "only accreditations valid on 15 Dec 2026"). The pack's Event, Venue, Credential type and Date range are greyed until supported. *(source: screens/P08-venue-back-office.yaml#BO-681 / screens/P08-venue-back-office.yaml#BO-683 / contracts/satellite/accreditation.yaml#/components/schemas/AccreditationDataExport)*
- **fields**: Checklist of the dataset's columns, standard set pre-ticked; personal columns (contact, date of birth, nationality, document references) appear only when Include personal data is on. *(source: contracts/satellite/accreditation.yaml#exportAccreditationData)*
- **includePersonalData / purpose**: A switch disabled with "Needs personal-data export rights" for users without them (VO-R08); when on, Purpose (max 500) is required and the confirm says the export is recorded in the audit trail. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationDataExport)*
- **format**: CSV or XLSX. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationDataExport)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Export history**: Columns from the pack: Requested by, Export date/time, Filters (as a short sentence), Fields (count, hover list), Records, Status (Queued, Running, Ready, Failed, Expired), with a padlock on exports that carried personal data. Cursor paging. *(source: screens/P08-venue-back-office.yaml#BO-683 / contracts/satellite/accreditation.yaml#listAccreditationExports)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Export**: Queues the export and adds a row Queued that becomes Ready with Download; large exports are asynchronous, the user may leave. *(source: contracts/satellite/accreditation.yaml#exportAccreditationData / contracts/satellite/accreditation.yaml#getAccreditationExport)*
- **Download**: Fetches the signed link; an Expired row offers "Export again" with the same settings instead of a link. *(source: contracts/satellite/accreditation.yaml#getAccreditationExport)*

**Data it reads**: `listAccreditationHolders` (onLoad, Export); `listAccreditationExports` (onLoad, Export history: requested by, date, filters, fields …)

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation export data configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation export data untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation export data configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Personal data requested without a purpose |

#### Edge cases to draw

- **Export fails**: Row Failed with the reason and Retry with the same settings. *(source: contracts/satellite/accreditation.yaml#/components/schemas/AccreditationDataExport)*

#### Consistency with other screens

- Match `BO-683`: Exports appear in the operational history with the same columns.
- Match `BO-690`: Exports with personal data appear as audit records.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
history:
- by: Ahmed Al Mansoori
  at: 14 Dec 2026 17:20
  dataset: Holders
  filters: Valid on 15 Dec 2026, Media and Contractor
  fields: 9
  records: 1142
  status: Ready
  personalData: 'No'
- by: Fatima Al Hashimi
  at: 10 Dec 2026 11:02
  dataset: Documents
  filters: Gulf Media Network
  fields: 12
  records: 214
  status: Expired
  personalData: Yes - visa processing
```

#### Permissions

- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationExports` → `ACCREDITATION_MANAGE` (configure) · staff
- `exportAccreditationData` → `ACCREDITATION_MANAGE` (configure) · staff
- `getAccreditationExport` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.55 | Accreditation Export - System shall support export of accreditation data. | Accreditation & Credential Management | CONTRACTED | `exportAccreditationData` |

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-682` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-682`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 16: Works in Accreditation Export & Data Extract Center → Export authorized accreditation data for operational or reporting purposes.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-682?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-683` Delivery, Batch & Operational History

**Provide a consolidated history of notifications, communications, imports and exports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/delivery-batch-operational-history-bo-683` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** One searchable history of the board's operations: communications sent (recipient, type, template, channel, delivery status, failure reason, retries), imports and exports. Used to answer "did the contractor get the collection notice" and to retry failed messages without recreating them. The one thing to get right: three kinds of rows in one timeline with a type filter, and Retry on a failed message resends the original.

**Known correction pending (do not draw the wrong version)**

- **Only listAccreditationAudit is bound** Why: The audit trail records who changed what, not message delivery or retry; the history needs the communication platform's delivery records, an import batch list and listAccreditationExports, plus a retry call. *(source: contracts/satellite/accreditation.yaml#listAccreditationAudit / contracts/satellite/marketing-crm.yaml#listDeliveryQueueFailure / contracts/satellite/accreditation.yaml#listAccreditationExports; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Data table has no label or columns** Why: Generated placeholder; "Operational history". *(source: screens/P08-venue-back-office.yaml#BO-683; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationAudit` ?holderId |
| From | date and time picker | — | — | `listAccreditationAudit` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **filters**: Type (Communication / Import / Export), date range, user, status, recipient or holder search. *(source: screens/P08-venue-back-office.yaml#BO-683)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **History table**: Type icon, When, Subject (recipient and notification type, or batch file, or export dataset), By, Channel or scope, Status, Detail (failure reason, records processed). Communications show retry count and expand to the attempt list. Cursor paging (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-683)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Retry**: For a failed communication, resends the same message to the same recipient; the row shows the new attempt. Only for authorised administrators. *(source: screens/P08-venue-back-office.yaml#BO-683)*
- **Open**: Imports open BO-681 batch detail; exports open BO-682 row; communications open the message preview. *(source: screens/P08-venue-back-office.yaml#BO-683)*

**Data it reads**: `listAccreditationAudit` (onLoad, Import and export audit)

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delivery batch operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delivery batch operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No delivery batch operational yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the delivery batch operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Recipient's address changed since the failure**: Retry goes to the holder's current own address, and the row says so. *(source: contracts/satellite/accreditation.yaml#deliverAccreditationCredential)*

#### Consistency with other screens

- Match `BO-791`: Communication delivery states and retry belong to the communication platform; same status names.
- Match `BO-690`: The audit log is the immutable record; this is an operational view and may summarise.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- type: Communication
  when: 14 Dec 2026 08:00
  subject: Khalid Al Zaabi - Collection instructions
  channel: SMS
  status: Failed
  detail: Number unreachable, 2 retries
- type: Import
  when: 02 Dec 2026 14:05
  subject: GulfMediaNetwork_WinterFestival_crew.xlsx
  by: Maria Santos
  status: Partially completed
  detail: 205 of 214
- type: Export
  when: 14 Dec 2026 17:20
  subject: Holders valid on 15 Dec
  by: Ahmed Al Mansoori
  status: Ready
  detail: 1,142 records
```

#### Permissions

- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-683` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-683`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 18: Works in Delivery, Batch & Operational History → Provide a consolidated history of notifications, communications, imports and exports.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-683?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
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
"exportAccreditationData": {"method":"POST","path":"/accreditation-exports","contract":"accreditation","summary":"Export holders, applications, credentials or access assignments","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationDataExport","responds":null},
"getAccreditationExport": {"method":"GET","path":"/accreditation-exports/{exportId}","contract":"accreditation","summary":"One export, and its download link once ready","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccreditationDataExport"},
"importAccreditationHolders": {"method":"POST","path":"/accreditation-imports","contract":"accreditation","summary":"Load a roster supplied by an organisation","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationImportResult"},
"listAccreditationAudit": {"method":"GET","path":"/accreditation-audit","contract":"accreditation","summary":"The immutable record of who granted what to whom","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"holderId","in":"query","required":null},{"name":"from","in":"query","required":null}],"requestBody":null,"responds":"AccreditationAuditRecord"},
"listAccreditationExports": {"method":"GET","path":"/accreditation-exports","contract":"accreditation","summary":"Exports taken, by whom, of what","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccreditationHolders": {"method":"GET","path":"/accreditation-holders","contract":"accreditation","summary":"Everybody accredited, and what state they are in","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"organisationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"setAccreditationNotificationRules": {"method":"PUT","path":"/accreditation-notifications","contract":"accreditation","summary":"Who is told what, and when","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationNotificationRules","responds":"AccreditationNotificationRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationAuditRecord": {"type":"object","x-ticvai-persistence":"accreditation.audit","description":"Board 8.7. **Who gave this person access to that place, when, and on whose authority.**\n","properties":{"id":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"holderId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"previousRecordHash":{"type":"string","nullable":true},"recordHash":{"type":"string"},"integrity":{"type":"string","readOnly":true,"enum":["intact","broken","unverifiable"]},"scopePath":{"type":"string"}}},
"AccreditationDataExport": {"type":"object","x-ticvai-persistence":"accreditation.data_export","description":"12.1.55. **A spreadsheet of accredited people leaving the platform is an event someone should own.** Requested by `exportAccreditationData`, listed for BO-682, and fetched once `ready`.\n","required":["dataset","format"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dataset":{"type":"string","enum":["holders","applications","credentials","accessAssignments","documents"]},"format":{"type":"string","enum":["csv","xlsx"]},"programmeId":{"type":"string","format":"uuid","nullable":true},"statusFilter":{"type":"string","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"validOn":{"type":"string","format":"date","nullable":true,"description":"Only accreditations valid on this date — the register for one performance"},"fields":{"type":"array","description":"The columns wanted. Omitted means the dataset's standard set","items":{"type":"string"}},"includePersonalData":{"type":"boolean","default":false,"description":"Contact details, date of birth, nationality and document references. Requires REPORT_EXPORT_PII and a purpose; recorded in the accreditation audit trail"},"purpose":{"type":"string","maxLength":500,"nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"requestedAt":{"type":"string","format":"date-time","readOnly":true},"recordCount":{"type":"integer","nullable":true,"readOnly":true},"status":{"type":"string","readOnly":true,"enum":["queued","running","ready","failed","expired"]},"downloadUrl":{"type":"string","nullable":true,"readOnly":true,"description":"Signed and expiring"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationHolder": {"type":"object","x-ticvai-persistence":"accreditation.holder","description":"**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n","required":["id","fullName"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true},"nationality":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true,"description":"12.1.16. The holder's own address — where a mobile credential and renewal notices go"},"phone":{"type":"string","nullable":true,"description":"12.1.16. E.164"},"identityDocumentVerified":{"type":"boolean","default":false},"organisationId":{"type":"string","format":"uuid","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","suspended","revoked","expired","archived"]},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"completenessPercent":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationImportResult": {"type":"object","description":"Board 7.8. **A bulk import is exactly where the same person gets accredited twice.**\n","properties":{"rowsRead":{"type":"integer"},"created":{"type":"integer"},"updated":{"type":"integer"},"rejected":{"type":"integer"},"identityConflicts":{"type":"integer"},"rows":{"type":"array","items":{"type":"object","properties":{"row":{"type":"integer"},"name":{"type":"string"},"outcome":{"type":"string"},"detail":{"type":"string","nullable":true}}}},"committed":{"type":"boolean"}}},
"AccreditationNotificationRules": {"type":"object","x-ticvai-persistence":"accreditation.notification_rules","description":"Board 7.2. **Notices go to the organisation as well as the holder.**","properties":{"programmeId":{"type":"string","format":"uuid"},"rules":{"type":"array","items":{"type":"object","properties":{"event":{"type":"string","enum":["applicationReceived","informationRequested","approved","rejected","credentialReady","expiringSoon","renewalWindowOpen","expired","suspended","revoked"]},"daysBefore":{"type":"integer","nullable":true},"recipients":{"type":"array","items":{"type":"string","enum":["holder","organisation","sponsor","accreditationTeam"]}},"channels":{"type":"array","items":{"type":"string"}},"templateId":{"type":"string","format":"uuid","nullable":true}}}},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
