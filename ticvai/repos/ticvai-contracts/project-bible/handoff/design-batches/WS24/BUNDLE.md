# WS24 — Communication & Notification Platform Services board 1

**10 screens · 11 operations · 19 schemas · 4 permissions**

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
  `AI_USE, GUEST_VIEW, MARKETING_MANAGE, MARKETING_VIEW`. A control nobody can use must say so,
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
| `ADM-038` | Communication Service Command Center | D | 0 | 18 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-039` | Channel & Provider Configuration | D | 6 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-040` | Sender Identity, Domain & Brand Configuration | D | 19 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `ADM-041` | System Transactional Template Registry | D | 9 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-042` | Business Event & Notification Trigger Mapping | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-043` | Routing, Priority, Throttling & Fallback Rules | D | 14 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-044` | Consent, Preference & Communication Policy Enforcement | D | 0 | 0 | 6 | 0 | 1 | 4 | — | notStarted (generated) |
| `ADM-045` | Delivery Queue, Failure & Retry Management | D | 0 | 24 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `ADM-046` | Provider Health, Usage & Cost Monitoring | D | 2 | 20 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-047` | AI Delivery Optimization & Communication Platform Diagnostics | D | 0 | 12 | 6 | 11 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-038, ADM-044, ADM-045, ADM-047 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-038` Communication Service Command Center

**Provide administrators and technical/operations teams with a centralized view of the health and activity of TICVAI's communication infrastructure. This is not a marketing dashboard.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-038 |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/communication-service-command-center-adm-038` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** For TICVAI administrators and operations: the health and activity of the communication infrastructure across tenants. It is not a marketing dashboard - it shows throughput, queues, failures and provider state, not campaign performance.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listCommunicationService` ?from |
| To | date and time picker | — | — | `listCommunicationService` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every communication service** (data table, from `listCommunicationService`)

| Shows | Format | Notes |
|---|---|---|
| Messages processed | 1,234 | Messages accepted by the service in the window (the pack's "Messages Processed Today"). |
| Sent | 1,234 | — |
| Delivered | 1,234 | — |
| Failed | 1,234 | — |
| Pending | 1,234 | — |
| Retrying | 1,234 | — |
| Average delivery seconds | 1,234.5 | Mean time from acceptance to provider-confirmed delivery, in (fractional) seconds. |
| Provider availability rate | 12.5% | Share of the window the active providers were reachable, weighted by volume. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |

**The selected communication service** (detail panel): The pack groups this record's detail under its own headings: “Module Activity”, “Channel Provider Health”, “Health”, “WhatsAp Warni”.

| Shows | Format | Notes |
|---|---|---|
| Messages processed | 1,234 | Messages accepted by the service in the window (the pack's "Messages Processed Today"). |
| Sent | 1,234 | — |
| Delivered | 1,234 | — |
| Failed | 1,234 | — |
| Pending | 1,234 | — |
| Retrying | 1,234 | — |
| Average delivery seconds | 1,234.5 | Mean time from acceptance to provider-confirmed delivery, in (fractional) seconds. |
| Provider availability rate | 12.5% | Share of the window the active providers were reachable, weighted by volume. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Platform KPIs**: Volume by channel and provider, queue depth, failure rate, providers degraded. *(source: contracts/satellite/marketing-crm.yaml#listCommunicationService)*

**Data it reads**: `listCommunicationService` (onLoad, Communication Service Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-039` Channel & Provider Configuration: *Works in Channel & Provider Configuration*; calls `listCommunicationService`
- → `ADM-040` Sender Identity, Domain & Brand Configuration: *Works in Sender Identity, Domain & Brand Configuration*; calls `listCommunicationService`
- → `ADM-041` System Transactional Template Registry: *Works in System Transactional Template Registry*; calls `listCommunicationService`
- → `ADM-042` Business Event & Notification Trigger Mapping: *Works in Business Event & Notification Trigger Mapping*; calls `listCommunicationService`
- → `ADM-043` Routing, Priority, Throttling & Fallback Rules: *Works in Routing, Priority, Throttling & Fallback Rules*; calls `listCommunicationService`
- → `ADM-044` Consent, Preference & Communication Policy Enforcement: *Works in Consent, Preference & Communication Policy Enforcement*; calls `listCommunicationService`
- → `ADM-045` Delivery Queue, Failure & Retry Management: *Works in Delivery Queue, Failure & Retry Management*; calls `listCommunicationService`
- → `ADM-046` Provider Health, Usage & Cost Monitoring: *Works in Provider Health, Usage & Cost Monitoring*; calls `listCommunicationService`
- → `ADM-047` AI Delivery Optimization & Communication Platform Diagnostics: *Works in AI Delivery Optimization & Communication Platform Diagnostics*; calls `listCommunicationService`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The communication service list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the communication service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No communication service yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the communication service are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `BO-784`: Same object scoped to one venue there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  messagesToday: 1240000
  queueDepth: 3420
  failureRate: 0.6%
  degradedProviders:
  - SMS gateway KSA
```

#### Permissions

- `listCommunicationService` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-038` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-038`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 1: Opens Communication Service Command Center → Provide administrators and technical/operations teams with a centralized view of the health and activity of TICVAI's communication infrastructure. This is not a marketing dashboard.
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F133 branch at step 1 (expected): when Nothing has been set up on Communication Service Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F133 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-038?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-039`, `ADM-040`, `ADM-041`, `ADM-042`, `ADM-043`, `ADM-044`, `ADM-045`, `ADM-046`, `ADM-047`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-039` Channel & Provider Configuration

**Configure the external/internal services used by TICVAI to deliver communications.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-039 |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/channel-provider-configuration-adm-039` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Legal Entity, Test Connection, Send Test Message, Validate Credentials, Test Webhook, Verify Delivery …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Configure the providers TICVAI uses to deliver each channel: SMTP or email service, SMS gateway, WhatsApp provider, push service, in-app. Credentials are stored in the vault and never shown again; connections, webhooks and delivery receipts can be tested.

**Known correction pending (do not draw the wrong version)**

