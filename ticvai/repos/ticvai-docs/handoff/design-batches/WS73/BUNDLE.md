# WS73 — Waiver, Consent & Digital Form Management board 2

**10 screens · 11 operations · 13 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII`. A control nobody can use must say so,
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
| `CMS-051` | Waiver Operations Command Center | D | 2 | 22 | 6 | 0 | 2 | 4 | — | notStarted (generated) |
| `CMS-052` | Participant Waiver Status & Tracking | D | 2 | 14 | 6 | 0 | 1 | 4 | — | notStarted (generated) |
| `CMS-053` | Digital Signing & Collection Operations | D | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `CMS-054` | Minor, Guardian & Group Consent Management | D | 0 | 12 | 6 | 0 | 1 | 4 | — | notStarted (generated) |
| `CMS-055` | Waiver Verification & Validation Workspace | D | 0 | 40 | 6 | 0 | 1 | 4 | — | notStarted (generated) |
| `CMS-056` | Missing, Expired & Invalid Waiver Management | D | 0 | 20 | 6 | 0 | 2 | 4 | — | notStarted (generated) |
| `CMS-057` | On-Site Waiver & Exception Handling | D | 7 | 0 | 5 | 0 | 0 | 4 | — | notStarted (generated) |
| `CMS-058` | Compliance Evidence, Audit & Waiver Repository | D | 2 | 0 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `CMS-059` | Waiver Analytics, Compliance & Operational Insights | D | 2 | 26 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `CMS-060` | AI Waiver Compliance & Risk Intelligence Center | D | 0 | 0 | 6 | 0 | 0 | 4 | — | notStarted (generated) |

## Thin screens in this batch

**CMS-056, CMS-058, CMS-060 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-051` Waiver Operations Command Center

**Provide Operations, Customer Service, Compliance and venue teams with a real-time overview of waiver completion across upcoming and active activities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-051 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/waiver-operations-command-center-cms-051` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Waiver completion across upcoming and active activities for operations, customer service, compliance and venue teams: required, completed, pending, partial, expiring, invalid, rejected, guardian pending, upcoming participants missing a waiver, access blocked, manual exceptions, completion rate.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search waiver operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by brand, venue, event, product, waiver, date and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | picker: choose a brand | — | — | `listWaiver` ?brandId |
| Event | picker: choose an event | — | — | `listWaiver` ?eventId |
| Product | picker: choose a product | — | — | `listWaiver` ?productId |
| Form | picker: choose a form | — | — | `listWaiver` ?formId |
| From | date and time picker | — | — | `listWaiver` ?from |
| To | date and time picker | — | — | `listWaiver` ?to |
| Status | select | — | Not assigned · Assigned · Sent · Opened · In progress · Completed · Verified · Rejected · Expired · Superseded | `listWaiver` ?status |
| Participant type | segmented control | — | Adult · Minor | `listWaiver` ?participantType |
| Booking channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listWaiver` ?bookingChannel |
| Breakdown by | select | Venue | Venue · Event · Product · Activity · Group · Booking · Waiver type | `listWaiver` ?breakdownBy |

#### Outputs: what the screen shows and produces

**Shown**

**Waivers Required** (metric tile)

**Completed** (metric tile)

**Pending** (metric tile)

**Partially Completed** (metric tile)

**Expiring** (metric tile)

**Invalid** (metric tile)

**Rejected** (metric tile)

**Guardian Consent Pending** (metric tile)

**Upcoming Participants Missing Waiver** (metric tile)

**Access Blocked** (metric tile)

**Manual Exceptions** (metric tile)

**Completion Rate** (metric tile)

**Every waiver operations** (data table, from `listWaiver`)

| Shows | Format | Notes |
|---|---|---|
| Event activity | text | The event or activity name. |
| Venue | text | The venue name. |
| Date time | 1 Oct 2026, 14:30 | When the performance starts. |
| Participants | 1,234 | — |
| Waivers required | 1,234 | — |
| Completed | 1,234 | — |
| Missing | 1,234 | — |
| Completion | 1,234.5 | The performance's waiver readiness (the pack's Readiness Score). |
| Guardian pending | 1,234 | — |
| Exceptions | 1,234 | — |
| Operational risk | chip: Ready, Attention, Critical | `critical` when a missing requirement would block admission; `attention` when anything is missing; otherwise `ready`. |

**The selected waiver operations** (detail panel): The pack groups this record's detail under its own headings: “Display by”, “Activity Status”, “Youth Attentio”, “Climbing”, “Session”.

| Shows | Format | Notes |
|---|---|---|
| Event activity | text | The event or activity name. |
| Venue | text | The venue name. |
| Date time | 1 Oct 2026, 14:30 | When the performance starts. |
| Participants | 1,234 | — |
| Waivers required | 1,234 | — |
| Completed | 1,234 | — |
| Missing | 1,234 | — |
| Completion | 1,234.5 | The performance's waiver readiness (the pack's Readiness Score). |
| Guardian pending | 1,234 | — |
| Exceptions | 1,234 | — |
| Operational risk | chip: Ready, Attention, Critical | `critical` when a missing requirement would block admission; `attention` when anything is missing; otherwise `ready`. |

**Data it reads**: `listWaiver` (onLoad, Waiver Operations Command Center)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-052` Participant Waiver Status & Tracking: *Works in Participant Waiver Status & Tracking*; calls `listWaiver`
- → `CMS-053` Digital Signing & Collection Operations: *Works in Digital Signing & Collection Operations*; calls `listWaiver`
- → `CMS-054` Minor, Guardian & Group Consent Management: *Works in Minor, Guardian & Group Consent Management*; calls `listWaiver`
- → `CMS-055` Waiver Verification & Validation Workspace: *Works in Waiver Verification & Validation Workspace*; calls `listWaiver`
- → `CMS-056` Missing, Expired & Invalid Waiver Management: *Works in Missing, Expired & Invalid Waiver Management*; calls `listWaiver`
- → `CMS-057` On-Site Waiver & Exception Handling: *Works in On-Site Waiver & Exception Handling*; calls `listWaiver`
- → `CMS-058` Compliance Evidence, Audit & Waiver Repository: *Works in Compliance Evidence, Audit & Waiver Repository*; calls `listWaiver`
- → `CMS-059` Waiver Analytics, Compliance & Operational Insights: *Works in Waiver Analytics, Compliance & Operational Insights*; calls `listWaiver`
- → `CMS-060` AI Waiver Compliance & Risk Intelligence Center: *Works in AI Waiver Compliance & Risk Intelligence Center*; calls `listWaiver`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the waiver operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `BO-844`: Same object.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  required: 340
  completed: 291
  pending: 37
  guardianPending: 9
  accessBlockedToday: 4
  completion: 86%
```

#### Permissions

- `listWaiver` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-051` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-051`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 1: Opens Waiver Operations Command Center → Provide Operations, Customer Service, Compliance and venue teams with a real-time overview of waiver completion across upcoming and active activities.
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F182 branch at step 1 (expected): when Nothing has been set up on Waiver Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F182 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-001`, `CMS-052`, `CMS-053`, `CMS-054`, `CMS-055`, `CMS-056`, `CMS-057`, `CMS-058`, `CMS-059`, `CMS-060`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-052` Participant Waiver Status & Tracking

**Provide a detailed operational record of the waiver requirements for each participant.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-052 |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/participant-waiver-status-tracking-cms-052` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** For each participant on a booking, every waiver they need and its status, with delivery channel (email, WhatsApp, SMS) and minor or guardian handling. PII-permissioned.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search participant waiver status | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by participant, booking, ticket, email, mobile, group and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Q | text field | — | max length 200 | `listParticipantWaiverStatus` ?q |
| Participant subject | picker: choose a participant subject | — | — | `listParticipantWaiverStatus` ?participantSubjectId |
| Order | picker: choose an order | — | — | `listParticipantWaiverStatus` ?orderId |
| Ticket | picker: choose a ticket | — | — | `listParticipantWaiverStatus` ?ticketId |
| Group booking | picker: choose a group booking | — | — | `listParticipantWaiverStatus` ?groupBookingId |
| Form | picker: choose a form | — | — | `listParticipantWaiverStatus` ?formId |
| Performance | picker: choose a performance | — | — | `listParticipantWaiverStatus` ?performanceId |
| Visit from | date and time picker | — | — | `listParticipantWaiverStatus` ?visitFrom |
| Visit to | date and time picker | — | — | `listParticipantWaiverStatus` ?visitTo |
| Completion status | segmented control | — | Ready · Not ready · Exception approved | `listParticipantWaiverStatus` ?completionStatus |

#### Outputs: what the screen shows and produces

**Shown**

**Every participant waiver status** (data table, from `listParticipantWaiverStatus`)

| Shows | Format | Notes |
|---|---|---|
| Participant | text | The participant's name. |
| Booking | the name it points at, never the id | The order id. |
| Ticket | the name it points at, never the id | The ticket (entitlement) id. |
| Visit date | 1 Oct 2026, 14:30 | — |
| Age category | chip: Adult, Minor | From the participant's date of birth against the age of majority configured for the venue's jurisdiction (no shipped default). |
| Completion status | chip: Ready, Not ready, Exception approved | `ready` when every mandatory requirement is completed or verified; `exceptionApproved` when the gap is covered by an approved exception. |

**The selected participant waiver status** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Participant | text | The participant's name. |
| Customer purchaser | grouped details | Who bought the booking; may differ from the participant. |
| Booking | the name it points at, never the id | The order id. |
| Ticket | the name it points at, never the id | The ticket (entitlement) id. |
| Product | grouped details | — |
| Visit date | 1 Oct 2026, 14:30 | — |
| Age category | chip: Adult, Minor | From the participant's date of birth against the age of majority configured for the venue's jurisdiction (no shipped default). |
| Completion status | chip: Ready, Not ready, Exception approved | `ready` when every mandatory requirement is completed or verified; `exceptionApproved` when the gap is covered by an approved exception. |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Send Waiver, Resend, Open, View, Verify, Request Correction, Replace Signatory, Record Exception, View Audit History. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listParticipantWaiverStatus` (onLoad, Participant Waiver Status & Tracking)

