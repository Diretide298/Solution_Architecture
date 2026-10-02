# WS26 — Customer Service board 2

**10 screens · 14 operations · 20 schemas · 2 permissions**

Platform P12 Venue Support · ships as **venue-management** ·
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
  `CASE_MANAGE, CASE_VIEW`. A control nobody can use must say so,
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
| `SUP-019` | Contact Center Operations Command Center | B–D | 2 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `SUP-020` | Queue Configuration & Management | B–D | 25 | 6 | 5 | 0 | 0 | 6 | — | notStarted (generated) |
| `SUP-021` | Intelligent Routing, Skills & Assignment Engine | B–D | 4 | 13 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `SUP-022` | SLA Policy & Service-Level Management | B–D | 18 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `SUP-023` | Agent Workload, Availability & Workforce Control | B–D | 5 | 26 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `SUP-024` | Escalation & Critical Case Monitor | B–D | 0 | 24 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `SUP-025` | Quality Management & Agent Evaluation | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `SUP-026` | Customer Satisfaction, Feedback & Voice of Customer | B–D | 0 | 0 | 6 | 3 | 1 | 0 | — | notStarted (generated) |
| `SUP-027` | Service Analytics & Root-Cause Intelligence | B–D | 0 | 4 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `SUP-028` | AI Contact Center Intelligence & Automation Studio | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**SUP-023, SUP-024, SUP-025, SUP-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SUP-019` Contact Center Operations Command Center

**Provide supervisors and management with a real-time view of customer-service operations across**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/contact-center-operations-command-center-sup-019` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Supervisors' real-time view of the contact centre: cases today, open, unassigned, customers waiting, critical, SLA at risk and breached, resolved, response and resolution times, first-contact resolution, CSAT, active agents and utilisation; volume by category (general support, refund, ticketing, membership).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search contact operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by channel → queue → agent → case — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Queue | picker: choose a queue | — | — | `listContact` ?queueId |
| Channel | select | — | Email · Phone · Live chat · Whatsapp · Web form · Mobile app · B2C portal · Social · Front desk | `listContact` ?channel |

#### Outputs: what the screen shows and produces

**Shown**

**Cases Today** (metric tile)

**Open Cases** (metric tile)

**Unassigned Cases** (metric tile)

**Customers Waiting** (metric tile)

**Critical Cases** (metric tile)

**SLA At Risk** (metric tile)

**SLA Breached** (metric tile)

**Cases Resolved Today** (metric tile)

**First Response Time** (metric tile)

**Average Resolution Time** (metric tile)

**First Contact Resolution** (metric tile)

**CSAT** (metric tile)

**Active Agents** (metric tile)