- **"Legal Entity" is the primary button and the channel fields are selects.** Why: The act is Save provider; legal entity is a field. *(source: screens/P08-venue-back-office.yaml#ADM-039; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Email | select field | — | — | — | — | — | — |
| SMS | select field | — | — | — | — | — | — |
| WhatsApp | select field | — | — | — | — | — | — |
| Mobile Push | select field | — | — | — | — | — | — |
| In-App Notification | select field | — | — | — | — | — | — |
| Future supported channels | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Provider credentials**: Write-only; after saving, only a masked reference is shown. *(source: contracts/satellite/marketing-crm.yaml#setChannelProvider)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Legal Entity (primary button) | navigation or local | — | — | — | — |
| Test Connection (secondary button) | navigation or local | — | — | — | — |
| Send Test Message (secondary button) | navigation or local | — | — | — | — |
| Validate Credentials (secondary button) | navigation or local | — | — | — | — |
| Test Webhook (secondary button) | navigation or local | — | — | — | — |
| Verify Delivery Receipt (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Test connection / Send test message / Test webhook**: Each shows pass or fail with the provider's response. *(source: screens/P08-venue-back-office.yaml#ADM-039)*

**Where the user goes next**

- → `ADM-038` Communication Service Command Center: *Returns to the board's landing screen*; calls `setChannelProvider`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel provider configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel provider untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel provider configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.; 422 The provider cannot be activated: credentials, connection or webhook verification failed, or the secret reference does not resolve. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
providers:
- Email - SendGrid - primary
- SMS - Etisalat gateway - primary
- WhatsApp - Meta Cloud API - primary
```

#### Permissions

- `setChannelProvider` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-039` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-039`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 2: Works in Channel & Provider Configuration → Configure the external/internal services used by TICVAI to deliver communications.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-039?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Legal Entity, Test Connection, Send Test Message, Validate Credentials, Test Webhook, Verify Delivery Receipt.
- [ ] Every transition is wired: `ADM-038`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-040` Sender Identity, Domain & Brand Configuration

**Manage the identities from which TICVAI communications are sent.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-040 |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/sender-identity-domain-brand-configuration-adm-040` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The identities messages are sent from: email sending domains with from and reply-to per brand (no-reply@venue.com, customerservice@venue.com), SMS sender ids per country, WhatsApp business accounts and numbers with approved templates, and verification status.

**Known correction pending (do not draw the wrong version)**

- **Every field (From name, From address, Reply-To, Phone number) is a select.** Why: Names and addresses are typed; only brand, provider and country are selects. *(source: screens/P08-venue-back-office.yaml#ADM-040; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Sending Domain | select field | — | — | — | — | — | — |
| From Name | select field | — | — | — | — | — | — |
| From Address | select field | — | — | — | — | — | — |
| Reply-To | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Region | select field | — | — | — | — | — | — |
| Sender ID | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Approved Use | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Application | select field | — | — | — | — | — | — |
| Platform | select field | — | — | — | — | — | — |
| Environment | select field | — | — | — | — | — | — |
| Business Account | select field | — | — | — | — | — | — |
| Phone Number | select field | — | — | — | — | — | — |
| Verification Status | select field | — | — | — | — | — | — |
| Approved Templates | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **From name and address**: Text fields; the domain must be verified (SPF, DKIM) before use. *(source: contracts/satellite/marketing-crm.yaml#setSenderIdentityDomain; DI-560)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-038` Communication Service Command Center: *Returns to the board's landing screen*; calls `setSenderIdentityDomain`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sender identity domain configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sender identity domain untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sender identity domain configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.; 422 The identity cannot take this status (not yet verified), the channel-specific fields are missing, or the provider does not serve this channel. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
identities:
- Coastal Aqua <no-reply@coastalaqua.ae> reply-to customerservice@coastalaqua.ae - verified
- SMS sender CoastalAqua (UAE) - approved
```

#### Permissions

- `setSenderIdentityDomain` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sender identity per brand (from and reply-to, e.g. no-reply@venue.com, customerservice@venue.com). Templates fully configurable per channel (email, SMS, WhatsApp): header, logo, footer and content, for consistent branded communications. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-560)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-040` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-040`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 4: Works in Sender Identity, Domain & Brand Configuration → Manage the identities from which TICVAI communications are sent.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-040?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-038`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-041` System Transactional Template Registry

**Maintain centralized system/transactional communication templates used by TICVAI operational modules. This screen must not replace CRM's marketing template builder.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-041 |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/system-transactional-template-registry-adm-041` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Attachments where applicable. Each needs an operation, or needs removing from the screen; this is the Phase …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The registry of system transactional templates the operational modules send (ticket confirmation, payment failed, waiver reminder, deposit due), per business event, channel, brand and language, with versions. It must not replace the CRM marketing template builder.

**Known correction pending (do not draw the wrong version)**

- **Only a list read is declared, and the fields are selects (Template ID, Template Name, Version).** Why: A registry that maintains templates needs a write; ids and names are not chosen from a list. *(source: contracts/satellite/marketing-crm.yaml#listSystemTransactionalTemplate; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Template ID | select field | — | — | — | — | — | — |
| Template Name | select field | — | — | — | — | — | — |
| Business Event | select field | — | — | — | — | — | — |
| Source Module | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Version | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Ownership | segmented control | — | Platform · Crm | `listSystemTransactionalTemplate` ?ownership |
| Source module | select | — | Crm · Ticketing · Membership · Waiver · Group sales · Customer service · Finance · Wallet · Resource management · Access control · Other | `listSystemTransactionalTemplate` ?sourceModule |
| Business event | text field | — | — | `listSystemTransactionalTemplate` ?businessEvent |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listSystemTransactionalTemplate` ?channel |
| Brand | picker: choose a brand | — | — | `listSystemTransactionalTemplate` ?brandId |
| Language | text field | — | — | `listSystemTransactionalTemplate` ?language |
| Status | segmented control | — | Draft · Published · Archived | `listSystemTransactionalTemplate` ?status |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Attachments where applicable (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Template row**: Template, business event, source module, channel, languages (missing flagged), version, status. *(source: contracts/satellite/marketing-crm.yaml#listSystemTransactionalTemplate)*

**Data it reads**: `listSystemTransactionalTemplate` (onLoad, System Transactional Template Registry)

**Where the user goes next**

- → `ADM-038` Communication Service Command Center: *Returns to the board's landing screen*; calls `listSystemTransactionalTemplate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The system transactional template configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the system transactional template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No system transactional template configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
templates:
- TICKET_ISSUED - ticketing - email/WhatsApp - EN AR - v5
- PAYMENT_FAILED - orders - email - EN AR - v2
- WAIVER_INCOMPLETE - waiver - email/SMS - EN - v1 (AR missing)
```

#### Permissions

- `listSystemTransactionalTemplate` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sender identity per brand (from and reply-to, e.g. no-reply@venue.com, customerservice@venue.com). Templates fully configurable per channel (email, SMS, WhatsApp): header, logo, footer and content, for consistent branded communications. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-560)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-041` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-041`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 6: Works in System Transactional Template Registry → Maintain centralized system/transactional communication templates used by TICVAI operational modules. This screen must not replace CRM's marketing template builder.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-041?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Attachments where applicable.
- [ ] Every transition is wired: `ADM-038`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-042` Business Event & Notification Trigger Mapping

**Map TICVAI business events to the operational communications they should generate. This is the core of the event-driven communication architecture.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-042 |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/business-event-notification-trigger-mapping-adm-042` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Product, Venue, Customer, Channel, Transaction Status, Membership, Booking Type. Each needs an operation, or … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Map business events (OrderConfirmed, TicketIssued, TicketScanned, PaymentFailed, WaiverIncomplete) to the operational communications each generates. Triggers key off precise event states.

**Known correction pending (do not draw the wrong version)**

- **The action bar is buttons named Product, Event, Venue, Customer, Channel, Transaction Status, Membership, Booking Type.** Why: These are condition dimensions (filters or condition fields), not actions; and no write operation is declared. *(source: screens/P08-venue-back-office.yaml#ADM-042; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Source module | select | — | Crm · Ticketing · Membership · Waiver · Group sales · Customer service · Finance · Wallet · Resource management · Access control · Other | `listBusinessEventNotification` ?sourceModule |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listBusinessEventNotification` ?channel |
| Status | segmented control | — | Active · Inactive | `listBusinessEventNotification` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product (primary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |
| Customer (secondary button) | navigation or local | — | — | — | — |
| Channel (secondary button) | navigation or local | — | — | — | — |
| Transaction Status (secondary button) | navigation or local | — | — | — | — |
| Membership (secondary button) | navigation or local | — | — | — | — |
| Booking Type (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Mapping row**: Event, state, conditions (product, venue, channel, booking type), template, timing. *(source: contracts/satellite/marketing-crm.yaml#listBusinessEventNotification; DI-561)*

**Data it reads**: `listBusinessEventNotification` (onLoad, Business Event & Notification Trigger Mapping)

**Where the user goes next**

- → `ADM-038` Communication Service Command Center: *Returns to the board's landing screen*; calls `listBusinessEventNotification`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The business event notification list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the business event notification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No business event notification yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the business event notification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
mapping: TicketScanned (first entry of the day) -> post-visit survey after 3 hours
```

#### Permissions

- `listBusinessEventNotification` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Notification triggers must key off precise event states where needed: a post-visit survey only when the ticket was actually scanned/used, whereas a "how was your experience" follow-up can trigger off the sale. Trigger mapping must expose such event states. *(agreed · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-561)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-042` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-042`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 8: Works in Business Event & Notification Trigger Mapping → Map TICVAI business events to the operational communications they should generate. This is the core of the event-driven communication architecture.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-042?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product, Event, Venue, Customer, Channel, Transaction Status, Membership, Booking Type.
- [ ] Every transition is wired: `ADM-038`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-043` Routing, Priority, Throttling & Fallback Rules

**Determine how TICVAI delivers a message after a communication requirement has been created.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-043 |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure based on; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/routing-priority-throttling-fallback-rules-adm-043` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** How a message is delivered once required: ordered providers per channel, country, brand, message class, priority and recipient type; throttles (per second, per minute, provider, brand, event); fallback channel.

**Known correction pending (do not draw the wrong version)**

- **Only a list read; throttle values are selects.** Why: Rates are numbers and the screen needs a write. *(source: contracts/satellite/marketing-crm.yaml#listRoutingPriorityThrottling; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Message Type | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Recipient Type | select field | — | — | — | — | — | — |
| Cost | select field | — | — | — | — | — | — |
| Provider Health | select field | — | — | — | — | — | — |
| Messages per second | select field | — | — | — | — | — | — |
| Messages per minute | select field | — | — | — | — | — | — |
| Provider limit | select field | — | — | — | — | — | — |
| Brand limit | select field | — | — | — | — | — | — |
| Event limit | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listRoutingPriorityThrottling` ?channel |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listRoutingPriorityThrottling` ?country |
| Brand | picker: choose a brand | — | — | `listRoutingPriorityThrottling` ?brandId |
| Priority class | radio group | — | P1 · P2 · P3 · P4 | `listRoutingPriorityThrottling` ?priorityClass |

#### Outputs: what the screen shows and produces

**Data it reads**: `listRoutingPriorityThrottling` (onLoad, Routing, Priority, Throttling & Fallback Rules)

**Where the user goes next**

- → `ADM-038` Communication Service Command Center: *Returns to the board's landing screen*; calls `listRoutingPriorityThrottling`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The routing priority throttling configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the routing priority throttling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No routing priority throttling configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: WhatsApp, UAE, transactional, Critical -> Meta primary, fallback SMS after 2 minutes, 200 msg/s
```

#### Permissions

- `listRoutingPriorityThrottling` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-043` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-043`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 10: Works in Routing, Priority, Throttling & Fallback Rules → Determine how TICVAI delivers a message after a communication requirement has been created.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-043?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-038`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-044` Consent, Preference & Communication Policy Enforcement

**Create a central enforcement layer ensuring communications respect the appropriate communication rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-044 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/consent-preference-communication-policy-enforcement-adm-044` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The central enforcement layer: for each communication, its class, channel, the consent and preference read from CRM at that moment, and whether it was allowed or blocked and why. Transactional messages pass without marketing consent; marketing is blocked without it; suppression always wins.

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a guest-checkout opt-in sufficient marketing consent?** → Drawn default stands (answer: "From WEB-011: the checkout opt-in, unticked by default, recorded with source checkout"): Treated as consent with source checkout; shown as such in the decision row. *(decided by Chinmay, 2026-10-02; DEC-276 / CHG-NOTE-002)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Decision | radio group | — | Allowed · Blocked · Rerouted · Suppressed | `listConsentPreferenceCommunication` ?decision |
| Message class | radio group | — | Transactional · Operational · Service · Marketing | `listConsentPreferenceCommunication` ?messageClass |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listConsentPreferenceCommunication` ?channel |
| Subject | picker: choose a subject | — | — | `listConsentPreferenceCommunication` ?subjectId |
| From | date and time picker | — | — | `listConsentPreferenceCommunication` ?from |
| To | date and time picker | — | — | `listConsentPreferenceCommunication` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Decision row**: Time, message class, channel, consent read (Given, Withdrawn, Not asked), preference, decision and reason. *(source: contracts/satellite/marketing-crm.yaml#listConsentPreferenceCommunication; DI-562)*

**Data it reads**: `listConsentPreferenceCommunication` (onLoad, Consent, Preference & Communication Policy Enforcement)

**Where the user goes next**

- → `ADM-038` Communication Service Command Center: *Returns to the board's landing screen*; calls `listConsentPreferenceCommunication`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consent preference communication list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consent preference communication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consent preference communication yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the consent preference communication are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
decisions:
- MKT-AUTUMN to Rahul Menon - WhatsApp - consent Withdrawn - blocked
- TKT-CONFIRM to Rahul Menon - WhatsApp - transactional - allowed
```

#### Permissions

- `listConsentPreferenceCommunication` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Consent and communication preference tracking records marketing/newsletter opt-in status per customer. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-562)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-044` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-044`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 12: Works in Consent, Preference & Communication Policy Enforcement → Create a central enforcement layer ensuring communications respect the appropriate communication rules.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-044?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-038`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-045` Delivery Queue, Failure & Retry Management

**Provide technical/operations teams with visibility into communications currently being processed or failing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-045 |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/delivery-queue-failure-retry-management-adm-045` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Communications being processed or failing across the platform: queue state, attempts, last failure, counts per state, with retry and channel fallback.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Pending · Processing · Sent · Delivered · Failed · Retrying · Dead lettered · Cancelled | `listDeliveryQueueFailure` ?status |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listDeliveryQueueFailure` ?channel |
| Source module | select | — | Crm · Ticketing · Membership · Waiver · Group sales · Customer service · Finance · Wallet · Resource management · Access control · Other | `listDeliveryQueueFailure` ?sourceModule |
| Business event | text field | — | — | `listDeliveryQueueFailure` ?businessEvent |
| Provider | picker: choose a provider | — | — | `listDeliveryQueueFailure` ?providerId |
| Priority | radio group | — | P1 · P2 · P3 · P4 | `listDeliveryQueueFailure` ?priority |
| Failure category | select | — | Provider unavailable · Invalid address · Invalid mobile · Rate limited · Authentication error · Template rejected · Timeout · Consent block · Unknown error | `listDeliveryQueueFailure` ?failureCategory |
| From | date and time picker | — | — | `listDeliveryQueueFailure` ?from |
| To | date and time picker | — | — | `listDeliveryQueueFailure` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every delivery queue failure** (data table, from `listDeliveryQueueFailure`)

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Pending, Processing, Sent, Delivered, Failed, Retrying… | — |
| Communication | text | marketing.message_dispatch id. |
| Source module | chip: Crm, Ticketing, Membership, Waiver, Group sales, Customer service… | — |
| Business event | text | The originating event type, e.g. TicketIssued. |
| Recipient | text | Address or number, masked (e.g. j*@example.com) unless the caller holds GUEST_VIEW_PII. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Template | grouped details | — |
| Provider | grouped details | — |
| Priority | chip: P1, P2, P3, P4 | — |
| Created at | 1 Oct 2026, 14:30 | — |
| Status | chip: Pending, Processing, Sent, Delivered, Failed, Retrying… | — |
| Attempts | 1,234 | — |

**The selected delivery queue failure** (detail panel): The pack groups this record's detail under its own headings: “Attempt 1”, “Wait 1 minute”, “Attempt 2”, “Wait 5 minutes”, “Attempt 3”, “Authorized administrators can”.

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Pending, Processing, Sent, Delivered, Failed, Retrying… | — |
| Communication | text | marketing.message_dispatch id. |
| Source module | chip: Crm, Ticketing, Membership, Waiver, Group sales, Customer service… | — |
| Business event | text | The originating event type, e.g. TicketIssued. |
| Recipient | text | Address or number, masked (e.g. j*@example.com) unless the caller holds GUEST_VIEW_PII. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Template | grouped details | — |
| Provider | grouped details | — |
| Priority | chip: P1, P2, P3, P4 | — |
| Created at | 1 Oct 2026, 14:30 | — |
| Status | chip: Pending, Processing, Sent, Delivered, Failed, Retrying… | — |
| Attempts | 1,234 | — |

**Data it reads**: `listDeliveryQueueFailure` (onLoad, Delivery Queue, Failure & Retry Management)

**Where the user goes next**

- → `ADM-038` Communication Service Command Center: *Returns to the board's landing screen*; calls `listDeliveryQueueFailure`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delivery queue failure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delivery queue failure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No delivery queue failure yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the delivery queue failure are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `BO-791`: Same queue scoped to one venue.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
  queued: 3420
  retrying: 210
  failed: 96
  deadLetter: 4
```

#### Permissions

- `listDeliveryQueueFailure` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-045` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-045`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 14: Works in Delivery Queue, Failure & Retry Management → Provide technical/operations teams with visibility into communications currently being processed or failing.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-045?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-038`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-046` Provider Health, Usage & Cost Monitoring

**Monitor the operational and commercial performance of communication providers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-046 |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/provider-health-usage-cost-monitoring-adm-046` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Provider performance and cost: KPIs per provider, usage and cost by channel, tenant or country, threshold breaches. Cost is shown in the currency billed.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search provider health usage | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by channel, provider, brand, venue, module, country and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listProviderHealthUsage` ?channel |
| Provider | picker: choose a provider | — | — | `listProviderHealthUsage` ?providerId |
| Brand | picker: choose a brand | — | — | `listProviderHealthUsage` ?brandId |
| Module | select | — | Crm · Ticketing · Membership · Waiver · Group sales · Customer service · Finance · Wallet · Resource management · Access control · Other | `listProviderHealthUsage` ?module |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listProviderHealthUsage` ?country |
| Message class | radio group | — | Transactional · Operational · Service · Marketing | `listProviderHealthUsage` ?messageClass |
| Group by | select | — | Channel · Provider · Brand · Venue · Module · Country · Message class · Campaign · Event · Business unit | `listProviderHealthUsage` ?groupBy |
| From | date and time picker | — | — | `listProviderHealthUsage` ?from |
| To | date and time picker | — | — | `listProviderHealthUsage` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Every provider health usage** (data table, from `listProviderHealthUsage`)

| Shows | Format | Notes |
|---|---|---|
| Volume | 1,234 | — |
| Success rate | 12.5% | — |
| Failure rate | 12.5% | — |
| Average delivery seconds | 1,234.5 | — |
| Average API latency seconds | 1,234.5 | — |
| Availability rate | 12.5% | — |
| Retries | 1,234 | — |
| Fallback count | 1,234 | Messages delivered through a fallback provider or channel. |
| Cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Cost per message | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**The selected provider health usage** (detail panel): The pack groups this record's detail under its own headings: “Health”, “Warni”, “Cost Allocation”, “SLA Monitoring”.

| Shows | Format | Notes |
|---|---|---|
| Volume | 1,234 | — |
| Success rate | 12.5% | — |
| Failure rate | 12.5% | — |
| Average delivery seconds | 1,234.5 | — |
| Average API latency seconds | 1,234.5 | — |
| Availability rate | 12.5% | — |
| Retries | 1,234 | — |
| Fallback count | 1,234 | Messages delivered through a fallback provider or channel. |
| Cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Cost per message | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Data it reads**: `listProviderHealthUsage` (onLoad, Provider Health, Usage & Cost Monitoring)

**Where the user goes next**

- → `ADM-038` Communication Service Command Center: *Returns to the board's landing screen*; calls `listProviderHealthUsage`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provider health usage list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provider health usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provider health usage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the provider health usage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
providers:
- Meta WhatsApp - 412,000 messages - USD 3,296.00
- Etisalat SMS - 98,000 - AED 2,940.00
```

#### Permissions

- `listProviderHealthUsage` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-046` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-046`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 16: Works in Provider Health, Usage & Cost Monitoring → Monitor the operational and commercial performance of communication providers.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-046?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-038`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-047` AI Delivery Optimization & Communication Platform Diagnostics

**Provide an AI intelligence layer focused specifically on communication infrastructure performance, not CRM marketing strategy.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task VM-ADM-047 |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-delivery-optimization-communication-platform-diagnost-adm-047` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** AI diagnostics for the communication infrastructure (not marketing strategy): health summary, detected provider incidents with probable cause, recommendations a person accepts.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listDeliveryCommunicationPlatform` ?channel |
| From | date and time picker | — | — | `listDeliveryCommunicationPlatform` ?from |
| To | date and time picker | — | — | `listDeliveryCommunicationPlatform` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every delivery optimization communication** (data table, from `listDeliveryCommunicationPlatform`)

| Shows | Format | Notes |
|---|---|---|
| Health summary | text | — |
| Incidents | list or chips (count when long) | — |
| Failure groups | list or chips (count when long) | Failures grouped by probable root cause. |
| Recommendations | list or chips (count when long) | — |
| Forecasts | list or chips (count when long) | — |
| Automated actions | list or chips (count when long) | — |

**The selected delivery optimization communication** (detail panel): The pack groups this record's detail under its own headings: “Administrators can ask”, “Potential Provider Incident”, “Automation Governance”, “Backend Screen Primary Responsibility”, “Platform communication”, “Marketing & CRM owns”.

| Shows | Format | Notes |
|---|---|---|
| Health summary | text | — |
| Incidents | list or chips (count when long) | — |
| Failure groups | list or chips (count when long) | Failures grouped by probable root cause. |
| Recommendations | list or chips (count when long) | — |
| Forecasts | list or chips (count when long) | — |
| Automated actions | list or chips (count when long) | — |

**Data it reads**: `listDeliveryCommunicationPlatform` (onLoad, AI Delivery Optimization & Communication Platform …)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delivery optimization communication list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delivery optimization communication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No delivery optimization communication yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the delivery optimization communication are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
finding: Bounce rate on coastalaqua.ae rose to 4% after DKIM key rotation - recommend re-verifying domain
```

#### Permissions

- `listDeliveryCommunicationPlatform` → `MARKETING_VIEW` (read) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| 4.1.16 | Analyze menu performance and profitability. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.19 | Recommend actions to reduce waste and spoilage. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.20 | Recommend pricing and promotion strategies. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.8.15 | AI predicts potential food waste and recommends actions. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 5.4.24 | Segment customers automatically. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.27 | Recommend staffing adjustments, ride allocation, and queue balancing. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.36 | The system shall estimate queue wait times using historical and real-time operational data. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 8.9.9 | AI shall identify operational risks, anomalies, congestion, capacity issues, device failures, staffing shortages, and service disruptions and provide recommendations. | Unified Operations Dashboard | CONTRACTED | `requestSuggestion` |
| 15.4.7 | Inventory Optimization - System shall optimize inventory levels. | Inventory Management | CONTRACTED_PARTIAL | `requestSuggestion` |
| 22.2.25 | AI Audience Classification | Marketing & CRM | CONTRACTED | `requestSuggestion` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-047` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-047`
- Workshop pack: Communication & Notification Platform Services_Reference.pdf board 1
- Flow F133 *Communication & Notification Platform Services board 1: Communication Service …*, step 18: Works in AI Delivery Optimization & Communication Platform Diagnostics → Provide an AI intelligence layer focused specifically on communication infrastructure performance, not CRM marketing strategy.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-047?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_VIEW`.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listBusinessEventNotification": {"method":"GET","path":"/business-event-notification","contract":"marketing-crm","summary":"Business Event & Notification Trigger Mapping","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sourceModule","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCommunicationService": {"method":"GET","path":"/communication-service","contract":"marketing-crm","summary":"Communication Service Command Center","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"CommunicationServiceCommandCenterView"},
"listConsentPreferenceCommunication": {"method":"GET","path":"/consent-preference-communication","contract":"marketing-crm","summary":"Consent, Preference & Communication Policy Enforcement","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"decision","in":"query","required":false},{"name":"messageClass","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"subjectId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDeliveryCommunicationPlatform": {"method":"GET","path":"/delivery-communication-platform","contract":"marketing-crm","summary":"AI Delivery Optimization & Communication Platform Diagnostics","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"AiDeliveryOptimizationCommunicationPlatformDiagnostiView"},
"listDeliveryQueueFailure": {"method":"GET","path":"/delivery-queue-failure","contract":"marketing-crm","summary":"Delivery Queue, Failure & Retry Management","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"sourceModule","in":"query","required":false},{"name":"businessEvent","in":"query","required":false},{"name":"providerId","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":"failureCategory","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProviderHealthUsage": {"method":"GET","path":"/provider-health-usage","contract":"marketing-crm","summary":"Provider Health, Usage & Cost Monitoring","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"channel","in":"query","required":false},{"name":"providerId","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"messageClass","in":"query","required":false},{"name":"groupBy","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"ProviderHealthUsageCostMonitoringView"},
"listRoutingPriorityThrottling": {"method":"GET","path":"/routing-priority-throttling","contract":"marketing-crm","summary":"Routing, Priority, Throttling & Fallback Rules","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"priorityClass","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSystemTransactionalTemplate": {"method":"GET","path":"/system-transactional-template","contract":"marketing-crm","summary":"System Transactional Template Registry","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"ownership","in":"query","required":false},{"name":"sourceModule","in":"query","required":false},{"name":"businessEvent","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"setChannelProvider": {"method":"PUT","path":"/channel-provider","contract":"marketing-crm","summary":"Channel & Provider Configuration","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelProviderConfigurationInput","responds":"ChannelProviderConfigurationView"},
"setSenderIdentityDomain": {"method":"PUT","path":"/sender-identity-domain","contract":"marketing-crm","summary":"Sender Identity, Domain & Brand Configuration","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SenderIdentityDomainBrandConfigurationInput","responds":"SenderIdentityDomainBrandConfigurationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiDeliveryOptimizationCommunicationPlatformDiagnostiView": {"type":"object","x-ticvai-persistence":"none — projection over ai.suggestion, marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)","description":"AI findings over the communication platform for the window; empty arrays when AI processing is off.","required":["generatedAt","incidents","recommendations"],"properties":{"generatedAt":{"type":"string","format":"date-time"},"healthSummary":{"type":"string"},"incidents":{"type":"array","items":{"type":"object","required":["title","detectedAt"],"properties":{"title":{"type":"string"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"providerId":{"type":"string","format":"uuid"},"country":{"type":"string","pattern":"^[A-Z]{2}$"},"messageClass":{"type":"string","enum":["transactional","operational","service","marketing"]},"sourceModule":{"type":"string","enum":["crm","ticketing","membership","waiver","groupSales","customerService","finance","wallet","resourceManagement","accessControl","other"]},"baselineFailureRate":{"type":"number","minimum":0,"maximum":1},"currentFailureRate":{"type":"number","minimum":0,"maximum":1},"affectedMessages":{"type":"integer","minimum":0},"failoverAvailable":{"type":"boolean"},"probableRootCause":{"type":"string"},"detectedAt":{"type":"string","format":"date-time"}}}},"failureGroups":{"type":"array","description":"Failures grouped by probable root cause.","items":{"type":"object","required":["probableRootCause","count"],"properties":{"probableRootCause":{"type":"string"},"failureCategory":{"type":"string","enum":["providerUnavailable","invalidAddress","invalidMobile","rateLimited","authenticationError","templateRejected","timeout","consentBlock","unknownError"]},"providerId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"count":{"type":"integer","minimum":0},"firstSeenAt":{"type":"string","format":"date-time"}}}},"recommendations":{"type":"array","items":{"type":"object","required":["kind","summary"],"properties":{"kind":{"type":"string","enum":["routing","cost","senderAnomaly"]},"summary":{"type":"string"},"evidence":{"type":"string"},"estimatedMonthlySaving":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["proposed","applied","dismissed"]}}}},"forecasts":{"type":"array","items":{"type":"object","required":["driver","date","forecastVolume"],"properties":{"driver":{"type":"string","enum":["majorEvent","ticketRelease","membershipRenewal","groupArrival","waiverDeadline"]},"referenceId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"date":{"type":"string","format":"date"},"forecastVolume":{"type":"integer","minimum":0},"capacitySufficient":{"type":"boolean"}}}},"automatedActions":{"type":"array","items":{"type":"object","required":["action","takenAt"],"properties":{"action":{"type":"string","enum":["providerFailover","queueScaling","retryAdjustment","operationalAlert"]},"summary":{"type":"string"},"takenAt":{"type":"string","format":"date-time"}}}}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"BusinessEventNotificationTriggerMappingView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.business_event (new), marketing.message_trigger, marketing.message_trigger_condition (new), marketing.message_template","description":"One registered business event and the communications mapped to it; also the body of setBusinessEventMapping (readOnly fields are ignored on write).\n","required":["eventId","eventType","sourceModule","priority","status","communications"],"properties":{"eventId":{"type":"string","format":"uuid","readOnly":true,"description":"The event registry entry."},"eventType":{"type":"string","description":"Registered event name, e.g. TicketIssued, MembershipExpiring."},"sourceModule":{"type":"string","enum":["crm","ticketing","membership","waiver","groupSales","customerService","finance","wallet","resourceManagement","accessControl","other"]},"eventState":{"type":"string","readOnly":true,"description":"The precise state that fires it (e.g. scanned, not merely sold)."},"payloadFields":{"type":"array","readOnly":true,"description":"Fields the event carries, available to templates as variables.","items":{"type":"string"}},"priority":{"type":"string","enum":["P1","P2","P3","P4"]},"status":{"type":"string","enum":["active","inactive"]},"communications":{"type":"array","description":"One entry per mapped message (message_trigger row); several entries make a multi-channel or scheduled trigger.","items":{"type":"object","required":["channel","templateId","offsetMinutes","isActive"],"properties":{"triggerId":{"type":"string","format":"uuid","description":"Present on an existing mapping; omit to create one."},"channel":{"$ref":"#/components/schemas/MessageChannel"},"templateId":{"type":"string","format":"uuid"},"templateName":{"type":"string","readOnly":true},"offsetMinutes":{"type":"integer","description":"0 = immediately; negative = before the anchor (T-30 days = -43200)."},"anchor":{"type":"string","enum":["eventTime","performanceStart","visitEnd"]},"conditions":{"type":"array","description":"All must hold (e.g. customer has a valid email and email is permitted; event within 24 hours).","items":{"type":"object","required":["dimension","operator"],"properties":{"dimension":{"type":"string","enum":["product","event","venue","brand","customer","channel","time","transactionStatus","membership","bookingType"]},"operator":{"type":"string","enum":["equals","notEquals","in","withinMinutes","isValid","isPermitted"]},"value":{"type":"string"}}}},"isActive":{"type":"boolean"}}}}}},
"ChannelProviderConfigurationInput": {"type":"object","x-ticvai-persistence":"marketing.communication_provider","x-ticvai-record-definition":"For each provider","description":"One delivery provider on one channel (the pack's \"For each provider\" record). Rate limits, timeout and the retry policy apply to every message routed through it; routing between providers is `listRoutingPriorityThrottling`.\n","required":["providerName","channel","account","environment","credentialsSecretRef","role","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"providerName":{"type":"string","maxLength":120},"channel":{"$ref":"#/components/schemas/MessageChannel"},"account":{"type":"string","maxLength":200,"description":"The account or sub-account identifier at the provider."},"environment":{"type":"string","enum":["production","sandbox"]},"region":{"type":"string","description":"Provider data region (e.g. eu-west, me-central); also a routing selector."},"country":{"type":"string","pattern":"^[A-Z]{2}$","description":"ISO 3166-1 alpha-2; set when this provider serves one country only."},"brandId":{"type":"string","format":"uuid","description":"Set when this provider serves one brand only."},"legalEntityId":{"type":"string","format":"uuid","description":"Set when this provider serves one legal entity only."},"credentialsSecretRef":{"type":"string","description":"Reference into the secret store; the secret itself is never sent, stored or shown."},"apiConfiguration":{"type":"object","additionalProperties":true,"description":"Non-secret API settings (base URL, API version, provider-specific options)."},"webhookConfiguration":{"type":"object","properties":{"callbackUrl":{"type":"string","format":"uri"},"signingSecretRef":{"type":"string","description":"Reference into the secret store for the webhook signing key."}}},"rateLimitPerSecond":{"type":"integer","minimum":1},"rateLimitPerMinute":{"type":"integer","minimum":1},"timeoutSeconds":{"type":"integer","minimum":1},"retryPolicy":{"type":"object","description":"Waits between attempts, then what happens when they are spent (e.g. 1 min, 5 min, then fallback provider).","required":["waitsSeconds","onExhausted"],"properties":{"waitsSeconds":{"type":"array","maxItems":10,"items":{"type":"integer","minimum":0}},"onExhausted":{"type":"string","enum":["fallbackProvider","deadLetter"]}}},"role":{"type":"string","enum":["primary","secondary","emergencyFallback"]},"priority":{"type":"integer","minimum":1,"description":"Order among providers with the same role and selectors; 1 is tried first."},"status":{"type":"string","enum":["active","standby","degraded","suspended","disabled"]},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ChannelProviderConfigurationView": {"x-ticvai-persistence":"none — the marketing.communication_provider row plus its latest verification","description":"The stored provider record and the outcome of the checks run on save.","allOf":[{"$ref":"#/components/schemas/ChannelProviderConfigurationInput"},{"type":"object","properties":{"lastVerification":{"type":"object","readOnly":true,"properties":{"checkedAt":{"type":"string","format":"date-time"},"credentialsValid":{"type":"boolean"},"connectionOk":{"type":"boolean"},"webhookOk":{"type":"boolean"},"deliveryReceiptOk":{"type":"boolean"},"message":{"type":"string"}}}}}]},
"CommunicationServiceCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)","description":"Platform KPIs and breakdowns for the communication service over the requested window. Counts are messages (one dispatch = one message on one channel), not recipients.\n","required":["windowFrom","windowTo","messagesProcessed","byChannel","byModule"],"properties":{"windowFrom":{"type":"string","format":"date-time"},"windowTo":{"type":"string","format":"date-time"},"messagesProcessed":{"type":"integer","minimum":0,"description":"Messages accepted by the service in the window (the pack's \"Messages Processed Today\")."},"delivered":{"type":"integer","minimum":0},"failed":{"type":"integer","minimum":0},"pending":{"type":"integer","minimum":0},"retrying":{"type":"integer","minimum":0},"averageDeliverySeconds":{"type":"number","minimum":0,"description":"Mean time from acceptance to provider-confirmed delivery, in (fractional) seconds."},"providerAvailabilityRate":{"type":"number","minimum":0,"maximum":1,"description":"Share of the window the active providers were reachable, weighted by volume."},"byChannel":{"type":"array","description":"Sent volume and health per channel, one row per provider on it (the pack's channel tiles and Channel Health table).","items":{"type":"object","required":["channel","sent"],"properties":{"channel":{"$ref":"#/components/schemas/MessageChannel"},"providerId":{"type":"string","format":"uuid"},"providerName":{"type":"string"},"sent":{"type":"integer","minimum":0},"successRate":{"type":"number","minimum":0,"maximum":1},"averageLatencySeconds":{"type":"number","minimum":0},"health":{"type":"string","enum":["healthy","warning","critical"]}}}},"byModule":{"type":"array","description":"Volume originating from each TICVAI module.","items":{"type":"object","required":["module","volume"],"properties":{"module":{"type":"string","enum":["crm","ticketing","membership","waiver","groupSales","customerService","finance","wallet","resourceManagement","accessControl","other"]},"volume":{"type":"integer","minimum":0},"successRate":{"type":"number","minimum":0,"maximum":1},"averageLatencySeconds":{"type":"number","minimum":0},"health":{"type":"string","enum":["healthy","warning","critical"]}}}},"alerts":{"type":"array","description":"Live operational alerts (failure-rate spikes, queued backlogs, providers near their rate limit).","items":{"type":"object","required":["kind","severity","message","raisedAt"],"properties":{"kind":{"type":"string","enum":["failureRateSpike","queueBacklog","rateLimitApproaching","providerDegraded","other"]},"severity":{"type":"string","enum":["info","warning","critical"]},"message":{"type":"string"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"providerId":{"type":"string","format":"uuid"},"raisedAt":{"type":"string","format":"date-time"}}}},"aiHealthSummary":{"type":"string","description":"AI-written plain-language summary of platform health; absent when AI processing is off for the tenant."}}},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPreferenceCommunicationPolicyEnforcementView": {"type":"object","x-ticvai-persistence":"marketing.communication_policy_decision","description":"One policy evaluation of one communication, with the inputs as they stood when it was evaluated. Append-only evidence; retained per the tenant's retention policy (ADR-0047). **Job note:** written by the dispatch worker behind `sendTransactionalMessage` and campaign sends (`launchCampaign`) as it evaluates each message, never by an operation of its own (decided 29 September, writers pass; DM6).\n","required":["id","communicationId","subjectId","messageClass","channel","decision","evaluatedAt"],"properties":{"id":{"type":"string","format":"uuid"},"communicationId":{"type":"string","description":"marketing.message_dispatch id."},"subjectId":{"type":"string","format":"uuid"},"messageClass":{"type":"string","enum":["transactional","operational","service","marketing"]},"channel":{"$ref":"#/components/schemas/MessageChannel"},"marketingConsent":{"$ref":"#/components/schemas/ConsentDecision"},"emailPreference":{"type":"boolean"},"smsPreference":{"type":"boolean"},"whatsappPreference":{"type":"boolean"},"pushPreference":{"type":"boolean"},"language":{"type":"string","description":"Preferred language (BCP 47) used to pick the template language."},"contactRestricted":{"type":"boolean","description":"A contact restriction (e.g. do-not-contact, legal hold) applied."},"jurisdiction":{"type":"string","pattern":"^[A-Z]{2}$","description":"Country whose policy was applied."},"suppressionReason":{"type":"string","enum":["unsubscribed","invalidEmail","invalidMobile","hardBounce","complaint","administrative"]},"decision":{"type":"string","enum":["allowed","blocked","rerouted","suppressed"]},"reasons":{"type":"array","description":"Why the decision was reached; empty when allowed with nothing notable.","items":{"type":"string","enum":["noMarketingConsent","channelPreferenceOff","optedOut","suppressed","contactRestricted","jurisdictionPolicy","channelUnavailable"]}},"reroutedToChannel":{"$ref":"#/components/schemas/MessageChannel"},"evaluatedAt":{"type":"string","format":"date-time"}}},
"DeliveryQueueFailureRetryManagementView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.message_template, marketing.communication_provider (new)","description":"One communication in the delivery queue and where it stands.","required":["communicationId","channel","status","attempts","createdAt"],"properties":{"communicationId":{"type":"string","description":"marketing.message_dispatch id."},"sourceModule":{"type":"string","enum":["crm","ticketing","membership","waiver","groupSales","customerService","finance","wallet","resourceManagement","accessControl","other"]},"businessEvent":{"type":"string","description":"The originating event type, e.g. TicketIssued."},"businessEventId":{"type":"string","description":"The originating event instance, kept so a failed message can be replayed with its context."},"recipient":{"type":"string","description":"Address or number, masked (e.g. j***@example.com) unless the caller holds GUEST_VIEW_PII."},"subjectId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"template":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"}}},"provider":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"priority":{"type":"string","enum":["P1","P2","P3","P4"]},"status":{"type":"string","enum":["pending","processing","sent","delivered","failed","retrying","deadLettered","cancelled"]},"attempts":{"type":"integer","minimum":0},"lastFailureCategory":{"type":"string","enum":["providerUnavailable","invalidAddress","invalidMobile","rateLimited","authenticationError","templateRejected","timeout","consentBlock","unknownError"]},"lastFailureMessage":{"type":"string"},"nextAttemptAt":{"type":"string","format":"date-time"},"createdAt":{"type":"string","format":"date-time"},"sentAt":{"type":"string","format":"date-time"}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProviderHealthUsageCostMonitoringView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)","description":"Provider reliability, usage and cost for the window and filters.","required":["windowFrom","windowTo","volume","providers"],"properties":{"windowFrom":{"type":"string","format":"date-time"},"windowTo":{"type":"string","format":"date-time"},"volume":{"type":"integer","minimum":0},"successRate":{"type":"number","minimum":0,"maximum":1},"failureRate":{"type":"number","minimum":0,"maximum":1},"averageDeliverySeconds":{"type":"number","minimum":0},"averageApiLatencySeconds":{"type":"number","minimum":0},"availabilityRate":{"type":"number","minimum":0,"maximum":1},"retries":{"type":"integer","minimum":0},"fallbackCount":{"type":"integer","minimum":0,"description":"Messages delivered through a fallback provider or channel."},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"costPerMessage":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providers":{"type":"array","description":"Provider comparison.","items":{"type":"object","required":["providerId","channel","volume"],"properties":{"providerId":{"type":"string","format":"uuid"},"providerName":{"type":"string"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"volume":{"type":"integer","minimum":0},"successRate":{"type":"number","minimum":0,"maximum":1},"averageDeliverySeconds":{"type":"number","minimum":0},"costPerThousand":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"health":{"type":"string","enum":["healthy","warning","critical"]}}}},"breakdown":{"type":"array","description":"Usage and cost per value of the groupBy dimension.","items":{"type":"object","required":["key","volume"],"properties":{"key":{"type":"string","description":"The dimension value's id or code."},"label":{"type":"string"},"volume":{"type":"integer","minimum":0},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"alerts":{"type":"array","items":{"type":"object","required":["kind","message","raisedAt"],"properties":{"kind":{"type":"string","enum":["budgetThreshold","successRateBelowTarget","latencyAboveTarget","slaBreach"]},"message":{"type":"string"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"providerId":{"type":"string","format":"uuid"},"raisedAt":{"type":"string","format":"date-time"}}}},"slaTargets":{"type":"array","description":"Contractual provider targets, only where configured.","items":{"type":"object","required":["providerId","metric","target"],"properties":{"providerId":{"type":"string","format":"uuid"},"metric":{"type":"string","enum":["successRate","availabilityRate","averageDeliverySeconds"]},"target":{"type":"number"},"observed":{"type":"number"},"met":{"type":"boolean"}}}},"aiRecommendations":{"type":"array","description":"Advisory provider changes on cost/performance trade-offs.","items":{"type":"string"}}}},
"RoutingPriorityThrottlingFallbackRulesView": {"type":"object","x-ticvai-persistence":"marketing.communication_routing_rule","description":"One routing rule, read by listRoutingPriorityThrottling and written by setCommunicationRoutingRule. Unset selectors match anything; a rule with more selectors set is more specific.\n","required":["id","channel","providers","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"channel":{"$ref":"#/components/schemas/MessageChannel"},"country":{"type":"string","pattern":"^[A-Z]{2}$"},"brandId":{"type":"string","format":"uuid"},"messageClass":{"type":"string","enum":["transactional","operational","service","marketing"]},"priorityClass":{"type":"string","enum":["P1","P2","P3","P4"]},"recipientType":{"type":"string","enum":["customer","partner","employee"]},"providers":{"type":"array","description":"Tried in order; a provider below minimum health is skipped.","items":{"type":"object","required":["providerId","role"],"properties":{"providerId":{"type":"string","format":"uuid"},"providerName":{"type":"string","readOnly":true},"role":{"type":"string","enum":["primary","secondary","emergencyFallback"]}}}},"skipUnhealthyProviders":{"type":"boolean","description":"Route past providers whose health is degraded or worse."},"costAware":{"type":"boolean","description":"Among providers meeting the service and compliance rules, prefer the cheapest."},"channelFallback":{"type":"array","description":"Alternate channels, in order, when delivery on this channel fails; used only where consent and preferences permit.","items":{"$ref":"#/components/schemas/MessageChannel"}},"throttle":{"type":"object","properties":{"messagesPerSecond":{"type":"integer","minimum":1},"messagesPerMinute":{"type":"integer","minimum":1},"brandMessagesPerMinute":{"type":"integer","minimum":1,"description":"Cap across every rule for the same brand."},"eventMessagesPerMinute":{"type":"integer","minimum":1,"description":"Cap per originating business event."}}},"isActive":{"type":"boolean"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"SenderIdentityDomainBrandConfigurationInput": {"type":"object","x-ticvai-persistence":"marketing.sender_identity","description":"One identity TICVAI sends from, bound to one brand. Fields apply by channel: email uses sendingDomain/fromName/fromAddress/replyTo; sms uses senderId/country/approvedUses; whatsapp uses businessAccount/phoneNumber/country; push uses application/platform/environment.\n","required":["channel","brandId","providerId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"channel":{"$ref":"#/components/schemas/MessageChannel"},"brandId":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid"},"region":{"type":"string"},"country":{"type":"string","pattern":"^[A-Z]{2}$","description":"ISO 3166-1 alpha-2 (required for sms and whatsapp)."},"providerId":{"type":"string","format":"uuid","description":"The marketing.communication_provider row this identity is registered with."},"sendingDomain":{"type":"string","maxLength":253},"fromName":{"type":"string","maxLength":120},"fromAddress":{"type":"string","format":"email"},"replyTo":{"type":"string","format":"email"},"senderId":{"type":"string","maxLength":15,"description":"Alphanumeric or numeric SMS sender ID as registered in the country."},"approvedUses":{"type":"array","description":"Communication classes this sender may carry.","items":{"type":"string","enum":["transactional","operational","service","marketing"]}},"businessAccount":{"type":"string","description":"WhatsApp business account identifier at the provider."},"phoneNumber":{"type":"string","pattern":"^\\+[1-9][0-9]{6,14}$","description":"E.164."},"application":{"type":"string","description":"Push application identifier (bundle id / package name)."},"platform":{"type":"string","enum":["ios","android","web"]},"environment":{"type":"string","enum":["production","sandbox"]},"status":{"type":"string","enum":["pendingVerification","verified","active","suspended","expired"],"description":"Set by verification except `active` and `suspended`, which a caller may request."},"approvedTemplateIds":{"type":"array","readOnly":true,"description":"WhatsApp templates the provider has approved for this number (marketing.message_template ids).","items":{"type":"string","format":"uuid"}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"SenderIdentityDomainBrandConfigurationView": {"x-ticvai-persistence":"none — the marketing.sender_identity row plus its verification timestamps","description":"The stored sender identity and when it was last verified.","allOf":[{"$ref":"#/components/schemas/SenderIdentityDomainBrandConfigurationInput"},{"type":"object","properties":{"verifiedAt":{"type":"string","format":"date-time","readOnly":true},"verificationExpiresAt":{"type":"string","format":"date-time","readOnly":true}}}]},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"SystemTransactionalTemplateRegistryView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.message_template, marketing.message_template_version (new), marketing.message_trigger","description":"One version of one template on one channel and language, with its content and variables.","required":["templateId","code","name","channel","language","version","status","ownership"],"properties":{"templateId":{"type":"string","format":"uuid","description":"marketing.message_template id."},"code":{"type":"string","description":"The human template ID (e.g. TICKET_CONFIRMATION)."},"name":{"type":"string"},"businessEvent":{"type":"string","description":"The registered business event this template answers (e.g. TicketIssued)."},"sourceModule":{"type":"string","enum":["crm","ticketing","membership","waiver","groupSales","customerService","finance","wallet","resourceManagement","accessControl","other"]},"channel":{"$ref":"#/components/schemas/MessageChannel"},"brandId":{"type":"string","format":"uuid"},"language":{"type":"string","description":"BCP 47 tag."},"version":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","published","archived"]},"ownership":{"type":"string","enum":["platform","crm"],"description":"platform = transactional template owned here; crm = marketing template owned by CRM."},"subject":{"type":"string"},"header":{"type":"string"},"body":{"type":"string"},"footer":{"type":"string"},"ctaLabel":{"type":"string"},"ctaUrl":{"type":"string","description":"May contain variables, e.g. {{TicketLink}}."},"attachmentKinds":{"type":"array","items":{"type":"string","enum":["ticketPdf","invoicePdf","walletPass","calendarInvite","waiverPdf"]}},"variables":{"type":"array","description":"Dynamic variables the content uses (e.g. CustomerName, OrderNumber, EventDate, AmountDue).","items":{"type":"string"}},"publishedAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}}
}
```
