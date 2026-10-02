# P08-access-venue-01 — P08 · Access & Venue (1 of 3)

**10 screens · 27 operations · 36 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `ACCESS_POINT_CONFIGURE, AI_USE, PARKING_CONFIGURE, QUEUE_MANAGE, QUEUE_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW, WORK_ORDER_VERIFY, WORK_ORDER_VIEW`. A control nobody can use must say so,
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
| `BO-001` | Queue Directory | A | 62 | 72 | 6 | 23 | 1 | 6 | — | notStarted (generated) |
| `BO-002` | Queue Configuration | B–D | 59 | 28 | 6 | 21 | 4 | 6 | — | notStarted (generated) |
| `BO-003` | Queue Integration Setup | B–D | 12 | 23 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-004` | Manual Wait Time Entry | B–D | 6 | 56 | 6 | 6 | 2 | 6 | — | notStarted (generated) |
| `BO-005` | Queue Monitor | A | 55 | 62 | 6 | 34 | 3 | 6 | — | notStarted (generated) |
| `BO-006` | Parking Configuration | A | 11 | 12 | 6 | 3 | 2 | 2 | — | notStarted (generated) |
| `BO-030` | Work Order Verification | B–D | 7 | 44 | 6 | 10 | 0 | 2 | — | notStarted (generated) |
| `BO-031` | Asset Register | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-032` | Admission Profiles | A | 94 | 31 | 6 | 12 | 1 | 0 | — | notStarted (generated) |
| `BO-033` | Blacklist Management | A | 5 | 10 | 6 | 2 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-006, BO-031 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-001` Queue Directory

**See every queue in the venue and whether its data is arriving.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `queue` module |
| Block | Block A · ticket #17954 (APP-SETUP-BO-001) |
| Who uses it | venue staff holding `QUEUE_MANAGE`, `QUEUE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listQueues` reads the population and `getEvent` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `feedId` (deepLink), `queueId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/queue-management/queue-directory` |

**What the spec says about it.** A queue on the manual adaptor shows "manual" rather than "no feed". It is configured and working; treating it as unconfigured makes the health view lie. **Was the declared entry point to the whole back office until 20 August**, which is why 93 screens were unreachable. Now reached from BO-100 through its section.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Event and performance operations were wired from flow F09 (event cancellation); events and performances are the ticketing back office (BO-015), not the ride … Removed 2 October 2026 (CHG-WIR-001): Event and performance operations were wired from flow F09 (event cancellation); events and performances are the ticketing back office (BO-015), not the ride … Removed 2 October 2026 (CHG-WIR-001): Event and performance operations were wired from flow F09 (event cancellation); events and performances are the ticketing back office (BO-015), not the ride …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Every ride queue in the venue with its current wait, where the figure comes from, and whether its data feed is arriving - the duty manager's first check. A queue on manual entry shows "Manual", not "No feed". The one thing to get right: queues whose feed has gone quiet are at the top in a banner.

**Fixed on main** (the package already carries these; draw what it says): Event and performance operations (listEvents, createEvent, updateEvent, listPerformances, createPerformances, getEvent) and an exit … (CHG-WIR-001); "Venue id" text field filter (CHG-SBO-009); Many screens (BO-006, BO-031, BO-032, BO-033, BO-034, BO-035, BO-038) have inferred exits to this screen (CHG-WIR-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Open only | toggle | optional | off | — | — | Sends `?openOnly=` to `listQueues`. | `listQueues` ?openOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |

**Form: Call next parties** (modal, opened by *Call next parties*; *Call next parties* calls `callNextParties`, *Cancel* sends nothing)

**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party count `partyCount` | number field | optional | — | min 1 | — | Defaults to the queue's capacity per cycle. | `callNextParties` body |

**Form: Configure queue feed** (modal, opened by *Configure queue feed*; *Configure queue feed* calls `configureQueueFeed`, *Cancel* sends nothing)

**Collects what `configureQueueFeed` sends before it is called.** Required: `id`, `queueId`, `adaptor`, `isEnabled`. Optional: `adaptorName`, `credentialsRef`, `expectedIntervalSeconds`, `health`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `configureQueueFeed` body |
| Queue `queueId` | picker: choose a queue | required | — | — | shows names, sends the id | — | `configureQueueFeed` body |
| Adaptor `adaptor` | segmented control | required | — | Generic · Mock · Vendor adaptor | — | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and demonstrated with no vendor at all. | `configureQueueFeed` body |
| Adaptor name `adaptorName` | text field | optional | — | — | — | Named vendor where `adaptor` is `vendorAdaptor`. | `configureQueueFeed` body |
| Credentials ref `credentialsRef` | text field | optional | — | — | — | Key vault reference. Credentials are never returned. | `configureQueueFeed` body |
| Expected interval seconds `expectedIntervalSeconds` | number field (seconds) | optional | 60 | — | — | Beyond this without a reading, the feed is considered quiet. | `configureQueueFeed` body |
| Is enabled `isEnabled` | toggle | required | — | — | — | — | `configureQueueFeed` body |

Errors to draw in the form: 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue.

**Form: Create queue** (modal, opened by *Create queue*; *Create queue* calls `createQueue`, *Cancel* sends nothing)

**Collects what `createQueue` sends before it is called.** Required: `code`, `name`, `venueId`, `capacityPerCycle`, `cycleMinutes`. Optional: `attractionProductId`, `assetId`, `accessPointId`, `kind`, `operatingWindows`, `parentQueueId`, `loadBalanceWithQueueIds`, `inQueueOfferEnabled`, `notifyBeforeCallMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm` and 2 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createQueue` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createQueue` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createQueue` body |
| Attraction product `attractionProductId` | picker: choose an attraction product | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. | `createQueue` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Kind `kind` | select | optional | Standby | Standby · Single rider · Fast pass · Virtual · Accessible · Group only · Staff only | — | 5.6.x. A ride has several queues and the model had one. | `createQueue` body |
| Operating windows `operatingWindows` | repeatable rows | optional | — | — | — | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen. | `createQueue` body |
| Day `operatingWindows[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `createQueue` body |
| From `operatingWindows[].from` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue starts running. | `createQueue` body |
| To `operatingWindows[].to` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue stops running. | `createQueue` body |
| Last entry minutes before `operatingWindows[].lastEntryMinutesBefore` | number field (minutes) | optional | 0 | — | — | When the queue stops accepting, which is before it stops running. A guest joining two minutes before close waits twenty and is turned away at the front. | `createQueue` body |
| Parent queue `parentQueueId` | picker: choose a parent queue | optional | — | — | shows names, sends the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that is expressed without either queue … | `createQueue` body |
| Load balance with queues `loadBalanceWithQueueIds` | multi-picker: choose load balance with queues | optional | — | — | — | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. | `createQueue` body |
| In queue offer enabled `inQueueOfferEnabled` | toggle | optional | off | — | — | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. | `createQueue` body |
| Notify before call minutes `notifyBeforeCallMinutes` | number field (minutes) | optional | 5 | — | — | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line is visible. | `createQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | required | — | min 1 | — | — | `createQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | required | — | min 0 | — | — | `createQueue` body |
| Max party size `maxPartySize` | number field | optional | 6 | — | — | — | `createQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | 15 | — | — | How long a called party has to arrive before the entry expires. | `createQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `createQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | 0 | min 0; max 100 | — | Share of each cycle reserved for Fast Pass holders. | `createQueue` body |
| Zone `zone` | text field | optional | — | — | — | — | `createQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass. | `createQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `createQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `createQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `createQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `createQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `createQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `createQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `createQueue` body |

Errors to draw in the form: 400 Validation failed

**Form: Save queue status** (modal, opened by *Save queue status*; *Save queue status* calls `setQueueStatus`, *Cancel* sends nothing)

**Collects what `setQueueStatus` sends before it is called.** Required: `status`, `reason`. Optional: `guestMessage`, `expectedReopenAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Open · Paused · Closed · At capacity | — | — | `setQueueStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `setQueueStatus` body |
| Guest message `guestMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setQueueStatus` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setQueueStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save queue** (modal, opened by *Save queue*; *Save queue* calls `updateQueue`, *Cancel* sends nothing)

**Collects what `updateQueue` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacityPerCycle`, `cycleMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm`, `fastPassAllocationPercent`. Dismissing sends nothing; the screen behind is unchanged.

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

#### Outputs: what the screen shows and produces

**Shown**

**Every queue** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**Every queue feed** (data table, from `listQueueFeeds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Queue | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Adaptor name | text | Named vendor where `adaptor` is `vendorAdaptor`. |
| Credentials ref | text | Key vault reference. Credentials are never returned. |
| Expected interval seconds | 1,234 | Beyond this without a reading, the feed is considered quiet. |
| Is enabled | yes / no (icon or chip) | — |
| Health | grouped details | Whether the feed is currently reporting, computed on read — what `listQueueFeeds` promises per row. |