**Where the user goes next**

- → `CMS-051` Waiver Operations Command Center: *Returns to the board's landing screen*; calls `listParticipantWaiverStatus`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The participant waiver status list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the participant waiver status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No participant waiver status yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the participant waiver status are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row: ORD-55821 - Layla Haddad (9) - Water activity v3 - guardian pending - link sent WhatsApp 1 Oct
```

#### Permissions

- `listParticipantWaiverStatus` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-052` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-052`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 2: Works in Participant Waiver Status & Tracking → Provide a detailed operational record of the waiver requirements for each participant.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-052?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-051`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-053` Digital Signing & Collection Operations

**Manage the actual distribution and completion of digital waivers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-053 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/digital-signing-collection-operations-cms-053` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Email Link, SMS Link, WhatsApp where integrated, POS, Staff-Assisted Device. Each needs an operation, or … Contract gap recorded 2 October 2026 (CHG-WIR-007): No operation sends or resends a waiver signing link (email, SMS, WhatsApp, QR).

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** How waiver links go out and come back: by method (email, SMS, WhatsApp, POS, staff-assisted device) and by stage of signing. These are transactional messages.

**Known correction pending (do not draw the wrong version)**

- **Delivery methods are buttons, but no operation sends a link.** Why: Sending or resending a waiver link has no operation. *(source: contracts/satellite/marketing-crm.yaml#listDigitalSigningCollection; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `listDigitalSigningCollection` ?formId |
| Performance | picker: choose a performance | — | — | `listDigitalSigningCollection` ?performanceId |
| Group booking | picker: choose a group booking | — | — | `listDigitalSigningCollection` ?groupBookingId |
| Order | picker: choose an order | — | — | `listDigitalSigningCollection` ?orderId |
| Method | select | — | Email · SMS · Whatsapp · Guest web · Guest app · Group portal · QR code · POS · Kiosk · Staff assisted device | `listDigitalSigningCollection` ?method |
| From | date and time picker | — | — | `listDigitalSigningCollection` ?from |
| To | date and time picker | — | — | `listDigitalSigningCollection` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every digital signing collection** (data table, from `listDigitalSigningCollection`)

| Shows | Format | Notes |
|---|---|---|
| Sent | 1,234 | — |
| Delivered | 1,234 | — |
| Opened | 1,234 | — |
| Started | 1,234 | — |
| Completed | 1,234 | — |
| Failed | 1,234 | Links whose message could not be delivered on any channel. |
| Expired links | 1,234 | Links that expired unused, or were refused because already used. |

**The selected digital signing collection** (detail panel): The pack groups this record's detail under its own headings: “Link Issued”, “For groups”, “Waiver Completed”, “Security”.

| Shows | Format | Notes |
|---|---|---|
| Sent | 1,234 | — |
| Delivered | 1,234 | — |
| Opened | 1,234 | — |
| Started | 1,234 | — |
| Completed | 1,234 | — |
| Failed | 1,234 | Links whose message could not be delivered on any channel. |
| Expired links | 1,234 | Links that expired unused, or were refused because already used. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Email Link (primary button) | navigation or local | — | — | — | — |
| SMS Link (secondary button) | navigation or local | — | — | — | — |
| WhatsApp where integrated (secondary button) | navigation or local | — | — | — | — |
| POS (secondary button) | navigation or local | — | — | — | — |
| Staff-Assisted Device (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listDigitalSigningCollection` (onLoad, Digital Signing & Collection Operations)

**Where the user goes next**

- → `CMS-051` Waiver Operations Command Center: *Returns to the board's landing screen*; calls `listDigitalSigningCollection`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital signing collection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital signing collection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital signing collection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital signing collection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
funnel:
  sent: 120
  opened: 96
  started: 80
  signed: 71
```

#### Permissions

- `listDigitalSigningCollection` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-053` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-053`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 4: Works in Digital Signing & Collection Operations → Manage the actual distribution and completion of digital waivers.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-053?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Email Link, SMS Link, WhatsApp where integrated, POS, Staff-Assisted Device.
- [ ] Every transition is wired: `CMS-051`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-054` Minor, Guardian & Group Consent Management

**Manage complex consent relationships for minors and organized groups. This screen is particularly important for camps, academies, schools, family attractions and youth activities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-054 |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/minor-guardian-group-consent-management-cms-054` |

**What the spec says about it.** **Minors (decided by Chinmay, 2 October 2026; DEC-237, superseding the GST-069 default):** a child is enrolled or consents through a guardian on the venue's consent form; the minor age is set per country (`RegionSettings.minorAgeThreshold`) and the venue can switch minors off (`VenueSettings.biometrics.allowMinors`); the guardian links this screen sends go to that form (DEC-549) (CHG-SGU-004).

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Send Guardian Links, Notify Group Leader, Export Missing List. Each needs an operation, or needs removing …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Minors and groups: each minor's guardians and what each may do, and the group they travel with (camps, academies, schools, family attractions). Missing guardian consents are chased.

**Known correction pending (do not draw the wrong version)**

- **Send Guardian Links, Notify Group Leader and Export Missing List have no operation.** Why: Read-only; the chasing actions cannot run. *(source: contracts/satellite/marketing-crm.yaml#listMinorGuardianGroup; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Group booking | picker: choose a group booking | — | — | `listMinorGuardianGroup` ?groupBookingId |
| Guardian subject | picker: choose a guardian subject | — | — | `listMinorGuardianGroup` ?guardianSubjectId |
| Order | picker: choose an order | — | — | `listMinorGuardianGroup` ?orderId |
| Performance | picker: choose a performance | — | — | `listMinorGuardianGroup` ?performanceId |
| Consent status | segmented control | — | Complete · Pending · Rejected | `listMinorGuardianGroup` ?consentStatus |
| Visit from | date and time picker | — | — | `listMinorGuardianGroup` ?visitFrom |
| Visit to | date and time picker | — | — | `listMinorGuardianGroup` ?visitTo |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every minor guardian group** (data table, from `listMinorGuardianGroup`)

| Shows | Format | Notes |
|---|---|---|
| Organization | text | The school, club or company. |
| Group leader | grouped details | — |
| Contact | text | The leader's email or mobile. |
| Group booking | the name it points at, never the id | The group's order id. |
| Responsibility | chip: Coordinator only, Supervising adult, Organisation representative | `organisationRepresentative` when the leader's `GuestRelationship` (kind `groupLeader`) carries `signWaiver`; `supervisingAdult` when the … |
| Permitted actions | list or chips (count when long) | What the leader may do for this group under the form's signatory rule. |

**The selected minor guardian group** (detail panel): The pack groups this record's detail under its own headings: “Multiple Children”.

| Shows | Format | Notes |
|---|---|---|
| Organization | text | The school, club or company. |
| Group leader | grouped details | — |
| Contact | text | The leader's email or mobile. |
| Group booking | the name it points at, never the id | The group's order id. |
| Responsibility | chip: Coordinator only, Supervising adult, Organisation representative | `organisationRepresentative` when the leader's `GuestRelationship` (kind `groupLeader`) carries `signWaiver`; `supervisingAdult` when the … |
| Permitted actions | list or chips (count when long) | What the leader may do for this group under the form's signatory rule. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send Guardian Links (primary button) | navigation or local | — | — | — | — |
| Notify Group Leader (secondary button) | navigation or local | — | — | — | — |
| Export Missing List (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listMinorGuardianGroup` (onLoad, Minor, Guardian & Group Consent Management)

**Where the user goes next**

- → `CMS-051` Waiver Operations Command Center: *Returns to the board's landing screen*; calls `listMinorGuardianGroup`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The minor guardian group list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the minor guardian group untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No minor guardian group yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the minor guardian group are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row: Saeed Al Suwaidi (6) - guardian Khalid Al Suwaidi (may book, sign) - Al Noor school trip - consent pending
```

#### Permissions

- `listMinorGuardianGroup` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-054` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-054`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 6: Works in Minor, Guardian & Group Consent Management → Manage complex consent relationships for minors and organized groups. This screen is particularly important for camps, academies, schools, family attractions and youth activities.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-054?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send Guardian Links, Notify Group Leader, Export Missing List.
- [ ] Every transition is wired: `CMS-051`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-055` Waiver Verification & Validation Workspace

**Provide authorized staff with a controlled process for reviewing waiver submissions that require verification.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-055 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW_PII` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/waiver-verification-validation-workspace-cms-055` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Staff review submissions that need verification (ID, guardian authority, signature validity). Verified is refused while an automatic check fails or no signature is present; every decision records who and why.

**Fixed on main** (the package already carries these; draw what it says): The list is bound to setWaiverVerificationValidation (a write). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Automatically validated · Pending manual verification · Verified · Correction required · Rejected · Escalated | `listWaiverVerificationQueue` ?status |
| Risk | segmented control | — | Low · Medium · High | `listWaiverVerificationQueue` ?risk |
| Form | picker: choose a form | — | — | `listWaiverVerificationQueue` ?formId |
| Performance | picker: choose a performance | — | — | `listWaiverVerificationQueue` ?performanceId |
| Order | picker: choose an order | — | — | `listWaiverVerificationQueue` ?orderId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every waiver verification validation** (data table, from `setWaiverVerificationValidation`)

| Shows | Format | Notes |
|---|---|---|
| Submission | the name it points at, never the id | — |
| Participant | grouped details | — |
| Waiver | grouped details | — |
| Version | 1,234 | The form version signed. |
| Booking | the name it points at, never the id | — |
| Signatory | grouped details | — |
| Submitted | 1 Oct 2026, 14:30 | `FormSubmission.submittedAt`, the device time of signing. |
| Verification reason | chip: Configured manual review, Automatic check failed, Minor signed as adult, Guardian … | — |
| Risk | chip: Low, Medium, High | — |
| Status | chip: Automatically validated, Pending manual verification, Verified, Correction … | — |

**Submissions to verify** (data table, from `listWaiverVerificationQueue`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Submission | the name it points at, never the id | — |
| Requirement | the name it points at, never the id | — |
| Participant | grouped details | — |
| Subject | the name it points at, never the id | — |
| Name | text | — |
| Age | 1,234 | — |
| Waiver | grouped details | — |
| Form | the name it points at, never the id | — |
| Name | text | — |
| Booking | the name it points at, never the id | — |
| Signatory | grouped details | — |
| Subject | the name it points at, never the id | — |
| Name | text | — |
| Signatory type | chip: Participant, Guardian, Organisation representative | — |
| Submitted | 1 Oct 2026, 14:30 | `FormSubmission.submittedAt`, the device time of signing. |
| Verification reason | chip: Configured manual review, Automatic check failed, Minor signed as adult, Guardian … | — |
| Risk | chip: Low, Medium, High | — |
| Status | chip: Automatically validated, Pending manual verification, Verified, Correction … | — |
| Checks | grouped details | Each check the form's configuration applies; null when it does not apply. The first seven are evaluated by the server, the last three … |

**The selected waiver verification validation** (detail panel): The pack groups this record's detail under its own headings: “Reviewer Actions”, “Human Governance”.

| Shows | Format | Notes |
|---|---|---|
| Submission | the name it points at, never the id | — |
| Participant | grouped details | — |
| Waiver | grouped details | — |
| Version | 1,234 | The form version signed. |
| Booking | the name it points at, never the id | — |
| Signatory | grouped details | — |
| Submitted | 1 Oct 2026, 14:30 | `FormSubmission.submittedAt`, the device time of signing. |
| Verification reason | chip: Configured manual review, Automatic check failed, Minor signed as adult, Guardian … | — |
| Risk | chip: Low, Medium, High | — |
| Status | chip: Automatically validated, Pending manual verification, Verified, Correction … | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listWaiverVerificationQueue` (onLoad, Waiver submissions awaiting or given verification)

**Where the user goes next**

- → `CMS-051` Waiver Operations Command Center: *Returns to the board's landing screen*; calls `setWaiverVerificationValidation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver verification validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver verification validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver verification validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the waiver verification validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.; 422 `verified` while an automatic check fails or no signature is present (`checksFailing`), or a required `note` or `escalatedTo` is missing (`reasonRequired`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
submission: SUB-88412 - guardian authority unverified - reviewer Hana Yousef - rejected (relationship not on file)
```

#### Permissions

- `setWaiverVerificationValidation` → `GUEST_MANAGE` (configure) · staff
- `listWaiverVerificationQueue` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-055` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-055`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 8: Works in Waiver Verification & Validation Workspace → Provide authorized staff with a controlled process for reviewing waiver submissions that require verification.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-055?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `CMS-051`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW_PII`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-056` Missing, Expired & Invalid Waiver Management

**Provide a dedicated exception workspace for waiver requirements preventing operational readiness.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-056 |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/missing-expired-invalid-waiver-management-cms-056` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The exception queue of waiver requirements standing between a participant and a ready visit (missing, expired, invalid, wrong version) for activities not yet ended, soonest first.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Problem | select | — | Missing waiver · Incomplete · Missing signature · Guardian missing · Expired · Wrong version · Rejected · Verification failed · Link expired · Participant mismatch · Correction required | `listMissingExpiredInvalid` ?problem |
| Status | radio group | — | Open · In progress · Awaiting customer · Resolved · Exception approved | `listMissingExpiredInvalid` ?status |
| Access impact | radio group | — | None · Ticket download blocked · Activation blocked · Check in blocked · Access blocked | `listMissingExpiredInvalid` ?accessImpact |
| Owner staff | picker: choose an owner staff | — | — | `listMissingExpiredInvalid` ?ownerStaffId |
| Performance | picker: choose a performance | — | — | `listMissingExpiredInvalid` ?performanceId |
| Group booking | picker: choose a group booking | — | — | `listMissingExpiredInvalid` ?groupBookingId |
| Visit from | date and time picker | — | — | `listMissingExpiredInvalid` ?visitFrom |
| Visit to | date and time picker | — | — | `listMissingExpiredInvalid` ?visitTo |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every missing expired invalid** (data table, from `listMissingExpiredInvalid`)

| Shows | Format | Notes |
|---|---|---|
| Participant | grouped details | — |
| Booking | the name it points at, never the id | — |
| Event | grouped details | — |
| Visit time | 1 Oct 2026, 14:30 | — |
| Waiver | grouped details | — |
| Problem | chip: Missing waiver, Incomplete, Missing signature, Guardian missing, Expired, Wrong … | — |
| Time remaining seconds | 1,234 | Seconds until the activity starts; negative once it has started. |
| Access impact | chip: None, Ticket download blocked, Activation blocked, Check in blocked, Access blocked | — |
| Owner | grouped details | — |
| Status | chip: Open, In progress, Awaiting customer, Resolved, Exception approved | — |

**The selected missing expired invalid** (detail panel): The pack groups this record's detail under its own headings: “Include”, “Highest priority should consider”, “Authorized staff can”.

| Shows | Format | Notes |
|---|---|---|
| Participant | grouped details | — |
| Booking | the name it points at, never the id | — |
| Event | grouped details | — |
| Visit time | 1 Oct 2026, 14:30 | — |
| Waiver | grouped details | — |
| Problem | chip: Missing waiver, Incomplete, Missing signature, Guardian missing, Expired, Wrong … | — |
| Time remaining seconds | 1,234 | Seconds until the activity starts; negative once it has started. |
| Access impact | chip: None, Ticket download blocked, Activation blocked, Check in blocked, Access blocked | — |
| Owner | grouped details | — |
| Status | chip: Open, In progress, Awaiting customer, Resolved, Exception approved | — |

**Data it reads**: `listMissingExpiredInvalid` (onLoad, Missing, Expired & Invalid Waiver Management)

**Where the user goes next**

- → `CMS-051` Waiver Operations Command Center: *Returns to the board's landing screen*; calls `listMissingExpiredInvalid`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The missing expired invalid list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the missing expired invalid untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No missing expired invalid yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the missing expired invalid are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row: Deep Dive 14:00 today - Omar Haddad - waiver v2 signed, v3 required - re-sign needed
```

#### Permissions

- `listMissingExpiredInvalid` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*
- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-056` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-056`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 10: Works in Missing, Expired & Invalid Waiver Management → Provide a dedicated exception workspace for waiver requirements preventing operational readiness.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-056?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-051`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-057` On-Site Waiver & Exception Handling

**Support customers who arrive at the venue without completing required waivers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-057 |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Depending on configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/on-site-waiver-exception-handling-cms-057` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-007): No write records an on-site waiver exception with its reason.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Guests arriving without a completed waiver: look them up by ticket, QR, booking or name and resolve on site (send a mobile link, show a QR, complete on a kiosk or staff tablet, contact the guardian, re-sign an updated version, or request a supervisor exception).

**Known correction pending (do not draw the wrong version)**

- **The resolution options are select fields and only a lookup read is declared.** Why: They are actions; the supervisor exception needs a write with reason. *(source: contracts/satellite/marketing-crm.yaml#listSiteWaiverException; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Send Mobile Link | select field | — | — | — | — | — | — |
| Display QR for Customer | text field | — | — | — | — | — | — |
| Complete on Kiosk | select field | — | — | — | — | — | — |
| Complete on Staff Tablet | text field | — | — | — | — | — | — |
| Contact Guardian | select field | — | — | — | — | — | — |
| Re-Sign Updated Waiver | select field | — | — | — | — | — | — |
| Request Supervisor Exception | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Ticket | picker: choose a ticket | — | — | `listSiteWaiverException` ?ticketId |
| Media code | text area | — | max length 512 | `listSiteWaiverException` ?mediaCode |
| Order | picker: choose an order | — | — | `listSiteWaiverException` ?orderId |
| Customer subject | picker: choose a customer subject | — | — | `listSiteWaiverException` ?customerSubjectId |
| Participant subject | picker: choose a participant subject | — | — | `listSiteWaiverException` ?participantSubjectId |
| Group booking | picker: choose a group booking | — | — | `listSiteWaiverException` ?groupBookingId |
| Membership | picker: choose a membership | — | — | `listSiteWaiverException` ?membershipId |

#### Outputs: what the screen shows and produces

**Data it reads**: `listSiteWaiverException` (onLoad, On-Site Waiver & Exception Handling)

**Where the user goes next**

- → `CMS-051` Waiver Operations Command Center: *Returns to the board's landing screen*; calls `listSiteWaiverException`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The on-site waiver exception configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the on-site waiver exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No on-site waiver exception configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
lookup: Ticket TK-3381 - Layla Haddad (9) - guardian not present - Contact guardian by WhatsApp
```

#### Permissions

- `listSiteWaiverException` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-057` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-057`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 12: Works in On-Site Waiver & Exception Handling → Support customers who arrive at the venue without completing required waivers.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-057?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-051`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-058` Compliance Evidence, Audit & Waiver Repository

**Maintain the complete evidentiary record of every waiver and consent transaction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-058 |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/compliance-evidence-audit-waiver-repository-cms-058` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The evidentiary record of every waiver signed: what was presented, answered, acknowledged and signed, by whom, on what device and channel, the content hash, and what happened afterwards. The exact version text signed is always retrievable.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search compliance evidence audit | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by participant, customer, ticket, booking, event, waiver and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Participant subject | picker: choose a participant subject | — | — | `listComplianceEvidenceWaiver` ?participantSubjectId |
| Customer subject | picker: choose a customer subject | — | — | `listComplianceEvidenceWaiver` ?customerSubjectId |
| Signatory subject | picker: choose a signatory subject | — | — | `listComplianceEvidenceWaiver` ?signatorySubjectId |
| Ticket | picker: choose a ticket | — | — | `listComplianceEvidenceWaiver` ?ticketId |
| Order | picker: choose an order | — | — | `listComplianceEvidenceWaiver` ?orderId |
| Event | picker: choose an event | — | — | `listComplianceEvidenceWaiver` ?eventId |
| Form | picker: choose a form | — | — | `listComplianceEvidenceWaiver` ?formId |
| Form version | number field | — | min 1 | `listComplianceEvidenceWaiver` ?formVersion |
| From | date and time picker | — | — | `listComplianceEvidenceWaiver` ?from |
| To | date and time picker | — | — | `listComplianceEvidenceWaiver` ?to |

#### Outputs: what the screen shows and produces

**Data it reads**: `listComplianceEvidenceWaiver` (onLoad, Compliance Evidence, Audit & Waiver Repository)

**Where the user goes next**

- → `CMS-051` Waiver Operations Command Center: *Returns to the board's landing screen*; calls `listComplianceEvidenceWaiver`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The compliance evidence audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the compliance evidence audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No compliance evidence audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the compliance evidence audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `BO-853`: Same repository.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
evidence: Water activity v3 - Fatima Al Mansoori - signed 26 Sep 2026 10:12 GST - kiosk 4 - hash 9f2c...e1
```

#### Permissions

- `listComplianceEvidenceWaiver` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-058` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-058`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 14: Works in Compliance Evidence, Audit & Waiver Repository → Maintain the complete evidentiary record of every waiver and consent transaction.
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-058?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-051`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-059` Waiver Analytics, Compliance & Operational Insights

**Analyze waiver completion, customer behavior and operational effectiveness.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-059 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/waiver-analytics-compliance-operational-insights-cms-059` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Waiver completion and the signing funnel, where people abandon, which reminder timing works, and the on-site workload waivers cause.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search waiver analytics compliance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by waiver, version, product, event, venue, customer type and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `listWaiverComplianceOperational` ?formId |
| Form version | number field | — | min 1 | `listWaiverComplianceOperational` ?formVersion |
| Product | picker: choose a product | — | — | `listWaiverComplianceOperational` ?productId |
| Event | picker: choose an event | — | — | `listWaiverComplianceOperational` ?eventId |
| Customer type | segmented control | — | Individual · Group · Member | `listWaiverComplianceOperational` ?customerType |
| Participant type | segmented control | — | Adult · Minor | `listWaiverComplianceOperational` ?participantType |
| Channel | select | — | Email · SMS · Whatsapp · Guest web · Guest app · Group portal · QR code · POS · Kiosk · Staff assisted device | `listWaiverComplianceOperational` ?channel |
| Language | text field | — | max length 10 | `listWaiverComplianceOperational` ?language |
| Group booking | picker: choose a group booking | — | — | `listWaiverComplianceOperational` ?groupBookingId |
| From | date and time picker | — | — | `listWaiverComplianceOperational` ?from |
| To | date and time picker | — | — | `listWaiverComplianceOperational` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Every waiver analytics compliance** (data table, from `listWaiverComplianceOperational`)

| Shows | Format | Notes |
|---|---|---|
| Waivers assigned | 1,234 | — |
| Completion rate | 12.5% | — |
| Pre arrival completion | 1,234 | Requirements completed before the participant arrived. |
| On site completion | 1,234 | Requirements completed on site (kiosk, POS, staff-assisted device, on-site QR). |
| Average completion seconds | 1,234 | Mean time from opening the link to submitting. |
| Guardian completion rate | 12.5% | — |
| Rejection rate | 12.5% | — |
| Exception rate | 12.5% | — |
| Access blocks | 1,234 | Access attempts refused with `waiverRequired`. |
| Reminder effectiveness | list or chips (count when long) | Completion after each reminder, by how long before the activity it was sent. |
| Check in delays | 1,234 | Check-ins held while a waiver was completed or resolved on site. |
| Staff interventions | 1,234 | Staff actions taken on requirements (sends, corrections, verifications, exceptions). |
| Exceptions | 1,234 | Exceptions approved. |

**The selected waiver analytics compliance** (detail panel): The pack groups this record's detail under its own headings: “Visualize”, “Abandonment Analysis”, “Reminder Analysis”.

| Shows | Format | Notes |
|---|---|---|
| Waivers assigned | 1,234 | — |
| Completion rate | 12.5% | — |
| Pre arrival completion | 1,234 | Requirements completed before the participant arrived. |
| On site completion | 1,234 | Requirements completed on site (kiosk, POS, staff-assisted device, on-site QR). |
| Average completion seconds | 1,234 | Mean time from opening the link to submitting. |
| Guardian completion rate | 12.5% | — |
| Rejection rate | 12.5% | — |
| Exception rate | 12.5% | — |
| Access blocks | 1,234 | Access attempts refused with `waiverRequired`. |
| Reminder effectiveness | list or chips (count when long) | Completion after each reminder, by how long before the activity it was sent. |
| Check in delays | 1,234 | Check-ins held while a waiver was completed or resolved on site. |
| Staff interventions | 1,234 | Staff actions taken on requirements (sends, corrections, verifications, exceptions). |
| Exceptions | 1,234 | Exceptions approved. |

**Data it reads**: `listWaiverComplianceOperational` (onLoad, Waiver Analytics, Compliance & Operational Insights)

**Where the user goes next**

- → `CMS-051` Waiver Operations Command Center: *Returns to the board's landing screen*; calls `listWaiverComplianceOperational`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver analytics compliance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver analytics compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver analytics compliance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the waiver analytics compliance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
insight: Reminder at T-24h converts 3x better than T-7d; 18% of on-site desk time is waiver completion
```

#### Permissions

- `listWaiverComplianceOperational` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-059` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-059`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 16: Works in Waiver Analytics, Compliance & Operational Insights → Analyze waiver completion, customer behavior and operational effectiveness.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-059?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-051`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-060` AI Waiver Compliance & Risk Intelligence Center

**Provide an AI intelligence layer across the complete waiver lifecycle. This should combine Board 1 configuration data + Board 2 operational data.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-060 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/ai-waiver-compliance-risk-intelligence-center-cms-060` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** AI across the waiver lifecycle: configuration risks (products without a waiver, versions missing Arabic), operational risks (tomorrow's activities with low completion), with recommendations a person acts on.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Forecast date | date picker | — | — | `listWaiverComplianceRisk` ?forecastDate |
| Category | radio group | — | Operational · Configuration · Version · Customer experience | `listWaiverComplianceRisk` ?category |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** “Which waiver version generates the most corrections?”. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listWaiverComplianceRisk` (onLoad, AI Waiver Compliance & Risk Intelligence Center)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver compliance risk list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver compliance risk untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver compliance risk yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the waiver compliance risk are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
risk: Tomorrow's Deep Dive 10:00 - 40% completion forecast - recommend extra reminder at 18:00 (AI)
```

#### Permissions

- `listWaiverComplianceRisk` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-060` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-060`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 2
- Flow F182 *Waiver, Consent & Digital Form Management board 2: Waiver Operations Command …*, step 18: Works in AI Waiver Compliance & Risk Intelligence Center → Provide an AI intelligence layer across the complete waiver lifecycle. This should combine Board 1 configuration data + Board 2 operational data.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-060?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listComplianceEvidenceWaiver": {"method":"GET","path":"/compliance-evidence-waiver","contract":"marketing-crm","summary":"Compliance Evidence, Audit & Waiver Repository","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"participantSubjectId","in":"query","required":false},{"name":"customerSubjectId","in":"query","required":false},{"name":"signatorySubjectId","in":"query","required":false},{"name":"ticketId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"formId","in":"query","required":false},{"name":"formVersion","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDigitalSigningCollection": {"method":"GET","path":"/digital-signing-collection","contract":"marketing-crm","summary":"Digital Signing & Collection Operations","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"formId","in":"query","required":false},{"name":"performanceId","in":"query","required":false},{"name":"groupBookingId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"method","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"DigitalSigningCollectionOperationsView"},
"listMinorGuardianGroup": {"method":"GET","path":"/minor-guardian-group","contract":"marketing-crm","summary":"Minor, Guardian & Group Consent Management","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"groupBookingId","in":"query","required":false},{"name":"guardianSubjectId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"performanceId","in":"query","required":false},{"name":"consentStatus","in":"query","required":false},{"name":"visitFrom","in":"query","required":false},{"name":"visitTo","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMissingExpiredInvalid": {"method":"GET","path":"/missing-expired-invalid","contract":"marketing-crm","summary":"Missing, Expired & Invalid Waiver Management","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"problem","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"accessImpact","in":"query","required":false},{"name":"ownerStaffId","in":"query","required":false},{"name":"performanceId","in":"query","required":false},{"name":"groupBookingId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"visitFrom","in":"query","required":false},{"name":"visitTo","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listParticipantWaiverStatus": {"method":"GET","path":"/participant-waiver-statu","contract":"marketing-crm","summary":"Participant Waiver Status & Tracking","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"q","in":"query","required":false},{"name":"participantSubjectId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"ticketId","in":"query","required":false},{"name":"groupBookingId","in":"query","required":false},{"name":"formId","in":"query","required":false},{"name":"performanceId","in":"query","required":false},{"name":"visitFrom","in":"query","required":false},{"name":"visitTo","in":"query","required":false},{"name":"completionStatus","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSiteWaiverException": {"method":"GET","path":"/site-waiver-exception","contract":"marketing-crm","summary":"On-Site Waiver & Exception Handling","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"ticketId","in":"query","required":false},{"name":"mediaCode","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"customerSubjectId","in":"query","required":false},{"name":"participantSubjectId","in":"query","required":false},{"name":"groupBookingId","in":"query","required":false},{"name":"membershipId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWaiver": {"method":"GET","path":"/waiver","contract":"marketing-crm","summary":"Waiver Operations Command Center","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"brandId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"formId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"participantType","in":"query","required":false},{"name":"bookingChannel","in":"query","required":false},{"name":"breakdownBy","in":"query","required":false}],"requestBody":null,"responds":"WaiverOperationsCommandCenterView"},
"listWaiverComplianceOperational": {"method":"GET","path":"/waiver-compliance-operational","contract":"marketing-crm","summary":"Waiver Analytics, Compliance & Operational Insights","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"formId","in":"query","required":false},{"name":"formVersion","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"customerType","in":"query","required":false},{"name":"participantType","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":"groupBookingId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"WaiverAnalyticsComplianceOperationalInsightsView"},
"listWaiverComplianceRisk": {"method":"GET","path":"/waiver-compliance-risk","contract":"marketing-crm","summary":"AI Waiver Compliance & Risk Intelligence Center","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"forecastDate","in":"query","required":false},{"name":"category","in":"query","required":false}],"requestBody":null,"responds":"AiWaiverComplianceRiskIntelligenceCenterView"},
"listWaiverVerificationQueue": {"method":"GET","path":"/waiver-verification-validation","contract":"marketing-crm","summary":"The waiver submissions awaiting or given verification","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"formId","in":"query","required":false},{"name":"performanceId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setWaiverVerificationValidation": {"method":"PUT","path":"/waiver-verification-validation","contract":"marketing-crm","summary":"Record a reviewer's verification decision on a waiver submission","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WaiverVerificationValidationWorkspaceInput","responds":"WaiverVerificationValidationWorkspaceView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiWaiverComplianceRiskIntelligenceCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_definition + marketing.form_definition_field, marketing.waiver_requirement (new), marketing.waiver_requirement_event (new), marketing.form_submission, marketing.waiver_verification (new), marketing.waiver_exception (new) and catalogue product associations; predictions computed at read time","description":"Waiver risks, recommendations and the readiness forecast. Advisory only.","required":["risks","recommendations"],"properties":{"templates":{"type":"integer","minimum":0,"description":"Waiver forms analysed (published or scheduled)."},"versions":{"type":"integer","minimum":0,"description":"Form versions in effect or scheduled."},"questions":{"type":"integer","minimum":0,"description":"Questions across those versions."},"signatoryRules":{"type":"integer","minimum":0},"productAssociations":{"type":"integer","minimum":0},"risks":{"type":"array","maxItems":100,"items":{"type":"object","required":["category","severity","message"],"properties":{"category":{"type":"string","enum":["operational","configuration","version","customerExperience"]},"severity":{"type":"string","enum":["high","medium","low"]},"source":{"type":"string","enum":["rule","ai"],"description":"`rule` for a deterministic check, `ai` for a prediction."},"message":{"type":"string","maxLength":500},"subjectType":{"type":"string","nullable":true,"enum":["performance","product","form","formVersion","groupBooking"]},"subjectId":{"type":"string","nullable":true},"affectedParticipants":{"type":"integer","minimum":0,"nullable":true}}}},"recommendations":{"type":"array","maxItems":50,"items":{"type":"object","required":["message","action"],"properties":{"message":{"type":"string","maxLength":500},"action":{"type":"string","enum":["sendTargetedReminders","reorderFormSections","reviewMobileLayout","updateVersionAssociation","addReminderTrigger","enableAccessBlocking","other"]},"operationId":{"type":"string","nullable":true,"description":"The operation that would carry it out, e.g. `actOnWaiverRequirements`, `setMessageTrigger`, `setDigitalWaiverForm`."},"riskIndex":{"type":"integer","minimum":0,"nullable":true,"description":"Index into `risks` of the risk it answers."}}}},"forecast":{"type":"object","nullable":true,"required":["forDate","readinessRate"],"properties":{"forDate":{"type":"string","format":"date"},"readinessRate":{"type":"number","minimum":0,"maximum":1,"description":"Predicted share of participants ready at arrival."},"potentialUnresolved":{"type":"integer","minimum":0},"highRisk":{"type":"integer","minimum":0}}}}},
"ComplianceEvidenceAuditWaiverRepositoryView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_submission, marketing.waiver_signature, marketing.form_definition + marketing.form_definition_field, marketing.guest_document, marketing.waiver_verification (new), marketing.waiver_requirement (new) and marketing.waiver_requirement_event (new); names from pii.subject","description":"One signed waiver as evidence. Nothing here changes after signing except the verification and the audit events appended to it.","required":["submissionId","waiverId","exactVersion","participant","signatory","submittedAt","documentHash","auditEvents"],"properties":{"submissionId":{"type":"string","format":"uuid"},"signatureId":{"type":"string","format":"uuid","nullable":true,"description":"The `MarketingWaiverSignature` row."},"waiverId":{"type":"string","format":"uuid","description":"The waiver form (`FormDefinition.id`)."},"waiverName":{"type":"string"},"exactVersion":{"type":"integer","minimum":1,"description":"The form version presented and signed; `getForm` with this `version` returns its wording and questions."},"participant":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"dateOfBirth":{"type":"string","format":"date","nullable":true}}},"signatory":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"signedName":{"type":"string","description":"The name as typed or drawn at signing."}}},"signatoryType":{"type":"string","enum":["participant","guardian","organisationRepresentative"]},"guardianRelationshipId":{"type":"string","format":"uuid","nullable":true,"description":"The `GuestRelationship` relied on when a guardian or representative signed."},"submittedAt":{"type":"string","format":"date-time","description":"Device time of signing."},"syncedAt":{"type":"string","format":"date-time","description":"Server time the submission arrived."},"channel":{"type":"string","description":"`FormSubmission.capturedAtChannel`."},"collectionMethod":{"type":"string","nullable":true,"enum":["email","sms","whatsapp","guestWeb","guestApp","groupPortal","qrCode","pos","kiosk","staffAssistedDevice"]},"assistedByStaffId":{"type":"string","format":"uuid","nullable":true,"description":"The staff member who helped on a staff-assisted device; never the signer."},"responses":{"type":"object","description":"`FormSubmission.answers`, keyed by field key.","additionalProperties":true},"acknowledgements":{"type":"array","items":{"type":"object","required":["key","accepted"],"properties":{"key":{"type":"string"},"label":{"type":"string","description":"The wording as presented in `exactVersion`."},"accepted":{"type":"boolean"}}}},"signatureEvidence":{"type":"object","properties":{"signatureKind":{"type":"string","enum":["drawn","typed","checkbox"]},"signatureAssetId":{"type":"string","format":"uuid","nullable":true},"signedDocumentId":{"type":"string","format":"uuid","nullable":true,"description":"The rendered document as signed (`GuestDocument`, kind `signedWaiver`)."}}},"documentHash":{"type":"string","maxLength":128,"description":"Hash of the rendered document as signed."},"deviceEvidence":{"type":"object","nullable":true,"description":"Personal data (ADR-0023); null once the subject is erased.","properties":{"ipAddress":{"type":"string","nullable":true},"deviceInfo":{"type":"string","nullable":true}}},"verification":{"type":"object","nullable":true,"properties":{"result":{"type":"string","enum":["automaticallyValidated","pendingManualVerification","verified","correctionRequired","rejected","escalated"]},"reviewedBy":{"type":"string","format":"uuid","nullable":true},"reviewedAt":{"type":"string","format":"date-time","nullable":true}}},"relatedBooking":{"type":"string","format":"uuid","nullable":true},"relatedTicket":{"type":"string","format":"uuid","nullable":true},"applicableProductId":{"type":"string","format":"uuid","nullable":true},"applicablePerformanceId":{"type":"string","format":"uuid","nullable":true},"retainUntil":{"type":"string","format":"date-time","nullable":true,"description":"From the retention policy in force."},"auditEvents":{"type":"array","description":"The requirement's timeline, oldest first (link issued, opened, completed, signed, validated, verified and every staff action).","items":{"type":"object","required":["at","event","actor"],"properties":{"at":{"type":"string","format":"date-time"},"event":{"type":"string","enum":["linkIssued","linkOpened","participantIdentified","guardianInformationCompleted","questionsCompleted","acknowledgementsAccepted","signatureSubmitted","validationPassed","validationFailed","markedComplete","verified","rejected","correctionRequested","signatoryReplaced","exceptionApproved","evidenceViewed"]},"actor":{"type":"string","enum":["participant","guardian","staff","system"]},"staffId":{"type":"string","format":"uuid","nullable":true}}}}}},
"DigitalSigningCollectionOperationsView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.waiver_requirement (new), marketing.waiver_requirement_event (new), marketing.message_dispatch and marketing.form_submission","description":"Waiver link distribution and completion for the filters given.","required":["sent","delivered","opened","started","completed","failed","expiredLinks","byMethod","journey"],"properties":{"sent":{"type":"integer","minimum":0},"delivered":{"type":"integer","minimum":0},"opened":{"type":"integer","minimum":0},"started":{"type":"integer","minimum":0},"completed":{"type":"integer","minimum":0},"failed":{"type":"integer","minimum":0,"description":"Links whose message could not be delivered on any channel."},"expiredLinks":{"type":"integer","minimum":0,"description":"Links that expired unused, or were refused because already used."},"completionRate":{"type":"number","minimum":0,"maximum":1,"description":"`completed` / `sent`."},"byMethod":{"type":"array","description":"One entry per delivery method used in the window.","items":{"type":"object","required":["method","sent","completed"],"properties":{"method":{"type":"string","enum":["email","sms","whatsapp","guestWeb","guestApp","groupPortal","qrCode","pos","kiosk","staffAssistedDevice"]},"sent":{"type":"integer","minimum":0},"completed":{"type":"integer","minimum":0},"completionRate":{"type":"number","minimum":0,"maximum":1}}}},"journey":{"type":"array","description":"How many requirements reached each stage of the signing journey, in journey order.","items":{"type":"object","required":["stage","count"],"properties":{"stage":{"type":"string","enum":["linkIssued","participantIdentified","waiverLoaded","questionsCompleted","acknowledgementsAccepted","signatureCaptured","submissionValidated","evidenceStored"]},"count":{"type":"integer","minimum":0}}}},"recentCompletions":{"type":"array","maxItems":50,"items":{"type":"object","required":["requirementId","participantSubjectId","formName","formVersion","completedAt"],"properties":{"requirementId":{"type":"string","format":"uuid"},"participantSubjectId":{"type":"string","format":"uuid","description":"The name is not returned here (GUEST_VIEW); `listParticipantWaiverStatus` resolves it under GUEST_VIEW_PII."},"booking":{"type":"string","format":"uuid"},"formName":{"type":"string"},"formVersion":{"type":"integer","minimum":1},"method":{"type":"string","nullable":true},"completedAt":{"type":"string","format":"date-time"}}}}}},
"MinorGuardianGroupConsentManagementView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.guest_relationship, marketing.waiver_requirement (new), marketing.form_submission, orders.group_booking and orders.order_line; names and contacts from pii.subject and pii.subject_contact","description":"One minor participant on one booking, their guardians and their group.","required":["minor","booking","guardians","consentStatus"],"properties":{"minor":{"type":"object","required":["subjectId","name"],"properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"age":{"type":"integer","minimum":0,"nullable":true}}},"booking":{"type":"string","format":"uuid","description":"The order id."},"visitDate":{"type":"string","format":"date-time","nullable":true},"guardians":{"type":"array","description":"Everyone holding a parent or guardian relationship to the minor; empty when none is recorded.","items":{"type":"object","required":["subjectId","name","relationship","verificationStatus","signatureStatus"],"properties":{"relationshipId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"relationship":{"type":"string","enum":["parent","guardian"]},"contact":{"type":"string","nullable":true,"description":"The address the guardian link goes to (email or mobile)."},"mayWaive":{"type":"boolean","description":"The relationship carries the `signWaiver` authority and is in effect."},"verificationStatus":{"type":"string","enum":["verified","unverified"],"description":"`verified` when `GuestRelationship.verifiedAt` is set."},"signatureStatus":{"type":"string","enum":["notRequested","sent","opened","signed","rejected","expired"]}}}},"consentStatus":{"type":"string","enum":["complete","pending","rejected"],"description":"`complete` when every mandatory guardian consent for the minor on this booking is signed by an authorised signatory."},"group":{"type":"object","nullable":true,"description":"The group booking the minor is part of, and its leader.","properties":{"groupBookingId":{"type":"string","format":"uuid"},"organization":{"type":"string","nullable":true,"description":"The school, club or company."},"groupLeader":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"contact":{"type":"string","nullable":true,"description":"The leader's email or mobile."},"groupBooking":{"type":"string","format":"uuid","description":"The group's order id."},"responsibility":{"type":"string","enum":["coordinatorOnly","supervisingAdult","organisationRepresentative"],"description":"`organisationRepresentative` when the leader's `GuestRelationship` (kind `groupLeader`) carries `signWaiver`; `supervisingAdult` when the leader is a participant on the booking; otherwise `coordinatorOnly`."},"permittedActions":{"type":"array","description":"What the leader may do for this group under the form's signatory rule.","items":{"type":"string","enum":["viewStatus","sendLinks","receiveNotifications","signOnBehalf"]}}}}}},
"MissingExpiredInvalidWaiverManagementView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.waiver_requirement (new), marketing.form_submission, marketing.waiver_verification (new), marketing.waiver_exception (new), marketing.message_dispatch, orders.order_line, orders.group_booking and catalogue.performance; names from pii.subject","description":"One participant waiver requirement that is not ready, why, and what it blocks.","required":["requirementId","participant","booking","waiver","problem","accessImpact","status","priority"],"properties":{"requirementId":{"type":"string","format":"uuid"},"participant":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"isMinor":{"type":"boolean"}}},"booking":{"type":"string","format":"uuid"},"groupBookingId":{"type":"string","format":"uuid","nullable":true},"event":{"type":"object","properties":{"performanceId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"visitTime":{"type":"string","format":"date-time","nullable":true},"waiver":{"type":"object","properties":{"formId":{"type":"string","format":"uuid"},"name":{"type":"string"},"version":{"type":"integer","minimum":1,"nullable":true},"mandatory":{"type":"boolean"}}},"problem":{"type":"string","enum":["missingWaiver","incomplete","missingSignature","guardianMissing","expired","wrongVersion","rejected","verificationFailed","linkExpired","participantMismatch","correctionRequired"]},"timeRemainingSeconds":{"type":"integer","nullable":true,"description":"Seconds until the activity starts; negative once it has started."},"accessImpact":{"type":"string","enum":["none","ticketDownloadBlocked","activationBlocked","checkInBlocked","accessBlocked"]},"owner":{"type":"object","nullable":true,"properties":{"staffId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"status":{"type":"string","enum":["open","inProgress","awaitingCustomer","resolved","exceptionApproved"]},"priority":{"type":"string","enum":["P1","P2","P3","P4"]},"priorityFactors":{"type":"array","description":"The factors that raised this row's priority.","items":{"type":"string","enum":["eventProximity","mandatoryWaiver","accessBlocking","minorGuardianIssue","groupSize","operationalImpact"]}},"remindersSent":{"type":"integer","minimum":0},"nextReminderAt":{"type":"string","format":"date-time","nullable":true},"completionLikelihood":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Advisory prediction that the participant completes before the activity without staff contact."}}},
"OnSiteWaiverExceptionHandlingView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.waiver_requirement (new), marketing.waiver_exception (new), marketing.form_definition, orders.order_line, access.entitlement and the order's payment state; names from pii.subject","description":"One participant found at arrival, their waiver state, and how it can be resolved.","required":["participant","booking","waivers","accessStatus","resolutionOptions"],"properties":{"participant":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"isMinor":{"type":"boolean"}}},"customer":{"type":"object","nullable":true,"description":"The purchaser.","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"booking":{"type":"string","format":"uuid"},"ticket":{"type":"string","format":"uuid","nullable":true},"groupBookingId":{"type":"string","format":"uuid","nullable":true},"ticketValid":{"type":"boolean"},"paymentComplete":{"type":"boolean"},"waivers":{"type":"array","items":{"type":"object","required":["requirementId","formName","mandatory","status"],"properties":{"requirementId":{"type":"string","format":"uuid"},"formId":{"type":"string","format":"uuid"},"formName":{"type":"string"},"mandatory":{"type":"boolean"},"status":{"type":"string","enum":["notAssigned","assigned","sent","opened","inProgress","completed","verified","rejected","expired","superseded"]},"signedVersionOutdated":{"type":"boolean","description":"Signed, but a newer mandatory version is in effect (re-sign needed)."}}}},"accessStatus":{"type":"string","enum":["eligible","blocked","admittedByException"]},"resolutionOptions":{"type":"array","description":"The options the venue has enabled that apply to this participant.","items":{"type":"string","enum":["sendMobileLink","displayQrForCustomer","completeOnKiosk","completeOnStaffTablet","contactGuardian","reSignUpdatedWaiver","requestSupervisorException"]}},"exceptions":{"type":"array","description":"Exceptions requested or in force for this participant.","items":{"$ref":"#/components/schemas/WaiverAccessException"}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ParticipantWaiverStatusTrackingView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.waiver_requirement (new), marketing.form_definition, marketing.form_submission, marketing.waiver_verification (new), marketing.waiver_exception (new), orders.order_line, orders.group_booking and catalogue.performance; names from pii.subject","description":"One participant on one booking and the waivers that participant needs. Purchaser, participant and each waiver's signatory are separate people.","required":["participantId","participant","booking","waiverRequirements","completionStatus"],"properties":{"participantId":{"type":"string","format":"uuid","description":"The participant's subject id."},"participant":{"type":"string","description":"The participant's name."},"customerPurchaser":{"type":"object","nullable":true,"description":"Who bought the booking; may differ from the participant.","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"booking":{"type":"string","format":"uuid","description":"The order id."},"ticket":{"type":"string","format":"uuid","nullable":true,"description":"The ticket (entitlement) id."},"product":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"event":{"type":"object","nullable":true,"properties":{"eventId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"visitDate":{"type":"string","format":"date-time","nullable":true},"ageCategory":{"type":"string","enum":["adult","minor"],"description":"From the participant's date of birth against the age of majority configured for the venue's jurisdiction (no shipped default). A participant whose age cannot be established is treated as a minor."},"group":{"type":"object","nullable":true,"properties":{"groupBookingId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"waiverRequirements":{"type":"array","description":"Each waiver this participant needs on this booking.","items":{"type":"object","required":["requirementId","formId","formName","mandatory","status"],"properties":{"requirementId":{"type":"string","format":"uuid"},"formId":{"type":"string","format":"uuid"},"formName":{"type":"string"},"formVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version assigned, or signed once completed."},"mandatory":{"type":"boolean","description":"False for an optional consent (e.g. media), which never blocks readiness."},"status":{"type":"string","enum":["notAssigned","assigned","sent","opened","inProgress","completed","verified","rejected","expired","superseded"]},"declined":{"type":"boolean","default":false,"description":"An optional consent answered no."},"signatory":{"type":"object","nullable":true,"properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"signatoryType":{"type":"string","enum":["participant","guardian","organisationRepresentative"]}}},"deliveryChannel":{"type":"string","nullable":true,"enum":["email","sms","whatsapp","push","inApp","qrCode","pos","kiosk","staffAssistedDevice","groupPortal"]},"lastSentAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true},"submissionId":{"type":"string","format":"uuid","nullable":true},"blocks":{"type":"array","description":"What an incomplete requirement blocks, from the trigger configuration.","items":{"type":"string","enum":["ticketDownload","activation","checkIn","access"]}}}}},"completionStatus":{"type":"string","enum":["ready","notReady","exceptionApproved"],"description":"`ready` when every mandatory requirement is completed or verified; `exceptionApproved` when the gap is covered by an approved exception."}}},
"WaiverAccessException": {"type":"object","x-ticvai-persistence":"marketing.waiver_exception","description":"A supervisor-approved exception letting a participant be admitted without a completed waiver, within a stated scope. Never marks the waiver signed.","required":["requirementId","reasonCode","reason","scope","status"],"properties":{"id":{"type":"string","format":"uuid","description":"Absent on a new request; set by the server."},"requirementId":{"type":"string","format":"uuid"},"reasonCode":{"type":"string","enum":["guardianUnreachable","deviceOrConnectivityFailure","signedOnPaper","accessibilityNeed","operationalDecision","other"]},"reason":{"type":"string","maxLength":1000},"supportingEvidenceAssetIds":{"type":"array","maxItems":10,"description":"`GuestDocument` ids, e.g. a paper waiver scanned on site.","items":{"type":"string","format":"uuid"}},"supervisorStaffId":{"type":"string","format":"uuid","nullable":true,"description":"The supervisor asked to decide."},"status":{"type":"string","enum":["requested","approved","rejected","revoked","expired"],"default":"requested"},"scope":{"type":"string","enum":["oneTime","ticketSpecific","activitySpecific","timeLimited"]},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"Required for `ticketSpecific`."},"performanceId":{"type":"string","format":"uuid","nullable":true,"description":"Required for `activitySpecific`."},"validUntil":{"type":"string","format":"date-time","nullable":true,"description":"Required for `timeLimited`."},"decisionNote":{"type":"string","maxLength":1000,"nullable":true},"usedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a `oneTime` exception was used at access."},"requestedBy":{"type":"string","format":"uuid","readOnly":true},"requestedAt":{"type":"string","format":"date-time","readOnly":true},"decidedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaiverAnalyticsComplianceOperationalInsightsView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.waiver_requirement (new), marketing.waiver_requirement_event (new), marketing.form_submission, marketing.waiver_verification (new), marketing.waiver_exception (new), marketing.message_dispatch and access validation outcomes","description":"Waiver analytics for the filters given; aggregate only.","required":["waiversAssigned","completionRate","funnel"],"properties":{"waiversAssigned":{"type":"integer","minimum":0},"completionRate":{"type":"number","minimum":0,"maximum":1},"preArrivalCompletion":{"type":"integer","minimum":0,"description":"Requirements completed before the participant arrived."},"onSiteCompletion":{"type":"integer","minimum":0,"description":"Requirements completed on site (kiosk, POS, staff-assisted device, on-site QR)."},"averageCompletionSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Mean time from opening the link to submitting."},"guardianCompletionRate":{"type":"number","minimum":0,"maximum":1},"rejectionRate":{"type":"number","minimum":0,"maximum":1},"exceptionRate":{"type":"number","minimum":0,"maximum":1},"accessBlocks":{"type":"integer","minimum":0,"description":"Access attempts refused with `waiverRequired`."},"checkInDelays":{"type":"integer","minimum":0,"description":"Check-ins held while a waiver was completed or resolved on site."},"staffInterventions":{"type":"integer","minimum":0,"description":"Staff actions taken on requirements (sends, corrections, verifications, exceptions)."},"exceptions":{"type":"integer","minimum":0,"description":"Exceptions approved."},"reminderEffectiveness":{"type":"array","description":"Completion after each reminder, by how long before the activity it was sent.","items":{"type":"object","required":["hoursBeforeActivity","sent","completedAfter"],"properties":{"hoursBeforeActivity":{"type":"integer","minimum":0},"sent":{"type":"integer","minimum":0},"completedAfter":{"type":"integer","minimum":0},"completionRate":{"type":"number","minimum":0,"maximum":1}}}},"funnel":{"type":"array","description":"In funnel order.","items":{"type":"object","required":["stage","count"],"properties":{"stage":{"type":"string","enum":["assigned","sent","delivered","opened","started","signed","verified"]},"count":{"type":"integer","minimum":0}}}},"abandonment":{"type":"array","maxItems":50,"description":"Where people leave the form, highest abandonment first.","items":{"type":"object","required":["formId","formVersion","section","abandonmentRate"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"section":{"type":"string","description":"The section or field key where the session ended."},"deviceClass":{"type":"string","enum":["mobile","desktop","tablet","kiosk"]},"abandoned":{"type":"integer","minimum":0},"abandonmentRate":{"type":"number","minimum":0,"maximum":1}}}},"insights":{"type":"array","maxItems":20,"description":"Advisory findings.","items":{"type":"object","required":["message"],"properties":{"message":{"type":"string","maxLength":500}}}}}},
"WaiverOperationsCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.waiver_requirement (new), marketing.form_definition, marketing.form_submission, marketing.waiver_signature, marketing.waiver_verification (new), marketing.waiver_exception (new), orders.order_line, orders.group_booking and catalogue.performance","description":"Waiver readiness for the filters given. Counts are of participant waiver requirements for activities in the window unless the name says otherwise.","required":["waiversRequired","completed","pending","completionRate","byPeriod","breakdown","upcomingActivities"],"properties":{"waiversRequired":{"type":"integer","minimum":0,"description":"Requirements assigned, excluding `superseded`."},"completed":{"type":"integer","minimum":0,"description":"Requirements `completed` or `verified`."},"pending":{"type":"integer","minimum":0,"description":"Requirements `assigned`, `sent` or `opened`, not yet started."},"partiallyCompleted":{"type":"integer","minimum":0,"description":"Requirements `inProgress`, and participants with some but not all waivers complete."},"expiring":{"type":"integer","minimum":0,"description":"Completed requirements whose acceptance (`FormSubmission.expiresAt`) ends before the activity starts."},"invalid":{"type":"integer","minimum":0,"description":"Requirements `expired`, or completed against a superseded version."},"rejected":{"type":"integer","minimum":0},"guardianConsentPending":{"type":"integer","minimum":0,"description":"Minor participants whose guardian has not yet signed."},"upcomingParticipantsMissingWaiver":{"type":"integer","minimum":0,"description":"Participants with at least one mandatory requirement not complete."},"accessBlocked":{"type":"integer","minimum":0,"description":"Participants whose ticket download, activation, check-in or access is currently blocked by a waiver."},"manualExceptions":{"type":"integer","minimum":0,"description":"Approved exceptions (`setWaiverException`) in force."},"completionRate":{"type":"number","minimum":0,"maximum":1,"description":"`completed` / `waiversRequired`."},"byPeriod":{"type":"array","description":"Today, tomorrow and this week, in that order, whatever the window.","items":{"type":"object","required":["period","waiversRequired","completed","missing"],"properties":{"period":{"type":"string","enum":["today","tomorrow","thisWeek"]},"waiversRequired":{"type":"integer","minimum":0},"completed":{"type":"integer","minimum":0},"missing":{"type":"integer","minimum":0}}}},"breakdown":{"type":"array","maxItems":100,"description":"One entry per value of `breakdownBy`, lowest completion first.","items":{"type":"object","required":["key","label","waiversRequired","completed","completionRate"],"properties":{"key":{"type":"string","description":"The id of the venue, event, product, performance, group booking, booking or waiver form."},"label":{"type":"string"},"waiversRequired":{"type":"integer","minimum":0},"completed":{"type":"integer","minimum":0},"missing":{"type":"integer","minimum":0},"completionRate":{"type":"number","minimum":0,"maximum":1}}}},"upcomingActivities":{"type":"array","maxItems":100,"description":"Performances in the window, most at risk first, then by `dateTime`.","items":{"type":"object","required":["performanceId","eventActivity","dateTime","participants","waiversRequired","completed","missing","completion","operationalRisk"],"properties":{"performanceId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"eventActivity":{"type":"string","description":"The event or activity name."},"venueId":{"type":"string","format":"uuid"},"venue":{"type":"string","description":"The venue name."},"dateTime":{"type":"string","format":"date-time","description":"When the performance starts."},"participants":{"type":"integer","minimum":0},"waiversRequired":{"type":"integer","minimum":0},"completed":{"type":"integer","minimum":0},"missing":{"type":"integer","minimum":0},"completion":{"type":"number","minimum":0,"maximum":1,"description":"The performance's waiver readiness (the pack's Readiness Score)."},"guardianPending":{"type":"integer","minimum":0},"exceptions":{"type":"integer","minimum":0},"admissionAtRisk":{"type":"boolean","description":"At least one missing requirement is configured to block check-in or access."},"operationalRisk":{"type":"string","enum":["ready","attention","critical"],"description":"`critical` when a missing requirement would block admission; `attention` when anything is missing; otherwise `ready`."}}}},"insights":{"type":"array","maxItems":20,"description":"Advisory predictions, e.g. participants unlikely to complete before arrival without another reminder. Never change a status.","items":{"type":"object","required":["message"],"properties":{"performanceId":{"type":"string","format":"uuid","nullable":true},"predictedIncomplete":{"type":"integer","minimum":0,"nullable":true},"message":{"type":"string","maxLength":500}}}}}},
"WaiverVerificationValidationWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.waiver_verification","description":"A reviewer's decision on one waiver submission. The automatic checks are the server's and are not sent; the reviewer records the checks only a person can make.","required":["submissionId","result"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"submissionId":{"type":"string","format":"uuid","description":"The `FormSubmission` reviewed; the natural key."},"result":{"type":"string","enum":["verified","rejected","correctionRequired","escalated"]},"participantMatch":{"type":"boolean","nullable":true,"description":"The reviewer confirmed the signed participant is the booked participant."},"bookingMatch":{"type":"boolean","nullable":true},"guardianRelationshipPresent":{"type":"boolean","nullable":true,"description":"The reviewer confirmed the signatory's guardianship under the configured policy."},"requiredEvidencePresent":{"type":"boolean","nullable":true,"description":"Any supporting document the form requires was seen."},"reasonCode":{"type":"string","nullable":true,"enum":["signatoryNotAuthorised","participantMismatch","wrongVersion","incompleteAnswers","evidenceMissing","suspectedFraud","other"]},"note":{"type":"string","maxLength":2000,"nullable":true,"description":"Required for `rejected`, `correctionRequired`, `escalated`, and for changing an earlier decision."},"escalatedTo":{"type":"string","format":"uuid","nullable":true,"description":"The staff member the review is escalated to; required for `escalated`."},"reviewedBy":{"type":"string","format":"uuid","readOnly":true},"reviewedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaiverVerificationValidationWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_submission, marketing.waiver_signature, marketing.form_definition, marketing.waiver_verification (new) and marketing.waiver_requirement (new); names from pii.subject","description":"One waiver submission in the verification queue, with its automatic checks, the reviewer's findings and any anomalies flagged.","required":["submissionId","participant","waiver","version","submitted","status","checks"],"properties":{"submissionId":{"type":"string","format":"uuid"},"requirementId":{"type":"string","format":"uuid","nullable":true},"participant":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"age":{"type":"integer","minimum":0,"nullable":true}}},"waiver":{"type":"object","properties":{"formId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"version":{"type":"integer","minimum":1,"description":"The form version signed."},"booking":{"type":"string","format":"uuid","nullable":true},"signatory":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"signatoryType":{"type":"string","enum":["participant","guardian","organisationRepresentative"]}}},"submitted":{"type":"string","format":"date-time","description":"`FormSubmission.submittedAt`, the device time of signing."},"verificationReason":{"type":"string","enum":["configuredManualReview","automaticCheckFailed","minorSignedAsAdult","guardianDiscrepancy","participantMismatch","evidenceRequired","aiAnomaly","sampleReview"]},"risk":{"type":"string","enum":["low","medium","high"]},"status":{"type":"string","enum":["automaticallyValidated","pendingManualVerification","verified","correctionRequired","rejected","escalated"]},"checks":{"type":"object","description":"Each check the form's configuration applies; null when it does not apply. The first seven are evaluated by the server, the last three recorded by the reviewer.","properties":{"requiredFieldsComplete":{"type":"boolean","nullable":true},"requiredQuestionsAnswered":{"type":"boolean","nullable":true},"requiredAcknowledgementsAccepted":{"type":"boolean","nullable":true},"signaturePresent":{"type":"boolean","nullable":true},"correctWaiverVersion":{"type":"boolean","nullable":true},"effectiveDateValid":{"type":"boolean","nullable":true,"description":"The version signed was in effect at signing and the acceptance covers the visit."},"guardianRelationshipPresent":{"type":"boolean","nullable":true,"description":"Evaluated from `GuestRelationship` where recorded, otherwise the reviewer's."},"participantMatch":{"type":"boolean","nullable":true},"bookingMatch":{"type":"boolean","nullable":true},"requiredEvidencePresent":{"type":"boolean","nullable":true}}},"anomalies":{"type":"array","description":"Advisory flags for the reviewer; never a decision.","items":{"type":"object","required":["code","message"],"properties":{"code":{"type":"string","enum":["minorSignedAsAdult","guardianSurnameDiffers","signatoryIsMinor","signedAfterActivity","duplicateSubmission","other"]},"message":{"type":"string","maxLength":500},"source":{"type":"string","enum":["rule","ai"]}}}},"reviewedBy":{"type":"string","format":"uuid","nullable":true},"reviewedAt":{"type":"string","format":"date-time","nullable":true},"note":{"type":"string","nullable":true}}}
}
```