**Agent Utilization** (metric tile)

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Tiles**: Each tile drills into its filtered list; "customers waiting" counts queued conversations, not assistant ones. *(source: contracts/satellite/marketing-crm.yaml#listContact; DI-544)*

**Data it reads**: `listContact` (onLoad, Contact Center Operations Command Center)

**Where the user goes next**

- → `SUP-001` Venue Management Sign In: *Agent Login*
- → `SUP-020` Queue Configuration & Management: *Works in Queue Configuration & Management*; calls `listContact`
- → `SUP-021` Intelligent Routing, Skills & Assignment Engine: *Works in Intelligent Routing, Skills & Assignment Engine*; calls `listContact`
- → `SUP-022` SLA Policy & Service-Level Management: *Works in SLA Policy & Service-Level Management*; calls `listContact`
- → `SUP-023` Agent Workload, Availability & Workforce Control: *Works in Agent Workload, Availability & Workforce Control*; calls `listContact`
- → `SUP-024` Escalation & Critical Case Monitor: *Works in Escalation & Critical Case Monitor*; calls `listContact`
- → `SUP-025` Quality Management & Agent Evaluation: *Works in Quality Management & Agent Evaluation*; calls `listContact`
- → `SUP-026` Customer Satisfaction, Feedback & Voice of Customer: *Works in Customer Satisfaction, Feedback & Voice of Customer*; calls `listContact`
- → `SUP-027` Service Analytics & Root-Cause Intelligence: *Works in Service Analytics & Root-Cause Intelligence*; calls `listContact`
- → `SUP-028` AI Contact Center Intelligence & Automation Studio: *Works in AI Contact Center Intelligence & Automation Studio*; calls `listContact`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The contact operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the contact operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No contact operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the contact operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  casesToday: 64
  open: 23
  unassigned: 4
  waiting: 7
  slaAtRisk: 5
  breached: 2
  csat: 4.4
  utilisation: 78%
```

#### Permissions

- `listContact` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Supervisor dashboard: case volume by category (general support, refund, ticketing, membership) and status, quality scores per agent (resolution time and outcome vs SLA), customer-satisfaction results and week-over-week case-volume trends. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-544)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-019` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-019`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 1: Opens Contact Center Operations Command Center → Provide supervisors and management with a real-time view of customer-service operations across
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F135 branch at step 1 (expected): when Nothing has been set up on Contact Center Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F135 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SUP-001`, `SUP-020`, `SUP-021`, `SUP-022`, `SUP-023`, `SUP-024`, `SUP-025`, `SUP-026`, `SUP-027`, `SUP-028`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-020` Queue Configuration & Management

**Configure and operate the queues through which customer-service cases are organized.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/queue-configuration-management-sup-020` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Payments, Membership, Wallet, Group Sales Support, Access Control. Each needs an operation, or needs … Removed 2 October 2026 (CHG-WIR-005): listQueues reads ride and attraction virtual queues (queue contract); customer-service queues are listServiceQueues (declared) (design-notes correction …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Configure the customer-service queues: name, code (never changes), department, brand, venue, languages, channels, hours, priority, SLA profile, supervisor, backup queue, maximum workload, overflow, after-hours and VIP handling.

**Known correction pending (do not draw the wrong version)**

- **Name, code, thresholds and hours are select fields.** Why: Typed values. *(source: screens/P12-support-agent-console.yaml#SUP-020; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

**Fixed on main** (the package already carries these; draw what it says): listQueues (ride and attraction virtual queues, queue contract) is declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Queue Name | select field | — | — | — | — | — | — |
| Queue Code | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Languages | select field | — | — | — | — | — | — |
| Supported Channels | select field | — | — | — | — | — | — |
| Operating Hours | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| SLA Profile | select field | — | — | — | — | — | — |
| Supervisor | select field | — | — | — | — | — | — |
| Backup Queue | select field | — | — | — | — | — | — |
| Maximum workload | select field | — | — | — | — | — | — |
| Overflow threshold | select field | — | — | — | — | — | — |
| Escalation threshold | select field | — | — | — | — | — | — |
| After-hours behavior | select field | — | — | — | — | — | — |
| Backup routing | select field | — | — | — | — | — | — |
| VIP handling | select field | — | — | — | — | — | — |
| Emergency handling | select field | — | — | — | — | — | — |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listServiceQueues`. | `listServiceQueues` ?isActive |

**Form: Save service queue definition** (modal, opened by *Save service queue definition*; *Save service queue definition* calls `setServiceQueueDefinition`, *Cancel* sends nothing)

**Collects what `setServiceQueueDefinition` sends before it is called.** Required: `id`, `code`, `name`, `isActive`. Optional: `overflowWaitSeconds`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 60 | — | — | `setServiceQueueDefinition` body |
| Name `name` | text field | required | — | max length 150 | — | — | `setServiceQueueDefinition` body |
| Overflow wait seconds `overflowWaitSeconds` | number field (seconds) | optional | — | min 0 | — | The queue's overflow threshold; a case waiting longer marks the queue `critical`. | `setServiceQueueDefinition` body |
| Is active `isActive` | toggle | required | on | — | — | — | `setServiceQueueDefinition` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Retiring a queue that an active routing rule names, or that an unresolved case still waits in.

#### Outputs: what the screen shows and produces

**Shown**

**Every service queue** (data table, from `listServiceQueues`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Overflow wait seconds | 1,234 | The queue's overflow threshold; a case waiting longer marks the queue `critical`. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Payments (primary button) | navigation or local | — | — | — | — |
| Membership (secondary button) | navigation or local | — | — | — | — |
| Wallet (secondary button) | navigation or local | — | — | — | — |
| Group Sales Support (secondary button) | navigation or local | — | — | — | — |
| Access Control (secondary button) | navigation or local | — | — | — | — |
| Save service queue definition (secondary button) | `setServiceQueueDefinition` PUT `/service-queues` | ServiceQueue | ServiceQueue | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Retiring a queue that an active routing rule names, or that an unresolved case still waits in. | gated `CASE_MANAGE`; opens modal first |

**Data it reads**: `listServiceQueues` (onLoad, List customer-service queues)

**Where the user goes next**

- → `SUP-019` Contact Center Operations Command Center: *Returns to the board's landing screen*; calls `listServiceQueues`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Retiring a queue that an active routing rule names, or that an unresolved case still waits in. |

#### Consistency with other screens

- Match `BO-800`: Same queues.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
  name: Reservations
  code: RES
  languages:
  - EN
  - AR
  hours: 08:00-22:00
  overflow: 180 s to General
```

#### Permissions

- `listServiceQueues` → `CASE_VIEW` (read) · staff
- `setServiceQueueDefinition` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-020` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-020`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 2: Works in Queue Configuration & Management → Configure and operate the queues through which customer-service cases are organized.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-020?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Payments, Membership, Wallet, Group Sales Support, Access Control, Save service queue definition.
- [ ] Every transition is wired: `SUP-019`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-021` Intelligent Routing, Skills & Assignment Engine

**Determine the best agent or team to handle each customer request.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/intelligent-routing-skills-assignment-engine-sup-021` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The routing rules that pick the best agent or team: match category, channel, language, customer type, tier, venue, event, product and priority; route by skill, workload and availability; manual override is allowed and recorded.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Parent category id | picker: choose a parent category (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?parentCategoryId=` to `listCaseCategories`. | `listCaseCategories` ?parentCategoryId |
| Top level only | toggle | optional | off | — | — | Sends `?topLevelOnly=` to `listCaseCategories`. | `listCaseCategories` ?topLevelOnly |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listCaseCategories`. | `listCaseCategories` ?isActive |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listServiceQueues`. | `listServiceQueues` ?isActive |

#### Outputs: what the screen shows and produces

**Shown**

**Every case category** (data table, from `listCaseCategories`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Parent category | the name it points at, never the id | Set on a subcategory; null on a top-level category. |
| Default priority | chip: Low, Normal, High, Urgent | The priority a case in this category starts at before routing factors apply. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Every service queue** (data table, from `listServiceQueues`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Overflow wait seconds | 1,234 | The queue's overflow threshold; a case waiting longer marks the queue `critical`. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCaseCategories` (onLoad, List case categories and subcategories); `listServiceQueues` (onLoad, List customer-service queues)

**Where the user goes next**

- → `SUP-019` Contact Center Operations Command Center: *Returns to the board's landing screen*; calls `setIntelligentRoutingSkill`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The intelligent routing skills list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the intelligent routing skills untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No intelligent routing skills yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the intelligent routing skills are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. |

#### Consistency with other screens

- Match `SUP-012`: The routing preview there applies these rules.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Arabic + Membership > Renewal + Gold -> Membership & billing, skill Arabic, least load
```

#### Permissions

- `setIntelligentRoutingSkill` → `CASE_MANAGE` (configure) · staff
- `listCaseCategories` → `CASE_VIEW` (read) · staff
- `listServiceQueues` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Intelligent routing assigns cases by skill, language, availability, workload and priority, showing an assignment preview that the user can manually override before confirming. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-545)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-021` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-021`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 4: Works in Intelligent Routing, Skills & Assignment Engine → Determine the best agent or team to handle each customer request.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `SUP-019`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-022` SLA Policy & Service-Level Management

**Define and monitor service-level commitments for different customer-service scenarios.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/sla-policy-service-level-management-sup-022` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Venue operating hours. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Service-level commitments and their performance: first, next and resolution response; internal escalation; refund processing; complaint resolution; business hours; and the cases forecast to breach.

**Fixed on main** (the package already carries these; draw what it says): Only the performance read is declared; setSlaPolicy is not. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| First Response SLA | select field | — | — | — | — | — | — |
| Next Response SLA | select field | — | — | — | — | — | — |
| Resolution SLA | select field | — | — | — | — | — | — |
| Internal Escalation SLA | select field | — | — | — | — | — | — |
| Refund Processing SLA | select field | — | — | — | — | — | — |
| Complaint Resolution SLA | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Sla policy | picker: choose a sla policy | — | — | `listSlaPolicyService` ?slaPolicyId |
| Priority | radio group | — | Low · Normal · High · Urgent | `listSlaPolicyService` ?priority |
| Kind | select | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | `listSlaPolicyService` ?kind |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listSlaPolicyService` ?channel |
| Queue | picker: choose a queue | — | — | `listSlaPolicyService` ?queueId |
| From | date and time picker | — | — | `listSlaPolicyService` ?from |
| To | date and time picker | — | — | `listSlaPolicyService` ?to |

**Form: Save SLA policy** (modal, opened by *Save SLA policy*; *Save SLA policy* calls `setSlaPolicy`, *Cancel* sends nothing)

**Collects what `setSlaPolicy` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `setSlaPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setSlaPolicy` body |
| Code `code` | text field | required | — | max length 100 | — | — | `setSlaPolicy` body |
| Name `name` | text field | required | — | max length 150 | — | — | `setSlaPolicy` body |
| Priority `priority` | text field | optional | — | max length 20 | — | — | `setSlaPolicy` body |
| First response minutes `firstResponseMinutes` | number field (minutes) | optional | — | — | — | — | `setSlaPolicy` body |
| Resolution minutes `resolutionMinutes` | number field (minutes) | optional | — | — | — | — | `setSlaPolicy` body |
| Escalation minutes `escalationMinutes` | number field (minutes) | optional | — | — | — | — | `setSlaPolicy` body |
| Business hours only `businessHoursOnly` | toggle | required | — | — | — | — | `setSlaPolicy` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setSlaPolicy` body |
| Created at `createdAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setSlaPolicy` body |
| Updated at `updatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setSlaPolicy` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue operating hours (primary button) | navigation or local | — | — | — | — |
| Save SLA policy (secondary button) | `setSlaPolicy` PUT `/sla-policies` | MarketingSlaPolicy | MarketingSlaPolicy | — | opens modal first |

**Data it reads**: `listSlaPolicyService` (onLoad, SLA Policy & Service-Level Management)

**Where the user goes next**

- → `SUP-019` Contact Center Operations Command Center: *Returns to the board's landing screen*; calls `listSlaPolicyService`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sla policy service-level configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sla policy service-level untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sla policy service-level configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy: Complaint resolution 24 business hours - 94% met this month - 3 forecast to breach today
```

#### Permissions

- `listSlaPolicyService` → `CASE_VIEW` (read) · staff
- `setSlaPolicy` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- SLA policies per case type; agent workload view allows reassigning cases to balance load; unresolved cases can be escalated further from case monitoring. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-546)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-022` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-022`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 6: Works in SLA Policy & Service-Level Management → Define and monitor service-level commitments for different customer-service scenarios.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-022?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue operating hours, Save SLA policy.
- [ ] Every transition is wired: `SUP-019`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-023` Agent Workload, Availability & Workforce Control

**Give supervisors visibility and control over active customer-service resources.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `caseId` (navigation) |
| Route | `/support/agent-workload-availability-workforce-control-sup-023` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Supervisors see every agent's status, skills, languages, queues and live workload, and rebalance by reassigning cases.

**Fixed on main** (the package already carries these; draw what it says): Read-only; reassignment (updateCase) is not declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Queue | picker: choose a queue | — | — | `listAgentWorkloadAvailability` ?queueId |
| Team | text field | — | max length 100 | `listAgentWorkloadAvailability` ?team |
| Status | select | — | Available · Busy · On call · Chatting · After call work · Break · Training · Offline | `listAgentWorkloadAvailability` ?status |
| Skill | text field | — | max length 60 | `listAgentWorkloadAvailability` ?skill |
| Language | text field | — | max length 10 | `listAgentWorkloadAvailability` ?language |

**Form: Reassign** (modal, opened by *Reassign*; *Reassign* calls `updateCase`, *Cancel* sends nothing)

**Collects what `updateCase` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | — | `updateCase` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent | — | — | `updateCase` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Resolution note `resolutionNote` | text area | optional | — | max length 2000 | — | — | `updateCase` body |

Errors to draw in the form: 400 Resolving without a resolution note

#### Outputs: what the screen shows and produces

**Shown**

**Every agent workload availability** (data table, from `listAgentWorkloadAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Agent name | text | The agent's display name. |
| Team | text | — |
| Skills | list or chips (count when long) | — |
| Languages | list or chips (count when long) | — |
| Status | chip: Available, Busy, On call, Chatting, After call work, Break… | — |
| Active cases | 1,234 | — |
| Chats | 1,234 | Conversations the agent holds now. |
| Calls | 1,234 | Voice conversations in progress (0 or 1). |
| Queue name | text | — |
| Sla risk cases | 1,234 | The agent's open cases at risk or breached. |
| Average handle seconds | 1,234 | — |
| Resolution rate | 12.5% | Cases resolved over cases handled. |
| Utilization | 1,234.5 | Active cases and conversations over `maxConcurrentCases`; above 1 means overloaded. |

**The selected agent workload availability** (detail panel): The pack groups this record's detail under its own headings: “Authorized supervisors can”, “Resource Management Integration”.

| Shows | Format | Notes |
|---|---|---|
| Agent name | text | The agent's display name. |
| Team | text | — |
| Skills | list or chips (count when long) | — |
| Languages | list or chips (count when long) | — |
| Status | chip: Available, Busy, On call, Chatting, After call work, Break… | — |
| Active cases | 1,234 | — |
| Chats | 1,234 | Conversations the agent holds now. |
| Calls | 1,234 | Voice conversations in progress (0 or 1). |
| Queue name | text | — |
| Sla risk cases | 1,234 | The agent's open cases at risk or breached. |
| Average handle seconds | 1,234 | — |
| Resolution rate | 12.5% | Cases resolved over cases handled. |
| Utilization | 1,234.5 | Active cases and conversations over `maxConcurrentCases`; above 1 means overloaded. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Reassign (secondary button) | `updateCase` PATCH `/cases/{caseId}` | inline | Case | 400 Resolving without a resolution note | opens modal first |

**Data it reads**: `listAgentWorkloadAvailability` (onLoad, Agent Workload, Availability & Workforce Control)

**Where the user goes next**

- → `SUP-019` Contact Center Operations Command Center: *Returns to the board's landing screen*; calls `listAgentWorkloadAvailability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The agent workload availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the agent workload availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No agent workload availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the agent workload availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Resolving without a resolution note |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
agents:
- Aisha Rahman - Available - 3/3
- Joseph Mathew - Busy - 5/5
- Noor Hassan - Away (lunch)
```

#### Permissions

- `listAgentWorkloadAvailability` → `CASE_VIEW` (read) · staff
- `updateCase` → `CASE_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.4 | Case Workflow Management | Marketing & CRM | CONTRACTED | `updateCase` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- SLA policies per case type; agent workload view allows reassigning cases to balance load; unresolved cases can be escalated further from case monitoring. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-546)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-023` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-023`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 8: Works in Agent Workload, Availability & Workforce Control → Give supervisors visibility and control over active customer-service resources.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Reassign.
- [ ] Every transition is wired: `SUP-019`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-024` Escalation & Critical Case Monitor

**Provide supervisors with one workspace for cases requiring elevated attention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/escalation-critical-case-monitor-sup-024` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** One workspace for cases needing elevated attention: open escalations with level and reason, and suspected major incidents (many similar cases at once).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Escalation type | select | — | Vip · Financial · Event day · Management · Technical · Other | `listEscalationCriticalCase` ?escalationType |
| Priority | radio group | — | Low · Normal · High · Urgent | `listEscalationCriticalCase` ?priority |
| Event | picker: choose an event | — | — | `listEscalationCriticalCase` ?eventId |
| Breached only | toggle | — | — | `listEscalationCriticalCase` ?breachedOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every escalation critical case** (data table, from `listEscalationCriticalCase`)

| Shows | Format | Notes |
|---|---|---|
| Case number | text | — |
| Customer name | text | Resolved from `pii.subject`; null unless the caller holds `GUEST_VIEW_PII`. |
| Reason | text | The reason given to `escalateCase`, or `SLA breached` for an automatic escalation. |
| Priority | chip: Low, Normal, High, Urgent | — |
| Transaction value | AED 1,234.50 | The related order's total, when the case has one. |
| Event name | text | — |
| Assigned to principal | the name it points at, never the id | — |
| Escalated to principal | the name it points at, never the id | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Sla due at | 1 Oct 2026, 14:30 | — |
| Is sla breached | yes / no (icon or chip) | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |

**The selected escalation critical case** (detail panel): The pack groups this record's detail under its own headings: “Major Issue Detection”, “Potential Major Incident”.

| Shows | Format | Notes |
|---|---|---|
| Case number | text | — |
| Customer name | text | Resolved from `pii.subject`; null unless the caller holds `GUEST_VIEW_PII`. |
| Reason | text | The reason given to `escalateCase`, or `SLA breached` for an automatic escalation. |
| Priority | chip: Low, Normal, High, Urgent | — |
| Transaction value | AED 1,234.50 | The related order's total, when the case has one. |
| Event name | text | — |
| Assigned to principal | the name it points at, never the id | — |
| Escalated to principal | the name it points at, never the id | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Sla due at | 1 Oct 2026, 14:30 | — |
| Is sla breached | yes / no (icon or chip) | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |

**Data it reads**: `listEscalationCriticalCase` (onLoad, Escalation & Critical Case Monitor)

**Where the user goes next**

- → `SUP-019` Contact Center Operations Command Center: *Returns to the board's landing screen*; calls `listEscalationCriticalCase`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The escalation critical case list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the escalation critical case untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No escalation critical case yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the escalation critical case are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
incident: 14 cases in 30 min - "Payment failed at Gate 2 kiosks" - suspected major incident
```

#### Permissions

- `listEscalationCriticalCase` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- SLA policies per case type; agent workload view allows reassigning cases to balance load; unresolved cases can be escalated further from case monitoring. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-546)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-024` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-024`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 10: Works in Escalation & Critical Case Monitor → Provide supervisors with one workspace for cases requiring elevated attention.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SUP-019`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-025` Quality Management & Agent Evaluation

**Measure whether customer-service interactions meet TICVAI's defined service-quality standards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/quality-management-agent-evaluation-sup-025` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Case. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Whether interactions meet the service standard: evaluations per call, chat, email, WhatsApp thread or case, scored on resolution time and outcome against the SLA, with coaching notes.

**Known correction pending (do not draw the wrong version)**

- **The primary button is labelled "Case".** Why: Meaningless label; the act is Evaluate interaction. *(source: screens/P12-support-agent-console.yaml#SUP-025; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Agent principal | picker: choose an agent principal | — | — | `listQualityAgentEvaluation` ?agentPrincipalId |
| Evaluator principal | picker: choose an evaluator principal | — | — | `listQualityAgentEvaluation` ?evaluatorPrincipalId |
| Source type | select | — | Call · Chat · Email · Whatsapp · Case · Complaint | `listQualityAgentEvaluation` ?sourceType |
| Status | segmented control | — | Draft · Scored · Acknowledged | `listQualityAgentEvaluation` ?status |
| Critical failure only | toggle | — | — | `listQualityAgentEvaluation` ?criticalFailureOnly |
| From | date and time picker | — | — | `listQualityAgentEvaluation` ?from |
| To | date and time picker | — | — | `listQualityAgentEvaluation` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Case (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listQualityAgentEvaluation` (onLoad, Quality Management & Agent Evaluation)

**Where the user goes next**

- → `SUP-019` Contact Center Operations Command Center: *Returns to the board's landing screen*; calls `listQualityAgentEvaluation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The quality agent evaluation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the quality agent evaluation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No quality agent evaluation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the quality agent evaluation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
evaluation: Aisha Rahman - WhatsApp CA-1120 - 92/100 - coaching none
```

#### Permissions

- `listQualityAgentEvaluation` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Supervisor dashboard: case volume by category (general support, refund, ticketing, membership) and status, quality scores per agent (resolution time and outcome vs SLA), customer-satisfaction results and week-over-week case-volume trends. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-544)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-025` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-025`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 12: Works in Quality Management & Agent Evaluation → Measure whether customer-service interactions meet TICVAI's defined service-quality standards.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-025?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Case.
- [ ] Every transition is wired: `SUP-019`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-026` Customer Satisfaction, Feedback & Voice of Customer

**Measure customer perception of TICVAI's support experience and identify recurring service problems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/customer-satisfaction-feedback-voice-of-customer-sup-026` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Service Rating, NPS where used, Direct Customer Comment. Each needs an operation, or needs removing from the …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Perception of the support experience: CSAT, response rate, positive, neutral and negative share, complaints, repeat contact, effort; recurring problems with AI themes linked to comments.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Source | select | — | Csat survey · Service rating · Nps · Post case survey · Complaint · App feedback · Web feedback · Direct comment | `listCustomerSatisfactionFeedback` ?source |
| Group by | select | Channel | Agent · Team · Venue · Product · Event · Case kind · Channel · Customer type · Language | `listCustomerSatisfactionFeedback` ?groupBy |
| Event | picker: choose an event | — | — | `listCustomerSatisfactionFeedback` ?eventId |
| Product | picker: choose a product | — | — | `listCustomerSatisfactionFeedback` ?productId |
| Agent principal | picker: choose an agent principal | — | — | `listCustomerSatisfactionFeedback` ?agentPrincipalId |
| Sentiment | segmented control | — | Positive · Neutral · Negative | `listCustomerSatisfactionFeedback` ?sentiment |
| From | date and time picker | — | — | `listCustomerSatisfactionFeedback` ?from |
| To | date and time picker | — | — | `listCustomerSatisfactionFeedback` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**CSAT** (metric tile)

**Survey Response Rate** (metric tile)

**Positive %** (metric tile)

**Neutral %** (metric tile)

**Negative %** (metric tile)

**Complaints** (metric tile)

**Repeat Contact Rate** (metric tile)

**Customer Effort where measured** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Service Rating (primary button) | navigation or local | — | — | — | — |
| NPS where used (secondary button) | navigation or local | — | — | — | — |
| Direct Customer Comment (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCustomerSatisfactionFeedback` (onLoad, Customer Satisfaction, Feedback & Voice of Customer)

**Where the user goes next**

- → `SUP-019` Contact Center Operations Command Center: *Returns to the board's landing screen*; calls `listCustomerSatisfactionFeedback`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer satisfaction feedback list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer satisfaction feedback untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer satisfaction feedback yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer satisfaction feedback are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  csat: 4.4
  responseRate: 22%
  negative: 9%
  repeatContact: 6%
```

#### Permissions

- `listCustomerSatisfactionFeedback` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.5.11 | AI Issue Detection | Marketing & CRM | CONTRACTED | `listCustomerSatisfactionFeedback` |
| 22.5.12 | AI Review Summarization | Marketing & CRM | CONTRACTED | `listCustomerSatisfactionFeedback` |
| 22.7.18 | AI Insight Generation | Marketing & CRM | CONTRACTED | `listCustomerSatisfactionFeedback` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Supervisor dashboard: case volume by category (general support, refund, ticketing, membership) and status, quality scores per agent (resolution time and outcome vs SLA), customer-satisfaction results and week-over-week case-volume trends. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-544)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-026` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-026`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 14: Works in Customer Satisfaction, Feedback & Voice of Customer → Measure customer perception of TICVAI's support experience and identify recurring service problems.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-026?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Service Rating, NPS where used, Direct Customer Comment.
- [ ] Every transition is wired: `SUP-019`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-027` Service Analytics & Root-Cause Intelligence

**Provide comprehensive analytics explaining why customers contact TICVAI and what is driving service demand.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Analyze; Compare) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/service-analytics-root-cause-intelligence-sup-027` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Why guests contact the venue and what drives demand: volume, response and resolution times, first-contact resolution, reopen and escalation rates, SLA compliance, refund requests and complaint rate, compared over periods, with contributing drivers.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Event | picker: choose an event | — | — | `listServiceRootCause` ?eventId |
| Product | picker: choose a product | — | — | `listServiceRootCause` ?productId |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listServiceRootCause` ?channel |
| From | date and time picker | — | — | `listServiceRootCause` ?from |
| To | date and time picker | — | — | `listServiceRootCause` ?to |
| Compare | select | Previous week | Previous day · Previous week · Previous month · Event · Venue · Product | `listServiceRootCause` ?compare |
| Compare | picker: choose a compare | — | The event, venue or product to compare with; required when `compare` is `event`, `venue` or `product`. | `listServiceRootCause` ?compareId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Contact Volume** (metric tile)

**Cases** (metric tile)

**First Response Time** (metric tile)

**Resolution Time** (metric tile)

**First Contact Resolution** (metric tile)

**Reopen Rate** (metric tile)

**Escalation Rate** (metric tile)

**SLA Compliance** (metric tile)

**Cost per Case where available** (metric tile)

**CSAT** (metric tile)

**Refund Requests** (metric tile)

**Complaint Rate** (metric tile)

**Comparison** (data table, from `listServiceRootCause`): One comparison panel in place of the pack's six tiles (Today vs Yesterday, Week vs Week, Month vs Month, Event vs Event, Venue vs Venue, Product vs Product). The compare selector sends `?compare=` (previousDay, previousWeek, previousMonth, event, venue, product) and `?compareId=` to `listServiceRootCause`; the basis shown is `comparison.basis`.

| Shows | Format | Notes |
|---|---|---|
| Kpi | text | The KPI's property name above, e.g. `contactVolume`. |
| Current | 1,234.5 | — |
| Previous | 1,234.5 | — |
| Change rate | 12.5% | — |

**Data it reads**: `listServiceRootCause` (onLoad, Service Analytics & Root-Cause Intelligence)

**Where the user goes next**

- → `SUP-019` Contact Center Operations Command Center: *Returns to the board's landing screen*; calls `listServiceRootCause`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The service analytics root-cause list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the service analytics root-cause untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No service analytics root-cause yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the service analytics root-cause are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
driver: Reschedule requests up 40% week on week after rain forecast
```

#### Permissions

- `listServiceRootCause` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-027` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-027`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 16: Works in Service Analytics & Root-Cause Intelligence → Provide comprehensive analytics explaining why customers contact TICVAI and what is driving service demand.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SUP-019`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-028` AI Contact Center Intelligence & Automation Studio

**Create the management-level AI intelligence layer for Customer Service. This is different from 10.1.10 AI Customer Service Copilot. Board 1 Copilot = helps one agent resolve one case. Board 2 AI Intelligence = improves the entire service operation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Forecast) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/ai-contact-center-intelligence-automation-studio-sup-028` |

**Known gaps.** **AI Contact Center Intelligence & Automation Studio declares no operation that writes anything** — its only declared call is `listContactAutomation`, a read. The name promises authoring and the …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The management AI layer for customer service: demand forecast, recommendations and governed automations for the whole operation (distinct from the copilot that helps one agent with one case). Automations are approved by a person.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Horizon hours | number field (hours) | 24 | min 1; max 168 | `listContactAutomation` ?horizonHours |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every contact intelligence automation** (data table, from `listContactAutomation`)

| Shows | Format | Notes |
|---|---|---|
| Contact volume | 1,234 | — |
| Queue demand | list or chips (count when long) | — |
| Required agents | 1,234 | — |
| Sla risk cases | 1,234 | Cases expected to breach. |
| Expected complaints | 1,234 | — |
| Event day support demand | 1,234 | Expected cases tied to events on the day. |

**The selected contact intelligence automation** (detail panel): The pack groups this record's detail under its own headings: “Analyze governed information from”, “Workforce”, “Self-Service”, “Product Improvement”, “Operational Improvement”, “Incident Detection”.

| Shows | Format | Notes |
|---|---|---|
| Contact volume | 1,234 | — |
| Queue demand | list or chips (count when long) | — |
| Required agents | 1,234 | — |
| Sla risk cases | 1,234 | Cases expected to breach. |
| Expected complaints | 1,234 | — |
| Event day support demand | 1,234 | Expected cases tied to events on the day. |

**Data it reads**: `listContactAutomation` (onLoad, AI Contact Center Intelligence & Automation Studio)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The contact intelligence automation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the contact intelligence automation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No contact intelligence automation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the contact intelligence automation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
recommendation: Add 2 Arabic agents Saturday 14:00-18:00 - forecast 120 contacts (AI, model cs-demand-v1)
```

#### Permissions

- `listContactAutomation` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-028` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS43 Customer Service Board 2.dc.html#sup-028`
- Workshop pack: Customer Service_Reference.pdf board 2
- Flow F135 *Customer Service board 2: Contact Center Operations Command Center*, step 18: Works in AI Contact Center Intelligence & Automation Studio → Create the management-level AI intelligence layer for Customer Service. This is different from 10.1.10 AI Customer Service Copilot. Board 1 Copilot = helps one agent resolve one case. Board 2 AI …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-028?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P12 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for operator density.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P12 Venue Support

- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Client support staff log into TICVAI to view and respond to their own tickets/chats (keeps a full audit trail); adapters to clients' own support systems are phase two. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-257)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listAgentWorkloadAvailability": {"method":"GET","path":"/agent-workload-availability","contract":"marketing-crm","summary":"Agent Workload, Availability & Workforce Control","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":"queueId","in":"query","required":false},{"name":"team","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"skill","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCaseCategories": {"method":"GET","path":"/case-categories","contract":"marketing-crm","summary":"List case categories and subcategories","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"parentCategoryId","in":"query","required":false},{"name":"topLevelOnly","in":"query","required":false},{"name":"isActive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listContact": {"method":"GET","path":"/contact","contract":"marketing-crm","summary":"Contact Center Operations Command Center","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"queueId","in":"query","required":false},{"name":"channel","in":"query","required":false}],"requestBody":null,"responds":"ContactCenterOperationsCommandCenterView"},
"listContactAutomation": {"method":"GET","path":"/contact-automation","contract":"marketing-crm","summary":"AI Contact Center Intelligence & Automation Studio","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"horizonHours","in":"query","required":false}],"requestBody":null,"responds":"AiContactCenterIntelligenceAutomationStudioView"},
"listCustomerSatisfactionFeedback": {"method":"GET","path":"/customer-satisfaction-feedback","contract":"marketing-crm","summary":"Customer Satisfaction, Feedback & Voice of Customer","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"source","in":"query","required":false},{"name":"groupBy","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"agentPrincipalId","in":"query","required":false},{"name":"sentiment","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"CustomerSatisfactionFeedbackVoiceOfCustomerView"},
"listEscalationCriticalCase": {"method":"GET","path":"/escalation-critical-case","contract":"marketing-crm","summary":"Escalation & Critical Case Monitor","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":"escalationType","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"breachedOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQualityAgentEvaluation": {"method":"GET","path":"/quality-agent-evaluation","contract":"marketing-crm","summary":"Quality Management & Agent Evaluation","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"agentPrincipalId","in":"query","required":false},{"name":"evaluatorPrincipalId","in":"query","required":false},{"name":"sourceType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"criticalFailureOnly","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listServiceQueues": {"method":"GET","path":"/service-queues","contract":"marketing-crm","summary":"List customer-service queues","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"isActive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listServiceRootCause": {"method":"GET","path":"/service-root-cause","contract":"marketing-crm","summary":"Service Analytics & Root-Cause Intelligence","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"compare","in":"query","required":false},{"name":"compareId","in":"query","required":false}],"requestBody":null,"responds":"ServiceAnalyticsRootCauseIntelligenceView"},
"listSlaPolicyService": {"method":"GET","path":"/sla-policy-service","contract":"marketing-crm","summary":"SLA Policy & Service-Level Management","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"slaPolicyId","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":"kind","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"queueId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"SlaPolicyServiceLevelManagementView"},
"setIntelligentRoutingSkill": {"method":"PUT","path":"/intelligent-routing-skill","contract":"marketing-crm","summary":"Create or change a case routing rule","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IntelligentRoutingSkillsAssignmentEngineInput","responds":"IntelligentRoutingSkillsAssignmentEngineView"},
"setServiceQueueDefinition": {"method":"PUT","path":"/service-queues","contract":"marketing-crm","summary":"Create or change a customer-service queue","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ServiceQueue","responds":"ServiceQueue"},
"setSlaPolicy": {"method":"PUT","path":"/sla-policies","contract":"marketing-crm","summary":"Define an SLA policy","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MarketingSlaPolicy","responds":"MarketingSlaPolicy"},
"updateCase": {"method":"PATCH","path":"/cases/{caseId}","contract":"marketing-crm","summary":"Assign, reprioritise or resolve a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AgentWorkloadAvailabilityWorkforceControlView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.agent_service_profile (new), marketing.agent_availability, marketing.case, marketing.conversation, marketing.service_queue (new) and workforce.shift","description":"One agent's live status and workload. Rates are over the period since the agent's current shift started, or the venue's current day when no shift is rostered.","required":["principalId","agentName","status","activeCases"],"properties":{"principalId":{"type":"string","format":"uuid"},"agentName":{"type":"string","description":"The agent's display name."},"team":{"type":"string","nullable":true},"skills":{"type":"array","items":{"type":"string"}},"languages":{"type":"array","items":{"type":"string"}},"status":{"type":"string","enum":["available","busy","onCall","chatting","afterCallWork","break","training","offline"]},"activeCases":{"type":"integer","minimum":0},"chats":{"type":"integer","minimum":0,"description":"Conversations the agent holds now."},"calls":{"type":"integer","minimum":0,"description":"Voice conversations in progress (0 or 1)."},"queues":{"type":"array","items":{"type":"object","required":["queueId","queueName"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"type":"string"}}}},"slaRiskCases":{"type":"integer","minimum":0,"description":"The agent's open cases at risk or breached."},"averageHandleSeconds":{"type":"integer","minimum":0,"nullable":true},"resolutionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Cases resolved over cases handled."},"utilization":{"type":"number","minimum":0,"description":"Active cases and conversations over `maxConcurrentCases`; above 1 means overloaded."},"workloadBand":{"type":"string","enum":["available","normal","overloaded"],"description":"`overloaded` at utilization 0.9 or above, `available` below 0.5."},"availabilityExpiresAt":{"type":"string","format":"date-time","nullable":true}}},
"AiContactCenterIntelligenceAutomationStudioView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.contact_automation (new), with the forecast and recommendations computed over marketing.case, marketing.conversation and marketing.agent_availability","description":"The studio's forecast, recommendations and automations for the filters given.","required":["forecast","recommendations","automations"],"properties":{"forecast":{"type":"object","nullable":true,"description":"Expected over the next `horizonHours`.","properties":{"contactVolume":{"type":"integer","minimum":0},"queueDemand":{"type":"array","items":{"type":"object","required":["queueId","expectedCases"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"type":"string"},"expectedCases":{"type":"integer","minimum":0},"requiredAgents":{"type":"integer","minimum":0}}}},"requiredAgents":{"type":"integer","minimum":0},"slaRiskCases":{"type":"integer","minimum":0,"description":"Cases expected to breach."},"expectedComplaints":{"type":"integer","minimum":0},"eventDaySupportDemand":{"type":"integer","minimum":0,"description":"Expected cases tied to events on the day."},"generatedAt":{"type":"string","format":"date-time"}}},"recommendations":{"type":"array","maxItems":20,"items":{"type":"object","required":["category","text"],"properties":{"category":{"type":"string","enum":["workforce","selfService","productImprovement","operationalImprovement","incidentDetection"]},"text":{"type":"string","maxLength":500},"evidence":{"type":"string","maxLength":500,"nullable":true},"confidence":{"type":"number","minimum":0,"maximum":1}}}},"automations":{"type":"array","maxItems":200,"items":{"$ref":"#/components/schemas/ContactAutomation"}}}},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseCategory": {"type":"object","x-ticvai-persistence":"marketing.case_category","description":"**The venue's case taxonomy**: categories and, under them, subcategories (`parentCategoryId`). `Case.categoryId` and the routing rules' `match.categoryIds` point here; `createCaseClassificationIntelligent` recommends one. Maintained by `setCaseCategoryDefinition`, read by `listCaseCategories` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n","required":["id","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60},"name":{"type":"string","maxLength":150},"parentCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a subcategory; null on a top-level category."},"defaultPriority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"nullable":true,"description":"The priority a case in this category starts at before routing factors apply."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"ContactAutomation": {"type":"object","x-ticvai-persistence":"marketing.contact_automation","description":"One governed contact-centre automation (pack 10.2.10 AI Governance).","required":["code","name","level","trigger","allowedActions","confidenceThreshold","onException","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60,"description":"The natural key, e.g. `autoResendValidTicket`."},"name":{"type":"string","maxLength":150},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"level":{"type":"string","enum":["recommendOnly","agentConfirmation","supervisorGoverned","fullyAutomated"]},"trigger":{"type":"object","required":["event"],"properties":{"event":{"type":"string","enum":["caseCreated","caseUpdated","conversationMessageReceived","caseClusterDetected"]},"conditions":{"type":"array","maxItems":20,"description":"All must hold.","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","maxLength":100,"description":"e.g. `case.kind`, `ticket.isValid`, `guest.identityVerified`, `cluster.caseCount`."},"operator":{"type":"string","enum":["eq","neq","in","gt","gte","lt","lte","exists"]},"value":{"description":"Any JSON value; omitted for `exists`."}}}},"windowMinutes":{"type":"integer","minimum":1,"nullable":true,"description":"For cluster triggers, e.g. 5 cases in 10 minutes."}}},"scope":{"type":"object","description":"Where it applies; empty lists mean everywhere in the scope path.","properties":{"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"queueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}}}},"allowedActions":{"type":"array","minItems":1,"items":{"type":"string","enum":["resendTicket","resolveCase","createCase","assignQueue","setPriority","sendMessage","notifySupervisor","flagPotentialIncident"]}},"confidenceThreshold":{"type":"number","minimum":0,"maximum":1},"onException":{"type":"string","enum":["leaveForAgent","routeToQueue","notifySupervisor"]},"exceptionQueueId":{"type":"string","format":"uuid","nullable":true},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"killSwitch":{"type":"boolean","default":false},"status":{"type":"string","enum":["draft","approved","active","paused","retired"]},"version":{"type":"integer","minimum":1,"readOnly":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"approvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"lastSimulation":{"type":"object","nullable":true,"readOnly":true,"properties":{"simulatedVersion":{"type":"integer","minimum":1},"periodStart":{"type":"string","format":"date-time"},"periodEnd":{"type":"string","format":"date-time"},"casesMatched":{"type":"integer","minimum":0},"casesResolvable":{"type":"integer","minimum":0},"agentHoursSaved":{"type":"number","minimum":0},"estimatedConfidence":{"type":"number","minimum":0,"maximum":1}}},"executionsLast30Days":{"type":"integer","minimum":0,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ContactCenterOperationsCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case, marketing.conversation, marketing.agent_availability, marketing.sla_policy, marketing.form_submission (post-case CSAT surveys) and marketing.service_queue (new)","description":"The contact centre's live figures for the filters given. Counts are of cases unless the name says otherwise; durations are averages over cases first responded to or resolved today.","required":["casesToday","openCases","unassignedCases","customersWaiting","criticalCases","slaAtRisk","slaBreached","channels","queues"],"properties":{"casesToday":{"type":"integer","minimum":0,"description":"Cases created today."},"openCases":{"type":"integer","minimum":0,"description":"Cases not `resolved` or `closed`."},"unassignedCases":{"type":"integer","minimum":0},"customersWaiting":{"type":"integer","minimum":0,"description":"Unclaimed conversations waiting in a queue now."},"criticalCases":{"type":"integer","minimum":0,"description":"Open cases at priority `urgent`."},"slaAtRisk":{"type":"integer","minimum":0,"description":"Open cases that have used 75% or more of their SLA and have not breached."},"slaBreached":{"type":"integer","minimum":0,"description":"Open cases past their SLA (`Case.isSlaBreached`)."},"casesResolvedToday":{"type":"integer","minimum":0},"averageFirstResponseSeconds":{"type":"integer","minimum":0,"nullable":true},"averageResolutionSeconds":{"type":"integer","minimum":0,"nullable":true},"firstContactResolutionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Share of cases resolved today with no reopen and no transfer."},"csat":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Share of today's post-case CSAT responses that are satisfied (top two points of the scale). Null when there are none."},"activeAgents":{"type":"integer","minimum":0,"description":"Agents whose availability is not `offline`."},"agentUtilization":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Active cases and conversations held, over the active agents' combined capacity."},"channels":{"type":"array","description":"Workload per contact channel, from `Case.channel` and `Conversation.channel`.","items":{"type":"object","required":["channel","openCases","waiting"],"properties":{"channel":{"type":"string","enum":["email","phone","liveChat","whatsapp","webForm","mobileApp","b2cPortal","social","frontDesk"]},"openCases":{"type":"integer","minimum":0},"waiting":{"type":"integer","minimum":0},"slaAtRisk":{"type":"integer","minimum":0},"averageFirstResponseSeconds":{"type":"integer","minimum":0,"nullable":true}}}},"queues":{"type":"array","description":"Queue health, worst first.","items":{"type":"object","required":["queueId","queueName","openCases","waiting","health"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"type":"string"},"openCases":{"type":"integer","minimum":0},"waiting":{"type":"integer","minimum":0},"slaAtRisk":{"type":"integer","minimum":0},"agentsOnline":{"type":"integer","minimum":0},"health":{"type":"string","enum":["healthy","warning","critical"],"description":"`critical` when any case in the queue has breached or waiting exceeds the queue's overflow threshold; `warning` when any is at risk."}}}},"operationalFeed":{"type":"array","maxItems":50,"description":"Notable changes in the last hour, newest first (queue surges, cases nearing breach, a channel over its response target).","items":{"type":"object","required":["occurredAt","severity","message"],"properties":{"occurredAt":{"type":"string","format":"date-time"},"severity":{"type":"string","enum":["info","warning","critical"]},"message":{"type":"string","maxLength":300},"queueId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","nullable":true}}}},"serviceRiskSummary":{"type":"object","nullable":true,"description":"The AI operational summary; null when AI is disabled for the tenant. Advisory only, it changes nothing.","required":["riskLevel","summary","generatedAt"],"properties":{"riskLevel":{"type":"string","enum":["low","medium","high","critical"]},"summary":{"type":"string","maxLength":1000},"recommendations":{"type":"array","maxItems":5,"items":{"type":"string","maxLength":300}},"generatedAt":{"type":"string","format":"date-time"}}}}},
"CustomerSatisfactionFeedbackVoiceOfCustomerView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_submission and marketing.form_definition (survey forms), marketing.review, marketing.case and marketing.feedback_classification (new, the AI sentiment and topic per feedback item)","description":"Voice-of-customer figures for the filters given. Rates are shares of feedback items in the period.","required":["responses","breakdown","comments"],"properties":{"responses":{"type":"integer","minimum":0,"description":"Feedback items in the period."},"csat":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Share of CSAT answers in the top two points of the scale."},"nps":{"type":"integer","minimum":-100,"maximum":100,"nullable":true,"description":"Null where the tenant runs no NPS survey."},"surveyResponseRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Surveys answered over surveys sent."},"positiveRate":{"type":"number","minimum":0,"maximum":1},"neutralRate":{"type":"number","minimum":0,"maximum":1},"negativeRate":{"type":"number","minimum":0,"maximum":1},"complaints":{"type":"integer","minimum":0},"repeatContactRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Customers with a second case within 7 days of the first, over customers with a case."},"customerEffortScore":{"type":"number","minimum":1,"maximum":7,"nullable":true,"description":"Mean CES answer; null where effort is not measured."},"csatChangeRate":{"type":"number","nullable":true,"description":"Relative change in `csat` against the previous period of equal length."},"aiSummary":{"type":"object","nullable":true,"description":"AI-derived narrative of the feedback matching the filters (22.5.12; 29 September, build pass, group G2), labelled as AI on screen. Null when AI is off or fewer than 5 items match.","required":["text","basedOnCount","modelVersion"],"properties":{"text":{"type":"string","maxLength":2000},"basedOnCount":{"type":"integer","minimum":0,"description":"The feedback items the summary was written from."},"modelVersion":{"type":"string","maxLength":60},"generatedAt":{"type":"string","format":"date-time"}}},"breakdown":{"type":"array","description":"One row per value of the `groupBy` dimension, most responses first.","items":{"type":"object","required":["key","label","responses"],"properties":{"key":{"type":"string","description":"The id or enum value of the group."},"label":{"type":"string"},"responses":{"type":"integer","minimum":0},"csat":{"type":"number","minimum":0,"maximum":1,"nullable":true},"negativeRate":{"type":"number","minimum":0,"maximum":1}}}},"themes":{"type":"array","maxItems":20,"description":"AI topic themes, largest share first. Empty when AI is disabled for the tenant.","items":{"type":"object","required":["topic","shareRate"],"properties":{"topic":{"type":"string","maxLength":100},"shareRate":{"type":"number","minimum":0,"maximum":1},"negativeRate":{"type":"number","minimum":0,"maximum":1},"changeRate":{"type":"number","nullable":true,"description":"Relative change in the theme's volume against the previous period."}}}},"trendAlerts":{"type":"array","maxItems":10,"items":{"type":"string","maxLength":300},"description":"AI-detected shifts, e.g. negative feedback on ticket delivery rising after a release."},"comments":{"type":"array","maxItems":50,"description":"The 50 latest comments with text, newest first.","items":{"type":"object","required":["feedbackId","source","receivedAt"],"properties":{"feedbackId":{"type":"string","format":"uuid"},"source":{"type":"string","enum":["csatSurvey","serviceRating","nps","postCaseSurvey","complaint","appFeedback","webFeedback","directComment"]},"receivedAt":{"type":"string","format":"date-time"},"comment":{"type":"string","maxLength":4000,"nullable":true},"rating":{"type":"number","nullable":true,"description":"The answer on its survey's own scale."},"ratingScale":{"type":"string","nullable":true,"enum":["nps","csat","ces","likert5","likert7","stars"]},"sentiment":{"type":"string","nullable":true,"enum":["positive","neutral","negative"]},"topic":{"type":"string","nullable":true},"caseId":{"type":"string","format":"uuid","nullable":true},"agentPrincipalId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true},"followUpCaseId":{"type":"string","format":"uuid","nullable":true}}}}}},
"EscalationCriticalCaseMonitorView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case, marketing.case_escalation (new, one row per escalateCase call) and the related order in orders","description":"One open escalated case, as of its latest escalation.","required":["caseId","caseNumber","reason","escalationType","priority","escalatedAt","status"],"properties":{"caseId":{"type":"string","format":"uuid"},"caseNumber":{"type":"string"},"subjectId":{"type":"string","format":"uuid","nullable":true},"customerName":{"type":"string","nullable":true,"description":"Resolved from `pii.subject`; null unless the caller holds `GUEST_VIEW_PII`."},"reason":{"type":"string","description":"The reason given to `escalateCase`, or `SLA breached` for an automatic escalation."},"reasonCategory":{"type":"string","nullable":true,"enum":["slaRisk","customerComplaint","repeatedContact","highValue","refundException","operationalFailure","systemFailure","legalCompliance","vipCustomer","supervisorRequested","other"]},"escalationType":{"type":"string","enum":["vip","financial","eventDay","management","technical","other"],"description":"`vip` for a VIP-tier customer, `financial` for a refund or high-value order, `eventDay` when the case's event is today, `management` when escalated to a manager, `technical` for a technical category; the first that applies, in that order."},"priority":{"$ref":"#/components/schemas/CasePriority"},"transactionValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"The related order's total, when the case has one."},"eventId":{"type":"string","format":"uuid","nullable":true},"eventName":{"type":"string","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"escalatedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"escalatedAt":{"type":"string","format":"date-time"},"escalationCount":{"type":"integer","minimum":1},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean"},"status":{"$ref":"#/components/schemas/CaseStatus"}}},
"IntelligentRoutingSkillsAssignmentEngineInput": {"type":"object","x-ticvai-persistence":"marketing.case_routing_rule","description":"One case routing rule (pack 10.2.3). Empty match lists match everything; all non-empty lists must match.","required":["code","name","strategy","rank","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60,"description":"The natural key, e.g. `eventDayArabic`."},"name":{"type":"string","maxLength":150},"rank":{"type":"integer","minimum":1,"description":"Lower is tried first."},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The queue this rule routes into; null routes straight to an agent."},"match":{"type":"object","properties":{"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Case categories and subcategories (`Case.categoryId`)."},"kinds":{"type":"array","items":{"$ref":"#/components/schemas/CaseKind"}},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"customerLanguages":{"type":"array","items":{"type":"string","maxLength":10},"description":"BCP-47 tags, e.g. `ar`, `en`."},"customerTypes":{"type":"array","items":{"type":"string","enum":["individual","member","vip","corporate","group","partner"]}},"membershipTierIds":{"type":"array","items":{"type":"string","format":"uuid"}},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"eventIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"priorities":{"type":"array","items":{"$ref":"#/components/schemas/CasePriority"}},"eventWithinHours":{"type":"integer","minimum":0,"nullable":true,"description":"Event proximity - matches only when the case's event starts within this many hours."}}},"strategy":{"type":"string","enum":["roundRobin","leastBusy","skillBased","priorityBased","languageBased","customerTierBased","aiRecommended"]},"requiredSkills":{"type":"array","items":{"type":"string","maxLength":60},"description":"Skills an agent must hold (`AgentServiceProfile.skills`), e.g. `ticketing`, `refunds`."},"requireLanguageMatch":{"type":"boolean","default":true,"description":"Only agents who speak the customer's language are candidates."},"maxUtilizationRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Agents above this workload are skipped."},"respectSlaCapability":{"type":"boolean","default":true,"description":"Skip agents whose current queue would push the case past its SLA."},"stickyOwnership":{"type":"boolean","default":false,"description":"Prefer the agent who last handled the customer or the reopened case, if available."},"stickyWindowHours":{"type":"integer","minimum":1,"nullable":true},"fallbackQueueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the case goes when no candidate agent is available."},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"IntelligentRoutingSkillsAssignmentEngineView": {"description":"A routing rule as stored, with how often it has matched.","x-ticvai-persistence":"none — the marketing.case_routing_rule (new) row plus a count over marketing.case","allOf":[{"$ref":"#/components/schemas/IntelligentRoutingSkillsAssignmentEngineInput"},{"type":"object","properties":{"matchedLast7Days":{"type":"integer","minimum":0,"readOnly":true},"lastMatchedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}]},
"MarketingSlaPolicy": {"type":"object","x-ticvai-persistence":"marketing.sla_policy","description":"**Taken from the backend workbook, 20 September.** Defines service-level response and resolution targets used by support cases.","required":["code","name","businessHoursOnly","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"scopePath":{"type":"string","nullable":true},"code":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":150},"priority":{"type":"string","maxLength":20,"nullable":true},"firstResponseMinutes":{"type":"integer","nullable":true},"resolutionMinutes":{"type":"integer","nullable":true},"escalationMinutes":{"type":"integer","nullable":true},"businessHoursOnly":{"type":"boolean"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"QualityManagementAgentEvaluationView": {"type":"object","x-ticvai-persistence":"marketing.quality_evaluation","description":"One quality evaluation of one interaction (pack 10.2.7). Resolution time and SLA outcome are read from the case, not entered.","required":["id","agentPrincipalId","sourceType","evaluatedBy","status","criteria"],"properties":{"id":{"type":"string","format":"uuid"},"agentPrincipalId":{"type":"string","format":"uuid"},"evaluatorPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The caller who scored it; null while only the AI has."},"sourceType":{"type":"string","enum":["call","chat","email","whatsapp","case","complaint"]},"caseId":{"type":"string","format":"uuid","nullable":true},"conversationId":{"type":"string","format":"uuid","nullable":true},"evaluatedBy":{"type":"string","enum":["human","ai"]},"status":{"type":"string","enum":["draft","scored","acknowledged"]},"criteria":{"type":"array","maxItems":30,"items":{"type":"object","required":["criterion","score","maxScore"],"properties":{"criterion":{"type":"string","maxLength":60,"description":"The tenant's criterion code; the pack's defaults are `greeting`, `customerVerification`, `understanding`, `accuracy`, `policyCompliance`, `communicationQuality`, `empathy`, `resolution`, `documentation`, `closing`."},"score":{"type":"integer","minimum":0},"maxScore":{"type":"integer","minimum":1},"comment":{"type":"string","maxLength":1000,"nullable":true}}}},"criticalFailures":{"type":"array","items":{"type":"string","enum":["incorrectRefund","privacyViolation","unauthorisedCompensation","incorrectTicketInformation","securityVerificationFailure","other"]}},"overallScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"Criteria score as a percentage; 0 when any critical failure is recorded."},"aiFindings":{"type":"array","readOnly":true,"items":{"type":"object","required":["area","finding"],"properties":{"area":{"type":"string","enum":["policyAdherence","requiredStatements","tone","accuracy","resolutionQuality","missingCaseDocumentation"]},"finding":{"type":"string","maxLength":500},"confidence":{"type":"number","minimum":0,"maximum":1}}}},"feedback":{"type":"string","maxLength":2000,"nullable":true},"coachingActions":{"type":"array","items":{"type":"object","required":["type"],"properties":{"type":{"type":"string","enum":["productTraining","policyTraining","communicationCoaching","systemTraining"]},"note":{"type":"string","maxLength":500,"nullable":true},"dueAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}}},"resolutionSeconds":{"type":"integer","minimum":0,"nullable":true,"readOnly":true},"slaMet":{"type":"boolean","nullable":true,"readOnly":true},"agentComment":{"type":"string","maxLength":1000,"nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"evaluatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ServiceAnalyticsRootCauseIntelligenceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case, marketing.conversation, marketing.form_submission (CSAT) and the related orders and payments","description":"Service analytics for the filters given, with the comparison asked for.","required":["contactVolume","cases","drivers","comparison"],"properties":{"contactVolume":{"type":"integer","minimum":0,"description":"Conversations and cases opened, a conversation that became a case counted once."},"cases":{"type":"integer","minimum":0},"averageFirstResponseSeconds":{"type":"integer","minimum":0,"nullable":true},"averageResolutionSeconds":{"type":"integer","minimum":0,"nullable":true},"firstContactResolutionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"reopenRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"escalationRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"slaComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"costPerCase":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"csat":{"type":"number","minimum":0,"maximum":1,"nullable":true},"refundRequests":{"type":"integer","minimum":0},"complaintRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"comparison":{"type":"object","required":["basis","kpis"],"properties":{"basis":{"type":"string","enum":["previousDay","previousWeek","previousMonth","event","venue","product"]},"compareId":{"type":"string","format":"uuid","nullable":true},"kpis":{"type":"array","items":{"type":"object","required":["kpi"],"properties":{"kpi":{"type":"string","description":"The KPI's property name above, e.g. `contactVolume`."},"current":{"type":"number","nullable":true},"previous":{"type":"number","nullable":true},"changeRate":{"type":"number","nullable":true}}}}}},"drivers":{"type":"array","description":"Contact drivers, most cases first.","items":{"type":"object","required":["driver","cases","shareRate"],"properties":{"driver":{"type":"string","enum":["ticketDelivery","refund","reschedule","paymentFailure","membership","accessIssue","groupBooking","generalInformation","other"]},"cases":{"type":"integer","minimum":0},"shareRate":{"type":"number","minimum":0,"maximum":1},"changeRate":{"type":"number","nullable":true}}}},"rootCauses":{"type":"array","maxItems":20,"description":"Case surges traced to one cause, largest first. Empty when AI is disabled for the tenant.","items":{"type":"object","required":["summary","cases"],"properties":{"summary":{"type":"string","maxLength":500},"driver":{"type":"string","nullable":true},"cases":{"type":"integer","minimum":0},"causeType":{"type":"string","enum":["paymentProvider","event","product","release","incident","venueArea","other"]},"causeRef":{"type":"string","nullable":true,"description":"The id of the provider, event, product or incident, where there is one."},"windowStart":{"type":"string","format":"date-time","nullable":true},"windowEnd":{"type":"string","format":"date-time","nullable":true}}}},"avoidableContacts":{"type":"array","description":"AI estimate of cases that could have been prevented, by remedy.","items":{"type":"object","required":["preventableBy","cases"],"properties":{"preventableBy":{"type":"string","enum":["betterB2cInformation","selfService","productConfiguration","improvedNotifications","technicalFixes","betterTicketDelivery"]},"cases":{"type":"integer","minimum":0},"recommendation":{"type":"string","maxLength":500,"nullable":true}}}}}},
"ServiceQueue": {"type":"object","x-ticvai-persistence":"marketing.service_queue","description":"**A customer-service queue** (e.g. `eventDaySupport`). Cases (`Case.queueId`), routing rules (`queueId`, `fallbackQueueId`) and agents (`AgentAvailability.queueIds`) name it; `listContact` and `listAgentWorkloadAvailability` report per queue. Maintained by `setServiceQueueDefinition`, read by `listServiceQueues` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n","required":["id","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60},"name":{"type":"string","maxLength":150},"overflowWaitSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"The queue's overflow threshold; a case waiting longer marks the queue `critical`."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"SlaPolicyServiceLevelManagementView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case and marketing.sla_policy","description":"SLA performance for the filters given. Counts are of open cases for the state counts and of cases in the period for the averages and the compliance rate.","required":["withinSla","atRisk","breached","byPolicy"],"properties":{"withinSla":{"type":"integer","minimum":0},"atRisk":{"type":"integer","minimum":0},"breached":{"type":"integer","minimum":0},"averageResponseSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Mean time to first response, less paused time."},"averageResolutionSeconds":{"type":"integer","minimum":0,"nullable":true},"slaComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Cases resolved in the period within target, over cases resolved in the period."},"byPolicy":{"type":"array","description":"One row per SLA policy that timed a case in the period, worst compliance first.","items":{"type":"object","required":["slaPolicyId","code","name","withinSla","atRisk","breached"],"properties":{"slaPolicyId":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"firstResponseMinutes":{"type":"integer","nullable":true},"resolutionMinutes":{"type":"integer","nullable":true},"withinSla":{"type":"integer","minimum":0},"atRisk":{"type":"integer","minimum":0},"breached":{"type":"integer","minimum":0},"slaComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true}}}},"forecastBreaches":{"type":"array","maxItems":50,"description":"AI forecast of open cases likely to breach before the static thresholds fire, soonest first. Advisory; empty when AI is disabled for the tenant.","items":{"type":"object","required":["caseCount","horizonMinutes"],"properties":{"queueId":{"type":"string","format":"uuid","nullable":true},"queueName":{"type":"string","nullable":true},"slaPolicyId":{"type":"string","format":"uuid","nullable":true},"caseCount":{"type":"integer","minimum":0},"horizonMinutes":{"type":"integer","minimum":1},"confidence":{"type":"number","minimum":0,"maximum":1}}}}}}
}
```