**Every waiting guest** (data table, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |

**Data table** (data table): Current wait, source, feed health, status

**Banner** (banner): Queues whose feed has gone quiet. The first thing a duty manager checks

**The selected queue** (detail panel, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |
| Capacity per cycle | 1,234 | — |
| Cycle minutes | 1,234.5 | — |
| Max party size | 1,234 | — |
| Return window minutes | 1,234 | How long a called party has to arrive before the entry expires. |

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**The queue feed health** (detail panel, from `getQueueFeedHealth`)

| Shows | Format | Notes |
|---|---|---|
| Feed | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Is healthy | yes / no (icon or chip) | Healthy means the last reading arrived within the feed's expected interval (decided 28 September, audit R106 (1)): `lastReadingAt` is no … |
| Is quiet | yes / no (icon or chip) | No reading within the expected interval. The wait time falls back to throughput-derived and is marked stale rather than freezing at the … |
| Last reading at | 1 Oct 2026, 14:30 | — |
| Expected interval seconds | 1,234 | The feed's `expectedIntervalSeconds` — the interval `isQuiet` is judged against, returned here so a health panel does not need the feed row … |
| Readings last hour | 1,234 | — |
| Discarded last hour | 1,234 | Out-of-order readings rejected in the last hour — rows of `queue.reading` for this feed with `disposition: discardedOutOfOrder`. |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Call next parties (primary button) | `callNextParties` POST `/queues/{queueId}/call-next` | inline | inline | — | opens modal first |
| Configure queue feed (secondary button) | `configureQueueFeed` PUT `/queue-feeds` | QueueFeed | QueueFeed | 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue. | opens modal first |
| Create queue (secondary button) | `createQueue` POST `/queues` | CreateQueueRequest | Queue | 400 Validation failed | opens modal first |
| Save queue status (secondary button) | `setQueueStatus` PUT `/queues/{queueId}/status` | inline | QueueStatusResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save wait time (secondary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Test queue feed (secondary button) | `testQueueFeed` POST `/queue-feeds/{feedId}/test` | — | FeedTestResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save queue (secondary button) | `updateQueue` PATCH `/queues/{queueId}` | inline | Queue | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Quiet-feed banner**: "2 queues have had no reading for over 5 minutes: Falcon Coaster (last 14:02), Wave Rider (last 13:55)" with Open feed. *(source: contracts/satellite/queue.yaml#getQueueFeedHealth / screens/P08-venue-back-office.yaml#BO-001)*
- **Queue list**: Ride, queue kind (Standby, Single rider, Fast Pass, Virtual, Accessible, Group only, Staff only), status, current wait with source, feed health (Healthy, Quiet, Manual, Disabled), now serving, throughput last hour, no-show rate. *(source: contracts/satellite/queue.yaml#listQueues / contracts/satellite/queue.yaml#getQueue / contracts/satellite/queue.yaml#listQueueFeeds)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open configuration / integration / manual wait / monitor**: To BO-002, BO-003, BO-004, BO-005 with the queue selected. *(source: screens/P08-venue-back-office.yaml#BO-001)*
- **Call next parties**: Manual call for queues without a sensor cycle; defaults to the queue's capacity per cycle. *(source: contracts/satellite/queue.yaml#callNextParties)*

**Data it reads**: `listQueues` (onLoad, Every queue with its current wait); `listQueueFeeds` (onLoad, Feed health per queue); `getWaitTimes` (onLoad, Wait times across a venue)

**Where the user goes next**

- → `BO-003` Queue Integration Setup: *Queue Integration Setup*; carries `feedId`
- → `BO-004` Manual Wait Time Entry: *Manual Wait Time Entry*; carries `queueId`
- → `BO-005` Queue Monitor: *Queue Monitor*; carries `queueId`
- → `BO-006` Parking Configuration: *Parking Configuration*
- → `BO-002` Queue Configuration: *Queue Configuration*; carries `queueId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue yet. Offers Create queue (`createQueue`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, openOnly and the queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown adaptor, or credentials missing for the selected adaptor; 400 Validation failed; 409 The feed with this `id` belongs to a different queue. |

#### Edge cases to draw

- **Ride out of service**: The queue shows Closed with the asset status as the reason (taking the ride out of service closes its queue). *(source: contracts/satellite/queue.yaml#createQueue)*

#### Consistency with other screens

- Match `BO-005`: Queue monitor uses the same health and source labels.
- Match `GST-022`: Source labels match what guests see.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queues:
- ride: Falcon Coaster
  kind: Standby
  status: Open
  wait: 60 min (Live)
  feed: Healthy
  serving: 198
  throughput: 580/h
  noShow: 4%
- ride: Falcon Coaster
  kind: Virtual
  status: Open
  wait: 55 min
  feed: Healthy
- ride: Laser Arena
  kind: Standby
  status: Open
  wait: 25 min (Manual)
  feed: Manual
- ride: Wave Rider
  kind: Standby
  status: Paused
  feed: Quiet since 13:55
```

#### Permissions

- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `listQueueFeeds` → `QUEUE_MANAGE` (configure) · staff
- `callNextParties` → `QUEUE_MANAGE` (configure) · staff
- `configureQueueFeed` → `QUEUE_MANAGE` (configure) · staff
- `createQueue` → `QUEUE_MANAGE` (configure) · staff
- `getQueue` → `QUEUE_VIEW` (read) · staff
- `getQueueFeedHealth` → `QUEUE_MANAGE` (configure) · staff
- `getWaitTimes` → no permission · guest, public
- `listQueueEntries` → `QUEUE_VIEW` (read) · staff
- `setQueueStatus` → `QUEUE_MANAGE` (configure) · staff
- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff
- `testQueueFeed` → `QUEUE_MANAGE` (configure) · staff
- `updateQueue` → `QUEUE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

23 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.6.4 | VIP / Priority Handling: Separate or fast-track queues for premium guests. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 5.6.7 | Support priority queueing for VIP guests, annual pass holders, premium packages, loyalty tiers, and accessibility requirements. | F&B & Guest Management | CONTRACTED_PARTIAL | `createQueue` |
| 5.6.12 | Automatically expire queue reservations after configurable grace periods. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.2 | Real-time Queue Dashboard: Staff view of queue lengths, wait times, and customer flow. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 5.6.29 | Maintain complete audit logs for reservations, transfers, modifications, cancellations, and check-ins. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 5.6.24 | Automatically recover queue reservations after operational disruptions. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| 5.6.25 | Support automatic queue suspension and guest reallocation when attractions become unavailable. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| 19.2.38 | Queue Notifications - System shall provide queue notifications. | Guest Mobile App & Branding | CONTRACTED | data `CreateQueueRequest` |
| … 11 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- VQ configuration: rides enabled/disabled per day, queue/express split, target wait time and return-window duration, and handling of early or late arrivals at the ride's entry scanner. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-676)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-001` · status **notStarted** · provenance generated
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (62), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (72 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Call next parties, Configure queue feed, Create queue, Save queue status, Save wait time, Test queue feed, Save queue.
- [ ] Every transition is wired: `BO-003`, `BO-004`, `BO-005`, `BO-006`, `BO-002`.
- [ ] Every gated control is gated: `QUEUE_MANAGE`, `QUEUE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-002` Queue Configuration

**Create a queue and set how it behaves.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `queue` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `QUEUE_MANAGE`, `QUEUE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listQueueEntries` reads the population and `getPerformance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `queueId` (BO-001) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/queue-management/queue-configuration` |

**What the spec says about it.** **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Seat and performance operations (getSeatAvailability, recommendSeats, getPerformance, updatePerformance, cancelPerformance) were carried from a seat-board frame … Removed 2 October 2026 (CHG-WIR-001): Seat and performance operations (getSeatAvailability, recommendSeats, getPerformance, updatePerformance, cancelPerformance) were carried from a seat-board frame … Removed 2 October 2026 (CHG-WIR-001): Seat and performance operations (getSeatAvailability, recommendSeats, getPerformance, updatePerformance, cancelPerformance) were carried from a seat-board frame …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Creates a ride's queues and sets how they behave: the ride (attraction and asset), queue kind, capacity per cycle and cycle length, maximum party, return window, height rule, notice before call, parent queue for shared capacity, load balancing with similar rides, in-queue offers, and the Fast Pass lane (allocation %, products, loyalty tiers, promotions, accessibility priority, per-guest daily cap, redeeming gates). The one thing to get right: the split of a ride's hourly capacity across walk-in, virtual queue and express is visible as one bar.

**Known correction pending (do not draw the wrong version)**

- **Duplicate save buttons (Save, Save queue, Create queue) and a "Status" text filter over waiting guests** Why: One save; the waiting-guest list belongs to the monitor (BO-005). *(source: screens/P08-venue-back-office.yaml#BO-002; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Target wait time and early/late arrival handling (DI-676) have no field in the queue contract** Why: The client asked for them as configuration. *(source: DI-676 / contracts/satellite/queue.yaml#createQueue; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Seat and performance operations (getSeatAvailability, recommendSeats, getPerformance, updatePerformance, cancelPerformance) on queue … (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Name | text field | — | — | — | — | — | — |
| Attraction or resource | select field | — | — | — | — | — | — |
| Capacity per call | number field | — | — | — | — | — | — |
| Guests may join from the app | toggle | — | — | — | — | — | — |
| Redemption window (minutes) | number field | — | — | — | — | How long after being called before the entry expires | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Open only | toggle | off | — | `listQueues` ?openOnly |

**Form: Create queue** (modal, opened by *Create queue*; *Create queue* calls `createQueue`, *Cancel* sends nothing)

**Collects what `createQueue` sends before it is called.** Required: `code`, `name`, `venueId`, `capacityPerCycle`, `cycleMinutes`. Optional: `attractionProductId`, `assetId`, `accessPointId`, `kind`, `operatingWindows`, `parentQueueId`, `loadBalanceWithQueueIds`, `inQueueOfferEnabled`, `notifyBeforeCallMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm` and 2 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createQueue` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createQueue` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createQueue` body |
| Attraction product `attractionProductId` | picker: choose an attraction product | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. | `createQueue` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Kind `kind` | select | optional | Standby | Standby · Single rider · Fast pass · Virtual · Accessible · Group only · Staff only | — | 5.6.x. A ride has several queues and the model had one. | `createQueue` body |
| Operating windows `operatingWindows` | repeatable rows | optional | — | — | — | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen. | `createQueue` body |
| Day `operatingWindows[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `createQueue` body |
| From `operatingWindows[].from` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue starts running. | `createQueue` body |
| To `operatingWindows[].to` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue stops running. | `createQueue` body |
| Last entry minutes before `operatingWindows[].lastEntryMinutesBefore` | number field (minutes) | optional | 0 | — | — | When the queue stops accepting, which is before it stops running. A guest joining two minutes before close waits twenty and is turned away at the front. | `createQueue` body |
| Parent queue `parentQueueId` | picker: choose a parent queue | optional | — | — | shows names, sends the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that is expressed without either queue … | `createQueue` body |
| Load balance with queues `loadBalanceWithQueueIds` | multi-picker: choose load balance with queues | optional | — | — | — | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. | `createQueue` body |
| In queue offer enabled `inQueueOfferEnabled` | toggle | optional | off | — | — | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. | `createQueue` body |
| Notify before call minutes `notifyBeforeCallMinutes` | number field (minutes) | optional | 5 | — | — | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line is visible. | `createQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | required | — | min 1 | — | — | `createQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | required | — | min 0 | — | — | `createQueue` body |
| Max party size `maxPartySize` | number field | optional | 6 | — | — | — | `createQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | 15 | — | — | How long a called party has to arrive before the entry expires. | `createQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `createQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | 0 | min 0; max 100 | — | Share of each cycle reserved for Fast Pass holders. | `createQueue` body |
| Zone `zone` | text field | optional | — | — | — | — | `createQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass. | `createQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `createQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `createQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `createQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `createQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `createQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `createQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `createQueue` body |

Errors to draw in the form: 400 Validation failed

**Form: Save queue** (modal, opened by *Save queue*; *Save queue* calls `updateQueue`, *Cancel* sends nothing)

**Collects what `updateQueue` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacityPerCycle`, `cycleMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm`, `fastPassAllocationPercent`. Dismissing sends nothing; the screen behind is unchanged.

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

**Form: Call next parties** (modal, opened by *Call next parties*; *Call next parties* calls `callNextParties`, *Cancel* sends nothing)

**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party count `partyCount` | number field | optional | — | min 1 | — | Defaults to the queue's capacity per cycle. | `callNextParties` body |

**Form: Save queue status** (modal, opened by *Save queue status*; *Save queue status* calls `setQueueStatus`, *Cancel* sends nothing)

**Collects what `setQueueStatus` sends before it is called.** Required: `status`, `reason`. Optional: `guestMessage`, `expectedReopenAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Open · Paused · Closed · At capacity | — | — | `setQueueStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `setQueueStatus` body |
| Guest message `guestMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setQueueStatus` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setQueueStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ride and kind**: Ride picker (attraction product) with its asset; kind Standby / Single rider / Fast Pass / Virtual / Accessible / Group only / Staff only; queues sharing one ride's capacity set a parent. *(source: contracts/satellite/queue.yaml#createQueue)*
- **Capacity per cycle and cycle minutes**: Shown together with the derived hourly capacity ("40 riders every 4 min = 600/hour"). *(source: contracts/satellite/queue.yaml#createQueue / DI-674)*
- **Lane split**: A stacked bar of walk-in / virtual / express shares of hourly capacity (illustrative 75/25), express share from the Fast Pass allocation %; adjusting one adjusts the rest. *(source: DI-674 / contracts/satellite/queue.yaml#createQueue)*
- **Return window and arrivals**: Return window minutes (default 15); early/late arrival handling at the ride's scanner as a setting. *(source: contracts/satellite/queue.yaml#createQueue / DI-676)*
- **Operating windows**: When the queue runs (not the venue's hours) on a week grid, plus days the ride's virtual queue is off. *(source: contracts/satellite/queue.yaml#createQueue / DI-676)*
- **Fast Pass block**: Products, loyalty tiers and promotions that grant the lane; accessibility priority toggle; Fast Pass return window; max per guest per day; redeeming access points. *(source: contracts/satellite/queue.yaml#/components/schemas/QueueFastPass)*
- **Name**: English and Arabic (localised text), shown to guests. *(source: contracts/satellite/queue.yaml#createQueue)*

#### Outputs: what the screen shows and produces

**Shown**

**Every queue** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create queue (primary button) | `createQueue` POST `/queues` | CreateQueueRequest | Queue | 400 Validation failed | opens modal first |
| Save queue (secondary button) | `updateQueue` PATCH `/queues/{queueId}` | inline | Queue | — | opens modal first |
| Call next parties (secondary button) | `callNextParties` POST `/queues/{queueId}/call-next` | inline | inline | — | opens modal first |
| Save queue status (secondary button) | `setQueueStatus` PUT `/queues/{queueId}/status` | inline | QueueStatusResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save wait time (secondary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Queue status controls**: Open / Pause (keeps places, stops joins) / Close (releases everyone and notifies) with a required reason and guest message; closing without notifying is not offered. *(source: contracts/satellite/queue.yaml#setQueueStatus)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save queue**: Create, or amend (a name edit replaces the whole localised map; the Fast Pass block is replaced as a whole). *(source: contracts/satellite/queue.yaml#updateQueue)*

**Data it reads**: `getQueue` (onLoad, Read a queue with live position); `getWaitTimes` (onLoad, Wait times across a venue); `listQueues` (onLoad, List queues)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `feedId`, `queueId`
- → `BO-003` Queue Integration Setup: *Queue Integration Setup*; carries `feedId`
- → `BO-004` Manual Wait Time Entry: *Manual Wait Time Entry*; carries `queueId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue yet. Offers Create queue (`createQueue`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and the queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `getQueue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Kiosk-only virtual queue at a water park**: A setting "Guests may join from the app" off still allows wristband joins at the ride kiosk. *(source: DI-677)*
- **VQ guests merged with VIP**: Never; virtual and express lanes are separate queues at the ride. *(source: DI-678)*

#### Consistency with other screens

- Match `BO-001`: Same kind names and statuses.
- Match `BO-231`: Lane and queue rules on the access board (BO-221, BO-231) must not contradict these lanes.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
  ride: Falcon Coaster
  kinds: Standby, Virtual, Fast Pass
  cycle: 40 riders / 4 min (600/h)
  split: Walk-in 337, Virtual 113, Express 150 per hour
  returnWindow: 15 min
  height: 120 cm
  maxParty: 6
```

#### Permissions

- `createQueue` → `QUEUE_MANAGE` (configure) · staff
- `updateQueue` → `QUEUE_MANAGE` (configure) · staff
- `callNextParties` → `QUEUE_MANAGE` (configure) · staff
- `getQueue` → `QUEUE_VIEW` (read) · staff
- `getWaitTimes` → no permission · guest, public
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `setQueueStatus` → `QUEUE_MANAGE` (configure) · staff
- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `getQueue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

21 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.6.4 | VIP / Priority Handling: Separate or fast-track queues for premium guests. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 5.6.7 | Support priority queueing for VIP guests, annual pass holders, premium packages, loyalty tiers, and accessibility requirements. | F&B & Guest Management | CONTRACTED_PARTIAL | `createQueue` |
| 5.6.12 | Automatically expire queue reservations after configurable grace periods. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.24 | Automatically recover queue reservations after operational disruptions. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| 5.6.25 | Support automatic queue suspension and guest reallocation when attractions become unavailable. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| 19.2.38 | Queue Notifications - System shall provide queue notifications. | Guest Mobile App & Branding | CONTRACTED | data `CreateQueueRequest` |
| 5.6.1 | Multiple Queue Types: First-come-first-serve, priority/VIP, group queues. | F&B & Guest Management | CONTRACTED | data `CreateQueueRequest` |
| 5.6.5 | Load Balancing: Redirect customers to less busy queues/rides/entry points. | F&B & Guest Management | CONTRACTED | data `CreateQueueRequest` |
| … 9 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: walk-in, virtual-queue and VIP guests must be distinguished at the ride; VQ guests are never merged into the VIP line (would erode paid value); VQ arrivals need their own handling, e.g. a separate line or a QR scan within the arrival window. *(agreed · MoM 7 Sep 2026, 4.15 Virtual Queue - Three-Tier Guest Model · DI-678)*
- Allam: water-park guests rarely carry phones, so a kiosk at the ride lets a guest scan their wristband to book a queue slot and get a return time, then scan the wristband again to enter. *(agreed · MoM 7 Sep 2026, 4.14 Virtual Queue - Multi-Venue Applicability · DI-677)*
- VQ configuration: rides enabled/disabled per day, queue/express split, target wait time and return-window duration, and handling of early or late arrivals at the ride's entry scanner. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-676)*
- Per-ride hourly capacity (e.g. 600/hour) split across express/fast-lane, virtual queue and walk-in (illustrative 75% general split walk-in/VQ, 25%/150 express); allocation adjusts dynamically if one lane is disproportionately busy. *(client request · MoM 7 Sep 2026, 4.12 Virtual Queue - Concept & Lane/Allocation Model · DI-674)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-002` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 2.dc.html`
- Client design-board frames: `Seat Board 2.dc.html#seat-2c`

#### Acceptance for the design

- [ ] Every input above is drawn (59), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create queue, Save queue, Call next parties, Save queue status, Save wait time, Save.
- [ ] Every transition is wired: `BO-001`, `BO-003`, `BO-004`.
- [ ] Every gated control is gated: `QUEUE_MANAGE`, `QUEUE_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-003` Queue Integration Setup

**Connect a queue to an on-site system, or leave it on manual entry.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `queue` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `QUEUE_MANAGE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listQueueFeeds` reads the population and `getQueueFeedHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `feedId` (BO-001), `orderId` (deepLink), `venueId` (session) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/queue-management/queue-integration-setup` |

**What the spec says about it.** ADR-0012, adaptor-first. A named vendor is a driver behind a stable inbound shape, so adding one is configuration plus a driver rather than a core change. Vendor selection is CF-33a and deliberately late. **createRefund removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Corrected 24 August**: removed applyManualDiscount, createOrder, exchangeOrderLines, getOrder, getOrderStatement, getRefundPolicy and 11 more. **A queue integration screen carried 15 order operations** — create an order, apply a discount, exchange lines, hold, refund — and four queue ones. Bulk-attach residue, and `requiresModule` was `ticketing` to match the operations rather than the screen. **Found by deriving the empty states.** `emptyNoAccess` came out reading *"needs `ORDER_CREATE` to create orders"* on a screen called Queue Integration Setup — **a generated sentence that was accurate to the data and absurd about the screen**, which is exactly what made it visible.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Connects a ride queue to the venue's people-counting system or leaves it on manual: adaptor (Generic inbound API, Mock, or a named vendor adaptor), endpoint, credential reference, expected reading interval, a test that shows the five checks and the mapped sample, and Enabled only after a passing test. TICVAI ships no vendor adaptors. The one thing to get right: a reachable source whose payload nobody mapped must show as a failure, not as silence.

**Known correction pending (do not draw the wrong version)**

- **Two primary buttons (Configure queue feed and Save) and an unlabelled detail panel** Why: One Save; the panel is the test result. *(source: screens/P08-venue-back-office.yaml#BO-003; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Body requires id** Why: A new feed has no id (VO-R03). *(source: contracts/satellite/queue.yaml#configureQueueFeed; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which people-counting technology will venues use (entry sensors, manual counts, CCTV)?** → Drawn default accepted: Generic adaptor and manual entry; vendor adaptor greyed. *(decided by Chinmay, 2026-10-02; DEC-371 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Adaptor | segmented control | optional | — | Generic · Mock · Vendor adaptor | — | **Follows the contract's `QueueFeedAdaptor`** — generic (the inbound API that sensor APIs, webhooks, MQTT, turnstile counts and cameras all post to), mock, or vendorAdaptor (with `adaptorName`) … | `QueueFeed.adaptor` |
| Endpoint or topic | text field | — | — | — | — | Shown for generic and vendorAdaptor feeds | — |
| Credential reference | text field | — | — | — | — | A key vault reference, never the secret. A secret typed into a form ends up in a screenshot | — |
| Expected interval (seconds) | number field | — | — | — | — | Drives the went-quiet alarm. Too tight and a duty manager learns to ignore it | — |
| Enabled | toggle | — | — | — | — | Disabled by default. A feed goes live only after a passing test | — |

**Form: Configure queue feed** (modal, opened by *Configure queue feed*; *Configure queue feed* calls `configureQueueFeed`, *Cancel* sends nothing)

**Collects what `configureQueueFeed` sends before it is called.** Required: `id`, `queueId`, `adaptor`, `isEnabled`. Optional: `adaptorName`, `credentialsRef`, `expectedIntervalSeconds`, `health`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `configureQueueFeed` body |
| Queue `queueId` | picker: choose a queue | required | — | — | shows names, sends the id | — | `configureQueueFeed` body |
| Adaptor `adaptor` | segmented control | required | — | Generic · Mock · Vendor adaptor | — | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and demonstrated with no vendor at all. | `configureQueueFeed` body |
| Adaptor name `adaptorName` | text field | optional | — | — | — | Named vendor where `adaptor` is `vendorAdaptor`. | `configureQueueFeed` body |
| Credentials ref `credentialsRef` | text field | optional | — | — | — | Key vault reference. Credentials are never returned. | `configureQueueFeed` body |
| Expected interval seconds `expectedIntervalSeconds` | number field (seconds) | optional | 60 | — | — | Beyond this without a reading, the feed is considered quiet. | `configureQueueFeed` body |
| Is enabled `isEnabled` | toggle | required | — | — | — | — | `configureQueueFeed` body |

Errors to draw in the form: 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **adaptor**: Generic (any sensor API, webhook, MQTT, turnstile counts, cameras post to it) / Mock (demo) / Vendor adaptor (named); vendor name only for the last. *(source: contracts/satellite/queue.yaml#configureQueueFeed / ADR-0012)*
- **credentialsRef**: Key-vault reference picker; never a secret typed into the form; never displayed back. *(source: contracts/satellite/queue.yaml#configureQueueFeed)*
- **expectedIntervalSeconds**: Default 60; hint that too tight a value trains managers to ignore the quiet alarm. *(source: contracts/satellite/queue.yaml#configureQueueFeed / screens/P08-venue-back-office.yaml#BO-003)*
- **isEnabled**: Off by default; can only be switched on after a passing test. *(source: screens/P08-venue-back-office.yaml#BO-003)*

#### Outputs: what the screen shows and produces

**Shown**

**Every queue feed** (data table, from `listQueueFeeds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Queue | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Adaptor name | text | Named vendor where `adaptor` is `vendorAdaptor`. |
| Credentials ref | text | Key vault reference. Credentials are never returned. |
| Expected interval seconds | 1,234 | Beyond this without a reading, the feed is considered quiet. |
| Is enabled | yes / no (icon or chip) | — |

**Detail panel** (detail panel): Five checks, plus the mapped sample reading and the raw payload. A source that is reachable and returns a shape nobody mapped looks like silence, not an error

**The selected queue feed** (detail panel, from `listQueueFeeds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Queue | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Adaptor name | text | Named vendor where `adaptor` is `vendorAdaptor`. |
| Credentials ref | text | Key vault reference. Credentials are never returned. |
| Expected interval seconds | 1,234 | Beyond this without a reading, the feed is considered quiet. |
| Is enabled | yes / no (icon or chip) | — |
| Health | grouped details | Whether the feed is currently reporting, computed on read — what `listQueueFeeds` promises per row. |

**The queue feed health** (detail panel, from `getQueueFeedHealth`)

| Shows | Format | Notes |
|---|---|---|
| Feed | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Is healthy | yes / no (icon or chip) | Healthy means the last reading arrived within the feed's expected interval (decided 28 September, audit R106 (1)): `lastReadingAt` is no … |
| Is quiet | yes / no (icon or chip) | No reading within the expected interval. The wait time falls back to throughput-derived and is marked stale rather than freezing at the … |
| Last reading at | 1 Oct 2026, 14:30 | — |
| Expected interval seconds | 1,234 | The feed's `expectedIntervalSeconds` — the interval `isQuiet` is judged against, returned here so a health panel does not need the feed row … |
| Readings last hour | 1,234 | — |
| Discarded last hour | 1,234 | Out-of-order readings rejected in the last hour — rows of `queue.reading` for this feed with `disposition: discardedOutOfOrder`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Test connection (secondary button) | navigation or local | — | — | — | — |
| Configure queue feed (primary button) | `configureQueueFeed` PUT `/queue-feeds` | QueueFeed | QueueFeed | 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue. | opens modal first |
| Test queue feed (secondary button) | `testQueueFeed` POST `/queue-feeds/{feedId}/test` | — | FeedTestResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Test result**: Reachable, Authenticated, Payload parsed, Reading mapped, Within interval - each pass/fail - plus the mapped sample reading and the raw payload. *(source: contracts/satellite/queue.yaml#testQueueFeed / screens/P08-venue-back-office.yaml#BO-003)*
- **Health**: Healthy / Quiet with last reading time, readings and discarded readings in the last hour. *(source: contracts/satellite/queue.yaml#getQueueFeedHealth)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save feed**: Whole-feed upsert (VO-R04). *(source: contracts/satellite/queue.yaml#configureQueueFeed)*

**Data it reads**: `getQueueFeedHealth` (onLoad, Current feed state); `listQueueFeeds` (onLoad, List configured sensor feeds)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `feedId`, `queueId`
- → `BO-002` Queue Configuration: *Queue Configuration*; carries `queueId`
- → `BO-004` Manual Wait Time Entry: *Manual Wait Time Entry*; carries `queueId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue integration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue integration yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listQueueFeeds` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_MANAGE`, which `getQueueFeedHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue. |

#### Edge cases to draw

- **Feed goes quiet**: Wait time falls back to throughput estimate and is labelled so; the queue shows in BO-001's banner. *(source: contracts/satellite/queue.yaml#getQueueFeedHealth)*

#### Consistency with other screens

- Match `BO-004`: Manual entry remains available whatever the feed state.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
feed:
  queue: Falcon Coaster Standby
  adaptor: Generic
  endpoint: https://ingest.ticvai.ae/q/falcon
  credential: kv://yas/falcon-feed
  interval: 60 s
  test: 5 of 5 passed
  lastReading: 14:02:31 - 212 guests in line
```

#### Permissions

- `configureQueueFeed` → `QUEUE_MANAGE` (configure) · staff
- `testQueueFeed` → `QUEUE_MANAGE` (configure) · staff
- `getQueueFeedHealth` → `QUEUE_MANAGE` (configure) · staff
- `listQueueFeeds` → `QUEUE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `QUEUE_MANAGE`, which `getQueueFeedHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ride wait times come from the venue's sensor/camera counts via a live API (or a people count converted at a per-person rate) and are shown in the guest app; an AI "which ride to visit next" recommendation may follow. *(agreed · MoM 14 Aug 2026, 9. Queue Management · DI-299)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-003` · status **notStarted** · provenance generated
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Test connection, Configure queue feed, Test queue feed, Save.
- [ ] Every transition is wired: `BO-001`, `BO-002`, `BO-004`.
- [ ] Every gated control is gated: `QUEUE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-004` Manual Wait Time Entry

**Set a wait time by hand, whether or not a feed exists.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `queue` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `QUEUE_MANAGE`, `QUEUE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `approveRefund` decides items that `listQueues` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `queueId` (BO-001) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/queue-management/manual-wait-time-entry` |

**What the spec says about it.** The screen the client asked for on 14 August. Available regardless of integration state — a venue with no sensors runs entirely from here, and a venue whose sensor failed falls back to it.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Refund operations (createBulkRefund, approveRefund) and queue create/update/status were carried from flow F09 and BO-001; this screen sets waits (F09 step 4 … Removed 2 October 2026 (CHG-WIR-001): Refund operations (createBulkRefund, approveRefund) and queue create/update/status were carried from flow F09 and BO-001; this screen sets waits (F09 step 4 … Removed 2 October 2026 (CHG-WIR-001): Refund operations (createBulkRefund, approveRefund) and queue create/update/status were carried from flow F09 and BO-001; this screen sets waits (F09 step 4 …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The screen the client asked for on 14 August: set a ride's wait time by hand, whether or not a feed exists. A venue with no sensors runs entirely from here; a failed sensor falls back to it. A manual figure expires after a stated time and the queue reverts. The one thing to get right: one row per ride with a stepper and the current value and source, fast enough to update ten rides in a minute.

**Known correction pending (do not draw the wrong version)**

- **Table labelled "Waiting for a decision" over queues, a "Publish" primary button and a waiting-guest table** Why: Generated labels; there is nothing to publish, each row saves on its own. *(source: screens/P08-venue-back-office.yaml#BO-004; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Refund operations (createBulkRefund, approveRefund) and queue create/update/status on the manual wait screen (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listQueues`. | `listQueues` ?venueId |
| Open only | toggle | optional | off | — | — | Sends `?openOnly=` to `listQueues`. | `listQueues` ?openOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Status | select | — | Waiting · Called · Redeemed · Expired · No show · Cancelled · Released | `listQueueEntries` ?status |

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Call next parties** (modal, opened by *Call next parties*; *Call next parties* calls `callNextParties`, *Cancel* sends nothing)

**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party count `partyCount` | number field | optional | — | min 1 | — | Defaults to the queue's capacity per cycle. | `callNextParties` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **waitMinutes**: Stepper in 5-minute steps (typing allowed), 0 or more. *(source: contracts/satellite/queue.yaml#setWaitTime)*
- **expiresInMinutes**: "Valid for" chips 15 / 30 (default) / 60 / custom; after it, the queue reverts to sensor, throughput or Unavailable. *(source: contracts/satellite/queue.yaml#setWaitTime)*
- **note**: Optional, max 200 (e.g. "Counted at queue entrance"). *(source: contracts/satellite/queue.yaml#setWaitTime)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**Every waiting guest** (data table, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |

**Card list** (card list): One row per queue with a stepper and the current value

**Banner** (banner): Where a feed is live, a manual entry overrides it for a stated period and then reverts. A permanent silent override is how a broken sensor goes unnoticed for a season

**The selected queue** (detail panel, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |
| Capacity per cycle | 1,234 | — |
| Cycle minutes | 1,234.5 | — |
| Max party size | 1,234 | — |
| Return window minutes | 1,234 | How long a called party has to arrive before the entry expires. |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save wait time (primary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Call next parties (secondary button) | `callNextParties` POST `/queues/{queueId}/call-next` | inline | inline | — | opens modal first |
| Publish (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ride rows**: Ride, current wait with source and age, feed state; where a feed is live, a banner says the manual value overrides it until <time> and then reverts. *(source: screens/P08-venue-back-office.yaml#BO-004 / contracts/satellite/queue.yaml#getWaitTimes)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save wait time**: Per row; guests see it labelled "Set by staff". *(source: contracts/satellite/queue.yaml#setWaitTime / contracts/satellite/queue.yaml#getWaitTimes)*

**Data it reads**: `listQueues` (onLoad, Current values); `getQueue` (onLoad, Read a queue with live position); `getWaitTimes` (onLoad, Wait times across a venue); `listQueueEntries` (onLoad, List entries in a queue)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `feedId`, `queueId`
- → `BO-002` Queue Configuration: *Queue Configuration*; carries `queueId`
- → `BO-003` Queue Integration Setup: *Queue Integration Setup*; carries `feedId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The manual wait time list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the manual wait time untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, openOnly and the manual wait time are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Saving offline (from a handheld)**: Offline-capable; queued and applied on reconnect with the device time. *(source: contracts/satellite/queue.yaml#setWaitTime)*

#### Consistency with other screens

- Match `EMP-032`: The Staff App manual wait entry is the same action on a phone.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- ride: Laser Arena
  wait: 25
  source: Manual
  validUntil: '14:45'
  by: Maria Santos
- ride: Falcon Coaster
  wait: 60
  source: Live sensor
- ride: Bumper Cars
  wait: 15
  source: Estimated
```

#### Permissions

- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `callNextParties` → `QUEUE_MANAGE` (configure) · staff
- `getQueue` → `QUEUE_VIEW` (read) · staff
- `getWaitTimes` → no permission · guest, public
- `listQueueEntries` → `QUEUE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.2 | Real-time Queue Dashboard: Staff view of queue lengths, wait times, and customer flow. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 5.6.29 | Maintain complete audit logs for reservations, transfers, modifications, cancellations, and check-ins. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: how per-ride occupancy is counted (entry sensors, manual security counts, CCTV/computer vision); Allam to check with Warner Bros. World, which has a visible wait-time display. Manual count entry stays a possible source. *(open · MoM 7 Sep 2026, 4.16 Wait-Time Calculation & People-Counting Technology · DI-680)*
- The client asked for a manual wait-time entry screen: set a wait time by hand whether or not a sensor feed exists; a venue with no sensors runs entirely from it and a failed sensor falls back to it. *(client request · MoM 14 Aug 2026, (cited in BO-004 notes) · DI-315)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-004` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (56 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save wait time, Call next parties, Publish.
- [ ] Every transition is wired: `BO-001`, `BO-002`, `BO-003`.
- [ ] Every gated control is gated: `QUEUE_MANAGE`, `QUEUE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-005` Queue Monitor

**Watch queues during operation and call parties forward.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `marketing` module |
| Block | Block A · ticket #20777 (APP-SETUP-BO-005) |
| Who uses it | venue staff holding `AI_USE`, `QUEUE_MANAGE`, `QUEUE_VIEW`, `REPORT_VIEW_VENUE` (2 operate, 1 configure, 1 read); in the flows as guest |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listQueueEntries` reads the population and `getWaitTimes` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `queueId` (BO-001) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/queue-management/queue-monitor` |

**What the spec says about it.** Pulled to Wave 1 on 17 August (CF-101): F09 closes a cancelled event’s queue, and a Wave 1 flow cannot step through a Wave 2 screen. **Cross-platform navigation removed 24 August**: EMP-032. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): A queue monitor does not run marketing campaigns; the queue's guest notifications come from setQueueStatus and callNextParties and are transactional. The second … Removed 2 October 2026 (CHG-WIR-001): A queue monitor does not run marketing campaigns; the queue's guest notifications come from setQueueStatus and callNextParties and are transactional. The second … Removed 2 October 2026 (CHG-WIR-001): A queue monitor does not run marketing campaigns; the queue's guest notifications come from setQueueStatus and callNextParties and are transactional. The second …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The supervisor watches queues during operation and calls parties forward. From this process's angle, the guest messages a queue sends (called, paused, closed) are operational and transactional, not marketing. Closing a queue always notifies every waiting guest, and that is not a campaign. The screen's campaign controls do not belong here.

**Fixed on main** (the package already carries these; draw what it says): BO-005 declares nine campaign operations (createCampaign, launchCampaign, pauseCampaign, stopCampaign, testSendCampaign … (CHG-WIR-001); Two primary buttons, "Call next parties" (callNextParties) and "Call next" (no operation). (CHG-SBO-013).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Waiting · Called · Redeemed · Expired · No show · Cancelled · Released | — | Sends `?status=` to `listQueueEntries`. | `listQueueEntries` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |
| Open only | toggle | off | — | `listQueues` ?openOnly |

**Form: Call next parties** (modal, opened by *Call next parties*; *Call next parties* calls `callNextParties`, *Cancel* sends nothing)

**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party count `partyCount` | number field | optional | — | min 1 | — | Defaults to the queue's capacity per cycle. | `callNextParties` body |

**Form: Create queue** (modal, opened by *Create queue*; *Create queue* calls `createQueue`, *Cancel* sends nothing)

**Collects what `createQueue` sends before it is called.** Required: `code`, `name`, `venueId`, `capacityPerCycle`, `cycleMinutes`. Optional: `attractionProductId`, `assetId`, `accessPointId`, `kind`, `operatingWindows`, `parentQueueId`, `loadBalanceWithQueueIds`, `inQueueOfferEnabled`, `notifyBeforeCallMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm` and 2 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createQueue` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createQueue` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createQueue` body |
| Attraction product `attractionProductId` | picker: choose an attraction product | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. | `createQueue` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Kind `kind` | select | optional | Standby | Standby · Single rider · Fast pass · Virtual · Accessible · Group only · Staff only | — | 5.6.x. A ride has several queues and the model had one. | `createQueue` body |
| Operating windows `operatingWindows` | repeatable rows | optional | — | — | — | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen. | `createQueue` body |
| Day `operatingWindows[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `createQueue` body |
| From `operatingWindows[].from` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue starts running. | `createQueue` body |
| To `operatingWindows[].to` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue stops running. | `createQueue` body |
| Last entry minutes before `operatingWindows[].lastEntryMinutesBefore` | number field (minutes) | optional | 0 | — | — | When the queue stops accepting, which is before it stops running. A guest joining two minutes before close waits twenty and is turned away at the front. | `createQueue` body |
| Parent queue `parentQueueId` | picker: choose a parent queue | optional | — | — | shows names, sends the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that is expressed without either queue … | `createQueue` body |
| Load balance with queues `loadBalanceWithQueueIds` | multi-picker: choose load balance with queues | optional | — | — | — | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. | `createQueue` body |
| In queue offer enabled `inQueueOfferEnabled` | toggle | optional | off | — | — | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. | `createQueue` body |
| Notify before call minutes `notifyBeforeCallMinutes` | number field (minutes) | optional | 5 | — | — | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line is visible. | `createQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | required | — | min 1 | — | — | `createQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | required | — | min 0 | — | — | `createQueue` body |
| Max party size `maxPartySize` | number field | optional | 6 | — | — | — | `createQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | 15 | — | — | How long a called party has to arrive before the entry expires. | `createQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `createQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | 0 | min 0; max 100 | — | Share of each cycle reserved for Fast Pass holders. | `createQueue` body |
| Zone `zone` | text field | optional | — | — | — | — | `createQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass. | `createQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `createQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `createQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `createQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `createQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `createQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `createQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `createQueue` body |

Errors to draw in the form: 400 Validation failed

**Form: Save queue status** (modal, opened by *Save queue status*; *Save queue status* calls `setQueueStatus`, *Cancel* sends nothing)

**Collects what `setQueueStatus` sends before it is called.** Required: `status`, `reason`. Optional: `guestMessage`, `expectedReopenAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Open · Paused · Closed · At capacity | — | — | `setQueueStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `setQueueStatus` body |
| Guest message `guestMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setQueueStatus` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setQueueStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save queue** (modal, opened by *Save queue*; *Save queue* calls `updateQueue`, *Cancel* sends nothing)

**Collects what `updateQueue` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacityPerCycle`, `cycleMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm`, `fastPassAllocationPercent`. Dismissing sends nothing; the screen behind is unchanged.

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

#### Outputs: what the screen shows and produces

**Shown**

**Every waiting guest** (data table, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |

**Every queue** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**Metric tile** (metric tile): Waiting, called, expired, average wait

**Takings and admissions today** (metric tile, from `getKpiValues`): **Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Period | text | — |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Chart** (chart): Wait over the day. Stale where the feed has gone quiet

**The selected waiting guest** (detail panel, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |
| Called at | 1 Oct 2026, 14:30 | — |
| Return window ends at | 1 Oct 2026, 14:30 | — |
| Redeemed at | 1 Oct 2026, 14:30 | — |
| Admitted count | 1,234 | — |

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Call next parties (primary button) | `callNextParties` POST `/queues/{queueId}/call-next` | inline | inline | — | opens modal first |
| Create queue (secondary button) | `createQueue` POST `/queues` | CreateQueueRequest | Queue | 400 Validation failed | opens modal first |
| Save queue status (secondary button) | `setQueueStatus` PUT `/queues/{queueId}/status` | inline | QueueStatusResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save wait time (secondary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save queue (secondary button) | `updateQueue` PATCH `/queues/{queueId}` | inline | Queue | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Notified guests after a close or pause**: Show how many waiting guests were released and notified, with the message they received, from the queue status result. *(source: contracts/satellite/queue.yaml#setQueueStatus; F09 step 5)*
- **Called parties**: After Call next, show which parties were called and how many remain; each called party is notified in their app (and signage where configured). *(source: contracts/satellite/queue.yaml#callNextParties)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Close queue**: Requires a reason and offers a guest message in English and Arabic (prefilled). Closing without notifying is not offered. The guests receive it as an operational notification, with no consent check. *(source: contracts/satellite/queue.yaml#setQueueStatus; DI-019)*

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `listQueueEntries` (onInterval, Who is waiting); `getWaitTimes` (onInterval, Current waits); `getQueue` (onLoad, Read a queue with live position); `listQueues` (onLoad, List queues)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `feedId`, `queueId`
- → `BO-002` Queue Configuration: *Queue Configuration*; carries `queueId`
- → `BO-003` Queue Integration Setup: *Queue Integration Setup*; carries `feedId`
- → `EMP-032` Manual wait entry: *The feed dies and a supervisor types the wait*; carries `queueId`; calls `listQueues`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue yet. Offers Create queue (`createQueue`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and the queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `listQueueEntries` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Consistency with other screens

- Match `GST-030`: The call and closure messages arrive in the guest's notification feed with kind Queue.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue: Tornado Slide - standby - 38 waiting - average wait 42 min (sensor)
closeMessage: Tornado Slide is closed for the rest of today. Your place has been released - try the Lazy River,
  wait 10 min.
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `listQueueEntries` → `QUEUE_VIEW` (read) · staff
- `callNextParties` → `QUEUE_MANAGE` (configure) · staff
- `getWaitTimes` → no permission · guest, public
- `createQueue` → `QUEUE_MANAGE` (configure) · staff
- `getQueue` → `QUEUE_VIEW` (read) · staff
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `setQueueStatus` → `QUEUE_MANAGE` (configure) · staff
- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff
- `updateQueue` → `QUEUE_MANAGE` (configure) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `listQueueEntries` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

34 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.6.2 | Real-time Queue Dashboard: Staff view of queue lengths, wait times, and customer flow. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 5.6.29 | Maintain complete audit logs for reservations, transfers, modifications, cancellations, and check-ins. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.4 | VIP / Priority Handling: Separate or fast-track queues for premium guests. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 5.6.7 | Support priority queueing for VIP guests, annual pass holders, premium packages, loyalty tiers, and accessibility requirements. | F&B & Guest Management | CONTRACTED_PARTIAL | `createQueue` |
| 5.6.12 | Automatically expire queue reservations after configurable grace periods. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 5.6.24 | Automatically recover queue reservations after operational disruptions. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| 5.6.25 | Support automatic queue suspension and guest reallocation when attractions become unavailable. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| … 22 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*
- Ops view shows current wait per ride with general and virtual-queue waits separately, and alerts for e.g. a growing express queue or unusually long overall queue. *(client request · MoM 7 Sep 2026, 4.17 Virtual Queue - Operations Dashboard & AI Guest Flow Optimization · DI-681)*
- **Open question.** Open: how per-ride occupancy is counted (entry sensors, manual security counts, CCTV/computer vision); Allam to check with Warner Bros. World, which has a visible wait-time display. Manual count entry stays a possible source. *(open · MoM 7 Sep 2026, 4.16 Wait-Time Calculation & People-Counting Technology · DI-680)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-005` · status **notStarted** · provenance generated
- Flow F21 *A ride queue fills and a guest is redirected*, step 3: A supervisor sees the queue building → Before guests complain
- Flow F21 *A ride queue fills and a guest is redirected*, step 5: Parties are called → From the virtual queue
- Flow F21 branch at step 3 (requiresStaff): when The asset goes out of service, **The queue closes and waiting parties are released, not silently dropped.** A guest holding a place for a closed ride will come back to ask.
- Flow F21 branch at step 5 (recoverable): when A called party does not arrive, Held for a window then skipped. Their place is not restored — **unlike a waitlist, where being asleep is not declining**, a called queue place expires because the ride is running.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (55), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (62 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Call next parties, Create queue, Save queue status, Save wait time, Save queue.
- [ ] Every transition is wired: `BO-001`, `BO-002`, `BO-003`, `EMP-032`.
- [ ] Every gated control is gated: `AI_USE`, `QUEUE_MANAGE`, `QUEUE_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-006` Parking Configuration

**Set up each car park and how it integrates with the venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 2 · needs the `access` module |
| Block | Block A · ticket #18145 (APP-SETUP-BO-006) |
| Who uses it | venue staff holding `PARKING_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAccessPoints` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/parking/parking-configuration` |

**What the spec says about it.** Placeholder. Parking was discussed on 14 August and the MoM has not yet been received. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Parking configuration needs only the facility read and write; editing access points belongs to BO-064, and the venue comes from the session (ADR-0030 … Removed 2 October 2026 (CHG-WIR-001): Parking configuration needs only the facility read and write; editing access points belongs to BO-064, and the venue comes from the session (ADR-0030 … Open: Answered by the 14 August MoM section 10, which this question was waiting for. Parking is barrier integration, in three models, and it is not space counting. (1) No integration - TICVAI issues its …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** One screen per car park choosing how parking works at the barrier: no integration (security checks the TICVAI QR by eye), plate whitelist (the guest gives a plate at checkout and TICVAI pushes it to the parking system's ANPR whitelist) or QR handoff (the barrier validates the TICVAI code). It is barrier integration, not space counting and not pay-per-hour. The one thing to get right: the mode drives which other fields appear, and the guest checkout changes with it.

**Fixed on main** (the package already carries these; draw what it says): Screen binds listAccessPoints, updateAccessPoint and a "Venue id" text field, with a detail panel marked TODO (CHG-WIR-001); Navigation exit to BO-001 Queue Directory (inferred) and the "Placeholder" note (CHG-WIR-002).

#### Inputs: what the user enters or picks

**Form: Save parking facility** (modal, opened by *Save parking facility*; *Save parking facility* calls `setParkingFacility`, *Cancel* sends nothing)

**Collects what `setParkingFacility` sends before it is called.** Required: `name`, `venueId`, `mode`. Optional: `id`, `capacity`, `takesPayment`, `vendorSwapTargetDays`, `vendorName`, `endpoint`, `credentialRef`, `pushLeadMinutes`, `accessPointIds`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | Server-assigned, and the upsert key of `setParkingFacility`. Absent in a body, it creates; present, it names the facility being replaced. | `setParkingFacility` body |
| Name `name` | text field | required | — | — | — | — | `setParkingFacility` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setParkingFacility` body |
| Mode `mode` | segmented control | required | — | None · Plate whitelist · QR handoff | — | CF-52, settled 14 August. Not variations of one thing — each decides what happens at sale and what a guest presents at the barrier. | `setParkingFacility` body |
| Capacity `capacity` | number field | optional | — | There is no live space count from the car park; a guest sees *full* only when capacity is reached, never an availability figure. | — | What "full" means in the first release (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid for a time reach this number. | `setParkingFacility` body |
| Vendor name `vendorName` | text field | optional | — | — | — | Staff only — omitted from a guest's `listParkingFacilities` response. | `setParkingFacility` body |
| Endpoint `endpoint` | text field | optional | — | — | — | Staff only — omitted from a guest's `listParkingFacilities` response. | `setParkingFacility` body |
| Credential ref `credentialRef` | text field | optional | — | — | — | A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response. | `setParkingFacility` body |
| Push lead minutes `pushLeadMinutes` | number field (minutes) | optional | — | — | — | Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. | `setParkingFacility` body |
| Access points `accessPointIds` | multi-picker: choose access points | optional | — | — | — | Where the platform validates its own code, in `none` and `qrHandoff` modes. | `setParkingFacility` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `setParkingFacility` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **mode**: Three large option cards, each saying what the guest does: "No integration - guest shows QR to security", "Plate whitelist (ANPR) - guest enters plate at checkout, barrier opens by itself", "QR handoff - guest scans QR at the barrier". Required. *(source: contracts/spine/access.yaml#setParkingFacility / DI-300 / DI-316)*
- **vendorName, endpoint, credentialRef, pushLeadMinutes**: Visible only for Plate whitelist and QR handoff, grouped as "Parking system connection". The credential is chosen from the vault (a reference), never typed or shown. Push lead in minutes with the hint "Plates are sent this long before the visit"; for QR handoff the push lead is hidden. *(source: contracts/spine/access.yaml#/components/schemas/ParkingFacility)*
- **accessPointIds**: For No integration and QR handoff only: "Where TICVAI checks the parking code" as a multi-select of the venue's car-park entry access points; hidden for Plate whitelist. *(source: contracts/spine/access.yaml#/components/schemas/ParkingFacility)*
- **capacity**: "Spaces sold per time window" - full means the issued parking entitlements reach it; label it as a sales cap, not live occupancy. *(source: contracts/spine/access.yaml#/components/schemas/ParkingFacility)*
- **takesPayment**: Not an input; show a fixed note "Hourly paid parking stays on the parking operator's own pay station". *(source: DI-300 / contracts/spine/access.yaml#/components/schemas/ParkingFacility)*
- **id, venueId**: Never inputs (per VO-R03); the venue is the top-bar venue. *(source: contracts/spine/access.yaml#setJourneySequenceRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Every parking facility** (data table, from `listParkingFacilities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-assigned, and the upsert key of `setParkingFacility`. Absent in a body, it creates; present, it names the facility being replaced. |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Mode | chip: None, Plate whitelist, QR handoff | CF-52, settled 14 August. Not variations of one thing — each decides what happens at sale and what a guest presents at the barrier. |
| Capacity | 1,234 | What "full" means in the first release (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid … |
| Takes payment | yes / no (icon or chip) | Always false, and stated rather than assumed (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client … |
| Vendor swap target days | 1,234 | A new parking vendor should take days, not weeks — Qossai, 14 August. The team has integrated parking APIs before and the architecture is … |
| Vendor name | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Endpoint | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Credential ref | text | A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response. |
| Push lead minutes | 1,234 | Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. |
| Access points | list or chips (count when long) | Where the platform validates its own code, in `none` and `qrHandoff` modes. |

**Detail panel** (detail panel): TODO

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save parking facility (secondary button) | `setParkingFacility` PUT `/parking-facilities` | ParkingFacility | ParkingFacility | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Car park list**: Name, mode (as words), spaces per window, connection status (for integrated modes), active toggle state. *(source: contracts/spine/access.yaml#listParkingFacilities)*
- **Guest impact note**: Under the mode, show what changes in the guest checkout (Plate whitelist adds a plate field to checkout; the others do not). *(source: contracts/spine/access.yaml#setParkingFacility / DI-316)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save car park**: Upsert of the whole facility (VO-R04); "New car park" sends no id. *(source: contracts/spine/access.yaml#setParkingFacility)*
- **Test connection**: Not in the contract; draw greyed with "Coming with the parking adaptor" if wanted. *(source: designer default)*

**Data it reads**: `listParkingFacilities` (onLoad, Car parks at a venue, and how each integrates)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The parking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the parking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No parking yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId and the parking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PARKING_CONFIGURE`, which `listParkingFacilities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Switching an active facility from Plate whitelist to another mode while plates are pushed for upcoming visits**: Confirm names the upcoming bookings affected and says guests will receive a QR instead. *(source: contracts/spine/access.yaml#setParkingFacility)*

#### Consistency with other screens

- Match `WEB-041`: Guest parking purchase shows the plate field only for Plate whitelist facilities (cross-process, guest).
- Match `BO-064`: Car-park entry access points are created in Zones & Areas; this screen only selects them.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
facilities:
- name: Aqua Park Main Car Park
  mode: Plate whitelist
  spaces: 850
  vendor: Skidata (via adaptor)
  pushLead: 120 min
- name: Summit Peaks Overflow
  mode: No integration
  spaces: 300
  checkedAt: Overflow Gate (security)
```

#### Permissions

- `listParkingFacilities` → `PARKING_CONFIGURE` (configure) · staff, guest
- `setParkingFacility` → `PARKING_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PARKING_CONFIGURE`, which `listParkingFacilities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.4.1 | The payment can be done upfront or at exit. | Admission and Access | PARKED | data `ParkingFacility` |
| 7.4.12 | The system can manage Parking | F&B POS | PARKED | data `ParkingFacility` |
| 7.4.30 | For each PLU, it is possible to manage Parking tickets which can have a fixed rate per day or per hour. | F&B POS | PARKED | data `ParkingFacility` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Parking is barrier integration, not space counting: one configuration screen chooses a model - no integration (TICVAI QR checked by security), ANPR (guest enters a plate at checkout, pushed to the barrier whitelist) or QR handoff to the barrier. Pay-per-hour parking is out of scope. *(agreed · MoM 14 Aug 2026, 10 · DI-316)*
- Parking supports three models: (1) no integration — TICVAI QR verified manually by security; (2) plate number at checkout pushed to the parking system's ANPR whitelist; (3) TICVAI QR passed to the barrier. Hourly pay-on-exit parking stays on the parking system's own POS. *(agreed · MoM 14 Aug 2026, 10. Parking Integrations · DI-300)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A41** Analyse the integration effort for third-party systems (parking, ride/queue-timing sensors, etc.) to consume TAIS's own standardised API as the default integration model *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*
- **A42** Design the parking module to support both native QR-based validation (own solution) and a plate-number capture field for future ANPR/third-party parking integrations *(Softlabs Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-006` · status **notStarted** · provenance generated
- ADR-0030 *A deep link is a pointer, not authorisation* (`docs/adr/0030-deep-link-cold-entry.md`)
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save parking facility.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PARKING_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-030` Work Order Verification

**Verify completed work by someone other than the technician, or send it back.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW` (1 operate, 1 read); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `workOrderId` (deepLink) · cold entry: A work order opened from a queue or an alert. |
| Route | `/venue-operations/access-point-directory` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried eight work-order operations.** An access point directory is `access`, not `maintenance` — the two share the word *point* and nothing else. **Rewired 20 August.** **Named `Access Point Directory` and carried nine work-order operations.** On 20 August I rewired it to access points; **F12 step 4 then refused, because a supervisor verifies a work order here.** The operations were right and the name was wrong — **the flow knew what the screen was for and the name did not.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The screen exists to verify or reject completed work; create, accept, complete, cancel, close and attach-evidence belong to BO-070 and the technician's app (F12 … Removed 2 October 2026 (CHG-WIR-001): The screen exists to verify or reject completed work; create, accept, complete, cancel, close and attach-evidence belong to BO-070 and the technician's app (F12 … Removed 2 October 2026 (CHG-WIR-001): The screen exists to verify or reject completed work; create, accept, complete, cancel, close and attach-evidence belong to BO-070 and the technician's app (F12 …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The supervisor's verification queue: work orders the technician has completed that need a second person to confirm before the asset may return to service. The verifier cannot be the technician who did the work. The one thing to get right: the evidence (before and after photos, resolution, parts, checklist) is in front of the verifier before Verify or Reject.

**Fixed on main** (the package already carries these; draw what it says): Purpose reads "See every gate and what it is doing" (CHG-WIR-003); Create, Accept, Complete, Cancel, Close and Attach evidence actions on the verification screen; id text filters (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listWorkOrders`. | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Sends `?status=` to `listWorkOrders`. | `listWorkOrders` ?status |
| Priority | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Sends `?priority=` to `listWorkOrders`. | `listWorkOrders` ?priority |
| Asset id | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Sends `?assetId=` to `listWorkOrders`. | `listWorkOrders` ?assetId |
| Overdue only | toggle | optional | off | — | — | Sends `?overdueOnly=` to `listWorkOrders`. | `listWorkOrders` ?overdueOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Form: Verify work order** (modal, opened by *Verify work order*; *Verify work order* calls `verifyWorkOrder`, *Cancel* sends nothing)

**Collects what `verifyWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | segmented control | required | — | Verified · Rejected | — | — | `verifyWorkOrder` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `verifyWorkOrder` body |

Errors to draw in the form: 403 Verifier is the technician who completed the work

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Default "Completed, awaiting verification" for the venue; filter by asset category, technician (name picker), priority, overdue - no id text fields. *(source: contracts/satellite/maintenance.yaml#listWorkOrders)*
- **Verification outcome and note**: Verify or Reject; Reject requires a note (what is still wrong) and sends the work order back to the technician. *(source: contracts/satellite/maintenance.yaml#verifyWorkOrder)*

#### Outputs: what the screen shows and produces

**Shown**

**Every work order** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |

**The selected work order** (detail panel, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**The work order** (detail panel, from `getWorkOrder`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Verify work order (primary button) | `verifyWorkOrder` POST `/work-orders/{workOrderId}/verify` | inline | WorkOrder | 403 Verifier is the technician who completed the work | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Queue**: Work order number, asset, priority with source, technician, completed at, time waiting for verification, safety-critical flag first. *(source: contracts/satellite/maintenance.yaml#listWorkOrders / DI-923)*
- **Evidence panel**: Resolution and code, before/during/after photos in stage order, parts used, sign-off signature; downtime minutes. *(source: contracts/satellite/maintenance.yaml#attachWorkOrderEvidence / contracts/satellite/maintenance.yaml#completeWorkOrder)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Verify**: Moves Completed to Verified; if the asset requires an inspection to return, offers "Return to service" which needs a completed inspection. *(source: contracts/satellite/maintenance.yaml#verifyWorkOrder / contracts/satellite/maintenance.yaml#setAssetStatus)*
- **Reject**: Back to the technician with the note; appears in their Staff App queue. *(source: contracts/satellite/maintenance.yaml#verifyWorkOrder)*

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `BO-070` Work Orders: *Work Orders*; carries `workOrderId`
- → `BO-069` Asset Register: *Asset returns to service*; carries `assetId`; calls `verifyWorkOrder`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The work order verification list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the work order verification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No work order verification yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the work order verification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Verifier is the technician who completed it**: Verify disabled with "You completed this job - another supervisor must verify". *(source: contracts/satellite/maintenance.yaml#verifyWorkOrder)*
- **Safety-critical job completed without completion photos**: Flag "Missing completion evidence"; Verify still possible only with a note. *(source: contracts/satellite/maintenance.yaml#completeWorkOrder)*

#### Consistency with other screens

- Match `BO-070`: Same work-order row, statuses and priority-with-source display.
- Match `BO-069`: Return to service lands on the asset.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
- wo: WO-2026-01482
  asset: Falcon Coaster restraint bar R3
  priority: Emergency (asset override)
  tech: Rahul Menon
  completed: 1 Oct 2026 09:12
  waiting: 38 min
  safety: true
- wo: WO-2026-01477
  asset: Main Plaza Gate 2 turnstile
  priority: High (scored 78)
  tech: Omar Haddad
  completed: 1 Oct 2026 08:40
```

#### Permissions

- `verifyWorkOrder` → `WORK_ORDER_VERIFY` (operate) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.4.6 | Work Order Approval - System shall support work order approvals. | Maintenance & Safety Management | CONTRACTED | `verifyWorkOrder` |
| 17.4.7 | Work Order Closure - System shall support work order closure workflows. | Maintenance & Safety Management | CONTRACTED | `verifyWorkOrder` |
| 17.4.8 | Work Order Audit Trail - System shall maintain work order audit logs. | Maintenance & Safety Management | CONTRACTED | `getWorkOrder` |
| 17.3.4 | Root Cause Analysis - System shall support root cause analysis. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.3.5 | Maintenance Escalation - System shall support maintenance escalation workflows. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.3.6 | Downtime Tracking - System shall track equipment downtime. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.4.5 | Work Order Escalation - System shall support work order escalations. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.5.6 | Corrective Actions - System shall support corrective action management. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.5.8 | Safety Escalations - System shall support safety escalation workflows. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.6.2 | Spare Parts Reservations - System shall support spare parts reservations. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-030` · status **notStarted** · provenance generated
- Flow F12 *Asset fails and closes a queue*, step 4: Supervisor verifies → **By someone other than the person who did the work.** Safety-critical assets cannot return without it
- Flow F12 branch at step 4 (requiresStaff): when Verifier is the person who did the work, **Refused.** This is the control, and it is enforced rather than trusted.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-030?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Verify work order.
- [ ] Every transition is wired: `BO-070`, `BO-069`.
- [ ] Every gated control is gated: `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-031` Asset Register

**Know what equipment exists and where (merged into BO-069 Asset Register).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAssets` reads the population and `getAsset` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `assetId` (deepLink) · cold entry: An asset opened from the register or a work order. |
| Route | `/venue-operations/access-point-configuration` |

**What the spec says about it.** **Merged into BO-069** (decided 2 October 2026, Chinmay: fix the wrong wiring now; CHG-WIR-001). BO-031 and BO-069 are the same asset register (same seven maintenance operations, near-identical layouts); keep BO-069 and retire BO-031 (DI-671, DI-987; design-notes corrections venue-operations BO-031, BO-069). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-069, and nothing on it is built separately. Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried seven asset operations.** A turnstile is an asset and configuring an access point is not asset management. **Rewired 20 August.** **Named `Access Point Configuration` and carried seven asset operations.** Same correction as BO-030 — F12 step 5 returns an asset to service here.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Duplicate of BO-069 (both "Asset Register" on the same listAssets/getAsset/createAsset operations). Keep one asset register; this note set describes the differences so the lead can choose. The one thing to get right for whichever survives: the 360 view of an asset (documents, warranty, lifecycle history, open work orders, location), searchable by scanning its QR tag.

**Fixed on main** (the package already carries these; draw what it says): BO-031 and BO-069 are the same asset register (CHG-WIR-001); Purpose "Define what a gate is and where it is" and navigation exit to BO-001 Queue Directory (CHG-WIR-003).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Asset 360**: Header with tag, name, category, criticality and status; tabs Overview, Documents (manuals, SOPs, certificates, warranty, drawings, risk assessments), History (work orders, inspections, incidents, status changes in sequence), Maintenance plans, Location. *(source: DI-910 / contracts/satellite/maintenance.yaml#getAsset / contracts/satellite/maintenance.yaml#getAssetHistory)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset register list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset register untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset register yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, categoryId, status, maintenanceDue and the asset register are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission the screen requires, and names it. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-069`: Same screen; merge into BO-069 (which already carries the fault priority override).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asset:
  tag: AP-RIDE-0007
  name: Falcon Coaster
  category: Rides
  criticality: Safety critical
  status: In service
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission the screen requires, and names it. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A 360-degree asset view, searchable via QR code, consolidates all asset details: attached documentation (installation manuals, wiring diagrams, safety inspection reports), warranty period and full lifecycle history (installed, maintained, operational, upcoming maintenance); a location view shows where each asset physically sits. *(client request · MoM 17 Sep 2026, 4.1 Asset Registry & Classification · DI-910)*
- Corrective-maintenance priority combines a configurable weighted scoring model (e.g. P1 emergency when guest operations are affected) with a direct per-asset priority override field: "if this specific device goes down, raise this priority level". *(agreed · MoM 17 Sep 2026, 4.3 Corrective & Emergency Maintenance · DI-909)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-031` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-031?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-032` Admission Profiles

**Set the rules a gate enforces, including offline.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · ticket #17917 (APP-SETUP-BO-032) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAdmissionRules` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `profileId` (deepLink), `ruleId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/admission-rules` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The admission profile editor: the named rule set a gate enforces, online and offline, for every product that points at it. A venue access manager creates and maintains a handful of profiles (Standard day ticket, Annual pass, Gold tier, School group) and the gates judge every scan against them. The one thing to get right: one profile is edited in one place, as sections (Admission window, Entries and re-entry, Validity, Crossover, Where it is valid), with one Save, because the write replaces the whole profile.

**Fixed on main** (the package already carries these; draw what it says): Navigation exit to BO-001 Queue Directory (CHG-WIR-002); Create and Save overlays list `id` (and `scopePath`) as required inputs (CHG-SBO-009); Table and detail panel bind only the eleven old columns (and show id, scopePath) (CHG-SBO-009); Labels "Every admission rules", "Create admission rules", "Save admission rules" (CHG-SBO-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should an edit to a profile already used by issued tickets be effective-dated (apply from a chosen date) rather than at the next package refresh?** → Drawn default accepted: Draw a "Takes effect" control with "Next package refresh" selected and a greyed "From date" option. *(decided by Chinmay, 2026-10-02; DEC-125 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Form: New profile** (modal, opened by *New profile*; *New profile* calls `createAdmissionRules`, *Cancel* sends nothing)

**Collects what `createAdmissionRules` sends before it is called.** Required: `code`, `name`, `openMinutesBefore`, `closeMinutesAfter`. Optional: `perProductRules`, `maxDurationMinutes`, `requiresExitBeforeReentry`, `maxReentries`, `entryLimit`, `exitScan`, `maxExits`, `reEntryWindowMinutes`, `sameDayOnly`, `designatedAccessPointIds`, `validity`, `crossover`, `allowedAccessPointIds`, `reEntryVerification`, `ruleConditions`. `id` and `scopePath` are the server's and never asked (VO-R03). Entry limit, exit scan, re-entry window and verification, validity, crossover and the rule conditions are blocks of the profile (29 September close-out), edited here so BO-156, BO-158 and BO-160 have a home. …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `createAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `createAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `createAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `createAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `createAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `createAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `createAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `createAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `createAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `createAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `createAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `createAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `createAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `createAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `createAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `createAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `createAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `createAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `createAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `createAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `createAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `createAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `createAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `createAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `createAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `createAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `createAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `createAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `createAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `createAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `createAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `createAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `createAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `createAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `createAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `createAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `createAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `createAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `createAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `createAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `createAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `createAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `createAdmissionRules` body |

**Form: Save profile** (modal, opened by *Save profile*; *Save profile* calls `updateAdmissionRules`, *Cancel* sends nothing)

**Collects what `updateAdmissionRules` sends before it is called.** Required: `code`, `name`, `openMinutesBefore`, `closeMinutesAfter`. Optional: `perProductRules`, `maxDurationMinutes`, `requiresExitBeforeReentry`, `maxReentries`, `entryLimit`, `exitScan`, `maxExits`, `reEntryWindowMinutes`, `sameDayOnly`, `designatedAccessPointIds`, `validity`, `crossover`, `allowedAccessPointIds`, `reEntryVerification`, `ruleConditions`. `id` and `scopePath` are the server's and never asked (VO-R03). Entry limit, exit scan, re-entry window and verification, validity, crossover and the rule conditions are blocks of the profile (29 September close-out), edited here so BO-156, BO-158 and BO-160 have a home. …

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

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **name / code**: Name is what staff see on scan screens and reports (max 200, Arabic variant per VO-R10); code is a short unique key (max 64, upper-case, e.g. ANNUAL-1PD) shown in exports. Code is editable only until a product points at the profile; afterwards show it read-only with the reason. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **id, scopePath**: Never shown as inputs (per VO-R03); the overlay that lists `id` as required is wrong. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **openMinutesBefore / closeMinutesAfter / maxDurationMinutes**: Group as "Admission window": "Gates open [30] min before the performance and close [60] min after"; "An unused admission expires [20] min after its admission time" (maxDurationMinutes, empty = never). Minutes, whole numbers, 0 allowed. Show a one-line preview on a sample 14:00 performance ("Valid 13:30 to 15:00"). *(source: MATRIX 3.2.10 / contracts/spine/access.yaml#createAdmissionRules)*
- **entryLimit (mode, count, periodDays)**: A single choice: Unlimited / Once / N times / N per day / N per period; the count appears only for the last three and is required for them (min 1); period days only for N per period. Absent = Unlimited. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules / DI-171 / DI-626)*
- **exitScan, maxExits, reEntryWindowMinutes, sameDayOnly, designatedAccessPointIds, reEntryVerification, maxReentries …**: Group as "Exit and re-entry". Exit scan is Required / Optional (free rotation, default) / None; when Required, "Exit before re-entry" is implied and shown ticked and locked. Re-entry window in minutes (empty = any time while valid), Same day only (default on), Re-entry only through (multi-select of access points, empty = any allowed point), and Re-entry check (Credential only, Credential + UV stamp, Credential + face, Credential + operator check). Hide the re-entry fields when the entry limit is Once. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules / DI-461 / DI-626)*
- **validity (anchor, days, from, to, endOf, daysOfWeek, dayTypes, blackoutDates)**: "Valid" as one sentence builder: Fixed dates (from-to date pickers, to not before from) or N days after sale / activation / first use, optionally "to the end of that day/week/month/year"; then weekday chips (empty = every day), day types (peak, off-peak, holidays, seasons, event dates) and blackout dates on a month calendar (per VO-R01). Blackout always wins; say so under the calendar. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules / DI-628 / DI-171)*
- **crossover**: Off by default ("Admits to one park only"). When on: pick at least two parks, optional required order, same day only (default) or different days, consecutive from first scan vs flexible within validity, max park entries, number of crossovers, earliest crossover time (HH:MM venue time), park that must be entered first, re-entry after crossover. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules / DI-628)*
- **allowedAccessPointIds (and setEntryRulePoints)**: "Where it is valid": a venue topology tree (park > zone > access point) with tick boxes; empty means every access point in the venue and must be shown as "All access points" not as nothing ticked. Tier profiles (Bronze/Silver/Gold) need explicit deny as well as allow: show a third state per access point (Allowed / Denied / Not set). Saving coverage replaces the whole set, so show "4 added, 1 removed" before Save. *(source: DI-185 / contracts/spine/access.yaml#setEntryRulePoints / MATRIX 7.4.25)*
- **perProductRules**: A small table "Product exceptions": a product picker and the entry limit for that product (e.g. Annual pass: 1 per day while the profile default is Unlimited). Replaced as one list on save. *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Admission profiles** (data table, from `listAdmissionRules`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Open minutes before | 1,234 | How long before a performance validation opens. |
| Close minutes after | 1,234 | — |
| Max duration minutes | 1,234 | — |
| Entry limit | grouped details | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & … |
| Exit scan | chip: Required, Optional, None | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. |
| Max exits | 1,234 | Null is unlimited (decided 29 September, VM close-out) |
| Requires exit before reentry | yes / no (icon or chip) | — |
| Max reentries | 1,234 | — |
| Re entry window minutes | 1,234 | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) |
| Re entry verification | chip: Credential only, Credential uv stamp, Credential face, Credential operator, Custom | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out … |

**The selected profile** (detail panel, from `listAdmissionRules`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Open minutes before | 1,234 | How long before a performance validation opens. |
| Close minutes after | 1,234 | — |
| Max duration minutes | 1,234 | — |
| Entry limit | grouped details | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & … |
| Exit scan | chip: Required, Optional, None | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. |
| Max exits | 1,234 | Null is unlimited (decided 29 September, VM close-out) |
| Requires exit before reentry | yes / no (icon or chip) | — |
| Max reentries | 1,234 | — |
| Re entry window minutes | 1,234 | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) |
| Re entry verification | chip: Credential only, Credential uv stamp, Credential face, Credential operator, Custom | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out … |
| Same day only | yes / no (icon or chip) | Re-entry only on the day of the exit (decided 29 September, VM close-out) |
| Validity | grouped details | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). |
| Crossover | grouped details | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules) … |
| Designated access points | list or chips (count when long) | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) |
| Allowed access points | list or chips (count when long) | Empty means any access point in the venue. |
| Rule conditions | grouped details | The visual rule builder body `setVisualAccessRule` writes: `appliesTo` (products or credential types), `conditions`, `logic` (AND / OR / … |
| Per product rules | list or chips (count when long) | BL-059. Transaction rules were per profile and a ticket type could not state its own. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| New profile (primary button) | `createAdmissionRules` POST `/admission-rules` | AdmissionRules | AdmissionRules | — | opens modal first |
| Save profile (secondary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Profile list (left)**: Columns: Name, Code, Entries (e.g. "Once", "1 per day"), Re-entry (e.g. "Exit required, same day"), Valid (e.g. "Fixed 1 Oct - 31 Dec 2026" or "30 days after first use"), Access points ("All" or count), Products using it (count). Never show raw minutes columns or ids (per VO-R12). *(source: designer default / MATRIX 3.2.7)*
- **Detail panel**: A plain-language summary of the profile as a guest-at-the-gate would experience it ("Enter once a day, re-enter the same day after an exit scan at Main Plaza gates, valid 30 days from first use, Aqua Park and Summit Peaks, crossover after 14:00"), then the sections. *(source: designer default / DI-626)*
- **Effect notice**: After saving: "Gates apply this after their next offline package refresh" with the time of the last package build; changes are not retroactive to scans already made, and do apply to tickets already issued that reference the profile. *(source: contracts/spine/access.yaml#updateAdmissionRules / MATRIX 3.2.34)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New profile**: Opens the editor empty with defaults (Exit scan Optional, Same day only on, Unlimited entries); no id field. *(source: contracts/spine/access.yaml#createAdmissionRules)*
- **Save profile**: Sends the whole profile (per VO-R04). Confirmation names the products and access points affected ("Used by 6 products; applies at 14 access points after next package refresh"). 422 messages appear against the field (e.g. count missing for N per day; to-date before from-date). *(source: contracts/spine/access.yaml#updateAdmissionRules)*
- **Test with a virtual scan**: Opens the in-screen simulation (pick a product, gate, date and time; shows Admitted or the deny reason) before publishing. *(source: DI-629 / DI-722)*

**Data it reads**: `listAdmissionRules` (onLoad, List admission profiles)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The admission profiles list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the admission profiles untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No admission profiles yet. Offers New profile (`createAdmissionRules`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listAdmissionRules` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listAdmissionRules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Edge cases to draw

- **Profile used by products already on sale**: Save allowed; the confirm names the count of issued tickets it will change, because a profile is referenced, not copied. *(source: MATRIX 3.2.34)*
- **Exit scan Required but no exit access point exists in the coverage**: Warn before save ("No exit gate in this profile's access points; guests could never re-enter"). *(source: contracts/spine/access.yaml#/components/schemas/AdmissionRules / DI-461)*
- **Viewer without access configuration rights**: Read-only editor, Save disabled with "Needs access configuration rights" (per VO-R08). *(source: contracts/spine/access.yaml#updateAdmissionRules)*

#### Consistency with other screens

- Match `BO-156`: BO-156 (Entry, Exit & Re-entry), BO-158 (Validity), BO-160 (Crossover) and BO-155 (Visual rule builder) edit blocks of this same profile; draw them as sections of this editor (per VO-R14), same labels.
- Match `SCN-003`: The deny reasons the scanner shows (Re-entry limit reached, Exit scan required, Wrong gate, Not yet valid, Expired) are the consequences of these fields; use the same words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profiles:
- name: Standard day ticket
  code: STD-DAY
  entries: Once
  reentry: Exit required, same day, 120 min window
  valid: 'Fixed: visit date'
  accessPoints: Aqua Park main gates (3)
  products: 12
- name: Annual pass
  code: ANNUAL-1PD
  entries: 1 per day
  reentry: Exit optional
  valid: 365 days after activation
  accessPoints: All
  products: 2
- name: Gold tier
  code: TIER-GOLD
  entries: Unlimited
  reentry: Any time
  valid: Fixed 1 Oct 2026 - 30 Sep 2027
  accessPoints: All, denied at Silver/Bronze entrance
  products: 1
- name: Two-park crossover
  code: XPARK-2
  entries: Once per park
  reentry: Same day
  valid: Visit date
  crossover: Aqua Park > Summit Peaks after 14:00
  products: 3
```

#### Permissions

- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `createAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `setEntryRulePoints` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listAdmissionRules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 1.1.51 | Admission entitlement management | Ticketing Catalogue | CONTRACTED | `createAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 1.5.5 | The system should allow specification of rules and conditions associated with a ticket. These rules and conditions will govern the usage of the ticket and any transactions associated with a ticket … | Ticketing Catalogue | CONTRACTED | data `AdmissionRules` |
| 3.2.9 | The system should have the possibility to activate/deactivate the biometric check on some type of tickets. For example, membership passes, annual pass holder, multi day and multi attraction tickets. | Admission and Access | CONTRACTED | data `AdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Tiered access (e.g. Bronze/Silver/Gold): the client fills a matrix of which gates/attractions each tier may scan into; configured as location → admission profile → gate → access point, with explicit deny rules (e.g. Gold denied at the Silver/Bronze entrance). *(agreed · MoM 7 Aug 2026, 24. Tiered Ticketing & Access Control Deep Dive · DI-185)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-032` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (94), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-032?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: New profile, Save profile.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-033` Blacklist Management

**Bar a media code outright.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · ticket #17918 (APP-SETUP-BO-033) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listBlacklist` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `mediaCode` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/blacklist-management` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The tenant-wide list of media codes that are refused at every gate whatever the ticket says, with the reason and an optional expiry. It travels in the offline package, so a blacklisted wristband is refused even when the gate is offline. The one thing to get right: adding an entry is a serious, attributed act with a reason, and the scanner treats it differently from an ordinary denial (no override, supervisor summoned).

**Fixed on main** (the package already carries these; draw what it says): Navigation exit to BO-001 Queue Directory (inferred) (CHG-WIR-002); Columns show addedByPrincipalId and scopePath (CHG-SBO-009).

#### Inputs: what the user enters or picks

**Form: Add blacklist entry** (modal, opened by *Add blacklist entry*; *Add blacklist entry* calls `addBlacklistEntry`, *Cancel* sends nothing)

**Collects what `addBlacklistEntry` sends before it is called.** Required: `mediaCode`, `reason`. Optional: `expiresAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Media code `mediaCode` | text area | required | — | max length 256 | — | — | `addBlacklistEntry` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `addBlacklistEntry` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addBlacklistEntry` body |
| List type `listType` | segmented control | optional | Blacklist | Blacklist · Whitelist | — | A whitelist entry waits for a second approver (DEC-254; CHG-CSP-031). | `addBlacklistEntry` body |
| Disable scope `disableScope` | select | optional | Entire credential | Entire credential · Venue access · Attraction access · Re entry · Fast pass · Specific entitlement | — | What the entry disables (`BlacklistEntry.disableScope`). | `addBlacklistEntry` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **mediaCode**: Scan or type the media code (QR, wristband serial); on entry, show what it belongs to (ticket number, product, holder if name-bound) so the operator blacklists the right thing. One entry per code across the tenant: an existing code shows "Already blacklisted since <date>". *(source: contracts/spine/access.yaml#addBlacklistEntry)*
- **reason**: Required, max 500; offer common reasons as chips (Reported lost, Fraud suspected, Banned guest, Duplicate printed) with free text. *(source: contracts/spine/access.yaml#addBlacklistEntry)*
- **expiresAt**: Optional "Blacklisted until" date and time; empty = permanent, shown as "Permanent". *(source: contracts/spine/access.yaml#addBlacklistEntry)*

#### Outputs: what the screen shows and produces

**Shown**

**Blacklist** (data table, from `listBlacklist`): `addedByPrincipalId` is shown as the person's name.

| Shows | Format | Notes |
|---|---|---|
| Media code | text | Unique within the tenant (decided 28 September, audit R108): one entry per code. |
| Reason | text | — |
| Added at | 1 Oct 2026, 14:30 | — |
| Added by principal | the name it points at, never the id | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**The selected blacklist entry** (detail panel, from `listBlacklist`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | Unique within the tenant (decided 28 September, audit R108): one entry per code. |
| Reason | text | — |
| Added at | 1 Oct 2026, 14:30 | — |
| Added by principal | the name it points at, never the id | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Add blacklist entry (primary button) | `addBlacklistEntry` POST `/blacklist` | inline | BlacklistEntry | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Remove blacklist entry (destructive button) | `removeBlacklistEntry` DELETE `/blacklist/{mediaCode}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Blacklist table**: Media code, what it belonged to, reason, added by (person's name, not principal id), added on, until. Newest first; expired entries hidden by default with a toggle. *(source: contracts/spine/access.yaml#listBlacklist)*
- **Offline note**: "Gates receive changes with their next offline package" with the last package time. *(source: contracts/spine/access.yaml#addBlacklistEntry)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add to blacklist**: Confirmation names the media and says it will be refused at every venue of the tenant. *(source: contracts/spine/access.yaml#addBlacklistEntry)*
- **Remove**: Confirm "This code will be admitted again if its ticket is valid"; to change a reason, remove and re-add. *(source: contracts/spine/access.yaml#removeBlacklistEntry / contracts/spine/access.yaml#addBlacklistEntry)*

**Data it reads**: `listBlacklist` (onLoad, List blacklisted media)

**What opens over it**

- confirmDialog *Remove blacklist entry*: **Names what `removeBlacklistEntry` changes and what it leaves alone**, in the consequence rather than the verb. A blacklist this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The blacklist list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the blacklist untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No blacklist yet. Offers Add blacklist entry (`addBlacklistEntry`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listBlacklist` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listBlacklist` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … |

#### Edge cases to draw

- **Code already blacklisted**: 409 shown inline with a link to the existing entry. *(source: contracts/spine/access.yaml#addBlacklistEntry)*
- **Refunded, transferred or reissued tickets**: These are invalidated by the entitlement state, not by adding them here; say so in the empty state to stop staff blacklisting by hand. *(source: MATRIX 3.1.4)*

#### Consistency with other screens

- Match `SCN-003`: A blacklisted scan shows "Blacklisted - call a supervisor" with no override (F06 branch).
- Match `BO-034`: Scan activity filters by deny reason Blacklisted using the same label.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entries:
- media: WB-221903
  belongsTo: VT0451 Aqua Park Day Pass
  reason: Reported lost
  addedBy: Fatima Al Hashimi
  true: 28 Sep 2026 11:20
  until: Permanent
- media: QR-9KD2-11PX
  belongsTo: VT0788 Summit Peaks Annual Pass
  reason: Fraud suspected - shared at two gates
  addedBy: Omar Haddad
  true: 30 Sep 2026 16:05
  until: 31 Dec 2026
```

#### Permissions

- `listBlacklist` → `SCOPE_VIEW` (read) · staff
- `addBlacklistEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `removeBlacklistEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listBlacklist` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.6 | The system should be able to validate tickets and membership passes with different rules based on entitlements, manage black and white list of tickets. Upon a scanning a valid ticket, the system … | Admission and Access | CONTRACTED | `listBlacklist` |
| 3.1.4 | The system shall immediately invalidate dynamic QR codes when tickets are refunded, cancelled, transferred, exchanged, upgraded, or re-issued. | Admission and Access | CONTRACTED | `addBlacklistEntry` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-033` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-033?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Add blacklist entry, Remove blacklist entry.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

**16 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addBlacklistEntry": {"method":"POST","path":"/blacklist","contract":"access","summary":"Blacklist a media code","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BlacklistEntry"},
"callNextParties": {"method":"POST","path":"/queues/{queueId}/call-next","contract":"queue","summary":"Call the next parties forward","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"configureQueueFeed": {"method":"PUT","path":"/queue-feeds","contract":"queue","summary":"Configure a sensor feed","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"QueueFeed","responds":"QueueFeed"},
"createAdmissionRules": {"method":"POST","path":"/admission-rules","contract":"access","summary":"Create an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"createQueue": {"method":"POST","path":"/queues","contract":"queue","summary":"Create a queue","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateQueueRequest","responds":"Queue"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getQueue": {"method":"GET","path":"/queues/{queueId}","contract":"queue","summary":"Read a queue with live position","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"QueueDetail"},
"getQueueFeedHealth": {"method":"GET","path":"/queue-feeds/{feedId}/health","contract":"queue","summary":"Feed health","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"QueueFeedHealth"},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"getWorkOrder": {"method":"GET","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Read a work order","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkOrderDetail"},
"listAdmissionRules": {"method":"GET","path":"/admission-rules","contract":"access","summary":"List admission profiles","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBlacklist": {"method":"GET","path":"/blacklist","contract":"access","summary":"List blacklisted media","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listParkingFacilities": {"method":"GET","path":"/parking-facilities","contract":"access","summary":"Car parks at a venue, and how each integrates","permission":"PARKING_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueueEntries": {"method":"GET","path":"/queues/{queueId}/entries","contract":"queue","summary":"List entries in a queue","permission":"QUEUE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueueFeeds": {"method":"GET","path":"/queue-feeds","contract":"queue","summary":"List configured sensor feeds","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"QueueFeed"},
"listQueues": {"method":"GET","path":"/queues","contract":"queue","summary":"List queues","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkOrders": {"method":"GET","path":"/work-orders","contract":"maintenance","summary":"List work orders","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"overdueOnly","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"removeBlacklistEntry": {"method":"DELETE","path":"/blacklist/{mediaCode}","contract":"access","summary":"Remove a blacklist entry","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"setEntryRulePoints": {"method":"PUT","path":"/admission-rules/{ruleId}/points","contract":"access","summary":"Set the access points an admission rule covers","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"ruleId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"AccessEntryRulePoint","responds":"AccessEntryRulePoint"},
"setParkingFacility": {"method":"PUT","path":"/parking-facilities","contract":"access","summary":"Configure a car park and its integration","permission":"PARKING_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ParkingFacility","responds":"ParkingFacility"},
"setQueueStatus": {"method":"PUT","path":"/queues/{queueId}/status","contract":"queue","summary":"Open, pause or close a queue","permission":"QUEUE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"QueueStatusResult"},
"setWaitTime": {"method":"PUT","path":"/queues/{queueId}/wait-time","contract":"queue","summary":"Manually set a wait time","permission":"QUEUE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WaitTime"},
"testQueueFeed": {"method":"POST","path":"/queue-feeds/{feedId}/test","contract":"queue","summary":"Test a feed before trusting it","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FeedTestResult"},
"updateAdmissionRules": {"method":"PUT","path":"/admission-rules/{profileId}","contract":"access","summary":"Update an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"updateQueue": {"method":"PATCH","path":"/queues/{queueId}","contract":"queue","summary":"Amend queue configuration","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Queue"},
"verifyWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/verify","contract":"maintenance","summary":"Supervisor verification","permission":"WORK_ORDER_VERIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessEntryRulePoint": {"type":"object","x-ticvai-persistence":"access.entry_rule_point","description":"**Taken from the backend workbook, 20 September.** Maps the access points that are allowed for an admission profile.","required":["admissionProfileId","accessPointId","isActive","createdAt"],"properties":{"admissionProfileId":{"type":"string","format":"uuid","readOnly":true},"accessPointId":{"type":"string","format":"uuid"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"id":{"type":"string","format":"uuid","readOnly":true}}},
"AdmissionRules": {"x-ticvai-persistence":"access.admission_rules","type":"object","required":["id","code","name","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Server-assigned.** Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names.\n"},"code":{"type":"string","maxLength":64},"perProductRules":{"allOf":[{"$ref":"#/components/schemas/PerProductRuleList"}],"description":"BL-059. **Transaction rules were per profile and a ticket type could not state its own.** An annual pass allowing one entry per day and a single ticket allowing one entry ever are different rules, and forcing a profile per product multiplies profiles instead.\n"},"name":{"type":"string","maxLength":200},"openMinutesBefore":{"type":"integer","description":"How long before a performance validation opens."},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean","default":false},"maxReentries":{"type":"integer","nullable":true},"entryLimit":{"type":"object","description":"**How many times the credential may enter** (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). Absent means `unlimited`.","required":["mode"],"properties":{"mode":{"type":"string","enum":["unlimited","once","nTimes","nPerDay","nPerPeriod"],"default":"unlimited"},"count":{"type":"integer","minimum":1,"description":"N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it)"},"periodDays":{"type":"integer","minimum":1,"description":"The period for nPerPeriod"}}},"exitScan":{"type":"string","enum":["required","optional","none"],"default":"optional","description":"(decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. `optional`: exits run in free rotation and headcount is inferred. `none`: the exit has no reader."},"maxExits":{"type":"integer","minimum":0,"nullable":true,"description":"Null is unlimited (decided 29 September, VM close-out)"},"reEntryWindowMinutes":{"type":"integer","minimum":1,"nullable":true,"description":"Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out)"},"sameDayOnly":{"type":"boolean","default":true,"description":"Re-entry only on the day of the exit (decided 29 September, VM close-out)"},"designatedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out)"},"validity":{"type":"object","description":"**When the credential is valid** (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). The admission window above still applies inside it.","required":["anchor"],"properties":{"anchor":{"type":"string","enum":["fixedRange","afterSale","afterActivation","afterFirstUse"],"description":"fixedRange uses from and to; the others count days from the event"},"days":{"type":"integer","minimum":1,"description":"N days after the anchor; required unless the anchor is fixedRange"},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date","description":"Inclusive. Must not be before from (`422`)"},"endOf":{"type":"string","enum":["day","week","month","year"],"nullable":true,"description":"Validity runs to the end of the day, week, month or year the relative period ends in"},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Empty is every day"},"dayTypes":{"type":"array","items":{"type":"string","enum":["peakDates","offPeakDates","holidays","seasons","eventDates"]},"description":"Calendar day types on which access is allowed; empty is every day type"},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Dates on which access is refused whatever else allows it"}}},"crossover":{"type":"object","nullable":true,"description":"**Crossover between parks** (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. Null means the profile admits to one park only.","required":["allowedParkOrgUnitIds"],"properties":{"allowedParkOrgUnitIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"parkOrder":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Required order of parks, if any; empty is any order"},"sameDayOnly":{"type":"boolean","default":true},"differentDayAccess":{"type":"boolean","default":false},"dayPattern":{"type":"string","enum":["consecutiveFromFirstScan","flexibleWithinValidity"],"default":"flexibleWithinValidity"},"maxParkEntries":{"type":"integer","minimum":1,"nullable":true,"description":"Null is unlimited"},"crossoverQuantity":{"type":"integer","minimum":1,"nullable":true,"description":"How many crossovers; null is unlimited"},"crossoverAfterTime":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Earliest venue-local time HH:MM a crossover is allowed"},"prerequisiteParkOrgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The park that must be entered first"},"reEntryAfterCrossover":{"type":"boolean","default":false}}},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Empty means any access point in the venue."},"reEntryVerification":{"type":"string","enum":["credentialOnly","credentialUvStamp","credentialFace","credentialOperator","custom"],"default":"credentialOnly","description":"What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1)."},"ruleConditions":{"type":"object","nullable":true,"description":"The visual rule builder body `setVisualAccessRule` writes: `appliesTo` (products or credential types), `conditions`, `logic` (AND / OR / NOT over the conditions), `decision` (allow, deny, referToOperator, overrideEligible) and `consequences`. **One `jsonb` column on the rule row**, read with the rule and never queried on its own; the locations stay in `access.entry_rule_point` (added 29 September, data-model close-out DM1)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"BlacklistEntry": {"x-ticvai-persistence":"access.blacklist","type":"object","required":["mediaCode","reason","addedAt","addedByPrincipalId"],"properties":{"mediaCode":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108): one entry per code. `addBlacklistEntry` refuses a second entry with `409 duplicate-code`. **One code space for both lists** (decided 29 September, writers pass): a code on the blacklist cannot also be whitelisted; adding it to the other list is the same `409 duplicate-code`. Move a code between lists by removing and re-adding it."},"reason":{"type":"string"},"addedAt":{"type":"string","format":"date-time"},"addedByPrincipalId":{"type":"string","format":"uuid"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"listType":{"type":"string","enum":["blacklist","whitelist"],"default":"blacklist","description":"A blacklist entry refuses the media; a whitelist entry is an approved exception to a restriction (added 29 September, data-model close-out DM1)."},"disableScope":{"type":"string","enum":["entireCredential","venueAccess","attractionAccess","reEntry","fastPass","specificEntitlement"],"default":"entireCredential","description":"What the entry disables (added 29 September, data-model close-out DM1)."},"distributedTo":{"type":"array","items":{"type":"string","enum":["centralPlatform","venueEdge","onlineGates","offlineRevocationPackage"]},"description":"Where the restriction has been distributed so far, as `listCredentialDisableBlacklist` returns it (added 29 September, data-model close-out DM1)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"CreateQueueRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","capacityPerCycle","cycleMinutes"],"properties":{"code":{"type":"string","maxLength":64},"name":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid"},"attractionProductId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["standby","singleRider","fastPass","virtual","accessible","groupOnly","staffOnly"],"default":"standby","description":"5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"},"operatingWindows":{"type":"array","description":"**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n","items":{"type":"object","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue starts running."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue stops running."},"lastEntryMinutesBefore":{"type":"integer","default":0,"description":"**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"}}}},"parentQueueId":{"type":"string","format":"uuid","nullable":true,"description":"Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"},"loadBalanceWithQueueIds":{"type":"array","description":"BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n","items":{"type":"string","format":"uuid"}},"inQueueOfferEnabled":{"type":"boolean","default":false,"description":"**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"},"notifyBeforeCallMinutes":{"type":"integer","default":5,"description":"BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"},"capacityPerCycle":{"type":"integer","minimum":1},"cycleMinutes":{"type":"number","minimum":0},"maxPartySize":{"type":"integer","default":6},"returnWindowMinutes":{"type":"integer","default":15,"description":"How long a called party has to arrive before the entry expires."},"heightRequirementCm":{"type":"integer","nullable":true},"fastPassAllocationPercent":{"type":"number","minimum":0,"maximum":100,"default":0,"description":"Share of each cycle reserved for Fast Pass holders."},"zone":{"type":"string","nullable":true},"fastPass":{"allOf":[{"$ref":"#/components/schemas/QueueFastPass"}],"nullable":true,"description":"The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"}}},
"FeedTestResult": {"type":"object","x-ticvai-persistence":"none — computed, discarded","required":["succeeded","checks","testedAt"],"properties":{"succeeded":{"type":"boolean"},"checks":{"type":"array","items":{"type":"object","required":["check","passed"],"properties":{"check":{"type":"string","enum":["reachable","authenticated","payloadParsed","readingMapped","withinInterval"]},"passed":{"type":"boolean"},"detail":{"type":"string"},"latencyMs":{"type":"integer","nullable":true}}}},"sampleReading":{"allOf":[{"$ref":"#/components/schemas/QueueReading"}],"description":"What the source actually returned, mapped. Shown so a configurer can see whether \"people count 4\" means four people or four groups before it drives a board.\n"},"rawSample":{"type":"string","nullable":true,"description":"Truncated raw payload. The only way to diagnose a source that is reachable and returning a shape nobody mapped.\n"},"testedAt":{"type":"string","format":"date-time"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ParkingFacility": {"type":"object","x-ticvai-persistence":"access.parking_facility","required":["name","venueId","mode"],"properties":{"id":{"type":"string","format":"uuid","description":"**Server-assigned, and the upsert key of `setParkingFacility`.** Absent in a body, it creates; present, it names the facility being replaced. A client never mints one.\n"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"mode":{"$ref":"#/components/schemas/ParkingIntegrationMode"},"capacity":{"type":"integer","nullable":true,"description":"**What \"full\" means in the first release** (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid for a time reach this number. There is no live space count from the car park; a guest sees *full* only when capacity is reached, never an availability figure. Null means no limit is enforced.\n"},"takesPayment":{"type":"boolean","readOnly":true,"default":false,"description":"**Always false, and stated rather than assumed** (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client decided on 14 August that it does not.\nAll three integration models are entitlement-based — the ticket carries the parking right and the platform pushes a plate or a code. **Pay-per-hour parking unrelated to a ticket runs on the parking system's own POS**, because taking that money here would make the venue an acquirer for parking, with a settlement path and a tax treatment nobody has designed.\nThe field exists so that a future reversal is a value change with a visible blast radius, rather than a silent gap somebody rediscovers.\n"},"vendorSwapTargetDays":{"type":"integer","readOnly":true,"default":5,"description":"**A new parking vendor should take days, not weeks** — Qossai, 14 August. The team has integrated parking APIs before and the architecture is expected to make the next one cheap.\nRecorded as a design constraint rather than a runtime value: **everything vendor-specific lives in `vendorName`, `endpoint` and `credentialRef`**, and the three modes are the adaptor surface (ADR-0012). A vendor needing a fourth mode is the signal this has been violated.\n"},"vendorName":{"type":"string","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response."},"endpoint":{"type":"string","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response."},"credentialRef":{"type":"string","nullable":true,"description":"A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response."},"pushLeadMinutes":{"type":"integer","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. **Too early and the whitelist fills with cars that will not arrive; too late and the guest is at the barrier.**\n"},"accessPointIds":{"type":"array","description":"Where the platform validates its own code, in `none` and `qrHandoff` modes.","items":{"type":"string","format":"uuid"}},"isActive":{"type":"boolean"}}},
"ParkingIntegrationMode": {"type":"string","description":"CF-52, settled 14 August. **Not variations of one thing** — each decides what happens at sale and what a guest presents at the barrier.\n","enum":["none","plateWhitelist","qrHandoff"]},
"PerProductRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the profile row** (`access.admission_rules.per_product_rules`). The rules are read with the profile and a rule is never queried on its own, so a child table would add a join for nothing.\n","items":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"entriesPerDay":{"type":"integer","nullable":true},"minimumGapMinutes":{"type":"integer","nullable":true,"description":"**Anti-passback in minutes rather than a boolean.** A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back over a fence.\n"},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"biometricPolicy":{"allOf":[{"$ref":"#/components/schemas/BiometricPolicy"}],"description":"BL-105, 3.2.9. **The biometric check is a property of the product, not of the venue** — memberships checked, day tickets not. It sits here rather than on the profile because `perProductRules` is already where a ticket type states its own terms, and a profile per product would multiply profiles to carry one flag.\n**Absent means `disabled`**, and `disabled` is the answer for every product until somebody chooses otherwise. **Inert while `VenueSettings.biometrics.isEnabled` is false**, so a rules profile copied to another venue cannot begin capturing faces there.\n"},"maxPassesPerBiometricIdentity":{"type":"integer","nullable":true,"minimum":1,"description":"BL-096, 2.14.7. **The annual-pass quota, keyed to biometric identity.** `enrolFacePass` already answers 409 where a face is on another annual pass; the constant behind that refusal was one and was invisible. **Null means unlimited** and is the answer for every product that is not an annual pass — a quota applied where nobody asked for one turns a family sharing a day ticket into a fraud alert.\n"}}}},
"Queue": {"x-ticvai-persistence":"queue.queue + queue.queue_operating_window","allOf":[{"$ref":"#/components/schemas/CreateQueueRequest"},{"type":"object","required":["id","status","waitingPartyCount"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/QueueStatus"},"statusReason":{"type":"string","nullable":true},"waitingPartyCount":{"type":"integer"},"waitingGuestCount":{"type":"integer"},"currentWaitMinutes":{"type":"integer","nullable":true},"waitTimeSource":{"$ref":"#/components/schemas/WaitTimeSource"},"waitTimeAsOf":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"},"manualWaitExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"},"manualWaitNote":{"type":"string","maxLength":200,"nullable":true,"readOnly":true,"description":"The `note` given with the current manual figure. Cleared when it expires."},"expectedReopenAt":{"type":"string","format":"date-time","nullable":true}}}]},
"QueueDetail": {"x-ticvai-persistence":"queue.queue","allOf":[{"$ref":"#/components/schemas/Queue"},{"type":"object","properties":{"nowServingPartyNumber":{"type":"integer","nullable":true},"lastCalledAt":{"type":"string","format":"date-time","nullable":true},"throughputLastHour":{"type":"integer"},"noShowRatePercent":{"type":"number"},"feed":{"$ref":"#/components/schemas/QueueFeedHealth"}}}]},
"QueueEntryStatus": {"type":"string","enum":["waiting","called","redeemed","expired","noShow","cancelled","released"]},
"QueueFastPass": {"x-ticvai-persistence":"queue.queue","type":"object","description":"**Which Fast Pass entitlements this lane accepts, and how** (decided 29 September, VM close-out; pack 'Access Control Module' p.109, BO-221 Fast Pass & Attraction Access Journey). Fast Pass stays an entitlement owned by Product & Entitlement; this block is the lane's side of it: which products it honours, the return window, a per-guest daily cap and the access points that redeem it. Stored on the queue row. Only meaningful where `kind` is `fastPass` or `fastPassAllocationPercent` is above 0.\n**Four ways into priority, not one** (decided 29 September, build pass; 5.6.7 and 5.6.34). A guest joins this lane as priority when they hold an entitlement from `entitlementProductIds` (VIP, annual pass, premium package), are a member of a tier in `loyaltyTierIds`, qualify for a live promotion in `promotionIds`, or declare an accessibility need where `accessibilityPriority` is on. The first criterion met is recorded on the entry as `WaitingGuest.priorityBasis`. Every criterion is resolved by the server at join time; nothing the request asserts about a tier or a promotion is trusted. All four draw on the same reserved `fastPassAllocationPercent`, so widening who qualifies never widens the share of the ride they take.\n","required":["entitlementProductIds"],"properties":{"entitlementProductIds":{"type":"array","description":"Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need.\n","items":{"type":"string","format":"uuid"}},"loyaltyTierIds":{"type":"array","description":"5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. Read from the guest's own loyalty position at join time, never from the request, so a guest cannot claim a tier they do not hold. Empty: tier grants nothing on this lane.\n","items":{"type":"string","format":"uuid"}},"promotionIds":{"type":"array","description":"5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. A guest qualifies when the promotion's conditions hold for them at join (the evaluation `promotions` already makes for a price), or by presenting its code in `JoinQueueRequest.promotionCode`. A paused or expired promotion grants nothing.\n","items":{"type":"string","format":"uuid"}},"accessibilityPriority":{"type":"boolean","default":false,"description":"5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. **Taken on trust**, because asking for proof at a ride entrance is worse than the occasional abuse; the declaration is on the entry, so the operator at the front sees it (`listQueueEntries`). A venue that wants proof sells or issues an accessibility pass and lists it in `entitlementProductIds` instead. **Not the `accessible` lane**: that is where a guest who cannot stand in a switchback waits; this moves them ahead in the lane they chose.\n"},"returnWindowMinutes":{"type":"integer","minimum":1,"maximum":240,"default":60,"description":"How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan.\n"},"maxPerGuestPerDay":{"type":"integer","minimum":1,"nullable":true,"description":"Fast Pass redemptions one guest may make on this lane per day; null is no cap."},"allowedAccessPointIds":{"type":"array","description":"Access points that redeem Fast Pass for this lane; empty is the queue's own.","items":{"type":"string","format":"uuid"}}}},
"QueueFeed": {"x-ticvai-persistence":"queue.feed","type":"object","required":["id","queueId","adaptor","isEnabled"],"properties":{"id":{"type":"string","format":"uuid"},"queueId":{"type":"string","format":"uuid"},"adaptor":{"$ref":"#/components/schemas/QueueFeedAdaptor"},"adaptorName":{"type":"string","nullable":true,"description":"Named vendor where `adaptor` is `vendorAdaptor`."},"credentialsRef":{"type":"string","nullable":true,"description":"Key vault reference. Credentials are never returned."},"expectedIntervalSeconds":{"type":"integer","default":60,"description":"Beyond this without a reading, the feed is considered quiet."},"isEnabled":{"type":"boolean"},"health":{"allOf":[{"$ref":"#/components/schemas/QueueFeedHealth"}],"readOnly":true,"x-ticvai-persisted":false,"description":"Whether the feed is currently reporting, computed on read — what `listQueueFeeds` promises per row. Ignored on input to `configureQueueFeed`.\n"}}},
"QueueFeedAdaptor": {"type":"string","description":"Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and demonstrated with no vendor at all.\n**`manual` is not an adaptor.** A queue with no enabled feed runs on figures an operator sets through `setWaitTime`, and its `WaitTimeSource` reads `manual` — that is the whole of the manual path, and there is no feed row for it. Transports a screen might list (sensor API, webhook, MQTT, turnstile count, camera) all post to the one inbound API, which is `generic`; anything that needs code of its own to fetch or translate is `vendorAdaptor`.\n","enum":["generic","mock","vendorAdaptor"]},
"QueueFeedHealth": {"x-ticvai-persistence":"none — computed","type":"object","required":["feedId","isHealthy","isQuiet"],"properties":{"feedId":{"type":"string","format":"uuid"},"adaptor":{"$ref":"#/components/schemas/QueueFeedAdaptor"},"isHealthy":{"type":"boolean","description":"**Healthy means the last reading arrived within the feed's expected interval** (decided 28 September, audit R106 (1)): `lastReadingAt` is no older than `expectedIntervalSeconds`. It is the opposite of `isQuiet`, and nothing else (latency, discards) makes a reporting feed unhealthy.\n"},"isQuiet":{"type":"boolean","description":"No reading within the expected interval. The wait time falls back to throughput-derived and is marked stale rather than freezing at the last value.\n"},"lastReadingAt":{"type":"string","format":"date-time","nullable":true},"expectedIntervalSeconds":{"type":"integer","description":"The feed's `expectedIntervalSeconds` — the interval `isQuiet` is judged against, returned here so a health panel does not need the feed row as well.\n"},"readingsLastHour":{"type":"integer"},"discardedLastHour":{"type":"integer","description":"Out-of-order readings rejected in the last hour — rows of `queue.reading` for this feed with `disposition: discardedOutOfOrder`. Duplicates are not counted here: a duplicate has no row, and `submitQueueReading` reports it in its own `duplicates`.\n"}}},
"QueueReading": {"x-ticvai-persistence":"queue.reading","type":"object","required":["id","kind","value","observedAt"],"properties":{"id":{"type":"string","format":"uuid"},"feedId":{"type":"string","format":"uuid","readOnly":true,"description":"The feed that sent it, taken from the `submitQueueReading` body. Per-feed health counts by this, not by queue.\n"},"disposition":{"type":"string","readOnly":true,"enum":["applied","discardedOutOfOrder"],"description":"Set on receipt. A `discardedOutOfOrder` reading is kept so feed health can count it and never moves an estimate.\n"},"kind":{"type":"string","description":"Deliberately narrow. Anything richer would couple the platform to one vendor's model of a queue.\n","enum":["peopleCount","dwellSeconds","throughputPerHour","queueLengthMetres"]},"value":{"type":"number","minimum":0},"confidence":{"type":"number","minimum":0,"maximum":1},"observedAt":{"type":"string","format":"date-time"}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"QueueStatusResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["queue","affectedEntries"],"properties":{"queue":{"$ref":"#/components/schemas/Queue"},"affectedEntries":{"type":"object","description":"What happened to guests already waiting. Closing releases and notifies them — a guest holding a position for a ride that will not run should be told.\n","properties":{"released":{"type":"integer"},"held":{"type":"integer"},"notified":{"type":"integer"}}}}},
"ResolutionCode": {"type":"string","enum":["repaired","partReplaced","adjusted","cleaned","noFaultFound","referredExternal","replaced","deferred"]},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]},
"WaitingGuest": {"x-ticvai-persistence":"queue.entry","type":"object","required":["id","queueId","partyNumber","partySize","status","joinedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. `listMyWaitingGuests` gives it back to a guest who has lost it.\n"},"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"subjectId":{"type":"string","format":"uuid","nullable":true},"partyNumber":{"type":"integer","description":"What the guest sees and what appears on signage."},"partySize":{"type":"integer"},"status":{"$ref":"#/components/schemas/QueueEntryStatus"},"positionInQueue":{"type":"integer","nullable":true},"partiesAhead":{"type":"integer","nullable":true},"estimatedCallAt":{"type":"string","format":"date-time","nullable":true},"isFastPass":{"type":"boolean"},"priorityBasis":{"type":"string","enum":["none","entitlement","loyaltyTier","promotion","accessibility"],"default":"none","description":"Why this party is priority, when it is (decided 29 September, build pass; 5.6.7, 5.6.34): the first `QueueFastPass` criterion met at join, in the order entitlement, loyalty tier, promotion, accessibility. `isFastPass` is true whenever this is not `none`. Kept on the entry so a disputed priority can be explained afterwards.\n"},"priorityTierId":{"type":"string","format":"uuid","nullable":true,"description":"The loyalty tier that granted priority, where `priorityBasis` is `loyaltyTier`."},"priorityPromotionId":{"type":"string","format":"uuid","nullable":true,"description":"The promotion that granted priority, where `priorityBasis` is `promotion`."},"accessibilityNeedDeclared":{"type":"boolean","default":false,"description":"What the party declared at join, shown to the operator at the front."},"entitlementId":{"type":"string","nullable":true},"calledAt":{"type":"string","format":"date-time","nullable":true},"returnWindowEndsAt":{"type":"string","format":"date-time","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"admittedCount":{"type":"integer","nullable":true},"joinedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderDetail": {"x-ticvai-persistence":"maintenance.work_order","allOf":[{"$ref":"#/components/schemas/WorkOrder"},{"type":"object","properties":{"description":{"type":"string","nullable":true},"resolution":{"type":"string","nullable":true},"resolutionCode":{"$ref":"#/components/schemas/ResolutionCode"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"timeEntries":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"pauseReason":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}}},"parts":{"type":"array","items":{"type":"object","properties":{"inventoryItemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"quantity":{"type":"number"},"reservedQuantity":{"type":"number","description":"Still reserved for this work order and not yet issued (M17-02)."},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"labourCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"partsCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"net_cost_amount"},"completedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who called `completeWorkOrder`. **What `verifyWorkOrder` compares against** — the verifier may not be the technician who completed the work, and the assignee is not necessarily that person.\n"},"followUpRequired":{"type":"boolean","default":false},"followUpNote":{"type":"string","maxLength":1000,"nullable":true},"verificationOutcome":{"type":"string","enum":["verified","rejected"],"nullable":true,"description":"The latest `verifyWorkOrder` outcome."},"verificationNote":{"type":"string","maxLength":1000,"nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"verifiedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"cancelReason":{"type":"string","enum":["raisedInError","duplicate","superseded","noLongerRequired"],"nullable":true},"cancelNote":{"type":"string","maxLength":300,"nullable":true},"supersededByWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `cancelWorkOrder` where the reason is `superseded`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"closeOutcome":{"type":"string","enum":["completedAndVerified","notReproducible","supersededByReplacement","noLongerApplicable","duplicate"],"nullable":true},"closeNote":{"type":"string","maxLength":500,"nullable":true},"duplicateOfWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `closeWorkOrder` where the outcome is `duplicate`."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}}]},
"WorkOrderFaultAssessment": {"x-ticvai-persistence":"none — columns on maintenance.work_order","type":"object","description":"What the person raising a fault says about it, which the priority score reads (M17-01).","properties":{"safetyRisk":{"type":"boolean","default":false},"guestImpact":{"type":"string","enum":["none","degraded","closed"],"default":"none"}}},
"WorkOrderKind": {"type":"string","enum":["corrective","planned","inspectionFollowUp","incidentCorrective","improvement"]},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]},
"WorkOrderStatus": {"type":"string","enum":["open","assigned","inProgress","paused","awaitingParts","completed","verified","closed","cancelled"]}
}
```
